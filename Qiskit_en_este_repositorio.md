# Qiskit en este repositorio

## Para que sirve esta guia

Este documento explica como usar la parte de Qiskit dentro del proyecto sin perderse entre notebooks conceptuales, laboratorios y articulos teoricos.

## Tipos de cuadernos

### `ejemplos/`

Son cuadernos cortos, pensados para introducir una idea concreta:

- una representacion;
- una API;
- una intuicion matematica;
- una comparacion simple.

Conviene leerlos como apoyo inmediato a los articulos.

### `problemas_resueltos/`

Son cuadernos mas guiados, con vocacion de ejercicio trabajado paso a paso. Sirven para consolidar conceptos despues de leer teoria.

### `laboratorios/`

Son cuadernos mas abiertos o mas largos. Su papel es acercar la experiencia a una pequeña exploracion: comparar resultados, variar parametros o enlazar varias ideas del curso.

## Como leer Qiskit en este proyecto

La ruta recomendada es:

1. leer primero el articulo teorico;
2. pasar luego a un `ejemplo` corto;
3. despues a un `problema_resuelto` o `laboratorio`;
4. volver al articulo si hace falta reinterpretar lo visto.

## Que cuadernos son mas conceptuales

Especialmente conceptuales:

- `18_qiskit_sampler_conceptual.ipynb`
- `19_qiskit_estimator_conceptual.ipynb`
- `20_noise_model_conceptual.ipynb`
- `28_complejidad_y_bqp_intuicion.ipynb`
- `29_tomografia_estado_intuicion.ipynb`

## Que cuadernos son mas operativos

Mas cercanos a practica con flujo de trabajo:

- `06_qiskit_estado_vector_y_medicion.ipynb`
- `07_qiskit_backends_y_shots.ipynb`
- `11_qiskit_transpilacion_basica.ipynb`
- `21_qiskit_sparsepauliop_basico.ipynb`
- `26_estimator_y_hamiltonianos_sencillos.ipynb`

## Compatibilidad de versiones

Qiskit evoluciona. Por eso este repositorio intenta separar:

- la intuicion conceptual, que envejece mejor;
- de detalles de API concretos, que pueden cambiar con versiones.

Cuando una API concreta cambie, el objetivo pedagogico del cuaderno debe seguir siendo valido aunque el codigo requiera ajustes menores.

## Relacion con el tutorial

Las secciones teoricas mas ligadas a Qiskit son:

- [Tutorial/04_qiskit](Tutorial/04_qiskit/README.md)
- [Tutorial/10_qiskit_avanzado](Tutorial/10_qiskit_avanzado/README.md)
- [Tutorial/15_hamiltonianos_y_evolucion_temporal](Tutorial/15_hamiltonianos_y_evolucion_temporal/README.md)
- [Tutorial/19_tomografia_y_caracterizacion](Tutorial/19_tomografia_y_caracterizacion/README.md)
