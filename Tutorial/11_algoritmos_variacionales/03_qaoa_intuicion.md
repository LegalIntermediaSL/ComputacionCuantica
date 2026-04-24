# QAOA: Quantum Approximate Optimization Algorithm

## 1. Del problema combinatorio al Hamiltoniano de coste

El **QAOA (Quantum Approximate Optimization Algorithm)**, propuesto por Farhi, Goldstone y Gutmann en 2014, está diseñado para atacar problemas de optimización combinatoria: encontrar la configuración de bits $z \in \{0,1\}^n$ que minimiza una función de coste $C(z)$.

Ejemplos representativos:
- **MaxCut:** dado un grafo $G = (V, E)$, encontrar la partición de vértices que maximiza el número de aristas cortadas.
- **Satisfacibilidad (SAT):** encontrar la asignación de variables booleanas que satisface el mayor número de cláusulas.
- **QUBO:** problemas de optimización cuadrática sin restricciones sobre variables binarias.

La idea central es codificar la función de coste $C(z)$ como el valor esperado de un **Hamiltoniano de coste diagonal** en la base computacional:

$$
H_C |z\rangle = C(z) |z\rangle
$$

Maximizar $C(z)$ equivale a encontrar el autovector de máximo autovalor de $H_C$.

## 2. El ejemplo de MaxCut

Para el problema MaxCut en un grafo con aristas $(i,j)$, la función de coste es:

$$
C(z) = \sum_{(i,j) \in E} \frac{1 - z_i z_j}{2}, \quad z_i \in \{-1, +1\}
$$

El Hamiltoniano cuántico correspondiente, usando $z_i = (-1)^{s_i}$ con $s_i \in \{0,1\}$, es:

$$
H_C = \frac{1}{2} \sum_{(i,j) \in E} (I - Z_i Z_j)
$$

donde $Z_i$ es la puerta Pauli $Z$ actuando sobre el qubit $i$.

## 3. El ansatz QAOA

A diferencia del VQE con ansatz heurístico, el QAOA tiene una arquitectura específica motivada por la computación adiabática. El ansatz de profundidad $p$ es:

$$
|\vec{\gamma}, \vec{\beta}\rangle = \prod_{l=1}^{p} e^{-i\beta_l H_M} e^{-i\gamma_l H_C} |s\rangle
$$

donde:
- $|s\rangle = |+\rangle^{\otimes n}$ es la superposición uniforme (estado inicial).
- $H_C$ es el Hamiltoniano de coste.
- $H_M = \sum_i X_i$ es el **Hamiltoniano mezclador** (mixer), que introduce superposición entre estados.
- $\vec{\gamma} = (\gamma_1, \ldots, \gamma_p)$ y $\vec{\beta} = (\beta_1, \ldots, \beta_p)$ son los $2p$ parámetros a optimizar.

Para $p = 1$ la implementación en circuito es:
1. Preparar $|+\rangle^{\otimes n}$ con Hadamards.
2. Aplicar $e^{-i\gamma H_C}$: para MaxCut, esto es una puerta $R_{ZZ}(\gamma)$ por cada arista.
3. Aplicar $e^{-i\beta H_M}$: rotaciones $R_x(2\beta)$ sobre cada qubit.
4. Medir y evaluar $\langle H_C \rangle$.

## 4. Conexión con la computación adiabática

El QAOA está motivado por el **teorema de computación adiabática**: si se evoluciona lentamente desde el estado fundamental de $H_M$ hasta el de $H_C$, se obtiene la solución óptima. Para tiempos infinitos ($p \to \infty$), QAOA reproduce esta evolución. Para $p$ finito, da una aproximación.

Para $p = 1$, la relación de aproximación para MaxCut en grafos 3-regulares es al menos $0.6924$. Con $p \to \infty$, QAOA converge a la solución óptima.

## 5. Implementación en Qiskit

