"""
Tests para Tensor Networks — Fase 16.

Verifica propiedades de MPS, entropía de entrelazamiento, Schmidt values
y la implementación de TEBD para la cadena XX.

Cobertura: Módulo 42, Lab 46.
"""

import numpy as np
import pytest
from scipy.linalg import svd


# ── Utilidades (duplicadas del lab para independencia) ──────────────────────

def schmidt_values(psi: np.ndarray, cut: int) -> np.ndarray:
    n = int(np.log2(len(psi)))
    M = psi.reshape(2**cut, 2**(n - cut))
    _, S, _ = svd(M, full_matrices=False)
    return S


def entanglement_entropy(psi: np.ndarray, cut: int) -> float:
    S = schmidt_values(psi, cut)
    lam2 = S**2
    lam2 = lam2[lam2 > 1e-14]
    return float(-np.sum(lam2 * np.log2(lam2))) if len(lam2) > 0 else 0.0


def mps_from_statevector(psi: np.ndarray, max_chi: int = None, tol: float = 1e-12) -> list:
    """Descomposición MPS por SVD recursiva con truncamiento de valores singulares nulos."""
    n = int(np.log2(len(psi)))
    d = 2
    tensors = []
    mat = psi.reshape(1, -1)
    for k in range(n - 1):
        chi_L = mat.shape[0]
        mat = mat.reshape(chi_L * d, -1)
        U, S, Vh = svd(mat, full_matrices=False)
        # Truncar valores singulares nulos
        nnz = int(np.sum(S > tol * S[0])) if S[0] > 0 else 1
        chi = nnz
        if max_chi is not None:
            chi = min(chi, max_chi)
        chi = max(chi, 1)
        U, S, Vh = U[:, :chi], S[:chi], Vh[:chi, :]
        tensors.append(U.reshape(chi_L, d, chi))
        mat = np.diag(S) @ Vh
    tensors.append(mat.reshape(mat.shape[0], d, 1))
    return tensors


def mps_to_statevector(tensors: list) -> np.ndarray:
    """Reconstruye estado contrayendo todos los tensores del MPS."""
    result = tensors[0]
    for t in tensors[1:]:
        result = np.tensordot(result, t, axes=([-1], [0]))
    return result.flatten()


# ===========================================================================
# 1. Propiedades del estado producto (χ=1)
# ===========================================================================

def test_product_state_mps_bond_dim_one():
    """|0000⟩ en MPS tiene bond dimension 1 (sin entrelazamiento)."""
    n = 4
    psi = np.zeros(2**n)
    psi[0] = 1.0
    tensors = mps_from_statevector(psi)
    max_chi = max(t.shape[-1] for t in tensors)
    assert max_chi == 1, f"Estado producto: χ_max = {max_chi} ≠ 1"


def test_product_state_zero_entropy():
    """|0000⟩ tiene entropía de entrelazamiento = 0 en todos los cortes."""
    n = 4
    psi = np.zeros(2**n)
    psi[0] = 1.0
    for cut in range(1, n):
        S = entanglement_entropy(psi, cut)
        assert abs(S) < 1e-12, f"Corte {cut}: S = {S:.2e} ≠ 0"


def test_neel_state_mps_bond_dim_one():
    """Estado de Néel |0101⟩ es estado producto, χ=1."""
    n = 4
    idx = int('0101', 2)
    psi = np.zeros(2**n)
    psi[idx] = 1.0
    tensors = mps_from_statevector(psi)
    max_chi = max(t.shape[-1] for t in tensors)
    assert max_chi == 1, f"Néel: χ_max = {max_chi} ≠ 1"


# ===========================================================================
# 2. Estado GHZ — χ = 2
# ===========================================================================

def test_ghz_state_mps_bond_dim_two():
    """Estado GHZ tiene bond dimension exactamente 2."""
    n = 4
    psi = np.zeros(2**n)
    psi[0] = psi[-1] = 1.0 / np.sqrt(2)
    tensors = mps_from_statevector(psi)
    max_chi = max(t.shape[-1] for t in tensors)
    assert max_chi == 2, f"GHZ: χ_max = {max_chi} ≠ 2"


