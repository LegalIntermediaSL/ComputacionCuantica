# Algoritmo de Bernstein-Vazirani

## 1. El problema de la cadena oculta

El algoritmo de Bernstein-Vazirani generaliza la idea de Deutsch-Jozsa hacia un problema de recuperación de información: dado un oráculo que implementa el producto escalar modular

$$
f(x) = s \cdot x \pmod{2} = s_1 x_1 \oplus s_2 x_2 \oplus \cdots \oplus s_n x_n
$$

donde $s \in \{0,1\}^n$ es una cadena secreta fija, el objetivo es determinar $s$ consultando el oráculo el mínimo número de veces.

Clásicamente, para recuperar cada bit $s_i$ se consulta $f$ con la entrada $e_i$ (un $1$ en la posición $i$ y ceros en el resto), lo que requiere $n$ consultas en total. El algoritmo cuántico recupera $s$ por completo con **una sola consulta**.

## 2. Estructura del circuito

El circuito es estructuralmente idéntico al de Deutsch-Jozsa:

1. Inicializar $n$ qubits de consulta en $|0\rangle$ y un qubit auxiliar en $|1\rangle$.
2. Aplicar $H^{\otimes n+1}$.
3. Consultar el oráculo $U_f$.
4. Aplicar $H^{\otimes n}$ al registro de consulta.
5. Medir el registro de consulta.

## 3. Análisis matemático

Tras los Hadamards iniciales:

$$
|\psi_0\rangle = \frac{1}{\sqrt{2^n}} \sum_{x \in \{0,1\}^n} |x\rangle \otimes |-\rangle
$$

El phase kickback introduce la fase $(-1)^{f(x)} = (-1)^{s \cdot x}$:

$$
|\psi_1\rangle = \frac{1}{\sqrt{2^n}} \sum_{x \in \{0,1\}^n} (-1)^{s \cdot x} |x\rangle
$$

Este estado es precisamente la transformada de Hadamard del estado $|s\rangle$. Aplicar $H^{\otimes n}$ invierte la transformada:

$$
H^{\otimes n} \left( \frac{1}{\sqrt{2^n}} \sum_{x} (-1)^{s \cdot x} |x\rangle \right) = |s\rangle
$$

La medición produce siempre $s$ con probabilidad $1$.

Para verificarlo explícitamente, la amplitud del estado $|y\rangle$ tras los Hadamards finales es:

$$
\langle y | \psi_2 \rangle = \frac{1}{2^n} \sum_{x} (-1)^{(s \oplus y) \cdot x} = \mathbf{1}[y = s]
$$

ya que $\sum_{x \in \{0,1\}^n} (-1)^{c \cdot x} = 2^n$ si $c = 0$ y $0$ en caso contrario.

## 4. Conexión con el análisis de Fourier

El resultado puede enunciarse en términos más abstractos: la función $x \mapsto (-1)^{s \cdot x}$ es el carácter del grupo $\mathbb{Z}_2^n$ asociado al elemento $s$. La transformada de Hadamard es la transformada de Fourier sobre este grupo. El algoritmo simplemente invierte una transformada lineal conocida.

Esta perspectiva muestra que Bernstein-Vazirani no hace ningún truco especial: aplica una transformada, consulta el oráculo, y aplica la transformada inversa. La eficiencia cuántica emerge de la capacidad de preparar y manipular superposiciones de forma coherente.

## 5. Implementación en Qiskit

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

def bernstein_vazirani(secret: str) -> QuantumCircuit:
    """
    Recupera la cadena secreta 's' con una sola consulta al oráculo.
    secret: cadena de bits, ej. "1011"
    """
    n = len(secret)
    qc = QuantumCircuit(n + 1, n)

    # Qubit auxiliar en |1>
    qc.x(n)

    # Hadamards iniciales
    qc.h(range(n + 1))
    qc.barrier()

    # Oráculo: CNOT del qubit i al auxiliar si secret[i] == '1'
    for i, bit in enumerate(reversed(secret)):
        if bit == '1':
            qc.cx(i, n)

    qc.barrier()

    # Hadamards finales sobre el registro de consulta
    qc.h(range(n))

    qc.measure(range(n), range(n))
    return qc

# Probar con s = "1011"
secret = "1011"
qc = bernstein_vazirani(secret)

sampler = StatevectorSampler()
result = sampler.run([qc], shots=1024).result()
counts = result[0].data.c.get_counts()
print(f"Cadena secreta: {secret}")
print(f"Resultado: {counts}")
# El resultado debe ser siempre la cadena secreta (en orden de medición)
```

## 6. Comparación con Deutsch-Jozsa

| Característica | Deutsch-Jozsa | Bernstein-Vazirani |
|---|---|---|
| Tipo de oráculo | Constante o balanceada | Producto escalar $s \cdot x$ |
| Respuesta buscada | Categoría de $f$ | Cadena secreta $s$ |
| Consultas cuánticas | 1 | 1 |
| Consultas clásicas (determinista) | $2^{n-1}+1$ | $n$ |
| Tipo de ganancia | Exponencial | Lineal |

La ventaja de Bernstein-Vazirani frente al caso clásico es lineal, no exponencial. Sin embargo, la forma en que la información queda codificada en la fase y se recupera mediante la transformada de Hadamard ilustra un principio muy general de los algoritmos cuánticos.

## 7. Ideas clave

- El oráculo implementa un producto escalar modular con una cadena secreta $s$.
- Tras el phase kickback, el estado del registro es la transformada de Hadamard de $|s\rangle$.
- Aplicar Hadamard de nuevo invierte la transformada y produce $|s\rangle$ de forma determinista.
- La ganancia cuántica sobre el caso clásico es lineal (1 consulta frente a $n$).
- El algoritmo es un caso particular del análisis de Fourier sobre el grupo $\mathbb{Z}_2^n$.

## 8. Ejercicios sugeridos

1. Verificar a mano que para $n = 2$ y $s = 11$, el estado tras el oráculo es $\frac{1}{2}(|00\rangle - |01\rangle - |10\rangle + |11\rangle)$.
2. Ejecutar el circuito con Qiskit para $s = \texttt{"10110"}$ y comprobar que siempre se recupera $s$.
3. Construir el circuito inverso: dado $|s\rangle$, producir la superposición $\frac{1}{\sqrt{2^n}} \sum_x (-1)^{s \cdot x} |x\rangle$.
4. Razonar por qué el algoritmo produce exactamente $|s\rangle$ y no una distribución de probabilidad sobre varias cadenas.

## Navegacion

- Anterior: [Deutsch-Jozsa](01_deutsch_jozsa.md)
- Siguiente: [Grover](03_grover.md)
