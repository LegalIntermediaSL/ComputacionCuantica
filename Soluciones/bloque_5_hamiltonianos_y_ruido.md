# Soluciones: Hamiltonianos, Evolución Temporal y Ruido Avanzado

Soluciones detalladas para los ejercicios de los módulos 15, 16, 17 y 21.

---

## Módulo 15: Hamiltonianos y Evolución Temporal

### Ejercicio 1: Descomponer $H = X \otimes Z + Z \otimes X$ en la base de Pauli

**Enunciado:** Expresar el Hamiltoniano $H = X_0 Z_1 + Z_0 X_1$ como `SparsePauliOp`.

**Solución:**
```python
from qiskit.quantum_info import SparsePauliOp

# En la convención de Qiskit, el qubit 0 es el menos significativo (posición derecha)
H = SparsePauliOp.from_list([("ZX", 1.0), ("XZ", 1.0)])
print(H)
# Autovalores: λ ∈ {-√2, -√2, √2, √2} → E_0 = -√2 ≈ -1.4142
import numpy as np
eigvals = np.linalg.eigvalsh(H.to_matrix())
print(f"Autovalores: {eigvals}")
print(f"Energía del estado fundamental: {eigvals[0]:.6f}")
```

**Respuesta:** $H = ZX + XZ$ con autovalores $\pm\sqrt{2}$ (degenerados). La energía fundamental es $E_0 = -\sqrt{2} \approx -1.4142$.

---

### Ejercicio 2: Error de Trotter para $H = XX + ZI$, n pasos

**Enunciado:** Calcular el error de Trotter $\|e^{-iHt} - (e^{-iAdt}e^{-iBdt})^n\|$ para $A = XX$, $B = ZI$, $t = 1$, $n = 5, 10, 20$.

**Solución:**
```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
import numpy as np

A = np.array([[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]], dtype=complex)  # XX
Z = np.array([[1,0],[0,-1]], dtype=complex)
I = np.eye(2, dtype=complex)
B = np.kron(Z, I)  # ZI

H_mat = A + B
t = 1.0

U_exact = np.linalg.matrix_power(
    np.eye(4, dtype=complex), 1  # placeholder
)
from scipy.linalg import expm
U_exact = expm(-1j * H_mat * t)

for n in [5, 10, 20]:
    dt = t / n
    U_A = expm(-1j * A * dt)
    U_B = expm(-1j * B * dt)
    U_trotter_step = U_A @ U_B
    U_trotter = np.linalg.matrix_power(U_trotter_step, n)
    error = np.linalg.norm(U_exact - U_trotter, ord=2)
    print(f"n={n:3d}: error = {error:.6f}  (teoría: ~{t**2/(2*n) * np.linalg.norm(A@B - B@A, ord=2):.6f})")
```

**Resultado esperado:** el error escala como $O(t^2/n)$, con valores aproximados $\approx 0.12$ ($n=5$), $0.06$ ($n=10$), $0.03$ ($n=20$).

---

### Ejercicio 3: Energía de Heisenberg de 2 qubits con VQE

**Enunciado:** Usar VQE para encontrar la energía fundamental de $H = XX + YY + ZZ$.

**Solución:**
```python
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import EfficientSU2
from qiskit.primitives import StatevectorEstimator
from scipy.optimize import minimize
import numpy as np

H = SparsePauliOp.from_list([("XX", 1.0), ("YY", 1.0), ("ZZ", 1.0)])
# Autovalor exacto: E_0 = -3 (estado singlete de Bell)
print(f"E_0 exacta: {np.linalg.eigvalsh(H.to_matrix())[0]:.6f}")  # -3.0

ansatz = EfficientSU2(2, reps=1)
estimator = StatevectorEstimator()

def cost(params):
    bound = ansatz.assign_parameters(params)
    return float(estimator.run([(bound, H)]).result()[0].data.evs)

np.random.seed(42)
x0 = np.random.uniform(-np.pi, np.pi, ansatz.num_parameters)
res = minimize(cost, x0, method="COBYLA", options={"maxiter": 500})
print(f"VQE encontró E_0 = {res.fun:.6f}")
```

**Resultado:** VQE converge a $E_0 \approx -3.0$ (el estado singlete $|\Psi^-\rangle$ tiene $\langle H \rangle = -3$).

---

## Módulo 16: Canales Cuánticos y Ruido

### Ejercicio 4: Vector de Bloch bajo canal despolarizante

**Enunciado:** Para el estado $|+\rangle$ y canal despolarizante con $p = 0.3$, calcular el vector de Bloch resultante.

**Solución:**

Estado inicial $|+\rangle$: $\rho = \begin{pmatrix}1/2 & 1/2 \\ 1/2 & 1/2\end{pmatrix}$, vector de Bloch $\vec{r} = (1, 0, 0)$.

Canal despolarizante: $\vec{r} \to (1 - 4p/3)\vec{r}$.

Para $p = 0.3$: $1 - 4(0.3)/3 = 1 - 0.4 = 0.6$.

Vector de Bloch resultante: $\vec{r}' = (0.6, 0, 0)$.

