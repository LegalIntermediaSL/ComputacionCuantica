# Surface codes: intuición y estructura

## 1. Por qué la corrección de errores requiere algo más que redundancia

Los códigos de corrección de errores clásicos codifican información redundantemente: repetir un bit tres veces y votar. Para qubits, el teorema de no-clonación impide esta estrategia directa: no se puede copiar un estado cuántico desconocido.

La solución cuántica codifica la información lógica en correlaciones entre muchos qubits físicos, de forma que el error en cualquier qubit individual puede detectarse y corregirse **sin revelar el estado lógico**. Los **surface codes** son la arquitectura de corrección de errores más prometedora para hardware superconductor, por su umbral de error relativamente alto y su compatibilidad con la conectividad local de los chips.

## 2. La retícula bidimensional

Un surface code de distancia $d$ organiza $d^2 + (d-1)^2$ qubits en una retícula 2D con dos tipos de qubits:

- **Qubits de datos:** forman el soporte de la información lógica.
- **Qubits ancilla (de síndrome):** se usan para medir los síndromes sin perturbar la información lógica. Se dividen en ancillas-X (para detectar bit-flips) y ancillas-Z (para detectar phase-flips).

El patrón de conexión forma un tablero de ajedrez donde cada ancilla está conectada a sus cuatro vecinos de datos.

Para $d = 3$ (el surface code más pequeño útil):
- 9 qubits de datos
- 4 ancillas-Z y 4 ancillas-X
- Total: 17 qubits físicos para 1 qubit lógico

## 3. Operadores de estabilizadores

El surface code está definido por un **grupo de estabilizadores**: operadores $S_i$ que conmutan mutuamente y satisfacen $S_i |\psi_L\rangle = +|\psi_L\rangle$ para cualquier estado lógico $|\psi_L\rangle$.

Los estabilizadores tienen dos tipos:

**Estabilizadores-X** (detectan bit-flips en los qubits de datos):

$$
S_X^{(v)} = \prod_{j \in \partial(v)} X_j
$$

**Estabilizadores-Z** (detectan phase-flips):

$$
S_Z^{(f)} = \prod_{j \in \partial(f)} Z_j
$$

donde $\partial(v)$ denota los qubits de datos adyacentes al vértice $v$ (o cara $f$).

Cuando un error actúa sobre el sistema, alguno de estos estabilizadores cambia su valor de $+1$ a $-1$. El patrón de estabilizadores violados se denomina **síndrome del error**.

## 4. Detección y corrección de errores

El ciclo de corrección del surface code opera de forma continua:

1. **Medición de síndromes:** medir todos los ancillas-X y ancillas-Z.
2. **Decodificación:** un algoritmo clásico (decodificador) recibe el síndrome (el patrón de ancillas con valor $-1$) e infiere la cadena de errores más probable.
3. **Corrección:** aplicar las puertas correctoras sobre los qubits de datos.

Los errores individuales producen síndromes que forman **pares** de ancillas excitadas. El decodificador encuentra el emparejamiento de mínimo peso que explica el síndrome (problema de **Minimum Weight Perfect Matching, MWPM**).

Los errores no se propagan catastróficamente si la tasa de error física por puerta está por debajo del **umbral de error** del código.

## 5. Umbral de error y distancia

El **umbral de error** del surface code es $\sim 1\%$ de probabilidad de error por puerta (en el mejor caso con decodificadores ideales). Por debajo de este umbral, aumentar la distancia $d$ reduce exponencialmente la tasa de error lógica:

$$
p_L \approx A \left(\frac{p}{p_\text{th}}\right)^{\lfloor (d+1)/2 \rfloor}
$$

donde $p$ es la tasa de error física y $p_\text{th}$ es el umbral.

Para lograr $p_L < 10^{-10}$ con $p = 0.1\%$ (hardware de alta calidad), se necesita $d \approx 17$, lo que implica $\sim 600$ qubits físicos por qubit lógico.

## 6. Operadores lógicos

Las puertas sobre el qubit lógico se implementan mediante cadenas de operadores que atraviesan la retícula:

- **$\bar{X}_L$**: cadena de puertas $X$ que conecta un borde a otro borde en la dirección horizontal.
- **$\bar{Z}_L$**: cadena de puertas $Z$ en la dirección vertical.

Estas cadenas conmutan con todos los estabilizadores pero no entre sí, lo que las convierte en los verdaderos operadores lógicos del código.

## 7. Ideas clave

- El surface code codifica 1 qubit lógico en $\sim d^2$ qubits físicos usando correlaciones en una retícula 2D.
- Los síndromes de error se miden midiendo ancillas sin destruir la información lógica.
- El decodificador MWPM infiere la corrección más probable a partir del síndrome.
- Por debajo del umbral de error ($\sim 1\%$), aumentar la distancia $d$ reduce exponencialmente la tasa de error lógica.
- Los operadores lógicos son cadenas de Pauli que atraviesan la retícula de borde a borde.

## 8. Ejercicios sugeridos

1. Dibujar la retícula de un surface code $d = 3$ con los 9 qubits de datos y 8 ancillas, marcando los estabilizadores-X y estabilizadores-Z.
2. Para un error $X$ en el qubit central de la retícula $d = 3$, identificar qué ancillas-Z se excitan (cambian a $-1$).
3. Calcular cuántos qubits físicos se necesitan para un qubit lógico de distancia $d = 7$.
4. Estimar la tasa de error lógica para $d = 5$ si la tasa de error física por puerta es $p = 0.5\%$.

## Navegacion

- Anterior: [Codigo de Shor: intuicion](../09_correccion_errores/02_codigo_de_shor_intuicion.md)
- Siguiente: [Fault tolerance como horizonte](02_fault_tolerance_como_horizonte.md)
