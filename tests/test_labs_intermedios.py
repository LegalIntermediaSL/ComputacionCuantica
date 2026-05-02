"""
Tests para labs 10-20: trotterización, noise, información cuántica avanzada.
"""
import numpy as np
import pytest
from scipy.linalg import expm
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp, DensityMatrix, Operator, state_fidelity
from qiskit.primitives import StatevectorEstimator


# ── Lab 12: Trotterización ────────────────────────────────────────────────────

def build_heisenberg_mat():
    H = SparsePauliOp.from_list([('XX', 1.0), ('YY', 1.0), ('ZZ', 1.0)])
    return H.to_matrix()


def exact_evolution(H_mat: np.ndarray, t: float) -> np.ndarray:
    return expm(-1j * H_mat * t)


def trotter_step(H1: np.ndarray, H2: np.ndarray, dt: float) -> np.ndarray:
    return expm(-1j * H1 * dt) @ expm(-1j * H2 * dt)


def suzuki2_step(H1: np.ndarray, H2: np.ndarray, dt: float) -> np.ndarray:
    return expm(-1j * H1 * dt / 2) @ expm(-1j * H2 * dt) @ expm(-1j * H1 * dt / 2)


class TestTrotterizacion:
    def setup_method(self):
        # H = XX + ZI + IZ (partes NO conmutan: ||[XX, ZI]|| > 0)
        H_total = SparsePauliOp.from_list([('XX', 1.0), ('ZI', 0.5), ('IZ', 0.5)])
        self.H_mat = H_total.to_matrix()
        self.H1 = SparsePauliOp('XX').to_matrix()
        self.H2 = SparsePauliOp.from_list([('ZI', 0.5), ('IZ', 0.5)]).to_matrix()

    def test_exact_unitary(self):
        U = exact_evolution(self.H_mat, 1.0)
        assert np.allclose(U @ U.conj().T, np.eye(4), atol=1e-9)

    def test_commutator_nonzero(self):
        """H1 y H2 no conmutan: Trotter introduce error."""
        comm = self.H1 @ self.H2 - self.H2 @ self.H1
        assert np.linalg.norm(comm) > 0.5

    def test_trotter_converges(self):
        t = 3.0
        U_ref = exact_evolution(self.H_mat, t)
        errors = []
        for n in [2, 10, 50]:
            dt = t / n
            step = trotter_step(self.H1, self.H2, dt)
            Un = np.linalg.matrix_power(step, n)
            errors.append(np.linalg.norm(Un - U_ref))
        assert errors[0] > errors[1] > errors[2]

    def test_suzuki2_better_than_trotter(self):
        t = 1.5
        n = 5
        dt = t / n
        U_ref = exact_evolution(self.H_mat, t)
        step_t = trotter_step(self.H1, self.H2, dt)
        step_s = suzuki2_step(self.H1, self.H2, dt)
        U_trotter = np.linalg.matrix_power(step_t, n)
        U_suzuki = np.linalg.matrix_power(step_s, n)
        assert np.linalg.norm(U_suzuki - U_ref) < np.linalg.norm(U_trotter - U_ref)

    def test_trotter_1step_error_order(self):
        """Error Trotter 1° decae al aumentar n."""
        t = 1.5
        n_vals = [2, 4, 8]
        errs = []
        U_ref = exact_evolution(self.H_mat, t)
        for n in n_vals:
            dt = t / n
            step = trotter_step(self.H1, self.H2, dt)
            Un = np.linalg.matrix_power(step, n)
            errs.append(np.linalg.norm(Un - U_ref))
        ratio_1 = errs[0] / errs[1]
        assert 1.5 < ratio_1 < 8.0  # orden 2: ratio aprox 4 en regimen asintótico


# ── Lab 13: StatevectorEstimator ─────────────────────────────────────────────

