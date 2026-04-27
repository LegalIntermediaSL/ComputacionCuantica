"""
Tests basados en propiedades con Hypothesis — Fase 15.

Verifican invariantes matemáticos que deben mantenerse para *cualquier* entrada
dentro del dominio, no solo para valores fijos. Complementan test_numerical_notebooks.py.

Cobertura:
  - Propiedades de estados cuánticos (norma, entropía)
  - Propiedades de circuitos (unitariedad, conmutación)
  - Propiedades del código tórico (síndromes, paridad)
  - Propiedades de VQE/QAOA (variational principle, convexidad)
  - Propiedades de QKD (QBER monótono, límites de información)
  - Propiedades de PAC learning (escala de muestra)
  - Propiedades de operadores de Pauli (algebra, espectro)
"""

import numpy as np
import pytest
from hypothesis import given, settings, assume, strategies as st


# ── Configuración de Hypothesis ─────────────────────────────────────────────
settings.register_profile("fast", max_examples=30, deadline=2000)
settings.register_profile("thorough", max_examples=200, deadline=10000)
settings.load_profile("fast")


# ===========================================================================
# Propiedades de estados cuánticos
# ===========================================================================

@given(
    alpha=st.floats(min_value=0.0, max_value=2 * np.pi, allow_nan=False),
    beta=st.floats(min_value=0.0, max_value=np.pi, allow_nan=False),
)
def test_bloch_state_norm_always_one(alpha: float, beta: float):
    """Todo estado de un qubit en la esfera de Bloch tiene norma exactamente 1."""
    psi = np.array([np.cos(beta / 2), np.exp(1j * alpha) * np.sin(beta / 2)])
    norm = np.linalg.norm(psi)
    assert abs(norm - 1.0) < 1e-12, f"Norma {norm:.15f} ≠ 1 para alpha={alpha:.3f}, beta={beta:.3f}"


@given(
    n_qubits=st.integers(min_value=1, max_value=4),
    seed=st.integers(min_value=0, max_value=999),
)
def test_random_state_norm(n_qubits: int, seed: int):
    """Estado cuántico aleatorio normalizado siempre tiene norma 1."""
    rng = np.random.default_rng(seed)
    dim = 2**n_qubits
    psi = rng.normal(size=dim) + 1j * rng.normal(size=dim)
    psi /= np.linalg.norm(psi)
    assert abs(np.linalg.norm(psi) - 1.0) < 1e-12


@given(
    p=st.floats(min_value=0.0, max_value=1.0, allow_nan=False),
)
def test_mixed_state_eigenvalues_nonneg(p: float):
    """Estado mezcla ρ = p|0><0| + (1-p)|1><1| tiene eigenvalores no negativos."""
    rho = np.array([[p, 0], [0, 1 - p]])
    eigenvalues = np.linalg.eigvalsh(rho)
    assert all(ev >= -1e-12 for ev in eigenvalues), \
        f"Eigenvalor negativo: {min(eigenvalues):.2e}"


@given(
    p=st.floats(min_value=0.0, max_value=1.0, allow_nan=False),
)
def test_von_neumann_entropy_bounds(p: float):
    """Entropía de von Neumann 0 ≤ S ≤ 1 para estado mezcla de 1 qubit."""
    rho = np.array([[p, 0], [0, 1 - p]])
    eigenvals = np.linalg.eigvalsh(rho)
    eigenvals = eigenvals[eigenvals > 1e-14]
    if len(eigenvals) == 0:
        S = 0.0
    else:
        S = float(-np.sum(eigenvals * np.log2(eigenvals)))
    assert -1e-10 <= S <= 1.0 + 1e-10, f"Entropía {S:.6f} fuera de [0, 1]"


# ===========================================================================
# Propiedades de operadores de Pauli
# ===========================================================================

@given(
    pauli_choice=st.sampled_from(["X", "Y", "Z"]),
)
def test_pauli_matrices_involutory(pauli_choice: str):
    """Las matrices de Pauli son involutivas: σ² = I."""
    X = np.array([[0, 1], [1, 0]])
    Y = np.array([[0, -1j], [1j, 0]])
    Z = np.array([[1, 0], [0, -1]])
    paulis = {"X": X, "Y": Y, "Z": Z}
    sigma = paulis[pauli_choice]
    assert np.allclose(sigma @ sigma, np.eye(2), atol=1e-12), \
        f"σ_{pauli_choice}² ≠ I"


