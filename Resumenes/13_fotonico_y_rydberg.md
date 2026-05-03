# Resumen 13 — Computación Fotónica y Átomos Neutros (Rydberg)

## 1. Computación Fotónica Lineal — Teorema KLM

El **teorema Knill-Laflamme-Milburn (2001)** demuestra que la computación cuántica universal es posible con:
- Fuentes de fotones individuales
- Detección de fotones (medición)
- Óptica lineal (divisores de haz, desfasadores)

Sin embargo, la compuerta CNOT fotónica lineal es **probabilística**: éxito con probabilidad $1/16$ de forma nativa, mejorable con recursos auxiliares.

$$
U_{\text{BS}}(\theta) = \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}
$$

---

## 2. Boson Sampling

**Boson sampling** (Aaronson-Arkhipov 2011): computación de distribución de salida de $n$ fotones en $m$ modos tras interferómetro unitario $U$.

$$
p(s_1, \ldots, s_m) = \frac{|\text{Perm}(U_{S})|^2}{\prod_i s_i!}
$$

donde $\text{Perm}(M)$ es el **permanente** de la submatriz — \#P-difícil de calcular clásicamente.

- Demostración de ventaja cuántica sin aplicación práctica directa
- Xanadu Borealis (2022): 216 modos, ventaja cuántica verificada
- Variante gaussiana (GBS) usada para grafos y simulación molecular

---

## 3. Códigos GKP (Gottesman-Kitaev-Preskill)

Los **códigos GKP** codifican un qubit lógico en el espacio de fase de un oscilador armónico:

$$
|0_L\rangle \propto \sum_{n \in \mathbb{Z}} |q = 2n\sqrt{\pi}\rangle, \quad |1_L\rangle \propto \sum_{n \in \mathbb{Z}} |q = (2n+1)\sqrt{\pi}\rangle
$$

**Umbral de error**: los errores de desplazamiento son corregibles si $|\Delta q|, |\Delta p| < \sqrt{\pi}/2$.

| Parámetro | Valor |
|---|---|
| Umbral de squeezing | $\approx 10$ dB (para operaciones fault-tolerant) |
| Umbral de desplazamiento | $\delta < \sqrt{\pi}/2 \approx 0.886$ |
| Compatibilidad | Fotónica, microondas superconductor |
| Estado del arte 2025 | $>20$ dB demostrado en cavidades |

---

## 4. Bloqueo de Rydberg

Los **átomos de Rydberg** son átomos excitados con $n \gg 1$ (número cuántico principal grande):

$$
r_{n} \sim n^2 a_0, \quad U_{vdW} \sim C_6 / r^6, \quad C_6 \propto n^{11}
$$

**Bloqueo de Rydberg**: si dos átomos están dentro del radio de bloqueo $r_b$, solo uno puede ser excitado simultáneamente:

$$
r_b = \left(\frac{C_6}{\hbar \Omega}\right)^{1/6}
$$

Esto implementa una compuerta CZ nativa de alta fidelidad ($>99.5\%$ demostrada en 2023).

---

## 5. Hamiltoniano PXP y Fase Z₂

El **Hamiltoniano PXP** modela átomos Rydberg en cadena 1D:

$$
H_{PXP} = \Omega \sum_i P_{i-1} X_i P_{i+1}
$$

donde $P_i = |g\rangle\langle g|_i$ proyecta al estado base (restricción de bloqueo).

- Exhibe **cicatrices cuánticas** (quantum scars): órbitas periódicas en espacio de Hilbert restringido
- **Fase Z₂**: orden antiferromagnético $|g r g r \ldots\rangle$ con ruptura espontánea de simetría de traslación

---

## 6. QuEra Aquila — Hito 10,000 Qubits

**QuEra Aquila** (2024-2025) demostró escalado a ~10,000 qubits lógicos en arquitectura de átomos neutros:

| Característica | QuEra Aquila |
|---|---|
| Tecnología | Átomos de Rb en trampa óptica 2D |
| Qubits físicos | ~10,000 |
| Fidelidad CZ | $>99.5\%$ |
| Coherencia $T_2$ | $\sim 1$ s |
| Reconfiguración | Dinámica (movimiento atómico mid-circuit) |
| Ventaja | Conectividad arbitraria, escalado atómico |

---

## Fórmulas Clave

$$
\text{KLM CNOT prob} = \frac{1}{16} \text{ (lineal pura)}
$$

$$
H_{PXP} = \Omega \sum_i P_{i-1} X_i P_{i+1}, \quad \text{fase Z}_2: \langle Z_i Z_{i+1} \rangle < 0
$$

$$
\text{Fidelidad GBS} \sim |\text{Haf}(A_S)|^2
$$
