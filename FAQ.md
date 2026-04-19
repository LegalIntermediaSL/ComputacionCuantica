# FAQ

## Superposicion y mezcla son lo mismo?

No. Una superposicion mantiene coherencia entre amplitudes y puede producir interferencia. Una mezcla describe incertidumbre estadistica o perdida de acceso a la informacion y se representa de forma natural con matrices de densidad.

## Fase global y fase relativa son equivalentes?

No. La fase global no cambia resultados observables, mientras que la fase relativa si puede modificar la interferencia y, por tanto, el comportamiento del circuito.

## Un simulador ideal representa hardware real?

No. Un simulador ideal muestra el comportamiento matematico perfecto del circuito. El hardware real introduce ruido, limitaciones de conectividad, errores de puerta y errores de lectura.

## Por que la transpilacion cambia el circuito?

Porque adapta el circuito abstracto a un conjunto de puertas y restricciones concretas del backend. Puede cambiar la forma visible del circuito sin cambiar su significado ideal.

## Medir un circuito revela todo el estado?

No. La medicion produce un resultado clasico compatible con una distribucion de probabilidad, no una lectura completa de todas las amplitudes del estado cuantico.

## Por que no basta con copiar qubits para corregir errores?

Porque el teorema de no-clonacion impide copiar arbitrariamente un estado cuantico desconocido. La correccion de errores cuanticos necesita codificacion y mediciones de sindrome, no copias directas.

## Para que sirven Sampler y Estimator?

Sirven para organizar preguntas diferentes sobre un circuito:

- `Sampler` cuando interesa la distribucion de salidas;
- `Estimator` cuando interesan valores esperados de observables.
