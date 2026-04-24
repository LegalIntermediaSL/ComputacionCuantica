# Límites de la ventaja cuántica y comparación con lo clásico

## 1. La frontera entre BQP y NP

Una pregunta central en complejidad cuántica es si los procesadores cuánticos pueden resolver problemas NP-completos en tiempo polinomial. La respuesta, según la evidencia actual, es que probablemente no.

El argumento más sólido es el siguiente: si $NP \subseteq BQP$, entonces el algoritmo cuántico para SAT podría usarse para resolver todos los problemas NP en polinomial. Esto colapsa toda la jerarquía de complejidad de formas que se consideran extremadamente improbables.

Un resultado más formal: en el modelo de oráculo con un oráculo aleatorio, BQP no contiene NP con alta probabilidad. Esto no es una prueba en el modelo estándar, pero es evidencia de que la separación es real.

¿Qué puede ofrecer entonces la computación cuántica para problemas NP?

- **Grover:** aceleración cuadrática. Para SAT con $2^n$ asignaciones, requiere $O(2^{n/2})$ evaluaciones. Es exponencial en $n$, solo cuadráticamente mejor.
- **QAOA:** heurística variacional para optimización combinatoria. Sin garantías de optimalidad ni de superar a los mejores clásicos.
- **Quantum annealing (D-Wave):** heurística física para QUBO. En benchmarks cuidadosos, raramente supera al mejor clásico (simulated annealing, TABU search).

## 2. El límite de Grover y su impacto en criptografía

El algoritmo de Grover da una aceleración cuadrática universal para cualquier búsqueda no estructurada. Sus implicaciones más concretas son en criptografía simétrica:

- **AES-128:** la búsqueda de clave requiere $2^{128}$ operaciones clásicas, o $2^{64}$ con Grover. Migrar a AES-256 restaura el margen de seguridad.
- **SHA-256 (colisiones):** Grover no ayuda directamente porque encontrar colisiones en hash es diferente de búsqueda inversa.
- **Funciones hash (preimagen):** $O(2^{n/2})$ con Grover frente a $O(2^n)$ clásico.

La respuesta del sector: duplicar el tamaño de clave en criptografía simétrica, lo que es un ajuste menor. La amenaza de Shor a la criptografía asimétrica (RSA, ECC) es mucho más grave.

## 3. El problema de la simulación clásica

Una manera de entender los límites de BQP es preguntarse qué tan difícil es simular un circuito cuántico clásicamente.

**Resultado de Gottesman-Knill:** cualquier circuito que use solo puertas del grupo de Clifford ($H, S, CNOT$) y mediciones en la base computacional puede simularse eficientemente en un ordenador clásico en $O(n^2)$ por puerta.

Esto implica que la ventaja cuántica requiere necesariamente puertas no-Clifford (como la puerta $T$).

**Simulación con contracción de tensores:** para circuitos de baja profundidad con estructura de red tensorial, la simulación clásica es eficiente. Los mejores simuladores actuales (cuteQC, cotengra) pueden simular circuitos de 50+ qubits si su entrelazamiento es limitado.

**Limite de simulabilidad:** circuitos con entrelazamiento lineal (volume law) o profundidad $\Omega(\log n)$ con puertas no-Clifford aleatorizadas son difíciles de simular para los mejores métodos clásicos conocidos. Es en esta región donde se espera la ventaja cuántica genuina.

## 4. Algoritmos cuánticos con ventaja polinomial vs. exponencial

| Algoritmo | Problema | Speedup sobre clásico | Comentario |
|---|---|---|---|
| Deutsch-Jozsa | Constante vs. balanceada | Exponencial (consultas) | Modelo oráculo; sin ventaja vs. probabilista |
| Simon | Periodicidad mod 2 | Exponencial (consultas) | Modelo oráculo |
| Shor (factorización) | Factorizar $N$ | Exponencial (sin oráculo) | Asume $P \neq BQP$ |
| Grover | Búsqueda | Cuadrático | Óptimo para búsqueda no estructurada |
| QFT | Transformada de Fourier | Exponencial (sobre FFT) | Solo útil como subrutina interna |
| HHL | Sistemas lineales $Ax=b$ | Exponencial (con QRAM) | QRAM no disponible prácticamente |
| QAOA | Optimización combinatoria | No probado | Heurística; sin garantías |

## 5. El coste oculto: la medición

Una fuente frecuente de confusión sobre el poder de BQP es olvidar el papel de la medición. Un circuito cuántico puede preparar un estado que codifica una respuesta útil, pero extraer esa respuesta requiere medir, y la medición destruye la superposición.

Si la respuesta útil está en una amplitud específica de un estado de $n$ qubits, encontrarla con probabilidad $\geq 2/3$ puede requerir múltiples ejecuciones del circuito (amplificación de amplitudes). Este overhead puede cancelar parte de la ventaja teórica.

El ejemplo paradigmático es la QFT: calcula la transformada de Fourier discreta en $O(n^2)$ puertas, pero leer todos los coeficientes requeriría $O(N)$ mediciones, restaurando el coste original.

## 6. Ideas clave

- Los problemas NP-completos probablemente no están en BQP: Grover da aceleración cuadrática, no exponencial.
- La simulación de circuitos Clifford es eficiente clásicamente; la ventaja cuántica requiere puertas no-Clifford.
- Los algoritmos con ventaja exponencial sin oráculo (Shor) son escasos y aplican a estructuras algebraicas muy específicas.
- El coste de la medición y la necesidad de QRAM limitan la ventaja práctica de muchos algoritmos teóricos.
- La región de ventaja cuántica genuina (en hardware real) se centra en simulación cuántica y criptoanálisis.

## 7. Ejercicios sugeridos

1. Verificar que el circuito $H \to CNOT \to H$ (creación y medición de un estado de Bell) puede simularse eficientemente usando el formalismo de Clifford.
2. Estimar el tiempo clásico de Grover sobre AES-128 y AES-256, y la seguridad resultante.
3. Explicar por qué la QFT cuántica no puede usarse directamente para calcular la DFT de señales clásicas eficientemente.
4. Investigar el algoritmo HHL para sistemas lineales y las condiciones bajo las cuales da ventaja exponencial real.

## Navegacion

- Anterior: [BQP, oraculos y speedup](01_bqp_oraculos_y_speedup.md)
- Siguiente: [Tomografia de estados: intuicion y reconstruccion](../19_tomografia_y_caracterizacion/01_tomografia_de_estados_intuicion_y_reconstruccion.md)