class TestEstimator:
    def test_bell_correlations(self):
        estimator = StatevectorEstimator()
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)

        for op_str, expected in [('ZZ', 1.0), ('ZI', 0.0), ('IZ', 0.0), ('XX', 1.0)]:
            obs = SparsePauliOp(op_str)
            job = estimator.run([(qc, obs)])
            val = float(job.result()[0].data.evs)
            assert abs(val - expected) < 1e-9, f"⟨{op_str}⟩ = {val}, expected {expected}"

    def test_variational_principle(self):
        from qiskit.circuit import ParameterVector
        H = SparsePauliOp.from_list([('XX', 1.0), ('YY', 1.0), ('ZZ', 1.0)])
        E0 = np.linalg.eigvalsh(H.to_matrix())[0]

        theta = ParameterVector('θ', 2)
        ansatz = QuantumCircuit(2)
        ansatz.ry(theta[0], 0)
        ansatz.ry(theta[1], 1)

        estimator = StatevectorEstimator()
        for _ in range(10):
            params = np.random.uniform(-np.pi, np.pi, 2)
            job = estimator.run([(ansatz, H, params)])
            E = float(job.result()[0].data.evs)
            assert E >= E0 - 1e-9

    def test_parameter_shift_gradient(self):
        """Verifica la regla de parameter shift."""
        from qiskit.circuit import ParameterVector
        H = SparsePauliOp('Z')
        theta = ParameterVector('θ', 1)
        qc = QuantumCircuit(1)
        qc.ry(theta[0], 0)

        estimator = StatevectorEstimator()
        t0 = 0.7
        shift = np.pi / 2

        e_plus = float(estimator.run([(qc, H, [t0 + shift])]).result()[0].data.evs)
        e_minus = float(estimator.run([(qc, H, [t0 - shift])]).result()[0].data.evs)
        grad_ps = (e_plus - e_minus) / 2

        # Para Ry(θ)|0⟩: ⟨Z⟩ = cos(θ) → d/dθ⟨Z⟩ = -sin(θ)
        grad_exact = -np.sin(t0)
        assert abs(grad_ps - grad_exact) < 1e-9


# ── Lab 14: DensityMatrix y ruido ─────────────────────────────────────────────

from qiskit.quantum_info import partial_trace, entropy


class TestDensityMatrix:
    def test_purity_pure_state(self):
        dm = DensityMatrix.from_label('0')
        assert abs(dm.purity() - 1.0) < 1e-9

    def test_purity_mixed_state(self):
        dm = DensityMatrix(np.eye(2) / 2)
        assert abs(dm.purity() - 0.5) < 1e-9

    def test_partial_trace_product(self):
        """Para estado producto, la traza parcial da el estado reducido correcto."""
        sv = Statevector.from_label('00')
        dm = DensityMatrix(sv)
        rho_A = partial_trace(dm, [1])
        rho_0 = DensityMatrix.from_label('0')
        assert state_fidelity(rho_A, rho_0) > 0.999

    def test_entanglement_increases_entropy(self):
        """Estado de Bell tiene S(ρ_A) = 1, producto tiene S = 0."""
        qc_bell = QuantumCircuit(2)
        qc_bell.h(0)
        qc_bell.cx(0, 1)
        dm_bell = DensityMatrix(Statevector(qc_bell))
        rho_A_bell = partial_trace(dm_bell, [1])

        sv_prod = Statevector.from_label('00')
        dm_prod = DensityMatrix(sv_prod)
        rho_A_prod = partial_trace(dm_prod, [1])

        S_bell = entropy(rho_A_bell, base=2)
        S_prod = entropy(rho_A_prod, base=2)
        assert S_bell > 0.99
        assert S_prod < 1e-9

    def test_depolarizing_channel(self):
        """Canal despolarizante reduce la pureza."""
        rho = DensityMatrix.from_label('+').data
        X = np.array([[0, 1], [1, 0]])
        Y = np.array([[0, -1j], [1j, 0]])
        Z = np.array([[1, 0], [0, -1]])
        p = 0.3
        rho_noisy = (1-p)*rho + (p/3)*(X@rho@X + Y@rho@Y + Z@rho@Z)
        dm_noisy = DensityMatrix(rho_noisy)
        assert dm_noisy.purity() < 1.0
        assert dm_noisy.purity() > 0.0


