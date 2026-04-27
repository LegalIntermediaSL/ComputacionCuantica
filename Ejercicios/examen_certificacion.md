# Examen de Certificación — Computación Cuántica: Teoría y Práctica

**Versión:** 1.0 · 2026-04-27  
**Duración estimada:** 90 minutos  
**Puntuación máxima:** 100 puntos

---

## Instrucciones

- Cada pregunta tiene **una sola respuesta correcta** salvo indicación contraria.
- Las preguntas de **nivel básico** valen 2 puntos cada una (10 × 2 = 20 pt).
- Las preguntas de **nivel intermedio** valen 3 puntos cada una (15 × 3 = 45 pt).
- Las preguntas de **nivel avanzado** valen 4 puntos cada una (8 × 4 = 32 pt).
- Las preguntas de **investigación** valen 1.5 puntos por parte (2 × 1.5 = 3 pt — bonus).
- Clasificación: Básico ≥ 60 pt | Avanzado ≥ 80 pt | Investigador ≥ 92 pt.

---

## Nivel Básico (10 preguntas · 2 pt cada una)

### B1. Superposición
Un qubit en estado $|+\rangle = (|0\rangle + |1\rangle)/\sqrt{2}$ se mide en la base computacional. ¿Cuál es la probabilidad de obtener $|1\rangle$?

- a) 0  
- b) 0.25  
- **c) 0.5** ✓  
- d) 1  

> **Explicación:** $P(1) = |⟨1|+⟩|^2 = |1/\sqrt{2}|^2 = 0.5$. → Módulo 01.

---

### B2. Puerta X (NOT cuántico)
La puerta X actúa sobre $|0\rangle$ produciendo:

- **a) $|1\rangle$** ✓  
- b) $|+\rangle$  
- c) $i|1\rangle$  
- d) $(|0\rangle - |1\rangle)/\sqrt{2}$  

> **Explicación:** X = [[0,1],[1,0]]; X|0⟩ = |1⟩. → Módulo 02.

---

### B3. Entrelazamiento Bell
El circuito $H\otimes I \cdot \text{CNOT}$ sobre $|00\rangle$ produce:

- a) $|00\rangle$  
- b) $|01\rangle + |10\rangle$  
- **c) $(|00\rangle + |11\rangle)/\sqrt{2}$** ✓  
- d) $|11\rangle$  

> **Explicación:** H crea superposición en q0; CNOT engancha q1 → estado Bell $|\Phi^+\rangle$. → Módulo 03.

---

### B4. Puerta Hadamard
$H|1\rangle$ produce:

- a) $|0\rangle$  
- b) $|+\rangle$  
- **c) $|-\rangle = (|0\rangle - |1\rangle)/\sqrt{2}$** ✓  
- d) $|i\rangle$  

> **Explicación:** $H = [[1,1],[1,-1]]/\sqrt{2}$; $H|1\rangle = (|0\rangle-|1\rangle)/\sqrt{2} = |-\rangle$. → Módulo 02.

---

### B5. Medición cuántica
Tras medir un qubit entrelazado en $|\Phi^+\rangle$ y obtener $|0\rangle$ en el primer qubit, el segundo qubit colapsa a:

- **a) $|0\rangle$** ✓  
- b) $|1\rangle$  
- c) $|+\rangle$  
- d) Estado desconocido  

> **Explicación:** Correlación perfecta en $|\Phi^+\rangle$: si q0→0, entonces q1→0. → Módulo 03.

---

### B6. Complejidad de Grover
Grover busca en una base de N ítems desordenados en:

- a) $O(N)$  
- b) $O(\log N)$  
- **c) $O(\sqrt{N})$** ✓  
- d) $O(N^2)$  

> **Explicación:** Grover usa $\pi\sqrt{N}/4$ iteraciones de amplificación. → Módulo 05.

---

### B7. Teleportación cuántica
En el protocolo de teleportación, Alice necesita enviar a Bob para completar el protocolo:

- a) El qubit físico  
- b) El estado cuántico directamente  
- **c) 2 bits clásicos** ✓  
- d) 1 ebit de entrelazamiento y nada más  

