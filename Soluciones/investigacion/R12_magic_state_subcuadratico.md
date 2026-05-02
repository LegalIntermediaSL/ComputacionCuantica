# R12 — Destilación de Magic States con Overhead Sub-Cuadrático

> **Problema abierto #9:** ¿Es posible destilar magic states con overhead de qubits físicos $o(n^2)$ para producir $n$ estados $|T\rangle$ limpios?

---

## Por qué se necesitan Magic States

En computación tolerante a fallos, el grupo de Clifford (H, S, CNOT) es implementable eficientemente con bajo overhead físico. Sin embargo, el **teorema de Eastin-Knill** prohibe implementar puertas no-Clifford (como T) de forma transversal en códigos estabilizadores.

La solución estándar es la **destilación de magic states**: usar muchos estados $|T\rangle$ ruidosos para producir pocos estados $|T\rangle$ limpios, usando solo operaciones Clifford (que ya son tolerantes a fallos).

$$|T\rangle = \frac{1}{\sqrt{2}}(|0\rangle + e^{i\pi/4}|1\rangle) = T|+\rangle$$

---

## Protocolo Reed-Muller [[15,1,3]]

El protocolo más conocido (Bravyi-Kitaev 2005) usa el código $[[15,1,3]]$:

**Proceso:**
1. Preparar 15 estados $|T\rangle$ ruidosos con tasa de error $\varepsilon$
2. Medir los estabilizadores del código [[15,1,3]] (solo operaciones Clifford)
3. Si no hay síndromes: la salida es un estado $|T\rangle$ con error $O(\varepsilon^3)$
4. Descartar si hay síndromes

**Overhead:** $15 \to 1$, reducción de error $\varepsilon \to \varepsilon' \approx 35\varepsilon^3$.

Para obtener un estado con error $\varepsilon_\text{target}$ partiendo de $\varepsilon_0$, se necesitan $k$ rondas de destilación:

$$k = \left\lceil \frac{\log(\varepsilon_\text{target}/\varepsilon_0)}{\log(35\varepsilon_0^2)} \right\rceil$$

**Costo total:** $15^k$ estados iniciales → overhead **exponencial** en el número de rondas.

---

## Protocolo Bravyi-Haah 2012 — Reducción a 10→1

Bravyi y Haah demostraron que el código $[[10,2,2]]$ permite un protocolo más eficiente:
- **Tasa:** 10 estados ruidosos → 2 estados limpios (vs 15→1 de Reed-Muller)
- **Reducción de error:** $\varepsilon \to O(\varepsilon^2)$ (cuadrático vs cúbico)
- **Overhead por estado:** 5× vs 15× de [[15,1,3]]

**Comparativa:**

| Protocolo | Entradas/salidas | Reducción error | Umbral |
|-----------|-----------------|-----------------|--------|
| [[15,1,3]] | 15 → 1 | $\varepsilon^3$ | ~1.4% |
| Bravyi-Haah | 10 → 2 | $\varepsilon^2$ | ~14.5% |
| Haah et al. 2018 | 6 → 1 | $\varepsilon^2$ | ~32% |
| Litinski 2019 | variable | variable | hardware-dep. |

---

## Cotas de Overhead Sub-Cuadrático

### El overhead cuadrático de la destilación concatenada

Para el protocolo [[15,1,3]] con $k$ niveles, el overhead de qubits es:

$$n_\text{físicos}(n_\text{lógicos}) = O(n_\text{lógicos} \cdot 15^k \cdot d^2)$$

donde $d^2$ son los qubits del código surface. Para $k=2$ (suficiente para $\varepsilon_\text{target}\sim 10^{-10}$) y $d=7$: **$\sim 1500$ qubits físicos por estado T**. Esto es **cuadrático** en $d$.

### ¿Puede ser sub-cuadrático?

**Resultado de Bravyi-Haah (2012):** Existe una familia de protocolos de destilación con overhead $O(d \log d)$ en qubits físicos (sub-cuadrático) usando códigos topológicos 3D.

**Construcción:** Usar el código de color 3D $[[O(d^3), 1, d]]$ como código destilador. La clave es que los operadores de corrección del código tienen peso $O(d)$ en 3D vs $O(d^2)$ en 2D.

$$n_\text{físicos} = O(d^3) \cdot k \text{ vs } O(d^2 \cdot 15^k) \text{ (cuadrático)}$$

Para $d$ grande y muchas rondas $k$, el protocolo 3D domina.

### Protocolo de Litinski 2019 — "Garden Hose"

El protocolo de Litinski construye una **fábrica de magic states** integrada en el surface code que realiza la destilación sin overhead de espacio-tiempo adicional. El overhead es:

$$V \sim O(d^3) \text{ unidades de espacio-tiempo}$$

que puede implementarse en el "bulk" del computador tolerante a fallos sin requerir qubits físicos adicionales separados.

---

## Estado Actual y Perspectivas

| Año | Resultado | Overhead |
|-----|-----------|---------|
| 2005 | Bravyi-Kitaev [[15,1,3]] | $O(d^2 \cdot 15^k)$ |
| 2012 | Bravyi-Haah | $O(d^2 \cdot 5^k)$ (sub-15) |
| 2018 | Haah et al. quasi-poly | $O(d^{2+\epsilon})$ |
| 2019 | Litinski factory | $O(d^3)$ espacio-tiempo |
| 2024 | qLDPC + magic state | $O(\text{polylog}(d))$ teórico |

La combinación de **códigos qLDPC** (bivariate bicycle) con protocolos de destilación optimizados puede reducir el overhead hasta factores de 10-100× comparado con surface codes (Bravyi et al. 2024). Esto es el resultado más importante del año en fault-tolerance.

---

## Conclusión

El overhead estrictamente sub-cuadrático está **demostrado teóricamente** con protocolos de destilación 3D. En la práctica, el protocolo de Litinski $O(d^3)$ ya es sub-cuadrático en espacio. La combinación con qLDPC puede reducir el overhead de 1000× (surface code) a ~20× en hardware de próxima generación (IBM Flamingo, 2027-2028).
