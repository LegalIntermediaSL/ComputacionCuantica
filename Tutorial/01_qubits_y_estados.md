# Qubits y estados cuanticos

## 1. Del bit clasico al qubit

La computacion clasica trabaja con bits que pueden tomar uno de dos valores posibles: `0` o `1`. La computacion cuantica parte de una idea parecida, pero la enriquece profundamente. El objeto basico no es el bit, sino el qubit.

Un qubit es un sistema cuantico de dos niveles. Sus estados base se suelen denotar por

$$
|0\rangle
\quad \text{y} \quad
|1\rangle.
$$

La diferencia central con el bit clasico es que un qubit puede encontrarse en una combinacion lineal de ambos estados. Esa sola afirmacion ya obliga a abandonar la intuicion clasica segun la cual el sistema "esta en un estado definido aunque no lo sepamos". En mecanica cuantica, el estado es la descripcion mas completa disponible del sistema.

## 2. Espacio de estados

El estado general de un qubit se escribe como

$$
|\psi\rangle = \alpha |0\rangle + \beta |1\rangle,
$$

donde $\alpha$ y $\beta$ son numeros complejos que satisfacen la condicion de normalizacion

$$
|\alpha|^2 + |\beta|^2 = 1.
$$

Esta expresion resume buena parte del salto conceptual de la computacion cuantica. La informacion cuantica no se almacena como una etiqueta fija, sino como una amplitud distribuida entre varios resultados posibles. La presencia de coeficientes complejos no es una ornamentacion matematica: permite interferencia y fases relativas, dos ingredientes esenciales de la computacion cuantica.

## 3. Interpretacion probabilistica

Cuando medimos el qubit en la base computacional, obtenemos:

- el resultado `0` con probabilidad $|\alpha|^2$;
- el resultado `1` con probabilidad $|\beta|^2$.

Antes de la medicion, el sistema no se interpreta como "a veces cero y a veces uno" en sentido clasico. Lo que existe es un estado cuantico que contiene amplitudes, fases y coherencia. El cuadrado del modulo convierte las amplitudes en probabilidades observables.

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

Esta distincion es una buena primera leccion metodologica: en computacion cuantica hay estructuras matematicas que parecen similares, pero no todas tienen el mismo significado fisico.

## 6. Normalizacion y estados fisicos

No cualquier par de numeros complejos define un estado fisico. La condicion de normalizacion garantiza que la suma total de probabilidades sea uno. Por ejemplo,

$$
\frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)
$$

es un estado permitido, mientras que

$$
|0\rangle + |1\rangle
$$

no esta normalizado todavia y debe reescalarse.

Esta observacion puede parecer menor, pero es importante porque en calculo simbolico y en implementacion computacional conviene distinguir entre estados formales y estados fisicamente validos.

## 7. El qubit como recurso de informacion

Un error frecuente es pensar que un qubit "almacena mas informacion" que un bit simplemente porque tiene infinitas amplitudes posibles. El asunto es mas sutil. La medicion de un solo qubit sigue devolviendo solo un resultado clasico elemental en cada experimento. La ventaja cuantica no aparece por una lectura trivialmente mas rica, sino por la posibilidad de manipular coherentemente superposiciones y correlaciones entre muchos qubits antes de medir.

## 8. Por que esto importa en computacion cuantica

Los algoritmos cuanticos extraen potencia no del hecho trivial de tener dos niveles, sino de tres propiedades:

- superposicion;
- interferencia;
- entrelazamiento cuando hay varios qubits.

Por eso entender bien la estructura del estado de un solo qubit es el primer paso obligatorio antes de hablar de circuitos, puertas o algoritmos.

## 9. Ideas clave

- Un qubit es un sistema cuantico de dos niveles.
- Su estado general es una combinacion lineal de $|0\rangle$ y $|1\rangle$.
- Las amplitudes son complejas y deben normalizarse.
- La medicion traduce amplitudes en probabilidades.
- La fase relativa tiene efectos fisicos; la fase global no.

## 10. Ejercicios sugeridos

1. Verificar que el estado $\frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$ esta normalizado.
2. Calcular las probabilidades de medicion del estado $\sqrt{3}/2 \, |0\rangle + 1/2 \, |1\rangle$.
3. Explicar con tus palabras la diferencia entre fase global y fase relativa.
4. Dar un ejemplo de vector de dos componentes que no represente todavia un estado fisico y normalizarlo.
