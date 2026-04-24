# Medidas proyectivas, valores esperados y varianza

## 1. La medida proyectiva estándar

Cuando medimos un qubit en la base computacional ($Z$), obtenemos $0$ o $1$ con probabilidades $|\alpha|^2$ y $|\beta|^2$ respectivamente. Este es el caso más simple de una **medida proyectiva**.

En general, una medida proyectiva en la base de autovectores $\{|v_k\rangle\}$ de un observable $O$ con autovalores $\{\lambda_k\}$ funciona así:

1. El resultado de la medición es algún $\lambda_k$.
2. La probabilidad de obtener $\lambda_k$ es $p_k = \langle\psi|P_k|\psi\rangle$, donde $P_k = |v_k\rangle\langle v_k|$ es el proyector.
3. Tras la medición, el estado colapsa: $|\psi\rangle \to |v_k\rangle$.

Para estados mixtos con matriz de densidad $\rho$:

$$
p_k = \text{Tr}(P_k \rho)
$$

Los proyectores son operadores hermitianos idempotentes: $P_k^2 = P_k$, $P_k^\dagger = P_k$.

## 2. Valor esperado de un observable

El **valor esperado** de un observable $O$ en el estado $|\psi\rangle$ es:

$$
\langle O \rangle = \langle\psi|O|\psi\rangle = \sum_k \lambda_k \, p_k
$$

Es la media ponderada de los posibles resultados de la medición, con pesos iguales a sus probabilidades.

Para estados mixtos:

$$
\langle O \rangle = \text{Tr}(O\rho)
$$

Esta fórmula es fundamental: el `Estimator` de Qiskit calcula precisamente $\text{Tr}(O\rho)$ para un circuito que prepara $\rho$ y un observable $O$ expresado como `SparsePauliOp`.

## 3. Varianza y el principio de incertidumbre

La **varianza** de un observable $O$ en el estado $|\psi\rangle$ mide la dispersión de los resultados de la medición:

$$
\text{Var}(O) = \langle O^2 \rangle - \langle O \rangle^2 = \langle\psi|(O - \langle O\rangle)^2|\psi\rangle
$$

La varianza cuántica es genuinamente diferente del ruido clásico: incluso con un aparato de medición perfecto, múltiples mediciones del mismo estado cuántico (preparado idénticamente) darán resultados distintos. Esta dispersión es intrínseca al estado cuántico, no una imperfección experimental.

El **principio de incertidumbre de Heisenberg** establece que para dos observables $A$ y $B$:

$$
\text{Var}(A) \cdot \text{Var}(B) \geq \frac{1}{4}|\langle[A, B]\rangle|^2
$$

Para posición $X$ y momento $P$ con $[X, P] = i\hbar$: $\Delta x \cdot \Delta p \geq \hbar/2$.

Para $X$ y $Z$ en un qubit con $[X, Z] = -2iY$: $\Delta X \cdot \Delta Z \geq |\langle Y \rangle|$.

## 4. Medir en bases distintas

Para medir un observable $O$ con autovectores distintos de la base computacional, se aplica una rotación unitaria $V$ que lleva los autovectores de $O$ a la base computacional, y luego se mide en $Z$:

- **Medir $X$:** aplicar $H$ y medir en $Z$. ($H$ lleva $|+\rangle \to |0\rangle$, $|-\rangle \to |1\rangle$).
- **Medir $Y$:** aplicar $S^\dagger H$ y medir en $Z$. ($S^\dagger H$ lleva $|+i\rangle \to |0\rangle$, $|-i\rangle \to |1\rangle$).

Para un observable de $n$ qubits expresado como suma de Pauli $O = \sum_k c_k P_k$, el valor esperado se calcula midiendo cada término $P_k$ por separado y sumando con sus coeficientes:

$$
\langle O \rangle = \sum_k c_k \langle P_k \rangle
$$

## 5. Implementación en Qiskit

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator, StatevectorSampler
from qiskit.quantum_info import SparsePauliOp, Statevector
import numpy as np