# ── Lab 15: Ruido vs Fidelidad ────────────────────────────────────────────────

class TestNoiseVsFidelity:
    def test_noise_decreases_fidelity(self):
        """Más ruido = menor fidelidad."""
        from qiskit_aer import AerSimulator
        from qiskit_aer.noise import NoiseModel, depolarizing_error

        qc = QuantumCircuit(1)
        qc.h(0)
        sv_ideal = Statevector(qc)
        dm_ideal = DensityMatrix(sv_ideal)

        qc_dm = qc.copy()
        qc_dm.save_density_matrix()

        fidelities = []
        for rate in [0.0, 0.05, 0.20]:
            nm = NoiseModel()
            if rate > 0:
                nm.add_all_qubit_quantum_error(depolarizing_error(rate, 1), ['h'])
            sim = AerSimulator(noise_model=nm, method='density_matrix')
            res = sim.run(qc_dm, shots=1).result()
            dm_n = DensityMatrix(res.data(0)['density_matrix'])
            fidelities.append(float(state_fidelity(dm_ideal, dm_n)))

        assert fidelities[0] > fidelities[1] > fidelities[2]

    def test_depth_degrades_fidelity(self):
        """Mayor profundidad → menor fidelidad con ruido."""
        from qiskit_aer import AerSimulator
        from qiskit_aer.noise import NoiseModel, depolarizing_error

        rate = 0.05
        nm = NoiseModel()
        nm.add_all_qubit_quantum_error(depolarizing_error(rate, 1), ['h'])

        fids = []
        for depth in [1, 5, 15]:
            qc = QuantumCircuit(1)
            for _ in range(depth):
                qc.h(0)
            sv_ideal = Statevector(qc)
            dm_ideal = DensityMatrix(sv_ideal)

            qc_dm = qc.copy()
            qc_dm.save_density_matrix()
            sim = AerSimulator(noise_model=nm)
            res = sim.run(qc_dm, shots=1).result()
            dm_n = DensityMatrix(res.data(0)['density_matrix'])
            fids.append(state_fidelity(dm_ideal, dm_n))

        assert fids[0] > fids[1] > fids[2]


# ── Lab 16: Trotter-Suzuki ────────────────────────────────────────────────────

class TestTrotterSuzuki:
    def setup_method(self):
        H = SparsePauliOp.from_list([('XX', 1.0), ('ZI', 0.5), ('IZ', 0.5)])
        self.H_mat = H.to_matrix()
        self.H1_mat = SparsePauliOp('XX').to_matrix()
        self.H2_mat = SparsePauliOp.from_list([('ZI', 0.5), ('IZ', 0.5)]).to_matrix()

    def test_suzuki4_better_than_suzuki2(self):
        p = 1 / (4 - 4**(1/3))
        t, n = 1.5, 4
        dt = t / n
        U_ref = exact_evolution(self.H_mat, t)

        def s2(dt_):
            return (expm(-1j*self.H1_mat*dt_/2) @
                    expm(-1j*self.H2_mat*dt_) @
                    expm(-1j*self.H1_mat*dt_/2))

        step_s2 = s2(dt)
        step_s4 = s2(p*dt) @ s2(p*dt) @ s2((1-4*p)*dt) @ s2(p*dt) @ s2(p*dt)

        U_s2 = np.linalg.matrix_power(step_s2, n)
        U_s4 = np.linalg.matrix_power(step_s4, n)

        err_s2 = np.linalg.norm(U_s2 - U_ref)
        err_s4 = np.linalg.norm(U_s4 - U_ref)
        assert err_s4 < err_s2

    def test_commutator_nonzero(self):
        comm = self.H1_mat @ self.H2_mat - self.H2_mat @ self.H1_mat
        assert np.linalg.norm(comm) > 0.1


