# Módulo 47. Códigos qLDPC y decodificadores neuronales

Los **códigos cuánticos de comprobación de paridad de bajo peso** (quantum Low-Density Parity-Check, qLDPC) representan la frontera más activa de la corrección de errores cuántica en 2025. Frente al surface code —el caballo de batalla actual—, los mejores códigos qLDPC prometen reducir el overhead en qubits físicos por un factor de 10× o más, manteniendo distancias de código comparables. Esta lección construye la teoría desde los códigos LDPC clásicos hasta los decodificadores neuronales de latencia submicróseconda.

---

## 1. Repaso: códigos LDPC clásicos

### 1.1 Definición y matriz de comprobación de paridad

Un **código LDPC** $[n, k, d]$ es un código lineal binario definido por una matriz dispersa de comprobación de paridad $H \in \mathbb{F}_2^{(n-k) \times n}$ con la propiedad de que cada fila y cada columna tiene un peso muy bajo (típicamente 3–6 unos), independientemente de $n$.

El espacio de codewords es el núcleo de $H$:

$$
\mathcal{C} = \{ \mathbf{c} \in \mathbb{F}_2^n \mid H\mathbf{c} = \mathbf{0} \}
$$

La **tasa del código** es $R = k/n$ y la **distancia mínima** $d$ es el peso mínimo de un codeword no nulo.

### 1.2 Grafo de Tanner

La herramienta geométrica esencial es el **grafo de Tanner** $G = (V \cup C, E)$, un grafo bipartito con:

- **Nodos variable** $V = \{v_1, \ldots, v_n\}$ (uno por bit del codeword).
- **Nodos de comprobación** $C = \{c_1, \ldots, c_{n-k}\}$ (uno por ecuación de paridad).
- Una arista $(v_j, c_i)$ existe si y solo si $H_{ij} = 1$.

La dispersión del código se traduce en que cada nodo tiene grado pequeño y constante: el grafo tiene $O(n)$ aristas en total, frente a $O(n^2)$ de un código denso.

> **Note:** La ausencia de ciclos cortos en el grafo de Tanner es crucial para la eficiencia de los decodificadores por propagación de creencias. Los mejores códigos LDPC modernos tienen *girth* (circunferencia mínima) $\geq 6$ ó $\geq 8$.

### 1.3 Decodificación por propagación de creencias (Belief Propagation)

El algoritmo **BP** (también llamado *sum-product*) opera sobre el grafo de Tanner intercambiando mensajes de probabilidad entre nodos variable y nodos de comprobación hasta convergencia.

En la iteración $t$, el mensaje del nodo de comprobación $c_i$ al nodo variable $v_j$ es:

$$
\mu_{c_i \to v_j}^{(t)} = 2\,\tanh^{-1}\!\left(\prod_{j' \in \partial(c_i) \setminus \{j\}} \tanh\!\left(\frac{\mu_{v_{j'} \to c_i}^{(t-1)}}{2}\right)\right)
$$

La complejidad es $O(n \cdot t_{\max})$ con $t_{\max}$ iteraciones, típicamente 50–100 en la práctica. Esta eficiencia contrasta con la decodificación óptima de máxima verosimilitud, que es NP-difícil en general.

### 1.4 Ventajas sobre códigos densos

| Propiedad | LDPC | Código denso (e.g., Reed-Solomon) |
|---|---|---|
| Complejidad decodificación | $O(n)$ | $O(n^2)$ – $O(n^3)$ |
| Umbral de Shannon | Alcanzable con BP | Alcanzable, pero costoso |
| Implementación hardware | Masivamente paralelo | Secuencial |
| Ciclos cortos | Evitables por diseño | No aplica |

Los códigos LDPC modernos (turbo-códigos, polar codes, LDPC de 5G) se acercan al límite de Shannon a $O(n \log n)$ con BP.

---

## 2. Códigos CSS cuánticos

### 2.1 Definición formal

