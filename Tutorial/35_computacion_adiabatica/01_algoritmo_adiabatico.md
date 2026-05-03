# Algoritmo Adiabático y AQC

**Módulo 35 · Artículo 1 · Nivel muy avanzado**

---

## El teorema adiabático

Si un sistema cuántico comienza en el estado base de H(0) y H(t) varía
**suficientemente despacio**, el sistema permanece en el estado base instantáneo:

$$
H(s) = (1-s)\,H_i + s\,H_f, \quad s = t/T \in [0,1]
$$

**Condición adiabática:** el tiempo total T debe satisfacer:

$$
T \gg \frac{\max_s \left|\langle E_1(s) | \dot{H}(s) | E_0(s) \rangle\right|}{\min_s \Delta(s)^2}
$$

donde $\Delta(s) = E_1(s) - E_0(s)$ es el **gap espectral** (diferencia entre los
dos eigenvalores más bajos).

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh

def hamiltonian_adiabatico(s: float, n: int = 4) -> np.ndarray:
    """
    H(s) = (1-s)·H_i + s·H_f para un sistema de n qubits.
    
    H_i = -Σ X_j (Hamiltoniano transverso: estado base = |+⟩^n)
    H_f = Hamiltoniano de problema (Ising en cadena: -Σ Z_j Z_{j+1})
    """
    d = 2**n
    H_i = np.zeros((d, d), dtype=complex)
    H_f = np.zeros((d, d), dtype=complex)

    # Matrices de Pauli
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    I = np.eye(2, dtype=complex)

    # H_i = -Σ_j X_j
    for j in range(n):
        op = [I]*n
        op[j] = X
        mat = op[0]
        for k in range(1, n):
            mat = np.kron(mat, op[k])
        H_i -= mat

    # H_f = -Σ_j Z_j Z_{j+1}  (cadena de Ising)
    for j in range(n - 1):
        op = [I]*n
        op[j] = Z; op[j+1] = Z
        mat = op[0]
        for k in range(1, n):
            mat = np.kron(mat, op[k])
        H_f -= mat

    return (1 - s) * H_i + s * H_f

# Calcular el gap espectral vs s
s_vals = np.linspace(0, 1, 50)
gaps = []
for s in s_vals:
    H = hamiltonian_adiabatico(s, n=4)
    eigenvals = eigh(H, eigvals_only=True)
    gaps.append(eigenvals[1] - eigenvals[0])

min_gap = min(gaps)
s_min_gap = s_vals[np.argmin(gaps)]
print(f'Gap mínimo: Δ_min = {min_gap:.4f}  en s = {s_min_gap:.3f}')
print(f'Gap en s=0: {gaps[0]:.4f}  (Hamiltoniano transverso)')
print(f'Gap en s=1: {gaps[-1]:.4f}  (Hamiltoniano de problema)')

fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(s_vals, gaps, 'b-', lw=2, label='Gap espectral Δ(s)')
ax.axvline(s_min_gap, color='r', ls='--', alpha=0.7,
           label=f'Δ_min = {min_gap:.3f} en s={s_min_gap:.2f}')
ax.set_xlabel('s = t/T (parámetro adiabático)')
ax.set_ylabel('Gap espectral Δ(s)')
ax.set_title(f'Gap espectral del Hamiltoniano adiabático (n=4 Ising)')
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()
```

---

## Simulación de la evolución adiabática

```python
from scipy.linalg import expm

def evolucion_adiabatica(n: int = 3, T: float = 10.0,
                          n_pasos: int = 100) -> dict:
    """
    Simula la evolución adiabática de H_i → H_f.
    
    Usa integración de Trotter: divide [0,T] en n_pasos.
    Devuelve la fidelidad del estado final con el estado base de H_f.
    """
    d = 2**n
    dt = T / n_pasos

    # Estado inicial: estado base de H_i = |+⟩^n
    psi = np.ones(d, dtype=complex) / np.sqrt(d)

    # Evolución adiabática paso a paso
    for k in range(n_pasos):
        s = (k + 0.5) / n_pasos  # punto medio
        H_s = hamiltonian_adiabatico(s, n)
        # Evolución: e^{-iH(s)dt}
        U = expm(-1j * H_s * dt)
        psi = U @ psi
        psi /= np.linalg.norm(psi)

    # Estado base de H_f
    H_f = hamiltonian_adiabatico(1.0, n)
    eigenvals, eigenvecs = eigh(H_f)
    gs = eigenvecs[:, 0]

    fidelidad = abs(np.dot(gs.conj(), psi))**2
    energia_final = np.real(psi.conj() @ H_f @ psi)
    E_gs = eigenvals[0]

    return {
        'T': T,
        'fidelidad': fidelidad,
        'energia_final': energia_final,
        'E_gs': E_gs,
        'n_pasos': n_pasos,
    }

