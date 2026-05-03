# Soluciones: Algoritmos Avanzados (Módulos 18, 19, 20, 22)

---

## Módulo 18: Complejidad Cuántica

### Ejercicio 1: Verificar que el problema de Simon es en BQP pero no en BPP

**Enunciado:** Para una función $f: \{0,1\}^n \to \{0,1\}^n$ con período oculto $s$, comparar el coste clásico vs cuántico.

**Solución:**

**Clásico:** Con $m$ consultas aleatorias, la probabilidad de que dos inputs $x, x' = x \oplus s$ sean ambos elegidos es $\binom{2^{n-1}}{2}/\binom{2^n}{2} \approx 1/2$. Por el problema del cumpleaños, se necesitan $\Omega(2^{n/2})$ consultas para encontrar la colisión con probabilidad constante.

**Cuántico:** El algoritmo de Simon usa $O(n)$ consultas al oráculo, procesando superposiciones:
$$
\frac{1}{\sqrt{2^n}}\sum_x |x\rangle |0\rangle \xrightarrow{U_f} \frac{1}{\sqrt{2^n}}\sum_x |x\rangle|f(x)\rangle \xrightarrow{\text{medir }f(x)} \frac{1}{\sqrt{2}}(|x_0\rangle + |x_0\oplus s\rangle)
$$

Después de la QFT y medición, obtenemos $y$ con $y\cdot s = 0 \pmod{2}$. Con $n-1$ ecuaciones linealmente independientes, resolvemos para $s$.

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
import numpy as np

def simon_oracle(n: int, s: str) -> QuantumCircuit:
    """Oráculo de Simon para el período s."""
    qc = QuantumCircuit(2 * n)
    # Copiar los n qubits de entrada en los n qubits de salida
    for i in range(n):
        qc.cx(i, n + i)
    # Si el bit i de s es 1, aplicar XOR con el qubit i de salida
    for i, bit in enumerate(reversed(s)):
        if bit == "1":
            qc.cx(0, n + i)  # simplificado para demostración
    return qc

n, s = 3, "110"
qc = QuantumCircuit(2 * n, n)
qc.h(range(n))
qc.compose(simon_oracle(n, s), inplace=True)
qc.h(range(n))
qc.measure(range(n), range(n))

sampler = StatevectorSampler()
result = sampler.run([qc], shots=100).result()
print("Mediciones (y·s = 0 mod 2):")
print(result[0].data.c0.get_counts())
```

---

### Ejercicio 2: Verificar el teorema de Gottesman-Knill para el código de Bell

**Enunciado:** Mostrar que la preparación de $|\Phi^+\rangle = H_0 \cdot \text{CNOT}_{01}|00\rangle$ es simulable clásicamente.

**Solución:**

El estado $|\Phi^+\rangle$ es un **estado estabilizador**: es el único estado $+1$-autovector de $\{XX, ZZ\}$. El estabilizador es:
$$
\mathcal{S} = \langle XX, ZZ \rangle
$$

La descripción estabilizadora tiene $O(n)$ bits, no $O(2^n)$, confirmando la eficiencia clásica.

```python
# Verificación numérica del estabilizador
import numpy as np

XX = np.kron(np.array([[0,1],[1,0]]), np.array([[0,1],[1,0]]))
ZZ = np.kron(np.array([[1,0],[0,-1]]), np.array([[1,0],[0,-1]]))
phi_plus = np.array([1, 0, 0, 1]) / np.sqrt(2)

eigenval_XX = phi_plus @ XX @ phi_plus
eigenval_ZZ = phi_plus @ ZZ @ phi_plus
print(f"⟨Φ+|XX|Φ+⟩ = {eigenval_XX:.6f}")   # +1
print(f"⟨Φ+|ZZ|Φ+⟩ = {eigenval_ZZ:.6f}")   # +1
```

---

## Módulo 19: Tomografía y Caracterización

### Ejercicio 3: Verificar la desigualdad de Holevo para 1 qubit

**Enunciado:** Demostrar que un qubit puede transmitir como máximo 1 bit clásico.

**Solución:** La cota de Holevo establece que la información accesible está acotada por:
$$
\chi \leq S(\rho) \leq \log_2 d = 1 \text{ bit (para un qubit)}
$$

```python
from qiskit.quantum_info import DensityMatrix, entropy
import numpy as np

# Estado maximalmente mixto: entropía máxima
rho_mixed = DensityMatrix([[0.5, 0], [0, 0.5]])
print(f"S(ρ_mixed) = {entropy(rho_mixed, base=2):.4f} bits")   # 1.0

# Estado puro: entropía mínima
rho_pure = DensityMatrix([[1, 0], [0, 0]])
print(f"S(ρ_pure)  = {entropy(rho_pure, base=2):.4f} bits")    # 0.0

