# Resumen 15 — QNLP y Quantum Annealing

## 1. Gramática de Pregrupos y DisCoCat

El **NLP cuántico (QNLP)** (Coecke, Sadrzadeh, Clark 2010) usa **gramática de pregrupos** para asignar tipos a palabras:

- Sustantivo: $n$
- Verbo transitivo: $n^r \cdot s \cdot n^l$
- Adjetivo: $n \cdot n^l$

Los **funtores DisCoCat** mapean diagramas gramaticales a circuitos cuánticos:

$$F: \mathbf{Gram} \to \mathbf{FHilb}$$

Cada palabra mapea a un tensor en un espacio de Hilbert; la composición gramatical es contracción tensorial.

---

## 2. Circuitos IQP y Pipeline Lambeq

Los circuitos **IQP** (Instantaneous Quantum Polynomial) son el ansatz natural para QNLP:

$$U = H^{\otimes n} D(\theta) H^{\otimes n}$$

donde $D(\theta)$ es diagonal en la base computacional. Son difíciles de simular clásicamente bajo conjeturas estándar.

**Pipeline lambeq** (Cambridge Quantum / Quantinuum):

1. Parseo gramatical → diagrama de pregrupo
2. Reescritura de diagramas (reducción de qubits)
3. Compilación a circuito IQP o ansatz ansatz parametrizado
4. Entrenamiento con gradientes (Pennylane/Qiskit)
5. Clasificación/inferencia cuántica

```
texto → lambeq.BobcatParser → CircuitAnsatz → PennyLane → optimización
```

---

## 3. QUBO y Formulación MAX-CUT

El **Quadratic Unconstrained Binary Optimization (QUBO)** es el lenguaje nativo del annealing:

$$\min_{x \in \{0,1\}^n} x^T Q x = \min_{x} \sum_{i \leq j} Q_{ij} x_i x_j$$

**MAX-CUT → QUBO**: dado grafo $G=(V,E)$, maximizar corte equivale a:

$$\text{MAX-CUT} = \max_{x \in \{0,1\}^n} \sum_{(i,j)\in E} (x_i + x_j - 2x_i x_j)$$

En variables de espín $z_i = 2x_i - 1$:

$$\text{MAX-CUT} \Leftrightarrow \min_z \sum_{(i,j)\in E} z_i z_j = \min_z \frac{1}{2} \sum_{ij} J_{ij} z_i z_j$$

Este Hamiltoniano de Ising es directamente programable en D-Wave.

---

## 4. Arquitectura D-Wave Pegasus

| Característica | D-Wave Advantage (Pegasus) |
|---|---|
| Qubits | $\sim 5,000$ qubits físicos |
| Conectividad | Pegasus: 15 vecinos por qubit |
| Temperatura de operación | $\sim 15$ mK |
| Tiempo de annealing | $1\text{--}2000$ μs (programable) |
| Variables lógicas | $\sim 177$ (embedding completo) |
| Aplicaciones | Optimización combinatoria, ML, muestreo |

La topología **Pegasus** supera a Chimera (anterior) con mayor conectividad: embedding de grafos densos requiere menos qubits físicos.

---

## 5. Comparación Annealing vs QAOA

| Aspecto | D-Wave Annealing | QAOA |
|---|---|---|
| Paradigma | Evolución adiabática analógica | Circuito variacional digital |
| Hamiltonian | $H(t) = A(t)H_T + B(t)H_P$ | $e^{-i\gamma H_P} e^{-i\beta H_M}$ capas |
| Calidad solución | Heurística, no óptimo garantizado | $p$ capas → aproximación mejorable |
| Velocidad | Muy rápido ($\mu s$) | Lento (ruido actual limita $p$) |
| Escalado | 5000 qubits hoy | ~100-1000 qubits calidad |
| Ventaja cuántica | No demostrada en benchmark | Ventaja teórica en densas |

**Hamiltoniano adiabático de D-Wave**:

$$H(t) = -\frac{A(t)}{2} \sum_i \sigma_i^x + \frac{B(t)}{2} \left( \sum_i h_i \sigma_i^z + \sum_{ij} J_{ij} \sigma_i^z \sigma_j^z \right)$$

---

## Fórmulas Clave

$$F(\text{DisCoCat}) : n \otimes (n^r \cdot s \cdot n^l) \otimes n \to s$$

$$E_{\text{QAOA}}(\gamma,\beta) = \langle \gamma,\beta | H_P | \gamma,\beta \rangle, \quad \text{optimizar sobre } \gamma,\beta \in \mathbb{R}^p$$

$$\text{Approx. ratio QAOA-1 en MAX-CUT} \geq 0.6924$$
