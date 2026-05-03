"""
Tests para QNLP (Quantum Natural Language Processing) — Fase 22.

Verifica propiedades de diagramas DisCoCat, circuitos IQP y un
clasificador QNLP toy sin requerir lambeq ni pytket instalados.

Si lambeq está disponible, se activan tests adicionales de integración.

Cobertura: Módulo 48, Lab 52.
"""

import numpy as np
import pytest


# ══════════════════════════════════════════════════════════════════════════════
# Modelo DisCoCat simplificado (sin lambeq)
# ══════════════════════════════════════════════════════════════════════════════

class PregrupoTipo:
    """Tipo pregrupo básico: n, s, n·r, s·l, etc."""
    def __init__(self, base: str, adj: int = 0):
        self.base = base
        self.adj = adj  # 0=base, 1=adjunto derecho, -1=adjunto izquierdo

    def __repr__(self):
        if self.adj == 0:
            return self.base
        return f"{self.base}{'r' * self.adj if self.adj > 0 else 'l' * (-self.adj)}"


class DisCoCatDiagrama:
    """
    Diagrama DisCoCat para frase simple sujeto-verbo-objeto.
    Tipo resultante: s (tipo oración).
    """

    def __init__(self, n_sujeto: int = 2, n_verbo: int = 4, n_objeto: int = 2):
        self.n_s = n_sujeto   # dimensión espacio semántico noun
        self.n_v = n_verbo    # dimensión espacio semántico verbo transitivo
        self.n_o = n_objeto   # dimensión espacio semántico noun

        # Tipos: sujeto: n, verbo transitivo: n^r · s · n^l, objeto: n
        self.tipo_sujeto = "n"
        self.tipo_verbo = "n^r s n^l"
        self.tipo_objeto = "n"
        self.tipo_resultado = "s"

    def dim_espacio_sentido(self) -> int:
        """Dimensión del espacio de sentido resultante (tipo s)."""
        return self.n_s  # dim(s) = dim(n) por construcción DisCoCat

    def n_parametros_iqp(self, n_palabras: int) -> int:
        """
        Un circuito IQP para QNLP usa 1 qubit por dimensión de noun + overhead verbo.
        Número de parámetros ≈ n_palabras × log2(dim_noun).
        """
        return n_palabras * max(1, int(np.ceil(np.log2(self.n_s))))

    def tensor_verbo(self) -> np.ndarray:
        """Tensor del verbo transitivo en espacio n ⊗ s ⊗ n."""
        rng = np.random.default_rng(0)
        return rng.standard_normal((self.n_s, self.n_v // self.n_s, self.n_o))

    def evaluar_frase(self, v_sujeto: np.ndarray, t_verbo: np.ndarray,
                      v_objeto: np.ndarray) -> np.ndarray:
        """
        Composición funcional: frase = sujeto · verbo · objeto.
        Resultado: vector en espacio s (sentido de la frase).
        """
        # Contracción: resultado[j] = Σ_{i,k} sujeto[i] · verbo[i,j,k] · objeto[k]
        return np.einsum("i,ijk,k->j", v_sujeto, t_verbo, v_objeto)


# ══════════════════════════════════════════════════════════════════════════════
# Circuito IQP (Instantaneous Quantum Polynomial)
# ══════════════════════════════════════════════════════════════════════════════

class CircuitoIQP:
    """
    Circuito IQP para clasificación QNLP.
    Estructura: H^n → ZZ(θ)^m → H^n → medición.
    """

    def __init__(self, n_qubits: int, n_capas: int = 1):
        self.n_qubits = n_qubits
        self.n_capas = n_capas
        # Pares de qubits para gates ZZ (conexiones entre adyacentes)
        self.pares = [(i, i + 1) for i in range(n_qubits - 1)]
        self.n_params = len(self.pares) * n_capas

    def evaluar(self, params: np.ndarray) -> np.ndarray:
        """
        Simula el circuito IQP y devuelve el vector de estado.
        Usa representación de statevector 2^n.
        """
        assert len(params) == self.n_params
        dim = 2 ** self.n_qubits
        state = np.ones(dim, dtype=complex) / np.sqrt(dim)  # H^n |0...0⟩

        param_idx = 0
        for _ in range(self.n_capas):
            for i, j in self.pares:
                theta = params[param_idx]
                param_idx += 1
                # Gate ZZ(θ): e^{-iθ Z⊗Z / 2}
                for basis in range(dim):
                    bits_i = (basis >> (self.n_qubits - 1 - i)) & 1
                    bits_j = (basis >> (self.n_qubits - 1 - j)) & 1
                    zz = (1 - 2 * bits_i) * (1 - 2 * bits_j)
                    state[basis] *= np.exp(-1j * theta * zz / 2)

        # Segunda capa de Hadamard
        for qubit in range(self.n_qubits):
            state = self._apply_hadamard(state, qubit)

        return state

    def _apply_hadamard(self, state: np.ndarray, qubit: int) -> np.ndarray:
        dim = 2 ** self.n_qubits
        new_state = np.zeros(dim, dtype=complex)
        for basis in range(dim):
            bit = (basis >> (self.n_qubits - 1 - qubit)) & 1
            partner = basis ^ (1 << (self.n_qubits - 1 - qubit))
            factor = (1 / np.sqrt(2)) * (1 if bit == 0 else -1)
            new_state[basis] += factor * state[basis]
            new_state[basis] += (1 / np.sqrt(2)) * state[partner]
        return new_state / np.sqrt(2) * np.sqrt(2)  # normalización explícita

    def probabilidad_0(self, params: np.ndarray) -> float:
        """Probabilidad de medir |0...0⟩ — usada como score de clasificación."""
        state = self.evaluar(params)
        return float(abs(state[0]) ** 2)


# ══════════════════════════════════════════════════════════════════════════════
# Clasificador QNLP toy
# ══════════════════════════════════════════════════════════════════════════════

class ClasificadorQNLPToy:
    """
    Clasificador QNLP toy con SPSA para 2 clases (positivo/negativo).
    Usa un circuito IQP de 2 qubits por palabra (4 qubits total para S-V-O).
    """

    def __init__(self, n_qubits: int = 4, seed: int = 42):
        self.qc = CircuitoIQP(n_qubits, n_capas=1)
        rng = np.random.default_rng(seed)
        self.params = rng.uniform(0, 2 * np.pi, self.qc.n_params)

    def predict_proba(self, feature: np.ndarray) -> float:
        """Score de clasificación para un vector de features."""
        params = (self.params + feature[:self.qc.n_params]) % (2 * np.pi)
        return self.qc.probabilidad_0(params)

    def train_spsa(self, X: np.ndarray, y: np.ndarray,
                   n_epochs: int = 30, a: float = 0.1, c: float = 0.05) -> list:
        """Entrena con SPSA (Simultaneous Perturbation Stochastic Approximation)."""
        rng = np.random.default_rng(0)
        losses = []
        for epoch in range(n_epochs):
            total_loss = 0.0
            for xi, yi in zip(X, y):
                delta = rng.choice([-1, 1], size=len(self.params))
                p_plus = self.params + c * delta
                p_minus = self.params - c * delta

                def loss_at(p):
                    score = self.qc.probabilidad_0(
                        (p + xi[:len(p)]) % (2 * np.pi))
                    pred = score
                    return -(yi * np.log(pred + 1e-9) +
                             (1 - yi) * np.log(1 - pred + 1e-9))

                grad_approx = (loss_at(p_plus) - loss_at(p_minus)) / (2 * c * delta)
                ak = a / (epoch + 1)
                self.params -= ak * grad_approx
                self.params %= 2 * np.pi
                total_loss += loss_at(self.params)

            losses.append(total_loss / len(X))
        return losses

    def accuracy(self, X: np.ndarray, y: np.ndarray) -> float:
        preds = [(1 if self.predict_proba(xi) > 0.5 else 0) for xi in X]
        return np.mean(np.array(preds) == y)


# ══════════════════════════════════════════════════════════════════════════════
# Tests
# ══════════════════════════════════════════════════════════════════════════════

class TestDiagramaDisCoCat:
    def test_dim_espacio_sentido(self):
        """El espacio de sentido tiene dimensión = dim(noun)."""
        d = DisCoCatDiagrama(n_sujeto=2, n_verbo=4, n_objeto=2)
        assert d.dim_espacio_sentido() == 2

    def test_tensor_verbo_shape(self):
        """El tensor del verbo tiene forma (n_s, n_v/n_s, n_o)."""
        d = DisCoCatDiagrama(n_sujeto=2, n_verbo=4, n_objeto=2)
        t = d.tensor_verbo()
        assert t.shape == (2, 2, 2)

    def test_evaluacion_frase_shape(self):
        """La evaluación de la frase da un vector en espacio s."""
        d = DisCoCatDiagrama(n_sujeto=2, n_verbo=4, n_objeto=2)
        rng = np.random.default_rng(5)
        v_s = rng.standard_normal(2)
        t_v = d.tensor_verbo()
        v_o = rng.standard_normal(2)
        resultado = d.evaluar_frase(v_s, t_v, v_o)
        assert resultado.shape == (2,)  # dim(s) = 2

    def test_svo_produces_sentence_type(self):
        """Para frase S-V-O el tipo resultante es s."""
        d = DisCoCatDiagrama()
        assert d.tipo_resultado == "s"


class TestCircuitoIQP:
    def test_n_params_correct(self):
        """IQP de n qubits, 1 capa: n-1 pares → n-1 parámetros."""
        for n in range(2, 6):
            qc = CircuitoIQP(n, n_capas=1)
            assert qc.n_params == n - 1

    def test_n_params_multiple_layers(self):
        """Con L capas: L × (n-1) parámetros."""
        qc = CircuitoIQP(4, n_capas=3)
        assert qc.n_params == 3 * 3

    def test_output_normalized(self):
        """El statevector resultante debe estar normalizado."""
        qc = CircuitoIQP(3, n_capas=1)
        params = np.array([0.5, 1.2])
        state = qc.evaluar(params)
        assert abs(np.linalg.norm(state) - 1.0) < 1e-10

    def test_probability_sum_to_one(self):
        """Las probabilidades suman 1."""
        qc = CircuitoIQP(3)
        params = np.random.default_rng(0).uniform(0, np.pi, qc.n_params)
        state = qc.evaluar(params)
        assert abs(sum(abs(state[i]) ** 2 for i in range(len(state))) - 1.0) < 1e-10

    def test_n_params_proporcionality(self):
        """El número de parámetros crece linealmente con n_qubits."""
        qc2 = CircuitoIQP(2)
        qc4 = CircuitoIQP(4)
        qc6 = CircuitoIQP(6)
        assert qc4.n_params == 2 * qc2.n_params + 1
        assert qc6.n_params > qc4.n_params


class TestClasificadorQNLP:
    def _dataset_toy(self, seed: int = 0) -> tuple:
        """Dataset toy: 20 frases codificadas como vectores de ángulos."""
        rng = np.random.default_rng(seed)
        n_pos, n_neg = 10, 10

        # Clase positiva: ángulos pequeños (0 a π/2)
        X_pos = rng.uniform(0, np.pi / 2, (n_pos, 3))
        # Clase negativa: ángulos grandes (π a 3π/2)
        X_neg = rng.uniform(np.pi, 3 * np.pi / 2, (n_neg, 3))

        X = np.vstack([X_pos, X_neg])
        y = np.array([1] * n_pos + [0] * n_neg)
        return X, y

    def test_classifier_trains_without_error(self):
        """El entrenador termina sin errores y devuelve lista de losses."""
        clf = ClasificadorQNLPToy(n_qubits=4, seed=0)
        X, y = self._dataset_toy()
        losses = clf.train_spsa(X, y, n_epochs=5)
        assert len(losses) == 5
        assert all(np.isfinite(l) for l in losses)

    def test_accuracy_above_chance_after_training(self):
        """Después de 30 epochs la accuracy debe superar el azar (> 60%)."""
        clf = ClasificadorQNLPToy(n_qubits=4, seed=42)
        X, y = self._dataset_toy(seed=0)
        clf.train_spsa(X, y, n_epochs=30, a=0.15)
        acc = clf.accuracy(X, y)
        assert acc > 0.60, f"Accuracy {acc:.2f} ≤ 0.60 — el clasificador no aprende"

    def test_predict_proba_in_range(self):
        """predict_proba debe devolver un valor en [0, 1]."""
        clf = ClasificadorQNLPToy()
        X, _ = self._dataset_toy()
        for xi in X[:5]:
            p = clf.predict_proba(xi)
            assert 0.0 <= p <= 1.0
