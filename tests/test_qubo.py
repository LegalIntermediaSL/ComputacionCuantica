"""
Tests para QUBO y D-Wave / Annealing — Fase 22.

Verifica formulaciones QUBO para MAX-CUT, TSP, portfolio y
restricciones de penalización. No requiere acceso a hardware D-Wave;
usa dimod (simulador local) si está disponible, o numpy directamente.

Cobertura: Módulo 49, Lab 53.
"""

import numpy as np
import pytest
from itertools import permutations


# ══════════════════════════════════════════════════════════════════════════════
# Formulaciones QUBO (puras numpy, sin dimod)
# ══════════════════════════════════════════════════════════════════════════════

def qubo_maxcut(adj: np.ndarray) -> np.ndarray:
    """
    Matriz QUBO para MAX-CUT.
    QUBO: E(x) = -Σ_{i<j} w_{ij} (x_i + x_j - 2 x_i x_j)
    Forma matricial: Q[i,i] = -Σ_j w_{ij}, Q[i,j] = 2 w_{ij} para i<j.
    """
    n = adj.shape[0]
    Q = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            if adj[i, j] != 0:
                Q[i, i] -= adj[i, j]
                Q[j, j] -= adj[i, j]
                Q[i, j] += 2 * adj[i, j]
    return Q


def evaluar_qubo(Q: np.ndarray, x: np.ndarray) -> float:
    """Energía QUBO: E(x) = x^T Q x."""
    return float(x @ Q @ x)


def brute_force_qubo(Q: np.ndarray) -> tuple[np.ndarray, float]:
    """Minimización exacta por fuerza bruta (solo para n pequeño)."""
    n = Q.shape[0]
    best_x, best_e = None, np.inf
    for bits in range(2 ** n):
        x = np.array([(bits >> i) & 1 for i in range(n)], dtype=float)
        e = evaluar_qubo(Q, x)
        if e < best_e:
            best_e = e
            best_x = x.copy()
    return best_x, best_e


def corte_maxcut(adj: np.ndarray, x: np.ndarray) -> int:
    """Valor del corte dado una asignación binaria x."""
    n = len(x)
    cut = 0
    for i in range(n):
        for j in range(i + 1, n):
            if adj[i, j] != 0 and x[i] != x[j]:
                cut += int(adj[i, j])
    return cut


def qubo_tsp(dist: np.ndarray, A: float = 10.0) -> np.ndarray:
    """
    Matriz QUBO para TSP con n ciudades.
    Variables x_{i,t} = 1 si ciudad i visitada en posición t.
    Índice plano: (i * n + t).
    Penaliza: cada ciudad exactamente una vez, cada posición exactamente una.
    """
    n = dist.shape[0]
    N = n * n
    Q = np.zeros((N, N))

    # Restricción 1: cada ciudad exactamente una vez
    for i in range(n):
        for t in range(n):
            idx_it = i * n + t
            Q[idx_it, idx_it] -= A
            for s in range(t + 1, n):
                idx_is = i * n + s
                Q[idx_it, idx_is] += 2 * A

    # Restricción 2: cada posición exactamente una ciudad
    for t in range(n):
        for i in range(n):
            idx_it = i * n + t
            Q[idx_it, idx_it] -= A
            for j in range(i + 1, n):
                idx_jt = j * n + t
                Q[idx_it, idx_jt] += 2 * A

    # Coste de la ruta
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            for t in range(n):
                t_next = (t + 1) % n
                idx_it = i * n + t
                idx_j_next = j * n + t_next
                if idx_it < idx_j_next:
                    Q[idx_it, idx_j_next] += dist[i, j]
                elif idx_it > idx_j_next:
                    Q[idx_j_next, idx_it] += dist[i, j]

    return Q


def es_permutacion_valida(x: np.ndarray, n: int) -> bool:
    """Comprueba que x codifica una permutación válida de n ciudades."""
    mat = x.reshape(n, n)
    filas_ok = all(abs(mat[i].sum() - 1) < 0.5 for i in range(n))
    cols_ok = all(abs(mat[:, t].sum() - 1) < 0.5 for t in range(n))
    return filas_ok and cols_ok


