# Operadores de Kraus, decoherencia y modelos efectivos

## 1. Representacion de Kraus

Una forma muy util de escribir un canal cuantico es mediante operadores de Kraus:

$$
\mathcal{E}(\rho) = \sum_k E_k \rho E_k^\dagger,
$$

con la condicion

$$
\sum_k E_k^\dagger E_k = I.
$$

Esta representacion es importante porque permite modelar ruido de forma compacta y con interpretacion operativa.

## 2. Ejemplos tipicos

Entre los canales introductorios mas importantes estan:

- dephasing o perdida de coherencia de fase;
- bit-flip;
- amplitude damping;
- depolarizing channel.

Cada uno captura una familia distinta de deterioros fisicos. No son solo “errores abstractos”: representan mecanismos efectivos por los que la informacion cuantica deja de comportarse como en el simulador ideal.

## 3. Decoherencia como perdida de estructura cuantica

La decoherencia puede entenderse como la desaparicion progresiva de las componentes fuera de la diagonal en cierta base relevante. Eso no significa necesariamente destruccion total del estado, pero si perdida de la interferencia que hacia util el recurso cuantico.

En ese sentido, el paso de

$$
\rho =
\begin{pmatrix}
\rho_{00} & \rho_{01} \\
\rho_{10} & \rho_{11}
\end{pmatrix}
$$

a una version con terminos no diagonales mas pequeños ilustra bien la intuicion.

## 4. Relacion con modelos de ruido en Qiskit

Cuando en Qiskit hablamos de `noise models`, estamos usando de forma computacional una parte de esta idea: describir procesos efectivos que alteran la ejecucion ideal del circuito.

Esto enlaza muy bien con:

- simulacion ruidosa;
- fidelidad;
- mitigacion de errores;
- y la necesidad posterior de correccion de errores.

## 5. Por que este bloque mejora el tutorial

Hasta aqui, el proyecto ya hablaba de ruido, pero aun faltaba una capa intermedia entre intuicion fisica y formalismo util. Este modulo llena ese hueco:

- conecta ruido con matrices de densidad;
- conecta decoherencia con canales;
- conecta teoria con implementacion y simulacion;
- y prepara mejor el paso a hardware realista.

## 6. Ejercicios sugeridos

1. Explica con tus palabras la condicion $\sum_k E_k^\dagger E_k = I$.
2. Compara intuitivamente dephasing y amplitude damping.
3. Describe por que la perdida de coherencia es especialmente dañina para la interferencia.
4. Relaciona canales de ruido con la diferencia entre simulacion ideal y simulacion realista.

## 7. Material asociado

- Cuaderno: [20_noise_model_conceptual.ipynb](../../Cuadernos/ejemplos/20_noise_model_conceptual.ipynb)
- Cuaderno: [23_ideal_vs_ruidoso_conceptual.ipynb](../../Cuadernos/ejemplos/23_ideal_vs_ruidoso_conceptual.ipynb)
- Cuaderno: [25_canales_de_ruido_y_kraus.ipynb](../../Cuadernos/ejemplos/25_canales_de_ruido_y_kraus.ipynb)
- Articulo relacionado: [Noise models y simulacion realista](../10_qiskit_avanzado/03_noise_models_y_simulacion_realista.md)

## Navegacion

- Anterior: [Canales cuanticos: intuicion y representacion](01_canales_cuanticos_intuicion_y_representacion.md)
- Siguiente: [Proyectores, valores esperados y varianza](../17_medicion_avanzada_y_observables/01_proyectores_valores_esperados_y_varianza.md)