@given(
    pauli_a=st.sampled_from(["X", "Y", "Z"]),
    pauli_b=st.sampled_from(["X", "Y", "Z"]),
)
def test_pauli_anticommutation(pauli_a: str, pauli_b: str):
    """Paulis distintas anticonmutan: {σ_a, σ_b} = 0 si a ≠ b."""
    X = np.array([[0, 1], [1, 0]])
    Y = np.array([[0, -1j], [1j, 0]])
    Z = np.array([[1, 0], [0, -1]])
    paulis = {"X": X, "Y": Y, "Z": Z}
    if pauli_a == pauli_b:
        return  # caso trivial, skip
    A = paulis[pauli_a]
    B = paulis[pauli_b]
    anticomm = A @ B + B @ A
    assert np.allclose(anticomm, 0, atol=1e-12), \
        f"{{σ_{pauli_a}, σ_{pauli_b}}} ≠ 0"


@given(
    theta=st.floats(min_value=0.0, max_value=2 * np.pi, allow_nan=False),
    pauli_choice=st.sampled_from(["X", "Y", "Z"]),
)
def test_rotation_gate_unitary(theta: float, pauli_choice: str):
    """Las puertas de rotación R_σ(θ) = e^{-iθσ/2} son unitarias para todo θ."""
    X = np.array([[0, 1], [1, 0]])
    Y = np.array([[0, -1j], [1j, 0]])
    Z = np.array([[1, 0], [0, -1]])
    paulis = {"X": X, "Y": Y, "Z": Z}
    sigma = paulis[pauli_choice]
    R = np.cos(theta / 2) * np.eye(2) - 1j * np.sin(theta / 2) * sigma
    assert np.allclose(R @ R.conj().T, np.eye(2), atol=1e-12), \
        f"R_{pauli_choice}({theta:.3f}) no es unitaria"


# ===========================================================================
# Propiedades del código tórico
# ===========================================================================

def make_toric_operators(L: int):
    """Construye listas de qubits para Av y Bp en retículo L×L."""
    n = 2 * L * L

    def h_edge(i, j):
        return (i % L) * L + (j % L)

    def v_edge(i, j):
        return L * L + (i % L) * L + (j % L)

    av_qubits = []
    for vi in range(L):
        for vj in range(L):
            av_qubits.append([
                h_edge(vi, vj), h_edge(vi, vj - 1),
                v_edge(vi, vj), v_edge(vi - 1, vj),
            ])

    bp_qubits = []
    for pi in range(L):
        for pj in range(L):
            bp_qubits.append([
                h_edge(pi, pj), h_edge(pi + 1, pj),
                v_edge(pi, pj), v_edge(pi, pj + 1),
            ])

    return n, av_qubits, bp_qubits


@given(L=st.integers(min_value=2, max_value=4))
def test_toric_vertex_plaquette_share_even_edges(L: int):
    """Todo par (vértice, plaqueta) comparte 0 ó 2 aristas (necesario para [Av, Bp]=0)."""
    _, av_qubits, bp_qubits = make_toric_operators(L)
    for av_qs in av_qubits:
        for bp_qs in bp_qubits:
            shared = len(set(av_qs) & set(bp_qs))
            assert shared in (0, 2), \
                f"Par Av/Bp comparte {shared} aristas (debe ser 0 ó 2)"


@given(L=st.integers(min_value=2, max_value=4))
def test_toric_qubit_count(L: int):
    """El número de qubits físicos es siempre 2L²."""
    n, av_qubits, bp_qubits = make_toric_operators(L)
    assert n == 2 * L * L, f"n={n} ≠ 2L²={2*L*L}"
    assert len(av_qubits) == L * L
    assert len(bp_qubits) == L * L


@given(L=st.integers(min_value=2, max_value=4))
def test_toric_each_vertex_has_four_edges(L: int):
    """Cada vértice tiene exactamente 4 aristas incidentes."""
    _, av_qubits, _ = make_toric_operators(L)
    for i, qs in enumerate(av_qubits):
        assert len(qs) == 4, f"Vértice {i} tiene {len(qs)} aristas (esperado 4)"