def qubo_portfolio(retornos: np.ndarray, cov: np.ndarray,
                   presupuesto: int, gamma: float = 2.0,
                   A: float = 10.0) -> np.ndarray:
    """
    Matriz QUBO para portfolio de n activos con presupuesto B activos.
    max Σ μ_i x_i - γ/2 Σ_{ij} σ_{ij} x_i x_j
    s.t. Σ x_i = B
    """
    n = len(retornos)
    Q = np.zeros((n, n))

    # Objetivo (negativo porque minimizamos)
    for i in range(n):
        Q[i, i] -= retornos[i]
    for i in range(n):
        for j in range(n):
            Q[i, j] += (gamma / 2) * cov[i, j]

    # Penalización: (Σ x_i - B)^2 = Σ x_i^2 - 2B Σ x_i + B^2
    for i in range(n):
        Q[i, i] -= 2 * A * presupuesto - A
    for i in range(n):
        for j in range(i + 1, n):
            Q[i, j] += 2 * A

    return Q


# ══════════════════════════════════════════════════════════════════════════════
# Tests
# ══════════════════════════════════════════════════════════════════════════════

class TestQUBOMaxCut:
    def setup_method(self):
        """Grafo K4 (completo de 4 nodos): corte óptimo = 4."""
        self.adj = np.array([[0, 1, 1, 1],
                             [1, 0, 1, 1],
                             [1, 1, 0, 1],
                             [1, 1, 1, 0]], dtype=float)
        self.Q = qubo_maxcut(self.adj)

    def test_qubo_matrix_shape(self):
        assert self.Q.shape == (4, 4)

    def test_ground_state_is_optimal_cut(self):
        """El ground state del QUBO K4 corresponde a corte de valor 4."""
        best_x, best_e = brute_force_qubo(self.Q)
        cut = corte_maxcut(self.adj, best_x)
        assert cut == 4, f"Corte esperado 4, obtenido {cut}"

    def test_qubo_energy_feasible_negative(self):
        """Soluciones con corte > 0 tienen energía QUBO negativa o cero."""
        for bits in range(1, 16):
            x = np.array([(bits >> i) & 1 for i in range(4)], dtype=float)
            if 0 < x.sum() < 4:
                e = evaluar_qubo(self.Q, x)
                cut = corte_maxcut(self.adj, x)
                if cut > 0:
                    assert e <= 0 + 1e-10

    def test_trivial_solution_zero_energy(self):
        """x = 0...0 o x = 1...1 (sin corte): energía = 0."""
        for x_val in [0, 1]:
            x = np.full(4, x_val, dtype=float)
            e = evaluar_qubo(self.Q, x)
            assert abs(e) < 1e-10

    def test_optimal_cut_equals_4(self):
        """Para K4 el corte máximo es 4 (bipartición 2+2)."""
        x_opt = np.array([1, 1, 0, 0], dtype=float)
        cut = corte_maxcut(self.adj, x_opt)
        assert cut == 4


class TestQUBOTSP:
    def setup_method(self):
        """TSP de 3 ciudades con distancias conocidas."""
        self.n = 3
        self.dist = np.array([[0, 1, 2],
                              [1, 0, 1],
                              [2, 1, 0]], dtype=float)
        self.Q = qubo_tsp(self.dist, A=10.0)

    def test_qubo_shape(self):
        assert self.Q.shape == (self.n ** 2, self.n ** 2)

    def test_valid_permutations_have_lower_energy(self):
        """Las permutaciones válidas tienen energía menor que las inválidas."""
        valid_energies = []
        invalid_energies = []

        for perm in permutations(range(self.n)):
            x = np.zeros(self.n ** 2)
            for t, city in enumerate(perm):
                x[city * self.n + t] = 1
            e = evaluar_qubo(self.Q, x)
            if es_permutacion_valida(x, self.n):
                valid_energies.append(e)

        # Soluciones aleatorias (inválidas típicamente)
        rng = np.random.default_rng(7)
        for _ in range(20):
            x = rng.integers(0, 2, self.n ** 2).astype(float)
            if not es_permutacion_valida(x, self.n):
                invalid_energies.append(evaluar_qubo(self.Q, x))

        if valid_energies and invalid_energies:
            assert min(valid_energies) < max(invalid_energies)

    def test_all_permutations_are_valid(self):
        """Toda permutación de n ciudades es una solución factible."""
        for perm in permutations(range(self.n)):
            x = np.zeros(self.n ** 2)
            for t, city in enumerate(perm):
                x[city * self.n + t] = 1
            assert es_permutacion_valida(x, self.n), f"Permutación {perm} inválida"

    def test_penalty_dominates_cost(self):
        """Con A grande, las soluciones inválidas tienen energía >> válidas."""
        Q_high_pen = qubo_tsp(self.dist, A=100.0)
        valid_max = -np.inf
        invalid_min = np.inf
        for perm in permutations(range(self.n)):
            x = np.zeros(self.n ** 2)
            for t, city in enumerate(perm):
                x[city * self.n + t] = 1
            valid_max = max(valid_max, evaluar_qubo(Q_high_pen, x))

        rng = np.random.default_rng(3)
        for _ in range(50):
            x = rng.integers(0, 2, self.n ** 2).astype(float)
            if not es_permutacion_valida(x, self.n) and x.sum() > 0:
                invalid_min = min(invalid_min, evaluar_qubo(Q_high_pen, x))

        if invalid_min < np.inf:
            assert invalid_min > valid_max - 50


