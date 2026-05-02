# Módulo 46 — Átomos Neutros y Arrays de Rydberg

Los **átomos neutros atrapados** son hoy el paradigma cuántico con mayor número de qubits a escala global: QuEra anunció en 2024 un procesador de 10 000 átomos analógicos y 1 000 qubits lógicos tolerantes a fallos. Su física se basa en la interacción de van der Waals entre estados Rydberg altamente excitados, que genera puertas de 2 qubits con alta fidelidad y conectividad reconfigurable.

---

## Índice

1. [Trampas ópticas y tweezer arrays](#1-trampas)
2. [Interacción de Rydberg](#2-rydberg)
3. [Bloqueo de Rydberg — mecanismo de puerta CZ](#3-bloqueo)
4. [Hamiltoniano PXP y fases cuánticas](#4-pxp)
5. [Computación analógica vs digital](#5-analogica)
6. [QuEra Aquila — hardware y acceso](#6-quera)
7. [Pasqal Fresnel y otros fabricantes](#7-pasqal)
8. [Decoherencia y limitaciones actuales](#8-decoherencia)
9. [Casos de uso: optimización y simulación](#9-aplicaciones)
10. [Comparativa de plataformas](#10-comparativa)

---

## 1. Trampas Ópticas y Tweezer Arrays {#1-trampas}

### 1.1 Principio de la trampa óptica

Un átomo neutro con polarizabilidad $\alpha$ en un campo eléctrico oscilante $\mathbf{E}$ experimenta una fuerza de dipolo:

$$\mathbf{F} = \frac{\alpha}{2} \nabla |\mathbf{E}|^2$$

Un haz láser focalizado crea un pozo de potencial en el foco donde el átomo queda atrapado. Para un haz gaussiano de potencia $P$ y cintura $w_0$:

$$U(r, z) = -\frac{\alpha P}{\pi w^2(z)\epsilon_0 c} \exp\!\left(-\frac{2r^2}{w^2(z)}\right)$$

### 1.2 Tweezer arrays

Los **optical tweezer arrays** (Nogrette et al. 2014, Barredo et al. 2016) usan moduladores acusto-ópticos (AOD) o matrices de micro-lentes (SLM) para crear cientos o miles de trampas independientes en geometrías arbitrarias: cadenas 1D, redes 2D (cuadrada, triangular, kagome), grafos ad hoc.

Cada trampa captura un único átomo de $^{87}$Rb o $^{133}$Cs con eficiencia $\sim 50\%$ (llenado estocástico). Los átomos no cargados son insensibles al ruido electromagnético — $T_2^* \sim 1\text{--}10$ s en el estado base.

### 1.3 Qubit hiperfino

El qubit se codifica en dos niveles hiperfinos del estado base:
- $|0\rangle \equiv |F=1, m_F=0\rangle$
- $|1\rangle \equiv |F=2, m_F=0\rangle$

La transición "clock" a $\sim 6.8$ GHz es insensible al campo magnético en primer orden. La coherencia se puede extender con pulsos de eco y decodificación por simetría.

---

## 2. Interacción de Rydberg {#2-rydberg}

### 2.1 Estados de Rydberg

Los estados de Rydberg ($n \sim 50\text{--}100$) son estados atómicos con número cuántico principal $n$ muy alto. Sus propiedades escalan con $n$:

| Propiedad | Escalado | Valor típico ($n=70$) |
|---|---|---|
| Radio orbital | $n^2 a_0$ | $\sim 260$ nm |
| Tiempo de vida | $n^3$ | $\sim 100$ µs |
| Momento dipolar | $n^2 e a_0$ | $\sim 1000$ Debye |
| Coeficiente $C_6$ | $n^{11}$ | $\sim 10^{12}$ a.u. |

### 2.2 Potencial de van der Waals

Entre dos átomos de Rydberg separados una distancia $r$, la interacción dipolo-dipolo en el régimen de van der Waals da:

$$U(r) = \frac{C_6}{r^6}$$

Para $^{87}$Rb con $n=70$: $C_6 \approx 862\,000$ GHz·µm$^6$. A $r = 5$ µm: $U \approx 10$ MHz $\gg \Omega$ (frecuencia de Rabi típica $\sim 1$ MHz).

### 2.3 Hamiltoniano de Rydberg

Para un array de $N$ átomos con separaciones $r_{ij}$:

$$H = \frac{\hbar\Omega}{2}\sum_i \sigma_i^x - \hbar\Delta\sum_i n_i + \sum_{i<j} \frac{C_6}{r_{ij}^6} n_i n_j$$

donde:
- $\Omega$ = frecuencia de Rabi (amplitud del láser de excitación Rydberg)
- $\Delta$ = desintonización del láser respecto a la resonancia Rydberg
- $n_i = |r_i\rangle\langle r_i|$ = operador de ocupación Rydberg
- $\sigma_i^x = |g_i\rangle\langle r_i| + |r_i\rangle\langle g_i|$ = operador de volteo

---

## 3. Bloqueo de Rydberg — Mecanismo de Puerta CZ {#3-bloqueo}

### 3.1 El efecto de bloqueo

Cuando dos átomos están dentro del **radio de bloqueo**:

$$r_b = \left(\frac{C_6}{\hbar\Omega}\right)^{1/6}$$

la energía de interacción $U(r_b) = \hbar\Omega$ desplaza el estado doblemente excitado $|rr\rangle$ fuera de resonancia. El sistema solo puede tener **un átomo en Rydberg a la vez** dentro del bloque.

Para $^{87}$Rb con $n=70$ y $\Omega/2\pi = 1$ MHz: $r_b \approx 8\text{--}10$ µm (separación típica de red: $4\text{--}6$ µm).

### 3.2 Puerta CZ con bloqueo

La secuencia de 3 pulsos para implementar una puerta CZ entre dos átomos:

1. $\pi$-pulso en átomo control: $|1\rangle_c \to |r\rangle_c$
2. $2\pi$-pulso en átomo target: si control en $|r\rangle$, el target no puede excitarse (bloqueado); si control en $|0\rangle$, el target completa $|1\rangle \to |r\rangle \to -|1\rangle$
3. $\pi$-pulso en átomo control: $|r\rangle_c \to |1\rangle_c$

Tabla de verdad:
| $|c, t\rangle$ entrada | $|c, t\rangle$ salida |
|---|---|
| $|0, 0\rangle$ | $|0, 0\rangle$ |
| $|0, 1\rangle$ | $-|0, 1\rangle$ |
| $|1, 0\rangle$ | $|1, 0\rangle$ |
| $|1, 1\rangle$ | $|1, 1\rangle$ |

Esto es una puerta CZ (hasta fase global). Fidelidad experimental: $F \geq 99.5\%$ (Evered et al. 2023, Nature).

---

## 4. Hamiltoniano PXP y Fases Cuánticas {#4-pxp}

### 4.1 El modelo PXP

En el límite de bloqueo fuerte ($U \gg \Omega$), el espacio de Hilbert se proyecta al subespacio sin excitaciones adyacentes. El Hamiltoniano efectivo es:

$$H_\text{PXP} = \frac{\Omega}{2}\sum_i P_{i-1} X_i P_{i+1}$$

donde $P_i = |g_i\rangle\langle g_i|$ proyecta en el estado base y $X_i = \sigma_i^x$ voltea el qubit $i$.

### 4.2 Diagrama de fase del Hamiltoniano de Rydberg

En el estado estacionario (temperatura cero), el diagrama de fase $(\Omega, \Delta)$ tiene tres regiones:

| Región | Condición | Orden |
|---|---|---|
| **Paramagnet** (PM) | $\Delta \ll 0$ | $\langle n_i\rangle \approx 0$, desordenado |
| **Z₂ ordenado** | $\Delta/\Omega \approx 1.5$ | Patrón alternante $|grg\ldots\rangle$, $\langle n_i\rangle \approx 0.5$ alternante |
| **Z₃ ordenado** | $\Delta/\Omega \approx 2.6$ | $|ggrggr\ldots\rangle$ |
| **Fluido cuántico** | $\Delta \gg 0$ | $\langle n_i\rangle \approx 1$ (saturación) |

La transición PM → Z₂ es de segundo orden en la clase de universalidad de Ising cuántico.

### 4.3 Cicatrices cuánticas (quantum scars)

El Hamiltoniano PXP muestra un fenómeno inusual: **quantum many-body scars** — estados propios de baja entropía en el espectro medio de energía que violan la hipótesis de termalización del eigenstate (ETH). Descubiertos experimentalmente en QuEra (Bernien et al. 2017, Nature).

---

## 5. Computación Analógica vs Digital {#5-analogica}

### 5.1 Modo analógico

En modo analógico, el sistema evoluciona bajo el Hamiltoniano de Rydberg completo. El usuario controla:
- Forma del pulso $\Omega(t)$, $\Delta(t)$
- Geometría del array de átomos

No hay puertas discretas: la computación es la evolución continua. Es el modo nativo de QuEra Aquila.

**Aplicaciones**: simulación de modelos de Ising/Heisenberg en geometrías arbitrarias, exploración de fases cuánticas, QAOA analógico para MaxCut.

### 5.2 Modo digital (gate-based)

Usando pulsos individuales de $\pi$ y $2\pi$ se implementan:
- Puertas de 1 qubit: $R_x$, $R_y$, $R_z$ sobre la transición hiperfina.
- Puerta CZ (2 qubits): vía bloqueo de Rydberg.
- Puerta CCZ (3 qubits): dos operaciones CZ secuenciales.

El modo digital permite circuitos con puertas universales, equivalente a superconductores o iones. Ventaja clave: la conectividad puede ser **todos-con-todos** en una región gracias al largo alcance del bloqueo.

---

## 6. QuEra Aquila — Hardware y Acceso {#6-quera}

### 6.1 Especificaciones técnicas

| Parámetro | Aquila (2023) | Aquila (2024) |
|---|---|---|
| Qubits totales | 256 analógicos | 10 000 analógicos |
| Qubits lógicos (FT) | — | ~1 000 |
| Átomo | $^{87}$Rb | $^{87}$Rb |
| Geometría | 2D configurable | 2D configurable |
| $\Omega_\text{max}/2\pi$ | 4 MHz | 4 MHz |
| $\Delta_\text{max}/2\pi$ | ±125 MHz | ±125 MHz |
| Tiempo de coherencia | $T_2 \sim 4$ µs (analógico) | Mejorado |
| Error CZ | ~0.5% | ~0.5% |
| Temperatura operación | $10^{-10}$ Torr (UHV) | UHV |

### 6.2 Acceso mediante Amazon Braket

QuEra Aquila está disponible en **Amazon Braket** (pay-per-task). El SDK nativo es `braket-ahs` (Analog Hamiltonian Simulation):

```python
from braket.ahs import AnalogHamiltonianSimulation, AtomArrangement, DrivingField

# Definir posiciones
register = AtomArrangement()
register.add([0.0, 0.0]); register.add([5.0e-6, 0.0])

# Pulso de Rabi
drive = DrivingField(amplitude=..., phase=..., detuning=...)
ahs = AnalogHamiltonianSimulation(register=register, hamiltonian=drive)
```

El simulador local `LocalSimulator("default")` permite pruebas sin hardware.

---

## 7. Pasqal Fresnel y Otros Fabricantes {#7-pasqal}

### Pasqal

- Arquitectura: tweezer arrays con $^{87}$Rb (2D y 3D).
- Producto: Fresnel — 100 qubits, acceso cloud via Pasqal Cloud.
- SDK: `pulser` (Python) — define secuencias de pulsos sobre registros de átomos.
- Diferenciador: conectividad 3D (apilar capas de átomos).

### Atom Computing

- Arquitectura: $^{87}$Sr (alcalino-térreo) — transición de "reloj" ultraestable.
- Hito 2023: 1 180 qubits — el mayor array de tweezer demostrado hasta ese momento.
- Ventaja: coherencia $T_2 > 40$ s (sin decaimiento espontáneo desde estado base).

### Infleqtion (anteriormente ColdQuanta)

- Arquitectura: $^{87}$Rb en trampa de haz dipolo.
- Producto: Hilbert — acceso cloud, gate-based digital.

---

## 8. Decoherencia y Limitaciones Actuales {#8-decoherencia}

### 8.1 Fuentes de error

| Error | Causa | Escala |
|---|---|---|
| Decaimiento espontáneo desde Rydberg | $\tau_\text{Ryd} \sim 100$ µs | $\sim 1\%$ por puerta 2Q |
| Pérdida atómica del array | Colisiones, foto-ionización | $< 0.1\%$ por ciclo |
| Ruido de fase del láser | Jitter temporal del láser | $\sim 0.1\text{--}0.3\%$ |
| Movimiento atómico térmico | kT finita ($T \sim 10$ µK) | $\sim 0.5\%$ por puerta |
| Crosstalk entre átomos | Iluminación residual | Geométrico |

### 8.2 Límite de fidelidad actual

El récord de fidelidad de puerta CZ es $F = 99.5\%$ (Evered et al. 2023). Para alcanzar tolerancia a fallos se necesita $F > 99.9\%$ con el código de superficie — aún ~$5\times$ por encima de los mejores resultados.

### 8.3 Escalado

El mayor desafío no es el número de átomos sino la **fidelidad uniforma** en arrays grandes: la variación de intensidad del láser excitador introduce variaciones en $\Omega$ de $\sim 1\%$ rms, lo que limita la coherencia en sistemas > 100 qubits.

---

## 9. Casos de Uso: Optimización y Simulación {#9-aplicaciones}

### 9.1 Optimización combinatoria

El problema **Maximum Independent Set (MIS)** en un grafo $G=(V,E)$ se mapea naturalmente al Hamiltoniano de Rydberg: los átomos en estado Rydberg representan los vértices seleccionados, y el bloqueo impone la restricción de independencia (no dos adyacentes).

El estado fundamental del Hamiltoniano (con $\Omega \to 0$, $\Delta > 0$) es el MIS del grafo formado por los pares de átomos dentro del radio de bloqueo.

### 9.2 MaxCut analógico

Un protocolo QAOA analógico para MaxCut: la evolución bajo $H(\Omega(t), \Delta(t))$ con rampas adiabáticas emula las capas QAOA sin compilar puertas individuales.

### 9.3 Simulación de materiales

El Hamiltoniano de Rydberg simula directamente modelos cuánticos de spin:

| Modelo | Geometría | Aplicación |
|---|---|---|
| Ising transversal 1D | Cadena lineal | Transición de fase cuántica |
| Ising 2D frustrado | Red triangular | Magnetismo frustrado |
| $Z_2$ lattice gauge | Red cuadrada | Gauge theories cuánticas |
| Modelo de Hubbard (via mapping) | Red cuadrada | Superconductividad cuprato |

---

## 10. Comparativa de Plataformas {#10-comparativa}

| Característica | Rydberg (QuEra) | Superconductor (IBM) | Iones (IonQ) | Fotónica (PsiQ) |
|---|---|---|---|---|
| Temperatura | UHV, $T_\text{atomo} \sim 10$ µK | 15 mK (dilución) | UHV, laser cooling | Ambiente |
| Qubits actuales | 256–10 000 (analóg.) | 127–1 386 | 36–64 | En desarrollo |
| Error 2Q | ~0.5% | 0.3% | 0.1% | ~2% |
| Tiempo puerta 2Q | $\sim 300$ ns | $\sim 30$ ns | $\sim 600$ µs | ~ns (KLM estocástico) |
| Conectividad | Todos-con-todos (en $r_b$) | Local (vecinos) | Todos-con-todos | Flexible |
| Reconfiguración | Dinámica (mid-circuit) | No | Parcial | No (topología fija) |
| Modo analógico | Nativo | No | No | No |
| Escalado principal | Átomos (fácil) | Criogenia | Trampas de radio | Integración fotónica |

---

## Referencias

1. Bernien, H. et al. (2017). *Probing many-body dynamics on a 51-atom quantum simulator*. Nature **551**, 579.
2. Ebadi, S. et al. (2021). *Quantum phases of matter on a 256-atom programmable quantum simulator*. Nature **595**, 227.
3. Evered, S.J. et al. (2023). *High-fidelity parallel entangling gates on a neutral-atom quantum computer*. Nature **622**, 268.
4. Bluvstein, D. et al. (2024). *Logical quantum processor based on reconfigurable atom arrays*. Nature **626**, 58.
5. Pichler, H. et al. (2018). *Quantum optimization of maximum independent set using Rydberg atom arrays*. arXiv:1808.10816.
6. Turner, C.J. et al. (2018). *Weak ergodicity breaking from quantum many-body scars*. Nature Physics **14**, 745.