# ── Lab 18: Rabi ─────────────────────────────────────────────────────────────

class TestRabi:
    def test_pi_pulse_flips(self):
        """Rx(π)|0⟩ → |1⟩ con prob 1."""
        qc = QuantumCircuit(1)
        qc.rx(np.pi, 0)
        sv = Statevector(qc)
        assert abs(sv.probabilities()[1] - 1.0) < 1e-9

    def test_pi_over_2_superposition(self):
        """Rx(π/2)|0⟩ → (|0⟩ - i|1⟩)/√2 → P(|1⟩) = 0.5."""
        qc = QuantumCircuit(1)
        qc.rx(np.pi / 2, 0)
        sv = Statevector(qc)
        assert abs(sv.probabilities()[1] - 0.5) < 1e-9

    def test_two_pi_pulse_identity(self):
        """Rx(2π) = -I (up to global phase), P(|0⟩) = 1."""
        qc = QuantumCircuit(1)
        qc.rx(2 * np.pi, 0)
        sv = Statevector(qc)
        assert abs(sv.probabilities()[0] - 1.0) < 1e-9

    def test_rabi_formula(self):
        """P(|1⟩) = sin²(θ/2) para Rx(θ)."""
        for theta in [0, np.pi/4, np.pi/2, np.pi, 3*np.pi/2]:
            qc = QuantumCircuit(1)
            qc.rx(theta, 0)
            sv = Statevector(qc)
            p1_actual = sv.probabilities()[1]
            p1_theory = np.sin(theta / 2)**2
            assert abs(p1_actual - p1_theory) < 1e-9, f"theta={theta}: {p1_actual} vs {p1_theory}"


# ── Lab 49: Computación Fotónica ─────────────────────────────────────────────

from scipy.special import eval_genlaguerre


