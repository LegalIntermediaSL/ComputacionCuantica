# Soluciones Avanzadas Seleccionadas

## 1. El Lazo Híbrido VQE
**Solución:** 
1. La QPU prepara un estado $|\psi(\theta)\rangle$ usando un circuito paramétrico llamado **Ansatz**.
2. La QPU mide el valor esperado $\langle H \rangle_\theta$ (energía).
3. Este valor se envía a una CPU clásica.
4. Un **optimizador clásico** (como COBYLA o SLSQP) analiza el resultado y propone nuevos parámetros $\theta'$ para minimizar la energía.
5. El proceso se repite hasta alcanzar el mínimo (estado fundamental).
El optimizador es vital porque la superficie de energía es compleja y el Ansatz debe ser lo suficientemente flexible para cubrir el espacio relevante sin sufrir de *Barren Plateaus* (gradientes nulos).

## 2. Mapeo QUBO a Ising
**Solución:**
Partimos de $x_i = \frac{1 - Z_i}{2}$. Sustituyendo en $f(x)$:
$f(Z) = 3(\frac{1-Z_1}{2}) + 2(\frac{1-Z_2}{2}) - 5(\frac{1-Z_1}{2})(\frac{1-Z_2}{2})$
$f(Z) = \frac{3}{2} - \frac{3}{2}Z_1 + 1 - Z_2 - \frac{5}{4}(1 - Z_1 - Z_2 + Z_1Z_2)$
Agrupando términos constantes y operadores:
$H = C + \alpha Z_1 + \beta Z_2 + \gamma Z_1Z_2$
Este Hamiltoniano de Ising puede ser implementado directamente en Qiskit usando `SparsePauliOp`.

## 3. Error de Trotter
**Solución:**
$e^{(A+B)\Delta t} = e^{A\Delta t}e^{B\Delta t} + O(\Delta t^2 [A,B])$.
Si $[A,B] \neq 0$, aplicar las puertas de forma secuencial introduce un error proporcional al conmutador y al cuadrado del paso de tiempo. Para evoluciones largas, necesitamos muchos pasos pequeños, lo que aumenta la **profundidad del circuito** y, por ende, la exposición al ruido (decoherencia).

## 4. Operadores de Kraus (Bit-Flip)
**Solución:**
$K_0 = \sqrt{1-p} \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}$ (No hay error)
$K_1 = \sqrt{p} \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ (Ocurre X)
Comprobación:
$K_0^\dagger K_0 + K_1^\dagger K_1 = (1-p)I + p X^\dagger X = (1-p)I + pI = I$.
La condición se cumple, garantizando que el canal preserva la traza (probabilidad total = 1).

## 5. Dinámica de Lindblad
**Solución:**
- **Termino Unitario:** $-\frac{i}{\hbar}[H, \rho]$. Representa la evolución coherente y reversible dictada por la energía interna del sistema.
- **Término Disipativo:** $\sum \gamma_k (L_k \rho L_k^\dagger - \dots)$. Representa la interacción irreversible con el entorno. El operador $L_k$ (operador de salto) modela procesos físicos específicos como el decaimiento espontáneo o la pérdida de fase.

## 6. La Realidad de BQP
**Solución:**
La ventaja cuántica no surge de la fuerza bruta, sino de la **interferencia**. Para resolver un problema NP-Completo como el del viajante, necesitaríamos un algoritmo que haga interferir destructivamente todas las rutas incorrectas y constructivamente la correcta. Aunque Grover ofrece una mejora cuadrática, no cambia la naturaleza exponencial del problema. Hasta hoy, no se conoce ninguna subrutina cuántica que mueva los problemas NP-Completos a la clase BQP.
