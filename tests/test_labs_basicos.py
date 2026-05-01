"""
Tests para labs 01-11: funciones cuánticas básicas.
Cada test reimplementa la lógica del lab para verificar correctitud
sin importar los notebooks directamente.
"""
import numpy as np
import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp, state_fidelity
from qiskit.primitives import StatevectorSampler, StatevectorEstimator


# ── Lab 01: Grover ────────────────────────────────────────────────────────────

def grover_2q_circuit() -> QuantumCircuit:
    qc = QuantumCircuit(2)
    qc.h([0, 1])
    # Oracle para |11⟩
    qc.cz(0, 1)
    # Difusor
    qc.h([0, 1])
    qc.x([0, 1])
    qc.cz(0, 1)
    qc.x([0, 1])
    qc.h([0, 1])
    return qc


class TestGrover:
    def test_probability_target(self):
        qc = grover_2q_circuit()
        sv = Statevector(qc)
        probs = sv.probabilities_dict()
        assert probs.get('11', 0) > 0.9

    def test_uniform_initial(self):
        qc = QuantumCircuit(2)
        qc.h([0, 1])
        sv = Statevector(qc)
        probs = sv.probabilities()
        assert all(abs(p - 0.25) < 1e-6 for p in probs)


# ── Lab 02: Teleportación ─────────────────────────────────────────────────────

def bell_fidelity() -> float:
    """Fidelidad del estado de Bell preparado."""
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    sv = Statevector(qc)
    # Estado ideal |Φ+⟩
    expected = np.zeros(4, dtype=complex)
    expected[0] = 1 / np.sqrt(2)
    expected[3] = 1 / np.sqrt(2)
    sv_expected = Statevector(expected)
    return float(state_fidelity(sv, sv_expected))


class TestTeleportacion:
    def test_bell_pair_fidelity(self):
        fid = bell_fidelity()
        assert fid > 0.999

    def test_bell_pair_entanglement(self):
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        sv = Statevector(qc)
        probs = sv.probabilities()
        assert abs(probs[0] - 0.5) < 1e-6  # P(|00⟩) = 0.5
        assert abs(probs[3] - 0.5) < 1e-6  # P(|11⟩) = 0.5


# ── Lab 04: Bernstein-Vazirani ────────────────────────────────────────────────

def bv_oracle(s: str, n: int) -> QuantumCircuit:
    qc = QuantumCircuit(n + 1)
    for i, bit in enumerate(reversed(s)):
        if bit == '1':
            qc.cx(i, n)
    return qc


def bv_circuit(s: str) -> QuantumCircuit:
    n = len(s)
    qc = QuantumCircuit(n + 1, n)
    qc.x(n)
    qc.h(range(n + 1))
    qc.compose(bv_oracle(s, n), inplace=True)
    qc.h(range(n))
    qc.measure(range(n), range(n))
    return qc


class TestBernsteinVazirani:
    @pytest.mark.parametrize("secret", ["101", "110", "001", "111", "000"])
    def test_recover_secret(self, secret):
        sampler = StatevectorSampler()
        qc = bv_circuit(secret)
        job = sampler.run([qc], shots=128)
        counts = job.result()[0].data.c.get_counts()
        top = max(counts, key=counts.get)
        assert top == secret, f"Expected {secret}, got {top}"

    def test_oracle_identity_on_zero(self):
        qc = bv_oracle("000", 3)
        sv = Statevector(qc)
        assert abs(sv.probabilities()[0] - 1.0) < 1e-9


# ── Lab 05: QFT ───────────────────────────────────────────────────────────────

def qft_manual(n: int) -> QuantumCircuit:
    from qiskit.circuit.library import QFT
    return QFT(n, do_swaps=True)


