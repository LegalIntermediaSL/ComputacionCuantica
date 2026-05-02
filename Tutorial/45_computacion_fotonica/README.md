# Módulo 45 — Computación Cuántica Fotónica

La fotónica cuántica explota los **fotones** como portadores de información cuántica. A diferencia de los qubits superconductores o de iones trampa, los fotones viajan a la velocidad de la luz, no requieren criogenia para la propagación y son naturalmente resistentes a la decoherencia ambiental. Su desafío central es que la **interacción fotón-fotón** necesaria para puertas de 2 qubits es extremadamente débil.

---

## Índice

1. [Estados cuánticos de la luz](#1-estados)
2. [Óptica lineal cuántica y el teorema KLM](#2-klm)
3. [Boson Sampling y ventaja cuántica](#3-boson-sampling)
4. [Variables continuas (CV)](#4-cv)
5. [Operaciones gaussianas y no gaussianas](#5-gaussianas)
6. [Códigos GKP — Corrección de errores fotónica](#6-gkp)
7. [Computación basada en medida (MBQC)](#7-mbqc)
8. [Hardware fotónico 2024–2025](#8-hardware)
9. [Comparativa de plataformas](#9-comparativa)
10. [Conexiones con módulos anteriores](#10-conexiones)

---

## 1. Estados Cuánticos de la Luz {#1-estados}

### 1.1 Estados de Fock (número de fotones)

Los estados de Fock $|n\rangle$ son autoestados del operador número $\hat{n} = \hat{a}^\dagger \hat{a}$:

$$\hat{n}|n\rangle = n|n\rangle, \quad n = 0, 1, 2, \ldots$$

El estado de vacío $|0\rangle$ es el más puro: sin fotones, sin energía más allá de la energía de punto cero $\hbar\omega/2$.

El operador de creación $\hat{a}^\dagger$ y el de aniquilación $\hat{a}$ satisfacen:
$$\hat{a}^\dagger|n\rangle = \sqrt{n+1}|n+1\rangle, \quad \hat{a}|n\rangle = \sqrt{n}|n-1\rangle$$

### 1.2 Estados Coherentes

Los estados coherentes $|\alpha\rangle$ (con $\alpha \in \mathbb{C}$) son los más "clásicos" entre los estados cuánticos de la luz — los producen los láseres:

$$|\alpha\rangle = e^{-|\alpha|^2/2} \sum_{n=0}^\infty \frac{\alpha^n}{\sqrt{n!}}|n\rangle$$

Son eigenestados del operador de aniquilación: $\hat{a}|\alpha\rangle = \alpha|\alpha\rangle$.

La distribución de fotones es Poisson: $P(n) = e^{-\bar{n}}\bar{n}^n/n!$ con $\bar{n} = |\alpha|^2$.

### 1.3 Estados Comprimidos (Squeezed)

Los estados comprimidos reducen la fluctuación en una cuadratura a expensas de la otra, respetando la desigualdad de Heisenberg:

$$\Delta\hat{X}\,\Delta\hat{P} \geq \frac{1}{2}$$

El operador de compresión (squeezing): $\hat{S}(r) = \exp\!\left[\frac{r}{2}(\hat{a}^2 - \hat{a}^{\dagger 2})\right]$

Con $r > 0$ (squeezing en $X$):
- $\Delta\hat{X} = e^{-r}/2$ (comprimido)
- $\Delta\hat{P} = e^{+r}/2$ (amplificado)

El squeezing se mide en **dB**: $r_\text{dB} = -20\log_{10}(e^{-r}) \approx 8.69\,r$.

Los mejores laboratorios han alcanzado **15 dB** de squeezing (2021, PTB Braunschweig).

### 1.4 Función de Wigner

La función de Wigner es la representación fase-espacio de un estado cuántico $\rho$:

$$W(x, p) = \frac{1}{\pi\hbar}\int_{-\infty}^\infty \langle x+y|\rho|x-y\rangle e^{2ipy/\hbar}\, dy$$

- **Estado coherente**: gaussiana centrada en $(\text{Re}\,\alpha, \text{Im}\,\alpha)$.
- **Estado Fock** $|1\rangle$: gaussiana con una "depresión" negativa en el origen — **no clásico**.
- **Estado gato de Schrödinger** $|0\rangle + |\alpha\rangle$: franjas de interferencia en fase-espacio.

Los valores negativos de $W$ son **indicadores de no-clasicidad** — sólo los estados cuánticos genuinos los exhiben.

---

## 2. Óptica Lineal Cuántica y el Teorema KLM {#2-klm}

### 2.1 Red de óptica lineal

Una red de óptica lineal (divisores de haz, desfasadores) implementa una transformación unitaria $U \in U(m)$ sobre los modos fotónicos:

$$\hat{a}_i^\dagger \to \sum_j U_{ij} \hat{a}_j^\dagger$$

Los elementos básicos son:
- **Divisor de haz** (beamsplitter): $\text{BS}(\theta) = \begin{pmatrix}\cos\theta & -\sin\theta \\ \sin\theta & \cos\theta\end{pmatrix}$
- **Desfasador** (phase shifter): $\text{PS}(\phi) = \begin{pmatrix}e^{i\phi} & 0 \\ 0 & 1\end{pmatrix}$

Todo $U \in U(m)$ se descompone en $O(m^2)$ divisores de haz y desfasadores (descomposición de Reck-Zeilinger).

### 2.2 El Teorema KLM (Knill-Laflamme-Milburn, 2001)

KLM demostró que la **computación cuántica universal** es posible con:
1. Fotones individuales como qubits (codificación $|0\rangle = |1,0\rangle$, $|1\rangle = |0,1\rangle$).
2. Redes de óptica lineal.
3. Detectores de número de fotones.
4. Medidas y *feed-forward* clásico.

La puerta CNOT se implementa con probabilidad $p = 1/16$ con recursos lineales. Con teleportación cuántica y catálogos de estados ancilla, la probabilidad puede llevarse a $1 - O(1/n)$ con $O(n)$ fotones ancilla.

**Limitación práctica**: la tasa de éxito baja (y la necesidad de corrección de errores lineal-óptica) hizo que KLM no sea la arquitectura preferida para hardware actual — se usa como base teórica.

---

## 3. Boson Sampling y Ventaja Cuántica {#3-boson-sampling}

### 3.1 El problema del Boson Sampling

Dado $m$ modos y $n$ fotones, el Boson Sampling consiste en muestrear de la distribución de salida de una red de óptica lineal aleatoria $U \in U(m)$.

La probabilidad de una configuración de salida $(s_1, \ldots, s_m)$ es:

$$p(s_1,\ldots,s_m) = \frac{|\text{Perm}(U_{S,T})|^2}{s_1!\cdots s_m!\, t_1!\cdots t_m!}$$

donde $U_{S,T}$ es la submatriz de $U$ y $\text{Perm}$ es el **permanente de la matriz** — computacionalmente $\#P$-duro en el caso general.

### 3.2 El algoritmo de Ryser para el permanente

El permanente de una matriz $n\times n$ se calcula en $O(2^n n)$ con el algoritmo de Ryser:

$$\text{Perm}(A) = (-1)^n \sum_{S \subseteq [n]} (-1)^{|S|} \prod_{i=1}^n \sum_{j \in S} a_{ij}$$

Para $n=50$, esto requiere $\sim 10^{15}$ operaciones — intractable clásicamente.

### 3.3 Resultados experimentales

| Experimento | Año | Fotones | Modos | Ventaja demostrada |
|---|---|---|---|---|
| USTC (Jiuzhang 1.0) | 2020 | 50 (detect.) | 100 | $10^{14}\times$ vs CPU |
| USTC (Jiuzhang 2.0) | 2021 | 113 | 144 | $10^{24}\times$ vs supercomputador |
| Xanadu (Borealis) | 2022 | ~219 | 216 (CV) | Gaussian Boson Sampling |

**Nota**: la verificación de estos experimentos es objeto de debate activo — la contracción de tensores puede simular algunas instancias.

---

## 4. Variables Continuas (CV) {#4-cv}

### 4.1 Cuadraturas como observables

En computación de variables continuas, los qubits discretos se reemplazan por **cuadraturas** del campo:

$$\hat{X} = \frac{\hat{a} + \hat{a}^\dagger}{2}, \quad \hat{P} = \frac{\hat{a} - \hat{a}^\dagger}{2i}$$

con $[\hat{X}, \hat{P}] = i/2$.

Los estados lógicos son distribuciones en el espacio fase $(\hat{X}, \hat{P})$.

### 4.2 Computación gaussiana

Las **operaciones gaussianas** preservan la gaussianidad del estado:
- Desplazamiento: $\hat{D}(\alpha) = e^{\alpha\hat{a}^\dagger - \alpha^*\hat{a}}$
- Compresión: $\hat{S}(r) = e^{r(\hat{a}^2 - \hat{a}^{\dagger 2})/2}$
- Rotación de fase: $\hat{R}(\phi) = e^{i\phi\hat{a}^\dagger\hat{a}}$

Las operaciones gaussianas son **eficientemente simulables** clásicamente (análogo al teorema de Gottesman-Knill).

### 4.3 No-gaussianidad y universalidad

Para la computación universal CV se necesita al menos una operación **no gaussiana**:
- Medida de número de fotones (PNR — photon-number-resolving detector).
- Compuerta cúbica $\hat{V}(\chi) = e^{i\chi\hat{X}^3}$.
- Estado gato $|\alpha\rangle + |-\alpha\rangle$ como recurso.

---

## 5. Operaciones Gaussianas y No Gaussianas {#5-gaussianas}

### 5.1 El estado squeezed como recurso computacional

En arquitecturas de medida-basada (MBQC), los estados squeezed son la materia prima del "cluster state" continuo (CV). Un nivel de squeezing de $> 10$ dB es necesario para tolerancia a fallos en algunos esquemas.

### 5.2 El problema del umbral de squeezing

Para el esquema GKP de corrección de errores, el squeezing mínimo es:
$$r_\text{umbral} \approx 10\text{ dB} \quad (r \approx 1.15)$$

Debajo de este umbral, los errores no pueden corregirse. El estado del arte (15 dB, 2021) supera el umbral teórico pero los efectos prácticos de imperfecciones bajan el umbral efectivo.

---

## 6. Códigos GKP — Corrección de Errores Fotónica {#6-gkp}

### 6.1 La idea de Gottesman-Kitaev-Preskill (2001)

Los códigos GKP codifican un qubit lógico en los estados de fase-espacio del oscilador armónico. Los estados lógicos son superposiciones de estados squeezed:

$$|0\rangle_L = \sum_{n=-\infty}^\infty |x = 2n\sqrt{\pi}\rangle_X$$
$$|1\rangle_L = \sum_{n=-\infty}^\infty |x = (2n+1)\sqrt{\pi}\rangle_X$$

Son periódicas en el espacio-X con periodo $2\sqrt{\pi}$.

### 6.2 Corrección de errores GKP

Los errores de desplazamiento pequeños $\delta x, \delta p < \sqrt{\pi}/2$ son corregibles midiendo los estabilizadores:
$$S_X = e^{i 2\sqrt{\pi}\hat{P}}, \quad S_Z = e^{-i 2\sqrt{\pi}\hat{X}}$$

El código GKP protege contra el ruido gaussiano si $\sigma < \sqrt{\pi}/4 \approx 0.44$.

### 6.3 Implementación experimental

Los códigos GKP se han implementado en:
- **Iones trampa** (2019, Flühmann et al., Nature): squeezing efectivo 9.5 dB.
- **Microondas/superconductor** (2020, Campagne-Ibarcq et al., Nature): squeezing 13.3 dB en cavidad 3D.
- **Fotónica** (en desarrollo): requiere PNR detectors y squeezing >10 dB.

---

## 7. Computación Basada en Medida (MBQC) {#7-mbqc}

### 7.1 Cluster states y one-way quantum computing

En MBQC, se prepara un **cluster state** altamente entrelazado y la computación se realiza mediante medidas de un qubit en bases elegidas adaptativamente. Las medidas "consumen" el entrelazamiento del cluster.

Para fotones, el cluster state se prepara con divisores de haz y compuertas CZ controladas por fotones (usando medida + feed-forward).

### 7.2 MBQC con CV

La versión continua usa **cluster states gaussianos** (redes de estados squeezed) y medidas de homodino. Es el enfoque de Xanadu (plataforma Strawberry Fields).

La computación universal requiere estados squeezed en todos los nodos del cluster más una medida no gaussiana (PNR).

---

## 8. Hardware Fotónico 2024–2025 {#8-hardware}

### PsiQuantum

- Arquitectura: fotónica en silicio (Si-Ph), guías de onda en chip.
- Qubits: fotones individuales de 1550 nm.
- Objetivo: 1M+ qubits con tolerancia a fallos mediante fusión de Bell pairs.
- Hito 2024: demostración de módulo de fusión con >90% de eficiencia.

### Xanadu

- Arquitectura: CV fotónica con squeezing y detección homodino.
- Producto: Borealis (2022) — primera ventaja cuántica programable con CV.
- Plataforma: Strawberry Fields (Python, PennyLane).
- Hito 2025: integración GKP en chip fotónico.

### Quandela

- Arquitectura: fuentes de fotones individuales basadas en puntos cuánticos.
- Producto: Perceval (Python) — simulación y acceso a hardware fotónico.
- Eficiencia de extracción: >95% en puntos cuánticos GaAs.

### QuiX Quantum

- Arquitectura: chips fotónicos de nitruro de silicio (Si₃N₄).
- Producto: procesadores de hasta 20 modos.
- Ventaja: pérdidas ultrabajas (<0.1 dB/cm).

---

## 9. Comparativa de Plataformas {#9-comparativa}

| Característica | Fotónica (DV) | Fotónica (CV) | Superconductor | Iones trampa |
|---|---|---|---|---|
| Temperatura operación | Ambiente | Ambiente | 15 mK | Ultra-alto vacío |
| Qubit | Fotón único | Cuadratura | Transmon | Ión ⁴⁰Ca⁺/¹⁷¹Yb⁺ |
| Tiempo coherencia | N/A (en vuelo) | ~microsegundos | 100–500 μs | 10 s – 1 min |
| Velocidad puerta 2Q | Nanosegundos | Microsegundos | 10–100 ns | 100 μs – 1 ms |
| Error puerta 2Q | ~1–5% (KLM) | ~1% (CV-MBQC) | 0.1–0.5% | 0.1–0.2% |
| Conectividad | Flexible (fibra/chip) | Flexible | Local (vecinos) | Todos-con-todos |
| Escalado | Integración fotónica | Multiplexado en tiempo | Criogénico | Cadenas iónicas / módulos |
| Tolerancia a fallos | FBQC / GKP | GKP / cat qubit | Surface code | Color code |

---

## 10. Conexiones con Módulos Anteriores {#10-conexiones}

| Módulo | Conexión |
|---|---|
| Módulo 07 — QPE | LOQC puede implementar QPE con fotones individuales y óptica lineal |
| Módulo 09 — QEC | GKP es la versión continua del código de repetición, Tórico para fotones |
| Módulo 16 — Canales | El canal de pérdida fotónica es análogo al amortiguamiento de amplitud |
| Módulo 34 — DTQW | Los quantum walks fotónicos son el mecanismo nativo de Boson Sampling |
| Módulo 41 — Topological QC | Anyons de Fibonacci pueden implementarse con fotones entrelazados |
| Módulo 43 — QML | Gaussian Boson Sampling motiva kernels cuánticos en PennyLane/Strawberry Fields |
| Módulo 44 — DQC | Los fotones son el único candidato práctico para canales cuánticos de largo alcance |

---

## Referencias

1. Knill, E., Laflamme, R. & Milburn, G.J. (2001). *A scheme for efficient quantum computation with linear optics*. Nature **409**, 46–52.
2. Aaronson, S. & Arkhipov, A. (2011). *The Computational Complexity of Linear Optics*. STOC 2011.
3. Zhong, H.-S. et al. (2020). *Quantum computational advantage using photons*. Science **370**, 1460–1463.
4. Gottesman, D., Kitaev, A. & Preskill, J. (2001). *Encoding a qubit in an oscillator*. PRA **64**, 012310.
5. Bourassa, J.E. et al. (2021). *Blueprint for a scalable photonic fault-tolerant quantum computer*. Quantum **5**, 392.
6. Madsen, L.S. et al. (2022). *Quantum computational advantage with a programmable photonic processor*. Nature **606**, 75–81.