> **Explicación:** Alice mide en base Bell (2 bits) y Bob aplica corrección X/Z según el resultado. → Módulo 07.

---

### B8. Canal depolarizante
El canal depolarizante con tasa $p$ convierte $\rho$ en:

- a) $p\rho + (1-p)I/2$  
- **b) $(1-p)\rho + p\,I/2$** ✓  
- c) $\rho + pX\rho X$  
- d) $(1-p)|\psi\rangle\langle\psi|$  

> **Explicación:** Canal estándar: mezcla el estado original con estado máximamente mixto $I/2$ con peso $p$. → Módulo 06.

---

### B9. Primitivas Qiskit 2.x
En Qiskit 2.x, para calcular un valor esperado $\langle\psi|H|\psi\rangle$ se usa:

- a) `StatevectorSampler`  
- **b) `StatevectorEstimator`** ✓  
- c) `QuantumInstance`  
- d) `execute()`  

> **Explicación:** `StatevectorEstimator` calcula expectation values; `Sampler` devuelve distribuciones de probabilidad. → Módulo 04.

---

### B10. Número de estados base
Un registro de $n$ qubits puede representar simultáneamente:

- a) $n$ estados  
- b) $n^2$ estados  
- **c) $2^n$ estados** ✓  
- d) $n!$ estados  

> **Explicación:** Espacio de Hilbert de $n$ qubits tiene dimensión $2^n$. → Módulo 01.

---

## Nivel Intermedio (15 preguntas · 3 pt cada una)

### I1. Transformada de Fourier Cuántica
La QFT de $n$ qubits requiere aproximadamente cuántas puertas:

- a) $O(N)$ donde $N=2^n$  
- **b) $O(n^2)$** ✓  
- c) $O(n \log n)$  
- d) $O(n^3)$  

> **Explicación:** QFT usa $n$ Hadamards y $n(n-1)/2$ puertas de fase controladas. → Módulo 05.

---

### I2. Estimación de fase cuántica (QPE)
QPE con $t$ bits ancilla estima la fase $\phi$ con precisión:

- **a) $2^{-t}$** ✓  
- b) $2^{-t/2}$  
- c) $t^{-1}$  
- d) $e^{-t}$  

> **Explicación:** El registro ancilla de $t$ bits resuelve fases con separación mínima $1/2^t$. → Módulo 07.

---

### I3. VQE — Principio variacional
VQE minimiza la energía mediante:

- a) Medición directa del estado base  
- **b) Optimización clásica de parámetros del ansatz cuántico** ✓  
- c) QPE sobre el Hamiltoniano  
- d) Amplificación de amplitud del estado base  

> **Explicación:** VQE minimiza $\langle\psi(\theta)|H|\psi(\theta)\rangle$ ajustando $\theta$ con optimizador clásico. → Módulo 11.

---

### I4. Error de un qubit
Los tiempos T1 y T2 representan respectivamente:

- a) Tiempo de puerta y tiempo de lectura  
- **b) Tiempo de relajación y tiempo de decoherencia de fase** ✓  
- c) Tiempo de cooldown y tiempo de reinicio  
- d) Tasa de error de 1Q y 2Q  

> **Explicación:** T1 (relajación de energía), T2 (decoherencia de fase, incluye el efecto de T1 más dephasing puro). → Módulo 06.

---

### I5. Código de corrección de errores [[n,k,d]]
El código de Steane [[7,1,3]] codifica:

- **a) 1 qubit lógico en 7 qubits físicos con distancia 3** ✓  
- b) 7 qubits lógicos con distancia 1  
- c) 3 qubits lógicos en 7 físicos  
- d) 7 qubits con protección perfecta  

> **Explicación:** Notación [[n,k,d]]: n=qubits físicos, k=lógicos, d=distancia (errores corregibles ≤ ⌊(d-1)/2⌋). → Módulo 09.

---

### I6. Hamiltoniano de Ising
El Hamiltoniano de Ising $H = -J\sum_{i} Z_iZ_{i+1} - h\sum_i X_i$ tiene punto crítico en:

- a) $J/h = 0$  
- **b) $J/h = 1$** ✓  
- c) $J/h = \pi$  
- d) $J/h \to \infty$  