Los **códigos CSS** (Calderbank-Shor-Steane) son el andamiaje sobre el que se construyen la mayoría de los códigos qLDPC. Un código CSS $[[n, k, d]]$ se especifica mediante dos matrices binarias $H_X \in \mathbb{F}_2^{r_X \times n}$ y $H_Z \in \mathbb{F}_2^{r_Z \times n}$ que satisfacen la condición de ortogonalidad:

$$
\boxed{H_X H_Z^T = 0 \pmod{2}}
$$

Esta condición garantiza que los estabilizadores $X$ y $Z$ conmuten entre sí, como exige la mecánica cuántica.

Los $n$ qubits físicos soportan:
- **Estabilizadores $X$:** cada fila $i$ de $H_X$ define $\bigotimes_j X_j^{(H_X)_{ij}}$.
- **Estabilizadores $Z$:** cada fila $i$ de $H_Z$ define $\bigotimes_j Z_j^{(H_Z)_{ij}}$.

El número de qubits lógicos codificados es:

$$
k = n - \text{rank}(H_X) - \text{rank}(H_Z)
$$

La **distancia del código** es:

$$
d = \min\!\left(d_X,\, d_Z\right), \quad d_X = \min_{\mathbf{e} \in \ker H_Z \setminus \text{im}\,H_X^T} |\mathbf{e}|, \quad d_Z = \min_{\mathbf{e} \in \ker H_X \setminus \text{im}\,H_Z^T} |\mathbf{e}|
$$

### 2.2 Ejemplo: Código de Steane [[7, 1, 3]]

El código de Steane está basado en el código de Hamming $[7, 4, 3]$ clásico, con $H_X = H_Z = H_{\text{Hamming}}$:

$$
H = \begin{pmatrix} 1&0&1&0&1&0&1 \\ 0&1&1&0&0&1&1 \\ 0&0&0&1&1&1&1 \end{pmatrix}
$$

Se puede verificar que $H H^T = 0 \pmod{2}$ gracias a la estructura del código de Hamming. El resultado es:
- $n = 7$ qubits físicos
- $k = 7 - 3 - 3 = 1$ qubit lógico
- $d = 3$ (puede corregir 1 error arbitrario de Pauli)

```python
import numpy as np

H = np.array([
    [1,0,1,0,1,0,1],
    [0,1,1,0,0,1,1],
    [0,0,0,1,1,1,1]
], dtype=int)

# Verificar condicion CSS: H * H^T = 0 mod 2
producto = (H @ H.T) % 2
print("H * H^T mod 2 =")
print(producto)
# -> matriz de ceros: condicion CSS satisfecha

k = 7 - np.linalg.matrix_rank(H) - np.linalg.matrix_rank(H)
print(f"Qubits logicos k = {k}")
```

---

## 3. Construcción Hypergraph Product (HP)

### 3.1 Tillich-Zémor 2014

La construcción de **producto de hipergrafo** (Tillich & Zémor, 2014) es el primer método sistemático para producir códigos qLDPC con distancia $d = \Theta(\sqrt{n})$ y tasa finita $k = \Theta(1)$. Dados dos códigos LDPC clásicos con matrices $H_1 \in \mathbb{F}_2^{r_1 \times n_1}$ y $H_2 \in \mathbb{F}_2^{r_2 \times n_2}$, el código HP cuántico tiene:

$$
H_X = \bigl(H_1 \otimes I_{n_2},\; I_{r_1} \otimes H_2^T\bigr)
$$

$$
H_Z = \bigl(I_{n_1} \otimes H_2,\; H_1^T \otimes I_{r_2}\bigr)
$$

> **Note:** El producto tensorial $\otimes$ aquí es el producto tensorial de matrices binarias (producto de Kronecker sobre $\mathbb{F}_2$). La condición $H_X H_Z^T = 0$ se verifica directamente usando $H_1 H_1^T = 0$ y $H_2 H_2^T = 0$ (que se satisfacen si $H_1, H_2$ son matrices de códigos duales).

### 3.2 Parámetros del código HP

