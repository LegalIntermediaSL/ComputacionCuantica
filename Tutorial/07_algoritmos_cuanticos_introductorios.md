# Algoritmos cuanticos introductorios

## 1. Que significa algoritmo cuantico

Un algoritmo cuantico es un procedimiento que organiza la preparacion, evolucion y medicion de un sistema cuantico para resolver una tarea computacional. No cualquier circuito interesante constituye ya una ventaja cuantica, pero muchos algoritmos famosos muestran como aprovechar superposicion, interferencia y entrelazamiento de forma sistematica.

## 2. La idea general

Muchos algoritmos cuanticos siguen un esquema reconocible:

1. preparar un estado inicial sencillo;
2. crear superposicion;
3. aplicar una transformacion que codifica el problema;
4. usar interferencia para reforzar respuestas correctas;
5. medir en una base adecuada.

La potencia del algoritmo no reside en "probar todas las posibilidades a la vez" de manera ingenua, sino en diseñar una interferencia util.

## 3. Deutsch-Jozsa como ejemplo conceptual

El algoritmo de Deutsch-Jozsa es uno de los primeros ejemplos didacticos porque muestra una separacion clara entre enfoque clasico y cuantico en un problema idealizado. Su importancia es mas pedagogica que practica, pero enseña muy bien como la interferencia puede codificar informacion global sobre una funcion.

## 4. Grover como idea de amplificacion

El algoritmo de Grover introduce otra intuicion central: la amplificacion de amplitud. En lugar de enumerar resultados uno por uno, el circuito redistribuye amplitudes para aumentar la probabilidad de medir una respuesta buscada.

Este algoritmo es especialmente importante porque enseña una pauta recurrente: la ventaja cuantica puede surgir de manipular inteligentemente el espacio de estados, no solo de paralelismo ingenuo.

## 5. Que debe aprenderse en una primera etapa

Antes de entrar en demostraciones completas, conviene que el lector entienda:

- donde aparece la superposicion;
- donde interviene la fase;
- como actua la interferencia;
- por que la medicion final no revela todo el estado;
- que significa que un algoritmo cuantico sea probabilistico.

## 6. Ideas clave

- Un algoritmo cuantico es un circuito diseñado para explotar recursos cuanticos.
- La interferencia es mas importante que la intuicion simplista de "calcular todo a la vez".
- Deutsch-Jozsa y Grover son excelentes puertas de entrada pedagogica.
- La ejecucion cuantica suele producir distribuciones de salida, no respuestas deterministas en una sola corrida.

## Navegacion

- Anterior: [Algebra lineal minima para computacion cuantica](06_algebra_lineal_minima_para_computacion_cuantica.md)
- Siguiente: [Qiskit: simuladores, estado cuantico y resultados](08_qiskit_simuladores_estado_y_resultados.md)