```python
import numpy as np
from qiskit.quantum_info import DensityMatrix, Statevector

rho0 = np.array([[0.5, 0.5], [0.5, 0.5]])  # |+><+|
p = 0.3
X = np.array([[0,1],[1,0]])
Y = np.array([[0,-1j],[1j,0]])
Z = np.array([[1,0],[0,-1]])
rho_out = (1-p)*rho0 + (p/3)*(X@rho0@X + Y@rho0@Y + Z@rho0@Z)
print(f"ρ_out = {rho_out}")
print(f"Vector de Bloch: r_x = {2*rho_out[0,1].real:.4f}, r_y = {2*rho_out[0,1].imag:.4f}, r_z = {(rho_out[0,0]-rho_out[1,1]).real:.4f}")
# Salida: r_x = 0.6, r_y = 0.0, r_z = 0.0
```

---

### Ejercicio 5: Operadores de Kraus del canal de amortiguamiento de amplitud

**Enunciado:** Verificar que los operadores $K_0 = \begin{pmatrix}1&0\\0&\sqrt{1-\gamma}\end{pmatrix}$, $K_1 = \begin{pmatrix}0&\sqrt{\gamma}\\0&0\end{pmatrix}$ satisfacen $\sum_i K_i^\dagger K_i = I$.

**Solución:**
```python
import numpy as np
gamma = 0.5
K0 = np.array([[1, 0], [0, np.sqrt(1 - gamma)]])
K1 = np.array([[0, np.sqrt(gamma)], [0, 0]])
completeness = K0.conj().T @ K0 + K1.conj().T @ K1
print(f"K0†K0 + K1†K1 = {completeness}")
# Debe ser la identidad [[1,0],[0,1]]
```

**Explicación:** $K_0^\dagger K_0 + K_1^\dagger K_1 = \begin{pmatrix}1&0\\0&1-\gamma\end{pmatrix} + \begin{pmatrix}0&0\\0&\gamma\end{pmatrix} = I$. ✓

---

## Módulo 17: Medición Avanzada y POVM

### Ejercicio 6: Cota de Helstrom para estados de Bell cuasi-ortogonales

**Enunciado:** Calcular la probabilidad mínima de error para distinguir $|\Phi^+\rangle$ y $|\Phi^-\rangle$ con probabilidades a priori iguales.

**Solución:**

$|\langle\Phi^+|\Phi^-\rangle|^2 = 0$ (estados ortogonales). La cota de Helstrom:

$$P_e = \frac{1}{2}\left(1 - \sqrt{1 - 4 p_0 p_1 |\langle\psi_0|\psi_1\rangle|^2}\right) = \frac{1}{2}(1 - \sqrt{1 - 0}) = 0
$$

Con $p_0 = p_1 = 1/2$ y estados ortogonales, la probabilidad de error óptima es **cero**: los estados pueden distinguirse perfectamente por medición en la base de Bell.

```python
import numpy as np

phi_plus  = np.array([1, 0, 0, 1]) / np.sqrt(2)
phi_minus = np.array([1, 0, 0, -1]) / np.sqrt(2)
overlap   = abs(phi_plus @ phi_minus)**2
p0 = p1 = 0.5
P_e = 0.5 * (1 - np.sqrt(1 - 4 * p0 * p1 * overlap))
print(f"|⟨Φ+|Φ-⟩|² = {overlap:.6f}")
print(f"P_e (Helstrom) = {P_e:.6f}")  # 0.0
```

---

## Módulo 21: Open Quantum Systems

### Ejercicio 7: Calcular $T_\phi$ dado $T_1 = 150\,\mu s$ y $T_2 = 80\,\mu s$

**Enunciado:** Usando $\frac{1}{T_2} = \frac{1}{2T_1} + \frac{1}{T_\phi}$, calcular $T_\phi$.

**Solución:**

$$\frac{1}{T_\phi} = \frac{1}{T_2} - \frac{1}{2T_1} = \frac{1}{80\,\mu s} - \frac{1}{300\,\mu s}$$

```python
T1 = 150e-6  # s
T2 = 80e-6   # s

T_phi = 1 / (1/T2 - 1/(2*T1))
print(f"1/T_phi = {1/T2:.4e} - {1/(2*T1):.4e} = {1/T2 - 1/(2*T1):.4e} s⁻¹")
print(f"T_phi = {T_phi*1e6:.2f} μs")
```

**Resultado:** $T_\phi = \frac{1}{1/80 - 1/300}\,\mu s = \frac{1}{0.01250 - 0.00333}\,\mu s = \frac{1}{0.00917} = 109.1\,\mu s$.

---

### Ejercicio 8: Profundidad máxima de circuito

**Enunciado:** $T_2 = 200\,\mu s$, puertas CNOT de $200\,\text{ns}$. ¿Cuántos CNOTs caben?

**Solución:**

$$d_\text{max} = \frac{T_2}{t_\text{gate}} = \frac{200 \times 10^{-6}}{200 \times 10^{-9}} = 1000 \text{ puertas CNOT}$$

```python
T2 = 200e-6    # s
t_cnot = 200e-9  # s
d_max = T2 / t_cnot
print(f"Profundidad máxima: {d_max:.0f} puertas CNOT")
# Comparar con Shor RSA-2048: ~10^8 CNOTs
print(f"Fracción de Shor RSA-2048: {d_max/1e8*100:.4f}%")
```

**Resultado:** $d_\text{max} = 1000$ puertas CNOT. Esto es el $0.001\%$ de las puertas necesarias para el algoritmo de Shor en RSA-2048, ilustrando por qué la corrección de errores es imprescindible.
