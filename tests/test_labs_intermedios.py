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