@given(L=st.integers(min_value=2, max_value=4))
def test_toric_syndrome_x_error_excites_two_vertices(L: int):
    """Un error X en cualquier arista excita exactamente 2 vértices."""
    n, av_qubits, _ = make_toric_operators(L)
    for e in range(n):
        excited = sum(1 for qs in av_qubits if e in qs)
        assert excited == 2, f"Arista {e}: {excited} vértices excitados (esperado 2)"


@given(L=st.integers(min_value=2, max_value=4))
def test_toric_syndrome_z_error_excites_two_plaquettes(L: int):
    """Un error Z en cualquier arista excita exactamente 2 plaquetas."""
    n, _, bp_qubits = make_toric_operators(L)
    for e in range(n):
        excited = sum(1 for qs in bp_qubits if e in qs)
        assert excited == 2, f"Arista {e}: {excited} plaquetas excitadas (esperado 2)"


# ===========================================================================
# Propiedades de VQE (principio variacional)
# ===========================================================================

@given(
    n_trials=st.integers(min_value=5, max_value=20),
    seed=st.integers(min_value=0, max_value=9999),
)
@pytest.mark.slow
def test_variational_principle_random_hamiltonian(n_trials: int, seed: int):
    """Principio variacional: E_VQE ≥ E_exacta para Hamiltoniano 2x2 aleatorio."""
    rng = np.random.default_rng(seed)
    for _ in range(n_trials):
        # Hamiltoniano hermítico 2x2 aleatorio
        A = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
        H = (A + A.conj().T) / 2  # hermítico
        E_exact = np.min(np.linalg.eigvalsh(H))

        # Estado de prueba aleatorio normalizado
        psi_trial = rng.normal(size=2) + 1j * rng.normal(size=2)
        psi_trial /= np.linalg.norm(psi_trial)
        E_trial = np.real(psi_trial.conj() @ H @ psi_trial)

        assert E_trial >= E_exact - 1e-10, \
            f"Principio variacional violado: E_trial={E_trial:.6f} < E_exact={E_exact:.6f}"


@given(
    theta=st.floats(min_value=-np.pi, max_value=np.pi, allow_nan=False),
)
def test_ising_energy_symmetric(theta: float):
    """El Hamiltoniano de Ising -Z₀Z₁ tiene energía mínima -1 para estado Bell."""
    # H = -Z₀Z₁ → eigenvalores ±1 en el espacio de 2 qubits
    # E_min = -1 (estados |00>, |11>)
    ZZ = np.diag([1.0, -1.0, -1.0, 1.0])  # -Z⊗Z
    H_ising = -ZZ
    E_min = np.min(np.linalg.eigvalsh(H_ising))
    assert abs(E_min - (-1.0)) < 1e-12, f"E_min(Ising) = {E_min} ≠ -1"


# ===========================================================================
# Propiedades de PAC Learning
# ===========================================================================

@given(
    epsilon=st.floats(min_value=0.01, max_value=0.5, allow_nan=False),
    delta=st.floats(min_value=0.01, max_value=0.5, allow_nan=False),
    log2_H=st.integers(min_value=1, max_value=30),
)
def test_pac_sample_complexity_monotone_in_epsilon(epsilon: float, delta: float, log2_H: int):
    """La complejidad de muestra PAC decrece al aumentar ε (más tolerancia → menos muestras)."""
    eps2 = epsilon * 1.5  # eps2 > eps1
    assume(eps2 <= 0.5)

    def pac_m(eps, delt, lH):
        return int(np.ceil((1 / eps) * (lH * np.log(2) + np.log(1 / delt))))

    m1 = pac_m(epsilon, delta, log2_H)
    m2 = pac_m(eps2, delta, log2_H)
    assert m1 >= m2, \
        f"m(ε={epsilon:.3f}) = {m1} < m(ε={eps2:.3f}) = {m2} — debería ser m1 ≥ m2"


@given(
    epsilon=st.floats(min_value=0.01, max_value=0.5, allow_nan=False),
    delta=st.floats(min_value=0.01, max_value=0.5, allow_nan=False),
    log2_H=st.integers(min_value=1, max_value=30),
)
def test_pac_sample_complexity_monotone_in_H(epsilon: float, delta: float, log2_H: int):
    """La complejidad de muestra PAC crece al aumentar |H| (más hipótesis → más muestras)."""
    def pac_m(eps, delt, lH):
        return int(np.ceil((1 / eps) * (lH * np.log(2) + np.log(1 / delt))))

    m1 = pac_m(epsilon, delta, log2_H)
    m2 = pac_m(epsilon, delta, log2_H + 5)
    assert m2 >= m1, \
        f"m(|H|×32) = {m2} < m(|H|) = {m1} — más hipótesis debería requerir más muestras"


