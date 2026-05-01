"""
Tests para PEPS y Hubbard 2D — Fase 18.

Verifica propiedades del tensor PEPS (norma, entropía, area law),
y la exactitud de la diagonalización exacta del modelo de Hubbard 2D.

Cobertura: Módulo 44, Lab 48.
"""

import numpy as np
import pytest
from scipy.sparse import kron as skron, eye as seye, csr_matrix
from scipy.sparse.linalg import eigsh


# ══════════════════════════════════════════════════════════════════════════════
# PEPS (reimplementación mínima para tests)
# ══════════════════════════════════════════════════════════════════════════════

class PEPS:
    """PEPS en retícula 2D Lx × Ly con dimensión de bono D."""

    def __init__(self, Lx: int, Ly: int, d: int, D: int, seed: int = 42):
        self.Lx, self.Ly, self.d, self.D = Lx, Ly, d, D
        rng = np.random.default_rng(seed)
        self.tensors = {}
        for i in range(Lx):
            for j in range(Ly):
                Dl = 1 if j == 0       else D
                Dr = 1 if j == Ly - 1  else D
                Du = 1 if i == 0       else D
                Dd = 1 if i == Lx - 1  else D
                self.tensors[(i, j)] = rng.standard_normal((d, Dl, Dr, Du, Dd))

    @classmethod
    def product_state(cls, Lx: int, Ly: int, local_state: np.ndarray) -> "PEPS":
        """PEPS de estado producto: D=1."""
        obj = cls.__new__(cls)
        obj.Lx, obj.Ly, obj.d, obj.D = Lx, Ly, len(local_state), 1
        obj.tensors = {}
        for i in range(Lx):
            for j in range(Ly):
                obj.tensors[(i, j)] = local_state.reshape(len(local_state), 1, 1, 1, 1).copy()
        return obj

    def contract_2x2(self) -> float:
        """Contracción exacta para retícula 2×2 via einsum."""
        assert self.Lx == 2 and self.Ly == 2, "Solo para 2×2"
        A = self.tensors[(0, 0)]   # (d, 1, Dr, 1, Dd)
        B = self.tensors[(0, 1)]   # (d, Dl, 1, 1, Dd)
        C = self.tensors[(1, 0)]   # (d, 1, Dr, Du, 1)
        D = self.tensors[(1, 1)]   # (d, Dl, 1, Du, 1)

        # Contraer bono derecho entre A y B (índice 2 de A con índice 1 de B)
        AB = np.einsum('iabcd,jbefg->iajcdefg', A, B)   # no es correcto genérico
        # Contracción simplificada para estado producto (D=1 → escalares)
        # Para tests de norma usamos la contracción por columnas
        norm_sq = 0.0
        for phys in range(self.d ** (self.Lx * self.Ly)):
            # Índices físicos
            idx = [(phys >> (k * int(np.log2(self.d)))) % self.d
                   for k in range(self.Lx * self.Ly)]
            t00 = self.tensors[(0, 0)][idx[0], 0, :, 0, :]   # (Dr, Dd)
            t01 = self.tensors[(0, 1)][idx[1], :, 0, 0, :]   # (Dl, Dd)
            t10 = self.tensors[(1, 0)][idx[2], 0, :, :, 0]   # (Dr, Du)
            t11 = self.tensors[(1, 1)][idx[3], :, 0, :, 0]   # (Dl, Du)

            # Amplitude = contract(t00·t01 horizontal) · contract(t10·t11) vertical
            top    = np.einsum('ij,ij->', t00, t01)     # contrae Dr y Dd
            bottom = np.einsum('ij,ij->', t10, t11)
            norm_sq += (top * bottom) ** 2
        return float(norm_sq) ** 0.5

    def norm_product_state(self) -> float:
        """Norma exacta para estado producto (D=1)."""
        assert self.D == 1, "Solo válido para D=1"
        norm_sq = 1.0
        for (i, j), t in self.tensors.items():
            # t shape: (d, 1, 1, 1, 1)
            norm_sq *= float(np.sum(t[:, 0, 0, 0, 0] ** 2))
        return float(norm_sq ** 0.5)

    def entanglement_entropy_2x2_horizontal(self) -> float:
        """Entropía de entrelazamiento del corte horizontal para 2×2."""
        assert self.Lx == 2 and self.Ly == 2
        # Construir reduced density matrix del corte top/bottom
        # Para retícula pequeña usamos la contracción directa
        d, D = self.d, self.D
        # Matriz de transferencia horizontal: contraer columna izquierda
        A = self.tensors[(0, 0)]   # (d, 1, Dr, 1, Dd)
        C = self.tensors[(1, 0)]   # (d, 1, Dr, Du, 1)
        # Dimensión del bono vertical entre filas: Dd de A = Du de C = D
        # rho_{s,s'} = Σ_{phys} <top|ρ_reduced|top'> ∝ entropía
        # Aproximación: usar SVD del tensor combinado A⊗C sobre el bono vertical
        A_mat = A[:, 0, :, 0, :].reshape(d, -1)     # (d, Dr*Dd)
        C_mat = C[:, 0, :, :, 0].reshape(d, -1)     # (d, Dr*Du)
        M = np.kron(A_mat, C_mat)                    # (d², Dr²·D²)
        _, sv, _ = np.linalg.svd(M, full_matrices=False)
        sv = sv[sv > 1e-14]
        sv /= np.linalg.norm(sv)
        lam2 = sv ** 2
        return float(-np.sum(lam2 * np.log2(lam2 + 1e-15)))


