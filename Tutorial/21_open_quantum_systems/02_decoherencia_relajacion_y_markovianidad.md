# Decoherencia, relajacion y markovianidad

## Prerequisitos

- Canales cuanticos.
- Fidelidad y ruido.
- Idea minima de sistemas abiertos.

## Objetivos

- distinguir decoherencia y relajacion;
- introducir la intuicion de markovianidad;
- conectar estas ideas con hardware y caracterizacion.

## 1. Decoherencia frente a relajacion

Aunque a veces se mezclan en una misma intuicion informal, no son exactamente lo mismo.

- la decoherencia se relaciona con la perdida de fase y de capacidad de interferencia;
- la relajacion se asocia mas directamente al intercambio de energia con el entorno.

## 2. Markovianidad

En un nivel introductorio, la palabra `markoviano` sugiere que la evolucion efectiva no retiene memoria detallada del pasado del sistema. No hace falta formalizarlo demasiado aqui, pero si conviene dejar clara la intuicion: algunos modelos efectivos suponen memoria corta o despreciable del entorno.

## 3. Por que importa

Estas ideas importan porque ayudan a interpretar mejor:

- tiempos caracteristicos del hardware;
- modelos efectivos de ruido;
- limites de ciertos esquemas de mitigacion;
- y diferencias entre idealizacion teorica y dispositivo real.

Tambien ayudan a leer con mas madurez conceptos que aparecen mucho en hardware cuantico, como tiempos caracteristicos, deterioro progresivo del estado y diferencias entre perdida de poblacion y perdida de coherencia.

## 4. Errores comunes

- usar decoherencia y relajacion como sinonimos perfectos;
- pensar que toda dinamica abierta tiene memoria irrelevante;
- olvidar que el modelo efectivo elegido ya incorpora hipotesis fisicas.

## 5. Ejercicios sugeridos

1. Explica una diferencia intuitiva entre decoherencia y relajacion.
2. Relaciona markovianidad con la idea de memoria del entorno.
3. Describe por que este bloque ayuda a interpretar mejor el hardware cuantico.

## 6. Material asociado

- Cuaderno: [32_open_systems_intuicion.ipynb](../../Cuadernos/ejemplos/32_open_systems_intuicion.ipynb)
- Cuaderno: [31_fidelidad_antes_y_despues_de_ruido.ipynb](../../Cuadernos/ejemplos/31_fidelidad_antes_y_despues_de_ruido.ipynb)
- Cuaderno: [33_shots_y_estadistica_de_medicion.ipynb](../../Cuadernos/ejemplos/33_shots_y_estadistica_de_medicion.ipynb)
- Laboratorio: [15_noise_vs_fidelity_guiada.ipynb](../../Cuadernos/laboratorios/15_noise_vs_fidelity_guiada.ipynb)

## Navegacion

- Anterior: [Lindblad y dinamica efectiva](01_lindblad_y_dinamica_efectiva.md)
- Siguiente: [Coherencia, entrelazamiento y utilidad](../22_recursos_cuanticos/01_coherencia_entrelazamiento_y_utilidad.md)
