# Algebra lineal minima para computacion cuantica

## 1. Por que hace falta algebra lineal

La computacion cuantica se formula de manera natural en lenguaje de espacios vectoriales complejos, matrices y productos tensoriales. Por eso incluso un tutorial muy aplicado necesita una capa minima de algebra lineal.

No se trata de convertir el proyecto en un curso abstracto de matematicas. Se trata de introducir exactamente las herramientas que vuelven inteligibles los circuitos cuanticos.

## 2. Vectores y estados

Un estado cuantico puro se representa como un vector normalizado en un espacio de Hilbert. Para un qubit, usamos vectores complejos de dos componentes:

$$
|\psi\rangle =
\begin{pmatrix}
\alpha \\
\beta
\end{pmatrix}.
$$

La normalizacion exige

$$
\langle \psi | \psi \rangle = 1.
$$

## 3. Producto interno

El producto interno entre dos estados $|\phi\rangle$ y $|\psi\rangle$ se denota por

$$
\langle \phi | \psi \rangle.
$$

Este objeto permite:

- calcular normas;
- medir solapamiento entre estados;
- construir probabilidades de transicion.

## 4. Matrices y operadores

Las puertas cuanticas se describen mediante matrices unitarias. Por ejemplo,

$$
X =
\begin{pmatrix}
0 & 1 \\
1 & 0
\end{pmatrix}
$$

y

$$
H = \frac{1}{\sqrt{2}}
\begin{pmatrix}
1 & 1 \\
1 & -1
\end{pmatrix}.
$$

Aplicar una puerta es simplemente multiplicar la matriz por el vector de estado.

## 5. Producto tensorial

Cuando combinamos sistemas cuanticos, no sumamos dimensiones: tomamos productos tensoriales. Dos qubits forman un espacio de dimension cuatro:

$$
\mathbb C^2 \otimes \mathbb C^2 \cong \mathbb C^4.
$$

Esto explica por que el numero de amplitudes crece tan deprisa al aumentar el numero de qubits.

## 6. Autovalores y observables

La medicion de una magnitud se formula mediante operadores hermiticos. Sus autovalores representan posibles resultados de la medicion y sus autovectores determinan las direcciones privilegiadas del espacio de estados.

En un tutorial introductorio no hace falta entrar enseguida en toda la teoria espectral, pero si conviene entender que medir no es una operacion arbitraria: esta asociada a una estructura algebraica concreta.

## 7. Ideas clave

- Los estados son vectores complejos normalizados.
- Las puertas son matrices unitarias.
- Los sistemas compuestos se describen con productos tensoriales.
- La algebra lineal no es un añadido externo: es el lenguaje natural de la computacion cuantica.

## Navegacion

- Anterior: [Qiskit: primeros pasos y flujo de trabajo practico](05_qiskit_primeros_pasos.md)
- Siguiente: [Algoritmos cuanticos introductorios](07_algoritmos_cuanticos_introductorios.md)
