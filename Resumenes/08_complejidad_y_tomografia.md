# Resumen 08. Complejidad y tomografia

## Ideas clave

- la ventaja cuantica debe expresarse en terminos de problemas, recursos y comparaciones honestas;
- `BQP` organiza la idea de computacion cuantica eficiente con error acotado;
- los oraculos ayudan a entender varios speedups introductorios;
- la tomografia reconstruye informacion sobre estados a partir de muchas mediciones;
- fidelidad y caracterizacion sirven para comparar estado ideal y estado preparado.

## Formulas minimas

$$
p_i = \langle \psi | P_i | \psi \rangle
$$

$$
p_i = \mathrm{Tr}(\rho E_i)
$$

## Errores comunes

- llamar ventaja cuantica a cualquier circuito interesante;
- creer que una sola medicion puede reconstruir un estado general;
- olvidar que la comparacion clasica correcta puede cambiar por completo la conclusion.

## Cuadernos recomendados

- [28_complejidad_y_bqp_intuicion.ipynb](../Cuadernos/ejemplos/28_complejidad_y_bqp_intuicion.ipynb)
- [29_tomografia_estado_intuicion.ipynb](../Cuadernos/ejemplos/29_tomografia_estado_intuicion.ipynb)
- [14_densitymatrix_ruido_y_tomografia_guiada.ipynb](../Cuadernos/laboratorios/14_densitymatrix_ruido_y_tomografia_guiada.ipynb)