def test_ghz_state_entropy_one_ebit():
    """Estado GHZ tiene entropía S = 1 ebit en el corte central."""
    n = 4
    psi = np.zeros(2**n)
    psi[0] = psi[-1] = 1.0 / np.sqrt(2)
    S = entanglement_entropy(psi, n // 2)
    assert abs(S - 1.0) < 1e-10, f"GHZ entropía: S = {S:.6f} ≠ 1"


# ===========================================================================
# 3. Reconstrucción exacta desde MPS
# ===========================================================================

def test_mps_reconstruction_exact():
    """MPS exacto (sin truncar) reconstruye el estado con fidelidad 1."""
    rng = np.random.default_rng(42)
    n = 5
    psi = rng.normal(size=2**n) + 1j * rng.normal(size=2**n)
    psi /= np.linalg.norm(psi)

    tensors = mps_from_statevector(psi)
    psi_rec = mps_to_statevector(tensors)
    psi_rec /= np.linalg.norm(psi_rec)

    fidelity = abs(np.dot(psi.conj(), psi_rec))**2
    assert fidelity > 1 - 1e-10, f"Fidelidad de reconstrucción: {fidelity:.10f}"


def test_mps_truncation_monotone_fidelity():
    """Aumentar χ_max sólo puede mejorar (o mantener) la fidelidad de aproximación."""
    rng = np.random.default_rng(7)
    n = 6
    psi = rng.normal(size=2**n) + 1j * rng.normal(size=2**n)
    psi /= np.linalg.norm(psi)

    prev_fid = 0.0
    for chi in [1, 2, 4, 8, 16]:
        tensors = mps_from_statevector(psi, max_chi=chi)
        psi_approx = mps_to_statevector(tensors)
        norm = np.linalg.norm(psi_approx)
        if norm > 1e-10:
            psi_approx /= norm
        fid = abs(np.dot(psi.conj(), psi_approx))**2
        assert fid >= prev_fid - 1e-9, \
            f"Fidelidad no monótona: fid(χ={chi}) = {fid:.6f} < fid_prev = {prev_fid:.6f}"
        prev_fid = fid


# ===========================================================================
# 4. Propiedades de la entropía de entrelazamiento
# ===========================================================================

def test_entropy_nonnegative():
    """Entropía de entrelazamiento siempre ≥ 0."""
    rng = np.random.default_rng(0)
    n = 5
    for _ in range(10):
        psi = rng.normal(size=2**n) + 1j * rng.normal(size=2**n)
        psi /= np.linalg.norm(psi)
        for cut in range(1, n):
            S = entanglement_entropy(psi, cut)
            assert S >= -1e-12, f"Entropía negativa: S(corte={cut}) = {S:.2e}"


def test_entropy_bounded_by_log_dim():
    """Entropía S ≤ min(cut, n-cut) para n qubits."""
    rng = np.random.default_rng(1)
    n = 4
    for _ in range(5):
        psi = rng.normal(size=2**n) + 1j * rng.normal(size=2**n)
        psi /= np.linalg.norm(psi)
        for cut in range(1, n):
            S = entanglement_entropy(psi, cut)
            max_S = min(cut, n - cut)
            assert S <= max_S + 1e-10, \
                f"Entropía {S:.4f} > máximo teórico {max_S} para corte={cut}"


def test_schmidt_values_sum_to_one():
    """Los valores de Schmidt al cuadrado suman 1 (norma del estado)."""
    rng = np.random.default_rng(2)
    n = 4
    psi = rng.normal(size=2**n) + 1j * rng.normal(size=2**n)
    psi /= np.linalg.norm(psi)

    for cut in range(1, n):
        S = schmidt_values(psi, cut)
        total = np.sum(S**2)
        assert abs(total - 1.0) < 1e-12, \
            f"Σλ_k² = {total:.10f} ≠ 1 para corte={cut}"


# ===========================================================================
# 5. Propiedades del bond dimension y area law
# ===========================================================================

def test_random_state_max_bond_dim():
    """El bond dimension máximo exacto de un estado aleatorio de n qubits es 2^(n//2)."""
    rng = np.random.default_rng(3)
    for n in [4, 5, 6]:
        psi = rng.normal(size=2**n) + 1j * rng.normal(size=2**n)
        psi /= np.linalg.norm(psi)
        tensors = mps_from_statevector(psi)
        max_chi = max(t.shape[-1] for t in tensors)
        expected_max = 2**(n // 2)
        assert max_chi <= expected_max, \
            f"n={n}: χ_max = {max_chi} > 2^(n//2) = {expected_max}"


def test_mps_tensor_count():
    """El MPS de n qubits tiene exactamente n tensores."""
    for n in [3, 4, 5, 6]:
        psi = np.zeros(2**n)
        psi[0] = 1.0
        tensors = mps_from_statevector(psi)
        assert len(tensors) == n, f"MPS n={n}: {len(tensors)} tensores ≠ {n}"


def test_mps_physical_dimension():
    """Cada tensor del MPS tiene dimensión física d=2."""
    n = 5
    rng = np.random.default_rng(4)
    psi = rng.normal(size=2**n)
    psi /= np.linalg.norm(psi)
    tensors = mps_from_statevector(psi)
    for k, t in enumerate(tensors):
        assert t.shape[1] == 2, f"Tensor {k}: dimensión física {t.shape[1]} ≠ 2"


# ===========================================================================
# 6. Evolución temporal — conservación de la norma
# ===========================================================================

def test_tebd_norm_conservation():
    """La norma se conserva durante la evolución TEBD de la cadena XX."""
    from scipy.linalg import expm

    n = 4
    J = 1.0
    dt = 0.1

    # Puerta XX de 2 qubits
    XX_YY = np.array([[0,0,0,0],[0,0,2,0],[0,2,0,0],[0,0,0,0]], dtype=complex)
    gate = expm(-1j * (-J * XX_YY / 2) * dt)

    # Estado inicial: Néel |0101⟩
    idx = int('0101', 2)
    psi = np.zeros(2**n, dtype=complex)
    psi[idx] = 1.0

    def apply_gate(psi, k, n, gate):
        psi_r = psi.reshape([2]*n)
        psi_r = np.tensordot(gate.reshape(2,2,2,2), psi_r, axes=([2,3],[k,k+1]))
        order = list(range(2, k+2)) + [0,1] + list(range(k+2, n))
        return np.transpose(psi_r, order).flatten()

    for step in range(10):
        for k in range(0, n-1, 2):
            psi = apply_gate(psi, k, n, gate)
        for k in range(1, n-1, 2):
            psi = apply_gate(psi, k, n, gate)

    norm_final = np.linalg.norm(psi)
    assert abs(norm_final - 1.0) < 1e-10, \
        f"Norma tras TEBD: {norm_final:.10f} ≠ 1 (no conservada)"