> **Explicación:** El Ising 1D transverso tiene transición de fase cuántica en $J=h$ (punto crítico). → Módulo 15.

---

### I7. Matriz de densidad
Una matriz de densidad $\rho$ es válida si y solo si:

- a) $\text{tr}(\rho) = 0$ y $\rho \geq 0$  
- **b) $\text{tr}(\rho) = 1$, $\rho \geq 0$, $\rho = \rho^\dagger$** ✓  
- c) $\rho^2 = I$  
- d) $\rho$ es unitaria  

> **Explicación:** Estado cuántico válido: hermítica, semidefinida positiva, traza 1. → Módulo 08.

---

### I8. Entropía de Von Neumann
Para un estado puro $|\psi\rangle$:

- **a) $S(\rho) = 0$** ✓  
- b) $S(\rho) = 1$  
- c) $S(\rho) = \log_2(d)$ donde $d$ es la dimensión  
- d) $S(\rho) = \text{tr}(\rho \log \rho)^{-1}$  

> **Explicación:** Estado puro: $\rho = |\psi\rangle\langle\psi|$, un solo autovalor no nulo = 1, $S = -1\log 1 = 0$. → Módulo 16.

---

### I9. QAOA p=1 sobre MAX-CUT
Para QAOA p=1 en un grafo de triángulo (3 nodos, 3 aristas), la razón de aproximación máxima es:

- a) 1.0 (solución exacta)  
- b) 0.5  
- **c) 0.75** ✓  
- d) 0.9  

> **Explicación:** QAOA p=1 garantiza razón ≥ 0.5 (trivial) para MAX-CUT; en triángulo el óptimo clásico es 2/3 de aristas, QAOA p=1 alcanza ~0.75. → Módulo 11.

---

### I10. ZNE — Extrapolación Richardson
ZNE con circuit folding a $\lambda=1,3,5$ y energías $E_1, E_3, E_5$ extrapola a $\lambda=0$ con:

- a) $E_{\text{ZNE}} = E_1$  
- **b) $E_{\text{ZNE}} = \text{polyfit}([1,3,5], [E_1,E_3,E_5], 2)$ evaluado en 0** ✓  
- c) $E_{\text{ZNE}} = (E_1 + E_3 + E_5)/3$  
- d) $E_{\text{ZNE}} = 3E_1 - 2E_3$  

> **Explicación:** Richardson cuadrático: ajuste polinómica de grado 2 en los 3 puntos, evaluado en λ=0. → Lab 24, Solución R4.

---

### I11. Información de Fisher Cuántica
Para un estado GHZ de $n$ qubits con generador $J_z = \sum Z_i/2$, la QFI es:

- a) $n$  
- **b) $n^2$** ✓  
- c) $n/4$  
- d) $2^n$  

> **Explicación:** GHZ alcanza el límite de Heisenberg $F_Q = n^2$; estado producto da solo SQL $F_Q = n$. → Módulo 38, R5.

---

### I12. Compilación KAK
Toda unitaria de 2 qubits se puede implementar con a lo sumo cuántas puertas CNOT:

- a) 2  
- **b) 3** ✓  
- c) 4  
- d) Depende de la unitaria  

> **Explicación:** Teorema KAK (Cartan): cualquier U ∈ SU(4) requiere ≤ 3 CNOT. Algunas unitarias necesitan exactamente 3. → Módulo 39.

---

### I13. Surface code — umbral
El surface code tiene umbral de error por puerta aproximadamente:

- a) 50%  
- b) 10%  
- **c) 1%** ✓  
- d) 0.1%  

> **Explicación:** Umbral empírico del surface code con decodificador MWPM: ~1%. Por debajo → corrección exponencialmente buena con d. → Módulo 29, R7.

---

### I14. Quantum Walk — propagación
El quantum walk discreto 1D con moneda Hadamard propaga con desviación estándar que escala como:

- **a) $\sigma(t) \approx t/\sqrt{2}$ (balístico)** ✓  
- b) $\sigma(t) \approx \sqrt{t}$ (difusivo)  
- c) $\sigma(t) \approx \log t$  
- d) $\sigma(t) = \text{const}$ (localización)  

