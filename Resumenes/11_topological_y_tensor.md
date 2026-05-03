# Resumen 11 — Computación Topológica y Redes Tensoriales

## 1. Anyones y Computación Topológica

La computación topológica usa **anyones** — cuasipartículas en 2D cuya estadística de intercambio ni es bosónica ni fermiónica. Al intercambiar dos anyones, el estado adquiere una fase arbitraria:

$$
|\psi\rangle \xrightarrow{\text{intercambio}} e^{i\theta}|\psi\rangle \quad (\theta \neq 0, \pi)
$$

Para anyones **no abelianos**, el intercambio aplica una matriz unitaria no trivial — la clave de la computación topológica.

### Anyones de Fibonacci

Los anyones de Fibonacci tienen reglas de fusión:

$$
\tau \times \tau = \mathbf{1} + \tau
$$

- Espacio de Hilbert crece como números de Fibonacci: dimensión $\sim \phi^n$ donde $\phi = (1+\sqrt{5})/2$
- Son **universales para computación cuántica** mediante trenzado (braiding)
- Umbral de error topológicamente protegido: sin necesidad de corrección activa

---

## 2. Código Tórico de Kitaev

El código tórico define qubits en aristas de un retículo toroidal. Los operadores estabilizadores son:

$$
A_v = \prod_{e \in \text{vértice}} X_e, \qquad B_p = \prod_{e \in \text{plaqueta}} Z_e
$$

| Propiedad | Valor |
|---|---|
| Qubits lógicos | 2 (en toro) |
| Distancia | $d = \sqrt{n}$ |
| Anyones de carga | excitaciones de $A_v$ |
| Anyones de flujo | excitaciones de $B_p$ |
| Temperatura crítica | 0 K (no robusto térmicamente) |

Los errores crean pares de anyones; la corrección consiste en reunirlos (MWPM).

---

## 3. Redes Tensoriales — MPS y Dimensión de Enlace

Un **Matrix Product State (MPS)** factoriza el estado de $n$ qubits como:

$$
|\psi\rangle = \sum_{s_1,\ldots,s_n} A^{s_1}[1] A^{s_2}[2] \cdots A^{s_n}[n] |s_1 \cdots s_n\rangle
$$

donde cada $A^s[k]$ es una matriz de dimensión $\chi \times \chi$ (**bond dimension** $\chi$).

- **Ley de área para entrelazamiento**: para estados de bajo entrelazamiento, $S \sim \partial V$ (no $\sim V$), permitiendo $\chi$ polinomial
- Estado de producto: $\chi = 1$
- Estado GHZ: $\chi = 2$
- Estado genérico: $\chi \sim 2^{n/2}$ (intractable)

$$
S(\rho_A) \leq \chi \log \chi
$$

---

## 4. Algoritmo DMRG

El **Density Matrix Renormalization Group (DMRG)** optimiza MPS variacionalmente:

1. Barrer de izquierda a derecha: optimizar cada tensor $A[k]$ resolviendo eigenproblema local
2. Truncar valores singulares por debajo de $\varepsilon$ (controla $\chi$)
3. Repetir hasta convergencia

**Complejidad**: $O(n \chi^3 d^2)$ por barrido, donde $d$ es dimensión local.

| Tipo de sistema | $\chi$ necesaria | ¿DMRG eficiente? |
|---|---|---|
| 1D gapped | $O(1)$ | Sí |
| 1D crítico | $O(\text{poly}(n))$ | Sí (con log corrections) |
| 2D | $O(e^{L})$ | Limitado |
| Caótico / alta temperatura | $O(2^{n/2})$ | No |

---

## 5. Ley de Área y Aplicaciones

**Teorema (Hastings 2007)**: en sistemas gapped en 1D con Hamiltoniano local, el estado base satisface:

$$
S(A) \leq c \cdot \xi \cdot \log(\xi)
$$

donde $\xi$ es la longitud de correlación. Esto justifica que DMRG funcione para sistemas 1D gapped.

### Aplicaciones de Redes Tensoriales

- **Simulación clásica eficiente** de circuitos de bajo entrelazamiento
- **MERA** (Multiscale Entanglement Renormalization Ansatz): estados críticos con $S \sim \log L$
- **PEPS** (Projected Entangled Pair States): extensión 2D de MPS
- **Decodificación de códigos cuánticos**: BP en grafos tensoriales
- **AdS/CFT**: geometría emergente desde redes tensoriales (Swingle 2012)

---

## Fórmulas Clave

$$
\chi_{\max} = 2^{n/2}, \quad S \leq \log_2 \chi
$$

$$
\text{DMRG gap energético} \sim e^{-L/\xi}
$$

$$
\text{Dimensión espacio de Fibonacci} = F_n \approx \phi^n/\sqrt{5}
$$
