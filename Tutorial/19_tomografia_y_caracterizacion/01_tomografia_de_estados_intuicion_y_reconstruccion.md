# Tomografía de estados cuánticos

## 1. El problema de la reconstrucción

Supongamos que preparamos repetidamente un estado cuántico desconocido $\rho$ en el laboratorio y queremos determinar qué estado es exactamente. El problema es que una sola medición solo da un resultado clásico (un bit), destruyendo el estado en el proceso. Necesitamos muchas copias del estado y mediciones en distintas bases.

La **tomografía de estados cuánticos (QST)** es el procedimiento para reconstruir la matriz de densidad $\rho$ a partir de mediciones estadísticas.

El problema que motiva la QST: mediciones en la base $Z$ sobre el estado $\frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$ y sobre la mezcla clásica $\frac{1}{2}(|00\rangle\langle 00| + |11\rangle\langle 11|)$ producen estadísticas **idénticas** (solo $00$ y $11$, con igual frecuencia). Para distinguirlos hay que medir en otras bases.

## 2. Tomografía de un qubit

Para un qubit, la matriz de densidad más general es:

$$
\rho = \frac{1}{2}(I + r_x X + r_y Y + r_z Z)
$$

Para determinar los tres parámetros reales $(r_x, r_y, r_z)$ se mide el valor esperado de los tres operadores de Pauli:

$$
r_x = \langle X \rangle = \text{Tr}(X\rho), \quad r_y = \langle Y \rangle = \text{Tr}(Y\rho), \quad r_z = \langle Z \rangle = \text{Tr}(Z\rho)
$$

Esto requiere tres conjuntos de mediciones:
1. Medir en la base $Z$ directamente.
2. Aplicar $H$ y medir (equivale a medir $X$).
3. Aplicar $S^\dagger H$ y medir (equivale a medir $Y$).

Con $N$ copias del estado divididas entre las tres bases, la precisión de la estimación escala como $O(1/\sqrt{N})$.

## 3. Tomografía de n qubits: el problema de escalado

Para $n$ qubits, $\rho$ es una matriz hermitiana de $2^n \times 2^n$ con $4^n - 1$ parámetros reales independientes. Determinarlos todos requiere medir $4^n - 1$ observables independientes (todos los productos de Pauli no triviales).

| Número de qubits | Parámetros independientes | Copias necesarias |
|---|---|---|
| 1 | 3 | ~$10^3$ |
| 2 | 15 | ~$10^4$ |
| 5 | 1023 | ~$10^6$ |
| 10 | $\sim 10^6$ | ~$10^9$ |
| 20 | $\sim 10^{12}$ | inalcanzable |

La QST completa escala exponencialmente y es impracticable para más de 8-10 qubits. Esto motiva alternativas escalables.

## 4. Estimación por máxima verosimilitud (MLE)

En la práctica, las frecuencias medidas contienen ruido estadístico y la matrix de densidad reconstruida directamente puede no ser semidefinida positiva. La **estimación por máxima verosimilitud (MLE)** resuelve este problema:

Se busca la $\hat{\rho}$ que maximiza la verosimilitud de haber observado los datos medidos, sujeto a que $\hat{\rho}$ sea una matriz de densidad válida ($\hat{\rho} \geq 0$, $\text{Tr}(\hat{\rho}) = 1$):

$$
\hat{\rho} = \arg\max_{\rho \geq 0, \, \text{Tr}(\rho)=1} \sum_{k,m} n_{k,m} \log \text{Tr}(M_{k,m} \rho)
$$

donde $n_{k,m}$ es el número de ocurrencias del resultado $m$ en la base de medición $k$.

## 5. Alternativas escalables: tomografía compressed sensing

Para estados con estructura especial (baja entropía, bajo rango), existen técnicas que requieren exponencialmente menos mediciones:

**Compressed sensing QST:** si $\rho$ tiene rango $r \ll 2^n$, se puede reconstruir con $O(r \cdot 2^n \log 2^n)$ mediciones (en lugar de $O(4^n)$) usando técnicas de compresión de señales.

**Matrix product state (MPS) tomography:** para estados con estructura de cadena unidimensional y entrelazamiento limitado, la tomografía escala polinomialmente.

**Shadow tomography:** usando mediciones aleatorias, estima valores esperados de $M$ observables con solo $O(\log M)$ copias del estado.

## 6. Implementación en Qiskit

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp, DensityMatrix
import numpy as np

def qubit_tomography(qc: QuantumCircuit) -> dict:
    """
    Tomografía completa de un qubit: calcula (rx, ry, rz).
    """
    estimator = StatevectorEstimator()
    paulis = {'X': SparsePauliOp('X'), 'Y': SparsePauliOp('Y'), 'Z': SparsePauliOp('Z')}

    bloch = {}
    for name, obs in paulis.items():
        result = estimator.run([(qc, obs)]).result()
        bloch[name] = result[0].data.evs
    return bloch

# Estado a caracterizar: |+i> = (|0> + i|1>)/sqrt(2)
qc = QuantumCircuit(1)
qc.h(0)
qc.s(0)

bloch = qubit_tomography(qc)
print("Vector de Bloch reconstruido:")
for axis, val in bloch.items():
    print(f"  r_{axis} = {val:.4f}")

# Reconstruir la matriz de densidad
rx, ry, rz = bloch['X'], bloch['Y'], bloch['Z']
rho = 0.5 * (np.eye(2) + rx * np.array([[0,1],[1,0]])
                         + ry * np.array([[0,-1j],[1j,0]])
                         + rz * np.array([[1,0],[0,-1]]))

print(f"\nMatriz de densidad reconstruida:\n{rho}")
print(f"Traza: {np.trace(rho).real:.4f}")
print(f"Pureza: {np.trace(rho @ rho).real:.4f}")
```

## 7. Ideas clave

- La QST reconstruye $\rho$ midiendo el mismo estado muchas veces en distintas bases.
- Para $n$ qubits, la QST completa requiere $4^n - 1$ parámetros y escala exponencialmente.
- La MLE garantiza que la matriz de densidad reconstruida sea válida semidefinida positiva.
- Las técnicas escalables (compressed sensing, shadow tomography) aplican a estados con estructura especial.
- La QST es el método de referencia para verificar experimentalmente la preparación de estados cuánticos.

## 8. Ejercicios sugeridos

1. Implementar la tomografía de un qubit en Qiskit y verificar que para el estado $|1\rangle$ se obtiene $(r_x, r_y, r_z) = (0, 0, -1)$.
2. Estimar la incertidumbre estadística de $r_z$ como función del número de disparos $N$.
3. Construir la matriz de densidad del estado de Bell $|\Phi^+\rangle$ y verificar que tiene pureza $1$.
4. Calcular cuántas mediciones se necesitan para estimar los 15 parámetros de un estado de 2 qubits con precisión $\pm 0.01$ con probabilidad $95\%$.

## Navegacion

- Anterior: [Limites de la ventaja y comparacion clasica](../18_complejidad_cuantica/02_limites_de_la_ventaja_y_comparacion_clasica.md)
- Siguiente: [Fidelidad y caracterizacion operacional](02_fidelidad_y_caracterizacion_operacional.md)