# Preparación de ensemble con 2 estados
rho_0 = DensityMatrix([[1, 0], [0, 0]])  # |0>
rho_1 = DensityMatrix([[0.5, 0.5], [0.5, 0.5]])  # |+>
p = 0.5
rho_avg = DensityMatrix(p * rho_0.data + (1-p) * rho_1.data)
chi = entropy(rho_avg, base=2) - p*entropy(rho_0, base=2) - (1-p)*entropy(rho_1, base=2)
print(f"χ (Holevo) = {chi:.4f} bits   (≤ 1)")
```

---

### Ejercicio 4: Randomized Benchmarking simplificado

**Enunciado:** Para un canal despolarizante con $p = 0.05$, calcular la fidelidad por puerta de Clifford y la curva RB.

**Solución:**

La fidelidad media por puerta Clifford es $r = 1 - p = 0.95$ y la curva de decaimiento RB:
$$
P(m) = A \cdot (1-p)^m + B
$$

```python
import numpy as np
import matplotlib.pyplot as plt

p_depol = 0.05
A, B = 0.5, 0.5  # constantes de preparación/medición
m_values = np.arange(0, 50, 5)
P_m = A * (1 - p_depol)**m_values + B

print("Curva RB:")
for m, p in zip(m_values, P_m):
    print(f"  m={m:3d}: P={p:.4f}")

# La tasa de error por puerta es p_depol = 0.05
r_clifford = 1 - p_depol
print(f"\nFidelidad por puerta Clifford: r = {r_clifford:.4f}")
print(f"P(m=20) = {A*(r_clifford)**20 + B:.4f}")
```

---

## Módulo 20: Simulación Cuántica Avanzada

### Ejercicio 5: Coste de Trotter para el modelo de Heisenberg 4 qubits

**Enunciado:** Calcular el número de CNOTs para simular el Hamiltoniano de Heisenberg de 4 qubits durante $t=1$ con $n=10$ pasos usando Trotter de primer orden.

**Solución:**

El Hamiltoniano de Heisenberg de 4 sitios tiene $3 \times 3 = 9$ términos (XX, YY, ZZ para cada enlace). Cada término de 2 qubits requiere 2 CNOTs.

$$
N_\text{CNOT} = n \times (\text{términos}) \times 2 = 10 \times 9 \times 2 = 180 \text{ CNOTs}
$$

```python
n_qubits = 4
n_enlaces = n_qubits - 1  # 3 enlaces en cadena
n_terminos_pauli = 3 * n_enlaces  # XX, YY, ZZ por enlace = 9
cnots_por_termino = 2  # para e^(-iθPQ) con P,Q ∈ {X,Y,Z}
n_pasos = 10
t = 1.0

total_cnots = n_pasos * n_terminos_pauli * cnots_por_termino
print(f"Heisenberg 4 qubits, n={n_pasos} pasos:")
print(f"  Términos de Pauli: {n_terminos_pauli}")
print(f"  CNOTs por paso: {n_terminos_pauli * cnots_por_termino}")
print(f"  CNOTs total: {total_cnots}")
```

**Resultado:** 180 CNOTs totales para 10 pasos de Trotter de primer orden.

---

## Módulo 22: Recursos Cuánticos

### Ejercicio 6: Verificar que el CNOT convierte coherencia en entrelazamiento

**Enunciado:** Mostrar que $\text{CNOT}_{01}(|+\rangle_0 \otimes |0\rangle_1) = |\Phi^+\rangle$.

**Solución:**

$$
\text{CNOT}|+\rangle|0\rangle = \text{CNOT}\frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)|0\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle) = |\Phi^+\rangle
$$

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

qc = QuantumCircuit(2)
qc.h(0)   # |+>|0>
qc.cx(0, 1)  # CNOT

sv = Statevector.from_instruction(qc)
print(f"Estado final: {sv}")
# [0.707+0j, 0, 0, 0.707+0j] = (|00> + |11>)/√2 = |Φ+>

# Medir entrelazamiento (entropía de von Neumann del estado reducido)
from qiskit.quantum_info import entropy, partial_trace
rho_full = sv.to_density_matrix()
# Estado reducido del qubit 0 (trazar qubit 1)
rho_0 = partial_trace(rho_full, [1])
E = entropy(rho_0, base=2)
print(f"Entropía de entrelazamiento: {E:.4f} ebits")  # 1.0

# Coherencia ℓ₁ del qubit 0 antes del CNOT
qc_solo_h = QuantumCircuit(1)
qc_solo_h.h(0)
sv_h = Statevector.from_instruction(qc_solo_h)
rho_h = sv_h.to_density_matrix().data
coh_l1 = sum(abs(rho_h[i, j]) for i in range(2) for j in range(2) if i != j)
print(f"Coherencia ℓ₁ de |+>: {coh_l1:.4f}")  # 1.0
print("→ 1 ebit de coherencia se convirtió en 1 ebit de entrelazamiento")
```
