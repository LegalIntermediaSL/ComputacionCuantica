# Coherencia, entrelazamiento y teoría de recursos

## 1. Recursos cuánticos: un marco operacional

En los primeros capítulos tratamos la coherencia y el entrelazamiento como propiedades de los estados cuánticos. La **teoría de recursos cuánticos** adopta un punto de vista más operacional: estos fenómenos son *recursos* que se pueden consumir, transformar y cuantificar, análogos a la energía libre en termodinámica.

La idea central es definir:
1. Un conjunto de **operaciones libres** (operaciones que no cuestan el recurso).
2. Un **estado libre** (el estado que se puede preparar sin el recurso).
3. Una **medida del recurso** que cuantifica cuánto del recurso tiene un estado.

## 2. Teoría de la coherencia

### 2.1 Estados libres y operaciones libres

En la teoría de coherencia, los **estados libres** son los estados incoherentes: matrices de densidad diagonales en la base computacional,

$$
\delta = \sum_i p_i |i\rangle\langle i|
$$

Las **operaciones libres** son las operaciones incoherentes completamente positivas y que preservan la traza (ICPTP), cuya acción sobre estados incoherentes produce solo estados incoherentes.

### 2.2 Medidas de coherencia

Una función $\mathcal{C}(\rho) \geq 0$ es una medida de coherencia válida si:
- $\mathcal{C}(\delta) = 0$ para todo estado incoherente $\delta$.
- $\mathcal{C}$ no aumenta bajo operaciones incoherentes.

Medidas fundamentales:

**Coherencia $\ell_1$:** suma de los valores absolutos de los elementos fuera de la diagonal:
$$
\mathcal{C}_{\ell_1}(\rho) = \sum_{i \neq j} |\rho_{ij}|
$$

**Coherencia relativa de entropía:**
$$
\mathcal{C}_\text{rel}(\rho) = S(\Delta(\rho)) - S(\rho) = H(\vec{p}) - S(\rho)
$$
donde $\Delta(\rho)$ es $\rho$ dephaseada (diagonal), $H(\vec{p})$ es la entropía de Shannon de las poblaciones y $S(\rho) = -\text{Tr}(\rho\log\rho)$ es la entropía de von Neumann.

### 2.3 Coherencia y ventaja cuántica

Un estado con $\mathcal{C}(\rho) > 0$ puede exhibir interferencia cuántica. Sin coherencia no hay interferencia, y sin interferencia los algoritmos como Deutsch-Jozsa, Grover o QFT pierden su ventaja: el circuito colapsa en un proceso clásico estocástico.

Formalmente: si todos los estados del circuito son incoherentes, los valores esperados son clásicamente reproducibles con muestreo de Monte Carlo eficiente.

## 3. Teoría del entrelazamiento

### 3.1 Estados libres y operaciones LOCC

Para sistemas bipartitos $AB$, los **estados libres** son los estados separables:
$$
\rho_\text{sep} = \sum_k p_k \rho_k^A \otimes \rho_k^B, \quad p_k \geq 0, \quad \sum_k p_k = 1
$$

Las **operaciones libres** son las operaciones **LOCC** (Local Operations and Classical Communication): cada parte puede hacer cualquier operación local y pueden comunicar clásicamente, pero no pueden crear entrelazamiento.

### 3.2 Medidas de entrelazamiento

Para estados puros bipartitos $|\psi\rangle_{AB}$, la medida canónica es la **entropía de entrelazamiento**:
$$
E(|\psi\rangle) = S(\rho_A) = -\text{Tr}(\rho_A \log \rho_A)
$$
donde $\rho_A = \text{Tr}_B(|\psi\rangle\langle\psi|)$ es el estado reducido de $A$.

Para los cuatro estados de Bell: $E = 1$ ebit (máximo para un par de qubits).
Para estados producto $|\phi\rangle \otimes |\chi\rangle$: $E = 0$.

Para estados mixtos, la situación es más compleja. Medidas como la **formación de entrelazamiento** $E_F$ y la **entropía de entrelazamiento destilable** $E_D$ satisfacen $E_D \leq E_F$.

### 3.3 Destilación y dilución de entrelazamiento

Dado un suministro de $n$ copias de un estado entrelazado $\rho^{\otimes n}$, las tareas asintóticas fundamentales son:

**Destilación:** ¿Cuántos pares de Bell máximamente entrelazados $|\Phi^+\rangle$ se pueden extraer usando LOCC?
$$
E_D(\rho) = \lim_{n\to\infty} \frac{m^*(n)}{n}
$$

**Dilución:** ¿Cuántos $|\Phi^+\rangle$ se necesitan para preparar $n$ copias de $\rho$?
$$
E_C(\rho) = \lim_{n\to\infty} \frac{m_{\min}(n)}{n}
$$

Para estados puros: $E_D = E_C = S(\rho_A)$. Para estados mixtos, la brecha $E_D < E_C$ indica irreversibilidad termodinámica.

## 4. Entrelazamiento como recurso computacional

El entrelazamiento es necesario (aunque no suficiente) para la ventaja cuántica en muchos contextos:

