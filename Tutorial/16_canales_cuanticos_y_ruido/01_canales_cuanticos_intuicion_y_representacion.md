# Canales cuánticos: intuición y representación

## 1. Más allá de la evolución unitaria

Hasta ahora, toda la dinámica cuántica estudiada ha sido **unitaria**: el estado evoluciona mediante $|\psi\rangle \to U|\psi\rangle$ con $UU^\dagger = I$. Esta descripción es exacta para sistemas aislados.

En la realidad, ningún sistema cuántico está completamente aislado. El qubit está acoplado a su entorno: fluctuaciones térmicas, radiación electromagnética, vibraciones del sustrato, campos magnéticos parásitos. Este acoplamiento provoca que el sistema cuántico pierda información hacia el entorno, fenómeno conocido como **decoherencia**.

Para describir la dinámica de sistemas cuánticos abiertos, necesitamos un formalismo más general: los **canales cuánticos**.

## 2. Matrices de densidad: estados mixtos

Para un sistema cuántico abierto, el estado no puede describirse siempre mediante un vector de estado $|\psi\rangle$. En general, se necesita la **matriz de densidad** $\rho$:

$$
\rho = \sum_i p_i |\psi_i\rangle\langle\psi_i|, \quad p_i \geq 0, \quad \sum_i p_i = 1
$$

Las propiedades esenciales de $\rho$:
- **Hermitiana:** $\rho = \rho^\dagger$.
- **Semidefinida positiva:** $\langle\phi|\rho|\phi\rangle \geq 0$ para todo $|\phi\rangle$.
- **Traza unitaria:** $\text{Tr}(\rho) = 1$.

El estado es **puro** si $\rho = |\psi\rangle\langle\psi|$ (con $\text{Tr}(\rho^2) = 1$) y **mixto** si $\text{Tr}(\rho^2) < 1$.

Para un qubit, la matriz de densidad más general es:

$$
\rho = \frac{1}{2}(I + \vec{r} \cdot \vec{\sigma}) = \frac{1}{2}\begin{pmatrix} 1+r_z & r_x - ir_y \\ r_x + ir_y & 1-r_z \end{pmatrix}
$$

donde $\vec{r} = (r_x, r_y, r_z)$ es el **vector de Bloch** con $|\vec{r}| \leq 1$. Los estados puros corresponden a $|\vec{r}| = 1$ (superficie de la esfera de Bloch); los mixtos, a $|\vec{r}| < 1$ (interior).

## 3. Canales cuánticos: la clase CPTP

Un **canal cuántico** $\mathcal{E}$ es un mapa lineal que transforma matrices de densidad:

$$
\rho \to \mathcal{E}(\rho)
$$

Para que $\mathcal{E}(\rho)$ sea siempre una matriz de densidad válida, el canal debe satisfacer dos condiciones:

- **Completamente positivo (CP):** $\mathcal{E} \otimes \mathcal{I}$ es positivo para cualquier extensión del sistema. Esto garantiza que el mapa sigue siendo físico cuando se considera el sistema como parte de uno mayor.
- **Trazante (TP):** $\text{Tr}(\mathcal{E}(\rho)) = 1$ para todo $\rho$. Conserva la normalización.

Los mapas CPTP son exactamente los canales cuánticos físicamente realizables.

## 4. La representación de Kraus

Todo canal CPTP admite una representación mediante **operadores de Kraus** $\{K_i\}$:

$$
\mathcal{E}(\rho) = \sum_i K_i \rho K_i^\dagger
$$

con la condición de completitud:

$$
\sum_i K_i^\dagger K_i = I
$$

Esta condición garantiza que $\text{Tr}(\mathcal{E}(\rho)) = 1$.

**Interpretación:** cada término $K_i \rho K_i^\dagger$ puede interpretarse como el estado resultante si ocurrió el "salto cuántico" $i$, con probabilidad $p_i = \text{Tr}(K_i^\dagger K_i \rho)$. El canal suma sobre todos los posibles saltos, sin revelar cuál ocurrió.

## 5. El canal despolarizante

