# Optimización financiera cuántica: QUBO, portafolios y límites del QAOA actual

**Módulo 30 · Artículo 2 · Nivel avanzado**

---

## El problema de optimización de portafolio

El problema de Markowitz busca el portafolio de mínima varianza para una rentabilidad objetivo:

$$\min_{\mathbf{w}} \mathbf{w}^T \Sigma \mathbf{w} - \mu \mathbf{w}^T \mathbf{r}$$

sujeto a: $\sum_i w_i = 1$, $w_i \geq 0$

Con variables binarias (comprar o no comprar n activos), se convierte en un **QUBO**
(Quadratic Unconstrained Binary Optimization):

$$\min_{\mathbf{x} \in \{0,1\}^n} \mathbf{x}^T Q \mathbf{x}$$

donde Q es la matriz de covarianzas penalizada con la restricción presupuestaria.

---

## Formulación QUBO para portafolio

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorSampler
from scipy.optimize import minimize

# Datos de ejemplo: 4 activos
np.random.seed(42)
n_activos = 4
retornos = np.array([0.12, 0.08, 0.15, 0.10])   # retorno esperado anual
sigma = np.array([                                 # matriz de covarianzas
    [0.10, 0.02, 0.03, 0.01],
    [0.02, 0.08, 0.02, 0.01],
    [0.03, 0.02, 0.12, 0.02],
    [0.01, 0.01, 0.02, 0.06],
])
lambda_risk = 0.5   # aversión al riesgo

# Construir matriz QUBO: Q = lambda_risk * Sigma - diag(r)
Q = lambda_risk * sigma - np.diag(retornos)

# Hamiltoniano QUBO: H = x^T Q x con x_i = (1 - Z_i)/2
# Expandir en operadores de Pauli
def qubo_to_ising(Q, n):
    """Convierte QUBO a Ising: H = sum_i h_i Z_i + sum_ij J_ij Zi Zj + const"""
    h = np.zeros(n)
    J = {}
    offset = 0.0
    for i in range(n):
        for j in range(n):
            if i == j:
                # x_i^2 = x_i → contribuye a h[i] y offset
                h[i] += Q[i,i] / 2
                offset += Q[i,i] / 4
            else:
                J[(i,j)] = Q[i,j] / 4
                h[i] += Q[i,j] / 4
    return h, J, offset

h_ising, J_ising, offset = qubo_to_ising(Q, n_activos)

# Construir SparsePauliOp para n=4 qubits
terms = []
for i, hi in enumerate(h_ising):
    if abs(hi) > 1e-10:
        pauli = ['I'] * n_activos
        pauli[n_activos - 1 - i] = 'Z'
        terms.append((''.join(pauli), hi))

for (i, j), Jij in J_ising.items():
    if abs(Jij) > 1e-10:
        pauli = ['I'] * n_activos
        pauli[n_activos - 1 - i] = 'Z'
        pauli[n_activos - 1 - j] = 'Z'
        terms.append((''.join(pauli), Jij))

H_portfolio = SparsePauliOp.from_list(terms)
print(f"Hamiltoniano de portafolio: {len(H_portfolio)} términos de Pauli")
print(f"Número de qubits: {H_portfolio.num_qubits}")
```

---

## QAOA para optimización de portafolio

```python
from qiskit.circuit import ParameterVector

def build_portfolio_qaoa(n: int, p: int, Q_mat):
    """Circuito QAOA para portafolio con p capas."""
    gammas = ParameterVector("gamma", p)
    betas  = ParameterVector("beta", p)
    qc = QuantumCircuit(n)
    qc.h(range(n))  # estado inicial uniforme

    for layer in range(p):
        # Capa de coste: phase gadgets ZZ por cada par (i,j)
        for i in range(n):
            for j in range(i+1, n):
                coef = Q_mat[i, j]
                if abs(coef) > 1e-10:
                    qc.cx(i, j)
                    qc.rz(2 * gammas[layer] * coef, j)
                    qc.cx(i, j)
        # Puertas diagonales (términos Z individuales)
        for i in range(n):
            if abs(h_ising[i]) > 1e-10:
                qc.rz(2 * gammas[layer] * h_ising[i], i)
        # Capa mixer: Rx(2*beta) en todos los qubits
        for q in range(n):
            qc.rx(2 * betas[layer], q)

    return qc, gammas, betas

