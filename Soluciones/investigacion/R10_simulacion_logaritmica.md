# R10 — Simulación Clásica en O(log n) para Circuitos Estructurados

> **Problema abierto #4:** ¿Existen familias de circuitos cuánticos de utilidad práctica que admitan simulación clásica en tiempo $O(\log n)$?

---

## Contexto

La supremacía cuántica implica que ciertos circuitos cuánticos *genéricos* no pueden simularse clásicamente en tiempo polinomial. Sin embargo, existen **familias estructuradas** de circuitos para las cuales la simulación es eficiente:

| Clase | Simulación clásica | Complejidad |
|-------|-------------------|-------------|
| Circuitos Clifford | Tableau de Gottesman | $O(n^2)$ |
| MPS (bond dim. $\chi$) | Contracción tensorial | $O(n\chi^3)$ |
| Circuitos libres de fermiones | Pfaffiano | $O(n^3)$ |
| Circuitos log-profundidad + local | Renormalización | $O(n \log n)$? |

---

## Simulación por MPS/DMRG en Circuitos de Baja Profundidad

Para circuitos de **profundidad logarítmica** $d = O(\log n)$ con puertas locales, la entropía de entrelazamiento satisface la **ley de área**:

$$S(A) \leq c \cdot d \leq c' \log n$$

Esto implica que el estado puede aproximarse eficientemente por un MPS de dimensión de enlace:

$$\chi \sim e^{S} \leq n^{c'}$$

La contracción de un MPS de longitud $n$ y dimensión $\chi$ requiere $O(n\chi^3) = O(n^{1+3c'})$ operaciones, que es **polinomial** pero no logarítmico.

**¿Puede ser $O(\log n)$?** Para $d = O(1)$ (profundidad constante), la entropía es $O(1)$, $\chi = O(1)$, y la simulación es $O(n)$. Para $d = O(\log n)$, con algoritmos de renormalización por bloques:

$$T_\text{sim} = O(n \cdot \chi^3) = O(n \cdot e^{O(\log n)}) = O(n^{1+O(1)})$$

No es $O(\log n)$, pero puede ser sub-cuadrático.

---

## Algoritmo FKS para Hamiltonianos Dispersos

Para Hamiltonianos con **interacciones de corto alcance** $H = \sum_{\langle i,j\rangle} h_{ij}$, el algoritmo de Feynman-Kitaev-Svore (FKS) aprovecha la **localidad**:

$$e^{-iHt} \approx \prod_{\langle i,j\rangle} e^{-ih_{ij}t/n}$$

La clave para eficiencia logarítmica es la **commutatividad por bloques**: si se puede particionar $H = H_\text{even} + H_\text{odd}$ donde todos los términos en $H_\text{even}$ conmutan entre sí (y análogo para $H_\text{odd}$), entonces:

$$e^{-iH_\text{even}t} = \bigotimes_{\langle i,j\rangle \in \text{even}} e^{-ih_{ij}t}$$

es un producto tensorial, simulable en $O(\log n)$ con paralelización.

### Circuitos del tipo Clifford + T con T-count bajo

Para circuitos con $t$ puertas T y el resto Clifford, la simulación exacta requiere $O(2^t \cdot n^2)$ (método de Bravyi-Gosset-König). Para $t = O(\log n)$: $T_\text{sim} = O(n^{1+c})$.

---

## Simulación con Estabilizadores Extendidos

Los **estabilizadores extendidos** (Bravyi-Gosset 2016) representan el estado como mezcla de $2^t$ estados estabilizadores:

$$|\psi\rangle = \frac{1}{\sqrt{2^t}}\sum_{s\in\{0,1\}^t} \omega^{f(s)} |C_s\rangle$$

donde $|C_s\rangle$ son estados estabilizadores y $\omega = e^{i\pi/4}$. Este método es exacto y requiere $O(2^t n^2)$ tiempo y memoria.

**Para $O(\log n)$:** Se necesita $t = O(1)$ puertas T, lo que es extremadamente restrictivo. Solo los circuitos casi-Clifford con $t \leq 3\log_2 n$ son simulables en tiempo polinomial.

---

## Conclusión

La simulación en $O(\log n)$ estricto solo está garantizada para:

1. **Circuitos de profundidad $O(1)$** con puertas locales (trivialmente)
2. **Circuitos Clifford log-profundos** sin puertas T (clases en BPP)
3. **MPS con $\chi = O(1)$** (entropía acotada)

Para uso práctico (algoritmos NISQ, VQE, QAOA), ninguna de estas clases cubre los casos de interés: los circuitos de profundidad $O(\log n)$ con entrelazamiento no trivial permanecen en la frontera de la simulabilidad clásica. La pregunta sobre $O(\log n)$ para familias útiles sigue **abierta**.
