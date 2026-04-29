"""
Tests para iDMRG y gravedad cuántica — Fase 17.

Verifica propiedades de la cadena de Heisenberg, DMRG blocks,
iDMRG convergencia y entrelazamiento.

Cobertura: Módulo 43, Lab 47.
"""

import numpy as np
import pytest
from scipy.linalg import eigh, svd
from scipy.sparse import kron as skron, eye as speye
from dataclasses import dataclass


# ── Operadores de Pauli ──────────────────────────────────────────────────────

I2 = np.eye(2)
Sx = np.array([[0., 1.], [1., 0.]]) / 2
Sy = np.array([[0., -1j], [1j, 0.]]) / 2
Sz = np.array([[1., 0.], [0., -1.]]) / 2


# ── Hamiltoniano de Heisenberg (duplicado del lab) ────────────────────────────

def heisenberg_hamiltonian(n: int, J: float = 1.0, periodic: bool = False) -> np.ndarray:
    dim = 2**n
    H = np.zeros((dim, dim), dtype=complex)

    def embed(op1, op2, k, n):
        ops = [I2] * n
        ops[k] = op1
        ops[k + 1] = op2
        result = ops[0]
        for op in ops[1:]:
            result = np.kron(result, op)
        return result

    bonds = list(range(n - 1))
    if periodic:
        bonds.append(n - 1)

    for k in bonds:
        k1 = k % n
        k2 = (k + 1) % n
        if k < n - 1:
            H += J * (embed(Sx, Sx, k1, n) * 4 +
                      embed(Sy, Sy, k1, n) * 4 +
                      embed(Sz, Sz, k1, n) * 4)
    return np.real(H)


def exact_ground_energy(n: int, J: float = 1.0):
    H = heisenberg_hamiltonian(n, J)
    evals, evecs = eigh(H)
    return float(evals[0]), evecs[:, 0]


# ── DMRG blocks (duplicado del lab) ──────────────────────────────────────────

@dataclass
class DMRGBlock:
    length: int
    basis_size: int
    H: np.ndarray
    Sp: np.ndarray
    Sm: np.ndarray
    Sz: np.ndarray


def initial_block() -> DMRGBlock:
    Sp = np.array([[0., 1.], [0., 0.]])
    Sm = np.array([[0., 0.], [1., 0.]])
    Sz_op = np.array([[0.5, 0.], [0., -0.5]])
    return DMRGBlock(1, 2, np.zeros((2, 2)), Sp, Sm, Sz_op)


def enlarge_block(block: DMRGBlock, J: float = 1.0) -> DMRGBlock:
    d = 2
    m = block.basis_size
    Sp_s = np.array([[0., 1.], [0., 0.]])
    Sm_s = np.array([[0., 0.], [1., 0.]])
    Sz_s = np.array([[0.5, 0.], [0., -0.5]])

    H_new = np.kron(block.H, np.eye(d)) + J * (
        0.5 * np.kron(block.Sp, Sm_s) +
        0.5 * np.kron(block.Sm, Sp_s) +
        np.kron(block.Sz, Sz_s)
    )
    return DMRGBlock(
        block.length + 1,
        m * d,
        H_new,
        np.kron(np.eye(m), Sp_s),
        np.kron(np.eye(m), Sm_s),
        np.kron(np.eye(m), Sz_s),
    )


def truncate_block(block: DMRGBlock, psi_gs: np.ndarray, m_left: int, m_right: int, chi: int) -> DMRGBlock:
    psi_mat = psi_gs.reshape(m_left, m_right)
    rho = psi_mat @ psi_mat.conj().T
    evals, evecs = eigh(rho)
    idx = np.argsort(evals)[::-1]
    chi_actual = min(chi, len(evals))
    T = evecs[:, idx[:chi_actual]]
    return DMRGBlock(
        block.length,
        chi_actual,
        T.conj().T @ block.H @ T,
        T.conj().T @ block.Sp @ T,
        T.conj().T @ block.Sm @ T,
        T.conj().T @ block.Sz @ T,
    )


