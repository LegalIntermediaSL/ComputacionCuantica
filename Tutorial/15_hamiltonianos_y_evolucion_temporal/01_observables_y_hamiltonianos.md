# Observables y Hamiltonianos

## 1. Observables como operadores hermitianos

En mecánica cuántica, cualquier magnitud física medible (energía, posición, momento, espín) se representa mediante un **operador hermitiano** $O = O^\dagger$ que actúa sobre el espacio de Hilbert del sistema.

Las propiedades fundamentales de un observable $O$:

- Sus **autovalores** son reales: $O|v_k\rangle = \lambda_k |v_k\rangle$, $\lambda_k \in \mathbb{R}$. Son los posibles resultados de la medición.
- Sus **autovectores** forman una base ortonormal del espacio de Hilbert.
- El **valor esperado** en un estado $|\psi\rangle$ es $\langle O \rangle = \langle\psi|O|\psi\rangle$.

Para estados mixtos descritos por una matriz de densidad $\rho$:

$$
\langle O \rangle = \text{Tr}(O\rho)
$$

## 2. El Hamiltoniano: el observable de energía

El **Hamiltoniano** $H$ es el observable que corresponde a la energía total del sistema. Tiene un papel especial: también es el **generador de la evolución temporal**.

Para un qubit, el Hamiltoniano más simple es proporcional a una de las matrices de Pauli:

$$
H = \frac{\hbar\omega}{2} Z = \frac{\hbar\omega}{2} \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}
$$

Este Hamiltoniano describe un qubit con dos niveles de energía: $|0\rangle$ con energía $+\hbar\omega/2$ y $|1\rangle$ con energía $-\hbar\omega/2$.

## 3. Descomposición en operadores de Pauli

Todo operador hermitiano sobre $n$ qubits puede expresarse como combinación lineal de productos tensoriales de matrices de Pauli:

$$
H = \sum_i c_i P_i, \quad P_i \in \{I, X, Y, Z\}^{\otimes n}, \quad c_i \in \mathbb{R}
$$

Esta representación es fundamental en computación cuántica porque:

1. Cada término $P_i$ es un operador de Pauli, cuyo valor esperado se puede medir directamente en hardware.
2. La suma puede ser sparse (pocas decenas de términos para moléculas pequeñas), lo que hace eficiente la evaluación de $\langle H \rangle$.
3. Es el formato que usa Qiskit con `SparsePauliOp`.

Ejemplo para el Hamiltoniano de Heisenberg de dos qubits ($J_x = J_y = J_z = J$):

$$
H = J(X \otimes X + Y \otimes Y + Z \otimes Z)
$$

## 4. Hamiltonianos moleculares en segunda cuantización

Para sistemas de electrones en química cuántica, el Hamiltoniano electrónico se expresa en segunda cuantización:

$$
H = \sum_{pq} h_{pq} a_p^\dagger a_q + \frac{1}{2} \sum_{pqrs} g_{pqrs} a_p^\dagger a_q^\dagger a_r a_s
$$

donde $a_p^\dagger$ y $a_p$ son operadores de creación y aniquilación fermiónicos. Para ejecutarlo en un procesador cuántico, se transforma a operadores de qubit mediante el **mapeado de Jordan-Wigner** o el mapeado de **Bravyi-Kitaev**:

$$
a_j^\dagger \to \frac{1}{2}(X_j - iY_j) \prod_{k<j} Z_k \quad \text{(Jordan-Wigner)}
$$

## 5. Implementación en Qiskit

```python
from qiskit.quantum_info import SparsePauliOp
import numpy as np

# Hamiltoniano de Heisenberg para 2 qubits
# H = J(X⊗X + Y⊗Y + Z⊗Z)
J = 0.5
heisenberg_H = SparsePauliOp.from_list([
    ("XX", J),
    ("YY", J),
    ("ZZ", J),
])

print("Hamiltoniano de Heisenberg:")
print(heisenberg_H)
print(f"\nMatriz densa:\n{heisenberg_H.to_matrix().real}")

# Calcular autovalores
eigenvalues = np.linalg.eigvalsh(heisenberg_H.to_matrix().real)
print(f"\nAutovalores: {eigenvalues}")

# Hamiltoniano simple: qubit en campo transverso
# H = hZ + gX
h, g = 1.0, 0.5
transverse_H = SparsePauliOp.from_list([("Z", h), ("X", g)])
E_min = np.min(np.linalg.eigvalsh(transverse_H.to_matrix().real))
print(f"\nEnergía del estado fundamental (campo transverso): {E_min:.4f}")
```

## 6. Conexión con las primitivas de Qiskit

El `Estimator` de Qiskit está diseñado precisamente para evaluar valores esperados de Hamiltonianos:

```python
from qiskit.primitives import StatevectorEstimator
from qiskit import QuantumCircuit

# Estado |+> = H|0>
qc = QuantumCircuit(1)
qc.h(0)

# Calcular <X>, <Y>, <Z> para el estado |+>
estimator = StatevectorEstimator()
observables = [SparsePauliOp("X"), SparsePauliOp("Y"), SparsePauliOp("Z")]

for obs in observables:
    result = estimator.run([(qc, obs)]).result()
    print(f"<{obs.paulis[0]}> = {result[0].data.evs:.4f}")
# Esperado: <X>=1, <Y>=0, <Z>=0 para |+>
```

## 7. Ideas clave

- Los observables son operadores hermitianos; sus autovalores son los posibles resultados de la medición.
- El Hamiltoniano $H$ es el observable de energía y el generador de la evolución temporal.
- Todo Hamiltoniano de $n$ qubits se puede escribir como suma de productos de Pauli: $H = \sum_i c_i P_i$.
- Esta descomposición permite evaluar $\langle H \rangle$ con el `Estimator` de Qiskit.
- Los Hamiltonianos moleculares se mapean a qubits mediante Jordan-Wigner o Bravyi-Kitaev.

## 8. Ejercicios sugeridos

1. Calcular los autovalores del Hamiltoniano de Heisenberg $H = X \otimes X + Y \otimes Y + Z \otimes Z$ a mano y verificar con Qiskit.
2. Para el Hamiltoniano $H = Z$, calcular el valor esperado en los estados $|0\rangle$, $|1\rangle$, $|+\rangle$, $|-\rangle$.
3. Construir el mapeado de Jordan-Wigner para el Hamiltoniano de dos sitios $H = a_0^\dagger a_1 + a_1^\dagger a_0$.
4. Evaluar $\langle H \rangle$ para el estado de Bell $|\Phi^+\rangle$ con el Hamiltoniano de Heisenberg.

## Navegacion

- Anterior: [Simulacion digital y Hamiltonianos sencillos](../12_aplicaciones/04_simulacion_digital_y_hamiltonianos_sencillos.md)
- Siguiente: [Evolucion unitaria y Trotterizacion](02_evolucion_unitaria_y_trotterizacion.md)