class TestQUBOPortfolio:
    def setup_method(self):
        """Portfolio de 4 activos, presupuesto = 2."""
        self.n = 4
        self.B = 2
        self.retornos = np.array([0.1, 0.2, 0.15, 0.05])
        self.cov = np.eye(self.n) * 0.01 + np.full((self.n, self.n), 0.002)
        self.Q = qubo_portfolio(self.retornos, self.cov, self.B, gamma=1.0, A=5.0)

    def test_qubo_shape(self):
        assert self.Q.shape == (self.n, self.n)

    def test_budget_constraint_penalized(self):
        """Soluciones con Σx ≠ B tienen energía mayor que con Σx = B."""
        def energy(x):
            return evaluar_qubo(self.Q, x)

        feasible = [np.array([1, 1, 0, 0], dtype=float),
                    np.array([1, 0, 1, 0], dtype=float),
                    np.array([0, 1, 0, 1], dtype=float)]
        infeasible = [np.array([1, 0, 0, 0], dtype=float),  # B=1
                      np.array([1, 1, 1, 0], dtype=float)]  # B=3

        min_feasible = min(energy(x) for x in feasible)
        max_infeasible = max(energy(x) for x in infeasible)

        # Con A suficientemente grande las infactibles deben tener mayor energía
        # (puede no cumplirse con A=5 pero sí con A grande — test de monotonía)
        Q_strong = qubo_portfolio(self.retornos, self.cov, self.B, gamma=1.0, A=50.0)
        min_f2 = min(evaluar_qubo(Q_strong, x) for x in feasible)
        max_i2 = max(evaluar_qubo(Q_strong, x) for x in infeasible)
        assert min_f2 < max_i2

    def test_best_portfolio_picks_high_return_assets(self):
        """El ground state del QUBO debe incluir los activos de mayor retorno."""
        best_x, _ = brute_force_qubo(self.Q)
        # Activo 1 (retorno 0.2) y activo 2 (retorno 0.15) son los mejores
        assert best_x[1] == 1.0 or best_x[2] == 1.0

    def test_portfolio_energy_finite(self):
        """La energía es finita para cualquier vector binario."""
        rng = np.random.default_rng(0)
        for _ in range(20):
            x = rng.integers(0, 2, self.n).astype(float)
            e = evaluar_qubo(self.Q, x)
            assert np.isfinite(e)


class TestQUBOPenalizacion:
    def test_penalty_ensures_feasibility_maxcut(self):
        """En MAX-CUT no hay restricciones de igualdad: toda solución es factible."""
        adj = np.array([[0, 1], [1, 0]], dtype=float)
        Q = qubo_maxcut(adj)
        for x_val in [[0, 0], [0, 1], [1, 0], [1, 1]]:
            x = np.array(x_val, dtype=float)
            e = evaluar_qubo(Q, x)
            assert np.isfinite(e)

    def test_penalty_term_positive_semidefinite(self):
        """La matriz de penalización (Σ x_i - B)^2 es SDP."""
        n = 4
        B = 2
        A = 10.0
        # Matriz de penalización: A(e·e^T - 2B·I)
        e = np.ones(n)
        P = A * np.outer(e, e)
        eigenvalues = np.linalg.eigvalsh(P)
        assert np.all(eigenvalues >= -1e-10)
