# Puertas cuanticas y circuitos

## 1. Operaciones unitarias

La evolucion reversible de un sistema cuantico aislado se describe mediante operadores unitarios. En computacion cuantica, esos operadores se implementan como puertas cuanticas.

Si el estado del sistema es $|\psi\rangle$, una puerta $U$ actua como

$$
|\psi'\rangle = U |\psi\rangle,
$$

con

$$
U^\dagger U = I.
$$

La unitaridad garantiza conservacion de la norma y, por tanto, coherencia con la interpretacion probabilistica.

## 2. Puertas basicas de un qubit

Algunas puertas fundamentales son:

### Puerta X

$$
X =
\begin{pmatrix}
0 & 1 \\
1 & 0
\end{pmatrix},
$$

que intercambia $|0\rangle$ y $|1\rangle$.

### Puerta Z

$$
Z =
\begin{pmatrix}
1 & 0 \\
0 & -1
\end{pmatrix},
$$

que deja $|0\rangle$ igual y cambia la fase de $|1\rangle$.

### Puerta H

La puerta de Hadamard cumple un papel central:

$$
H = \frac{1}{\sqrt{2}}
\begin{pmatrix}
1 & 1 \\
1 & -1
\end{pmatrix}.
$$

Convierte estados base en superposiciones:

$$
H|0\rangle = |+\rangle,
\qquad
H|1\rangle = |-\rangle.
$$

## 3. Puertas de fase y rotaciones

No todas las puertas relevantes intercambian amplitudes entre `0` y `1`. Algunas modifican fases relativas. Ejemplos tipicos son:

- la puerta `S`, que introduce una fase de $i$ sobre $|1\rangle$;
- la puerta `T`, que introduce una fase de $e^{i\pi/4}$;
- las rotaciones alrededor de ejes de la esfera de Bloch.

Estas puertas son esenciales porque la computacion cuantica no solo consiste en mover probabilidad entre resultados, sino en reorganizar la estructura de interferencia del estado.

## 4. Circuitos cuanticos

Un circuito cuantico organiza una secuencia de puertas y mediciones aplicadas sobre uno o varios qubits. En cierto sentido, cumple para la computacion cuantica el mismo papel que un circuito logico clasico para la computacion digital, aunque con una estructura matematica muy distinta.

En un circuito bien diseñado suele distinguirse:

- preparacion del estado inicial;
- bloque unitario de computacion;
- medicion final.

## 5. Sistemas de varios qubits

Cuando trabajamos con varios qubits, el espacio de estados se obtiene mediante producto tensorial. Dos qubits ya requieren un espacio de dimension cuatro:

$$
|00\rangle,\ |01\rangle,\ |10\rangle,\ |11\rangle.
$$

Esto significa que el numero de amplitudes crece exponencialmente con el numero de qubits. Esa es una de las razones por las que la simulacion clasica de sistemas cuanticos se vuelve rapidamente costosa.

## 6. Puertas de dos qubits

La puerta CNOT es una de las mas importantes. Actua sobre un qubit de control y uno objetivo:

- si el control esta en `0`, no hace nada;
- si el control esta en `1`, aplica una puerta `X` al objetivo.

La CNOT, combinada con puertas de un solo qubit, permite generar entrelazamiento.

Tambien conviene notar que las puertas de dos qubits no se interpretan simplemente como dos puertas individuales actuando en paralelo. Son operaciones genuinamente conjuntas sobre el sistema compuesto.

## 7. Universalidad

Una idea clave en computacion cuantica es que un conjunto pequeno de puertas puede ser universal, es decir, suficiente para aproximar cualquier operacion cuantica con precision arbitraria. Esta idea juega un papel analogo al de las bases universales en computacion clasica, pero con sutilezas nuevas asociadas a continuidad y unitarias.

## 8. Circuitos como lenguaje algoritmico

Los algoritmos cuanticos se expresan como circuitos porque:

- separan claramente preparacion, evolucion y medicion;
- permiten componer operaciones complejas a partir de puertas elementales;
- se implementan de forma natural en plataformas como Qiskit.

En otras palabras, un circuito es la interfaz entre la teoria matematica de la informacion cuantica y la ejecucion concreta en simulador o hardware.

## 9. Ideas clave

- Las puertas cuanticas son operadores unitarios.
- No todas las puertas modifican probabilidades directamente; algunas modifican fases.
- Los circuitos cuanticos componen secuencias de puertas y mediciones.
- El espacio de estados crece exponencialmente con el numero de qubits.
- Las puertas de varios qubits permiten construir correlaciones no clasicas.

## 10. Ejercicios sugeridos

1. Aplicar la puerta `H` al estado $|0\rangle$ y calcular el resultado.
2. Aplicar la puerta `X` a $|1\rangle$.
3. Explicar por que la CNOT puede generar entrelazamiento cuando el qubit de control esta en superposicion.
4. Explicar por que una puerta que solo cambia fase puede ser computacionalmente relevante.
