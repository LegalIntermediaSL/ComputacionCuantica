# Matrices de densidad y estados mixtos

## 1. Por qué no basta con estados puros

Hasta este punto en nuestro tutorial, la descripción de cualquier sistema cuántico se ha basado exclusivamente en vectores de estado, habitualmente denotados mediante la notación de Dirac como $|\psi\rangle$. A estos estados se les conoce como **estados puros**. 

Ese lenguaje resulta suficiente y extremadamente útil cuando trabajamos con circuitos ideales. Sin embargo, en el mundo real nos enfrentamos a situaciones mucho más sutiles que obligan a generalizar esta descripción:

- **Incertidumbre clásica:** Supongamos que un dispositivo prepara un qubit en el estado $|0\rangle$ con un 50% de probabilidad, y en el estado $|1\rangle$ con un 50% de probabilidad. No tenemos un vector puro para describir nuestro grado de conocimiento sobre el sistema.
- **Subsistemas en estados entrelazados:** Cuando observamos solo una parte de un sistema compuesto entrelazado, es físicamente imposible describir ese subsistema local como un vector puro aislado.
- **Ruido e interacciones:** La interacción incontrolada con el entorno (decoherencia) diluye la información cuántica, llevando al estado de superposición pura hacia una "mezcla estadística".

En todos estos casos, la herramienta matemática por excelencia para modelar el sistema recibe el nombre de **matriz de densidad**, y el objeto físico subyacente es un **estado mixto**.

## 2. Definición formal

Si sabemos con certeza absoluta que nuestro sistema se encuentra en un estado puro descrito por el vector normado $|\psi\rangle$, la matriz de densidad asociada, expresada mediante el producto exterior, es:

$$
\rho = |\psi\rangle\langle\psi|
$$

Esta matriz contiene exactamente la misma información que el vector de estado original. Por ejemplo, consideremos el estado puro $|0\rangle$. Su vector columna y su transpuesta conjugada son:

$$
|0\rangle = \begin{pmatrix} 1 \\ 0 \end{pmatrix}, \qquad \langle 0| = \begin{pmatrix} 1 & 0 \end{pmatrix}
$$

Su matriz de densidad correspondiente será:

$$
\rho_0 = |0\rangle\langle 0| = \begin{pmatrix} 1 \\ 0 \end{pmatrix} \begin{pmatrix} 1 & 0 \end{pmatrix} = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}
$$

### Valores esperados
En el formalismo de matrices de densidad, el valor esperado de un observable $A$ deja de calcularse como $\langle\psi|A|\psi\rangle$. En su lugar, utilizamos la función traza ($\text{Tr}$):

$$
\langle A \rangle = \text{Tr}(\rho A)
$$

## 3. Estados Mixtos: La diferencia entre Mezcla y Superposición

El verdadero poder de la matriz de densidad estalla cuando lidiamos con **estados mixtos**. Un estado mixto representa una *mezcla estadística o ensemble* de varios estados puros posibles. 

Si sabemos que nuestro sistema se preparó en el estado puro $|\psi_i\rangle$ con una probabilidad clásica $p_i$ (donde $\sum_i p_i = 1$), entonces el estado del sistema es una combinación convexa de las matrices de densidad individuales:

$$
\rho = \sum_i p_i |\psi_i\rangle\langle\psi_i|
$$

### El ejemplo crucial: Estado Mixto vs. Superposición al 50%

Es fundamental no confundir la combinación lineal de vectores (superposición) con la suma ponderada de matrices de densidad (mezcla estadística).
Supongamos que analizamos dos sistemas de un qubit muy distintos:

**1. Estado estructurado de superposición pura (estado $|+\rangle$):** 
Conocemos perfectamente que el estado obedece a una superposición exacta.
$$
|+\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)
$$
Su matriz de densidad resultará:
$$
\rho_+ = |+\rangle\langle+| = \frac{1}{2} \begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}
$$
Los términos **"fuera de la diagonal"** (llamados coherencias) no son cero, lo que implica que el sistema tiene capacidad para interferir consigo mismo cuánticamente. Este es el sello de un estado puro en superposición.

**2. Estado mixto máximo (mezcla caótica al 50%):** 
Una máquina falló antes de llegar a ti y escupió el estado $|0\rangle$ en la mitad exacta de tus intentos, y el estado $|1\rangle$ en la otra mitad de tus intentos. A priori, tu conocimiento del qubit es clásico y deficiente.

$$
\rho_{mixto} = \frac{1}{2} |0\rangle\langle 0| + \frac{1}{2} |1\rangle\langle 1| = \frac{1}{2} \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix} + \frac{1}{2} \begin{pmatrix} 0 & 0 \\ 0 & 1 \end{pmatrix} = \frac{1}{2} \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} = \frac{I}{2}
$$

A pesar de que ambos sistemas (el $|+\rangle$ y la matriz mixta $\frac{I}{2}$) ofrecen una probabilidad del 50/50 si medimos en la base computacional, el estado mixto es **físicamente y lógicamente distinto**. Este estado mixto presenta 0 en los términos de coherencia (los cruzados de la matriz diagonal), por lo tanto ha perdido absolutamente la capacidad de generar interferencia destructiva o constructiva.

Si aplicamos una puerta de Hadamard a ambos, el puro colapsa a $|0\rangle$, mientras que el mixto se queda exactamente en $\frac{I}{2}$.

## 4. Propiedades matemáticas para un objeto físico

No cualquier matriz aleatoria califica como "matriz de densidad". Para ser físicamente admisible y respetar las leyes de la cuántica, $\rho$ debe satisfacer tres axiomas inquebrantables:

1. **Hermiticidad ($\rho = \rho^\dagger$):** Garantiza que los autovalores algebraicos (que representan probabilidades matemáticas) sean siempre números reales.
2. **Traza igual a uno ($\text{Tr}(\rho) = 1$):** La suma total de todas las probabilidades del estado debe ser 1 al efectuar una medida proyectiva del universo de bases posibles.
3. **Positividad ($\rho \geq 0$):** Por ser semidefinida positiva, se evita que el sistema ofrezca "probabilidades negativas".

## 5. Pureza del estado

Podemos cuantificar médicamente "qué tan puro" es un estado. La **"pureza"** se define como la traza del cuadrado de la matriz de densidad ($\text{Tr}(\rho^2)$):
- Para un **estado puro**: $\text{Tr}(\rho^2) = 1$.
- Para un **estado mixto**: $ \frac{1}{d} \le \text{Tr}(\rho^2) < 1 $ donde $d$ refleja la dimensión del sistema ($d=2$ para un qubit). La cota inferior, $\frac{1}{2}$ en qubits, representa el estado máximamente mezclado sin ninguna información privilegiada (puro caos).

## 6. Ideas Clave

- Toda la mecánica cuántica puede reescribirse elegantemente usando $\rho$ en lugar de vectores.
- Un estado mixto representa una ignorancia real derivada del entorno o manipulación experimental, mientras que en una superposición pura disponemos de total predictibilidad de la dinámica, en tanto conozcamos la ecuación subyacente.
- El objeto central de estudio en los sistemas de decoherencia y algoritmos de corrección de errores es, en última instancia, el flujo hacia o la contención de entropías marcadas por la matriz de densidad.

## Navegacion

- Anterior: [Mitigacion de errores y fidelidad](../06_ruido_y_hardware/02_mitigacion_errores_y_fidelidad.md)
- Siguiente: [Traza parcial y entropia](02_traza_parcial_y_entropia.md)
