# Proyectores, valores esperados y varianza

## 1. Mas alla de leer `0` o `1`

En un primer contacto con la computacion cuantica, medir parece equivalente a leer un bit clasico al final del circuito. Pero esa imagen es demasiado pobre para describir buena parte de la teoria y de las aplicaciones.

Cuando medimos en una base ortonormal, cada posible resultado esta asociado a un proyector. Para una base $\{|a_i\rangle\}$, escribimos

$$
P_i = |a_i\rangle \langle a_i|.
$$

La probabilidad de obtener el resultado $i$ en el estado $|\psi\rangle$ es

$$
p_i = \langle \psi | P_i | \psi \rangle.
$$

## 2. Observables y descomposicion espectral

Un observable hermitico puede escribirse como

$$
A = \sum_i a_i P_i,
$$

donde los $a_i$ son autovalores y los $P_i$ los proyectores asociados.

Esta expresion deja claro algo fundamental: medir un observable no es un acto misterioso separado de la estructura matematica del sistema, sino una forma de organizar probabilidades y resultados posibles.

## 3. Valor esperado

El valor esperado de $A$ en el estado $|\psi\rangle$ es

$$
\langle A \rangle = \langle \psi | A | \psi \rangle.
$$

No debe interpretarse como “el resultado seguro” de una unica medicion, sino como el promedio teorico de muchas repeticiones. Esa idea es exactamente la que reaparece cuando usamos `Estimator` con un Hamiltoniano.

## 4. Varianza y dispersion

No basta con saber el valor esperado. Tambien interesa cuan dispersos estan los resultados. Para eso usamos la varianza:

$$
\mathrm{Var}(A) = \langle A^2 \rangle - \langle A \rangle^2.
$$

Esta cantidad mide la anchura de la distribucion de resultados asociada al observable.

Pedagogicamente es importante porque muestra que dos estados pueden tener el mismo valor esperado para un observable y, sin embargo, comportarse de forma distinta al mirar la fluctuacion.

## 5. Por que este bloque importa en el curso

Este articulo sirve de puente entre:

- medicion elemental;
- observables y Hamiltonianos;
- `Estimator`;
- informacion cuantica;
- y una comprension menos ingenua del significado de medir.

## 6. Ejercicios sugeridos

1. Calcula el valor esperado y la varianza de $Z$ en los estados $|0\rangle$, $|1\rangle$ y $|+\rangle$.
2. Explica por que medir un observable en su autoestado produce varianza nula.
3. Relaciona proyectores con probabilidades de resultados.

## 7. Material asociado

- Cuaderno: [24_observables_y_valores_esperados.ipynb](../../Cuadernos/ejemplos/24_observables_y_valores_esperados.ipynb)
- Cuaderno: [26_estimator_y_hamiltonianos_sencillos.ipynb](../../Cuadernos/ejemplos/26_estimator_y_hamiltonianos_sencillos.ipynb)
- Solucion relacionada: [soluciones_avanzadas_seleccionadas.md](../../Soluciones/soluciones_avanzadas_seleccionadas.md)
- Articulo relacionado: [Observables y Hamiltonianos](../15_hamiltonianos_y_evolucion_temporal/01_observables_y_hamiltonianos.md)

## Navegacion

- Anterior: [Operadores de Kraus, decoherencia y modelos efectivos](../16_canales_cuanticos_y_ruido/02_kraus_decoherencia_y_modelos_efectivos.md)
- Siguiente: [POVM: intuicion y medicion generalizada](02_povm_intuicion_y_medicion_generalizada.md)
