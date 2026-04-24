# Transformada Cuántica de Fourier (QFT)

## 1. Definición formal

La Transformada Cuántica de Fourier (QFT) es el análogo cuántico de la Transformada de Fourier Discreta (DFT). Actúa sobre la base computacional de la siguiente manera:

$$
\text{QFT}_N |j\rangle = \frac{1}{\sqrt{N}} \sum_{k=0}^{N-1} e^{2\pi i j k / N} |k\rangle
$$

donde $N = 2^n$ y $j \in \{0, 1, \ldots, N-1\}$.

Sobre un estado general $|\psi\rangle = \sum_{j} x_j |j\rangle$, la QFT produce $\sum_{k} y_k |k\rangle$ donde:

$$
y_k = \frac{1}{\sqrt{N}} \sum_{j=0}^{N-1} x_j \, e^{2\pi i j k / N}
$$

La QFT es una operación unitaria y su inversa $\text{QFT}^\dagger$ se obtiene conjugando las fases: $e^{2\pi i / N} \to e^{-2\pi i / N}$.

## 2. Factorización producto

Para $n$ qubits y $j = j_1 j_2 \cdots j_n$ en representación binaria ($j_1$ es el bit más significativo), la QFT admite una factorización:

$$
\text{QFT}_N |j\rangle = \frac{1}{\sqrt{N}} \bigotimes_{l=1}^{n} \left( |0\rangle + e^{2\pi i \, 0.j_{n-l+1}\cdots j_n} |1\rangle \right)
$$

donde $0.j_{n-l+1} \cdots j_n$ denota la fracción binaria $\sum_{m=1}^{l} j_{n-l+m} / 2^m$.

Esta factorización es la clave para construir el circuito eficiente: cada factor tensorial depende solo de un subconjunto de bits de entrada, lo que permite implementarlo con puertas de uno y dos qubits.

## 3. Construcción del circuito

El circuito de la QFT para $n$ qubits usa dos tipos de puertas:

**Hadamard** $H$: crea la superposición $\frac{1}{\sqrt{2}}(|0\rangle + e^{2\pi i \cdot 0.j_l} |1\rangle)$ sobre el qubit $l$.

**Puertas de fase controlada** $R_k$:

$$
R_k = \begin{pmatrix} 1 & 0 \\ 0 & e^{2\pi i / 2^k} \end{pmatrix}
$$

El algoritmo procesa los qubits de mayor a menor significancia. Para el qubit $l$:
1. Aplicar $H$.
2. Aplicar $R_2, R_3, \ldots, R_{n-l+1}$ controladas por los qubits $l+1, \ldots, n$.

Al final se aplican SWAPs para invertir el orden de los qubits de salida.

El número total de puertas es $\frac{n(n+1)}{2} + \lfloor n/2 \rfloor = O(n^2)$, frente a $O(n \cdot 2^n)$ de la FFT clásica sobre $N = 2^n$ elementos.

## 4. Implementación en Qiskit

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
import numpy as np

def qft_circuit(n: int, inverse: bool = False) -> QuantumCircuit:
    """Construye el circuito QFT o su inversa para n qubits."""
    qc = QuantumCircuit(n)

    def _qft_rotations(circuit, k):
        """Aplica H y las puertas de fase controladas al qubit k."""
        circuit.h(k)
        for j in range(k + 1, n):
            circuit.cp(2 * np.pi / 2 ** (j - k + 1), j, k)

    for qubit in range(n):
        _qft_rotations(qc, qubit)

    # Invertir orden de qubits (SWAPs)
    for i in range(n // 2):
        qc.swap(i, n - 1 - i)

    if inverse:
        qc = qc.inverse()
        qc.name = "QFT†"
    else:
        qc.name = "QFT"

    return qc

# Aplicar QFT al estado |5> en 4 qubits y luego QFT† para recuperar |5>
n = 4
target = 5  # |0101>

qc = QuantumCircuit(n, n)
for i, bit in enumerate(format(target, f'0{n}b')[::-1]):
    if bit == '1':
        qc.x(i)

qc.compose(qft_circuit(n), inplace=True)
qc.compose(qft_circuit(n, inverse=True), inplace=True)
qc.measure(range(n), range(n))

sampler = StatevectorSampler()
result = sampler.run([qc], shots=1024).result()
print(result[0].data.c.get_counts())
# Debe aparecer solo el estado target con probabilidad 1
```

## 5. Limitación fundamental: las amplitudes no son legibles

La QFT cuántica no es directamente equivalente a la FFT clásica en términos de utilidad general. Esta es la razón:

Los coeficientes $y_k$ de la transformada están codificados en las **amplitudes** del estado cuántico, que no son accesibles directamente. Medir el estado produce un único valor $k$ muestreado de la distribución $|y_k|^2$, destruyendo el estado en el proceso.

Por tanto, la QFT no sirve para analizar señales clásicas de forma eficiente. Su valor está en ser una subrutina dentro de algoritmos cuánticos donde la información de periodicidad se puede aprovechar internamente sin necesidad de leer todos los coeficientes.

## 6. La QFT como subrutina fundamental

**Estimación de fase (QPE):** La QFT inversa extrae la representación binaria de una fase codificada en amplitudes. Es el núcleo del algoritmo de Shor y de los métodos de química cuántica.

**Algoritmo de Shor:** La periodicidad de $f(x) = a^x \bmod N$ se codifica en el estado como una superposición de estados con fase periódica. La QFT inversa transforma esa periodicidad en un resultado medible que revela los factores de $N$.

**Algoritmos de estimación de amplitudes:** La QFT aparece como componente en versiones más generales del algoritmo de Grover para estimar probabilidades de forma cuadráticamente más eficiente.

## 7. Ideas clave

- La QFT mapea las amplitudes de la base computacional a sus coeficientes de Fourier discretos.
- El circuito se construye con $O(n^2)$ puertas, exponencialmente más eficiente que la FFT clásica sobre $N = 2^n$ puntos.
- Las amplitudes de salida no son directamente legibles: la QFT no sirve para analizar señales clásicas.
- La QFT es la subrutina central de Phase Estimation, del algoritmo de Shor y de otros algoritmos cuánticos importantes.
- La QFT inversa se obtiene invirtiendo el circuito y conjugando todas las fases.

## 8. Ejercicios sugeridos

1. Construir el circuito QFT para $n = 3$ a mano y verificar con Qiskit que produce el resultado correcto sobre $|0\rangle$.
2. Calcular la QFT del estado $|0\rangle$ para $n = 2$ y verificar que produce la superposición uniforme $|+\rangle^{\otimes 2}$.
3. Aplicar QFT y $\text{QFT}^\dagger$ consecutivamente sobre un estado arbitrario y verificar que el resultado es la identidad.
4. Comparar el número de puertas del circuito QFT para $n = 4, 8, 16$ con el número de operaciones de la FFT clásica.

## Navegacion

- Anterior: [Grover](03_grover.md)
- Siguiente: [Phase Estimation](05_phase_estimation.md)