El código resultante tiene:

- $n = n_1 n_2 + r_1 r_2$ qubits físicos
- $k = k_1 k_2$ qubits lógicos (donde $k_i = n_i - \text{rank}(H_i)$)
- $d = \min(d_1, d_2)$ distancia de código
- Peso de fila $w_{\text{row}} \leq w_1 + w_2$ (disperso si $H_1, H_2$ son LDPC)

### 3.3 Overhead $O(d^2)$ qubits

La relación fundamental de los códigos HP es:

$$
n \sim d^2 / R
$$

donde $R = k/n$ es la tasa del código. Para una distancia $d$ fija, el overhead en qubits físicos escala como $O(d^2)$. En comparación, el surface code requiere $n = d^2$ qubits para $k = 1$ qubit lógico (tasa $R \to 0$ para $d \to \infty$). Los códigos HP con tasa $R > 0$ son asintóticamente mucho más eficientes.

---

## 4. Bivariate Bicycle Codes (BB codes)

### 4.1 Bravyi et al., Nature 2024

El artículo de Bravyi, Cross, Gambetta, Nazario, Rall y Wood publicado en *Nature* en 2024 introdujo los **bivariate bicycle codes**, una familia de códigos qLDPC con parámetros excepcionalmente buenos para tamaños moderados (decenas a cientos de qubits), relevantes para el hardware actual.

### 4.2 Estructura de grupo abeliano

La construcción parte de un grupo abeliano $\mathbb{Z}_{l} \times \mathbb{Z}_{m}$ con elementos denotados como potencias del par de generadores $(x, y)$ con $x^l = y^m = 1$. Las matrices $H_X$ y $H_Z$ se definen como:

$$
H_X = [A \mid B], \quad H_Z = [B^T \mid A^T]
$$

donde $A$ y $B$ son matrices de circulante derivadas de polinomios $a(x, y)$ y $b(x, y)$ en el anillo $\mathbb{F}_2[x, y] / (x^l - 1, y^m - 1)$.

Por ejemplo, para el código **[[144, 12, 12]]**:

$$
l = 12,\; m = 6,\; a(x,y) = x^3 + y + y^2,\; b(x,y) = y^3 + x + x^2
$$

La condición CSS $H_X H_Z^T = 0$ se verifica algebraicamente gracias a la conmutatividad del anillo: $AB^T = BA^T$ cuando $A$ y $B$ son circulantes que conmutan.

### 4.3 Parámetros destacados

| Código BB | $n$ | $k$ | $d$ | Tasa $k/n$ |
|---|---|---|---|---|
| [[72, 12, 6]] | 72 | 12 | 6 | 1/6 |
| [[144, 12, 12]] | 144 | 12 | 12 | 1/12 |
| [[288, 12, 18]] | 288 | 12 | 18 | 1/24 |

### 4.4 Factor 10× frente al surface code

Para codificar 12 qubits lógicos con distancia 12 usando surface codes:

$$
n_{\text{surface}} = 12 \times d^2 = 12 \times 144 = 1728 \text{ qubits físicos}
$$

El código BB [[144, 12, 12]] logra lo mismo con solo 144 qubits físicos:

$$
\text{Factor de mejora} = \frac{1728}{144} = 12\times
$$

Este factor surge de la tasa $k/n = 1/12$ frente a la tasa $1/d^2 \to 0$ del surface code.

> **Note:** El factor exacto depende de la comparación precisa de los umbrales y la tasa de error lógica objetivo. Bravyi et al. (2024) reportan que para alcanzar $p_L = 10^{-10}$ con $p = 0.1\%$, los códigos BB requieren aproximadamente 10 veces menos qubits que los surface codes equivalentes.