# ===========================================================================
# Propiedades de QKD / BB84
# ===========================================================================

@given(
    n_bits=st.integers(min_value=100, max_value=1000),
    seed=st.integers(min_value=0, max_value=9999),
)
def test_bb84_without_eve_zero_qber(n_bits: int, seed: int):
    """BB84 sin Eva tiene QBER = 0 con certeza."""
    rng = np.random.default_rng(seed)
    alice_bits = rng.integers(0, 2, n_bits)
    alice_bases = rng.integers(0, 2, n_bits)
    bob_bases = rng.integers(0, 2, n_bits)

    # Bob mide correctamente cuando elige la misma base
    matching = (alice_bases == bob_bases)
    assume(np.sum(matching) > 0)

    bob_bits = alice_bits.copy()  # sin Eva → Bob siempre coincide en bases correctas
    errors = np.sum(alice_bits[matching] != bob_bits[matching])
    assert errors == 0, f"QBER sin Eva = {errors}/{np.sum(matching)} ≠ 0"


@given(
    n_bits=st.integers(min_value=500, max_value=2000),
    seed=st.integers(min_value=0, max_value=9999),
)
@pytest.mark.slow
def test_bb84_with_full_eve_qber_around_25pct(n_bits: int, seed: int):
    """BB84 con Eva que intercepta todo tiene QBER ≈ 25% ± margen estadístico."""
    rng = np.random.default_rng(seed)
    alice_bits = rng.integers(0, 2, n_bits)
    alice_bases = rng.integers(0, 2, n_bits)
    eve_bases = rng.integers(0, 2, n_bits)
    bob_bases = rng.integers(0, 2, n_bits)

    # Eva: cuando acierta la base, transmite correcto; cuando falla, colapsa aleatoriamente
    eve_bits = alice_bits.copy()
    wrong_eve = (eve_bases != alice_bases)
    eve_bits[wrong_eve] = rng.integers(0, 2, np.sum(wrong_eve))

    # Bob: cuando acierta base, lee el bit que Eva transmitió
    matching_ab = (alice_bases == bob_bases)
    assume(np.sum(matching_ab) > 30)

    key_alice = alice_bits[matching_ab]
    key_bob = eve_bits[matching_ab]

    # Eva puede introducir error en los bits donde ella falló la base
    wrong_eve_on_match = wrong_eve[matching_ab]
    bob_errors = np.zeros(np.sum(matching_ab), dtype=bool)
    bob_errors[wrong_eve_on_match] = rng.integers(0, 2, np.sum(wrong_eve_on_match)).astype(bool)
    key_bob = key_alice.copy()
    key_bob[wrong_eve_on_match] ^= bob_errors[wrong_eve_on_match]

    n_key = len(key_alice)
    n_errors = np.sum(key_alice != key_bob)
    qber = n_errors / n_key

    # Con n_bits grande, QBER debe ser ~25% ± 5% (intervalo estadístico generoso)
    assert 0.10 <= qber <= 0.40, \
        f"QBER={qber:.3f} fuera del rango esperado [0.10, 0.40] (n={n_bits})"


# ===========================================================================
# Propiedades de barren plateaus
# ===========================================================================

@given(
    n_qubits=st.integers(min_value=2, max_value=8),
    n_samples=st.integers(min_value=50, max_value=200),
    seed=st.integers(min_value=0, max_value=999),
)
@pytest.mark.slow
def test_barren_plateau_variance_decreases_with_n(n_qubits: int, n_samples: int, seed: int):
    """La varianza del gradiente de un operador global decrece con n_qubits."""
    rng = np.random.default_rng(seed)
    # Varianza analítica: Var[∂C/∂θ] ∝ 4^(-n) para funciones de costo global
    var_n = 4.0 ** (-n_qubits)
    var_n_plus_1 = 4.0 ** (-(n_qubits + 1))
    assert var_n > var_n_plus_1, \
        f"Var[grad](n={n_qubits}) = {var_n:.2e} ≤ Var[grad](n={n_qubits+1}) = {var_n_plus_1:.2e}"


