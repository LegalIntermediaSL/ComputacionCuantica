# Introducción al control por microondas

## 1. Del qubit abstracto al qubit físico

En los capítulos anteriores describimos las puertas cuánticas como matrices unitarias. Pero un procesador superconductor solo "entiende" señales de microondas: pulsos de voltaje a 4-6 GHz enviados a través de cables coaxiales criogénicos hasta el chip. La capa de **control de pulsos** es el puente entre la abstracción matemática y la electrónica real.

Comprender este nivel permite calibrar qubits, diseñar puertas de menor duración, estudiar fuentes de error y ejecutar operaciones que no están disponibles en el conjunto de puertas nativas del compilador.

## 2. La frecuencia de resonancia del qubit

Un transmón tiene una frecuencia de transición $\omega_q/2\pi \sim 4$-$6\,\text{GHz}$ entre $|0\rangle$ y $|1\rangle$. Si aplicamos una señal de microondas exactamente a $\omega_q$, la población del qubit oscila sinusoidalmente: son las **oscilaciones de Rabi**.

Para un pulso de amplitud constante $\Omega_0$ durante el tiempo $t$, el ángulo de rotación en la esfera de Bloch es:

$$
\theta = \Omega_0 \cdot t
$$

Una puerta $X$ ($\pi$-pulso) requiere $\theta = \pi$: $t_\pi = \pi/\Omega_0$.

Para $\Omega_0/2\pi = 20\,\text{MHz}$: $t_\pi = \pi/(2\pi \times 20\,\text{MHz}) = 25\,\text{ns}$.

## 3. El marco rotatorio

Un qubit libre precesa alrededor del eje $Z$ de la esfera de Bloch a $\omega_q$. En el **laboratorio**, el estado $|+\rangle$ rotaría miles de veces durante el tiempo de un pulso, haciendo el control difícil de visualizar.

La solución es trabajar en el **marco rotatorio** que gira a la frecuencia del drive $\omega_d$. En este marco, el vector de estado parece estático si $\omega_d = \omega_q$, y cualquier pulso aplicado produce una rotación lenta y controlable.

Matemáticamente, la transformación al marco rotatorio equivale a aplicar el operador:

$$
R(t) = e^{i\omega_d t Z/2}
$$

En el marco rotatorio, el Hamiltoniano del qubit libre ($H = \hbar\omega_q Z/2$) se reduce a un **detuning**:

$$
H_\text{rot} = \frac{\hbar\delta}{2}Z, \quad \delta = \omega_q - \omega_d
$$

Si $\delta = 0$ (drive en resonancia): el qubit está estático en el marco rotatorio hasta que se aplica un pulso.

## 4. El Hamiltoniano de drive

Cuando aplicamos una señal de microondas

$$
s(t) = a(t)\cos(\omega_d t + \phi_0)
$$

(donde $a(t)$ es la envolvente y $\phi_0$ la fase inicial), el Hamiltoniano de interacción efectivo en el marco rotatorio es:

$$
H_\text{ctrl}(t) = \frac{\hbar\Omega(t)}{2}[\cos(\phi)X + \sin(\phi)Y]
$$

donde $\Omega(t) \propto a(t)$ es la Frecuencia de Rabi instanánea y $\phi$ es la fase del drive. Esto significa:
- $\phi = 0$: rotación alrededor del eje $X$ ($R_x$).
- $\phi = \pi/2$: rotación alrededor del eje $Y$ ($R_y$).
- Las puertas $R_z(\theta)$ se implementan **virtualmente** como cambios de la fase de referencia del generador (no requieren pulso físico).

## 5. Mezclador IQ y generación de señales

El hardware de control usa un **mezclador IQ** para generar las señales de microondas. La señal de salida es:

$$
s(t) = I(t)\cos(\omega_\text{LO}t) - Q(t)\sin(\omega_\text{LO}t)
$$

donde $\omega_\text{LO}$ es la frecuencia del oscilador local (LO) y $I(t)$, $Q(t)$ son las componentes en fase y en cuadratura que el sistema de control digital (AWG, Arbitrary Waveform Generator) genera. Cambiando $I(t)$ y $Q(t)$:

- **Amplitud:** $A = \sqrt{I^2 + Q^2}$.
- **Fase:** $\phi = \arctan(Q/I)$.

Para implementar $R_x(\theta)$: enviar un pulso gaussiano con $Q = 0$.
Para implementar $R_y(\theta)$: enviar el mismo pulso con $I = 0$.

## 6. Envolventes de pulso: Gaussiana y DRAG

La elección de la envolvente $a(t)$ afecta directamente la fidelidad de la puerta.

**Pulso cuadrado (rectangular):** el más simple, pero tiene componentes espectrales de alta frecuencia que pueden excitar el nivel $|2\rangle$ del transmón (fuga).

