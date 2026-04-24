# Trotter-Suzuki: coste y límites de la simulación cuántica

## 1. Recapitulación: por qué la trotterización no es trivial

En el módulo anterior vimos que el operador de evolución $e^{-iHt}$ para un Hamiltoniano $H = \sum_k h_k$ no se factoriza directamente porque los términos $h_k$ no conmutan. La trotterización resuelve esto a costa de introducir un **error de Trotter** que depende del número de pasos $n$ y del tiempo total $t$.

El problema central es que, en hardware NISQ con tiempos de coherencia finitos, no podemos usar $n$ arbitrariamente grande: cada paso de Trotter requiere un número fijo de puertas CNOT, y la profundidad total crece como $O(n)$.

Existe por tanto una tensión fundamental entre precisión (requiere $n$ grande) y feasibilidad en hardware ruidoso (requiere $n$ pequeño).

## 2. Coste de circuito de la trotterización

Para un Hamiltoniano con $L$ términos de Pauli de $k$ qubits, cada término $e^{-i\theta P}$ con $P$ un operador de Pauli de $k$ cuerpos requiere exactamente $2(k-1)$ puertas CNOT más una rotación de un qubit.

El coste total de un paso de Trotter de primer orden:

| Tipo de Hamiltoniano | Términos ($L$) | CNOTs por paso | CNOTs totales ($n$ pasos) |
|---|---|---|---|
| Ising 1D ($n$ sitios) | $n-1$ | $2(n-1)$ | $2n(n-1)$ |
| Heisenberg 1D | $3(n-1)$ | $6(n-1)$ | $6n(n-1)$ |
| Molécula H₂ (8 terms) | 8 | 14 | $14n$ |
| FeMoco (nitrogenasa, ~1000 terms) | ~1000 | ~2000 | $2000n$ |

Para FeMoco con $n = 100$ pasos y puertas CNOT con tasa de error $1\%$: la probabilidad de que el circuito completo tenga cero errores es $(0.99)^{200000} \approx e^{-2000} \approx 0$. El circuito es completamente dominado por el ruido.

## 3. Error de Trotter y su análisis

Para la fórmula de primer orden, el error es:

$$
\left\|e^{-iHt} - \left(\prod_k e^{-ih_k t/n}\right)^n\right\| \leq \frac{t^2}{2n} \sum_{j<k} \|[h_j, h_k]\|
$$

La fórmula de Suzuki de orden $2p$ reduce el error a $O(t^{2p+1}/n^{2p})$, pero a costa de multiplicar el número de puertas por un factor exponencial en $p$.

**Ejemplo concreto:** para simular la evolución de una molécula con $H_2O$ (8 términos) durante $t = 1$ con error $\epsilon = 0.01$:

- Trotter orden 1: $n = O(t^2 \Lambda^2 / \epsilon) \approx 150$ pasos, $\sim 2100$ puertas CNOT.
- Trotter-Suzuki orden 2: $n = O(t^{3/2} \Lambda^{3/2} / \epsilon^{1/2}) \approx 30$ pasos, $\sim 420$ puertas CNOT.
- Qubitización (algoritmo LCU): $O(t\Lambda + \log(1/\epsilon)) \approx 50$ puertas CNOT (con QRAM).

## 4. Más allá de la trotterización: métodos de qubitización

Los **algoritmos de qubitización** (qubitization) superan a la trotterización en complejidad asintótica. En lugar de aproximar $e^{-iHt}$ como producto, codifican $H$ directamente en un oráculo y usan QPE para acceder a sus autovalores.

El método LCU (Linear Combination of Unitaries) expresa:

$$
H = \sum_k \alpha_k U_k, \quad \alpha_k > 0, \quad U_k \text{ unitarios}
$$

y construye el operador de selección $\text{SELECT}(H) = \sum_k |k\rangle\langle k| \otimes U_k$. Combinado con QPE, esto da el algoritmo de simulación cuántica más eficiente conocido, con coste $O(t \|H\|_1 + \log(1/\epsilon))$ donde $\|H\|_1 = \sum_k |\alpha_k|$.

## 5. Simulación variacional del tiempo (AVQDS/McLachlan)

Un enfoque alternativo para hardware NISQ es la **simulación variacional de la evolución temporal** (AVQDS, Adaptive Variational Quantum Dynamics Simulation). En lugar de trotterizar, se usa un ansatz parametrizado y se minimiza la distancia entre la evolución exacta y la variacional en cada paso:

