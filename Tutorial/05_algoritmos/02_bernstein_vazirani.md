# Algoritmo de Bernstein-Vazirani

## 1. Descifrando la Cadena Oculta
El algoritmo de Bernstein-Vazirani es una evolución directa de Deutsch-Jozsa. En este caso, el oráculo implementa una función de producto escalar oculta:
$$ f(x) = s \cdot x \pmod 2 $$
donde $s \in \{0,1\}^n$ es una cadena de bits secreta que queremos descubrir.

Clásicamente, para encontrar $s$, necesitaríamos $n$ consultas al oráculo (consultando $f(100\dots0), f(010\dots0)$, etc.). Cuánticamente, de nuevo, solo requerimos **una consulta**.

## 2. Ejecución y Phase Kickback
La estructura es idéntica a Deutsch-Jozsa:
1. Preparamos el estado inicial $|0\rangle^{\otimes n} |1\rangle$.
2. Aplicamos Hadamards para crear $|+\rangle^{\otimes n} |-\rangle$.
3. Consultamos el oráculo $U_f$. El phase kickback codifica el bit $s_i$ en la fase del qubit $i$.
4. Aplicamos Hadamards finales.

La operación de la Hadamard sobre la fase $(-1)^{s \cdot x}$ realiza una transformada que colapsa el estado exactamente sobre la cadena secreta:
$$ H^{\otimes n} \left( \frac{1}{\sqrt{2^n}} \sum_{x} (-1)^{s \cdot x} |x\rangle \right) = |s\rangle $$

## 3. Relevancia Práctica
Bernstein-Vazirani demuestra que la computación cuántica no solo es buena para saber "si algo es constante", sino para extraer **metadata estructurada** (como la cadena $s$) con una eficiencia inalcanzable para el procesamiento bit a bit tradicional. Es el precursor espiritual de algoritmos de búsqueda más complejos.

## Navegacion

- Anterior: [Deutsch-Jozsa](01_deutsch_jozsa.md)
- Siguiente: [Grover](03_grover.md)
