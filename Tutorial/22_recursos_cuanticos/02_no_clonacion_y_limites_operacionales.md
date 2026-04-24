# No-clonación y límites operacionales cuánticos

## 1. El teorema de no-clonación

### 1.1 Enunciado

**Teorema (Wootters & Zurek, Dieks, 1982):** No existe ninguna operación cuántica unitaria $U$ que realice

$$
U(|\psi\rangle \otimes |0\rangle) = |\psi\rangle \otimes |\psi\rangle
$$

para todo estado cuántico $|\psi\rangle$.

### 1.2 Demostración por linealidad

La prueba es directa. Supongamos que $U$ clona los estados de la base computacional:

$$
U(|0\rangle|0\rangle) = |0\rangle|0\rangle, \quad U(|1\rangle|0\rangle) = |1\rangle|1\rangle
$$

Por linealidad de $U$, para el estado $|+\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$:

$$
U(|+\rangle|0\rangle) = \frac{1}{\sqrt{2}}(|0\rangle|0\rangle + |1\rangle|1\rangle) = |\Phi^+\rangle
$$

Pero clonar $|+\rangle$ requeriría:

$$
U(|+\rangle|0\rangle) = |+\rangle|+\rangle = \frac{1}{2}(|00\rangle + |01\rangle + |10\rangle + |11\rangle)
$$

Estos dos resultados son diferentes, contradicción. $\square$

### 1.3 ¿Por qué importa la linealidad?

El argumento depende crucialmente de que las operaciones cuánticas sean lineales. La linealidad de la mecánica cuántica prohíbe la clonación perfecta, pero no la **clonación aproximada** (la fidelidad máxima de clonación universal de un qubit es $5/6 \approx 0.833$, alcanzada por la máquina de Bužek-Hillery).

## 2. Consecuencias del teorema de no-clonación

### 2.1 Seguridad de QKD

El protocolo BB84 basa su seguridad en el teorema de no-clonación: un espía (Eva) no puede copiar los fotones que Alice envía a Bob sin introducir errores detectables. Si Eva intenta medir y reenviar, el teorema de no-clonación garantiza que su copia es imperfecta, y la perturbación que introduce es detectable.

Formalmente, la tasa de error en la clave detectará la presencia de Eva si su fidelidad de clonación es inferior a 1.

### 2.2 No-broadcasting

El teorema de no-clonación se extiende a estados mixtos como el **teorema de no-broadcasting**: no existe un canal cuántico $\mathcal{E}$ tal que

$$
\text{Tr}_B[\mathcal{E}(\rho)] = \rho \quad \text{y} \quad \text{Tr}_A[\mathcal{E}(\rho)] = \rho
$$

para todos los estados $\rho$. Esto es, no podemos "difundir" un estado cuántico desconocido manteniendo copias perfectas en dos sistemas.

### 2.3 Teleportación: transmitir sin clonar

La teleportación cuántica evita el no-clonación de la siguiente manera: Alice destruye su qubit original al medirlo en la base de Bell. No hay dos copias en ningún momento; el estado es transportado, no copiado.

## 3. Monogamia del entrelazamiento

### 3.1 El principio

Si dos qubits $A$ y $B$ están máximamente entrelazados (un par de Bell), entonces $A$ no puede estar entrelazado en absoluto con ningún tercer qubit $C$. Este es el principio de **monogamia del entrelazamiento**.

La desigualdad de Coffman-Kundu-Wootters (CKW) lo cuantifica para tres qubits:

$$
\tau_{A|BC} \geq \tau_{AB} + \tau_{AC}
$$

donde $\tau_{AB} = C_{AB}^2$ es el **tangle** (cuadrado de la concurrencia), una medida de entrelazamiento bipartito.

### 3.2 Implicaciones para la seguridad cuántica

La monogamia del entrelazamiento tiene consecuencias directas para los protocolos de clave cuántica:
- Si Alice y Bob comparten un estado de Bell puro $|\Phi^+\rangle_{AB}$, ningún espía $E$ puede tener correlaciones cuánticas con la clave, porque todo el entrelazamiento de $A$ está "comprometido" con $B$.
- En el protocolo E91 (Ekert), la monogamia garantiza que la violación de la desigualdad de Bell certifica la ausencia de espías.

### 3.3 Estado de tres qubits: W vs. GHZ

Existen dos clases genuinamente distintas de entrelazamiento tripartito bajo LOCC:

**Estado GHZ:** $|\text{GHZ}\rangle = \frac{1}{\sqrt{2}}(|000\rangle + |111\rangle)$. Los tres qubits están entrelazados de forma frágil: trazar cualquier qubit destruye todo el entrelazamiento del par restante.

**Estado W:** $|W\rangle = \frac{1}{\sqrt{3}}(|001\rangle + |010\rangle + |100\rangle)$. El entrelazamiento es más robusto: trazar un qubit deja un par entrelazado.

Ningún estado GHZ puede convertirse en un estado W por LOCC y viceversa: son recursos genuinamente diferentes.

## 4. El principio de Landauer

