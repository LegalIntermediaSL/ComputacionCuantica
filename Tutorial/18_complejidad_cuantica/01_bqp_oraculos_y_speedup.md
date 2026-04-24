# BQP, oráculos y aceleración cuántica

## 1. Las clases de complejidad relevantes

La teoría de la complejidad computacional clasifica los problemas según los recursos necesarios para resolverlos. Para entender lo que la computación cuántica puede y no puede hacer, es indispensable conocer las clases de complejidad centrales.

**P:** problemas solucionables en tiempo polinomial por una máquina de Turing determinista. Ejemplos: ordenación, búsqueda en una lista ordenada, factorización de números pequeños, cálculo del MCD.

**NP:** problemas cuyas soluciones son verificables en tiempo polinomial. No se sabe si $P = NP$. Ejemplos: satisfacibilidad booleana (SAT), problema del viajante (TSP), coloración de grafos.

**BPP** (Bounded-error Probabilistic Polynomial time): problemas solucionables por un algoritmo probabilista en tiempo polinomial con probabilidad de éxito $\geq 2/3$. La clase que "hace" la computación clásica probabilista.

**BQP** (Bounded-error Quantum Polynomial time): la versión cuántica de BPP. Un problema está en BQP si un circuito cuántico de tamaño polinomial lo resuelve con probabilidad de éxito $\geq 2/3$.

Las relaciones conocidas son:
$$
P \subseteq BPP \subseteq BQP \subseteq PSPACE
$$

Se sabe que $BQP \not\subseteq P$ (bajo oráculos), lo que garantiza que existen problemas que la computación cuántica resuelve más eficientemente que la clásica determinista.

## 2. Dónde está el speedup: el mecanismo de la interferencia

La aceleración cuántica no proviene de "probar todas las soluciones a la vez". Esta descripción, aunque intuitiva, es engañosa: si así fuera, medir el estado cuántico final daría la solución correcta con probabilidad $1/N$ (igual que muestrear al azar), sin ninguna ventaja.

El mecanismo real es la **interferencia cuántica controlada**:

1. Se prepara una superposición uniforme sobre todos los estados.
2. El oráculo introduce fases negativas en los estados que cumplen la condición buscada.
3. Mediante operaciones unitarias diseñadas específicamente, las amplitudes de los estados incorrectos se cancelan (interferencia destructiva) y las de los estados correctos se refuerzan (interferencia constructiva).
4. La medición final produce la respuesta correcta con alta probabilidad.

Este mecanismo requiere que el problema tenga una **estructura matemática explotable**: periodicidad (Shor), paridad de una función (Deutsch-Jozsa), o marcado de un elemento específico (Grover). Sin esa estructura, el circuito cuántico no puede dirigir la interferencia de forma útil.

## 3. El modelo de oráculo y las separaciones

Muchas separaciones entre P, BPP y BQP se establecen en el **modelo de oráculo**: se comparan algoritmos que tienen acceso a una función $f$ como caja negra (pueden evaluar $f(x)$ pero no conocen su implementación).

En este modelo, las separaciones son limpias:

- **Deutsch-Jozsa:** distinguir funciones constantes de balanceadas en 1 consulta cuántica vs. $2^{n-1}+1$ clásica (determinista). Separación exponencial en número de consultas.
- **Bernstein-Vazirani:** recuperar $s$ en 1 consulta vs. $n$ clásica. Separación lineal.
- **Grover:** búsqueda en $O(\sqrt{N})$ vs. $O(N)$ clásica. Separación cuadrática.
- **Separación Simon:** existe un oráculo que BQP resuelve en polinomial pero BPP necesita exponencial. Primera separación exponencial vs. clásica probabilista.

Las separaciones en el modelo de oráculo no implican automáticamente separaciones en el modelo estándar (sin oráculo), pero proporcionan evidencia sólida de las diferencias en poder computacional.

## 4. El problema de Simon: una separación exponencial

El problema de Simon (precursor del algoritmo de Shor) ilustra la diferencia entre BQP y BPP de forma especialmente clara.

Dada una función $f : \{0,1\}^n \to \{0,1\}^n$ con la promesa de que $f(x) = f(y) \iff x = y \oplus s$ para algún $s$ oculto, encontrar $s$.

- **Clásicamente (BPP):** se necesitan $\Omega(2^{n/2})$ consultas con alta probabilidad.
- **Cuánticamente (BQP):** se necesitan $O(n)$ consultas.

La separación es exponencial. Y lo crucial: es frente a algoritmos clásicos **probabilistas**, no solo deterministas. El algoritmo de Shor generaliza esta idea al problema de periodicidad que está en la base de la factorización.

## 5. Qué no resuelve BQP

A pesar de las separaciones, BQP tiene limitaciones fundamentales:

**BQP y NP:** no se sabe si $NP \subseteq BQP$. La opinión predominante es que no. No existe ningún algoritmo cuántico que resuelva problemas NP-completos en tiempo polinomial.

El algoritmo de Grover da aceleración cuadrática para búsqueda en problemas NP: un problema con $2^n$ posibles soluciones se verifica en $O(2^{n/2})$ en lugar de $O(2^n)$. Pero esto no rompe la frontera exponencial: $O(2^{n/2})$ sigue siendo exponencial en $n$.

**QRAM:** muchos algoritmos cuánticos de procesamiento de datos (HHL, quantum ML) asumen acceso a **QRAM (Quantum Random Access Memory)**, que permitiría cargar $N$ datos en superposición en $O(\log N)$ tiempo. No existe una implementación escalable de QRAM en hardware real.

## 6. Ideas clave

- BQP es la clase de problemas eficientemente solucionables por circuitos cuánticos con error acotado.
- La ventaja cuántica no viene de "paralelismo cuántico" sino de interferencia constructiva/destructiva controlada.
- En el modelo de oráculo, BQP tiene separaciones exponenciales sobre BPP (problema de Simon).
- No se sabe si $NP \subseteq BQP$; la evidencia sugiere que no.
- Los algoritmos cuánticos de ML con ventaja exponencial suelen requerir QRAM, que no existe prácticamente.

## 7. Ejercicios sugeridos

1. Situar en el diagrama de clases de complejidad los siguientes problemas: factorización (Shor), búsqueda (Grover), satisfacibilidad, simulación de mecánica cuántica.
2. Explicar por qué el paralelismo cuántico (evaluar $f$ en superposición) por sí solo no da ventaja sin interferencia.
3. Describir el problema de Simon y el algoritmo cuántico que lo resuelve en $O(n)$ consultas.
4. Investigar qué es QRAM y por qué su ausencia limita los algoritmos de quantum machine learning.

## Navegacion

- Anterior: [POVM: intuicion y medicion generalizada](../17_medicion_avanzada_y_observables/02_povm_intuicion_y_medicion_generalizada.md)
- Siguiente: [Limites de la ventaja y comparacion clasica](02_limites_de_la_ventaja_y_comparacion_clasica.md)