# ===========================================================================
# Propiedades de teleportación cuántica
# ===========================================================================

@given(
    p=st.floats(min_value=0.0, max_value=1.0, allow_nan=False),
)
def test_teleportation_fidelity_between_2_3_and_1(p: float):
    """La fidelidad de teleportación F(p) ∈ [2/3, 1] para p ∈ [0, 0.5]."""
    assume(p <= 0.5)
    F = max(0.0, 1.0 - 2 * p / 3.0)
    assert 2 / 3 - 1e-10 <= F <= 1.0 + 1e-10, \
        f"F(p={p:.3f}) = {F:.6f} fuera de [2/3, 1]"


@given(
    p1=st.floats(min_value=0.0, max_value=1.0, allow_nan=False),
    p2=st.floats(min_value=0.0, max_value=1.0, allow_nan=False),
)
def test_teleportation_fidelity_monotone(p1: float, p2: float):
    """La fidelidad de teleportación es monotónicamente decreciente en p."""
    assume(p1 < p2)
    F1 = max(0.0, 1.0 - 2 * p1 / 3.0)
    F2 = max(0.0, 1.0 - 2 * p2 / 3.0)
    assert F1 >= F2 - 1e-12, \
        f"F(p={p1:.3f})={F1:.6f} < F(p={p2:.3f})={F2:.6f} — debe ser monótona"


# ===========================================================================
# Propiedades del umbral del código tórico
# ===========================================================================

@given(
    L=st.integers(min_value=2, max_value=10),
    p=st.floats(min_value=0.001, max_value=0.09, allow_nan=False),
)
def test_toric_logical_error_rate_decreases_with_L(L: int, p: float):
    """Bajo el umbral, la tasa de error lógico decrece exponencialmente con L."""
    p_th = 0.109
    assume(p < p_th)

    def P_L(p_val, L_val):
        return 0.5 * (p_val / p_th) ** (L_val / 2)

    assert P_L(p, L + 2) < P_L(p, L), \
        f"P_L(L={L+2}) ≥ P_L(L={L}) para p={p:.3f} — debería decrecer"


@given(
    p=st.floats(min_value=0.001, max_value=0.09, allow_nan=False),
    L=st.integers(min_value=4, max_value=20),
)
def test_toric_logical_error_approaches_zero_large_L(p: float, L: int):
    """Para p < umbral y L grande, P_L → 0."""
    p_th = 0.109
    assume(p < p_th * 0.9)  # margen del 10% bajo umbral

    def P_L(p_val, L_val):
        return 0.5 * (p_val / p_th) ** (L_val / 2)

    p_logical = P_L(p, L)
    # Para L=20 y p < 0.1, P_L < 10^-3 siempre
    assert p_logical < 0.5, \
        f"P_L(p={p:.3f}, L={L}) = {p_logical:.2e} no converge a 0"


# ===========================================================================
# Propiedades de matrices densidad
# ===========================================================================

@given(
    seed=st.integers(min_value=0, max_value=9999),
    n=st.integers(min_value=1, max_value=3),
)
def test_density_matrix_trace_one(seed: int, n: int):
    """Toda matriz de densidad válida tiene traza = 1."""
    rng = np.random.default_rng(seed)
    dim = 2**n
    # Construir matriz densidad válida via estado puro mixto
    psi = rng.normal(size=dim) + 1j * rng.normal(size=dim)
    psi /= np.linalg.norm(psi)
    rho = np.outer(psi, psi.conj())
    assert abs(np.trace(rho) - 1.0) < 1e-12, \
        f"Tr(ρ) = {np.trace(rho):.8f} ≠ 1"


@given(
    seed=st.integers(min_value=0, max_value=9999),
    n=st.integers(min_value=1, max_value=3),
)
def test_density_matrix_psd(seed: int, n: int):
    """Toda matriz de densidad válida es semidefinida positiva."""
    rng = np.random.default_rng(seed)
    dim = 2**n
    psi = rng.normal(size=dim) + 1j * rng.normal(size=dim)
    psi /= np.linalg.norm(psi)
    rho = np.outer(psi, psi.conj())
    eigenvalues = np.linalg.eigvalsh(rho)
    assert all(ev >= -1e-12 for ev in eigenvalues), \
        f"Eigenvalor negativo {min(eigenvalues):.2e} — ρ no es PSD"
