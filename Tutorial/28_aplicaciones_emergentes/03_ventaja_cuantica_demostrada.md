# Ventaja cuántica demostrada: experimentos reales 2019-2024

## 1. El estándar de la ventaja cuántica

Para que un experimento cuántico demuestre **ventaja cuántica** genuina, debe satisfacer tres criterios:

1. **Speedup verificable:** el tiempo de ejecución cuántico $t_Q$ debe ser significativamente menor que el mejor algoritmo clásico conocido $t_C$.
2. **Verificabilidad:** debe existir un método para verificar que el resultado cuántico es correcto (o al menos cercano al correcto).
3. **Tarea relevante:** idealmente, la tarea debe tener utilidad práctica más allá de ser un benchmark diseñado para que el dispositivo cuántico gane.

El tercer criterio es el más controvertido: los primeros experimentos de "supremacía cuántica" usaron tareas (muestreo de circuitos aleatorios) que son difíciles clásicamente precisamente porque son inútiles para cualquier aplicación práctica.

## 2. Google Sycamore (2019): sampling de circuitos aleatorios

### 2.1 El experimento

En octubre de 2019, el equipo de Google publicó en Nature la primera demostración de **supremacía cuántica**: el procesador Sycamore (53 qubits) ejecutó el muestreo de un circuito cuántico aleatorio de profundidad 20 en 200 segundos, una tarea que estimaron llevaría 10.000 años al supercomputador Summit (IBM) más potente del momento.

### 2.2 La métrica: Cross-Entropy Benchmarking (XEB)

La calidad del muestreo se verificó mediante XEB: comparar la distribución de bitstings medidos con la distribución teórica predicha por simulación clásica de un circuito más pequeño. La fidelidad XEB:

$$
F_\text{XEB} = 2^n \langle p(x) \rangle_\text{medido} - 1
$$

donde $p(x)$ es la probabilidad teórica del bitstring $x$ y el promedio es sobre los bitstings medidos. Para un dispositivo ideal: $F_\text{XEB} = 1$. Google midió $F_\text{XEB} \approx 0.002$, consistente con el error acumulado esperado del circuito.

### 2.3 La controversia

IBM respondió en el mismo mes que el tiempo clásico estimado era erróneo: usando almacenamiento en disco masivo y un algoritmo de simulación de árbol de Schrödinger mejorado, el tiempo clásico se reducía a 2.5 días (no 10.000 años). Investigadores chinos (2022) lograron simularlo en 304 segundos en un clúster de GPUs.

**Lección:** la "supremacía" de 2019 no es falsa, pero el margen de ventaja era mucho menor del afirmado, y la tarea no tiene utilidad práctica.

## 3. IBM Eagle y "quantum utility" (2023)

### 3.1 El experimento

En junio de 2023, IBM publicó en Nature el primer experimento de **quantum utility** con el procesador Eagle de 127 qubits: simulación de la dinámica del modelo de Ising transverso en 2D, un problema de física de muchos cuerpos.

La tarea específica: calcular $\langle Z \rangle$ en función del tiempo para el Hamiltoniano:
$$
H = -J\sum_{\langle i,j\rangle} Z_iZ_j - h\sum_i X_i
$$

con 127 qubits y hasta 60 capas de puertas (profundidad efectiva muy alta).

### 3.2 La clave: mitigación de errores

El resultado fue posible gracias a la combinación de:
- **ZNE** (Zero-Noise Extrapolation) para mitigar errores de puerta.
- **TREX** (Twirled Readout Error eXtinction) para mitigar errores de medición.
- **Probabilistic Error Amplification** para caracterizar el ruido.

Con estas técnicas, el resultado cuántico con mitigación coincidió con simulaciones clásicas exactas disponibles para sistemas pequeños, extrapolando a 127 qubits donde las simulaciones clásicas son infeasibles.

### 3.3 La controversia (de nuevo)

Investigadores de la ETH Zürich (2023) demostraron que el mismo sistema podía simularse clásicamente usando redes tensoriales 2D (PEPS) con tiempo de simulación comparable al experimento cuántico, argumentando que la ventaja no existía.

**Lección:** la frontera de la "utility" cuántica depende de los métodos clásicos disponibles, y esta frontera se mueve continuamente.

### 3.4 Evaluación honesta

El experimento IBM Eagle es significativo porque:
- Demuestra que la mitigación de errores permite obtener resultados físicos útiles en hardware NISQ.
- Para ciertos parámetros del modelo de Ising, la simulación clásica es genuinamente más lenta.
- La combinación de hardware + mitigación + software representa el estado del arte en NISQ.

Pero no es "ventaja cuántica incondicional" para una tarea de interés práctico general.

## 4. Quantinuum H2 y el primer experimento fault-tolerant (2024)

