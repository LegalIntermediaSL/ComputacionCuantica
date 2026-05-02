# Resumen 20 — Matemáticas Esenciales para Computación Cuántica

> Referencia rápida de los fundamentos matemáticos: álgebra lineal, grupos de Lie, funciones de Green y análisis de Fourier sobre grupos.

---

## 1. Álgebra Lineal Cuántica

### Teorema espectral
Para toda matriz hermítica $H = H^\dagger$ existe una base ortonormal de autovectores $\{|n\rangle\}$ con autovalores reales $\lambda_n \in \mathbb{R}$:
$$H = \sum_n \lambda_n |n\rangle\langle n|$$

**Aplicación:** Los observables cuánticos son hermíticos; sus autovalores son los posibles resultados de la medida.

### Descomposición en valores singulares (SVD)
Para toda matriz $A \in \mathbb{C}^{m\times n}$:
$$A = U \Sigma V^\dagger, \quad U \in U(m), \; V \in U(n), \; \Sigma = \mathrm{diag}(\sigma_1,\ldots,\sigma_r) \geq 0$$

**Aplicación en QSVT:** La transformación cuántica de valores singulares aplica polinomios $P(\sigma_i)$ a los valores singulares de un operador bloque-codificado.

### Producto tensorial
Para $A \in \mathcal{L}(\mathcal{H}_A)$, $B \in \mathcal{L}(\mathcal{H}_B)$:
$$(A \otimes B)(|v\rangle \otimes |w\rangle) = A|v\rangle \otimes B|w\rangle$$

Dimensiones: $\dim(\mathcal{H}_A \otimes \mathcal{H}_B) = \dim(\mathcal{H}_A) \cdot \dim(\mathcal{H}_B)$.

**Propiedad:** $(A\otimes B)(C\otimes D) = AC \otimes BD$.

### Traza parcial
Para un estado bipartito $\rho_{AB}$, el estado reducido de $A$ es:
$$\rho_A = \mathrm{Tr}_B(\rho_{AB}) = \sum_k (\mathbb{I}_A \otimes \langle k|_B) \rho_{AB} (\mathbb{I}_A \otimes |k\rangle_B)$$

### Entropía de von Neumann
$$S(\rho) = -\mathrm{Tr}(\rho \log_2 \rho) = -\sum_i \lambda_i \log_2 \lambda_i$$

donde $\lambda_i$ son los autovalores de $\rho$. Mide el entrelazamiento: $S(\rho_A) = S(\rho_B)$ para estados puros bipartitos.

---

## 2. Grupos de Lie y Álgebras

### SU(2) — Qubit single
El grupo especial unitario de $2\times 2$ matrices complejas con $\det=1$:
$$SU(2) = \left\{U = \begin{pmatrix}\alpha&-\beta^*\\\beta&\alpha^*\end{pmatrix}: |\alpha|^2+|\beta|^2=1\right\} \cong S^3$$

**Álgebra de Lie** $\mathfrak{su}(2)$: generada por $\{iX, iY, iZ\}/2$ con relaciones de conmutación:
$$[X,Y] = 2iZ, \quad [Y,Z] = 2iX, \quad [Z,X] = 2iY$$

**Mapa exponencial:** $U(\hat{n},\theta) = e^{-i\theta\hat{n}\cdot\boldsymbol{\sigma}/2} = \cos\frac{\theta}{2}I - i\sin\frac{\theta}{2}(\hat{n}\cdot\boldsymbol{\sigma})$

### SU(4) — Sistema de 2 qubits
Dimensión $\dim SU(4) = 15$, base de $\mathfrak{su}(4)$: las 15 matrices de Pauli de 2 qubits $\{I,X,Y,Z\}^{\otimes 2} \setminus \{I\otimes I\}$ multiplicadas por $i/2$.

**Decomposición KAK:** Todo $U \in SU(4)$ puede escribirse como:
$$U = (A_1 \otimes A_2) \cdot e^{i(c_x XX + c_y YY + c_z ZZ)} \cdot (B_1 \otimes B_2)$$

con $A_i, B_i \in SU(2)$ y $c_x, c_y, c_z \in \mathbb{R}$. Esta descomposición es la base de la síntesis óptima de puertas 2Q.

### SO(3) vs SU(2)
$SU(2)$ es el **doble cubrimiento** de $SO(3)$: el homomorfismo $\phi: SU(2) \to SO(3)$ tiene kernel $\{I,-I\}$. Un qubit rota $2\pi$ antes de volver al estado inicial (fase global $-1$), pero los observables son invariantes bajo rotaciones de $2\pi$.

---

## 3. Funciones de Green y Propagadores

