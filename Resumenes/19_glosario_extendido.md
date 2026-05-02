# Resumen 19 — Glosario Extendido

> Términos adicionales no incluidos en `glosario.md`. 50 entradas clave del vocabulario avanzado de computación cuántica.

---

## F

**Fault-tolerant quantum computing (FTQC):** Paradigma en el que errores son corregidos en tiempo real durante la computación, permitiendo ejecución arbitrariamente larga. Requiere tasa de error físico $p < p_{th}$ y overhead de ~1000 qubits físicos por lógico con surface codes actuales.

**Fidelity (fidelidad):** Medida de similitud entre dos estados cuánticos: $F(\rho,\sigma)=\left(\mathrm{Tr}\sqrt{\sqrt{\rho}\sigma\sqrt{\rho}}\right)^2$. Para estados puros $F(|\psi\rangle,|\phi\rangle)=|\langle\psi|\phi\rangle|^2 \in [0,1]$.

**Flag qubit:** Qubit ancilla que detecta errores de alto peso generados durante la medida de síndromes, evitando la necesidad de medir estabilizadores de peso mayor.

**Floquet engineering:** Irradiación periódica de un sistema cuántico para crear Hamiltonianos efectivos con propiedades deseadas (topología, magnetismo artificial). Usado en simuladores cuánticos con átomos ultrafríos.

**Free fermion:** Sistema de fermiones sin interacciones cuyo Hamiltoniano es cuadrático en operadores de creación/aniquilación. Simulable clásicamente en tiempo polinomial (Valiant 2001).

---

## I

**IQP (Instantaneous Quantum Polynomial):** Clase de circuitos de la forma $H^{\otimes n} D H^{\otimes n}$ donde $D$ es diagonal en la base computacional. Su muestreo se cree que es #P-hard clásicamente. Usado en QNLP y boson sampling análogo.

**Ising model:** $H_\text{Ising} = -J\sum_{\langle i,j\rangle}\sigma_i^z\sigma_j^z - h\sum_i\sigma_i^z$. El problema de encontrar el estado fundamental es NP-hard en grafos arbitrarios y es la base del annealing cuántico.

---

## N

**Naimark dilation:** Extensión de una POVM $\{M_i\}$ a una medida proyectiva en un espacio mayor. Si $\sum_i M_i^\dagger M_i = I$, existe un espacio ancilla y un unitario $U$ tal que $P_i = U^\dagger (|i\rangle\langle i|\otimes I) U$ implementa la POVM por medida proyectiva.

**Non-Clifford gate:** Puerta cuántica que no pertenece al grupo de Clifford (H, S, CNOT). Las más importantes son la puerta T ($R_Z(\pi/4)$) y Toffoli. Son el recurso fundamental para la computación universal tolerante a fallos.

**Normal ordering:** En teoría cuántica de campos, convención de reordenar operadores de campo poniendo los de creación a la izquierda. Elimina las divergencias de energía del vacío. $:\hat{a}^\dagger\hat{a}: = \hat{a}^\dagger\hat{a}$ (sin término de punto cero).

---

## P

**Pegasus topology:** Topología de chip de D-Wave Advantage: 5627 qubits con conectividad ~15 (cada qubit conectado a hasta 15 vecinos). Permite embedding más eficiente que la topología Chimera anterior.

**Permanente:** Análogo al determinante sin signos alternantes: $\mathrm{Perm}(A)=\sum_{\sigma\in S_n}\prod_i A_{i,\sigma(i)}$. Computar el permanente es #P-completo (Valiant 1979), base de la dificultad del Boson Sampling.

**Post-selection:** Condicionamiento de resultados sobre un outcome específico de la medida. En MBQC y QNLP, la post-selección en $|0\rangle$ implementa operaciones de "cup" que contraen los índices del tensor.

**Primitividad V2:** API de Qiskit 2.x: `StatevectorEstimator` y `StatevectorSampler`. Implementan la interfaz primitiva estándar aislando al usuario del backend subyacente.

**PRISM (Phase Randomized Ising Sampling Machine):** Alternativa clásica al boson sampling basada en redes Ising con fases aleatorias. Propuesta para falsear muestras boson sampling en hardware clásico.

---

## Q

**Quantum channel capacity:** Capacidad máxima de transmisión de información cuántica de un canal ruidoso $\mathcal{E}$. La capacidad cuántica $Q(\mathcal{E}) = \lim_{n\to\infty}\frac{1}{n}I_c(\rho^{\otimes n}, \mathcal{E}^{\otimes n})$ es difícil de calcular y no-aditiva en general.

**Quantum chromatic number:** Versión cuántica del número cromático de un grafo. Puede ser estrictamente menor que el clásico usando estrategias entrelazadas, ejemplo de ventaja cuántica en teoría de grafos.