**Pulso gaussiano:** $a(t) = A\exp\left(-\frac{(t-t_0)^2}{2\sigma^2}\right)$. La anchura espectral es $\Delta\omega \approx 1/\sigma$, y si $\sigma > 1/|\alpha|$ (donde $\alpha$ es la anharmonicidad), la fuga es suprimida.

**DRAG (Derivative Removal via Adiabatic Gate):** corrección que añade una componente en cuadratura proporcional a la derivada de la envolvente:

$$
I(t) = a(t), \quad Q(t) = -\frac{\lambda}{\alpha}\dot{a}(t)
$$

donde $\lambda$ es un parámetro ajustable. DRAG cancela la transición $|1\rangle \to |2\rangle$ de primer orden, permitiendo pulsos más cortos (menor $\sigma$) con la misma fidelidad. Es el estándar en los procesadores de IBM y Google.

## 7. El experimento de Rabi: calibración de la amplitud

El experimento más básico de control de pulsos es la **oscilación de Rabi**:

1. Preparar el qubit en $|0\rangle$.
2. Aplicar un pulso de amplitud $A$ y medir $P(1)$.
3. Repetir para distintas amplitudes $A$.

La probabilidad de encontrar el qubit en $|1\rangle$ oscila como:

$$
P(1) = \sin^2\left(\frac{\Omega_0 A \cdot t}{2}\right)
$$

El valor de $A$ que maximiza $P(1) = 1$ corresponde al pulso $\pi$ (puerta $X$). Este experimento calibra la amplitud necesaria para cada qubit del procesador.

```python
import numpy as np
import matplotlib.pyplot as plt

# Simulación analítica de oscilaciones de Rabi
t_total = 200e-9  # 200 ns
amplitudes = np.linspace(0, 1, 100)
omega_rabi = 2 * np.pi * 20e6  # 20 MHz

P1 = np.sin(omega_rabi * t_total * amplitudes / 2)**2

pi_amp = amplitudes[np.argmax(P1)]
print(f"Amplitud del pulso π: {pi_amp:.3f} (normalizada)")
print(f"Tiempo de puerta X: {t_total*1e9:.0f} ns")
```

## 8. Detuning y experimento de Ramsey

Si el drive no está exactamente en resonancia ($\delta \neq 0$), el qubit precesa alrededor del eje $Z$ en el marco rotatorio. Esto permite medir $\omega_q$ con alta precisión mediante el **experimento de Ramsey**:

1. Aplicar un pulso $\pi/2$ ($R_x(\pi/2)$).
2. Esperar un tiempo libre $\tau$.
3. Aplicar otro pulso $\pi/2$.
4. Medir.

Si hay detuning $\delta$, el qubit precesa durante $\tau$ y la probabilidad oscila como:

$$
P(1) = \frac{1}{2}(1 - \cos(\delta\tau))
$$

La frecuencia de oscilación da $\delta$ directamente. El Ramsey también mide $T_2^*$ a partir del decaimiento de la oscilación.

## 9. Ideas clave

- Las puertas cuánticas son pulsos de microondas: la amplitud controla el ángulo de rotación, la fase controla el eje.
- En el marco rotatorio, el drive en resonancia produce rotaciones lentas y controlables; el detuning introduce una precesión en $Z$.
- Las puertas $R_z$ se implementan virtualmente cambiando la fase de referencia del generador, sin coste de tiempo.
- Las envolventes DRAG suprimen la fuga al nivel $|2\rangle$, permitiendo puertas más rápidas y de mayor fidelidad.
- El experimento de Rabi calibra la amplitud del pulso $\pi$; el experimento de Ramsey mide la frecuencia de transición y $T_2^*$.

## 10. Ejercicios sugeridos

1. Calcular la anchura espectral $\Delta\omega$ de un pulso gaussiano con $\sigma = 10\,\text{ns}$ y compararla con la anharmonicidad del transmón ($\alpha/2\pi = -250\,\text{MHz}$).
2. Simular la evolución de un qubit bajo un pulso cuadrado fuera de resonancia (detuning $\delta = 2\pi \times 5\,\text{MHz}$) durante $50\,\text{ns}$.
3. Estimar qué amplitud máxima puede usar un pulso rectangular sin envolvente para limitar la fuga al nivel $|2\rangle$ por debajo del $0.1\%$.
4. Implementar el experimento de Ramsey en Qiskit y extraer $T_2^*$ del decaimiento de la oscilación.

## Navegación

- Anterior: [Iones atrapados y otras arquitecturas](../23_hardware_fisico_y_arquitecturas/02_iones_atrapados_y_otras_arquitecturas.md)
- Siguiente: [Programación de pulsos con Qiskit Pulse](02_programacion_de_pulsos_con_qiskit_pulse.md)
