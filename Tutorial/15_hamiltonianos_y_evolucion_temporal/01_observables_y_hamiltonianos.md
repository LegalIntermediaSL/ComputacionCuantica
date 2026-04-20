# Observables y Hamiltonianos Formales

## 1. El Hamiltoniano Matemático

Hasta ahora en tu formación de iniciación has tratado los circuitos rotando mediante compuertas pre-compiladas aisladas $H, X, Y$. Pero todo cambio o rotura de estado en el universo de superposición física ocurre dirigido e indexado inquebrantablemente a través de la presencia del **Hamiltoniano ($H$)**; un tensor hermitiano supremo o "Generador" que representa la matriz de toda la energía acumulada del universo analizado de las partículas.

Como el Hamiltoniano es una matriz completamente observable Hermitiana (es decir, $H = H^\dagger$), sus valores autovectores y autovalores son empíricos y físicos estables y puros Reales ($\mathbb{R}$). 

## 2. Abstracción Qiskit: Qiskit PauliOps
Dentro de Qiskit, la orquestación unitaria física real termodinámica se mapea mediante matrices formales en `SparsePauliOp`. Toda fórmula magnética $H$ molecular puede describirse y separarse abstractamente como sumas ponderales de las "Cartas Fundamentales Direccionales" que configuran el universo: las matrices Pauli $\sigma_X, \sigma_Y, \sigma_Z, I$.

$ H = \sum_{i} c_i P_i \quad \text{donde } P_i \in \{ I, X, Y, Z \}^{\otimes n} $

Es de vital importancia entender esto para la capa subyacente. Los estimadores variacionales $VQE$ calculados nunca interaccionan con matrices aleatorias inescrutables, sino que envían pulsaciones repetidas observando rigurosamente cada $P_i$ direccional separadamente en la física de base subyacente.

## Navegacion

- Anterior: [Simulacion digital y Hamiltonianos sencillos](../12_aplicaciones/04_simulacion_digital_y_hamiltonianos_sencillos.md)
- Siguiente: [Evolucion unitaria y Trotterizacion](02_evolucion_unitaria_y_trotterizacion.md)
