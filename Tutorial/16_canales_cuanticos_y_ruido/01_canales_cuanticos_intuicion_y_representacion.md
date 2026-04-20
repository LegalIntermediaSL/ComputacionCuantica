# Canales cuanticos: intuicion y representacion

## 1. Por que hace falta un lenguaje mas rico

Cuando se trabaja solo con estados puros y evoluciones unitarias, la imagen de la computacion cuantica es demasiado ideal. En cuanto aparece ruido, perdida de informacion o interaccion con un entorno, necesitamos una descripcion mas general.

Ese lenguaje lo proporcionan los canales cuanticos.

## 2. De evolucion unitaria a transformacion efectiva

Una evolucion unitaria transforma un estado como

$$
\rho \mapsto U \rho U^\dagger.
$$

Pero un canal cuantico permite describir procesos mas generales donde el sistema no esta aislado. Desde un punto de vista introductorio, puede pensarse como una regla fisicamente valida que lleva estados cuanticos a otros estados cuanticos.

## 3. Por que aparecen estados mixtos

En presencia de ruido o de subsistemas no observados, la descripcion por vectores de estado deja de ser suficiente. Por eso los canales cuanticos se expresan de forma natural actuando sobre matrices de densidad:

$$
\rho \mapsto \mathcal{E}(\rho).
$$

Ese cambio de perspectiva es muy importante: ya no seguimos solo amplitudes, sino tambien mezcla, perdida de coherencia y efectos efectivos del entorno.

## 4. Propiedades esenciales

Sin entrar aun en toda la teoria formal, un canal cuantico debe preservar lo que hace fisicamente interpretable al estado:

- positividad;
- traza;
- consistencia al extender el sistema.

En un curso introductorio no hace falta demostrarlo todo, pero si conviene dejar claro que no cualquier transformacion lineal sirve.

## 5. Valor dentro del proyecto

Este modulo conecta de forma muy natural con:

- matrices de densidad;
- decoherencia;
- noise models;
- mitigacion de errores;
- y simulacion mas realista en Qiskit.

## 6. Ejercicios sugeridos

1. Explica por que una evolucion unitaria ideal no basta para describir un sistema abierto.
2. Relaciona la necesidad de canales cuanticos con la aparicion de estados mixtos.
3. Describe un ejemplo intuitivo de proceso ruidoso que no pueda verse como una unica unitaria sobre el sistema aislado.

## 7. Material asociado

- Cuaderno: [14_densitymatrix_y_estado_mixto.ipynb](../../Cuadernos/ejemplos/14_densitymatrix_y_estado_mixto.ipynb)
- Cuaderno: [25_canales_de_ruido_y_kraus.ipynb](../../Cuadernos/ejemplos/25_canales_de_ruido_y_kraus.ipynb)
- Articulo relacionado: [Matrices de densidad y estados mixtos](../08_informacion_cuantica/01_matrices_de_densidad_y_estados_mixtos.md)
- Articulo relacionado: [Decoherencia y ruido](../06_ruido_y_hardware/01_decoherencia_y_ruido.md)

## Navegacion

- Anterior: [Evolucion unitaria y Trotterizacion](../15_hamiltonianos_y_evolucion_temporal/02_evolucion_unitaria_y_trotterizacion.md)
- Siguiente: [Operadores de Kraus, decoherencia y modelos efectivos](02_kraus_decoherencia_y_modelos_efectivos.md)