### Propagador cuántico
El propagador es el núcleo del operador de evolución temporal:
$$K(x',t';x,t) = \langle x'|e^{-iH(t'-t)/\hbar}|x\rangle = \sum_n \psi_n(x')\psi_n^*(x)e^{-iE_n(t'-t)/\hbar}$$

### Función de Green retardada
$$G^R(E) = \frac{1}{E - H + i\eta}, \quad \eta \to 0^+$$

La densidad de estados es: $\rho(E) = -\frac{1}{\pi}\mathrm{Im}\,\mathrm{Tr}[G^R(E)]$.

**Aplicación en QSVT:** La inversión de matriz $(H+i\eta)^{-1}$ puede implementarse cuánticamente con QSVT aplicando la función $f(\sigma) = 1/\sigma$ mediante polinomios de Chebyshev.

### Fórmula de Dyson
Para $H = H_0 + V$:
$$G = G_0 + G_0 V G = G_0 + G_0 V G_0 + G_0 V G_0 V G_0 + \cdots$$

Base de la teoría de perturbaciones. El método de Trotterización implementa una aproximación a $e^{-iHt}$ análoga a la serie de Dyson truncada.

---

## 4. Fourier sobre Grupos

### Transformada de Fourier cuántica (QFT)
Para el grupo $\mathbb{Z}_{2^n}$, la QFT es:
$$\text{QFT}|j\rangle = \frac{1}{\sqrt{2^n}}\sum_{k=0}^{2^n-1} e^{2\pi ijk/2^n}|k\rangle$$

Implementable en $O(n^2)$ puertas (vs $O(n\cdot 2^n)$ para FFT clásica). Base de Phase Estimation, Shor y HHL.

### Análisis armónico sobre $SU(2)$
Las **representaciones irreducibles** de $SU(2)$ son las representaciones de espín $j = 0, 1/2, 1, 3/2, \ldots$, de dimensión $2j+1$. Los caracteres son:
$$\chi_j(U) = \frac{\sin((2j+1)\theta/2)}{\sin(\theta/2)}, \quad U \sim e^{-i\theta\hat{n}\cdot\boldsymbol{\sigma}/2}$$

**Aplicación:** La randomized benchmarking usa la estructura de grupo de $SU(2)$ para aislar el error de depolarización del ruido de estado y medida.

### Transformada de Hadamard-Walsh
Para el grupo $(\mathbb{Z}_2)^n$:
$$H^{\otimes n}|x\rangle = \frac{1}{\sqrt{2^n}}\sum_{y \in \{0,1\}^n} (-1)^{x\cdot y}|y\rangle$$

Base del algoritmo de Deutsch-Jozsa, Simon y BV. Relacionada con la teoría de códigos binarios (código dual).

---

## 5. Herramientas de Análisis Matricial

### Desigualdad de Golden-Thompson
$$\mathrm{Tr}(e^{A+B}) \leq \mathrm{Tr}(e^A e^B) \quad \text{para } A,B \text{ hermíticas}$$

Implica que la fórmula de Trotter $e^{-i(A+B)t} \approx (e^{-iAt/n}e^{-iBt/n})^n$ tiene error $O(t^2/n)$.

### Fórmula de Baker-Campbell-Hausdorff (BCH)
$$e^X e^Y = e^{X+Y+\frac{1}{2}[X,Y]+\frac{1}{12}([X,[X,Y]]-[Y,[X,Y]])+\cdots}$$

El error de Trotter de primer orden es: $e^{A}e^{B} = e^{A+B+\frac{1}{2}[A,B]+O(\|A\|^2\|B\|+\|A\|\|B\|^2)}$.

### Norma de traza y norma espectral
- Norma de traza: $\|A\|_1 = \mathrm{Tr}\sqrt{A^\dagger A} = \sum_i\sigma_i$  
- Norma espectral (operador): $\|A\|_\infty = \sigma_\text{max}$  
- Norma de Frobenius: $\|A\|_F = \sqrt{\mathrm{Tr}(A^\dagger A)} = \sqrt{\sum_i\sigma_i^2}$

**Relación:** $\|A\|_\infty \leq \|A\|_F \leq \|A\|_1 \leq \sqrt{r}\,\|A\|_F$ donde $r = \mathrm{rank}(A)$.

### Distancia en traza
$$T(\rho,\sigma) = \frac{1}{2}\|\rho-\sigma\|_1 \in [0,1]$$

Satisface: $T(\rho,\sigma) = 0 \iff \rho = \sigma$, y $T(\mathcal{E}(\rho),\mathcal{E}(\sigma)) \leq T(\rho,\sigma)$ para cualquier canal cuántico $\mathcal{E}$ (no aumenta por operaciones).
