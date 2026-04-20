# Entrelazamiento y estados de Bell

## 1. Que es el entrelazamiento

El entrelazamiento es una de las propiedades mas caracteristicas de la informacion cuantica. Un estado de varios qubits esta entrelazado cuando no puede escribirse como producto de estados individuales.

Por ejemplo, el estado

$$
|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)
$$

no puede factorizarse como

$$
|\psi\rangle_A \otimes |\chi\rangle_B.
$$

Esto significa que el sistema compuesto contiene correlaciones que no pueden atribuirse a propiedades locales independientes de cada subsistema.

## 2. Correlacion clasica frente a entrelazamiento

Es importante no confundir correlacion con entrelazamiento. Dos variables clasicas pueden estar muy correlacionadas sin que haya nada cuantico en juego. El entrelazamiento aparece cuando la descripcion completa del sistema no puede descomponerse en estados separados para cada parte.

La diferencia se vuelve especialmente visible al cambiar de base o al estudiar desigualdades tipo Bell. En ese sentido, el entrelazamiento no es solo "mucho acuerdo estadistico", sino una estructura fisica distinta.

## 3. Estados de Bell

Los cuatro estados de Bell forman una familia especialmente importante:

$$
|\Phi^\pm\rangle = \frac{1}{\sqrt{2}}(|00\rangle \pm |11\rangle),
$$

$$
|\Psi^\pm\rangle = \frac{1}{\sqrt{2}}(|01\rangle \pm |10\rangle).
$$

Son ejemplos canonicos de estados maximamente entrelazados de dos qubits.

## 4. Como generarlos

Un circuito muy simple para generar $|\Phi^+\rangle$ es:

1. preparar el estado inicial $|00\rangle$;
2. aplicar una puerta Hadamard al primer qubit;
3. aplicar una puerta CNOT con el primer qubit como control.

Despues de `H`, el estado es

$$
\frac{1}{\sqrt{2}}(|00\rangle + |10\rangle).
$$

Despues de `CNOT`, obtenemos

$$
\frac{1}{\sqrt{2}}(|00\rangle + |11\rangle).
$$

Este ejemplo es especialmente valioso porque muestra que el entrelazamiento no es una propiedad exotica reservada a sistemas muy complicados: aparece ya en un circuito elemental.

## 5. Correlaciones y medicion

Si medimos ambos qubits de $|\Phi^+\rangle$ en la base computacional, los resultados posibles son:

- `00` con probabilidad $1/2$;
- `11` con probabilidad $1/2$.

Nunca aparecen `01` ni `10`. Esto muestra correlacion perfecta, pero el entrelazamiento es mas fuerte que una correlacion clasica ordinaria: tambien afecta el comportamiento al medir en otras bases.

## 6. Estados reducidos

Un rasgo interesante es que el estado global puede ser puro mientras que cada subsistema individual se describe por un estado mixto. En los estados de Bell, si observamos solo uno de los qubits e ignoramos el otro, no encontramos un estado puro bien definido para la parte individual.

Esta es una buena primera aproximacion a ideas mas generales de informacion cuantica, como matrices de densidad reducidas y entropia de entrelazamiento.

## 7. Por que el entrelazamiento importa

El entrelazamiento es recurso central para:

- teleportacion cuantica;
- superdense coding;
- criptografia cuantica;
- algoritmos y protocolos distribuidos;
- ventajas en tareas de informacion cuantica.

Sin entrelazamiento, gran parte del interes de la computacion cuantica quedaria drasticamente reducido.

## 8. Ideas clave

- Un estado entrelazado no se factoriza en estados individuales.
- Los estados de Bell son ejemplos maximamente entrelazados de dos qubits.
- Un circuito simple con `H` y `CNOT` basta para generarlos.
- El entrelazamiento produce correlaciones no clasicas.
- El estado global puede ser puro mientras las partes individuales no lo son.

## 9. Ejercicios sugeridos

1. Construir algebraicamente el estado de Bell a partir de `H` y `CNOT`.
2. Explicar por que $|\Phi^+\rangle$ no puede escribirse como producto tensorial.
3. Describir que resultados se esperan al medir el estado $|\Psi^+\rangle$ en la base computacional.
4. Explicar por que ver correlacion perfecta no basta por si solo para demostrar entrelazamiento.

## Navegacion

- Anterior: [Puertas cuanticas y circuitos](03_puertas_cuanticas_y_circuitos.md)
- Siguiente: [Qiskit: primeros pasos y flujo de trabajo practico](../02_qiskit_basico/05_qiskit_primeros_pasos.md)
