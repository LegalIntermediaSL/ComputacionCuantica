# Algoritmo de Deutsch-Jozsa

## 1. El problema de la caja negra

El algoritmo de Deutsch-Jozsa fue el primer ejemplo de un algoritmo cuántico que supera exponencialmente al mejor algoritmo clásico determinista para un problema concreto. Su importancia es sobre todo histórica y pedagógica: establece de forma limpia cómo la interferencia cuántica permite extraer información global sobre una función con una sola consulta.

El problema plantea lo siguiente: dada una función booleana

$$
f : \{0,1\}^n \to \{0,1\}
$$

implementada como una caja negra (oráculo), debemos determinar si $f$ es **constante** (devuelve siempre el mismo valor) o **balanceada** (devuelve $0$ para exactamente la mitad de las entradas y $1$ para la otra mitad).

Clásicamente, en el peor de los casos, se necesitan $2^{n-1} + 1$ consultas para estar seguros. El algoritmo cuántico resuelve el problema con **una única consulta** al oráculo.

## 2. Preparación del estado inicial

El circuito opera sobre $n + 1$ qubits. Los primeros $n$ qubits forman el registro de consulta; el último es un qubit auxiliar.

El estado inicial es $|0\rangle^{\otimes n} |1\rangle$. Aplicando una capa de puertas Hadamard a todos los qubits obtenemos:

$$
|\psi_0\rangle = H^{\otimes n}|0\rangle^{\otimes n} \otimes H|1\rangle
= \frac{1}{\sqrt{2^n}} \sum_{x \in \{0,1\}^n} |x\rangle \otimes |-\rangle
$$

donde $|-\rangle = \frac{1}{\sqrt{2}}(|0\rangle - |1\rangle)$ es el estado propio del Hadamard que da lugar al phase kickback.

## 3. Phase kickback: el mecanismo central

El oráculo implementa la función mediante la transformación unitaria $U_f$:

$$
U_f |x\rangle |y\rangle = |x\rangle |y \oplus f(x)\rangle
$$

Cuando el registro auxiliar está en el estado $|-\rangle$, la acción del oráculo produce un cambio de fase condicional:

$$
U_f |x\rangle |-\rangle = (-1)^{f(x)} |x\rangle |-\rangle
$$

La información de $f(x)$ se ha trasladado de los bits a las fases. Este mecanismo se denomina **phase kickback** y es un ingrediente recurrente en los algoritmos cuánticos.

Tras aplicar el oráculo, el estado del registro de consulta es:

$$
|\psi_1\rangle = \frac{1}{\sqrt{2^n}} \sum_{x \in \{0,1\}^n} (-1)^{f(x)} |x\rangle
$$

## 4. Interferencia y medición

Aplicamos de nuevo $H^{\otimes n}$ al registro de consulta. El estado final es:

$$
|\psi_2\rangle = \frac{1}{2^n} \sum_{y \in \{0,1\}^n} \left( \sum_{x \in \{0,1\}^n} (-1)^{f(x) + x \cdot y} \right) |y\rangle
$$

La amplitud del estado $|0\rangle^{\otimes n}$ es:

$$
A_0 = \frac{1}{2^n} \sum_{x \in \{0,1\}^n} (-1)^{f(x)}
$$

- Si $f$ es **constante**, todos los términos tienen el mismo signo y $|A_0| = 1$. Medimos $|0\rangle^{\otimes n}$ con probabilidad $1$.
- Si $f$ es **balanceada**, la mitad de los términos son $+1$ y la otra mitad $-1$, con lo que $A_0 = 0$. Nunca medimos $|0\rangle^{\otimes n}$.

## 5. Circuito completo

```
q_0: ─H─────────oráculo───H─M
q_1: ─H─────────oráculo───H─M
...
q_n-1: ─H───────oráculo───H─M
q_anc: ─X─H─────oráculo────────
```

## 6. Implementación en Qiskit

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

def deutsch_jozsa(n: int, oracle_type: str = "balanced") -> QuantumCircuit:
    qc = QuantumCircuit(n + 1, n)

    # Qubit auxiliar en |1>
    qc.x(n)

    # Hadamards iniciales sobre todos los qubits
    qc.h(range(n + 1))
    qc.barrier()

    # Oráculo balanceado: CNOT de cada qubit de consulta al auxiliar
    # Oráculo constante: no requiere puertas adicionales
    if oracle_type == "balanced":
        for qubit in range(n):
            qc.cx(qubit, n)

    qc.barrier()

    # Hadamards finales sobre el registro de consulta
    qc.h(range(n))

    # Medir el registro de consulta
    qc.measure(range(n), range(n))
    return qc

# Ejemplo con n=3 y oráculo balanceado
qc = deutsch_jozsa(3, oracle_type="balanced")
sampler = StatevectorSampler()
result = sampler.run([qc], shots=1024).result()
counts = result[0].data.c.get_counts()
print(f"Resultados: {counts}")
# Para oráculo balanceado: nunca aparece "000"
# Para oráculo constante: solo aparece "000"
```

## 7. Complejidad y límites de la ventaja

El algoritmo requiere exactamente una consulta al oráculo, independientemente de $n$. La ganancia exponencial frente al caso clásico determinista proviene de la capacidad de evaluar la función sobre todas las entradas en superposición y extraer una propiedad global mediante interferencia.

Es importante señalar que la ganancia desaparece frente a algoritmos clásicos **probabilistas**: un clasificador aleatorio puede distinguir ambos casos con alta probabilidad usando solo $O(1)$ consultas al oráculo. La ventaja cuántica de Deutsch-Jozsa es exclusivamente sobre algoritmos clásicos deterministas.

Esta distinción es una lección metodológica importante: la ganancia cuántica depende del modelo de computación clásico con el que se compara.

## 8. Ideas clave

- El problema pide distinguir funciones constantes de balanceadas con el mínimo número de consultas.
- El phase kickback traslada la información de $f(x)$ de los bits a las fases del estado cuántico.
- La interferencia destructiva elimina la amplitud del estado $|0\rangle^{\otimes n}$ cuando $f$ es balanceada.
- Una sola consulta cuántica es suficiente frente a $2^{n-1}+1$ en el caso clásico determinista.
- La ventaja no se extiende frente a algoritmos clásicos probabilistas.

## 9. Ejercicios sugeridos

1. Construir el oráculo para la función constante que siempre devuelve $1$ y verificar que el algoritmo mide $|0\rangle^{\otimes n}$.
2. Para $n = 2$, simular el circuito con Qiskit y comprobar que un oráculo balanceado nunca produce $|00\rangle$.
3. Calcular explícitamente la amplitud $A_0$ para $n = 1$ con $f$ constante igual a $0$ y con $f$ balanceada.
4. Diseñar un oráculo balanceado para $n = 3$ diferente al CNOT en cascada y verificar que el algoritmo lo identifica correctamente.

## Navegacion

- Anterior: [Qiskit Runtime y primitives](../04_qiskit/01_qiskit_runtime_y_primitives.md)
- Siguiente: [Bernstein-Vazirani](02_bernstein_vazirani.md)
