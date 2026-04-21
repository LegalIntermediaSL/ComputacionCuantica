# Introducción al Control por Microondas

¿Cómo "habla" una computadora clásica con un qubit superconductor? La respuesta está en los pulsos de microondas.

## El Marco Rotatorio

Un qubit tiene una frecuencia de transición $\omega_q$ (normalmente entre 4 y 6 GHz). Si intentamos visualizar el vector de estado en la Esfera de Bloch, este rotaría alrededor del eje Z a esa velocidad vertiginosa. 
Para simplificar el control, trabajamos en el **marco rotatorio** a la frecuencia del drive $\omega_d$. Si $\omega_d = \omega_q$, el qubit parece "estático", y cualquier pulso aplicado causará una rotación lenta y controlada.

## Hamiltonianos de Drive

Cuando aplicamos una señal de microondas $s(t) = a(t) \cos(\omega_d t + \phi)$, el Hamiltoniano de interacción efectivo es:
$$ H_{int} = \frac{\hbar \Omega(t)}{2} [ \cos(\phi) X + \sin(\phi) Y ] $$
Donde $\Omega(t)$ es la amplitud de la envolvente del pulso. 
- Si $\phi = 0$, realizamos una rotación alrededor del eje **X**.
- Si $\phi = \pi/2$, realizamos una rotación alrededor del eje **Y**.

## Mezcla IQ y Envolventes

Para generar estas señales, se utiliza un mezclador IQ. La señal de salida es:
$$ I(t) \cos(\omega_d t) + Q(t) \sin(\omega_d t) $$
Cambiando los voltajes de los canales I (In-phase) y Q (Quadrature), podemos controlar tanto la fase como la amplitud del pulso cuántico. Las envolventes típicas son **Gaussianas** o **DRAG** (Derivative Removal by Adiabatic Gate) para minimizar fugas a niveles superiores.

## Navegación
- Anterior: [Iones atrapados y otras arquitecturas](../23_hardware_fisico_y_arquitecturas/02_iones_atrapados_y_otras_arquitecturas.md)
- Siguiente: [Programación de pulsos con Qiskit Pulse](02_programacion_de_pulsos_con_qiskit_pulse.md)
