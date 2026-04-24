# Qué puede y qué no puede hacer la computación cuántica hoy

## 1. La promesa y la realidad

Una lectura superficial de la literatura sobre computación cuántica puede dar la impresión de que los procesadores cuánticos resolverán cualquier problema más rápido que un ordenador clásico. Esta impresión es incorrecta y conviene deshacer el malentendido antes de trabajar en el campo.

La computación cuántica **no** es una versión más rápida de la computación clásica para tareas arbitrarias. Para la mayoría de los problemas cotidianos (procesamiento de texto, renderizado gráfico, bases de datos, aprendizaje automático estándar), un procesador clásico moderno es mucho más eficiente que cualquier procesador cuántico existente o proyectado.

La ventaja cuántica es específica: aparece en un conjunto bien definido de problemas que tienen una estructura matemática explotable por la interferencia y el entrelazamiento cuánticos.

## 2. Dónde existe ventaja cuántica demostrada

Los problemas para los que existe ventaja cuántica asintótica comprobada son:

**Factorización de enteros (algoritmo de Shor):** factorizar un entero de $n$ bits en $O(n^3)$ tiempo cuántico, frente a subexponencial $O(e^{n^{1/3}})$ clásico. La ventaja es exponencial en sentido práctico y amenaza la criptografía RSA y de curvas elípticas.

**Búsqueda no estructurada (algoritmo de Grover):** $O(\sqrt{N})$ frente a $O(N)$ clásico. La aceleración es cuadrática, no exponencial.

**Simulación de sistemas cuánticos (propuesta de Feynman):** simular la dinámica de un sistema de $n$ partículas cuánticas requiere $O(2^n)$ memoria clásica pero $O(\text{poly}(n))$ en un procesador cuántico. Es la motivación original de la computación cuántica.

**Logaritmo discreto y problemas de periodicidad (algoritmo de Shor generalizado):** base de la criptografía de curvas elípticas y Diffie-Hellman.

## 3. Dónde no existe ventaja cuántica establecida

Para la mayoría de los problemas, no existe ventaja cuántica conocida o probada:

**Problemas NP-completos:** no hay evidencia de que BQP contenga NP-completo. Grover da aceleración cuadrática, pero no exponencial. El problema del viajante, la satisfacibilidad booleana, y la coloración de grafos no tienen soluciones cuánticas eficientes conocidas.

**Aprendizaje automático clásico:** la mayoría de los algoritmos de quantum machine learning tienen las mismas advertencias que la QFT aplicada a señales clásicas: la aceleración teórica requiere acceso cuántico a los datos (QRAM) que no existe de forma práctica.

**Optimización convexa:** los optimizadores cuánticos (QAOA) no garantizan mejora sobre los mejores algoritmos clásicos para problemas bien estructurados.

## 4. Las restricciones del hardware actual (NISQ)

Los procesadores cuánticos disponibles hoy están en el régimen **NISQ**:

- **Escala:** entre 100 y 1000 qubits en los mejores dispositivos actuales.
- **Fidelidad de puerta:** $F_1 \approx 99.9\%$ para puertas de un qubit, $F_2 \approx 99\%$-$99.5\%$ para CNOT.
- **Tiempo de coherencia:** $T_1 \sim 100 \mu s$, $T_2 \sim 100 \mu s$ en superconductores.
- **Profundidad de circuito efectiva:** limitada a $O(10^2)$ puertas CNOT antes de que el ruido destruya la señal.

Estas restricciones hacen imposible ejecutar el algoritmo de Shor para claves RSA reales (requeriría $\sim 10^6$ qubits lógicos con corrección de errores) o simulaciones moleculares de interés farmacéutico (requieren $\sim 10^3$-$10^4$ qubits lógicos).

## 5. Lo que sí es posible hoy

En el régimen NISQ, las aplicaciones más prometedoras son:

- **VQE y simulación de moléculas pequeñas:** 10-50 qubits, sin corrección de errores, con mitigación de errores. Valor científico en química de precisión media.
- **QAOA en grafos pequeños:** resultados comparables pero no superiores a métodos clásicos heurísticos.
- **Benchmarking y metrología cuántica:** verificación de dispositivos, estimación de parámetros físicos.
- **Algoritmos de muestreo:** random circuit sampling (base de las demostraciones de "supremacía cuántica").
- **Criptografía post-cuántica:** no requiere hardware cuántico, pero es una consecuencia directa de la amenaza del algoritmo de Shor.

## 6. Ideas clave

- La computación cuántica no acelera todos los problemas: la ventaja es específica y requiere estructura explotable.
- Las ventajas cuánticas demostradas asintóticamente son la factorización (exponencial), la búsqueda (cuadrática) y la simulación cuántica (exponencial).
- No hay evidencia de que BQP contenga NP-completo.
- El hardware NISQ actual limita la profundidad de circuito a ~100 puertas CNOT con fidelidad útil.
- Las aplicaciones más realistas hoy son VQE para moléculas pequeñas, QAOA heurístico y metrología.

## 7. Ejercicios sugeridos

1. Estimar cuántos qubits lógicos (con corrección de errores) se necesitarían para factorizar un número de 2048 bits con el algoritmo de Shor.
2. Buscar tres ejemplos de problemas en BQP que no estén en P clásico (según la evidencia actual).
3. Describir la diferencia entre "supremacía cuántica" y "ventaja cuántica" tal como se usan en la literatura.
4. Proponer una tarea concreta del mundo real para la que VQE sea actualmente útil y justificar la elección.

## Navegacion

- Anterior: [Repetidores y redes de entrelazamiento](../27_internet_cuantico_and_comunicaciones/02_repetidores_y_entanglement_swapping.md)
- Siguiente: [Realismo sobre ventaja cuantica](02_realismo_sobre_ventaja_cuantica.md)
