# Fidelidad y caracterización de dispositivos

## 1. Fidelidad entre estados cuánticos

La **fidelidad** mide el grado de parecido entre dos estados cuánticos. Para un estado puro $|\psi\rangle$ y una matriz de densidad $\rho$:

$$
F(|\psi\rangle, \rho) = \langle\psi|\rho|\psi\rangle
$$

Para dos estados mixtos $\rho$ y $\sigma$:

$$
F(\rho, \sigma) = \left(\text{Tr}\sqrt{\sqrt{\rho}\,\sigma\sqrt{\rho}}\right)^2
$$

Propiedades fundamentales:
- $0 \leq F \leq 1$.
- $F = 1$ si y solo si $\rho = \sigma$ (estados idénticos).
- $F = 0$ si los estados son ortogonales.
- Simétrica: $F(\rho, \sigma) = F(\sigma, \rho)$.

Para dos estados puros $|\psi\rangle$ y $|\phi\rangle$: $F = |\langle\psi|\phi\rangle|^2$.

## 2. Fidelidad de puerta

Para verificar si una puerta implementada en hardware reproduce la operación ideal, se usa la **fidelidad de proceso** o **fidelidad de puerta** (gate fidelity).

La fidelidad media de una operación cuántica $\mathcal{E}$ respecto a la unitaria ideal $U$ es:

$$
F_\text{avg}(\mathcal{E}, U) = \int d|\psi\rangle \, F\bigl(U|\psi\rangle, \mathcal{E}(|\psi\rangle\langle\psi|)\bigr)
$$

donde la integral es sobre la medida de Haar (distribución uniforme sobre estados puros).

Para un qubit, esta integral se simplifica:

$$
F_\text{avg} = \frac{2 F_\text{process} + 1}{3}
$$

donde $F_\text{process}$ es la fidelidad de proceso cuántico.

Los mejores procesadores superconductores actuales tienen:
- $F_\text{avg}(X, H, \ldots) > 99.9\%$ para puertas de un qubit.
- $F_\text{avg}(CNOT) > 99\%$ para puertas de dos qubits.

## 3. Randomized benchmarking (RB)

La **tomografía de procesos** (QPT) es exponencialmente costosa: requiere $4^n \cdot (4^n - 1)/2$ parámetros para una puerta de $n$ qubits. Para medir la fidelidad de puerta de forma escalable, se usa el **randomized benchmarking**.

El protocolo RB estándar:
1. Preparar el qubit en $|0\rangle$.
2. Aplicar una secuencia de $m$ puertas de Clifford aleatorias seguida de la puerta inversa.
3. Medir la probabilidad de regresar a $|0\rangle$.
4. Repetir para distintas longitudes $m$.

Si las puertas tienen error aleatorio depolarizante con parámetro $p$, la probabilidad de retorno decae exponencialmente:

$$
P(m) = A \cdot r^m + B
$$

donde $r = 1 - (1 - p)/(d-1)$ con $d = 2^n$ y $p$ es la tasa de error por puerta. La **fidelidad por puerta Clifford** es:

$$
r = F_\text{Clifford} = 1 - p
$$

La ventaja del RB es que es robusto frente a errores de preparación y medición (SPAM errors).

## 4. Tomografía de proceso cuántico (QPT)

La **tomografía de proceso cuántico** (QPT) reconstruye completamente la operación $\mathcal{E}$ usando la representación $\chi$:

$$
\mathcal{E}(\rho) = \sum_{mn} \chi_{mn} E_m \rho E_n^\dagger
$$

donde $\{E_m\}$ es una base de operadores (típicamente los productos de Pauli).

El procedimiento:
1. Preparar $4^n$ estados de entrada de referencia.
2. Aplicar la operación $\mathcal{E}$ a cada uno.
3. Realizar QST sobre los estados de salida.
4. Invertir el sistema lineal para obtener $\chi$.

Coste: $O(4^n)$ preparaciones de estado y $O(4^n)$ estados de salida a tomografiar, cada uno con $O(4^n)$ mediciones.

## 5. Implementación en Qiskit

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp, Statevector, process_fidelity, Operator
import numpy as np

# Calcular la fidelidad de un estado preparado vs el ideal
def state_fidelity_test(prepared_circuit: QuantumCircuit, ideal_state: Statevector) -> float:
    """Fidelidad entre el estado preparado por el circuito y el estado ideal."""
    actual_state = Statevector(prepared_circuit)
    return float(ideal_state.inner(actual_state).real**2 + ideal_state.inner(actual_state).imag**2)

# Ejemplo: puerta H ideal vs circuito con ruido
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

# Preparar circuito ideal
qc_ideal = QuantumCircuit(1)
qc_ideal.h(0)

ideal_state = Statevector.from_label('+')  # H|0> = |+>
prepared_state = Statevector(qc_ideal)
F_ideal = abs(ideal_state.inner(prepared_state))**2
print(f"Fidelidad circuito ideal: {F_ideal:.6f}")

# Fidelidad de proceso para la puerta CNOT
cnot_circuit = QuantumCircuit(2)
cnot_circuit.cx(0, 1)
cnot_ideal = Operator.from_label('CX')
cnot_actual = Operator(cnot_circuit)
F_process = process_fidelity(cnot_actual, cnot_ideal)
print(f"Fidelidad de proceso CNOT: {F_process:.6f}")
```

## 6. Benchmarks de hardware: métricas estándar

Las métricas más usadas para comparar procesadores cuánticos:

**Quantum Volume (QV):** mide el mayor circuito cuadrado ($n$ qubits, profundidad $n$) que el dispositivo puede ejecutar con fidelidad $> 2/3$. Un procesador con $QV = 64$ puede ejecutar circuitos de 6 qubits y profundidad 6 con fiabilidad.

**CLOPS (Circuit Layer Operations Per Second):** mide la velocidad de ejecución de circuitos cuánticos parametrizados, relevante para algoritmos variacionales.

**Error por puerta de 2 qubits:** la métrica más directamente relevante para algoritmos.

## 7. Ideas clave

- La fidelidad $F \in [0,1]$ mide el parecido entre dos estados; $F = 1$ para estados idénticos.
- La fidelidad de puerta mide qué bien un dispositivo implementa una operación ideal.
- El randomized benchmarking mide la fidelidad por puerta de forma escalable y robusta frente a SPAM.
- La tomografía de proceso reconstruye completamente una operación cuántica, pero escala exponencialmente.
- Las métricas QV y CLOPS permiten comparar dispositivos de distintas plataformas.

## 8. Ejercicios sugeridos

1. Calcular la fidelidad entre $|+\rangle$ y $|+i\rangle = \frac{1}{\sqrt{2}}(|0\rangle + i|1\rangle)$.
2. Para un canal despolarizante con $p = 0.05$, calcular la fidelidad media de la identidad.
3. Simular el protocolo de randomized benchmarking para un qubit con error de depolarización y estimar la fidelidad por puerta a partir de la curva de decaimiento.
4. Explicar por qué el QV aumenta cuando tanto el número de qubits como la fidelidad de las puertas mejoran.

## Navegacion

- Anterior: [Tomografia de estados: intuicion y reconstruccion](01_tomografia_de_estados_intuicion_y_reconstruccion.md)
- Siguiente: [Trotter-Suzuki y coste de simulacion](../20_simulacion_cuantica_avanzada/01_trotter_suzuki_y_coste_de_simulacion.md)
