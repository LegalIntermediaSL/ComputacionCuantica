# Qubits y estados cuanticos

## 1. Del bit clasico al qubit

La computacion clasica trabaja con bits que pueden tomar uno de dos valores posibles: `0` o `1`. La computacion cuantica parte de una idea parecida, pero la enriquece profundamente. El objeto basico no es el bit, sino el qubit.

Un qubit es un sistema cuantico de dos niveles. Sus estados base se suelen denotar por

$$
|0\rangle
\quad \text{y} \quad
|1\rangle.
$$

La diferencia central con el bit clasico es que un qubit puede encontrarse en una combinacion lineal de ambos estados.

## 2. Espacio de estados

El estado general de un qubit se escribe como

$$
|\psi\rangle = \alpha |0\rangle + \beta |1\rangle,
$$

donde $\alpha$ y $\beta$ son numeros complejos que satisfacen la condicion de normalizacion

$$
|\alpha|^2 + |\beta|^2 = 1.
$$

Esta expresion resume buena parte del salto conceptual de la computacion cuantica. La informacion cuantica no se almacena como una etiqueta fija, sino como una amplitud distribuida entre varios resultados posibles.

## 3. Interpretacion probabilistica

Cuando medimos el qubit en la base computacional, obtenemos:

- el resultado `0` con probabilidad $|\alpha|^2$;
- el resultado `1` con probabilidad $|\beta|^2$.

Antes de la medicion, el sistema no se interpreta como "a veces cero y a veces uno" en sentido clasico. Lo que existe es un estado cuantico que contiene amplitudes, fases y coherencia.

## 4. Representacion vectorial

En notacion matricial, los estados base pueden escribirse como

$$
|0\rangle =
\begin{pmatrix}
1 \\
0
\end{pmatrix},
\qquad
|1\rangle =
\begin{pmatrix}
0 \\
1
\end{pmatrix}.
$$

Por tanto,

$$
|\psi\rangle =
\begin{pmatrix}
\alpha \\
\beta
\end{pmatrix}.
$$

Esta representacion permite describir operaciones cuanticas mediante matrices unitarias, una idea que sera central cuando introduzcamos puertas cuanticas.

## 5. Fase global y fase relativa

No todas las fases tienen contenido fisico observable. Si multiplicamos todo el estado por un factor de fase global $e^{i\phi}$,

$$
|\psi\rangle \to e^{i\phi} |\psi\rangle,
$$

las probabilidades de medicion no cambian. En cambio, la fase relativa entre $\alpha$ y $\beta$ si tiene efectos fisicos y puede influir en interferencia y evolucion unitaria.

## 6. Por que esto importa en computacion cuantica

Los algoritmos cuanticos extraen potencia no del hecho trivial de tener dos niveles, sino de tres propiedades:

- superposicion;
- interferencia;
- entrelazamiento cuando hay varios qubits.

Por eso entender bien la estructura del estado de un solo qubit es el primer paso obligatorio antes de hablar de circuitos, puertas o algoritmos.

## 7. Ideas clave

- Un qubit es un sistema cuantico de dos niveles.
- Su estado general es una combinacion lineal de $|0\rangle$ y $|1\rangle$.
- Las amplitudes son complejas y deben normalizarse.
- La medicion traduce amplitudes en probabilidades.

## 8. Ejercicios sugeridos

1. Verificar que el estado $\frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$ esta normalizado.
2. Calcular las probabilidades de medicion del estado $\sqrt{3}/2 \, |0\rangle + 1/2 \, |1\rangle$.
3. Explicar con tus palabras la diferencia entre fase global y fase relativa.