```python
# Comparacion de overhead: surface code vs BB code
import numpy as np

d_target = 12  # distancia de codigo
k_logicos = 12  # qubits logicos requeridos

# Surface code: un [[d^2, 1, d]] por qubit logico
n_surface_por_qubit = d_target**2
n_surface_total = k_logicos * n_surface_por_qubit

# BB code [[144, 12, 12]]
n_bb = 144

factor = n_surface_total / n_bb
print(f"Surface code: {n_surface_total} qubits fisicos")
print(f"BB code [[144,12,12]]: {n_bb} qubits fisicos")
print(f"Factor de mejora: {factor:.1f}x")
# Output: Factor de mejora: 12.0x
```

---

## 5. Decodificadores

### 5.1 MWPM: Minimum Weight Perfect Matching

El decodificador **MWPM** modela el síndrome de errores como un conjunto de defectos (aniones) en el grafo del código y encuentra el emparejamiento de defectos de peso mínimo. Para el surface code, esto corresponde al algoritmo de Blossom de Kolmogorov (implementación: biblioteca `PyMatching`).

Complejidad: $O(n^3)$ en el peor caso con Blossom V, aunque implementaciones prácticas son $O(n^{1.5})$ amortizadas para errores raros.

**Limitación crítica para qLDPC:** MWPM asume que los errores son independientes y que el código tiene estructura de emparejamiento planar. Para códigos qLDPC de alta tasa, el grafo de síndrome no es planar y los errores correlacionados colapsan el rendimiento de MWPM.

### 5.2 BP+OSD

El decodificador **BP+OSD** (Belief Propagation + Ordered Statistics Decoding) es el estándar para códigos qLDPC:

1. **Fase BP:** ejecutar propagación de creencias en el grafo de Tanner durante $t_{\max}$ iteraciones. Si converge a un codeword válido, devolver el resultado.

2. **Fase OSD:** si BP no converge (debido a ciclos en el grafo), usar *ordered statistics decoding*: ordenar los bits por confianza de la salida BP, eliminar dependencias lineales entre las columnas más confiables para obtener una base sistemática, y resolver el sistema lineal sobre los bits restantes.

Complejidad: **$O(n \log n)$** para la fase BP más $O(n^3 / \log n)$ para OSD-$w$ de orden $w$ pequeño. En la práctica, OSD-2 u OSD-3 bastan para corregir casi todos los errores residuales de BP.

```python
# Pseudo-codigo: BP+OSD simplificado
import numpy as np

def bp_decode(H, syndrome, max_iter=50, channel_probs=None):
    """Belief Propagation sobre F2. Retorna estimado de error o None si no converge."""
    n = H.shape[1]
    if channel_probs is None:
        channel_probs = np.full(n, 0.01)
    
    # Inicializar mensajes con log-likelihood ratio
    llr = np.log((1 - channel_probs) / channel_probs)
    
    for t in range(max_iter):
        # Mensajes check -> variable (tanh sum-product)
        # [implementacion completa omitida por brevedad]
        pass
    
    return None  # no convergencia: pasar a OSD

def osd_decode(H, syndrome, bp_llr, order=2):
    """Ordered Statistics Decoding de orden 'order'."""
    # Ordenar columnas por |LLR| descendente
    sorted_cols = np.argsort(-np.abs(bp_llr))
    # Pivoteo Gaussiano sobre F2 para encontrar columnas pivot
    # Resolver sistema lineal sobre las columnas restantes
    # [implementacion completa: ver ldpc library de Roffe et al.]
    pass
```

> **Note:** La biblioteca `ldpc` de Joschka Roffe (Python/C++) incluye implementaciones optimizadas de BP+OSD para códigos qLDPC. Para códigos BB de tamaño moderado, BP+OSD alcanza un rendimiento cercano al óptimo.

### 5.3 Decodificadores neuronales

Los decodificadores basados en redes neuronales ofrecen la promesa de latencia $< 1\,\mu\text{s}$ mediante inferencia en hardware dedicado (FPGA o ASIC).

**LSTM (Long Short-Term Memory):**

El síndrome a lo largo del tiempo (múltiples rondas de medición) se modela como una secuencia temporal. Una red LSTM aprende a mapear $\{s_t\}_{t=1}^T \to \hat{\mathbf{e}}$:

