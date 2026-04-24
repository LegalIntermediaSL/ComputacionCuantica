# Estimación de Fase Cuántica (QPE)

## 1. El problema de la fase de un autovector

Los autovalores de un operador unitario $U$ son siempre números complejos de módulo $1$, parametrizados por una fase:

$$
U|u\rangle = e^{2\pi i \phi} |u\rangle, \quad \phi \in [0, 1)
$$

El objetivo de la **Quantum Phase Estimation (QPE)** es estimar $\phi$ con alta precisión dado acceso al operador $U$ y al estado $|u\rangle$. La fase $\phi$ suele contener información física directamente útil: la energía de un sistema cuántico ($\phi \propto E$), el período de una función periódica, o los autovalores de un operador Hamiltoniano.

## 2. Estructura del circuito

QPE utiliza dos registros de qubits:

- **Registro de conteo** ($t$ qubits): almacenará la estimación binaria de $\phi$.
- **Registro del estado** (varios qubits): contiene el autovector $|u\rangle$.

La precisión de la estimación es $|\phi - \tilde{\phi}| \leq 2^{-t}$ con probabilidad creciente con $t$.

## 3. El protocolo paso a paso

**Paso 1: Inicialización**

$$
|\psi_0\rangle = |0\rangle^{\otimes t} \otimes |u\rangle
$$

**Paso 2: Hadamards sobre el registro de conteo**

$$
|\psi_1\rangle = \frac{1}{\sqrt{2^t}} \sum_{j=0}^{2^t - 1} |j\rangle \otimes |u\rangle
$$

**Paso 3: Aplicaciones controladas de $U^{2^k}$**

El qubit $k$ del registro de conteo controla la aplicación de $U^{2^k}$. Como $U^{2^k}|u\rangle = e^{2\pi i \phi 2^k} |u\rangle$, el resultado es:

$$
|\psi_2\rangle = \frac{1}{\sqrt{2^t}} \sum_{j=0}^{2^t - 1} e^{2\pi i \phi j} |j\rangle \otimes |u\rangle
$$

El estado del registro de conteo es $\frac{1}{\sqrt{2^t}} \sum_j e^{2\pi i \phi j} |j\rangle$, que es la QFT del estado $|\lfloor 2^t \phi \rceil\rangle$.

**Paso 4: QFT inversa**

$$
\text{QFT}^\dagger \left( \frac{1}{\sqrt{2^t}} \sum_{j} e^{2\pi i \phi j} |j\rangle \right) \approx |\tilde{\phi}\rangle
$$

donde $\tilde{\phi}$ es la mejor aproximación de $\phi$ con $t$ bits.

**Paso 5: Medición del registro de conteo**

La medición produce la representación binaria de $\phi$ con $t$ bits de precisión.

## 4. Análisis de precisión

Si $\phi$ es exactamente representable con $t$ bits, el algoritmo devuelve $\phi$ con probabilidad $1$.

Si no lo es, la probabilidad de obtener el entero más cercano es al menos:

$$
P(\text{éxito}) \geq \frac{8}{\pi^2} \approx 0.81
$$

Para garantizar probabilidad de éxito $1 - \epsilon$, se necesitan $t + \lceil \log_2(2 + \frac{1}{2\epsilon}) \rceil$ qubits en el registro de conteo.

## 5. Implementación en Qiskit

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
import numpy as np

def qpe_circuit(t: int, phi: float) -> QuantumCircuit:
    """
    QPE para el operador de fase U = diag(1, exp(2*pi*i*phi)).
    El autovector es |1> con autovalor exp(2*pi*i*phi).
    t: número de qubits de conteo (precision = 1/2^t)
    """
    qc = QuantumCircuit(t + 1, t)

    # Preparar el autovector |1>
    qc.x(t)

    # Hadamards sobre el registro de conteo
    qc.h(range(t))

    # Puertas de fase controladas: qubit k controla U^(2^k)
    for k in range(t):
        angle = 2 * np.pi * phi * (2 ** k)
        qc.cp(angle, k, t)

    # QFT inversa sobre el registro de conteo
    # Paso 1: SWAPs
    for i in range(t // 2):
        qc.swap(i, t - 1 - i)
    # Paso 2: rotaciones inversas y Hadamards
    for j in range(t):
        for m in range(j):
            qc.cp(-np.pi / (2 ** (j - m)), m, j)
        qc.h(j)

    qc.measure(range(t), range(t))
    return qc

# Estimar phi = 3/8 = 0.375 con t=4 qubits (precision 1/16)
phi_true = 3 / 8
t = 4

qc = qpe_circuit(t, phi_true)

sampler = StatevectorSampler()
result = sampler.run([qc], shots=2048).result()
counts = result[0].data.c.get_counts()

# phi * 2^t = 3/8 * 16 = 6 => representación binaria "0110"
print(f"Fase verdadera: {phi_true} = {int(phi_true * 2**t)}/{2**t}")
print(f"Resultados: {counts}")
```

## 6. QPE como subrutina fundamental

**Algoritmo de Shor:** La función $f(x) = a^x \bmod N$ es periódica con período $r$. QPE aplicado al operador $U|y\rangle = |ay \bmod N\rangle$ estima $j/r$ para distintos $j$, y el algoritmo de fracciones continuas recupera $r$.

**Química cuántica:** Para encontrar la energía del estado fundamental de un Hamiltoniano $H$, se aplica QPE con $U = e^{-iHt}$, obteniendo los autovalores de $H$ directamente con precisión controlada.

**Algoritmo HHL:** Para resolver sistemas lineales $Ax = b$, QPE estima los autovalores de $A$ y permite invertirlos de forma coherente como parte del algoritmo.

## 7. Comparación con métodos clásicos

| Aspecto | Diagonalización clásica | QPE |
|---|---|---|
| Coste matricial | $O(N^3)$ para matrices $N \times N$ | $O(t^2 + t \cdot T_U)$ |
| Salida | Todos los autovalores | Un autovalor por ejecución |
| Precisión | Limitada por aritmética flotante | $2^{-t}$ con $t$ qubits |
| Ventaja cuántica | Solo si $U$ tiene implementación eficiente |

## 8. Ideas clave

- QPE estima la fase $\phi$ de $U|u\rangle = e^{2\pi i\phi}|u\rangle$ con $t$ bits de precisión.
- El mecanismo codifica $\phi$ en las fases del registro de conteo mediante $U^{2^k}$ controladas, luego usa la QFT inversa para hacerla medible.
- Si $\phi$ es exactamente representable en $t$ bits, la estimación es perfecta.
- QPE es la subrutina central de los algoritmos de Shor, HHL y métodos de química cuántica.
- La precisión mejora exponencialmente con el número de qubits del registro de conteo.

## 9. Ejercicios sugeridos

1. Simular QPE para $\phi = 1/4$ con $t = 3$ qubits y verificar que el resultado es $\texttt{010}$ (= $2/8 = 1/4$).
2. Repetir para $\phi = 1/3$ (no representable exactamente en binario) y analizar la distribución de resultados.
3. Calcular el número de aplicaciones de $U$ necesarias para estimar $\phi$ con error $< 0.01$ y probabilidad $> 0.99$.
4. Modificar el circuito para estimar la fase de la puerta $T = R_z(\pi/4)$ y verificar que $\phi = 1/8$.

## Navegacion

- Anterior: [Transformada cuantica de Fourier](04_transformada_cuantica_de_fourier.md)
- Siguiente: [Decoherencia y ruido](../06_ruido_y_hardware/01_decoherencia_y_ruido.md)
