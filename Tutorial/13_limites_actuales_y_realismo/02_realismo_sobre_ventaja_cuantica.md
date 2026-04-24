# Realismo sobre ventaja cuántica

## 1. Qué significa "ventaja cuántica"

El término **ventaja cuántica** (quantum advantage) designa una situación en la que un procesador cuántico resuelve un problema concreto más rápido, con menos recursos, o de forma más precisa que cualquier algoritmo clásico conocido ejecutado en el mejor hardware clásico disponible.

La definición tiene matices importantes:

- **Complejidad asintótica vs. rendimiento práctico:** un algoritmo cuántico puede ser asintóticamente superior pero necesitar $10^6$ qubits lógicos o tiempos de puerta que no existen actualmente. La ventaja teórica no implica ventaja práctica inmediata.
- **Ventaja en modelos de oráculo:** las separaciones más fuertes (Deutsch-Jozsa, Bernstein-Vazirani) están en modelos de caja negra que no se corresponden directamente con problemas prácticos.
- **Desplazamiento del mejor clásico:** los algoritmos clásicos también mejoran. Una ventaja cuántica medida hoy puede desaparecer mañana si un nuevo algoritmo clásico supera al clásico de referencia.

## 2. El experimento de Google Sycamore (2019)

En 2019, Google publicó el primer experimento de **supremacía cuántica**: el procesador Sycamore (53 qubits) completó en 200 segundos una tarea de muestreo aleatorio de circuitos que, según sus estimaciones, tomaría 10.000 años en el superordenador Summit de IBM.

Esta afirmación generó controversia inmediata. IBM respondió que con técnicas de simulación clásica mejoradas (compresión de tensores), el mismo cálculo podría realizarse en 2.5 días en hardware clásico. Investigaciones posteriores mostraron que con mejoras algorítmicas adicionales el tiempo clásico bajaba aún más.

La conclusión es que la separación práctica entre el procesador cuántico y el mejor clásico era mucho menor de lo afirmado inicialmente. Esto no invalida el experimento como demostración de capacidad, pero sí ilustra la dificultad de establecer ventajas cuánticas robustas en hardware actual.

## 3. El experimento de IBM Eagle y "quantum utility" (2023)

IBM adoptó el término más cauteloso de **quantum utility**: usar un procesador cuántico para calcular una cantidad física que es difícil (pero no imposible) de simular clásicamente, con valor científico real.

El experimento con el procesador Eagle (127 qubits) calculó valores esperados en un modelo de Ising 2D con 127 spins usando técnicas de mitigación de errores (ZNE). Los resultados cuánticos con mitigación concordaban mejor con el valor exacto que ciertos métodos de simulación clásica de referencia en regímenes de tiempo de evolución intermedios.

Sin embargo, trabajos posteriores mostraron que métodos clásicos mejorados (DMRG, TEBD con truncamiento adaptativo) podían igualar o superar los resultados cuánticos. La "utilidad" dependía de la elección del algoritmo clásico de comparación.

## 4. Perspectiva sobre el estado actual

Una evaluación honesta del estado del campo en 2026:

| Afirmación | Estado |
|---|---|
| Supremacía cuántica demostrada | Controvertido: la separación era mayor en 2019 que hoy dado el progreso clásico |
| Ventaja cuántica en simulación cuántica | Preliminar: resultados IBM Eagle son un paso, pero no definitivos |
| Ventaja cuántica en optimización combinatoria | No demostrada en problemas prácticos |
| Ventaja cuántica en ML | No demostrada con datos clásicos realistas |
| Ventaja cuántica en criptoanálisis (Shor) | Existente en teoría; inalcanzable con hardware actual sin corrección de errores |

## 5. El horizonte temporal de la ventaja práctica

Las proyecciones más conservadoras de los principales grupos de investigación apuntan a:

- **2025-2030:** primeros sistemas con corrección parcial de errores (~1000 qubits físicos por qubit lógico), capaces de ejecutar algoritmos con decenas de qubits lógicos.
- **2030-2040:** procesadores tolerantes a fallos con cientos de qubits lógicos, suficientes para química cuántica de moléculas medianas y factorización de números pequeños.
- **Post-2040:** procesadores con miles de qubits lógicos, donde la ventaja en factorización y simulación cuántica sería prácticamente significativa.

Estas proyecciones tienen incertidumbre considerable. El progreso en corrección de errores, fabricación de qubits de alta fidelidad, y software de compilación puede acelerar o retrasar estos plazos.

## 6. Cómo leer la literatura con criterio

Algunos criterios para evaluar afirmaciones de ventaja cuántica:

1. **¿Con qué algoritmo clásico se compara?** La comparación debe ser con el mejor algoritmo clásico conocido, no con fuerza bruta.
2. **¿Es el problema útil o diseñado para favorecer al cuántico?** El muestreo de circuitos aleatorios es difícil de simular clásicamente pero de utilidad práctica mínima.
3. **¿Se incluye el overhead de corrección de errores?** Los algoritmos teóricos suelen ignorar el coste masivo de los qubits lógicos.
4. **¿Es la ventaja asintótica o para tamaños realistas?** Una ventaja exponencial asintótica puede requerir tamaños de problema que no existen.

## 7. Ideas clave

- "Ventaja cuántica" requiere superar al mejor algoritmo clásico en un problema de utilidad real, no solo en modelos de oráculo.
- Los experimentos de supremacía cuántica (2019-2023) demostraron capacidad de hardware, no ventaja en problemas prácticos.
- La distancia real entre los mejores dispositivos cuánticos y los mejores clásicos es menor de lo que las afirmaciones iniciales sugerían.
- La ventaja cuántica práctica en problemas relevantes (química, criptoanálisis) requiere corrección de errores que aún no está disponible a escala.
- Evaluar afirmaciones de ventaja cuántica requiere comparar con el mejor algoritmo clásico, no con fuerza bruta.

## 8. Ejercicios sugeridos

1. Buscar el artículo original de Google Sycamore (2019) y leer la respuesta de IBM. Resumir los puntos de discrepancia.
2. Estimar el número de qubits físicos necesarios para factorizar un número de 512 bits con el algoritmo de Shor, asumiendo un umbral de corrección de errores del 1%.
3. Comparar las afirmaciones de ventaja cuántica en optimización de QAOA con los mejores algoritmos clásicos de aproximación para MaxCut.
4. Definir un criterio riguroso para declarar "ventaja cuántica práctica" en química computacional.

## Navegacion

- Anterior: [Que puede y que no puede hacer la computacion cuantica hoy](01_que_puede_y_que_no_puede_hacer_la_computacion_cuantica_hoy.md)
- Siguiente: [Bibliografia comentada](../07_apendices/bibliografia_comentada.md)