$$
\min_{\dot{\vec{\theta}}} \left\| \frac{d}{dt}|\psi(\vec{\theta})\rangle - (-iH)|\psi(\vec{\theta})\rangle \right\|
$$

Esto da un sistema de ecuaciones diferenciales ordinarias para $\vec{\theta}(t)$ que puede resolverse clásicamente, mientras que la QPU evalúa las métricas cuánticas necesarias.

La ventaja es que el circuito tiene profundidad fija (la del ansatz), independiente del tiempo de simulación. El inconveniente es que la calidad de la simulación depende de la expresividad del ansatz.

## 6. Implementación de un paso Trotter-Suzuki en Qiskit

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp
import numpy as np

def second_order_trotter_step(J: float, dt: float) -> QuantumCircuit:
    """
    Paso Trotter-Suzuki de orden 2 para H = J*(XX + YY + ZZ).
    exp(-i*J*(XX+YY+ZZ)*dt) ≈ exp(-i*J*ZZ*dt/2) * exp(-i*J*YY*dt) * exp(-i*J*ZZ*dt/2)
    """
    qc = QuantumCircuit(2)

    def rzz_gate(circuit, theta, q0, q1):
        circuit.cx(q0, q1)
        circuit.rz(theta, q1)
        circuit.cx(q0, q1)

    def ryy_gate(circuit, theta, q0, q1):
        circuit.rx(np.pi/2, [q0, q1])
        circuit.cx(q0, q1)
        circuit.rz(theta, q1)
        circuit.cx(q0, q1)
        circuit.rx(-np.pi/2, [q0, q1])

    def rxx_gate(circuit, theta, q0, q1):
        circuit.h([q0, q1])
        circuit.cx(q0, q1)
        circuit.rz(theta, q1)
        circuit.cx(q0, q1)
        circuit.h([q0, q1])

    # exp(-i*J*ZZ*dt/2)
    rzz_gate(qc, 2*J*dt/2, 0, 1)
    # exp(-i*J*YY*dt)
    ryy_gate(qc, 2*J*dt, 0, 1)
    # exp(-i*J*ZZ*dt/2)
    rzz_gate(qc, 2*J*dt/2, 0, 1)

    return qc

# Simular H = 0.5*(XX+YY+ZZ) desde |01> durante t=2
J, t_total, n_steps = 0.5, 2.0, 20
dt = t_total / n_steps

H = SparsePauliOp.from_list([("XX", J), ("YY", J), ("ZZ", J)])
estimator = StatevectorEstimator()

qc = QuantumCircuit(2)
qc.x(1)  # Estado inicial |01>

energies = []
for step in range(n_steps):
    qc.compose(second_order_trotter_step(J, dt), inplace=True)
    result = estimator.run([(qc.copy(), H)]).result()
    energies.append(result[0].data.evs)

print(f"Energía inicial: {energies[0]:.4f}")
print(f"Energía final: {energies[-1]:.4f}")
print(f"(La energía se conserva si la trotterización es precisa)")
```

## 7. Ideas clave

- Cada paso de Trotter tiene un coste en CNOTs que crece con el número de términos del Hamiltoniano.
- Para muchos pasos y Hamiltonianos complejos, el ruido destruye la señal antes de que la simulación sea útil.
- La fórmula de Suzuki de orden $p$ reduce el error a $O(1/n^{2p})$ pero multiplica el coste por un factor exponencial en $p$.
- Los algoritmos de qubitización (LCU) son asintóticamente más eficientes pero requieren QRAM u overhead de preparación de estado.
- La simulación variacional del tiempo resuelve la limitación de profundidad en hardware NISQ a costa de expresividad del ansatz.

## 8. Ejercicios sugeridos

1. Calcular el número de puertas CNOT necesarias para simular el Hamiltoniano de Heisenberg de 4 qubits durante $t = 1$ con $n = 10$ pasos usando Trotter de primer orden.
2. Comparar el error de Trotter de primer y segundo orden para $n = 5, 10, 20$ pasos en el modelo $H = X \otimes X + Z \otimes I$.
3. Implementar la simulación variacional de la evolución temporal con un ansatz de 4 parámetros para el oscilador armónico cuántico.
4. Estimar el tiempo máximo de simulación viable para el sistema de Heisenberg de 4 qubits dado $T_2 = 100\,\mu s$ y puertas CNOT de $300\,ns$.

## Navegacion

- Anterior: [Fidelidad y caracterizacion operacional](../19_tomografia_y_caracterizacion/02_fidelidad_y_caracterizacion_operacional.md)
- Siguiente: [Simulacion digital frente a analogica](02_simulacion_digital_frente_a_analogica.md)