qc_qaoa, gammas, betas = build_portfolio_qaoa(n_activos, p=2, Q_mat=Q)
print(f"Circuito QAOA portafolio: {qc_qaoa.count_ops()}")
print(f"Profundidad: {qc_qaoa.depth()}")
```

---

## Benchmarking: QAOA vs. búsqueda exhaustiva

Para n activos pequeños (n ≤ 20), se puede comparar con la solución exacta:

```python
# Solución exacta por fuerza bruta (solo para n pequeño)
mejor_energia = np.inf
mejor_solucion = None

for bits in range(2**n_activos):
    x = np.array([(bits >> i) & 1 for i in range(n_activos)])
    if x.sum() == 0:  # no invertir en nada no tiene sentido
        continue
    energia = x @ Q @ x
    if energia < mejor_energia:
        mejor_energia = energia
        mejor_solucion = x.copy()

print(f"Solución óptima exacta: activos {np.where(mejor_solucion)[0].tolist()}")
print(f"Energía QUBO óptima: {mejor_energia:.4f}")
print(f"Retorno esperado: {mejor_solucion @ retornos:.3f}")
print(f"Riesgo (varianza): {mejor_solucion @ sigma @ mejor_solucion:.4f}")
```

---

## Análisis crítico: ¿Hay ventaja cuántica en finanzas?

### Caso optimista (teórico)

QAOA con p capas tiene garantía de aproximación ratio:

$$\text{ApproxRatio}(p) \geq 1 - \left(\frac{\pi}{4p+4}\right)^2$$

Para p → ∞, QAOA converge a la solución exacta. Para p finito:

| p | Ratio mínimo garantizado | CNOTs (n=100 activos) |
|---|---|---|
| 1 | ~0.75 | ~5000 |
| 3 | ~0.92 | ~15000 |
| 10 | ~0.98 | ~50000 |

### Caso realista (NISQ actual)

En hardware NISQ con F_CNOT = 99,5 % y n = 100 activos:

```python
n = 100        # activos
p = 3          # capas QAOA
F_cnot = 0.995 # fidelidad por puerta CNOT

# CNOTs por capa: O(n^2 / 2) para grafo completo
n_cnots = p * n * (n-1) // 2
F_total = F_cnot ** n_cnots

print(f"CNOTs totales: {n_cnots:,}")
print(f"Fidelidad total del circuito: {F_total:.6f}")
print(f"El resultado es prácticamente ruido aleatorio" if F_total < 0.01 else "")
```

**Conclusión:** Para n = 100 activos y p = 3, el circuito QAOA requiere ~15000 CNOTs,
lo que con F_CNOT = 99,5 % da una fidelidad total de ~10⁻³³. **No hay señal útil.**

### ¿Cuándo hay ventaja?

Los mejores algoritmos clásicos de optimización combinatoria (Gurobi, CPLEX) resuelven
QUBO con n ~ 10.000 variables en minutos gracias a técnicas de branch-and-bound.

La ventaja cuántica en finanzas requiere:
- **Hardware fault-tolerant** con ~10⁴ qubits lógicos.
- Instancias donde el landscape de energía tiene estructura que QAOA aprovecha.
- Restricciones reales (sectores, límites de peso) que complican el espacio de búsqueda.

Estimación conservadora: **horizonte 2030-2035** para ventaja en portafolios reales.

---

## Casos de uso financiero más prometedores

| Caso | Complejidad clásica | Qubits necesarios | Horizonte |
|---|---|---|---|
| Portafolio n=50 binario | NP-hard, pero heurísticas buenas | ~200 lógicos | 2028-2030 |
| Pricing de derivados (QMC) | O(1/ε²) → O(1/ε) cuántico | ~100 lógicos | 2027-2030 |
| Detección de arbitraje | Problema de flujo, polinomial | Sin ventaja cuántica | Nunca |
| Riesgo crediticio (simulación) | Monte Carlo, O(1/ε²) | ~50 lógicos | 2026-2029 |

---

## Conclusión

El problema de portafolio es un **caso de uso prometedor** pero no inmediato.
En el corto plazo (2025-2027), el valor real está en la **aceleración cuántica
de Monte Carlo** (Quantum Amplitude Estimation) para simulación de riesgo,
donde la ventaja cuántica es cuadrática y los circuitos son más superficiales.

Para QAOA en optimización combinatoria financiera, la ventaja práctica requiere
hardware fault-tolerant aún no disponible.