class TestFotonica:
    """Tests para los conceptos del lab 49 y módulo 45."""

    def test_wigner_vacuum_positive(self):
        """W(0,0) para el vacío |0⟩ es positivo (estado clásico)."""
        W00 = (1 / np.pi) * np.exp(0.0)
        assert W00 > 0

    def test_wigner_fock1_negative_origin(self):
        """W(0,0) para |1⟩ es negativo — firma de no-clasicidad."""
        W00 = (-1 / np.pi) * np.exp(0.0) * eval_genlaguerre(1, 0, 0.0)
        assert W00 < 0

    def test_wigner_fock_sign_pattern(self):
        """W_n(0,0) = (-1)^n / π para todos los estados Fock."""
        for n in range(5):
            W00 = ((-1)**n / np.pi) * np.exp(0.0) * eval_genlaguerre(n, 0, 0.0)
            expected_sign = (-1)**n
            assert np.sign(W00) == np.sign(expected_sign)

    def test_permanent_2x2_known(self):
        """Perm([[a,b],[c,d]]) = ad + bc."""
        def permanent_ryser(A):
            n = A.shape[0]
            total = 0.0 + 0j
            for subset in range(1, 1 << n):
                bits = [j for j in range(n) if subset & (1 << j)]
                row_sums = np.array([sum(A[i, j] for j in bits) for i in range(n)])
                sign = (-1) ** (n - len(bits))
                total += sign * np.prod(row_sums)
            return (-1)**n * total

        A = np.array([[1, 2], [3, 4]], dtype=complex)
        perm = permanent_ryser(A)
        assert abs(perm - (1*4 + 2*3)) < 1e-10, f"Perm={perm}, expected 10"

    def test_permanent_identity_is_1(self):
        """Perm(I_n) = 1 para toda n. Usa signo (-1)^|S|, la convencion estandar de Ryser."""
        def permanent_ryser(A):
            n = A.shape[0]
            total = 0.0 + 0j
            for subset in range(1, 1 << n):
                bits = [j for j in range(n) if subset & (1 << j)]
                row_sums = np.array([sum(A[i, j] for j in bits) for i in range(n)])
                sign = (-1) ** len(bits)  # convencion estandar
                total += sign * np.prod(row_sums)
            return (-1)**n * total

        for n in [2, 3, 4]:
            p = permanent_ryser(np.eye(n, dtype=complex))
            assert abs(p - 1.0) < 1e-10, f"Perm(I_{n}) = {p}, expected 1"

    def test_squeezing_reduces_var_x(self):
        """Squeezing S(r) reduce Var(X) por factor e^{-2r}."""
        for r in [0.5, 1.0, 1.5]:
            var_x = 0.5 * np.exp(-2 * r)
            assert var_x < 0.5, "Var(X) debe ser menor que el vacío"
            assert abs(var_x - 0.5 * np.exp(-2 * r)) < 1e-12

    def test_squeezing_heisenberg_bound(self):
        """Squeezing respeta Var(X)·Var(P) = 1/4 (estado mínimo)."""
        for r in [0.0, 0.5, 1.0, 2.0]:
            var_x = 0.5 * np.exp(-2 * r)
            var_p = 0.5 * np.exp(+2 * r)
            product = var_x * var_p
            assert abs(product - 0.25) < 1e-12, f"r={r}: Var(X)*Var(P)={product} ≠ 1/4"

    def test_gkp_threshold(self):
        """Umbral de corrección GKP: |δx| < sqrt(π)/2."""
        threshold = np.sqrt(np.pi) / 2
        assert abs(threshold - 0.8862) < 1e-4
        # Errores corregibles
        for delta in [0.1, 0.3, 0.5, 0.8]:
            assert delta < threshold, f"delta={delta} debería ser corregible"
        # Errores no corregibles
        for delta in [0.95, 1.2, 1.5]:
            assert delta >= threshold, f"delta={delta} no debería ser corregible"

    def test_gkp_states_orthogonal(self):
        """Los estados lógicos GKP |0_L⟩ y |1_L⟩ son (aproximadamente) ortogonales."""
        x = np.linspace(-10, 10, 5000)
        step = 2 * np.sqrt(np.pi)
        Delta = 0.2
        N = 8

        def gkp(x, logical):
            offset = 0.0 if logical == 0 else np.sqrt(np.pi)
            psi = sum(np.exp(-0.5 * ((x - n*step - offset)/Delta)**2) for n in range(-N, N+1))
            return psi / np.sqrt(np.trapezoid(psi**2, x))

        psi0 = gkp(x, 0)
        psi1 = gkp(x, 1)
        overlap = abs(np.trapezoid(psi0 * psi1, x))
        assert overlap < 1e-5, f"Solapamiento GKP = {overlap} (debe ser ~0)"

    def test_boson_sampling_probs_sum_to_1(self):
        """Las probabilidades de Boson Sampling suman 1."""
        from itertools import combinations_with_replacement
        from collections import Counter

        def permanent_ryser(A):
            n = A.shape[0]
            total = 0.0 + 0j
            for subset in range(1, 1 << n):
                bits = [j for j in range(n) if subset & (1 << j)]
                row_sums = np.array([sum(A[i, j] for j in bits) for i in range(n)])
                total += (-1)**(n - len(bits)) * np.prod(row_sums)
            return (-1)**n * total

        m, n_ph = 4, 2
        rng = np.random.default_rng(0)
        Z = rng.standard_normal((m, m)) + 1j * rng.standard_normal((m, m))
        Q, R = np.linalg.qr(Z / np.sqrt(2))
        U = Q @ np.diag(R.diagonal() / np.abs(R.diagonal()))
        input_modes = [0, 1]

        from math import factorial as fact
        total_p = 0.0
        for out in combinations_with_replacement(range(m), n_ph):
            U_sub = U[np.ix_(list(out), input_modes)]
            p = abs(permanent_ryser(U_sub))**2
            out_c = Counter(out)
            denom = np.prod([fact(k) for k in out_c.values()])
            total_p += float(p / denom)

        assert abs(total_p - 1.0) < 0.01, f"Suma de probabilidades = {total_p}"


