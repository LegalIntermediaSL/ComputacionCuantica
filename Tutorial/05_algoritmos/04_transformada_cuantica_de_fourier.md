# Transformada Cuántica de Fourier (QFT)

## 1. Del Dominio del Tiempo a la Frecuencia
La Transformada Cuántica de Fourier es el análogo cuántico de la Transformada de Fourier Discreta (DFT). Es el motor interno de los algoritmos más potentes, incluyendo Shor y Phase Estimation. Su función es mapear un estado base $|x\rangle$ a una superposición de fases:

$$ QFT_N |x\rangle = \frac{1}{\sqrt{N}} \sum_{y=0}^{N-1} e^{2\pi i xy / N} |y\rangle $$

## 2. Construcción del Circuito
A diferencia de la FFT clásica que escala como $O(N \log N)$, la QFT cuántica se implementa con solo $O(n^2)$ puertas (siendo $n$ el número de qubits, $N=2^n$). El circuito se construye utilizando:
- **Puertas Hadamard ($H$):** Para crear superposiciones.
- **Puertas de Fase Controladas ($R_k$):** Donde $R_k = \begin{pmatrix} 1 & 0 \\ 0 & e^{2\pi i / 2^k} \end{pmatrix}$. Estas puertas aplican rotaciones proporcionales a la posición relativa de los qubits.

## 3. Aplicaciones e Intuición
La QFT no se usa para "analizar señales de audio clásicas" (ya que extraer los coeficientes requeriría medir y destruir el estado, lo cual es ineficiente). Su poder radica en que permite **manipular la información de periodicidad** dentro de un algoritmo cuántico. 

Cuando los datos están codificados en las amplitudes, la QFT los traslada a las fases (y viceversa). Esta propiedad de "revelar patrones periódicos" es la que permite romper el cifrado RSA en el algoritmo de Shor.

## Navegacion

- Anterior: [Grover](03_grover.md)
- Siguiente: [Phase Estimation](05_phase_estimation.md)
