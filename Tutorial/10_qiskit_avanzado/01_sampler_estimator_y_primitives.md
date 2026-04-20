# Sampler, Estimator y primitives

## 1. Que cambia al pasar a primitives

Cuando un proyecto madura, deja de ser natural pensar en Qiskit solo como una herramienta para “dibujar circuitos y medir”. En muchos workflows interesa pedir directamente cierto tipo de resultado de forma mas estructurada.

Las `primitives` aparecen precisamente para eso: encapsulan tareas frecuentes de manera mas clara y reusable.

## 2. Sampler

La primitive `Sampler` esta orientada a distribuciones de salida. Conceptualmente encaja muy bien cuando lo que queremos son probabilidades o cuentas asociadas a mediciones de circuitos.

Desde el punto de vista pedagogico, `Sampler` ayuda a consolidar una intuicion importante:

- hay casos donde lo relevante son strings de salida;
- el circuito es un medio para producir una distribucion;
- la interfaz de alto nivel puede reflejar mejor esa intencion.

## 3. Estimator

`Estimator` responde a otra necesidad: calcular valores esperados de observables. Esto lo vuelve especialmente importante en:

- algoritmos variacionales;
- estimacion de energia;
- evaluacion de cantidades fisicas asociadas a operadores.

Pedagogicamente, `Estimator` obliga a conectar tres capas:

- el circuito que prepara el estado;
- el observable que queremos medir;
- el valor esperado como magnitud de interes.

## 4. Ventaja conceptual

La principal ventaja de estas interfaces no es solo comodidad de programacion. Tambien ordenan mejor el pensamiento:

- `Sampler`: me interesan distribuciones de salida;
- `Estimator`: me interesan expectativas de observables.

Esa distincion es muy valiosa para evitar mezclar tipos de resultado diferentes bajo una misma intuicion difusa de “ejecutar un circuito”.

## 5. Lugar dentro del proyecto

En este tutorial, `Sampler` y `Estimator` deben introducirse como una puerta de entrada a Qiskit mas moderno y mas cercano a workflows reales, sin perder la claridad conceptual.

## 6. Ideas clave

- Las `primitives` añaden una capa de abstraccion útil sobre la ejecucion de circuitos.
- `Sampler` organiza resultados tipo distribucion o muestreo.
- `Estimator` organiza resultados tipo valor esperado.
- Entender la diferencia mejora tanto el codigo como la comprension teorica.

## Navegacion

- Anterior: [Fault tolerance como horizonte](../14_surface_codes_y_horizonte_fault_tolerant/02_fault_tolerance_como_horizonte.md)
- Siguiente: [Operators, Pauli y representaciones utiles](02_operator_y_paulis.md)
