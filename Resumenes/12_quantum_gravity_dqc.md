# Resumen 12 — Gravedad Cuántica, DQC e Internet Cuántico

## 1. Principio Holográfico

El **principio holográfico** (Bekenstein-Hawking, 't Hooft, Susskind) establece que la entropía máxima en una región de volumen $V$ con superficie frontera $A$ es:

$$
S \leq \frac{A}{4 l_P^2}
$$

donde $l_P = \sqrt{\hbar G / c^3} \approx 1.6 \times 10^{-35}$ m es la longitud de Planck. Implica que la información del volumen está codificada en la superficie.

---

## 2. AdS/CFT y Holografía

La correspondencia **AdS/CFT** (Maldacena 1997) establece una dualidad entre:

| Lado gravitacional (Bulk) | Lado cuántico (Borde) |
|---|---|
| Gravedad en AdS$_{d+1}$ | CFT en $\mathbb{R}^d$ |
| Geometría = entrelazamiento | Entropía de entrelazamiento |
| Horizonte de agujero negro | Estado térmico |
| Profundidad radial $z$ | Escala de energía UV/IR |

**Fórmula de Ryu-Takayanagi** (entropía holográfica):

$$
S(A) = \frac{\text{Area}(\gamma_A)}{4 G_N}
$$

donde $\gamma_A$ es la superficie mínima en el bulk homóloga a la región frontera $A$.

---

## 3. Experimento Mental Hayden-Preskill

El experimento de Hayden-Preskill (2007) analiza cuánta información se puede recuperar de la radiación de Hawking:

- **Setup**: un agujero negro viejo de $n$ qubits lanza $k$ qubits adicionales de información
- **Resultado**: la información emerge después de lanzar solo $k + O(1)$ qubits de radiación
- **Implicación**: los agujeros negros son **scrambladores rápidos** — mezclan información en tiempo $O(n \log n)$ (tiempo de scrambling)

$$
t_{\text{scramble}} \sim \frac{\beta}{2\pi} \log S
$$

donde $\beta = 1/T$ y $S$ es la entropía del agujero negro.

---

## 4. Repetidores Cuánticos y Pares Bell

La comunicación cuántica de largo alcance requiere **repetidores cuánticos** para superar la pérdida exponencial en fibra ($\sim 0.2$ dB/km).

**Par Bell** (estado maximalmente entrelazado):

$$
|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)
$$

### Entanglement Swapping

Permite extender entrelazamiento sin transmisión de qubits:

1. Alice-Bob comparten $|\Phi^+\rangle_{AB}$
2. Bob-Charlie comparten $|\Phi^+\rangle_{BC}$
3. Bob realiza medición Bell en sus qubits $(B, B')$
4. Resultado: Alice-Charlie quedan entrelazados $|\Phi^+\rangle_{AC}$

| Componente | Función |
|---|---|
| Memoria cuántica | Almacenar qubits mientras se espera entrelazamiento |
| Purificación | Mejorar fidelidad de pares entrelazados ruidosos |
| BSM (Bell State Measurement) | Proyectar en base Bell para swapping |
| Corrección clásica | Canal clásico para feed-forward |

---

## 5. Roadmap Internet Cuántico 2030

El **Quantum Internet Alliance** define 6 etapas de madurez:

1. **QKD Trusted Node** (operativo 2020): claves cuánticas entre nodos de confianza
2. **Prepare and Measure** (2022-2025): comunicación BB84, sin memoria
3. **Entanglement Distribution** (2025-2027): pares Bell entre nodos distantes
4. **Quantum Memory** (2027-2028): almacenamiento con fidelidad $>99\%$, coherencia $>1$ s
5. **Fault-Tolerant** (2029-2030): corrección de errores en red
6. **Quantum Computing** (post-2030): computación distribuida cuántica

**Experimentos recientes**:
- Satélite Micius (China): entrelazamiento a 1200 km (2017)
- Repetidores con memorias de átomos de Rb: coherencia $>100$ ms (2023)
- Redes metropolitanas QKD en múltiples ciudades (2024-2025)

---

## Fórmulas Clave

$$
S_{\text{BH}} = \frac{k_B A}{4 l_P^2}, \quad \text{Temperatura Hawking: } T_H = \frac{\hbar c^3}{8\pi G M k_B}
$$

$$
F_{\text{swap}} = F_1 \cdot F_2 \quad \text{(fidelidad de swapping)}
$$

$$
\text{Capacidad QKD} \sim -\log(1-\eta) \quad \eta = \text{transmisividad}
$$
