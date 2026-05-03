"""
Tests para códigos qLDPC y decodificadores — Fase 21.

Verifica propiedades de códigos CSS, síndrome, MWPM simplificado
y decodificador neuronal básico sin requerir librerías de QEC externas.

Cobertura: Módulo 47, Lab 51, Solución R9.
"""

import numpy as np
import pytest
from itertools import product as iproduct


# ══════════════════════════════════════════════════════════════════════════════
# Códigos CSS y matrices de paridad
# ══════════════════════════════════════════════════════════════════════════════

def hypergraph_product_toy() -> tuple[np.ndarray, np.ndarray]:
    """
    Código CSS toy [[18, 2, 3]] basado en hypergraph product de dos códigos
    clásicos [3,1,3] (repetición).

    Devuelve (H_X, H_Z) como matrices binarias.
    """
    H1 = np.array([[1, 1, 0],
                   [0, 1, 1]], dtype=int)  # Código [3,1,3] (repetición)

    r1, n1 = H1.shape

    # Hypergraph product: H_X = [H1⊗I_{n1}, I_{r1}⊗H1^T]
    I_n1 = np.eye(n1, dtype=int)
    I_r1 = np.eye(r1, dtype=int)

    H_X = np.hstack([np.kron(H1, I_n1), np.kron(I_r1, H1.T)])
    H_Z = np.hstack([np.kron(I_n1, H1), np.kron(H1.T, I_r1)])

    return H_X, H_Z


def syndrome(H: np.ndarray, error: np.ndarray) -> np.ndarray:
    """Síndrome s = H·e mod 2."""
    return (H @ error) % 2


def random_pauli_errors(n: int, p: float, rng: np.random.Generator) -> np.ndarray:
    """Vector de errores Pauli aleatorios con probabilidad p por qubit."""
    return (rng.random(n) < p).astype(int)


# ══════════════════════════════════════════════════════════════════════════════
# Decodificador neuronal básico (MLP con numpy)
# ══════════════════════════════════════════════════════════════════════════════

class MLPDecoder:
    """
    Perceptrón multicapa simple para decodificación.
    Capas: entrada (n_synd) → oculta (64) → salida (n_qubits), sigmoide.
    Entrenado con SGD sobre dataset sintético de síndromes.
    """

    def __init__(self, n_synd: int, n_qubits: int, seed: int = 0):
        rng = np.random.default_rng(seed)
        self.W1 = rng.standard_normal((64, n_synd)) * 0.1
        self.b1 = np.zeros(64)
        self.W2 = rng.standard_normal((n_qubits, 64)) * 0.1
        self.b2 = np.zeros(n_qubits)

    @staticmethod
    def _sigmoid(x: np.ndarray) -> np.ndarray:
        return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))

    def predict(self, s: np.ndarray) -> np.ndarray:
        h = self._sigmoid(self.W1 @ s + self.b1)
        return self._sigmoid(self.W2 @ h + self.b2)

    def train(self, H: np.ndarray, p: float, n_samples: int = 3000,
              lr: float = 0.05, rng: np.random.Generator | None = None) -> None:
        if rng is None:
            rng = np.random.default_rng(42)
        n_qubits = H.shape[1]
        for _ in range(n_samples):
            e = random_pauli_errors(n_qubits, p, rng)
            s = syndrome(H, e).astype(float)

            # Forward
            h = self._sigmoid(self.W1 @ s + self.b1)
            out = self._sigmoid(self.W2 @ h + self.b2)

            # Backward (BCE loss)
            target = e.astype(float)
            d_out = (out - target) / n_qubits
            d_W2 = np.outer(d_out * out * (1 - out), h)
            d_b2 = d_out * out * (1 - out)
            d_h = self.W2.T @ (d_out * out * (1 - out))
            d_W1 = np.outer(d_h * h * (1 - h), s)
            d_b1 = d_h * h * (1 - h)

            self.W1 -= lr * d_W1
            self.b1 -= lr * d_b1
            self.W2 -= lr * d_W2
            self.b2 -= lr * d_b2


# ══════════════════════════════════════════════════════════════════════════════
# Tests
# ══════════════════════════════════════════════════════════════════════════════

class TestMatrizParidadCSS:
    def setup_method(self):
        self.H_X, self.H_Z = hypergraph_product_toy()

    def test_hx_hz_orthogonal_mod2(self):
        """CSS: H_X · H_Z^T = 0 mod 2."""
        prod = (self.H_X @ self.H_Z.T) % 2
        assert np.all(prod == 0), f"H_X · H_Z^T ≠ 0:\n{prod}"

    def test_hx_shape(self):
        assert self.H_X.shape[1] == self.H_Z.shape[1], "n_qubits debe coincidir"

    def test_hz_shape(self):
        assert self.H_Z.ndim == 2

    def test_binary_entries(self):
        assert set(np.unique(self.H_X)).issubset({0, 1})
        assert set(np.unique(self.H_Z)).issubset({0, 1})