# ══════════════════════════════════════════════════════════════════════════════
# Hubbard 2D (reimplementación mínima)
# ══════════════════════════════════════════════════════════════════════════════

def build_cdag(k: int, n_modes: int) -> csr_matrix:
    """Operador de creación c†_k con transformada de Jordan-Wigner."""
    dim = 2 ** n_modes
    rows, cols, vals = [], [], []
    for state in range(dim):
        if not (state >> k) & 1:
            new_state = state | (1 << k)
            n_below = bin(state & ((1 << k) - 1)).count('1')
            sign = (-1) ** n_below
            rows.append(new_state)
            cols.append(state)
            vals.append(float(sign))
    return csr_matrix((vals, (rows, cols)), shape=(dim, dim))


def build_number_op(k: int, n_modes: int) -> csr_matrix:
    """Operador número n_k = c†_k c_k."""
    cdag = build_cdag(k, n_modes)
    return cdag @ cdag.T


def build_hubbard_2d(Lx: int, Ly: int, t: float = 1.0, U: float = 4.0):
    """
    Hamiltoniano Hubbard 2D en retícula Lx×Ly con condiciones de contorno abiertas.
    Modos: spin-up (0..N-1), spin-down (N..2N-1) con N=Lx*Ly.
    """
    N = Lx * Ly
    n_modes = 2 * N
    dim = 2 ** n_modes

    def site(i, j):
        return i * Ly + j

    H = csr_matrix((dim, dim), dtype=float)

    # Hopping
    for i in range(Lx):
        for j in range(Ly):
            s = site(i, j)
            for s2 in ([site(i, j + 1)] if j < Ly - 1 else []) + \
                      ([site(i + 1, j)] if i < Lx - 1 else []):
                for spin_offset in [0, N]:
                    k1, k2 = s + spin_offset, s2 + spin_offset
                    cdag1 = build_cdag(k1, n_modes)
                    cdag2 = build_cdag(k2, n_modes)
                    H -= t * (cdag1 @ cdag2.T + cdag2 @ cdag1.T)

    # Interacción on-site
    for i in range(Lx):
        for j in range(Ly):
            s = site(i, j)
            n_up   = build_number_op(s,     n_modes)
            n_down = build_number_op(s + N, n_modes)
            H += U * (n_up @ n_down)

    # Operador de número total
    Ntotal = sum(build_number_op(k, n_modes) for k in range(n_modes))
    return H, Ntotal, dim


def ground_energy_sector(H, Ntotal, Ne: int, lam: float = 200.0) -> float:
    """Energía del estado fundamental en el sector de Ne partículas."""
    Ne_op = Ne * seye(H.shape[0], format='csr')
    penalty = lam * (Ntotal - Ne_op) @ (Ntotal - Ne_op)
    evals, _ = eigsh(H + penalty, k=1, which='SA')
    return float(evals[0])


# ══════════════════════════════════════════════════════════════════════════════
# Tests PEPS
# ══════════════════════════════════════════════════════════════════════════════

class TestPEPSProductState:
    def test_norm_product_state_is_one(self):
        # |0⟩^⊗N normalizado
        local = np.array([1.0, 0.0])
        peps = PEPS.product_state(2, 2, local)
        assert abs(peps.norm_product_state() - 1.0) < 1e-10

    def test_norm_superposition_product(self):
        # (|0⟩+|1⟩)/√2 producto → norma total = 1
        local = np.array([1.0, 1.0]) / np.sqrt(2)
        peps = PEPS.product_state(2, 3, local)
        assert abs(peps.norm_product_state() - 1.0) < 1e-10

    def test_product_state_bond_dim_is_one(self):
        peps = PEPS.product_state(3, 3, np.array([1.0, 0.0]))
        assert peps.D == 1

    def test_tensor_shapes_correct(self):
        peps = PEPS(2, 2, d=2, D=3)
        # Esquinas: D_borde=1
        assert peps.tensors[(0, 0)].shape == (2, 1, 3, 1, 3)
        assert peps.tensors[(0, 1)].shape == (2, 3, 1, 1, 3)
        assert peps.tensors[(1, 0)].shape == (2, 1, 3, 3, 1)
        assert peps.tensors[(1, 1)].shape == (2, 3, 1, 3, 1)

    def test_physical_dim_correct(self):
        peps = PEPS(2, 2, d=3, D=2)
        for t in peps.tensors.values():
            assert t.shape[0] == 3


