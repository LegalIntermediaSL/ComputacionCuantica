# Resumen 07. Variacionales y aplicaciones

## Ideas clave

- los algoritmos variacionales mezclan preparacion cuantica y optimizacion clasica;
- VQE estima energias de Hamiltonianos;
- QAOA alterna operadores de coste y mezcla;
- las aplicaciones mas serias suelen aparecer en simulacion, optimizacion y quimica cuantica;
- la utilidad real depende de ruido, recursos y calidad de estimacion.

## Formulas minimas

$$
E(\theta) = \langle \psi(\theta) | H | \psi(\theta) \rangle
$$

## Errores comunes

- pensar que variar parametros siempre mejora automaticamente la solucion;
- olvidar que el coste de medir observables tambien importa;
- confundir una intuicion variacional bonita con una ventaja practica garantizada.

## Cuadernos recomendados

- [08_vqe_intuicion_guiada.ipynb](../Cuadernos/laboratorios/08_vqe_intuicion_guiada.ipynb)
- [09_qaoa_intuicion_guiada.ipynb](../Cuadernos/laboratorios/09_qaoa_intuicion_guiada.ipynb)
- [10_vqe_energy_scan.ipynb](../Cuadernos/laboratorios/10_vqe_energy_scan.ipynb)
- [11_qaoa_cost_landscape.ipynb](../Cuadernos/laboratorios/11_qaoa_cost_landscape.ipynb)
