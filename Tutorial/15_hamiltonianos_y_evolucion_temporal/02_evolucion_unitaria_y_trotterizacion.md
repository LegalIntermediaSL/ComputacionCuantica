# Evolución unitaria y trotterización

## 1. La ecuación de Schrödinger dependiente del tiempo

La evolución de un estado cuántico bajo un Hamiltoniano $H$ independiente del tiempo está gobernada por la ecuación de Schrödinger:

$$
i\hbar \frac{d}{dt}|\psi(t)\rangle = H|\psi(t)\rangle
$$

La solución formal es:

$$
|\psi(t)\rangle = e^{-iHt/\hbar} |\psi(0)\rangle = U(t)|\psi(0)\rangle
$$

donde el operador de evolución $U(t) = e^{-iHt/\hbar}$ es unitario. En unidades donde $\hbar = 1$:

$$
U(t) = e^{-iHt}
$$

El problema de la **simulación cuántica** consiste en implementar $U(t)$ como un circuito cuántico eficiente.

## 2. El problema de la exponencial matricial

Para un Hamiltoniano de $n$ qubits, $H$ es una matriz de tamaño $2^n \times 2^n$. Calcular $e^{-iHt}$ exactamente requiere diagonalizar $H$, con coste $O(2^{3n})$ en un ordenador clásico.

En un procesador cuántico, la dificultad es diferente: incluso si $H = A + B$ con $A$ y $B$ conocidos, en general:

$$
e^{-i(A+B)t} \neq e^{-iAt} e^{-iBt}
$$

porque los operadores $A$ y $B$ no conmutan ($[A, B] \neq 0$). Esto impide implementar $e^{-iHt}$ simplemente aplicando las exponenciales de los términos individuales en secuencia.

## 3. La fórmula de Trotter-Suzuki

La aproximación de Trotter (primer orden) divide el tiempo de evolución en $n$ pasos pequeños:

$$
e^{-i(A+B)t} = \lim_{n\to\infty} \left(e^{-iAt/n} e^{-iBt/n}\right)^n
$$

Para $n$ finito, el error de truncación es:

$$
\left\| e^{-i(A+B)t} - \left(e^{-iAt/n} e^{-iBt/n}\right)^n \right\| \leq \frac{t^2 \|[A,B]\|}{2n}
$$

La fórmula de Suzuki de segundo orden (Trotter-Suzuki simétrico) reduce el error a $O(1/n^2)$:

$$
e^{-i(A+B)t} \approx \left(e^{-iAt/2n} e^{-iBt/n} e^{-iAt/2n}\right)^n
$$

En general, para un Hamiltoniano con $L$ términos $H = \sum_{k=1}^L h_k$, la fórmula de Trotter de primer orden es:

$$
e^{-iHt} \approx \left(\prod_{k=1}^L e^{-ih_k t/n}\right)^n
$$

## 4. Implementación de la trotterización en Qiskit

Cada término $h_k$ en la descomposición de Pauli se puede implementar como una rotación sobre un eje de Pauli o como un producto de puertas simples. Por ejemplo:

- $e^{-i\theta Z/2} = R_z(\theta)$
- $e^{-i\theta X/2} = R_x(\theta)$
- $e^{-i\theta Z \otimes Z/2}$: se implementa con CNOT + $R_z$ + CNOT

