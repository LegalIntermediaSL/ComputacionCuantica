# Módulo 42 — Tensor Networks y DMRG

## Índice

1. [Motivación: el problema de la maldición de la dimensionalidad](#1-motivación)
2. [Tensores y notación diagramática](#2-notación-diagramática)
3. [Matrix Product States (MPS)](#3-matrix-product-states)
4. [Descomposición de Schmidt y entrelazamiento](#4-schmidt-y-entrelazamiento)
5. [Area law: por qué MPS funciona en 1D](#5-area-law)
6. [Operaciones con MPS: contracción y canonicalización](#6-operaciones-con-mps)
7. [DMRG: algoritmo variacional sobre MPS](#7-dmrg)
8. [TEBD: evolución temporal con MPS](#8-tebd)
9. [Más allá de 1D: PEPS, MERA, árbol tensor](#9-más-allá-de-1d)
10. [Conexión con computación cuántica](#10-conexión-qc)

---

## 1. Motivación

El espacio de Hilbert de $n$ qubits tiene dimensión $2^n$. Para $n = 50$, el vector de estado completo requiere $2^{50} \approx 10^{15}$ amplitudes complejas — más de un petabyte de memoria. Esto hace que la simulación clásica exacta sea inviable para más de ~50 qubits.

Sin embargo, **la mayoría de los estados físicamente relevantes** (estados de baja energía de Hamiltonianos locales) tienen muy poco entrelazamiento. Las redes tensoriales explotan esta estructura para representar estados de forma eficiente.

**Aplicaciones en computación cuántica:**
- Simular circuitos cuánticos con MPS (precisión controlada por la dimensión de enlace χ).
- Entender los límites del poder cuántico (dequantization, levantamiento de rangos bajos).
- DMRG como referencia para VQE — el benchmark clásico para moléculas 1D.
- Compresión de circuitos: cualquier circuito de baja profundidad puede representarse como MPS de χ pequeño.

---

## 2. Notación diagramática

Un tensor de orden k es un array multidimensional $T_{i_1 i_2 \ldots i_k}$. La notación diagramática representa tensores como nodos y contracciones como líneas que los conectan:

```
Estado |ψ⟩ de 4 qubits:
     i₁  i₂  i₃  i₄
      │   │   │   │
    ┌─────────────────┐
    │      ψ          │
    └─────────────────┘

Descomposición como MPS:
     i₁      i₂      i₃      i₄
      │        │        │        │
    ┌─┐  α₁ ┌─┐  α₂ ┌─┐  α₃ ┌─┐
    │A│──────│B│──────│C│──────│D│
    └─┘      └─┘      └─┘      └─┘
```

- Los índices físicos $i_k \in \{0, 1\}$ tienen dimensión $d = 2$.
- Los índices de enlace (bond) $\alpha_k$ tienen dimensión $\chi$ (dimensión de enlace o bond dimension).
- La contracción completa de los índices de enlace recupera las $2^n$ amplitudes del estado.

### Contracción de tensores

El producto escalar $\langle\phi|\psi\rangle$ se calcula contrayendo todos los índices físicos y de enlace:

$$\langle\phi|\psi\rangle = \sum_{i_1 \ldots i_n} \sum_{\alpha_1 \ldots \alpha_{n-1}} \phi^*_{i_1 \ldots i_n} \psi_{i_1 \ldots i_n}$$

Con MPS, el coste de esta contracción es $O(n \chi^3)$ en lugar de $O(2^n)$.

---

## 3. Matrix Product States (MPS)

Un estado de $n$ qubits en forma MPS se escribe como:

$$|\psi\rangle = \sum_{i_1, \ldots, i_n = 0}^{1} A^{[1]}_{i_1} A^{[2]}_{i_2} \cdots A^{[n]}_{i_n} |i_1 i_2 \cdots i_n\rangle$$

donde:
- $A^{[k]}_{i_k}$ es una **matriz** de dimensión $\chi_{k-1} \times \chi_k$ (con $\chi_0 = \chi_n = 1$ en los extremos).
- $\chi = \max_k \chi_k$ es la **dimensión de enlace** (bond dimension).

### Parámetros

| Descripción | Valor |
|-------------|-------|
| Número de tensores | $n$ |
| Dimensión máxima de cada tensor | $d \times \chi^2 = 2\chi^2$ |
| Parámetros totales | $O(n d \chi^2) = O(n \chi^2)$ |
| Estado completo (exacto) | $O(d^n) = O(2^n)$ |

Para $\chi = 1$: estados producto (sin entrelazamiento).  
Para $\chi = 2^{n/2}$: estado arbitrario (sin ganancia).  
Para $\chi \ll 2^{n/2}$: aproximación eficiente si el entrelazamiento es bajo.

### Ejemplos de estados y su χ exacto

| Estado | χ exacto | Descripción |
|--------|----------|-------------|
| Estado producto $|0\rangle^{\otimes n}$ | 1 | Sin entrelazamiento |
| Estado Bell $|\Phi^+\rangle$ (2 qubits) | 2 | Entrelazamiento máximo 2Q |
| Estado GHZ $\frac{1}{\sqrt{2}}(|0\rangle^n + |1\rangle^n)$ | 2 | Entrelazamiento multipartita |
| Estado W $\frac{1}{\sqrt{n}}\sum_k |0\cdots 1_k \cdots 0\rangle$ | $\sqrt{n}$ | Entrelazamiento distribuido |
| Estado genérico | $2^{n/2}$ | Sin estructura útil |

---

## 4. Descomposición de Schmidt y entrelazamiento

La **descomposición de Schmidt** de un estado bipartito $|\psi\rangle_{AB}$ es:

$$|\psi\rangle = \sum_{k=1}^{\chi} \lambda_k |u_k\rangle_A \otimes |v_k\rangle_B, \quad \lambda_k \geq 0, \quad \sum_k \lambda_k^2 = 1$$

donde $\chi$ es el **rango de Schmidt** — mide el entrelazamiento entre A y B.

### Relación con SVD

Dada la matriz de coeficientes $M_{(i_1 \ldots i_m)(i_{m+1} \ldots i_n)}$, la SVD nos da directamente los valores de Schmidt:

$$M = U \Sigma V^\dagger, \quad \lambda_k = \Sigma_{kk}$$

Los valores singulares $\lambda_k$ decrecen rápidamente para estados de baja energía. Truncar a los primeros $\chi$ da la mejor aproximación de rango $\chi$:

$$\text{Error} = \|\psi - \psi_\chi\|^2 = \sum_{k > \chi} \lambda_k^2$$

### Entropía de entrelazamiento

$$S_A = -\sum_k \lambda_k^2 \log_2(\lambda_k^2)$$

- $S_A = 0$: estado producto (sin entrelazamiento entre A y B).
- $S_A = \log_2 \chi$: estado maximalente entrelazado con rango de Schmidt $\chi$.

---

## 5. Area Law

**Teorema** (Hastings 2007): Para Hamiltonianos locales gapped en 1D, el estado fundamental satisface:

$$S_A(L) \leq c \cdot \xi \log \xi$$

donde $\xi$ es la longitud de correlación y $c$ es una constante. En particular:

- **Para sistemas con gap de energía:** $S_A \leq \text{cte}$ (independiente de $L$).
- **Para sistemas críticos (sin gap):** $S_A \sim \frac{c}{3} \log L$ (ley de área logarítmica, CFT).

### Consecuencia práctica

Un MPS con dimensión de enlace $\chi \approx \exp(S_A)$ puede representar el estado fundamental con error exponencialmente pequeño. Para sistemas gapped:

$$\chi \sim \exp(\text{cte}) \Rightarrow \text{coste clásico polinomial en } n$$

Esto explica por qué DMRG funciona tan bien para cadenas de spín 1D gapped.

---

## 6. Operaciones con MPS

### Forma canónica izquierda (left-canonical)

Un MPS está en **forma canónica izquierda** si para cada sitio $k$:

$$\sum_{i_k, \alpha_{k-1}} (A^{[k]}_{i_k})^\dagger A^{[k]}_{i_k} = I_{\chi_k}$$

Equivalente a que los tensores forman isometrias hacia la derecha. Se obtiene aplicando SVD recursivamente de izquierda a derecha.

### Truncamiento durante SVD

Para comprimir un MPS a bond dimension $\chi_{\max}$:

1. Descomponer el tensor del sitio $k$ en SVD: $M^{[k]} = U_k S_k V_k^\dagger$.
2. Retener solo los $\chi_{\max}$ valores singulares más grandes.
3. Actualizar $A^{[k]} = U_k$ y $A^{[k+1]} \leftarrow S_k V_k^\dagger A^{[k+1]}$.

### Valor esperado con MPO

Un operador local $H = \sum_k h_k$ puede representarse como **Matrix Product Operator** (MPO). El valor esperado es:

$$\langle\psi|H|\psi\rangle = \text{contracción de la red tensor (bra, MPO, ket)}$$

Coste: $O(n \chi^2 \chi_W^2 d)$, donde $\chi_W$ es la dimensión de enlace del MPO (típicamente pequeña para Hamiltonianos locales).

---

## 7. DMRG: algoritmo variacional sobre MPS

DMRG (Density Matrix Renormalization Group, White 1992) es un algoritmo de optimización variacional que minimiza $\langle\psi|H|\psi\rangle$ sobre el espacio de MPS de bond dimension $\chi$.

### Algoritmo (two-site DMRG)

```
Inicializar MPS aleatorio |ψ₀⟩ con bond dim χ

Para cada barrido (sweep):
    De izquierda a derecha (→):
        Para cada par de sitios (k, k+1):
            1. Construir el tensor efectivo "super-block" Θ = A[k]A[k+1]
            2. Resolver eigenproblema: H_eff Θ = E Θ  (Lanczos, costo O(χ³))
            3. SVD(Θ) → truncar a χ más grandes → actualizar A[k], A[k+1]
            4. Mover el "centro" a la derecha
    De derecha a izquierda (←):
        Mismo proceso en sentido contrario

Criterio de convergencia: |E[barrido k] - E[barrido k-1]| < ε
```

### Complejidad

| Operación | Coste |
|-----------|-------|
| Eigenproblema local | $O(\chi^3 d^2 + \chi^2 d^3)$ |
| Barrido completo (n sitios) | $O(n \chi^3 d^2)$ |
| Total (convergencia en B barridos) | $O(B n \chi^3)$ |

Para $\chi = 100$ y $n = 1000$: ~$10^9$ operaciones por barrido — factible en minutos.

---

## 8. TEBD: evolución temporal con MPS

**Time-Evolving Block Decimation** (Vidal 2003) simula la evolución $e^{-iHt}|\psi_0\rangle$ de estados MPS bajo un Hamiltoniano local.

Para $H = \sum_k h_{k,k+1}$ (Hamiltoniano de vecinos próximos):

1. **Descomposición de Trotter:** $e^{-iHt} \approx \prod_k e^{-ih_{k,k+1}\Delta t} + O(\Delta t^2)$.
2. **Capa par:** aplicar $e^{-ih_{2k,2k+1}\Delta t}$ para k=0,1,2,...
3. **Capa impar:** aplicar $e^{-ih_{2k+1,2k+2}\Delta t}$ para k=0,1,...
4. **Truncar** los valores singulares que crecen durante cada paso → mantener bond dimension $\chi$.

### Error de Trotter

$$\|e^{-iHt} - U_{\text{Trotter}}\| = O\left(\frac{t^3}{M^2}\right)$$

para $M$ pasos de tamaño $\Delta t = t/M$.

---

## 9. Más allá de 1D

Para sistemas 2D o de alta geometría, los MPS son ineficientes. Extensiones:

| Método | Geometría | Complejidad | Estado |
|--------|-----------|-------------|--------|
| MPS | 1D | Polinomial | ✅ Maduro |
| PEPS (2D MPS) | 2D | $O(\chi^{10})$ | ⚠️ Caro |
| MERA | Críticos 1D | $O(\chi^7)$ | ✅ Funcional |
| Árbol tensor | Árbol | $O(n \chi^3)$ | ✅ Funcional |
| TTN (Tree TN) | Jerárquico | $O(\chi^3)$ | ✅ Funcional |

**En 2D:** el área law implica $S_A \sim L$ (proporcional al perímetro), por lo que χ escala exponencialmente con L. PEPS puede representarlo exactamente pero la contracción es #P-difícil.

---

## 10. Conexión con computación cuántica

### Simulación de circuitos

Un circuito de profundidad $d$ sobre $n$ qubits inicializados en $|0\rangle^n$ produce un estado MPS de bond dimension $\chi \leq 2^d$. Para $d \ll n$: simulación eficiente con TEBD.

**Límite:** Para demostrar ventaja cuántica, los circuitos deben tener $d = \Omega(\log n)$ Y generar entrelazamiento que crezca rápido (circuitos de aleatoriedad cuántica, RCS).

### Dequantización

Tang (2019) mostró que algunos algoritmos cuánticos de ML basados en muestreo con estados MPS pueden ser *dequantizados* — existe un algoritmo clásico igualmente eficiente. Esto refuerza que la ventaja cuántica requiere acceso a estados con alto entrelazamiento genuino.

### VQE vs DMRG

Para moléculas 1D o cadenas de Hubbard 1D:

- **DMRG:** exacto hasta $\epsilon$ para $\chi$ suficientemente grande; no necesita gradiente.
- **VQE:** limitado por profundidad del circuito y ruido; generalizable a hardware real.
- **Regla práctica:** DMRG gana para L ≤ 100 sitios en 1D; VQE puede ganar cuando el sistema es 2D o cuando el estado objetivo tiene estructura de baja profundidad de circuito.

### Referencias clave

1. White, S. (1992). *Density matrix formulation for quantum renormalization groups*. PRL 69, 2863.
2. Vidal, G. (2003). *Efficient classical simulation of slightly entangled quantum computations*. PRL 91, 147902.
3. Hastings, M. (2007). *Area laws in quantum systems*. J. Stat. Mech. P08024.
4. Schollwöck, U. (2011). *The density-matrix renormalization group in the age of matrix product states*. Ann. Phys. 326, 96.
5. Orús, R. (2014). *A practical introduction to tensor networks*. Ann. Phys. 349, 117.
