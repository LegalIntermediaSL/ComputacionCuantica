# Superposicion, medicion y esfera de Bloch

## 1. Superposicion

La superposicion es una consecuencia directa de la linealidad de la mecanica cuantica. Si $|0\rangle$ y $|1\rangle$ son estados permitidos, entonces tambien lo es cualquier combinacion lineal normalizada

$$
|\psi\rangle = \alpha |0\rangle + \beta |1\rangle.
$$

Esta propiedad hace posible construir estados que no tienen un analogo clasico directo. La computacion cuantica se apoya precisamente en poder preparar, transformar y explotar estas combinaciones de forma controlada.

## 2. Estados notables

Dos estados especialmente importantes son

$$
|+\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle),
\qquad
|-\rangle = \frac{1}{\sqrt{2}}(|0\rangle - |1\rangle).
$$

Estos estados aparecen una y otra vez en circuitos cuanticos porque permiten cambiar de base y exhiben con claridad el papel de la fase relativa.

Tambien son utililes para entender que dos estados con las mismas probabilidades de medicion en una base concreta no tienen por que ser fisicamente equivalentes. $|+\rangle$ y $|-\rangle$ dan ambos 50 por ciento de `0` y 50 por ciento de `1` en la base computacional, pero responden de manera distinta a otras operaciones.

## 3. Medicion

La medicion es el puente entre el estado cuantico y el resultado clasico observable. En la base computacional:

- medir $|0\rangle$ produce `0` con certeza;
- medir $|1\rangle$ produce `1` con certeza;
- medir $|+\rangle$ produce `0` o `1` con probabilidad $1/2$ cada uno.

La medicion no solo revela informacion: tambien modifica el sistema. Despues de medir, el estado colapsa al subespacio compatible con el resultado observado.

Este colapso no debe pensarse como una "destruccion misteriosa" del estado, sino como una regla operativa que conecta el formalismo con la estadistica experimental.

## 4. Cambio de base

Una medicion no tiene significado completo si no se especifica la base en que se realiza. Medir en la base computacional no es lo mismo que medir en la base $\{|+\rangle, |-\rangle\}$. Esta observacion es crucial porque muchos algoritmos cuanticos alternan entre distintas bases para hacer visible la estructura de interferencia del estado.

La puerta Hadamard permite precisamente conectar ambas descripciones:

$$
H|0\rangle = |+\rangle,
\qquad
H|1\rangle = |-\rangle.
$$

## 5. La esfera de Bloch

Todo estado puro de un qubit puede escribirse, salvo una fase global, como

$$
|\psi\rangle =
\cos\left(\frac{\theta}{2}\right)|0\rangle
+ e^{i\phi}\sin\left(\frac{\theta}{2}\right)|1\rangle.
$$

Los parametros $\theta$ y $\phi$ permiten representar el estado como un punto en la esfera de Bloch. Esta imagen geometrica es muy util porque:

- ayuda a visualizar rotaciones unitarias;
- distingue fase global de fase relativa;
- permite interpretar puertas cuanticas como giros del vector de estado.

## 6. Puntos importantes en la esfera

Algunos estados notables ocupan posiciones sencillas:

- $|0\rangle$ en el polo norte;
- $|1\rangle$ en el polo sur;
- $|+\rangle$ sobre el eje $x$ positivo;
- $|-\rangle$ sobre el eje $x$ negativo.

Esta imagen vuelve muy intuitivo el efecto de ciertas puertas cuanticas, en particular de rotaciones alrededor de ejes concretos.

## 7. Limites de la intuicion geometrica

La esfera de Bloch funciona muy bien para un solo qubit puro, pero no debe confundirse con una imagen clasica del sistema. Tampoco generaliza de forma simple a muchos qubits, donde aparece entrelazamiento y el espacio de estados crece exponencialmente.

Ademas, los estados mixtos no ocupan la superficie de la esfera, sino su interior. Aunque este tutorial esta centrado por ahora en estados puros, conviene recordar que la representacion geometrica tiene limites.

## 8. Interferencia

La superposicion por si sola no basta para obtener ventaja cuantica. Lo importante es que las amplitudes pueden combinarse constructiva o destructivamente. Ese fenomeno es la interferencia, y es la razon por la que la fase relativa importa tanto en algoritmos cuanticos.

En cierto sentido, programar un algoritmo cuantico consiste en diseñar un circuito que redistribuya amplitudes para reforzar respuestas correctas y cancelar parcialmente respuestas incorrectas.

## 9. Ideas clave

- Superposicion significa combinacion lineal coherente de estados.
- La medicion traduce amplitudes en probabilidades observables.
- La base elegida importa tanto como el estado.
- La esfera de Bloch da una visualizacion util para estados puros de un qubit.
- La fase relativa controla la interferencia.

## 10. Ejercicios sugeridos

1. Comparar los estados $|+\rangle$ y $|-\rangle$ al medir en la base computacional.
2. Explicar por que ambos tienen las mismas probabilidades en esa base, pero no representan el mismo estado.
3. Describir geometricamente donde se encuentran $|0\rangle$, $|1\rangle$, $|+\rangle$ y $|-\rangle$ en la esfera de Bloch.
4. Explicar por que cambiar de base puede convertir una diferencia de fase en una diferencia observable.