**Teleportación cuántica:** requiere un par de Bell compartido. Con él, Alice puede transmitir un qubit arbitrario a Bob usando solo 2 bits clásicos. Sin el par entrelazado, la teleportación es imposible.

**Speedup en computación:** el teorema de Gottesman-Knill muestra que los circuitos de Clifford (sin entrelazamiento genuino de recursos) son simulables clásicamente en tiempo polinomial. El entrelazamiento multiqubit no estabilizador es necesario para ventaja computacional.

**Estimaciones cuantitativas:** para algoritmos como Shor, se genera un entrelazamiento que crece linealmente con el tamaño del registro, lo que explica por qué la simulación clásica exacta requiere $O(2^n)$ memoria.

## 5. Coherencia y entrelazamiento: relaciones

Coherencia y entrelazamiento no son independientes:

- Un estado sin coherencia en ninguna base factorizable no puede estar entrelazado.
- La **incoherencia relativa** de un estado bajo la base de Bell es exactamente su entrelazamiento.
- La coherencia puede convertirse en entrelazamiento: si Alice aplica un CNOT controlado por su qubit coherente a un qubit de Bob en $|0\rangle$, la coherencia del qubit de Alice se convierte en entrelazamiento del par.

Esta dualidad recursos-operaciones es una de las intuiciones más fecundas de la información cuántica moderna.

## 6. Implementación: medición de coherencia con Qiskit

```python
from qiskit.quantum_info import DensityMatrix, entropy
import numpy as np

def coherence_l1(rho: np.ndarray) -> float:
    """Coherencia ℓ₁: suma de |ρ_ij| para i≠j."""
    n = rho.shape[0]
    total = 0.0
    for i in range(n):
        for j in range(n):
            if i != j:
                total += abs(rho[i, j])
    return total

def entanglement_entropy(state_vector: np.ndarray, dim_A: int) -> float:
    """Entropía de entrelazamiento de un estado puro bipartito."""
    n_total = len(state_vector)
    dim_B = n_total // dim_A
    # Reshape a matriz dim_A × dim_B
    psi = state_vector.reshape(dim_A, dim_B)
    # Estado reducido de A: ρ_A = ψ ψ†
    rho_A = psi @ psi.conj().T
    dm_A = DensityMatrix(rho_A)
    return entropy(dm_A, base=2)

# Estado |+> = (|0> + |1>) / sqrt(2)
rho_plus = np.array([[0.5, 0.5], [0.5, 0.5]])
print(f"Coherencia ℓ₁ de |+>: {coherence_l1(rho_plus):.4f}")  # 1.0

# Estado |0>
rho_zero = np.array([[1.0, 0.0], [0.0, 0.0]])
print(f"Coherencia ℓ₁ de |0>: {coherence_l1(rho_zero):.4f}")  # 0.0

# Par de Bell |Φ+> = (|00> + |11>) / sqrt(2)
phi_plus = np.array([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)])
E = entanglement_entropy(phi_plus, dim_A=2)
print(f"Entropía de entrelazamiento de |Φ+>: {E:.4f} ebits")  # 1.0

# Estado producto |+0> = |+> ⊗ |0>
product = np.array([1/np.sqrt(2), 0, 1/np.sqrt(2), 0])
E_prod = entanglement_entropy(product, dim_A=2)
print(f"Entropía de entrelazamiento de |+0>: {E_prod:.4f} ebits")  # 0.0
```

## 7. Ideas clave

- La coherencia y el entrelazamiento son recursos operacionales cuantificables, no meras propiedades matemáticas.
- Las medidas de coherencia válidas deben ser cero para estados diagonales y no aumentar bajo operaciones incoherentes.
- La entropía de entrelazamiento mide cuántos ebits contiene un estado puro bipartito.
- Sin coherencia no hay interferencia; sin entrelazamiento, los circuitos de Clifford son simulables clásicamente.
- Coherencia y entrelazamiento están relacionados: la coherencia de un qubit puede "convertirse" en entrelazamiento mediante un CNOT.

## 8. Ejercicios sugeridos

1. Calcular la coherencia $\ell_1$ y la entropía relativa de coherencia del estado $\rho = \frac{3}{4}|0\rangle\langle 0| + \frac{1}{4}|1\rangle\langle 1| + \frac{i}{4}|0\rangle\langle 1| - \frac{i}{4}|1\rangle\langle 0|$.
2. Demostrar que la entropía de entrelazamiento de un estado producto es cero para cualquier corte bipartito.
3. Verificar numéricamente que aplicar un CNOT a $|+\rangle \otimes |0\rangle$ produce un estado con $E = 1$ ebit.
4. Explicar por qué la destilación de entrelazamiento es irreversible para estados mixtos genéricos.

## Navegacion

- Anterior: [Decoherencia, relajacion y markovianidad](../21_open_quantum_systems/02_decoherencia_relajacion_y_markovianidad.md)
- Siguiente: [No-clonacion y limites operacionales](02_no_clonacion_y_limites_operacionales.md)
