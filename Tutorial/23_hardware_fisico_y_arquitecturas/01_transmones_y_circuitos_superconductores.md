# Transmones y circuitos superconductores

## 1. El qubit como sistema físico

Hasta ahora hemos tratado a los qubits como sistemas abstractos de dos niveles. Para construir una computadora cuántica real, necesitamos un objeto físico que se comporte de forma cuántica a la escala del qubit individual. La arquitectura de **circuitos superconductores** —utilizada por IBM, Google, Rigetti y otros— usa corrientes eléctricas sin resistencia para crear osciladores cuánticos controlables con señales de microondas.

El principio básico: si enfriamos un circuito $LC$ superconductor a temperaturas de milikelvin ($T \sim 10$-$20\,\text{mK}$), los electrones forman pares de Cooper y el circuito exhibe cuantización de energía. El reto es que un oscilador armónico tiene niveles igualmente espaciados y no sirve como qubit: no podemos aislar únicamente los estados $|0\rangle$ y $|1\rangle$.

## 2. La unión de Josephson como inductor no lineal

La **unión de Josephson** resuelve el problema de los niveles igualmente espaciados. Consiste en dos superconductores separados por una capa aislante delgadísima ($\sim 1$-$2\,\text{nm}$). La corriente a través de la unión sigue la relación no lineal:

$$
I = I_c \sin(\delta)
$$

donde $\delta$ es la diferencia de fase de la función de onda superconductora entre los dos lados e $I_c$ es la corriente crítica. Esta no-linealidad hace que la energía potencial no sea cuadrática, rompiendo la degeneración de los niveles. El sistema se convierte en un **péndulo cuántico** con niveles de energía no igualmente espaciados.

La energía de la unión de Josephson es:

$$
E_J = -E_J \cos(\delta), \quad E_J = \frac{\hbar I_c}{2e}
$$

En paralelo con la capacitancia $C$ del circuito, el Hamiltoniano del sistema es:

$$
H = 4E_C(n - n_g)^2 - E_J\cos(\delta)
$$

donde $n$ es el número de pares de Cooper en la isla, $n_g$ es la polarización de carga (offset de carga) y $E_C = e^2/2C$ es la energía de carga.

## 3. El transmón: régimen $E_J \gg E_C$

El régimen de **transmón** ($E_J/E_C \sim 50$-$100$) es el más usado porque minimiza la sensibilidad al ruido de carga. En este régimen, los niveles de energía se pueden aproximar con un modelo de oscilador de Duffing:

$$
H \approx \hbar\omega_q a^\dagger a + \frac{\alpha}{2}a^\dagger a^\dagger aa
$$

donde:
- $\omega_q \approx \sqrt{8E_JE_C}/\hbar - E_C/\hbar$ es la frecuencia de transición $|0\rangle \to |1\rangle$ (típicamente 4-6 GHz).
- $\alpha = E_{12} - E_{01} \approx -E_C/\hbar$ es la **anharmonicidad** (típicamente $\alpha \approx -200$ a $-300\,\text{MHz}$).

La anharmonicidad es la clave: permite aplicar pulsos de microondas a frecuencia $\omega_q$ que solo excitan la transición $|0\rangle \to |1\rangle$ sin poblar inadvertidamente el nivel $|2\rangle$.

## 4. Lectura dispersiva: Circuit QED

Para leer el estado del qubit sin destruirlo (medición cuántica no demoledora), el transmón se acopla a una **cavidad resonadora** (un resonador de microondas coplanares con frecuencia $\omega_r \sim 6$-$8\,\text{GHz}$). El sistema completo se describe por el Hamiltoniano de Jaynes-Cummings:

$$
H = \hbar\omega_r b^\dagger b + \frac{\hbar\omega_q}{2}Z + \hbar g(a^\dagger\sigma_- + a\sigma_+)
$$

donde $g$ es la constante de acoplamiento qubit-cavidad (típicamente $g \sim 50$-$200\,\text{MHz}$).

En el **régimen dispersivo** ($|\Delta| = |\omega_q - \omega_r| \gg g$), la frecuencia efectiva de la cavidad depende del estado del qubit:

$$
H_\text{disp} \approx \hbar(\omega_r + \chi\, Z)b^\dagger b + \frac{\hbar\tilde{\omega}_q}{2}Z
$$

donde $\chi = g^2/\Delta$ es el desplazamiento dispersivo. Enviando un pulso de microondas a la cavidad y midiendo la fase de la señal reflejada, determinamos el estado del qubit:

- Si el qubit está en $|0\rangle$: la cavidad resuena a $\omega_r + \chi$.
- Si el qubit está en $|1\rangle$: la cavidad resuena a $\omega_r - \chi$.

La diferencia de fase entre ambos casos es $2\chi/\kappa$ (con $\kappa$ la tasa de decaimiento de la cavidad), que debe ser suficientemente grande para discriminar los estados.

## 5. Puertas de un qubit: pulsos de microondas