### 4.1 Enunciado

El principio de Landauer (1961) establece que **borrar un bit de información** en un sistema a temperatura $T$ disipa al menos

$$
W_\text{min} = k_B T \ln 2 \approx 2.85 \times 10^{-21}\, \text{J a } T = 300\,\text{K}
$$

de energía en el entorno.

### 4.2 Versión cuántica

Para un qubit, el principio de Landauer cuántico establece que resetear el estado $\rho$ al estado $|0\rangle\langle 0|$ disipa al menos

$$
W \geq k_B T \ln 2 \cdot S(\rho) / \ln 2 = k_B T \cdot S(\rho)
$$

donde $S(\rho) = -\text{Tr}(\rho \log \rho)$ es la entropía de von Neumann (en nats). El borrado de un estado puro ($S = 0$) puede hacerse sin disipación; el borrado de un estado mixto de máxima entropía ($S = \ln 2$) disipa $k_B T \ln 2$.

### 4.3 Implicaciones para los procesadores cuánticos

En un procesador cuántico real, el reseteo de qubits tiene dos componentes:
1. **Relajación pasiva** hacia $|0\rangle$ por el baño térmico (tiempo $T_1$): disipa $\hbar\omega_q$ por qubit.
2. **Reseteo activo** mediante medición y retroacción: más rápido, pero también disipativo.

Esto significa que computar con muchos ciclos de corrección de errores (que requieren reseteos frecuentes de los qubits ancilla) tiene un coste energético mínimo irreducible fijado por la termodinámica.

### 4.4 Computación reversible

La forma de evadir el principio de Landauer es usar **computación reversible**: operaciones unitarias que no destruyen información. Los circuitos cuánticos unitarios son inherentemente reversibles, pero la medición (que proyecta el estado) no lo es.

El modelo de computación cuántica tolerante a fallos usa ancillas que se miden y resetean repetidamente: esto es inevitablemente disipativo y establece un piso energético para la computación cuántica a gran escala.

## 5. No-deletion y complementariedad

### 5.1 Teorema de no-borrado

Análogo al no-clonación: no existe operación unitaria que borre un qubit arbitrario dejando el otro intacto:

$$
U(|\psi\rangle \otimes |\psi\rangle) = |\psi\rangle \otimes |A_\psi\rangle
$$

no puede valer para todos los $|\psi\rangle$ con $|A_\psi\rangle$ independiente de $\psi$. La prueba es idéntica al no-clonación por linealidad.

### 5.2 Principio de complementariedad

El principio de complementariedad (Bohr) establece que no se puede obtener simultáneamente información completa sobre observables incompatibles (posición y momento, o las dos componentes de espín). En el formalismo moderno, esto es la consecuencia de la no-conmutatividad y se cuantifica por la relación de incertidumbre:

$$
\text{Var}(A) \cdot \text{Var}(B) \geq \frac{1}{4}|\langle[A, B]\rangle|^2
$$

### 5.3 Holevo bound: límite de información accesible

Aunque un qubit puede codificar un estado con infinitos parámetros continuos, el **límite de Holevo** establece que de un qubit solo se puede extraer al más 1 bit de información clásica mediante cualquier medición (POVM):

$$
\chi \leq S(\rho) - \sum_i p_i S(\rho_i) \leq \log d
$$

Esto significa que no hay manera de "comprimir" más información clásica en un qubit de lo que permite la entropía de von Neumann.

## 6. Ideas clave

- El teorema de no-clonación es consecuencia directa de la linealidad de la mecánica cuántica: el estado cuántico no puede copiarse perfectamente.
- La seguridad de QKD depende del no-clonación: cualquier espionaje introduce errores detectables.
- La monogamia del entrelazamiento prohíbe que un qubit entrelazado con $B$ esté también entrelazado con $C$; esto fundamente la seguridad de los protocolos basados en pares de Bell.
- El principio de Landauer establece un piso energético para el borrado de información clásica y cuántica, directamente relevante para los costes energéticos de la corrección de errores.
- El límite de Holevo acota a 1 bit la información clásica extraíble de un qubit, independientemente de cuántos parámetros continuos describan su estado.

## 7. Ejercicios sugeridos

1. Demostrar que la clonación perfecta viola la conservación de la energía si el Hamiltoniano del clonicador es independiente del estado de entrada.
2. Calcular la energía mínima disipada para resetear $10^6$ qubits ancilla por ciclo de corrección de errores a $T = 20\,\text{mK}$ (temperatura de operación de los transmones).
3. Verificar la desigualdad CKW para el estado $|W\rangle$ calculando la concurrencia de cada par de qubits.
4. Explicar por qué la teleportación cuántica no viola el teorema de no-clonación aunque "transmite" el estado cuántico de Alice a Bob.

## Navegacion

- Anterior: [Coherencia, entrelazamiento y utilidad](01_coherencia_entrelazamiento_y_utilidad.md)
- Siguiente: [Transmones y circuitos superconductores](../23_hardware_fisico_y_arquitecturas/01_transmones_y_circuitos_superconductores.md)