**Quantum discord:** Medida de correlaciones cuánticas más allá del entrelazamiento: $\mathcal{D}(\rho_{AB}) = I(A:B) - J(A:B)$ donde $J$ es la información clásica. Un estado puede tener discord positivo pero sin entrelazamiento.

**Quantum Fisher Information (QFI):** $F_Q(\rho,H) = 2\sum_{k,l}\frac{(\lambda_k-\lambda_l)^2}{\lambda_k+\lambda_l}|\langle k|H|l\rangle|^2$. Cota la precisión de estimación de parámetros: $\Delta\theta \geq 1/\sqrt{N F_Q}$ (límite de Cramér-Rao cuántico).

**Quantum volume (QV):** Métrica de IBM para capacidad total del procesador. $QV = 2^n$ donde $n$ es el máximo número de qubits tal que un circuito cuadrado $n\times n$ aleatorio se ejecuta con >2/3 del resultado ideal en muestreo.

---

## R

**Readout error:** Error al medir un qubit: $|0\rangle$ leído como $1$ con probabilidad $\varepsilon_0$, $|1\rangle$ leído como $0$ con probabilidad $\varepsilon_1$. En procesadores IBM Heron r2: $\varepsilon \sim 0.5\%$. Mitigable con matriz de asignación.

**Resource state:** Estado cuántico que se consume durante la computación. En MBQC, el estado cluster es el resource state universal. En magic state distillation, los estados de magia $|T\rangle$ son el recurso para puertas no-Clifford.

**Rydberg blockade radius:** $r_b = (C_6/\hbar\Omega)^{1/6}$. Dos átomos dentro de $r_b$ no pueden estar simultáneamente en el estado Rydberg. Base del gate CZ nativo en arrays de Rydberg.

---

## S

**Sampling advantage:** Ventaja cuántica basada en la dificultad de muestrear la distribución de salida de un circuito cuántico. Demonstrada por Google (2019, RCS), USTC (2020, GBS). La ventaja en *tareas útiles* permanece por demostrar.

**Scar state (quantum scar):** Estado de alta energía con baja entropía de entrelazamiento que evita la termalización (viola la hipótesis ETH). Encontrados en el modelo PXP de átomos Rydberg (Bernien 2017). Permiten evolución coherente prolongada.

**Shot noise:** Ruido estadístico en la estimación de observables por muestreo. Escala como $\sim 1/\sqrt{N_\text{shots}}$. Para precisión $\varepsilon$ se necesitan $N_\text{shots} \sim 1/\varepsilon^2$ disparos.

**Stabilizer code:** Código cuántico definido por un grupo abeliano $\mathcal{S} \subset P_n$ de operadores de Pauli. El espacio de código es el espacio $+1$ de todos los estabilizadores: $\mathcal{H}_L = \{|\psi\rangle: S|\psi\rangle=|\psi\rangle \; \forall S\in\mathcal{S}\}$.

**String diagram:** Representación gráfica en teoría de categorías monoidal. Las cajas son morfismos, las líneas son objetos, la composición es conexión vertical y el producto tensorial es colocación horizontal.

---

## T

**T gate:** $T = \begin{pmatrix}1&0\\0&e^{i\pi/4}\end{pmatrix} = R_Z(\pi/4)$. Es la puerta no-Clifford más simple. En circuitos tolerantes a fallos, implementar $T$ requiere destilación de magic states (overhead ~100-1000×).

**Tanner graph:** Grafo bipartito representando un código LDPC. Nodos variables (bits/qubits) en un lado, nodos de restricción (checks) en el otro. Una arista $(v,c)$ indica que el bit $v$ participa en el check $c$. El nombre viene del trabajo de Tanner (1981).

**Threshold (umbral):** Tasa de error físico crítico $p_{th}$ por debajo de la cual el error lógico decrece al aumentar el tamaño del código. Surface code: $p_{th}\approx 1\%$ (Pauli), $\approx 0.5\%$ (circuito). BB codes: $p_{th}\approx 0.5-0.7\%$.

**Topological order:** Fase de la materia cuántica caracterizada por entrelazamiento de largo rango, degeneración topológica del estado fundamental (depende del género de la variedad) e inmunidad a perturbaciones locales. Base de la computación topológica.

---

## Z

**Zero-noise extrapolation (ZNE):** Técnica de mitigación de errores. Se escala el ruido artificialmente ($\lambda = 1, 2, 3$) y se extrapola a ruido cero: $E_\text{ideal} \approx p(\lambda\to 0)$ con extrapolación de Richardson o exponencial.

**ZX-calculus:** Lenguaje gráfico para computación cuántica con dos tipos de nodos (verde=Z, rojo=X) y reglas de reescritura completas para el cálculo cuántico. Permite simplificar circuitos, verificar equivalencias y compilar directamente a puertas nativas.
