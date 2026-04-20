# Álgebra Lineal Mínima para Computación Cuántica

## 1. El Espacio de Hilbert
La computación cuántica no ocurre en cables eléctricos, sino en un espacio vectorial complejo con producto interno llamado **Espacio de Hilbert**. Para un sistema de $n$ qubits, este espacio tiene una dimensión monumental de $2^n$.

## 2. Vectores de Estado (Kets) y Dualismo (Bras)
Usamos la notación de Dirac (Bra-Ket) para representar los estados:
- **Ket $| \psi \rangle$:** Un vector columna que representa el estado del sistema.
- **Bra $\langle \psi |$:** El vector fila conjugado traspuesto.
- **Producto Interno $\langle \phi | \psi \rangle$:** Nos da la amplitud de probabilidad (un número complejo).
- **Producto Externo $| \psi \rangle \langle \phi |$:** Da como resultado una matriz (un operador).

## 3. Operadores Unitarios y Hermíticos
Las puertas cuánticas se representan mediante **Matrices Unitarias** ($U^\dagger U = I$). Esto garantiza que la evolución sea reversible y que la probabilidad total ($||\psi||^2$) siempre sea 1.
Los observables (las cosas que podemos medir, como la energía) se representan mediante **Matrices Hermíticas** ($H^\dagger = H$), lo que asegura que sus valores propios (los resultados de la medición) sean números reales.

## 4. Producto Tensorial ($\otimes$)
Es la herramienta matemática para combinar qubits. Si un qubit está en $|a\rangle$ y otro en $|b\rangle$, el sistema total está en $|a\rangle \otimes |b\rangle$. Es aquí donde nace el crecimiento exponencial del espacio de estados y la posibilidad del **Entrelazamiento** (estados globales que no pueden expresarse como productos tensoriales de estados individuales).

## Navegacion

- Anterior: [Qiskit: primeros pasos y flujo de trabajo practico](../02_qiskit_basico/05_qiskit_primeros_pasos.md)
- Siguiente: [Algoritmos cuanticos introductorios](07_algoritmos_cuanticos_introductorios.md)
