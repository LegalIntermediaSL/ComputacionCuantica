# Algoritmo de Grover

## 1. El problema de la búsqueda no estructurada

El algoritmo de Grover resuelve el siguiente problema: dado un oráculo que implementa $f : \{0,1\}^n \to \{0,1\}$, encontrar una entrada $w$ tal que $f(w) = 1$.

Se asume que existe exactamente un elemento marcado (aunque el algoritmo se generaliza a varios). La base de datos no tiene ninguna estructura explotable: es búsqueda por fuerza bruta.

Clásicamente, en el peor caso se requieren $N = 2^n$ consultas y en promedio $N/2$. Grover logra encontrar $w$ con alta probabilidad en $O(\sqrt{N})$ consultas, una aceleración cuadrática que se ha demostrado óptima para este tipo de problema.

## 2. Estado inicial y superposición uniforme

El algoritmo trabaja en el espacio de $n$ qubits. El estado inicial es la superposición uniforme:

$$
|s\rangle = H^{\otimes n} |0\rangle^{\otimes n} = \frac{1}{\sqrt{N}} \sum_{x=0}^{N-1} |x\rangle
$$

Este estado tiene amplitud uniforme $\frac{1}{\sqrt{N}}$ sobre todos los elementos de la base computacional.

## 3. Los dos operadores de Grover

Cada iteración del algoritmo aplica dos operadores consecutivos.

### Oráculo de fase

El oráculo invierte la fase del estado marcado:

$$
O_f = I - 2|w\rangle\langle w|
$$

Para el elemento buscado $w$: $O_f |w\rangle = -|w\rangle$. Para todos los demás: $O_f |x\rangle = |x\rangle$.

Es una reflexión respecto al subespacio ortogonal a $|w\rangle$.

### Operador de difusión

El operador de difusión, también llamado inversión sobre la media, aplica la reflexión:

$$
D = 2|s\rangle\langle s| - I
$$

Amplifica las amplitudes que están por encima de la media y atenúa las que están por debajo.

## 4. Análisis geométrico

El estado del sistema vive en el subespacio bidimensional generado por $|w\rangle$ y

$$
|s_\perp\rangle = \frac{1}{\sqrt{N-1}} \sum_{x \neq w} |x\rangle
$$

El estado inicial se escribe como:

$$
|s\rangle = \sin\theta \, |w\rangle + \cos\theta \, |s_\perp\rangle, \quad \sin\theta = \frac{1}{\sqrt{N}}
$$

Cada iteración de Grover rota el estado un ángulo $2\theta$ hacia $|w\rangle$. Tras $k$ iteraciones:

$$
|\psi_k\rangle = \sin\bigl((2k+1)\theta\bigr)|w\rangle + \cos\bigl((2k+1)\theta\bigr)|s_\perp\rangle
$$

La probabilidad de medir $w$ es máxima cuando $(2k+1)\theta \approx \pi/2$, es decir:

$$
k_\text{opt} \approx \frac{\pi}{4\theta} \approx \frac{\pi}{4}\sqrt{N}
$$

## 5. Implementación en Qiskit

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
import numpy as np

def grover_oracle(n: int, target: int) -> QuantumCircuit:
    """Marca el estado |target> con un cambio de fase global."""
    qc = QuantumCircuit(n)
    target_bits = format(target, f'0{n}b')
    # Aplicar X donde el bit del target es 0
    for i, bit in enumerate(reversed(target_bits)):
        if bit == '0':
            qc.x(i)
    # Multi-controlled Z equivale a CX con el último qubit en superposición
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    # Revertir las X
    for i, bit in enumerate(reversed(target_bits)):
        if bit == '0':
            qc.x(i)
    return qc

def diffusion_operator(n: int) -> QuantumCircuit:
    """Operador de difusión: inversión sobre la media."""
    qc = QuantumCircuit(n)
    qc.h(range(n))
    qc.x(range(n))
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    qc.x(range(n))
    qc.h(range(n))
    return qc

def grover_circuit(n: int, target: int) -> QuantumCircuit:
    N = 2 ** n
    num_iter = max(1, int(np.round(np.pi / 4 * np.sqrt(N))))

    qc = QuantumCircuit(n, n)
    qc.h(range(n))

    oracle = grover_oracle(n, target)
    diff = diffusion_operator(n)

    for _ in range(num_iter):
        qc.compose(oracle, inplace=True)
        qc.compose(diff, inplace=True)

    qc.measure(range(n), range(n))
    return qc

# Buscar el elemento 5 en un espacio de 2^3 = 8
n, target = 3, 5
qc = grover_circuit(n, target)

sampler = StatevectorSampler()
result = sampler.run([qc], shots=2048).result()
counts = result[0].data.c.get_counts()
print(f"Buscando: {target} = {format(target, f'0{n}b')}")
print(f"Distribución: {counts}")
# El estado target debe aparecer con alta probabilidad (~97% para N=8, k=2)
```

## 6. Optimalidad y límites

Se ha demostrado mediante argumentos de oráculos que ningún algoritmo cuántico puede resolver la búsqueda no estructurada en menos de $\Omega(\sqrt{N})$ consultas. Grover es por tanto óptimo en este modelo.

La aceleración cuadrática contrasta con la ventaja exponencial de algoritmos como Shor, que explotan estructura algebraica (periodicidad). La búsqueda no estructurada no tiene esa estructura y la barrera $\Omega(\sqrt{N})$ es ineludible.

Para $M$ soluciones entre $N$ elementos, el número óptimo de iteraciones es $\approx \frac{\pi}{4}\sqrt{N/M}$.

## 7. Extensiones

**Amplificación de amplitudes:** La composición $O_f \cdot D$ es una instancia de amplificación de amplitudes, una técnica general que permite amplificar la probabilidad de cualquier subconjunto de estados deseados. Es una subrutina en algoritmos como estimación de amplitudes cuántica.

**Quantum walk:** El algoritmo de Grover se puede reformular como una caminata cuántica sobre el hipercubo de $n$ dimensiones, lo que abre generalizaciones a grafos arbitrarios con estructuras de vecindad.

## 8. Ideas clave

- Grover busca en una base de datos no estructurada de $N$ elementos en $O(\sqrt{N})$ consultas.
- Cada iteración aplica un oráculo de fase y un operador de difusión.
- El análisis geométrico muestra que cada iteración rota el estado $2\theta$ hacia el elemento buscado.
- La aceleración cuadrática es óptima: ningún algoritmo cuántico puede hacerlo en menos consultas.
- Para $M$ soluciones, el número óptimo de iteraciones escala como $\sqrt{N/M}$.

## 9. Ejercicios sugeridos

1. Para $N = 4$ ($n = 2$), calcular $\theta$ y el número exacto de iteraciones necesarias.
2. Simular el circuito con Qiskit para $n = 4$ y distintos valores de `target`. Verificar que la probabilidad de éxito es $> 90\%$.
3. Modificar el oráculo para marcar dos elementos simultáneamente y ajustar el número de iteraciones.
4. Simular cómo cambia la amplitud del estado buscado en cada iteración para $n = 3$ usando el simulador de vector de estado.

## Navegacion

- Anterior: [Bernstein-Vazirani](02_bernstein_vazirani.md)
- Siguiente: [Transformada cuantica de Fourier](04_transformada_cuantica_de_fourier.md)
