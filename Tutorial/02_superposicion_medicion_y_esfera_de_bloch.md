# Superposicion, medicion y esfera de Bloch

## 1. Superposicion

La superposicion es una consecuencia directa de la linealidad de la mecanica cuantica. Si $|0\rangle$ y $|1\rangle$ son estados permitidos, entonces tambien lo es cualquier combinacion lineal normalizada

$$
|\psi\rangle = \alpha |0\rangle + \beta |1\rangle.
$$

Esta propiedad hace posible construir estados que no tienen un analogo clasico directo.

## 2. Estados notables

Dos estados especialmente importantes son

$$
|+\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle),
\qquad
|-\rangle = \frac{1}{\sqrt{2}}(|0\rangle - |1\rangle).
$$

Estos estados aparecen una y otra vez en circuitos cuanticos porque permiten cambiar de base y exhiben con claridad el papel de la fase relativa.

## 3. Medicion

La medicion es el puente entre el estado cuantico y el resultado clasico observable. En la base computacional:

- medir $|0\rangle$ produce `0` con certeza;
- medir $|1\rangle$ produce `1` con certeza;
- medir $|+\rangle$ produce `0` o `1` con probabilidad $1/2$ cada uno.

La medicion no solo revela informacion: tambien modifica el sistema. Despues de medir, el estado colapsa al subespacio compatible con el resultado observado.

## 4. La esfera de Bloch

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

## 5. Limites de la intuicion geometrica

La esfera de Bloch funciona muy bien para un solo qubit puro, pero no debe confundirse con una imagen clasica del sistema. Tampoco generaliza de forma simple a muchos qubits, donde aparece entrelazamiento y el espacio de estados crece exponencialmente.

## 6. Interferencia

La superposicion por si sola no basta para obtener ventaja cuantica. Lo importante es que las amplitudes pueden combinarse constructiva o destructivamente. Ese fenomeno es la interferencia, y es la razon por la que la fase relativa importa tanto en algoritmos cuanticos.

## 7. Ideas clave

- Superposicion significa combinacion lineal coherente de estados.
- La medicion traduce amplitudes en probabilidades observables.
- La esfera de Bloch da una visualizacion util para estados puros de un qubit.
- La fase relativa controla la interferencia.

## 8. Ejercicios sugeridos

1. Comparar los estados $|+\rangle$ y $|-\rangle$ al medir en la base computacional.
2. Explicar por que ambos tienen las mismas probabilidades en esa base, pero no representan el mismo estado.
3. Describir geometricamente donde se encuentran $|0\rangle$, $|1\rangle$, $|+\rangle$ y $|-\rangle$ en la esfera de Bloch.