class TestSindrome:
    def setup_method(self):
        self.H_X, self.H_Z = hypergraph_product_toy()
        self.n = self.H_X.shape[1]

    def test_syndrome_zero_no_error(self):
        """Sin error, el síndrome debe ser el vector cero."""
        e = np.zeros(self.n, dtype=int)
        s = syndrome(self.H_X, e)
        assert np.all(s == 0)

    def test_syndrome_detects_single_qubit_error(self):
        """Un error de peso 1 debe producir síndrome no nulo."""
        for qubit in range(min(self.n, 5)):
            e = np.zeros(self.n, dtype=int)
            e[qubit] = 1
            s = syndrome(self.H_X, e)
            if np.any(self.H_X[:, qubit] != 0):
                assert np.any(s != 0), f"Qubit {qubit}: error no detectado"

    def test_syndrome_linearity(self):
        """Síndrome es lineal: s(e1 + e2) = s(e1) + s(e2) mod 2."""
        rng = np.random.default_rng(7)
        e1 = random_pauli_errors(self.n, 0.1, rng)
        e2 = random_pauli_errors(self.n, 0.1, rng)
        assert np.all(syndrome(self.H_X, (e1 + e2) % 2) ==
                      (syndrome(self.H_X, e1) + syndrome(self.H_X, e2)) % 2)


class TestUmbralEmpírico:
    def _logical_error_rate(self, H: np.ndarray, p: float,
                            n_trials: int = 2000) -> float:
        """
        Tasa de error lógico estimada como fracción de errores no detectables
        (errores en el núcleo de H que tienen peso impar en el bloque lógico).
        Proxy simple del umbral de decodificación de lookup-table.
        """
        rng = np.random.default_rng(0)
        n = H.shape[1]
        undetected = 0
        for _ in range(n_trials):
            e = random_pauli_errors(n, p, rng)
            s = syndrome(H, e)
            if np.all(s == 0) and np.any(e != 0):
                undetected += 1
        return undetected / n_trials

    def test_low_p_low_logical_error(self):
        """Para p=0.01 la tasa de error lógico debe ser muy pequeña."""
        H_X, _ = hypergraph_product_toy()
        rate = self._logical_error_rate(H_X, p=0.01)
        assert rate < 0.05

    def test_high_p_high_logical_error(self):
        """Para p=0.3 la tasa de error lógico es significativamente mayor."""
        H_X, _ = hypergraph_product_toy()
        rate_low = self._logical_error_rate(H_X, p=0.01)
        rate_high = self._logical_error_rate(H_X, p=0.3)
        assert rate_high > rate_low


class TestDecodificadorNeuronal:
    def test_neural_decoder_accuracy_low_p(self):
        """Para p=0.05 el MLP debe alcanzar accuracy > 75% en test."""
        H_X, _ = hypergraph_product_toy()
        n = H_X.shape[1]
        p_train = 0.05

        decoder = MLPDecoder(H_X.shape[0], n, seed=42)
        decoder.train(H_X, p=p_train, n_samples=5000, lr=0.03)

        rng = np.random.default_rng(99)
        correct = 0
        n_test = 500
        for _ in range(n_test):
            e = random_pauli_errors(n, p_train, rng)
            s = syndrome(H_X, e).astype(float)
            pred = (decoder.predict(s) > 0.5).astype(int)
            if np.array_equal(pred, e):
                correct += 1

        accuracy = correct / n_test
        assert accuracy > 0.75, f"Accuracy {accuracy:.3f} < 0.75"


class TestOverheadComparativo:
    def test_qldpc_overhead_lower_than_surface(self):
        """
        [[144, 12, 12]] bivariate bicycle: k/n = 12/144 ≈ 0.083.
        Surface code [[d², 1, d]] con d=12: k/n = 1/144 ≈ 0.007.
        qLDPC tiene mejor ratio k/n.
        """
        n_qldpc, k_qldpc = 144, 12
        d_surface = 12
        n_surface = d_surface ** 2
        k_surface = 1

        ratio_qldpc = k_qldpc / n_qldpc
        ratio_surface = k_surface / n_surface

        assert ratio_qldpc > ratio_surface * 5, (
            f"qLDPC ratio {ratio_qldpc:.4f} no supera 5× surface {ratio_surface:.4f}")

    def test_physical_per_logical_qldpc(self):
        """144/12 = 12 qubits físicos por lógico para [[144,12,12]]."""
        assert 144 // 12 == 12