El canal despolarizante con parámetro $p \in [0, 1]$ modela ruido isotrópico: con probabilidad $p$ el qubit sufre uno de los tres errores de Pauli con igual probabilidad, y con probabilidad $1-p$ no ocurre nada:

$$
\mathcal{D}_p(\rho) = (1-p)\rho + \frac{p}{3}(X\rho X + Y\rho Y + Z\rho Z)
$$

En términos del vector de Bloch:

$$
\vec{r} \to \left(1 - \frac{4p}{3}\right)\vec{r}
$$

El canal contrae la esfera de Bloch uniformemente. Para $p = 3/4$, el estado se vuelve completamente mixto ($\rho = I/2$).

## 6. Implementación en Qiskit

```python
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp, DensityMatrix

# Simular un qubit bajo canal despolarizante
p_depol = 0.1  # Probabilidad de error

noise_model = NoiseModel()
depol_error = depolarizing_error(p_depol, 1)
noise_model.add_all_qubit_quantum_error(depol_error, ['x', 'h', 'ry'])

# Preparar |+> y medir <X> con ruido
qc = QuantumCircuit(1)
qc.h(0)

# Sin ruido: <X> = 1.0
# Con despolarización p=0.1: <X> = (1 - 4*0.1/3) * 1.0 ≈ 0.867
backend = AerSimulator(noise_model=noise_model)

# Visualizar la contracción del vector de Bloch
from qiskit.quantum_info import Statevector
rho_puro = DensityMatrix.from_label('+')
print(f"Vector de Bloch puro: {rho_puro.expectation_value(SparsePauliOp('X')).real:.3f}")

# Canal despolarizante manual
def depolarizing_channel(rho_matrix, p):
    from qiskit.quantum_info import Operator
    I = np.eye(2) / 2
    X = np.array([[0,1],[1,0]])
    Y = np.array([[0,-1j],[1j,0]])
    Z = np.array([[1,0],[0,-1]])
    return (1-p)*rho_matrix + p/3 * (X @ rho_matrix @ X + Y @ rho_matrix @ Y + Z @ rho_matrix @ Z)

import numpy as np
rho = np.array([[0.5, 0.5], [0.5, 0.5]])  # |+><+|
rho_noisy = depolarizing_channel(rho, p_depol)
print(f"Vector de Bloch tras despolarización: {np.trace(np.array([[0,1],[1,0]]) @ rho_noisy).real:.3f}")
```

## 7. Ideas clave

- Los canales cuánticos describen la evolución de sistemas cuánticos abiertos en contacto con un entorno.
- Las matrices de densidad $\rho$ representan tanto estados puros como mixtos.
- Un canal cuántico físico es un mapa CPTP: completamente positivo y trazante.
- La representación de Kraus descompone el canal en "saltos cuánticos" discretos: $\mathcal{E}(\rho) = \sum_i K_i \rho K_i^\dagger$.
- El canal despolarizante contrae el vector de Bloch uniformemente hacia el origen.

## 8. Ejercicios sugeridos

1. Verificar que los operadores de Kraus del canal despolarizante ($\sqrt{1-p}I$, $\sqrt{p/3}X$, $\sqrt{p/3}Y$, $\sqrt{p/3}Z$) satisfacen la condición de completitud $\sum_i K_i^\dagger K_i = I$.
2. Calcular el efecto del canal despolarizante sobre el estado $|1\rangle$ y representarlo en la esfera de Bloch.
3. Verificar que la evolución unitaria $U|\psi\rangle$ es un caso especial de canal cuántico con un solo operador de Kraus.
4. Calcular el estado de salida de una cadena de dos canales despolarizantes con parámetros $p_1 = 0.1$ y $p_2 = 0.2$.

## Navegacion

- Anterior: [Evolucion unitaria y Trotterizacion](../15_hamiltonianos_y_evolucion_temporal/02_evolucion_unitaria_y_trotterizacion.md)
- Siguiente: [Operadores de Kraus, decoherencia y modelos efectivos](02_kraus_decoherencia_y_modelos_efectivos.md)