> **Explicación:** QW balístico: σ ∝ t; clásico difusivo: σ ∝ √t. A t=50, cuántico es ≈7× más disperso. → Lab 34.

---

### I15. Cota Cramér-Rao
La precisión mínima al estimar un parámetro $\phi$ con $N$ mediciones y QFI $F_Q$ es:

- **a) $\sigma(\phi) \geq 1/\sqrt{N \cdot F_Q}$** ✓  
- b) $\sigma(\phi) \geq F_Q / \sqrt{N}$  
- c) $\sigma(\phi) \geq 1/(N \cdot F_Q)$  
- d) $\sigma(\phi) \geq \sqrt{F_Q / N}$  

> **Explicación:** Cota cuántica de Cramér-Rao: $\text{Var}(\hat\phi) \geq 1/(N F_Q)$. → Módulo 38, R5.

---

## Nivel Avanzado (8 preguntas · 4 pt cada una)

### A1. QSVT — Número de queries
QSVT aplica el polinomio de Chebyshev de grado $d$ a los valores singulares de una matriz $A$ block-encoded usando exactamente:

- a) $d/2$ queries a $U_A$  
- **b) $d$ queries a $U_A$ o $U_A^\dagger$** ✓  
- c) $d^2$ queries  
- d) $O(d \log d)$ queries  

> **Explicación:** QSVT usa $d$ aplicaciones alternadas de $U_A$ y $U_A^\dagger$, intercaladas con $d+1$ rotaciones de señal. → Módulo 40, R1.

---

### A2. Block-encoding — Ancilla
Para block-encodar una matriz $A \in \mathbb{C}^{N\times N}$ con $N=2^n$ mediante QR-completion, el número de ancilla qubits necesarios es:

- a) $n^2$  
- **b) $n$** ✓  
- c) $\log_2 N$  
- d) $2n$  

> **Explicación:** QR-completion dobla el espacio (U de tamaño 2N×2N), lo que requiere 1 qubit adicional por registro → $n$ ancilla. → R2.

---

### A3. Barren plateaus — Escalado
Para un ansatz 2-diseño de $n$ qubits, la varianza del gradiente escala como:

- a) $O(1/n)$  
- b) $O(1/n^2)$  
- **c) $O(4^{-n})$ (exponencial en $n$)** ✓  
- d) $O(e^{-n/2})$  

> **Explicación:** Teorema de McClean et al. 2018: para 2-diseños globales, $\text{Var}[\partial E/\partial\theta] \leq 2/4^n$. → R3.

---

### A4. HHL — Complejidad
El algoritmo HHL resuelve $Ax=b$ (A de $N\times N$, condición $\kappa$) con complejidad:

- a) $O(N\kappa^2)$  
- **b) $O(\log N \cdot \kappa^2 / \varepsilon)$** ✓  
- c) $O(\sqrt{N}\kappa)$  
- d) $O(N^2)$  

> **Explicación:** Speedup exponencial en $N$ via QPE; dependencia cuadrática en $\kappa$ (solvable con preconditioning). La ventaja requiere lectura eficiente del resultado. → Módulo 40.

---

### A5. Advantage cuántica — lower bound Grover
El lower bound de Grover (Bennett et al. 1997) establece que búsqueda en base desordenada de $N$ elementos requiere:

- **a) $\Omega(\sqrt{N})$ queries cuánticas** ✓  
- b) $\Omega(N/\log N)$ queries  
- c) $\Omega(\log^2 N)$ queries  
- d) $\Omega(N^{2/3})$ queries  

> **Explicación:** Demostrado con el método polinómica (Beals et al.): ningún algoritmo cuántico puede superar $O(\sqrt{N})$ para búsqueda sin estructura. → R8.

---

### A6. QML — Kernel Target Alignment
El Kernel Target Alignment (KTA) se define como:

- a) $\text{KTA}(K,y) = \|K\|_F / \|yy^T\|_F$  
- **b) $\text{KTA}(K,y) = \langle K, yy^T\rangle_F / (\|K\|_F \|yy^T\|_F)$** ✓  
- c) $\text{KTA}(K,y) = \text{tr}(K \cdot yy^T)$  
- d) $\text{KTA}(K,y) = \max_{i,j} K_{ij} \cdot y_i y_j$  