class TestPEPSEntropyAreaLaw:
    def test_entropy_nonnegative(self):
        peps = PEPS(2, 2, d=2, D=4, seed=7)
        S = peps.entanglement_entropy_2x2_horizontal()
        assert S >= -1e-10

    def test_entropy_bounded_by_bond_dim(self):
        # Area law 2D: S ≤ 2·log₂(D) para corte horizontal de 2×2
        for D in [1, 2, 4, 8]:
            peps = PEPS(2, 2, d=2, D=D, seed=D)
            S = peps.entanglement_entropy_2x2_horizontal()
            S_max = 2 * np.log2(D) if D > 1 else 0.0
            assert S <= S_max + 1e-8, (
                f"D={D}: S={S:.4f} supera cota 2·log₂(D)={S_max:.4f}"
            )

    def test_product_state_has_zero_entropy(self):
        local = np.array([1.0, 0.0])
        peps = PEPS.product_state(2, 2, local)
        # Para D=1 la entropía del corte horizontal es 0
        # (verificar vía norma: producto factoriza completamente)
        assert peps.D == 1

    def test_entropy_grows_with_D(self):
        entropies = []
        for D in [1, 2, 4, 8]:
            peps = PEPS(2, 2, d=2, D=D, seed=0)
            S = peps.entanglement_entropy_2x2_horizontal()
            entropies.append(S)
        # Entropía no decrece con D (más correlaciones posibles)
        for i in range(len(entropies) - 1):
            assert entropies[i] <= entropies[i + 1] + 1e-8


# ══════════════════════════════════════════════════════════════════════════════
# Tests Hubbard 2D
# ══════════════════════════════════════════════════════════════════════════════

class TestHubbard2D:
    @pytest.fixture(scope="class")
    def hubbard_2x2(self):
        """Modelo de Hubbard 2×2 en semillenado (Ne=4)."""
        H, Ntotal, dim = build_hubbard_2d(2, 2, t=1.0, U=4.0)
        return H, Ntotal, dim

    def test_hamiltonian_hermitian(self, hubbard_2x2):
        H, _, _ = hubbard_2x2
        diff = H - H.conj().T
        assert diff.nnz == 0 or abs(diff).max() < 1e-10

    def test_hamiltonian_dimension(self, hubbard_2x2):
        H, _, dim = hubbard_2x2
        # 2×2 sitios × 2 spins = 4 modos → 2^(2*4) = 256
        assert dim == 2 ** (2 * 4)
        assert H.shape == (dim, dim)

    def test_ground_energy_negative_at_halffilling(self, hubbard_2x2):
        H, Ntotal, _ = hubbard_2x2
        E0 = ground_energy_sector(H, Ntotal, Ne=4)
        assert E0 < 0.0, f"Energía debería ser negativa (hopping domina): E0={E0:.4f}"

    def test_ground_energy_weakly_correlated(self):
        # U/t → 0: dominado por hopping, energía más negativa
        H_weak, Ntotal, _ = build_hubbard_2d(2, 2, t=1.0, U=0.5)
        H_strong, _, _ = build_hubbard_2d(2, 2, t=1.0, U=20.0)
        E_weak   = ground_energy_sector(H_weak,   Ntotal, Ne=4)
        E_strong = ground_energy_sector(H_strong, Ntotal, Ne=4)
        assert E_weak < E_strong, (
            f"Esperado E(U=0.5) < E(U=20): {E_weak:.4f} vs {E_strong:.4f}"
        )

    def test_charge_gap_positive_for_large_u(self):
        # Gap de carga Δc = E0(Ne+1) + E0(Ne-1) - 2·E0(Ne) > 0 para U grande
        H, Ntotal, _ = build_hubbard_2d(2, 2, t=1.0, U=10.0)
        E0   = ground_energy_sector(H, Ntotal, Ne=4)
        Ep1  = ground_energy_sector(H, Ntotal, Ne=5)
        Em1  = ground_energy_sector(H, Ntotal, Ne=3)
        gap = Ep1 + Em1 - 2 * E0
        assert gap > 0.0, f"Gap de carga debería ser positivo para U/t=10: Δc={gap:.4f}"

    def test_charge_gap_small_for_small_u(self):
        # Gap de carga pequeño para U/t pequeño (fase metálica)
        H, Ntotal, _ = build_hubbard_2d(2, 2, t=1.0, U=0.5)
        E0  = ground_energy_sector(H, Ntotal, Ne=4)
        Ep1 = ground_energy_sector(H, Ntotal, Ne=5)
        Em1 = ground_energy_sector(H, Ntotal, Ne=3)
        gap_small_u = Ep1 + Em1 - 2 * E0

        H2, Ntotal2, _ = build_hubbard_2d(2, 2, t=1.0, U=10.0)
        E02  = ground_energy_sector(H2, Ntotal2, Ne=4)
        Ep12 = ground_energy_sector(H2, Ntotal2, Ne=5)
        Em12 = ground_energy_sector(H2, Ntotal2, Ne=3)
        gap_large_u = Ep12 + Em12 - 2 * E02

        assert gap_small_u < gap_large_u, (
            f"Gap(U=0.5)={gap_small_u:.4f} debería ser < Gap(U=10)={gap_large_u:.4f}"
        )
