# Resumen 06. Hamiltonianos, ruido y medicion avanzada

## Ideas clave

- un observable es un operador hermitico;
- un Hamiltoniano organiza energia y evolucion temporal;
- un valor esperado no es un resultado individual, sino un promedio teorico;
- los canales cuanticos describen transformaciones efectivas sobre matrices de densidad;
- las POVM amplian la idea de medicion mas alla del caso proyectivo simple.

## Formulas minimas

$$
\langle A \rangle = \langle \psi | A | \psi \rangle
$$

$$
U(t) = e^{-iHt}
$$

$$
\mathcal{E}(\rho) = \sum_k E_k \rho E_k^\dagger
$$

$$
\sum_i E_i = I
$$

## Errores comunes

- confundir valor esperado con resultado seguro;
- pensar que todo ruido puede representarse como una unica unitaria sobre el sistema aislado;
- creer que toda medicion debe ser necesariamente proyectiva en una base ortonormal simple.

## Cuadernos recomendados

- [24_observables_y_valores_esperados.ipynb](../Cuadernos/ejemplos/24_observables_y_valores_esperados.ipynb)
- [25_canales_de_ruido_y_kraus.ipynb](../Cuadernos/ejemplos/25_canales_de_ruido_y_kraus.ipynb)
- [26_estimator_y_hamiltonianos_sencillos.ipynb](../Cuadernos/ejemplos/26_estimator_y_hamiltonianos_sencillos.ipynb)
- [13_estimator_y_energia_guiada.ipynb](../Cuadernos/laboratorios/13_estimator_y_energia_guiada.ipynb)
