# VQE: Variational Quantum Eigensolver

## 1. El problema que VQE ataca

Calcular la energía del estado fundamental de una molécula es uno de los problemas más importantes de la química computacional. Conocer esta energía permite predecir la reactividad química, diseñar fármacos, y entender catalizadores industriales.

El estado fundamental de un sistema cuántico de $n$ electrones es el autovector de menor autovalor del **Hamiltoniano** $H$ del sistema:

$$
H|\psi_0\rangle = E_0 |\psi_0\rangle, \quad E_0 = \min_\psi \langle\psi|H|\psi\rangle
$$

Calcular $E_0$ exactamente en un ordenador clásico requiere almacenar vectores en un espacio de Hilbert de dimensión $2^n$, lo que se vuelve inviable para más de $\sim 50$ electrones activos. El **VQE (Variational Quantum Eigensolver)** propone usar un procesador cuántico para preparar el estado de prueba y un optimizador clásico para ajustar sus parámetros.

## 2. El principio variacional

La base teórica del VQE es el **principio variacional de Rayleigh-Ritz**: para cualquier estado de prueba $|\psi(\vec{\theta})\rangle$, el valor esperado del Hamiltoniano es siempre mayor o igual a la energía del estado fundamental:

$$
E(\vec{\theta}) = \langle\psi(\vec{\theta})|H|\psi(\vec{\theta})\rangle \geq E_0
$$

La igualdad se alcanza únicamente si $|\psi(\vec{\theta})\rangle = |\psi_0\rangle$. Por tanto, minimizar $E(\vec{\theta})$ sobre $\vec{\theta}$ proporciona la mejor aproximación al estado fundamental alcanzable por el ansatz elegido.

## 3. Los tres componentes del VQE

**Hamiltoniano como observable cuántico:**

El Hamiltoniano molecular (en segunda cuantización, mapeado mediante Jordan-Wigner o Bravyi-Kitaev) se expresa como una suma de operadores de Pauli:

$$
H = \sum_i c_i P_i, \quad P_i \in \{I, X, Y, Z\}^{\otimes n}
$$

Qiskit representa esto con `SparsePauliOp`. El valor esperado se evalúa midiendo cada término $P_i$ por separado y promediando con los coeficientes $c_i$.

**Ansatz parametrizado:**

El ansatz debe ser suficientemente expresivo para capturar el estado fundamental. En química cuántica se usa habitualmente el **UCC (Unitary Coupled Cluster)**:

$$
U(\vec{\theta}) = e^{T(\vec{\theta}) - T^\dagger(\vec{\theta})}, \quad T = \sum_{ia} \theta_{ia} a_a^\dagger a_i + \sum_{ijab} \theta_{ijab} a_a^\dagger a_b^\dagger a_j a_i + \cdots
$$

Para hardware NISQ con conectividad limitada se prefiere el ansatz heurístico **EfficientSU2** de Qiskit, que aplica capas de rotaciones $R_y, R_z$ y puertas CNOT en patrones lineales o completos.

**Optimizador clásico:**

Los optimizadores más usados en VQE son:
- **COBYLA**: no requiere gradientes, robusto ante ruido.
- **SPSA** (Simultaneous Perturbation Stochastic Approximation): estima el gradiente con dos evaluaciones del circuito, resistente al ruido cuántico.
- **Gradient descent con parameter-shift**: más preciso pero requiere más evaluaciones.

## 4. Implementación en Qiskit

```python
from qiskit import QuantumCircuit
from qiskit.circuit.library import EfficientSU2
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp
from scipy.optimize import minimize
import numpy as np

# Hamiltoniano de ejemplo: H2 simplificado en 2 qubits
# (coeficientes ilustrativos, no valores reales de H2)
hamiltonian = SparsePauliOp.from_list([
    ("II", -1.0523),
    ("ZI", 0.3979),
    ("IZ", -0.3979),
    ("ZZ", -0.0112),
    ("XX", 0.1809),
])

# Ansatz EfficientSU2 para 2 qubits
n_qubits = 2
ansatz = EfficientSU2(n_qubits, reps=2)

estimator = StatevectorEstimator()
energy_evaluations = []

def cost_fn(params):
    bound = ansatz.assign_parameters(params)
    result = estimator.run([(bound, hamiltonian)]).result()
    energy = result[0].data.evs
    energy_evaluations.append(energy)
    return energy

# Inicialización aleatoria
np.random.seed(42)
x0 = np.random.uniform(-np.pi, np.pi, ansatz.num_parameters)

result = minimize(cost_fn, x0, method='COBYLA',
                  options={'maxiter': 1000, 'rhobeg': 0.5})

print(f"Energía VQE: {result.fun:.6f} Ha")
print(f"Evaluaciones: {len(energy_evaluations)}")
```

## 5. Retos y limitaciones

**Barren plateaus:** En ansatz genéricos, el gradiente de la energía se vuelve exponencialmente pequeño con el número de qubits. Solución: usar ansatz estructurados (UCC) o técnicas de inicialización inteligente.

**Error de circuito:** En hardware real, el ruido de las puertas CNOT introduce errores que sesgan la estimación de energía. Se mitigan con técnicas como Zero Noise Extrapolation (ZNE) o Probabilistic Error Cancellation (PEC).

**Mínimos locales:** La función de coste puede tener múltiples mínimos locales. Los optimizadores de gradiente pueden quedar atrapados. SPSA y los métodos evolutivos son más robustos.

**Brecha de aproximabilidad:** Si el ansatz no incluye al estado fundamental en su espacio de variación, VQE no puede encontrar $E_0$ exactamente, solo la mejor aproximación dentro del ansatz.

## 6. Ideas clave

- VQE minimiza el valor esperado del Hamiltoniano $\langle H \rangle_\theta$ para encontrar la energía del estado fundamental.
- El principio variacional garantiza que $E(\vec{\theta}) \geq E_0$ para cualquier estado de prueba.
- El algoritmo es híbrido: la QPU evalúa $\langle H \rangle$ y el ordenador clásico optimiza $\vec{\theta}$.
- El Hamiltoniano se representa como suma de operadores de Pauli (`SparsePauliOp`).
- Los principales retos son los barren plateaus, el ruido del hardware y los mínimos locales.

## 7. Ejercicios sugeridos

1. Implementar VQE para el Hamiltoniano $H = Z \otimes Z + 0.5(X \otimes I + I \otimes X)$ con un ansatz de 2 qubits y verificar que la energía converge al autovalor mínimo.
2. Comparar la convergencia de COBYLA y SPSA para el mismo problema con 1000 iteraciones máximas.
3. Añadir ruido simulado (canal de depolarización) y observar cómo varía la energía obtenida.
4. Calcular el autovalor mínimo de $H$ exactamente (descomposición espectral) y compararlo con el resultado VQE.

## Navegacion

- Anterior: [Circuitos parametrizados y optimizacion](01_circuitos_parametrizados_y_optimizacion.md)
- Siguiente: [QAOA: intuicion](03_qaoa_intuicion.md)
