"""
Tests para computación cuántica fotónica — Fase 19.

Verifica propiedades matemáticas de estados fotónicos, squeezing,
beamsplitter, GBS y función de Wigner sin requerir Strawberry Fields.

Cobertura: Módulo 45, Lab 49.
"""

import numpy as np
import pytest
from math import factorial


# ══════════════════════════════════════════════════════════════════════════════
# Utilidades fotónicas (reimplementación mínima)
# ══════════════════════════════════════════════════════════════════════════════

def fock_state(n: int, dim: int) -> np.ndarray:
    """Estado de Fock |n⟩ en espacio truncado de dimensión dim."""
    v = np.zeros(dim, dtype=complex)
    v[n] = 1.0
    return v


def creation_op(dim: int) -> np.ndarray:
    """Operador de creación a†."""
    a = np.zeros((dim, dim), dtype=complex)
    for n in range(dim - 1):
        a[n + 1, n] = np.sqrt(n + 1)
    return a


def annihilation_op(dim: int) -> np.ndarray:
    """Operador de aniquilación a."""
    return creation_op(dim).conj().T


def number_op(dim: int) -> np.ndarray:
    """Operador número n̂ = a†a."""
    a = annihilation_op(dim)
    return creation_op(dim) @ a


def squeeze_state(r: float, dim: int) -> np.ndarray:
    """Estado squeezed S(r)|0⟩ truncado a dim modos de Fock."""
    sech = 1.0 / np.cosh(r)
    tanh = np.tanh(r)
    state = np.zeros(dim, dtype=complex)
    for n in range(0, dim, 2):
        state[n] = ((-tanh) ** (n // 2) * np.sqrt(factorial(n))
                    / (2 ** (n // 2) * factorial(n // 2))) * np.sqrt(sech)
    norm = np.linalg.norm(state)
    return state / norm


def coherent_state(alpha: complex, dim: int) -> np.ndarray:
    """Estado coherente |α⟩ truncado a dim."""
    state = np.zeros(dim, dtype=complex)
    for n in range(dim):
        state[n] = (alpha ** n / np.sqrt(factorial(n))) * np.exp(-abs(alpha) ** 2 / 2)
    return state


def beamsplitter(state_a: np.ndarray, state_b: np.ndarray, theta: float) -> tuple:
    """Beamsplitter 50:50 aplicado a dos estados de un modo."""
    t = np.cos(theta)
    r = np.sin(theta)
    new_a = t * state_a + r * state_b
    new_b = -r * state_a + t * state_b
    return new_a / np.linalg.norm(new_a), new_b / np.linalg.norm(new_b)


def mean_photon_number(state: np.ndarray) -> float:
    """Número medio de fotones ⟨n̂⟩."""
    dim = len(state)
    n_op = number_op(dim)
    return float(np.real(state.conj() @ n_op @ state))


def quadrature_variance(state: np.ndarray) -> tuple:
    """Varianza de cuadraturas X = (a + a†)/2 y P = (a - a†)/2i."""
    dim = len(state)
    a = annihilation_op(dim)
    ad = creation_op(dim)
    X = 0.5 * (a + ad)
    P = 0.5j * (ad - a)

    ex = np.real(state.conj() @ X @ state)
    ep = np.real(state.conj() @ P @ state)
    ex2 = np.real(state.conj() @ (X @ X) @ state)
    ep2 = np.real(state.conj() @ (P @ P) @ state)

    var_x = ex2 - ex ** 2
    var_p = ep2 - ep ** 2
    return var_x, var_p


def hafnian_2x2(A: np.ndarray) -> complex:
    """Hafnian de matriz 2×2 simétrica: haf(A) = A[0,1]."""
    assert A.shape == (2, 2)
    return A[0, 1]


def hafnian_4x4(A: np.ndarray) -> complex:
    """Hafnian de matriz 4×4 simétrica por suma sobre perfect matchings."""
    assert A.shape == (4, 4)
    return A[0, 1] * A[2, 3] + A[0, 2] * A[1, 3] + A[0, 3] * A[1, 2]


def wigner_value(state: np.ndarray, alpha: complex, dim: int | None = None) -> float:
    """Función de Wigner W(α) por fórmula de Cahill-Glauber truncada."""
    if dim is None:
        dim = len(state)
    rho = np.outer(state, state.conj())
    # Matriz de desplazamiento truncada D(α)
    a = annihilation_op(dim)
    ad = creation_op(dim)
    # Aproximación: usar paridad del estado desplazado
    # W(α) = (2/π) Tr[ρ D(α) Π D†(α)] donde Π = (-1)^n̂
    parity = np.diag([(-1) ** n for n in range(dim)])
    # Operador desplazamiento truncado
    arg = alpha * ad - np.conj(alpha) * a
    # Exponencial truncada (orden 10 suficiente para |α| pequeño)
    D = np.eye(dim, dtype=complex)
    term = np.eye(dim, dtype=complex)
    for k in range(1, 12):
        term = term @ arg / k
        D += term
    W = (2 / np.pi) * np.real(np.trace(rho @ D @ parity @ D.conj().T))
    return W


def cat_state(alpha: float, dim: int) -> np.ndarray:
    """Estado gato |α⟩ + |-α⟩ normalizado."""
    ca = coherent_state(alpha, dim)
    cna = coherent_state(-alpha, dim)
    state = ca + cna
    return state / np.linalg.norm(state)


# ══════════════════════════════════════════════════════════════════════════════
# Tests
# ══════════════════════════════════════════════════════════════════════════════

class TestEstadosFock:
    def test_fock_norm(self):
        for n in range(5):
            v = fock_state(n, 10)
            assert abs(np.linalg.norm(v) - 1.0) < 1e-12

    def test_vacuum_photon_number(self):
        v = fock_state(0, 10)
        assert abs(mean_photon_number(v)) < 1e-12

    def test_fock_n_photon_number(self):
        for n in range(1, 6):
            v = fock_state(n, 12)
            assert abs(mean_photon_number(v) - n) < 1e-10


class TestSqueezing:
    def test_squeezing_reduces_x_variance(self):
        """El squeezing r > 0 reduce la varianza de X por debajo del vacío (1/4)."""
        vacuum = fock_state(0, 20)
        var_x_vac, _ = quadrature_variance(vacuum)

        squeezed = squeeze_state(0.5, 20)
        var_x_sq, _ = quadrature_variance(squeezed)

        assert var_x_sq < var_x_vac

    def test_squeezing_increases_p_variance(self):
        """El squeezing comprime X pero amplifica P: Var(X)·Var(P) ≥ 1/16."""
        squeezed = squeeze_state(0.5, 20)
        var_x, var_p = quadrature_variance(squeezed)
        assert var_p > 0.25  # mayor que el vacío
        assert var_x * var_p >= 1 / 16 - 1e-6  # principio de incertidumbre

    def test_uncertainty_principle_saturated(self):
        """El vacío satura el principio de incertidumbre: Var(X)·Var(P) = 1/16."""
        vacuum = fock_state(0, 20)
        var_x, var_p = quadrature_variance(vacuum)
        assert abs(var_x * var_p - 1 / 16) < 1e-4


class TestBeamsplitter:
    def test_beamsplitter_50_50_conserves_mean_photons(self):
        """BS 50:50 conserva el número medio total de fotones."""
        dim = 15
        alpha = 1.5
        state_a = coherent_state(alpha, dim)
        state_b = fock_state(0, dim)

        n_before = mean_photon_number(state_a) + mean_photon_number(state_b)
        state_a2, state_b2 = beamsplitter(state_a, state_b, np.pi / 4)
        n_after = mean_photon_number(state_a2) + mean_photon_number(state_b2)

        assert abs(n_after - n_before) < 0.1

    def test_beamsplitter_output_normalized(self):
        dim = 12
        state_a = coherent_state(1.0, dim)
        state_b = coherent_state(0.5, dim)
        a2, b2 = beamsplitter(state_a, state_b, np.pi / 4)
        assert abs(np.linalg.norm(a2) - 1.0) < 1e-10
        assert abs(np.linalg.norm(b2) - 1.0) < 1e-10


class TestHafnian:
    def test_hafnian_2x2(self):
        """haf([[0, a], [a, 0]]) = a."""
        A = np.array([[0, 2.5], [2.5, 0]])
        assert abs(hafnian_2x2(A) - 2.5) < 1e-12

    def test_hafnian_4x4_identity_matching(self):
        """haf de matriz constante 4×4 con 0 en diagonal."""
        A = np.array([[0, 1, 1, 1],
                      [1, 0, 1, 1],
                      [1, 1, 0, 1],
                      [1, 1, 1, 0]], dtype=float)
        h = hafnian_4x4(A)
        assert abs(h - 3.0) < 1e-12

    def test_hafnian_zero_matrix(self):
        A = np.zeros((2, 2))
        assert abs(hafnian_2x2(A)) < 1e-12


class TestGBSSuperPoissonian:
    def test_coherent_state_poissonian(self):
        """Estado coherente: Var(n̂) = ⟨n̂⟩ (distribución de Poisson)."""
        dim = 30
        alpha = 2.0
        state = coherent_state(alpha, dim)

        a = annihilation_op(dim)
        ad = creation_op(dim)
        n_op = number_op(dim)
        n2_op = n_op @ n_op

        mean_n = np.real(state.conj() @ n_op @ state)
        mean_n2 = np.real(state.conj() @ n2_op @ state)
        var_n = mean_n2 - mean_n ** 2

        # Para estado coherente: Var(n) = ⟨n⟩ → Mandel Q ≈ 0
        Q = (var_n - mean_n) / mean_n
        assert abs(Q) < 0.05

    def test_squeezed_vacuum_super_poissonian(self):
        """Estado squeezed: Var(n̂) > ⟨n̂⟩ (super-Poissonian, Mandel Q > 0)."""
        dim = 30
        state = squeeze_state(0.8, dim)

        n_op = number_op(dim)
        n2_op = n_op @ n_op

        mean_n = np.real(state.conj() @ n_op @ state)
        mean_n2 = np.real(state.conj() @ n2_op @ state)
        var_n = mean_n2 - mean_n ** 2

        if mean_n > 1e-6:
            Q = (var_n - mean_n) / mean_n
            assert Q > 0  # super-Poissonian


class TestFuncionWigner:
    def test_vacuum_wigner_positive(self):
        """La función de Wigner del vacío es gaussiana y positiva en el origen."""
        vacuum = fock_state(0, 15)
        W = wigner_value(vacuum, 0.0, 15)
        assert W > 0

    def test_cat_state_wigner_negative(self):
        """El estado gato tiene función de Wigner negativa entre los picos coherentes."""
        dim = 25
        alpha = 1.5
        state = cat_state(alpha, dim)
        # En el origen (entre los dos componentes coherentes) W < 0
        W_origin = wigner_value(state, 0.0, dim)
        assert W_origin < 0