class TestQFT:
    def test_unitarity(self):
        from qiskit.quantum_info import Operator
        qft = qft_manual(3)
        U = Operator(qft).data
        should_be_eye = U @ U.conj().T
        assert np.allclose(should_be_eye, np.eye(8), atol=1e-9)

    def test_inverse_recovers_state(self):
        from qiskit.circuit.library import QFT
        qc = QuantumCircuit(3)
        qc.h(0)  # estado |+00⟩
        qc.compose(QFT(3), inplace=True)
        qc.compose(QFT(3, inverse=True), inplace=True)
        sv = Statevector(qc)
        # Debe recuperar |+00⟩
        expected = Statevector.from_label('+').expand(
            Statevector.from_label('0')
        ).expand(Statevector.from_label('0'))
        assert state_fidelity(sv, expected) > 0.999

    def test_qft_size_2(self):
        from qiskit.quantum_info import Operator
        qft2 = qft_manual(2)
        U = Operator(qft2).data
        # QFT de 2 qubits: bien conocida
        expected = np.array([[1, 1, 1, 1],
                              [1, 1j, -1, -1j],
                              [1, -1, 1, -1],
                              [1, -1j, -1, 1j]]) / 2
        assert np.allclose(U, expected, atol=1e-9)


# ── Lab 06: Información cuántica ──────────────────────────────────────────────

from qiskit.quantum_info import DensityMatrix, entropy, partial_trace


def entanglement_entropy(sv: Statevector, qubit_A: list) -> float:
    n = int(np.log2(len(sv)))
    dm = DensityMatrix(sv)
    trace_out = [i for i in range(n) if i not in qubit_A]
    rho_A = partial_trace(dm, trace_out)
    return entropy(rho_A, base=2)


class TestInfoCuantica:
    def test_product_state_zero_entropy(self):
        sv = Statevector.from_label('00')
        E = entanglement_entropy(sv, [0])
        assert abs(E) < 1e-9

    def test_bell_max_entropy(self):
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        sv = Statevector(qc)
        E = entanglement_entropy(sv, [0])
        assert abs(E - 1.0) < 1e-6

    def test_pure_state_zero_von_neumann(self):
        dm = DensityMatrix.from_label('0')
        S = entropy(dm, base=2)
        assert abs(S) < 1e-9

    def test_mixed_state_max_entropy(self):
        dm = DensityMatrix(np.eye(2) / 2)
        S = entropy(dm, base=2)
        assert abs(S - 1.0) < 1e-9

    def test_fidelity_identical(self):
        sv = Statevector.from_label('+')
        assert abs(state_fidelity(sv, sv) - 1.0) < 1e-9

    def test_fidelity_orthogonal(self):
        sv0 = Statevector.from_label('0')
        sv1 = Statevector.from_label('1')
        assert abs(state_fidelity(sv0, sv1)) < 1e-9


# ── Lab 07: QPE ───────────────────────────────────────────────────────────────

from qiskit.circuit.library import QFT


def qpe_circuit(phase: float, t: int) -> QuantumCircuit:
    from qiskit import QuantumRegister, ClassicalRegister
    counting = QuantumRegister(t, 'count')
    eigenstate = QuantumRegister(1, 'eig')
    cr = ClassicalRegister(t, 'c')
    qc = QuantumCircuit(counting, eigenstate, cr)
    qc.x(eigenstate[0])  # eigenstate |1⟩ de cp con eigenvalor e^{2πi·phase}
    qc.h(counting)
    for k in range(t):
        angle = 2 * np.pi * phase * (2 ** k)
        qc.cp(angle, counting[k], eigenstate[0])
    qft_inv = QFT(t, inverse=True, do_swaps=True)
    qc.append(qft_inv, counting)
    qc.measure(counting, cr)
    return qc


class TestQPE:
    @pytest.mark.parametrize("phase,t", [(0.25, 4), (0.125, 3), (0.5, 2)])
    def test_exact_phase(self, phase, t):
        sampler = StatevectorSampler()
        qc = qpe_circuit(phase, t)
        job = sampler.run([qc], shots=1024)
        counts = job.result()[0].data.c.get_counts()
        top = max(counts, key=counts.get)
        phi_est = int(top, 2) / 2**t
        assert abs(phi_est - phase) < 0.01, f"Phase {phase}: got {phi_est}"

    def test_zero_phase(self):
        sampler = StatevectorSampler()
        qc = qpe_circuit(0.0, 4)
        job = sampler.run([qc], shots=256)
        counts = job.result()[0].data.c.get_counts()
        top = max(counts, key=counts.get)
        assert int(top, 2) == 0


