# Transmones y Circuitos Superconductores

En los capítulos anteriores hemos tratado a los qubits como sistemas abstractos de dos niveles. Sin embargo, para construir una computadora cuántica real, necesitamos un objeto físico que se comporte de forma cuántica. La arquitectura de **circuitos superconductores** (utilizada por IBM, Google y Rigetti) utiliza corrientes eléctricas sin resistencia.

## La Unión de Josephson como Inductor No Lineal

Un circuito $LC$ estándar (inductor y condensador) es un oscilador armónico cuántico. Sus niveles de energía están equiespaciados: $E_n = \hbar \omega (n + 1/2)$. Esto es un problema para la computación cuántica: si aplicamos un pulso para pasar del nivel $|0\rangle$ al $|1\rangle$, corremos el riesgo de saltar al $|2\rangle$ accidentalmente.

La **Unión de Josephson** es el componente crítico que introduce **anharmonicidad**. Consiste en dos superconductores separados por una capa aislante delgadísima. Su relación corriente-fase es no lineal:
$$ I = I_c \sin(\delta) $$
Esto convierte al circuito en un péndulo cuántico, donde los niveles de energía ya no son equidistantes. El **Transmón** es una variante diseñada para ser insensible al ruido de carga, manteniendo una anharmonicidad suficiente para aislar los estados $|0\rangle$ y $|1\rangle$.

## El Hamiltoniano del Transmón

El Hamiltoniano simplificado se puede aproximar por el modelo de un oscilador Duffing:
$$ H = \hbar \omega_q a^\dagger a + \frac{\alpha}{2} a^\dagger a^\dagger a a $$
Donde:
- $\omega_q$ es la frecuencia de transición $0 \to 1$.
- $\alpha = E_{12} - E_{01}$ es la **anharmonicidad**. En transmones típicos, $\alpha \approx -200$ a $-300$ MHz.

## Acoplamiento: Circuit QED

Para leer el estado del transmón sin destruirlo, se acopla a una **cavidad resonadora** (un bus de microondas). El sistema se describe mediante el Hamiltoniano de Jaynes-Cummings:
$$ H = \omega_r b^\dagger b + \frac{\omega_q}{2} Z + g(a^\dagger \sigma_- + a \sigma_+) $$
En el régimen dispersivo ($|\omega_q - \omega_r| \gg g$), la frecuencia de la cavidad se desplaza dependiendo de si el qubit está en $|0\rangle$ o $|1\rangle$. Midiendo el desfase de un pulso de microondas que rebota en la cavidad, determinamos el estado del qubit.

## Navegación
- Anterior: [No-clonación y límites operacionales](../22_recursos_cuanticos/02_no_clonacion_y_limites_operacionales.md)
- Siguiente: [Iones atrapados y otras arquitecturas](02_iones_atrapados_y_otras_arquitecturas.md)