Las puertas de un qubit se implementan aplicando pulsos de microondas en resonancia con $\omega_q$. En el **marco rotatorio** a $\omega_q$, el Hamiltoniano de control es:

$$
H_\text{ctrl}(t) = \frac{\hbar\Omega(t)}{2}[\cos(\phi)X + \sin(\phi)Y]
$$

donde $\Omega(t)$ es la envolvente del pulso y $\phi$ su fase:
- $\phi = 0$: rotación alrededor de $X$ (puerta $R_x(\theta)$).
- $\phi = \pi/2$: rotación alrededor de $Y$ (puerta $R_y(\theta)$).
- Ajustando la fase del generador de microondas: puerta $R_z(\theta)$ virtual (cambio de marco).

Las envolventes Gaussianas o DRAG (Derivative Removal via Adiabatic Gate) suprimen la fuga hacia el nivel $|2\rangle$ mejorando la fidelidad de puerta.

## 6. Puertas de dos qubits: Cross-Resonance y $i\text{SWAP}$

Para operar entre qubits vecinos existen dos mecanismos principales:

**Cross-Resonance (CR):** se aplica un pulso en el qubit de control a la frecuencia del qubit objetivo. En hardware IBM, esto implementa un CNOT con fidelidades $>99\%$ y tiempos $\sim 200$-$500\,\text{ns}$.

**iSWAP:** se activa el acoplamiento capacitivo entre qubits vecinos de forma pulsada. Usado en Google Sycamore y Rigetti. La puerta nativa es la $\sqrt{i\text{SWAP}}$ con fidelidades similares.

## 7. Tiempos de coherencia y fuentes de ruido

| Parámetro | Valor típico (2024) | Limitado por |
|---|---|---|
| $T_1$ | 100-500 μs | Radiación espontánea, two-level systems (TLS) |
| $T_2^*$ | 50-200 μs | Ruido de flujo $1/f$, ruido de carga |
| $T_2^E$ | 100-400 μs | Tras Hahn echo |
| Fidelidad X,H | >99.9% | Ruido de control, fugas a $|2\rangle$ |
| Fidelidad CNOT | 99-99.9% | Cross-talk, error dispersivo |
| Tiempo de medición | 0.5-2 μs | Ancho de banda de la cavidad |

Las principales fuentes de decoherencia en transmones son:
- **Two-level systems (TLS):** defectos en las interfaces de los materiales que absorben y emiten energía.
- **Ruido de flujo $1/f$:** fluctuaciones de campo magnético en las uniones Josephson.
- **Radiación del entorno:** fugas de fotones hacia las líneas de control.

## 8. Arquitecturas: chips y conectividad

Los procesadores superconductores actuales organizan los transmones en rejillas 2D con conectividad a primeros vecinos:

- **IBM Eagle (127 qubits), Osprey (433), Condor (1121):** topología en rejilla hexagonal.
- **Google Sycamore (53-70 qubits):** rejilla cuadrada con conectividad cruzada.
- **Rigetti Ankaa (84 qubits):** rejilla octogonal para mayor conectividad.

La conectividad limitada implica que los algoritmos deben compilarse mediante ruteo (inserción de puertas SWAP) para ejecutar operaciones entre qubits no vecinos, aumentando el número total de puertas.

## 9. Ideas clave

- La unión de Josephson introduce anharmonicidad en el oscilador $LC$, permitiendo aislar los dos niveles más bajos como qubit.
- El transmón opera en el régimen $E_J \gg E_C$, que minimiza la sensibilidad al ruido de carga.
- La lectura dispersiva en Circuit QED permite medir el qubit sin destruirlo mediante el desplazamiento de la frecuencia de la cavidad.
- Las puertas de un qubit son pulsos de microondas en resonancia; las puertas de dos qubits usan el mecanismo Cross-Resonance o iSWAP.
- Los tiempos de coherencia (T1, T2 ~ 100-500 μs) y las fidelidades de puerta (CNOT > 99%) son los parámetros clave para la utilidad cuántica.

## 10. Ejercicios sugeridos

1. Calcular la anharmonicidad $\alpha$ en MHz para un transmón con $E_C/h = 300\,\text{MHz}$ y $E_J/E_C = 50$.
2. Estimar el desplazamiento dispersivo $\chi$ para $g = 100\,\text{MHz}$ y $\Delta = 1\,\text{GHz}$.
3. Comparar la duración de un CNOT por Cross-Resonance ($t \sim 300\,\text{ns}$) con $T_2 = 200\,\mu\text{s}$: ¿cuántas puertas CNOT caben en la ventana de coherencia?
4. Explicar por qué aumentar $E_J/E_C$ mejora la robustez frente al ruido de carga pero dificulta la anharmonicidad suficiente para el qubit.

## Navegación

- Anterior: [No-clonación y límites operacionales](../22_recursos_cuanticos/02_no_clonacion_y_limites_operacionales.md)
- Siguiente: [Iones atrapados y otras arquitecturas](02_iones_atrapados_y_otras_arquitecturas.md)