$$
h_t = \text{LSTM}(s_t, h_{t-1}), \quad \hat{\mathbf{e}} = \sigma(W h_T + b)
$$

donde $s_t \in \{0,1\}^{r_X + r_Z}$ es el síndrome en la ronda $t$ y $\hat{\mathbf{e}} \in [0,1]^n$ es la probabilidad de error en cada qubit.

**Transformer:**

Los transformers codifican la correlación espacial del síndrome mediante atención:

$$
\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^T}{\sqrt{d_k}}\right) V
$$

Ventaja: capturan correlaciones de largo alcance que BP pierde en grafos con ciclos cortos.

**Requisito de latencia:**

Para QEC a 1 GHz (ciclo de síndrome $\sim 1\,\mu\text{s}$), el decodificador debe completarse en:

$$
t_{\text{decode}} < 1\,\mu\text{s}
$$

Con hardware GPU/FPGA de alto rendimiento, redes pequeñas ($\sim 10^5$ parámetros) pueden inferir en $\sim 200\,\text{ns}$ para códigos de tamaño moderado ($n \leq 200$). Para códigos más grandes, la latencia es el cuello de botella principal.

---

## 6. Estado del arte en 2025

### 6.1 Umbrales bajo ruido de circuito

Bajo el modelo de **ruido de Pauli independiente**, los códigos BB alcanzan umbrales $p_{\text{th}} \approx 1\%$, comparable al surface code. Sin embargo, el modelo más realista es el **ruido de circuito** (que incluye errores en puertas CNOT, preparación de ancillas y medición), que reduce los umbrales:

| Código | Umbral (Pauli) | Umbral (circuito) |
|---|---|---|
| Surface code $d=7$ | $\sim 1\%$ | $\sim 0.7\%$ |
| BB [[144,12,12]] | $\sim 1\%$ | $\sim 0.5\%$ – $0.7\%$ |
| BB [[72,12,6]] | $\sim 0.8\%$ | $\sim 0.4\%$ – $0.5\%$ |

### 6.2 Hoja de ruta IBM: Condor → Flamingo → Starling

- **Condor (2023):** 1127 qubits físicos, primera demostración de surface code de distancia $d=3$ en hardware real.
- **Flamingo (2024–2025):** arquitectura de interconexión modular, primer uso de códigos qLDPC en hardware IBM.
- **Starling (2026+):** objetivo de 100 qubits lógicos con corrección de errores activa usando códigos BB o similares. Requiere tasas de error de 2-qubit gate $< 0.1\%$ y ciclos de síndrome $< 1\,\mu\text{s}$.

> **Note:** IBM ha publicado que para 100 qubits lógicos con distancia 12, los códigos BB necesitan $\sim 1500$ qubits físicos frente a los $\sim 15000$ que requeriría el surface code. Este ahorro de 10× es el motor principal de la transición a qLDPC.

### 6.3 Ventaja sobre surface codes en el límite $k \to \infty$

El resultado teórico fundamental es el **good quantum LDPC codes** (Panteleev & Kalachev 2022; Leverrier & Zémor 2022), que demuestra la existencia de familias de códigos qLDPC con:

$$
k = \Theta(n), \quad d = \Theta(n)
$$

Esto implica que asintóticamente, el overhead en qubits es $O(1)$ por qubit lógico, frente al $O(d^2)$ del surface code. En el límite de muchos qubits lógicos, los códigos qLDPC son incomparablemente mejores.

---

## 7. Tabla comparativa

| Parámetro | Surface code $d=7$ (×1 lógico) | BB [[144,12,12]] (×12 lógicos) |
|---|---|---|
| Qubits físicos | 98 ($\approx d^2 \times 1.5$) | 144 |
| Qubits lógicos | 1 | 12 |
| Distancia $d$ | 7 | 12 |
| Overhead $n/k$ | 98 | 12 |
| Tasa $k/n$ | $\approx 0.010$ | $\approx 0.083$ |
| Umbral (Pauli) | $\sim 1\%$ | $\sim 1\%$ |
| Umbral (circuito) | $\sim 0.7\%$ | $\sim 0.6\%$ |
| Conectividad requerida | Local 2D | No local (6 vecinos) |
| Mejor decodificador | MWPM | BP+OSD |
| Complejidad decoder | $O(n^{1.5})$ | $O(n \log n)$ |