def idmrg(n_sites: int, chi: int = 20, J: float = 1.0):
    block_L = initial_block()
    block_R = initial_block()
    energies = []

    for step in range(n_sites // 2 - 1):
        block_L = enlarge_block(block_L, J)
        block_R = enlarge_block(block_R, J)
        m_L, m_R = block_L.basis_size, block_R.basis_size

        H_super = (np.kron(block_L.H, np.eye(m_R)) +
                   np.kron(np.eye(m_L), block_R.H) +
                   J * (0.5 * np.kron(block_L.Sp, block_R.Sm) +
                        0.5 * np.kron(block_L.Sm, block_R.Sp) +
                        np.kron(block_L.Sz, block_R.Sz)))

        evals, evecs = eigh(H_super)
        E0 = evals[0]
        psi_gs = evecs[:, 0]

        n_total = 2 * (step + 2)
        energies.append((n_total, E0, E0 / n_total))

        block_L = truncate_block(block_L, psi_gs, m_L, m_R, chi)
        block_R = truncate_block(block_R, psi_gs.reshape(m_L, m_R).T.flatten(), m_R, m_L, chi)

    return energies, block_L, block_R


# ── Tests: Hamiltoniano de Heisenberg ────────────────────────────────────────

def test_heisenberg_hermitian():
    """H debe ser Hermitiano."""
    H = heisenberg_hamiltonian(4)
    assert np.allclose(H, H.T), "Hamiltoniano no es hermitiano"


def test_heisenberg_dimension():
    """Dimensión de H debe ser 2^n × 2^n."""
    for n in [2, 3, 4]:
        H = heisenberg_hamiltonian(n)
        assert H.shape == (2**n, 2**n)


def test_heisenberg_ground_energy_antiferromagnetic():
    """Estado fundamental AFM (J>0) debe tener energía negativa."""
    E0, _ = exact_ground_energy(4, J=1.0)
    assert E0 < 0


def test_heisenberg_n2_exact():
    """Para n=2 (singlete) E0 = -3 en la convención 4·S⊗S = σ⊗σ del lab."""
    E0, _ = exact_ground_energy(2, J=1.0)
    # La función usa 4*Sx⊗Sx + ... = σx⊗σx + ...; singlete → E = -3
    assert abs(E0 - (-3.0)) < 1e-10


def test_ground_state_normalized():
    """Vector de estado fundamental debe estar normalizado."""
    _, psi0 = exact_ground_energy(6)
    assert abs(np.dot(psi0, psi0) - 1.0) < 1e-12


def test_heisenberg_ferromagnetic_positive():
    """Para J<0 (ferromagnético) el estado fundamental tiene energía < 0."""
    E0, _ = exact_ground_energy(4, J=-1.0)
    assert E0 < 0


# ── Tests: DMRG blocks ───────────────────────────────────────────────────────

def test_initial_block_shape():
    """initial_block debe tener basis_size=2 y H=0."""
    b = initial_block()
    assert b.basis_size == 2
    assert b.length == 1
    assert np.allclose(b.H, 0)


def test_enlarge_block_basis_growth():
    """Cada enlarge_block duplica el basis_size hasta chi."""
    b = initial_block()
    b2 = enlarge_block(b)
    assert b2.basis_size == 4
    assert b2.length == 2
    b3 = enlarge_block(b2)
    assert b3.basis_size == 8


def test_enlarged_block_hermitian():
    """H del bloque ampliado debe ser Hermitiano."""
    b = enlarge_block(enlarge_block(initial_block()))
    assert np.allclose(b.H, b.H.T)


def test_truncate_block_reduces_basis():
    """truncate_block con chi pequeño reduce el basis_size."""
    b = initial_block()
    for _ in range(3):
        b = enlarge_block(b)
    # Diagonalizar superbloque trivial para obtener psi_gs
    m = b.basis_size
    H_super = np.kron(b.H, np.eye(m)) + np.kron(np.eye(m), b.H)
    evals, evecs = eigh(H_super)
    psi_gs = evecs[:, 0]
    b_trunc = truncate_block(b, psi_gs, m, m, chi=4)
    assert b_trunc.basis_size <= 4


# ── Tests: iDMRG convergencia ─────────────────────────────────────────────────

def test_idmrg_energy_negative():
    """iDMRG debe producir energía por sitio negativa (AFM)."""
    energies, _, _ = idmrg(n_sites=8, chi=8)
    E_per_site = energies[-1][2]
    assert E_per_site < 0


def test_idmrg_converges_toward_bethe():
    """E0/n de iDMRG debe acercarse al límite de Bethe (≈ -0.4431) para chi grande."""
    E_bethe = -(np.log(2) - 0.25)
    energies, _, _ = idmrg(n_sites=20, chi=32)
    E_per_site = energies[-1][2]
    # Dentro del 5% del límite termodinámico para un sistema finito
    assert abs(E_per_site - E_bethe) < 0.05 * abs(E_bethe)


def test_idmrg_energy_sign_consistent():
    """E0/n de iDMRG debe ser negativa y menor que -0.3 (cadena AFM moderada)."""
    energies, _, _ = idmrg(n_sites=10, chi=16)
    E_per_site = energies[-1][2]
    # En la convención S·S con S=σ/2, E0/n → -0.4431 (Bethe)
    assert E_per_site < -0.3


def test_idmrg_larger_chi_lower_energy():
    """Mayor chi debe dar energía más baja (variacional)."""
    energies_small, _, _ = idmrg(n_sites=12, chi=4)
    energies_large, _, _ = idmrg(n_sites=12, chi=16)

    E_small = energies_small[-1][2]
    E_large = energies_large[-1][2]
    # Energía más negativa = menor variacionalmente
    assert E_large <= E_small + 1e-6
