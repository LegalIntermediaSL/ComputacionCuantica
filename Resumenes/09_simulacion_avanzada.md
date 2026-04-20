# Resumen 09. Simulacion cuantica avanzada

## Ideas clave

- simular un Hamiltoniano significa aproximar su evolucion con recursos finitos;
- las formulas de Trotter-Suzuki refinan la aproximacion elemental;
- mejor precision suele implicar mayor profundidad;
- la simulacion digital y la analogica responden a compromisos distintos.

## Formulas minimas

$$
U(t) = e^{-iHt}
$$

$$
e^{-i(A+B)t} \approx \left(e^{-iAt/n} e^{-iBt/n}\right)^n
$$

## Errores comunes

- pensar que precision y coste son independientes;
- identificar computacion cuantica solo con circuitos digitales;
- olvidar que el ruido puede destruir la utilidad de una aproximacion formalmente buena.

## Cuadernos recomendados

- [30_simulacion_hamiltoniana_intuicion.ipynb](../Cuadernos/ejemplos/30_simulacion_hamiltoniana_intuicion.ipynb)
- [16_trotter_suzuki_intuicion.ipynb](../Cuadernos/laboratorios/16_trotter_suzuki_intuicion.ipynb)
