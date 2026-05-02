# Resumen 14 — Códigos qLDPC y Decodificadores

## 1. Condición CSS y Construcción

Los **códigos CSS** (Calderbank-Shor-Steane) se construyen a partir de dos códigos clásicos $C_X$ y $C_Z$:

$$H_X H_Z^T = 0$$

Esta condición garantiza que los estabilizadores $X$ y $Z$ conmutan. Los parámetros del código son:

$$[[n, k, d]], \quad k = \dim(\ker H_X) - \dim(\text{im } H_Z^T)$$

---

## 2. Producto Hipergrafo (Tillich-Zémor 2014)

Dados dos códigos clásicos $[n_1, k_1, d_1]$ y $[n_2, k_2, d_2]$, el **hypergraph product** produce:

$$[[n_1 n_2 + n_1' n_2', \, k_1 k_2 + k_1' k_2', \, \min(d_1, d_2)]]$$

donde prima denota el código dual. Las matrices son:

$$H_X = (H_1 \otimes I_{n_2} \mid I_{n_1'} \otimes H_2^T)$$
$$H_Z = (I_{n_1} \otimes H_2 \mid H_1^T \otimes I_{n_2'})$$

Ventaja clave: peso constante (LDPC) y distancia $d \sim \sqrt{n}$.

---

## 3. Bicicleta Bivariante [[144,12,12]]

El código **bivariate bicycle** (BB) de IBM (2023) usa:

$$H_X = [A \mid B], \quad H_Z = [B^T \mid A^T]$$

donde $A, B$ son circulantes en $\mathbb{Z}_{l} \times \mathbb{Z}_m$.

| Parámetro | Valor |
|---|---|
| Código | $[[144, 12, 12]]$ |
| Overhead vs surface code | $10\times$ menor qubits para misma capacidad |
| Peso de checks | 6 (LDPC) |
| Arquitectura | Compatible con conectividad limitada |
| Estado arte 2025 | Threshold $\sim 0.5\%$ (simulación) |

---

## 4. Algoritmo MWPM

El **Minimum Weight Perfect Matching (MWPM)** es el decodificador estándar del surface code:

1. Construir grafo de síndrome con nodos = errores detectados
2. Asignar pesos $w_{ij} = -\log P(\text{camino más probable})$
3. Encontrar emparejamiento de peso mínimo (algoritmo de Blossom)
4. Aplicar correcciones correspondientes

**Complejidad**: $O(n^3)$ en el peor caso; $O(n^{1.5})$ en la práctica con Blossom V.

**Tiempo**: $\sim 10\text{--}100$ μs en software Python/C++, $\sim 300$ ns en FPGA.

---

## 5. Comparación de Decodificadores

| Decodificador | Threshold | Latencia | Complejidad | Hardware |
|---|---|---|---|---|
| MWPM | $\sim 1\%$ | $\sim 10$ μs (SW) | $O(n^{1.5})$ | CPU |
| MWPM FPGA | $\sim 1\%$ | $\sim 300$ ns | $O(n^{1.5})$ | FPGA |
| BP+OSD | $\sim 0.5\%$ qLDPC | $\sim 1$ ms | $O(n^2)$ | CPU/GPU |
| Neural (CNN) | $\sim 0.9\%$ | $\sim 100$ ns | $O(1)$ inferencia | GPU/ASIC |
| Union-Find | $\sim 0.9\%$ | $\sim 1$ μs | $O(n \alpha(n))$ | FPGA |

**BP+OSD** (Belief Propagation + Ordered Statistics Decoding): el mejor para qLDPC en threshold, pero lento. La combinación BP (iterativo, rápido) + OSD (corrección algebraica post-procesado) supera a MWPM puro para códigos no topológicos.

---

## 6. Decodificadores Neuronales

Los **decodificadores neuronales** entrenan una red (típicamente CNN o transformer) para mapear síndromes → correcciones:

$$\hat{e} = f_\theta(s), \quad \mathcal{L} = -\log P(\text{corrección exitosa})$$

- **Ventaja**: inferencia $O(1)$ en tiempo (si el modelo está compilado en ASIC)
- **Desventaja**: entrenamiento costoso, generalización limitada a nuevas tasas de error
- **2025**: modelos transformer con ventana de síndrome alcanzan threshold comparable a MWPM

---

## Fórmulas Clave

$$H_X H_Z^T = 0 \quad \text{(CSS condition)}$$

$$k = k_1 k_2 \text{ (hypergraph product)}, \quad d \geq \min(d_1, d_2)$$

$$\text{Overhead surface code: } n_{\text{phys}} \sim (d/p_{th})^2 \cdot k$$