```python
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp
from scipy.optimize import minimize
import numpy as np

def build_maxcut_qaoa(n_qubits: int, edges: list, p: int = 1) -> tuple:
    """Construye el circuito QAOA para MaxCut y su Hamiltoniano."""
    gamma = ParameterVector('γ', p)
    beta = ParameterVector('β', p)

    qc = QuantumCircuit(n_qubits)

    # Estado inicial: superposición uniforme
    qc.h(range(n_qubits))

    for layer in range(p):
        # Capa de coste: R_ZZ por cada arista
        for (i, j) in edges:
            qc.rzz(2 * gamma[layer], i, j)
        # Capa mezcladora: R_x sobre cada qubit
        for q in range(n_qubits):
            qc.rx(2 * beta[layer], q)

    # Hamiltoniano MaxCut: H_C = sum_{(i,j)} (I - Z_i Z_j) / 2
    pauli_terms = []
    for (i, j) in edges:
        op_str = ['I'] * n_qubits
        op_str[i] = 'Z'
        op_str[j] = 'Z'
        pauli_terms.append((''.join(reversed(op_str)), -0.5))
    pauli_terms.append(('I' * n_qubits, 0.5 * len(edges)))
    hamiltonian = SparsePauliOp.from_list(pauli_terms)

    return qc, hamiltonian

# Grafo de ejemplo: triángulo (3 nodos, 3 aristas)
n = 3
edges = [(0, 1), (1, 2), (0, 2)]
p = 1

qc, H_cost = build_maxcut_qaoa(n, edges, p)
estimator = StatevectorEstimator()

def cost_fn(params):
    bound = qc.assign_parameters(params)
    result = estimator.run([(bound, H_cost)]).result()
    return -result[0].data.evs  # Maximizar C = minimizar -C

x0 = np.random.uniform(0, 2 * np.pi, 2 * p)
result = minimize(cost_fn, x0, method='COBYLA')

print(f"Valor de corte máximo aproximado: {-result.fun:.3f}")
print(f"Óptimo teórico para triángulo: 2")
```

## 6. Comparacion con VQE

| Aspecto | VQE | QAOA |
|---|---|---|
| Problema objetivo | Autovalor mínimo de $H$ | Optimización combinatoria |
| Ansatz | Genérico o UCC | Estructurado (motivado por adiabático) |
| Parámetros | $O(nd)$ para profundidad $d$ | $2p$ (solo gamma y beta) |
| Garantías teóricas | Solo límite variacional | Relación de aproximación para $p \to \infty$ |
| Aplicación principal | Química cuántica | Optimización combinatoria |

## 7. Ideas clave

- QAOA codifica problemas combinatorios como el valor esperado de un Hamiltoniano diagonal $H_C$.
- El ansatz alterna capas de evolución con $H_C$ (parámetro $\gamma$) y con el mezclador $H_M$ (parámetro $\beta$).
- Para $p \to \infty$, QAOA converge a la solución óptima (reproduciendo la computación adiabática).
- Para $p$ finito, proporciona una aproximación con garantías teóricas en algunos casos (MaxCut, por ejemplo).
- El número de parámetros es solo $2p$, independiente del número de qubits.

## 8. Ejercicios sugeridos

1. Implementar QAOA para MaxCut en un grafo de 4 nodos con 4 aristas y verificar que la solución corresponde a una bipartición válida.
2. Comparar los resultados de QAOA con $p = 1$ y $p = 2$ para el mismo grafo.
3. Visualizar el estado de salida de QAOA en la base computacional y verificar que los estados de mayor amplitud corresponden a cortes de alta calidad.
4. Implementar el caso $p = 1$ del problema de 3-SAT con 3 variables y verificar que QAOA encuentra una asignación satisfactoria.

## Navegacion

- Anterior: [VQE: intuicion](02_vqe_intuicion.md)
- Siguiente: [Quimica cuantica y simulacion](../12_aplicaciones/01_quimica_cuantica_y_simulacion.md)