# Comparar velocidad de barrido
print('Fidelidad vs tiempo total T (n=3 qubits, 200 pasos):')
print(f'{"T":>6} | {"Fidelidad":>10} | {"E_final":>10} | {"E_gs":>10}')
print('-' * 44)
for T in [0.1, 1.0, 5.0, 20.0, 50.0]:
    r = evolucion_adiabatica(n=3, T=T, n_pasos=200)
    print(f'{T:>6.1f} | {r["fidelidad"]:>10.4f} | {r["energia_final"]:>10.4f} | {r["E_gs"]:>10.4f}')
```

---

## AQC para QUBO: formulación

Un problema de **Optimización Combinatoria QUBO** se formula como:

$$
\min_{x \in \{0,1\}^n} x^T Q x
$$

que se mapea a un Hamiltoniano de Ising:

$$
H_f = \sum_{ij} J_{ij} Z_i Z_j + \sum_i h_i Z_i
$$

con la correspondencia $x_i = (1 - Z_i)/2$.

```python
def qubo_a_ising(Q: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Convierte matriz QUBO Q a coeficientes Ising J (interacciones) y h (campos).
    x_i ∈ {0,1} → s_i ∈ {-1,+1} via x_i = (1-s_i)/2.
    """
    n = Q.shape[0]
    J = np.zeros((n, n))
    h = np.zeros(n)

    for i in range(n):
        for j in range(i+1, n):
            J[i, j] = Q[i, j] / 4

        h[i] = -Q[i, i] / 2 - sum(Q[i, j] + Q[j, i] for j in range(n) if j != i) / 4

    return J, h

def hamiltonian_ising(J: np.ndarray, h: np.ndarray) -> np.ndarray:
    """Hamiltoniano de Ising para n qubits en espacio de Hilbert 2^n."""
    n = len(h)
    d = 2**n
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    I = np.eye(2, dtype=complex)

    def kron_op(op_list):
        mat = op_list[0]
        for k in range(1, len(op_list)):
            mat = np.kron(mat, op_list[k])
        return mat

    H = np.zeros((d, d), dtype=complex)

    # Campo local
    for i in range(n):
        ops = [I]*n; ops[i] = Z
        H += h[i] * kron_op(ops)

    # Interacciones
    for i in range(n):
        for j in range(i+1, n):
            if abs(J[i, j]) > 1e-10:
                ops = [I]*n; ops[i] = Z; ops[j] = Z
                H += J[i, j] * kron_op(ops)

    return H

# Ejemplo: MAX-CUT en grafo triangular
# Q_ij = 1 si hay arista (i,j) en MAX-CUT → QUBO = -Σ (x_i - x_j)^2
# Equivale a maximizar Σ (x_i XOR x_j)

n_vars = 4
edges = [(0,1), (1,2), (2,3), (0,3), (0,2)]  # grafo de 4 nodos
Q = np.zeros((n_vars, n_vars))
for (i, j) in edges:
    Q[i, i] -= 1; Q[j, j] -= 1; Q[i, j] += 2

J, h = qubo_a_ising(Q)
H_f = hamiltonian_ising(J, h)
eigenvals, eigenvecs = eigh(H_f)

print(f'\nMAX-CUT en grafo de {n_vars} nodos ({len(edges)} aristas):')
print(f'Energía mínima Ising: {eigenvals[0]:.4f}')
print(f'Estado base (índice): {np.argmax(abs(eigenvecs[:, 0])**2)}')

# Decodificar solución
gs_idx = np.argmax(abs(eigenvecs[:, 0])**2)
bits = [(gs_idx >> k) & 1 for k in range(n_vars)]
corte = sum(1 for (i,j) in edges if bits[i] != bits[j])
print(f'Solución: x = {bits}')
print(f'Corte MAX-CUT: {corte} aristas (de {len(edges)} posibles)')
```

---

## AQC vs Gate-based: comparativa honesta

```python
comparativa = {
    'Modelo': ['AQC', 'Gate-based', 'QAOA (híbrido)'],
    'Tipo': ['Analógico', 'Digital', 'Digital'],
    'Ventaja_teorica': [
        'Polinomialmente equivalente a gate-based (Aharonov 2007)',
        'Universal, ampliamente probado',
        'Heurístico, sin garantía de óptimo',
    ],
    'Cuando_funciona': [
        'Cuando el gap permanece grande durante la evolución',
        'Siempre (con suficientes qubits y tiempo)',
        'Problemas con buena estructura local',
    ],
    'Limitacion_principal': [
        'Gap puede cerrarse exponencialmente (NP-duro ≈ gap pequeño)',
        'Requiere puertas coherentes, más susceptible al ruido',
        'P capas → mismo que AQC en el límite p→∞ (Farhi 2014)',
    ],
    'Hardware': [
        'D-Wave (superconductores flux), Pasqal (Rydberg)',
        'IBM, Google, IonQ, Quantinuum',
        'IBM, Google, cualquier gate-based',
    ],
}

print('\n=== AQC vs Gate-based vs QAOA ===\n')
for i in range(3):
    print(f'[{comparativa["Modelo"][i]}]')
    print(f'  Tipo: {comparativa["Tipo"][i]}')
    print(f'  Ventaja: {comparativa["Ventaja_teorica"][i]}')
    print(f'  Cuándo funciona: {comparativa["Cuando_funciona"][i]}')
    print(f'  Limitación: {comparativa["Limitacion_principal"][i]}')
    print(f'  Hardware: {comparativa["Hardware"][i]}')
    print()
```

---

## Quantum Approximate Optimization: límite p→∞

QAOA con p→∞ capas es equivalente a AQC. Para p finito, la fidelidad aumenta
pero el circuito se vuelve más profundo:

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def qaoa_maxcut_layer(qc: QuantumCircuit, gamma: float,
                       edges: list, n: int) -> None:
    """Aplica una capa QAOA para MAX-CUT."""
    # Capa de problema (phase separation)
    for (i, j) in edges:
        qc.cx(i, j)
        qc.rz(2 * gamma, j)
        qc.cx(i, j)
    # Capa de mezcla (mixing operator)
    qc.rx(2 * 0.5, range(n))  # β=0.5 fijo para simplificar

def energia_qaoa(n: int, edges: list, p: int, gammas: list) -> float:
    """Evalúa la energía QAOA para p capas."""
    qc = QuantumCircuit(n)
    qc.h(range(n))
    for layer in range(p):
        qaoa_maxcut_layer(qc, gammas[layer], edges, n)
    sv = Statevector(qc)
    probs = np.abs(sv.data)**2

    def cut_val(bs):
        bits = [(bs >> k) & 1 for k in range(n)]
        return sum(bits[i] != bits[j] for (i,j) in edges)

    return sum(probs[bs] * cut_val(bs) for bs in range(2**n))

n = 4
edges_g = [(0,1),(1,2),(2,3),(0,3),(0,2)]
max_cut = max(sum((bs>>i&1)!=(bs>>j&1) for i,j in edges_g) for bs in range(2**n))

print(f'MAX-CUT grafo: {max_cut} aristas óptimas')
print(f'{"p capas":>8} | {"E_QAOA":>8} | {"Aprox. ratio":>12}')
print('-' * 35)
for p in [1, 2, 3, 5]:
    # Parámetros heurísticos: gamma = pi/(2*(p+1)) para cada capa
    gammas = [np.pi / (2*(p+1))] * p
    E = energia_qaoa(n, edges_g, p, gammas)
    ratio = E / max_cut
    print(f'{p:>8} | {E:>8.3f} | {ratio:>12.4f}')
print(f'{"∞ (óptimo)":>8} | {max_cut:>8.1f} | {"1.0000":>12}')
```

---

**Referencias:**
- Farhi et al., *quant-ph/0001106* (2000) — AQC propuesto
- Aharonov et al., *SIAM J. Comp.* 37, 166 (2007) — AQC = gate-based
- Albash & Lidar, *Rev. Mod. Phys.* 90, 015002 (2018) — revisión AQC
- Farhi et al., *arXiv:1411.4028* (2014) — QAOA original
