# Fidelidad y caracterizacion operacional

## Prerequisitos

- Matrices de densidad.
- Ruido y canales cuanticos.
- Idea general de tomografia.

## Objetivos

- comprender por que la fidelidad es una metrica central;
- conectar caracterizacion con hardware real y ruido;
- enlazar teoria de estados con validacion experimental.

## 1. Por que necesitamos metricas

Una vez que intentamos reconstruir o estimar un estado, surge enseguida otra pregunta: cuan cerca esta ese estado del objetivo ideal que queriamos preparar?

Ahí aparece la fidelidad como una de las medidas mas usadas.

## 2. Idea general de fidelidad

Sin entrar en todas las variantes tecnicas, la fidelidad expresa cercania entre descripciones cuanticas. Pedagogicamente, su papel es claro:

- cuantificar calidad de preparacion;
- comparar salida ideal y salida real;
- y dar una medida interpretable del deterioro por ruido.

## 3. Caracterizacion y hardware

La fidelidad no vive aislada del resto del tutorial. Se conecta con:

- tomografia;
- ruido y canales;
- mitigacion de errores;
- y evaluacion realista de circuitos y dispositivos.

## 4. Valor para el lector

Este bloque ayuda a cambiar de mentalidad. No solo importa escribir un circuito correcto en papel. Tambien importa saber como evaluar si lo que se implementa sigue pareciendose a la intencion original.

## 5. Errores comunes

- pensar que un circuito bien definido garantiza automaticamente un estado bien preparado;
- usar la palabra fidelidad sin relacionarla con una comparacion concreta;
- separar demasiado la teoria de estados de la evaluacion experimental.

## 6. Ejercicios sugeridos

1. Explica por que la fidelidad es relevante aunque el circuito ideal este perfectamente definido.
2. Relaciona fidelidad con ruido y con desviaciones respecto al estado objetivo.
3. Describe por que tomografia y fidelidad forman una pareja natural.

## 7. Material asociado

- Cuaderno: [29_tomografia_estado_intuicion.ipynb](../../Cuadernos/ejemplos/29_tomografia_estado_intuicion.ipynb)
- Cuaderno: [31_fidelidad_antes_y_despues_de_ruido.ipynb](../../Cuadernos/ejemplos/31_fidelidad_antes_y_despues_de_ruido.ipynb)
- Laboratorio: [14_densitymatrix_ruido_y_tomografia_guiada.ipynb](../../Cuadernos/laboratorios/14_densitymatrix_ruido_y_tomografia_guiada.ipynb)
- Laboratorio: [15_noise_vs_fidelity_guiada.ipynb](../../Cuadernos/laboratorios/15_noise_vs_fidelity_guiada.ipynb)
- Articulo relacionado: [Mitigacion de errores y fidelidad](../06_ruido_y_hardware/02_mitigacion_errores_y_fidelidad.md)

## Navegacion

- Anterior: [Tomografia de estados: intuicion y reconstruccion](01_tomografia_de_estados_intuicion_y_reconstruccion.md)
- Siguiente: [Trotter-Suzuki y coste de simulacion](../20_simulacion_cuantica_avanzada/01_trotter_suzuki_y_coste_de_simulacion.md)