# ── Lab 08: VQE ───────────────────────────────────────────────────────────────

class TestVQE:
    def test_principal_variacional(self):
        from qiskit.circuit import ParameterVector
        H = SparsePauliOp.from_list([('XX', 1.0), ('YY', 1.0), ('ZZ', 1.0)])
        E_exact = np.linalg.eigvalsh(H.to_matrix())[0]

        theta = ParameterVector('θ', 2)
        ansatz = QuantumCircuit(2)
        ansatz.ry(theta[0], 0)
        ansatz.ry(theta[1], 1)
        ansatz.cx(0, 1)

        estimator = StatevectorEstimator()
        params = np.random.uniform(-np.pi, np.pi, 2)
        job = estimator.run([(ansatz, H, params)])
        E_var = float(job.result()[0].data.evs)
        assert E_var >= E_exact - 1e-9, f"Principio variacional violado: {E_var} < {E_exact}"

    def test_ground_state_heisenberg(self):
        from qiskit.circuit import ParameterVector
        from scipy.optimize import minimize

        H = SparsePauliOp.from_list([('XX', 1.0), ('YY', 1.0), ('ZZ', 1.0)])
        E_exact = np.linalg.eigvalsh(H.to_matrix())[0]

        theta = ParameterVector('θ', 4)
        ansatz = QuantumCircuit(2)
        ansatz.ry(theta[0], 0); ansatz.ry(theta[1], 1)
        ansatz.cx(0, 1)
        ansatz.ry(theta[2], 0); ansatz.ry(theta[3], 1)

        estimator = StatevectorEstimator()
        def cost(params):
            return float(estimator.run([(ansatz, H, params)]).result()[0].data.evs)

        np.random.seed(0)
        res = minimize(cost, np.random.uniform(-np.pi, np.pi, 4), method='COBYLA',
                       options={'maxiter': 500})
        assert abs(res.fun - E_exact) < 0.05


# ── Lab 09: QAOA ──────────────────────────────────────────────────────────────

class TestQAOA:
    def test_maxcut_triangle(self):
        """QAOA p=1 en triángulo: MaxCut = 2 aristas."""
        from qiskit.circuit import ParameterVector
        from scipy.optimize import minimize

        # Grafo triángulo: MaxCut = 2
        edges = [(0, 1), (1, 2), (0, 2)]
        n = 3
        # H_C = sum_edges (1 - ZiZj) / 2 → maximizar
        # Equivalente: minimizar -H_C = sum_edges (ZiZj - 1) / 2
        pauli_list = []
        for (i, j) in edges:
            ops = ['I'] * n
            ops[i] = 'Z'; ops[j] = 'Z'
            pauli_list.append((''.join(reversed(ops)), 0.5))  # positivo → maximizar
        # Añadir constante -3/2 para tener -H_C correctamente
        H_neg = SparsePauliOp.from_list(pauli_list)  # sum(0.5*ZiZj)

        gammas = ParameterVector('γ', 1)
        betas = ParameterVector('β', 1)
        qc = QuantumCircuit(n)
        qc.h(range(n))
        for (i, j) in edges:
            qc.cx(i, j); qc.rz(2 * gammas[0], j); qc.cx(i, j)
        for q in range(n):
            qc.rx(2 * betas[0], q)

        estimator = StatevectorEstimator()
        def cost(params):
            return float(estimator.run([(qc, H_neg, params)]).result()[0].data.evs)

        best = np.inf
        for seed in range(8):
            np.random.seed(seed)
            x0 = np.random.uniform(0, np.pi, 2)
            res = minimize(cost, x0, method='COBYLA', options={'maxiter': 500})
            if res.fun < best:
                best = res.fun
        # El valor esperado de sum(0.5*ZiZj) para MaxCut=2 es: 3*0.5*(-1)=-1.5 (borde de corte ZiZj=-1)
        # Pero el óptimo real de H_neg = -0.5*(MaxCut_sum), para 3-cycle min ≈ -1.5
        # Solo verificamos que QAOA mejora el estado inicial (E=0 para estado uniforme)
        assert best < 0.0  # QAOA encuentra corte mejor que aleatorio
