# Ejercicios Avanzados

1. **Derivación del Lazo VQE:** Explica paso a paso el flujo de información entre la QPU y la CPU en un algoritmo variacional. ¿Por qué es necesario un optimizador clásico y qué función cumple el "Ansatz"?
2. **Mapeo QUBO:** Toma el siguiente problema de optimización simple: minimizar $f(x_1, x_2) = 3x_1 + 2x_2 - 5x_1x_2$ (donde $x_i \in \{0,1\}$). Conviértelo a un Hamiltoniano de Ising sustituyendo $x_i = \frac{1 - Z_i}{2}$.
3. **Expansión de Trotter:** Para dos observables que no conmutan, $A$ y $B$, desarrolla la aproximación de primer orden de $e^{(A+B)\Delta t}$ y explica por qué el error de conmutación limita la profundidad del circuito.
4. **Matrices de Kraus:** Dado el canal de *Bit-Flip* con probabilidad $p$, escribe sus operadores de Kraus $K_0$ y $K_1$ y verifica la condición de completitud $\sum K_i^\dagger K_i = I$.
5. **Ecuación de Lindblad:** Discute conceptualmente la diferencia entre el término unitario (Hamiltoniano) y el término disipativo (Lindbladiano). ¿Qué representa físicamente el operador de salto $L_k$?
6. **Complejidad BQP:** Explica detalladamente por qué la capacidad de una computadora cuántica para evaluar $2^n$ estados en superposición no implica automáticamente que pueda resolver problemas NP-Completos de forma instantánea.
7. **Tomografía de Estados (QST):** Para un sistema de 3 qubits, ¿cuántos circuitos de medición independientes y cuántos parámetros de la matriz de densidad $\rho$ necesitamos determinar en total?
8. **Surface Codes:** Describe el ciclo de detección de un error de tipo $X$ en un código de superficie. ¿Cómo se usan los qubits ancilares para extraer el "síndrome de error" sin colapsar el estado de los qubits de datos?