> **Note:** La conectividad no local de los códigos BB es un reto de ingeniería. IBM resuelve esto mediante interconexiones de microondas en 3D y arquitecturas *heavy-hex* extendidas. Los trabajos de 2024–2025 demuestran que el overhead de conectividad no cancela la ganancia en overhead de qubits.

---

## 8. Ejercicios

**Ejercicio 1 (básico).** Para el código CSS con:

$$
H_X = H_Z = \begin{pmatrix} 1&1&0&1&1&0&0 \\ 0&1&1&0&1&1&0 \\ 0&0&1&1&0&1&1 \\ 1&0&0&1&0&0&1 \end{pmatrix}
$$

(a) Verificar que $H_X H_Z^T = 0 \pmod{2}$.
(b) Calcular el número de qubits lógicos $k$.
(c) Identificar el código resultante.

**Ejercicio 2 (intermedio).** Implementar en Python la construcción del producto de hipergrafo a partir de dos matrices LDPC $H_1$ y $H_2$ de tamaño $3 \times 6$. Verificar que el código resultante satisface la condición CSS.

**Ejercicio 3 (intermedio).** Para el código BB con $l = 6$, $m = 3$, $a(x,y) = x + y$, $b(x,y) = x^2 + y^2$:

(a) Construir las matrices $A$ y $B$ como circulantes de tamaño $18 \times 18$.
(b) Calcular los parámetros $[[n, k, d]]$ del código resultante.

**Ejercicio 4 (avanzado).** Implementar un decodificador BP básico (sin OSD) para el código de Steane [[7,1,3]]. Simular $10^4$ errores de Pauli con $p = 0.05$ y estimar la tasa de error lógica. Comparar con la cota teórica $p_L \leq \binom{3}{2} p^2$.

**Ejercicio 5 (investigación).** Reproducir la curva de umbral de los códigos BB [[72,12,6]] bajo ruido de Pauli independiente: simular Monte Carlo de $P_L(p)$ para tamaños $l \in \{6, 12, 24\}$ manteniendo la forma de $a(x,y), b(x,y)$, y estimar el crossing point. Comparar con el valor reportado en Bravyi et al. 2024.

---

## 9. Referencias

1. **Tillich, J.-P. & Zémor, G.** (2014). "Quantum LDPC codes with positive rate and minimum distance proportional to the square root of the blocklength." *IEEE Transactions on Information Theory*, 60(2), 1193–1202.

2. **Bravyi, S., Cross, A. W., Gambetta, J. M., Nazario, D., Rall, P., & Wood, C. J.** (2024). "High-threshold and low-overhead fault-tolerant quantum memory." *Nature*, 627, 778–782.

3. **Leverrier, A. & Zémor, G.** (2022). "Quantum Tanner codes." *Proceedings of the 63rd IEEE FOCS*, 872–883.

4. **Panteleev, P. & Kalachev, G.** (2022). "Asymptotically good quantum and locally testable classical LDPC codes." *Proceedings of the 54th STOC*, 375–388.

5. **Roffe, J.** (2022). "LDPC: Python tools for low density parity check codes." *arXiv:2205.09581*.

6. **Kuperberg, G. et al.** (2023). "Bivariate bicycle codes and MWPM." *arXiv:2308.07915*.

---

## Navegación

- Anterior: [Surface codes y horizonte fault-tolerant](../14_surface_codes_y_horizonte_fault_tolerant/README.md)
- Siguiente: Investigación R9 — [Umbral qLDPC bajo ruido de circuito](../../Soluciones/investigacion/R9_qldpc_threshold.md)
