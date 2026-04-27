# Solución R6 — QML: Kernel Cuántico vs Clásico

**Problema:** [Ejercicios de investigación R6](../../Ejercicios/ejercicios_investigacion.md#problema-r6)

---

## Parte a) — Construcción del kernel cuántico

```python
import numpy as np
from sklearn.svm import SVC
from sklearn.datasets import make_moons, make_circles
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as plt

# ─── Feature map ZZFeatureMap (sin qiskit_machine_learning) ──────────────────

def zz_feature_map(x: np.ndarray, reps: int = 2) -> QuantumCircuit:
    """
    ZZFeatureMap para d=len(x) características:
    [H → Rz(2x_i)]^reps × [CX → Rz(2(π-x_i)(π-x_j)) → CX]^reps
    """
    d = len(x)
    qc = QuantumCircuit(d)
    for _ in range(reps):
        for i in range(d):
            qc.h(i)
            qc.rz(2 * x[i], i)
        for i in range(d):
            for j in range(i + 1, d):
                val = 2 * (np.pi - x[i]) * (np.pi - x[j])
                qc.cx(i, j)
                qc.rz(val, j)
                qc.cx(i, j)
    return qc


def quantum_kernel_matrix(X1: np.ndarray, X2: np.ndarray, reps: int = 2) -> np.ndarray:
    """
    K[i,j] = |⟨ϕ(X2_j)|ϕ(X1_i)⟩|²
    Nota: O(|X1|·|X2|·2^d) — práctico solo para d≤6 y datasets pequeños.
    """
    K = np.zeros((len(X1), len(X2)))
    svs_1 = [Statevector(zz_feature_map(x, reps)) for x in X1]
    svs_2 = [Statevector(zz_feature_map(x, reps)) for x in X2]
    for i, sv_i in enumerate(svs_1):
        for j, sv_j in enumerate(svs_2):
            K[i, j] = abs(sv_j.inner(sv_i)) ** 2
    return K


# Kernel Target Alignment
def kta(K: np.ndarray, y: np.ndarray) -> float:
    """KTA = ⟨K, yy^T⟩_F / (‖K‖_F · ‖yy^T‖_F)"""
    Y = np.outer(y, y).astype(float)
    num = np.sum(K * Y)
    den = np.linalg.norm(K, 'fro') * np.linalg.norm(Y, 'fro')
    return num / den if den > 0 else 0.0
```

---

## Parte b) — Comparativa en dataset moons

```python
# Dataset
np.random.seed(0)
X, y = make_moons(n_samples=120, noise=0.15, random_state=42)
y_pm = 2 * y - 1  # {0,1} → {-1,+1} para KTA

# Escalar a [0, π]
scaler = MinMaxScaler((0, np.pi))
X_sc = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_sc, y, test_size=0.25, random_state=42)

# Kernel cuántico
print('Calculando kernel cuántico...')
K_train = quantum_kernel_matrix(X_train, X_train, reps=2)
K_test  = quantum_kernel_matrix(X_test, X_train, reps=2)

# SVMs
svm_q   = SVC(kernel='precomputed').fit(K_train, y_train)
svm_rbf = SVC(kernel='rbf', gamma='scale').fit(X_train, y_train)
svm_lin = SVC(kernel='linear').fit(X_train, y_train)

acc_q   = accuracy_score(y_test, svm_q.predict(K_test))
acc_rbf = accuracy_score(y_test, svm_rbf.predict(X_test))
acc_lin = accuracy_score(y_test, svm_lin.predict(X_test))

print(f'\n{"Modelo":>18} | {"Accuracy test":>14}')
print('-' * 36)
print(f'{"Kernel cuántico":>18} | {acc_q:.3f}')
print(f'{"Kernel RBF":>18} | {acc_rbf:.3f}')
print(f'{"Kernel lineal":>18} | {acc_lin:.3f}')

# KTA
kta_q   = kta(K_train, 2*y_train-1)
K_rbf = np.exp(-0.5 * np.sum((X_train[:,None,:] - X_train[None,:,:])**2, axis=-1))
kta_rbf = kta(K_rbf, 2*y_train-1)
print(f'\nKTA cuántico: {kta_q:.4f}')
print(f'KTA RBF:      {kta_rbf:.4f}')
```

---

## Parte c) — Visualización del decision boundary

```python
def plot_decision_boundary(clf, X_train, y_train, X_test, y_test,
                           kernel_fn=None, title='', ax=None):
    """Plot de frontera de decisión con puntos de train y test."""
    if ax is None:
        _, ax = plt.subplots(figsize=(5, 4))

    h = 0.04
    x_min, x_max = X_train[:, 0].min() - 0.1, X_train[:, 0].max() + 0.1
    y_min, y_max = X_train[:, 1].min() - 0.1, X_train[:, 1].max() + 0.1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    grid = np.c_[xx.ravel(), yy.ravel()]

    if kernel_fn is not None:
        K_grid = kernel_fn(grid, X_train)
        Z = clf.predict(K_grid)
    else:
        Z = clf.predict(grid)

    Z = Z.reshape(xx.shape)
    ax.contourf(xx, yy, Z, alpha=0.3, cmap='RdBu')
    colors = ['red' if yi == 0 else 'blue' for yi in y_train]
    ax.scatter(X_train[:, 0], X_train[:, 1], c=colors, s=30, edgecolors='k', lw=0.5, label='Train')
    colors_t = ['red' if yi == 0 else 'blue' for yi in y_test]
    ax.scatter(X_test[:, 0], X_test[:, 1], c=colors_t, s=60, marker='*',
               edgecolors='k', lw=0.5, label='Test')
    ax.set_title(title, fontsize=11)
    ax.legend(fontsize=8)
    return ax

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
plot_decision_boundary(svm_q,   X_train, y_train, X_test, y_test,
                       kernel_fn=lambda g, tr: quantum_kernel_matrix(g, tr),
                       title=f'SVM Kernel Cuántico (acc={acc_q:.2f})', ax=axes[0])
plot_decision_boundary(svm_rbf, X_train, y_train, X_test, y_test,
                       title=f'SVM RBF (acc={acc_rbf:.2f})', ax=axes[1])
plt.tight_layout(); plt.show()
```

---

## Parte d) — ¿Cuándo supera el kernel cuántico al clásico?

```python
analisis = """
VENTAJA DEL KERNEL CUÁNTICO: ANÁLISIS TEÓRICO
══════════════════════════════════════════════

1. EXPRESSIVIDAD:
   ZZFeatureMap accede a un espacio de Hilbert de dim 2^n.
   Para n=2 features: espacio de 4 dimensiones.
   El kernel es NO-LOCAL: correlaciones cruzadas (x_i)(x_j) capturadas.

2. CUÁNDO EL KERNEL CUÁNTICO SUPERA AL RBF:
   a) Datos generados por un proceso cuántico (Huang et al. 2021):
      Existe dataset D tal que kernel cuántico → 100% acc y RBF falla.
   b) Datos con correlaciones de alta dimensión que el RBF no captura.
   c) Pocos ejemplos de entrenamiento (KTA alto → mejor generalización).

3. LIMITACIONES ACTUALES:
   a) Coste O(N² · 2^d) para calcular la matriz de kernel → no escalable.
   b) Barren plateaus: KTA → 0 exponencialmente con n (Thanasilp 2022).
   c) Dequantization: muchos kernels cuánticos son eficientemente simulables.

4. CRITERIO PRÁCTICO (Kübler et al. 2021):
   KTA_cuántico > KTA_RBF → usar kernel cuántico
   KTA_cuántico < KTA_RBF → usar clásico

5. BENCHMARK HONESTO:
   Huang et al. (2021) Nature Comms:
   - Construyeron dataset donde kernel cuántico gana de forma provable
   - Clave: los datos deben tener ESTRUCTURA CUÁNTICA
   - Datos aleatorios/clásicos: kernel cuántico NO supera al RBF
"""
print(analisis)
```

**Conclusión:** el kernel cuántico tiene ventaja teórica garantizada solo para datos con estructura cuántica intrínseca. En datos clásicos estándar, el RBF suele ser competitivo o superior.

---

## Referencia
Huang et al., *Power of data in quantum machine learning*, **Nat. Commun.** 12, 2631 (2021);  
Kübler et al., *An adaptive optimizer for measurement-frugal variational algorithms*, **Quantum** 4, 263 (2020);  
Thanasilp et al., *Exponential concentration in quantum kernel methods*, **Nat. Commun.** 13, 7. (2022).