```python
from qiskit import QuantumCircuit
import numpy as np

def trotter_step_heisenberg(theta: float) -> QuantumCircuit:
    """
    Un paso de Trotter para H = J(XX + YY + ZZ) con J*dt = theta.
    """
    qc = QuantumCircuit(2)

    # exp(-i*theta*XX/2): Rx Rx CNOT Rz CNOT Rx Rx
    qc.rx(np.pi/2, [0, 1])
    qc.cx(0, 1)
    qc.rz(2*theta, 1)
    qc.cx(0, 1)
    qc.rx(-np.pi/2, [0, 1])

    # exp(-i*theta*YY/2)
    qc.ry(np.pi/2, [0, 1])
    qc.cx(0, 1)
    qc.rz(2*theta, 1)
    qc.cx(0, 1)
    qc.ry(-np.pi/2, [0, 1])

    # exp(-i*theta*ZZ/2)
    qc.cx(0, 1)
    qc.rz(2*theta, 1)
    qc.cx(0, 1)

    return qc

# Simular evolución temporal con n_steps pasos de Trotter
def simulate_evolution(t: float, n_steps: int) -> QuantumCircuit:
    dt = t / n_steps
    qc = QuantumCircuit(2, 2)

    # Estado inicial |01>
    qc.x(1)

    for _ in range(n_steps):
        qc.compose(trotter_step_heisenberg(dt), inplace=True)

    qc.measure([0, 1], [0, 1])
    return qc

# Comparar 1 vs 10 pasos de Trotter para t=1.0
from qiskit.primitives import StatevectorSampler
sampler = StatevectorSampler()

for n in [1, 5, 10]:
    qc = simulate_evolution(t=1.0, n_steps=n)
    result = sampler.run([qc], shots=2048).result()
    print(f"n={n}: {result[0].data.c.get_counts()}")
```

## 5. Coste y precisión

El número de puertas CNOT necesarias para simular $H$ hasta tiempo $t$ con error $\epsilon$:

- **Trotter primer orden:** $O\left(\frac{(Lt)^2}{\epsilon}\right)$ puertas de dos qubits.
- **Trotter-Suzuki $k$-ésimo orden:** $O\left(\frac{(Lt)^{1+1/2k}}{\epsilon^{1/2k}}\right)$.
- **Algoritmos de qubitización (LCU):** $O\left(Lt + \frac{\log(1/\epsilon)}{\log\log(1/\epsilon)}\right)$ (óptimo asintótico).

En hardware NISQ con profundidad de circuito limitada, el número de pasos de Trotter está restringido. Esto limita la precisión de la simulación a tiempos de evolución cortos.

## 6. Ventaja cuántica en simulación

Seth Lloyd demostró en 1996 que la simulación de sistemas cuánticos de $n$ partículas mediante trotterización requiere un número de operaciones que escala polinomialmente en $n$ en un procesador cuántico, frente al coste exponencial en un ordenador clásico (que debe almacenar el estado en $2^n$ amplitudes).

Esta es la ventaja cuántica más directamente motivada por la física: simular la naturaleza con hardware que obedece las mismas leyes.

## 7. Ideas clave

- La evolución unitaria del sistema cuántico está dada por $U(t) = e^{-iHt}$.
- La exponencial matricial no se factoriza cuando los términos del Hamiltoniano no conmutan.
- La trotterización divide el tiempo en pasos pequeños y aproxima $e^{-iHt}$ como producto de exponenciales simples.
- El error de Trotter de primer orden escala como $O(t^2/n)$; Trotter-Suzuki de orden $k$ reduce el error a $O(t^{1+1/k}/n^{1/k})$.
- La simulación cuántica de sistemas físicos fue la motivación original de Feynman para la computación cuántica.

## 8. Ejercicios sugeridos

1. Calcular explícitamente el conmutador $[X, Z]$ y verificar que $e^{-i(X+Z)t} \neq e^{-iXt}e^{-iZt}$.
2. Implementar un paso de Trotter para el Hamiltoniano $H = Z \otimes I + I \otimes Z + X \otimes X$ y verificar que la energía se conserva para un estado propio.
3. Comparar la distribución de salida de la trotterización con 1, 5 y 20 pasos para el sistema de Heisenberg partiendo del estado $|01\rangle$ a tiempo $t = 2$.
4. Estimar el número de puertas CNOT necesarias para simular $H = \sum_{k=1}^{10} Z_k Z_{k+1}$ durante $t = 1$ con error $\epsilon = 0.01$ usando Trotter de primer orden.

## Navegacion

- Anterior: [Observables y Hamiltonianos](01_observables_y_hamiltonianos.md)
- Siguiente: [Canales cuanticos: intuicion y representacion](../16_canales_cuanticos_y_ruido/01_canales_cuanticos_intuicion_y_representacion.md)