> **Explicación:** KTA es la correlación de Frobenius entre K y el kernel ideal $yy^T$; KTA=1 → alineación perfecta. → R6.

---

### A7. Fault tolerance — Magic state distillation
El protocolo 15-to-1 de destilación de estados T produce un estado T de fidelidad:

- a) $p_{\text{out}} = 15 p_{\text{in}}$  
- **b) $p_{\text{out}} \approx 35 p_{\text{in}}^3$** ✓  
- c) $p_{\text{out}} = p_{\text{in}}^{15}$  
- d) $p_{\text{out}} = p_{\text{in}} / 15$  

> **Explicación:** 15-to-1 Bravyi-Kitaev: consume 15 estados T con error $p$ y produce 1 con error $\approx 35p^3$, permitiendo reducción iterativa. → R7.

---

### A8. Ventaja cuántica práctica — Estado actual (2025)
¿Cuál de los siguientes problemas tiene ventaja cuántica **práctica demostrada** en hardware real hoy (2025)?

- a) Factorización RSA-2048  
- b) Optimización de portafolio real de 1000 activos  
- **c) Ninguno con ventaja práctica demostrada sobre el mejor clásico** ✓  
- d) Machine learning sobre datasets MNIST  

> **Explicación:** La ventaja cuántica es actualmente solo "demostrativa" (RCS, Boson Sampling). Ningún algoritmo cuántico ha resuelto un problema útil más rápido que el mejor clásico actual. → R8.

---

## Bonus — Investigación (2 preguntas · 1.5 pt cada parte)

### R1. QSVT vs LCU-Taylor para sgn(A)
**Parte a)** ¿Por qué QSVT supera a LCU-Taylor para aproximar $\text{sgn}(A)$ con $\|A\| \leq 1$ cuando $\delta \ll 1$?

> **Respuesta:** QSVT usa el polinomio de Chebyshev óptimo de grado $d = O(\log(1/\varepsilon)/\delta)$, mientras que LCU-Taylor necesita norma-1 $O(1/\delta)$ → overhead exponencialmente mayor en $1/\delta$. → R1.

**Parte b)** Para $\delta=0.1$, $\varepsilon=10^{-4}$: ¿cuántas queries necesita QSVT?

> **Respuesta:** $d = \lceil 4\ln(1/\delta)/\pi^2 \cdot \ln(1/\varepsilon)\rceil \approx \lceil 4\ln 10/\pi^2 \cdot 4\ln 10\rceil \approx 43$ queries.

---

### R2. Barren plateaus — Mitigación
**Parte a)** Explica por qué la inicialización "identity blocks" mitiga los barren plateaus.

> **Respuesta:** Si todos los parámetros son 0, el ansatz implementa la identidad y el gradiente en $\theta=0$ es de orden $O(1)$ (no exponencialmente pequeño). La zona plana aparece para puntos aleatorios del espacio de parámetros, no en $\theta \approx 0$.

**Parte b)** ¿Para qué tipo de observable no hay barren plateau incluso con circuitos profundos?

> **Respuesta:** Para observables locales (1-2 qubits), Cerezo et al. (2021) demostró que $\text{Var}[\partial E/\partial\theta] \propto 1/L$ (decaimiento polinómico, no exponencial), por lo que QAOA con costo local no sufre barren plateaus.

---

## Tabla de corrección

| Nivel | Preguntas | Pts cada | Total |
|---|---|---|---|
| Básico | 10 | 2 | 20 |
| Intermedio | 15 | 3 | 45 |
| Avanzado | 8 | 4 | 32 |
| Bonus | 2 × 2 partes | 1.5 | 6 |
| **TOTAL** | | | **103** |

| Clasificación | Puntuación |
|---|---|
| No certificado | < 60 pt |
| 🥉 Nivel Básico | 60–79 pt |
| 🥈 Nivel Avanzado | 80–91 pt |
| 🥇 Nivel Investigador | ≥ 92 pt |

---

*Examen generado automáticamente · [Computación Cuántica: Teoría y Práctica](https://github.com/LegalIntermediaSL/ComputacionCuantica)*