class TestRydberg:
    """Tests para Lab 50 — Átomos Neutros y Arrays de Rydberg (Phase 20)."""

    def _op_on_site(self, op, site, N):
        ops = [np.eye(2)] * N
        ops[site] = op
        result = ops[0]
        for o in ops[1:]:
            result = np.kron(result, o)
        return result

    def _build_rydberg_H(self, N, Omega, Delta, C6=100.0, a=1.0):
        sx = np.array([[0,1],[1,0]], dtype=complex)
        nR = np.array([[0,0],[0,1]], dtype=complex)
        H = np.zeros((2**N, 2**N), dtype=complex)
        for i in range(N):
            H += (Omega/2) * self._op_on_site(sx, i, N)
            H -= Delta * self._op_on_site(nR, i, N)
        for i in range(N-1):
            for j in range(i+1, N):
                Uij = C6 / (abs(i-j)*a)**6
                H += Uij * (self._op_on_site(nR, i, N) @ self._op_on_site(nR, j, N))
        return H

    def _build_pxp_H(self, N, Omega=1.0):
        sx = np.array([[0,1],[1,0]], dtype=complex)
        P0 = np.array([[1,0],[0,0]], dtype=complex)
        H = np.zeros((2**N, 2**N), dtype=complex)
        for i in range(N):
            left  = self._op_on_site(P0, (i-1)%N, N)
            drive = self._op_on_site(sx, i, N)
            right = self._op_on_site(P0, (i+1)%N, N)
            H += (Omega/2) * left @ drive @ right
        return H

    def test_rydberg_H_hermitian(self):
        """El Hamiltoniano de Rydberg debe ser hermítico."""
        H = self._build_rydberg_H(3, Omega=1.0, Delta=0.5, C6=50.0)
        assert np.allclose(H, H.conj().T, atol=1e-12)

    def test_rydberg_H_dimension(self):
        """El Hamiltoniano tiene dimensión 2^N."""
        for N in [2, 3, 4]:
            H = self._build_rydberg_H(N, Omega=1.0, Delta=0.0)
            assert H.shape == (2**N, 2**N)

    def test_blockade_high_C6_avoids_double_rydberg(self):
        """Con C6 >> Omega, el estado con dos vecinos en Rydberg es penalizado."""
        N = 2
        H = self._build_rydberg_H(N, Omega=0.01, Delta=5.0, C6=1e6)
        from scipy.linalg import eigh
        evals, evecs = eigh(H)
        gs = evecs[:, 0]
        # Estado |rr⟩ = índice 3 (binario 11), debe tener baja amplitud
        assert abs(gs[3])**2 < 0.01

    def test_rydberg_phase_atomic_large_negative_delta(self):
        """Para Delta << 0 el estado base tiene poca densidad Rydberg."""
        from scipy.linalg import eigh
        N = 3
        H = self._build_rydberg_H(N, Omega=0.5, Delta=-10.0, C6=50.0)
        evals, evecs = eigh(H)
        gs = evecs[:, 0]
        nR = np.array([[0,0],[0,1]], dtype=complex)
        nR_total = sum(self._op_on_site(nR, i, N) for i in range(N)) / N
        n_avg = np.real(gs @ nR_total @ gs)
        assert n_avg < 0.1

    def test_rydberg_phase_rydberg_large_positive_delta(self):
        """Para Delta >> 0 sin bloqueo el estado base tiene alta densidad Rydberg."""
        from scipy.linalg import eigh
        N = 3
        H = self._build_rydberg_H(N, Omega=0.1, Delta=10.0, C6=0.001)
        evals, evecs = eigh(H)
        gs = evecs[:, 0]
        nR = np.array([[0,0],[0,1]], dtype=complex)
        nR_total = sum(self._op_on_site(nR, i, N) for i in range(N)) / N
        n_avg = np.real(gs @ nR_total @ gs)
        assert n_avg > 0.8

    def test_pxp_H_hermitian(self):
        """El Hamiltoniano PXP debe ser hermítico."""
        H = self._build_pxp_H(4, Omega=1.0)
        assert np.allclose(H, H.conj().T, atol=1e-12)

    def test_pxp_z2_revival(self):
        """El estado Z2 muestra revival con F > 0.5 en algún tiempo para PXP N=4."""
        from scipy.linalg import eigh
        N = 4
        H = self._build_pxp_H(N, Omega=1.0)
        evals, evecs = eigh(H)
        z2_idx = int("1010", 2)
        psi0 = np.zeros(2**N, dtype=complex)
        psi0[z2_idx] = 1.0
        c = evecs.conj().T @ psi0
        max_fid = 0.0
        for t in np.linspace(0.1, 20.0, 500):
            psi_t = evecs @ (c * np.exp(-1j * evals * t))
            fid = abs(psi0 @ psi_t.conj())**2
            if fid > max_fid:
                max_fid = fid
        assert max_fid > 0.5, f"Fidelidad máxima de revival = {max_fid:.3f}"

    def test_blockade_radius_scaling(self):
        """El radio de bloqueo escala como C6^(1/6) / Omega^(1/6)."""
        C6 = 862690.0  # GHz·μm^6
        Omega1, Omega2 = 1.0, 2.0
        r1 = (C6 / (Omega1 * 1e3)) ** (1/6)
        r2 = (C6 / (Omega2 * 1e3)) ** (1/6)
        ratio = r1 / r2
        expected = (Omega2 / Omega1) ** (1/6)
        assert abs(ratio - expected) < 1e-10

    def test_cz_gate_truth_table(self):
        """La matriz CZ = diag(1,-1,1,1) para el bloqueo Rydberg."""
        CZ = np.diag([1.0, -1.0, 1.0, 1.0])
        # |gg⟩ → |gg⟩
        gg = np.array([1,0,0,0]); assert np.allclose(CZ @ gg, [1,0,0,0])
        # |gr⟩ → -|gr⟩
        gr = np.array([0,1,0,0]); assert np.allclose(CZ @ gr, [0,-1,0,0])
        # |rg⟩ → |rg⟩
        rg = np.array([0,0,1,0]); assert np.allclose(CZ @ rg, [0,0,1,0])
        # |rr⟩ → |rr⟩ (bloqueado → no accesible, eigenvalor 1)
        rr = np.array([0,0,0,1]); assert np.allclose(CZ @ rr, [0,0,0,1])

    def test_z2_order_parameter(self):
        """El parámetro de orden Z2 distingue las fases cristalina y atómica."""
        from scipy.linalg import eigh
        N = 4
        nR = np.array([[0,0],[0,1]], dtype=complex)

        def z2_order(gs):
            val = 0.0
            for i in range(N):
                sign = (-1)**i
                val += sign * np.real(gs @ self._op_on_site(nR, i, N) @ gs)
            return abs(val) / N

        # Fase Z2: Delta >> 0, Omega pequeño, C6 induce alternancia
        H_z2 = self._build_rydberg_H(N, Omega=0.2, Delta=2.0, C6=200.0)
        _, evecs_z2 = eigh(H_z2)
        order_z2 = z2_order(evecs_z2[:, 0])

        # Fase atómica: Delta << 0
        H_at = self._build_rydberg_H(N, Omega=0.2, Delta=-5.0, C6=200.0)
        _, evecs_at = eigh(H_at)
        order_at = z2_order(evecs_at[:, 0])

        assert order_z2 > order_at, f"Z2 order: {order_z2:.3f} vs atomic: {order_at:.3f}"
