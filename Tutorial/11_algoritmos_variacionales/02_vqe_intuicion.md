# VQE: Intuición (Variational Quantum Eigensolver)

## 1. El gran objetivo físico de VQE

Uno de los postulados fundamentales del algebra lineal dice que la energía más baja posible de un sistema cuántico subyacente escondida de manera hermética reside en el autovector menor de su **Matriz Mágica de Fenómenos: El Hamiltoniano ($H$)**.
Si tomásemos una molécula real inmensa (como Penicilina), y calculásemos su energía base inferior $E_0$, ganaríamos una comprensión termodinámica fundamental para poder crear su medicina análoga. 

Calcular autovalores de grandes matrices Hamiltonianas en computadoras clásicas escala trágicamente de manera exponencial y agota la RAM mundial pasados los $\sim 50$ átomos orgánicos.
El **VQE (Variational Quantum Eigensolver)** nace con una promesa: dejar que la naturaleza cuántica mapee las dimensiones combinatorias inmensas, mientras intentamos "escanear" el estado molecular base mediante circuitos cuánticos superficiales parametrizados dirigidos por un control de CPU clásica.

## 2. El principio variacional

El VQE se escuda religiosamente en el famoso "Principio Variacional de Rayleigh-Ritz". Este principio matemático establece que, si coges un estado arbitrario "adivinado" $|\psi(\vec{\theta})\rangle$, y calculas cual sería su valor esperado medido bajo el tensor del Hamiltoniano, el resultado **NUNCA** podría ser menor que la auténtica energía de estado base absoluta del universo $E_0$.

$$ \langle \psi(\vec{\theta}) | H | \psi(\vec{\theta}) \rangle \ge E_0 $$

Se trata por tanto, de un problema empírico de minimización por cotas superior al mínimo. Basta con adivinar configuraciones usando iteraciones hasta empujar la energía lo más abajo posible estrujando el optimizador.

## 3. Elementos constituyentes del VQE

Si ejecutas un VQE hoy de cara a la física química molecular, ensamblarás tres piezas inquebrantables:
1. **El Hamiltoniano ($H$)**: El mapeo del problema estático objetivo, habitualmente definido abstrayendo electrones fermiónicos orbitales (Ej. Jordan-Wigner Encoding) e inyectándolo hacia una variable autoadjunta de `SparsePauliOp`.
2. **El Ansatz paramétrico $\vec{\theta}$**: El circuito cuántico "moldeable" superficial que giramos y deformamos. (Se suele usar una plantilla HEA como `EfficientSU2` para entrelazar con baja latencia profunda del chip).
3. **Optimizador Clásico de Retroalimentación**: La inteligencia matemática iterativa de SciPy como el minimizador `COBYLA` o el algoritmo genérico asincrónico resiliente al ruido estadístico estocástico cuántico de lectura (`SPSA`).

## 4. Retos reales del algoritmo VQE

- **La maldición de Barren Plateaus**: Al programar un "Ansatz" súper expresivo que abarque todas las posibilidades angulares de un hipercubo denso (demasiado caos angular de Hilbert), la métrica devuelve un gradiente de llanuras planas indescifrables perdiendo inercia matemática la computadora clásica, perdiéndose e invalidando el descenso hacia localizaciones estables.

## Navegacion

- Anterior: [Circuitos parametrizados y optimizacion](01_circuitos_parametrizados_y_optimizacion.md)
- Siguiente: [QAOA: intuicion](03_qaoa_intuicion.md)