### 4.1 El experimento

En 2024, Quantinuum demostró en el procesador H2 (56 qubits con iones atrapados) los primeros cálculos con qubits lógicos con corrección de errores **activa** que superan en fidelidad a los qubits físicos en la misma tarea:

- Codificación de qubits lógicos con el código de Steane ([[7,1,3]]) y el código [[4,2,2]].
- Fidelidad de un qubit lógico > fidelidad del mejor qubit físico en el mismo dispositivo.
- Primer ejemplo de **quantum error correction below threshold** en un sistema de iones.

### 4.2 La métrica: logical error rate

Para el código [[4,2,2]] (distancia 2, detecta 1 error, corrige 0):
- Tasa de error física: $p_\text{físico} \approx 5 \times 10^{-3}$ por puerta CNOT.
- Tasa de error lógica: $p_\text{lógico} \approx 1.4 \times 10^{-3}$ por operación lógica.
- Ratio de mejora: $p_L / p_\text{físico} \approx 0.28 < 1$: la corrección mejora la fidelidad.

Este es el **umbral de corrección**: se demuestra que al añadir redundancia y corrección, el error disminuye en lugar de aumentar.

### 4.3 Relevancia

Este resultado de Quantinuum es el más significativo técnicamente de los tres porque demuestra:
- El principio fundamental de la computación cuántica tolerante a fallos funciona en hardware real.
- Los iones atrapados pueden operar por debajo del umbral de error.
- La ruta hacia la computación cuántica de gran escala con corrección es físicamente posible.

La limitación: el experimento usa solo 7-10 qubits lógicos. Los algoritmos útiles (Shor para RSA-2048, FeMoco) requieren $10^3$-$10^4$ qubits lógicos.

## 5. Google Willow (2024): sampling más allá del umbral de error

En diciembre de 2024, Google publicó resultados con el procesador Willow (105 qubits superconductores) mostrando:
- La primera demostración de que al añadir más qubits al código de corrección, la tasa de error **disminuye exponencialmente** (below threshold).
- Muestreo de circuito aleatorio en 5 minutos; simulación clásica estimada: $10^{25}$ años.

La estimación clásica del tiempo es más robusta que en 2019 porque usa el mejor conocimiento actual de algoritmos de simulación.

## 6. Tabla comparativa de hitos

| Año | Equipo | Procesador | Tarea | Ventaja | Controversia |
|---|---|---|---|---|---|
| 2019 | Google | Sycamore (53Q) | RCS sampling | 200s vs 10k años | IBM: reducible a 2.5 días |
| 2020 | USTC China | Jiuzhang (boson) | Boson sampling | 200s vs 600M años | Mejorado clásicamente |
| 2023 | IBM | Eagle (127Q) | Ising 2D | Útil con mitigación | ETH: simulable con PEPS |
| 2024 | Quantinuum | H2 (56Q) | Corrección errores | 1er below-threshold | Pocos qubits lógicos |
| 2024 | Google | Willow (105Q) | RCS sampling | 5 min vs 10²⁵ años | Sin tarea práctica |

## 7. Ideas clave

- "Supremacía cuántica" (Google 2019) y "quantum utility" (IBM 2023) son hitos reales pero no incondicionales: la frontera se mueve con la mejora de algoritmos clásicos.
- El experimento de Quantinuum H2 (2024) es el más fundamentado: demuestra corrección de errores below threshold, base de la computación tolerante a fallos.
- Google Willow (2024) amplía el sampling más allá de lo simulable clásicamente con más robustez metodológica que 2019.
- La ruta hacia aplicaciones prácticas (Shor, VQE para química, optimización) requiere $10^3$-$10^4$ qubits lógicos, estimados para 2030-2040.
- La mitigación de errores (ZNE, PEC) es la herramienta puente: permite resultados físicamente útiles en hardware NISQ mientras se desarrolla la corrección completa.

## 8. Ejercicios sugeridos

1. Implementar el protocolo XEB para un circuito aleatorio de 4 qubits y verificar que $F_\text{XEB} \approx 1$ para el simulador ideal.
2. Estimar el número de shots necesario para verificar $F_\text{XEB} > 0.001$ en un circuito de 20 qubits con ruido despolarizante del 0.5% por puerta.
3. Simular la dinámica del modelo de Ising transverso 1D para 10 sitios y comparar con y sin ZNE: ¿qué nivel de ruido requiere ZNE para recuperar el valor correcto?
4. Calcular la tasa de error lógica para el código de Steane [[7,1,3]] con $p_\text{físico} = 10^{-3}$ y comparar con el qubit físico desnudo.

## Navegación

- Anterior: [Quantum Machine Learning: kernels y barreras](02_quantum_machine_learning_kernels.md)
- Siguiente: (fin del bloque 28)