# Preparar el estado |psi> = cos(θ/2)|0> + sin(θ/2)|1>
theta = np.pi / 3

qc = QuantumCircuit(1)
qc.ry(theta, 0)

# Calcular valores esperados con Estimator
estimator = StatevectorEstimator()
observables = {
    'X': SparsePauliOp('X'),
    'Y': SparsePauliOp('Y'),
    'Z': SparsePauliOp('Z'),
}

print(f"Estado: cos({theta/2:.2f})|0> + sin({theta/2:.2f})|1>")
print(f"Vector de Bloch esperado: ({np.sin(theta):.3f}, 0, {np.cos(theta):.3f})")
print()

for name, obs in observables.items():
    result = estimator.run([(qc, obs)]).result()
    ev = result[0].data.evs
    print(f"<{name}> = {ev:.4f}")

# Calcular varianza de Z
sv = Statevector(qc)
ev_Z = sv.expectation_value(SparsePauliOp('Z')).real
ev_Z2 = sv.expectation_value(SparsePauliOp.from_list([('ZZ', 1)])).real  # Esto no es correcto para varianza
# Varianza de Z = <Z^2> - <Z>^2 = 1 - cos^2(theta) = sin^2(theta)
var_Z = 1 - np.cos(theta)**2  # Z^2 = I, así <Z^2> = 1
print(f"\nVar(Z) = {var_Z:.4f} = sin^2({theta:.2f}) = {np.sin(theta)**2:.4f}")
```

## 6. Postselección y medidas parciales

En sistemas de varios qubits, es frecuente medir solo algunos qubits dejando el resto en superposición. La **medida parcial** sobre el qubit $k$ colapsa ese qubit pero deja el resto del sistema en un estado condicionado al resultado.

Para el estado de Bell $|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$:
- Si medimos el qubit 0 y obtenemos $0$: el qubit 1 colapsa a $|0\rangle$.
- Si medimos el qubit 0 y obtenemos $1$: el qubit 1 colapsa a $|1\rangle$.

Esta correlación instantánea es la esencia del entrelazamiento y la base de la teleportación cuántica.

## 7. Ideas clave

- Los proyectores $P_k = |v_k\rangle\langle v_k|$ definen una medida proyectiva; la probabilidad de obtener $\lambda_k$ es $\text{Tr}(P_k \rho)$.
- El valor esperado $\langle O \rangle = \text{Tr}(O\rho)$ es la media de los posibles resultados.
- La varianza cuántica $\text{Var}(O) = \langle O^2\rangle - \langle O\rangle^2$ es intrínseca al estado, no un ruido experimental.
- Para medir en la base de $O$, se aplica la rotación que lleva los autovectores de $O$ a la base computacional.
- El `Estimator` de Qiskit evalúa $\text{Tr}(O\rho)$ eficientemente para observables expresados en `SparsePauliOp`.

## 8. Ejercicios sugeridos

1. Calcular $\langle X \rangle$, $\langle Y \rangle$, $\langle Z \rangle$ para el estado $|{+i}\rangle = \frac{1}{\sqrt{2}}(|0\rangle + i|1\rangle)$.
2. Verificar el principio de incertidumbre $\text{Var}(X)\cdot\text{Var}(Z) \geq |\langle Y \rangle|^2$ para el estado $|+\rangle$.
3. Implementar en Qiskit la medición del observable $H = Z \otimes Z + X \otimes I$ sobre el estado de Bell.
4. Calcular la varianza de $Z$ para los estados $|0\rangle$, $|1\rangle$, $|+\rangle$ y $\frac{\sqrt{3}}{2}|0\rangle + \frac{1}{2}|1\rangle$.

## Navegacion

- Anterior: [Operadores de Kraus, decoherencia y modelos efectivos](../16_canales_cuanticos_y_ruido/02_kraus_decoherencia_y_modelos_efectivos.md)
- Siguiente: [POVM: intuicion y medicion generalizada](02_povm_intuicion_y_medicion_generalizada.md)
