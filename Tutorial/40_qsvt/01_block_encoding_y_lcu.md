# Block Encoding y Linear Combination of Unitaries

**Módulo 40 · Artículo 1 · Nivel muy avanzado**

---

## El problema: matrices no unitarias en circuitos cuánticos

Los circuitos cuánticos solo implementan operaciones unitarias. Sin embargo,
muchos algoritmos necesitan aplicar matrices arbitrarias (Hamiltonianos, solvers
lineales). La **block encoding** resuelve esto incrustando la matriz en la
esquina superior izquierda de una unitaria mayor:

$$
U_A = \begin{pmatrix} A/\alpha & \cdot \\ \cdot & \cdot \end{pmatrix}
$$

donde $\alpha \geq \|A\|$ es un factor de normalización. Aplicar $U_A$ al estado
$|0\rangle_a \otimes |\psi\rangle$ y proyectar el ancilla en $|0\rangle_a$
implementa $A|\psi\rangle/\alpha$ con amplitud $1/\alpha$.

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Statevector

def block_encoding_2x2(A: np.ndarray) -> np.ndarray:
    """
    Construye una block encoding unitaria para A de 2×2.
    
    La matrix A debe satisfacer ||A|| ≤ 1 (normalizada).
    La unitaria 4×4 tiene A en la esquina [0:2, 0:2].
    """
    assert A.shape == (2, 2), "A debe ser 2×2"
    norm_A = np.linalg.norm(A, ord=2)
    assert norm_A <= 1 + 1e-10, f"||A|| = {norm_A:.4f} > 1, normaliza primero"

    # Construir U tal que ⟨0|U|0⟩ = A
    # Método: completar a unitaria usando descomposición QR
    # Top-left block = A, completar con el complemento ortogonal
    n = A.shape[0]
    U = np.zeros((2*n, 2*n), dtype=complex)
    U[:n, :n] = A

    # Completar las filas/columnas para que U sea unitaria
    # Columnas restantes: kernel ortogonal de A†
    for i in range(n):
        col = np.zeros(2*n, dtype=complex)
        col[n + i] = 1.0
        # Gram-Schmidt contra columnas ya definidas
        for j in range(i):
            col -= (U[:, j].conj() @ col) * U[:, j]
        norm = np.linalg.norm(col)
        if norm > 1e-12:
            U[:, n + i] = col / norm

    # Completar filas con Gram-Schmidt en las filas inferior-izquierda
    # Simplificado: usar SVD para garantizar unitaridad
    Q, R = np.linalg.qr(np.vstack([A, np.random.randn(n, n) + 1j * np.random.randn(n, n)]))
    # Construir manualmente: el método más robusto es via isometría
    # Usar la construcción del "complemento de Schur"
    _, s, Vh = np.linalg.svd(A)
    # Proyector complementario
    P_orth = np.eye(n) - A @ np.linalg.pinv(A)
    Q_orth, _ = np.linalg.qr(P_orth + 1e-10 * np.eye(n))

    U_block = np.block([
        [A,          np.sqrt(np.eye(n) - A @ A.conj().T)],
        [np.sqrt(np.eye(n) - A.conj().T @ A), -A.conj().T]
    ])
    return U_block

# Ejemplo: block encoding de una matriz de Pauli escalada
sigma_x = np.array([[0, 1], [1, 0]], dtype=complex) * 0.5  # ||σ_x/2|| = 0.5
U_be = block_encoding_2x2(sigma_x)

print('Block encoding de σ_x/2:')
print(f'U (4×4):\n{np.round(U_be, 3)}')
print(f'\n||U†U - I|| = {np.linalg.norm(U_be.conj().T @ U_be - np.eye(4)):.6e}')
print(f'Esquina superior izq. U[0:2, 0:2] = \n{np.round(U_be[:2, :2], 3)}')
print(f'(Debe ser σ_x/2 = [[0, 0.5], [0.5, 0]])')
```

---

## Linear Combination of Unitaries (LCU)

LCU (Childs et al. 2012) expresa una matriz como combinación lineal de unitarias:

$$
A = \sum_k \alpha_k U_k
$$

El circuito LCU usa dos registros: **select** (elige $U_k$) y **system**:

```
Preparar: |0⟩ → Σ_k √(α_k/λ) |k⟩    (operador PREPARE)
Aplicar:  |k⟩|ψ⟩ → |k⟩ U_k|ψ⟩        (operador SELECT)
Proyectar: ancilla → |0⟩                (post-selección)
```

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector

def lcu_hamiltonian_simulation(H: SparsePauliOp, t: float,
                                 n_terms: int = None) -> QuantumCircuit:
    """
    Implementa exp(-iHt) mediante LCU truncado (para demostración pedagógica).
    
    En la práctica, se usa la expansión de Taylor: exp(-iHt) = Σ_k (-iHt)^k/k!
    Cada término es una LCU de productos Pauli.
    
    Aquí mostramos el circuito conceptual, no la implementación completa.
    """
    n = H.num_qubits
    coeffs = H.coeffs
    paulis = [p.to_label() for p in H.paulis]

    # Normalización: λ = Σ |α_k|
    lam = sum(abs(c) for c in coeffs)

    # Registro PREPARE: log2(n_paulis) qubits ancilla
    n_ancilla = int(np.ceil(np.log2(len(coeffs))))

    qc = QuantumCircuit(n + n_ancilla, name=f'LCU(H,t={t:.2f})')
    qc.h(range(n_ancilla))  # preparación uniforme (simplificada)

    # SELECT: aplicar U_k condicionado a |k⟩ en ancilla
    # (circuito completo requeriría multiplexores)
    qc.barrier()
    qc.h(range(n_ancilla))  # PREPARE†

    return qc

# Hamiltoniano H₂ y su descomposición LCU
H2 = SparsePauliOp.from_list([
    ('II', -1.0523732),
    ('IZ',  0.3979374),
    ('ZI', -0.3979374),
    ('ZZ', -0.0112801),
    ('XX',  0.1809312),
])

print('Hamiltoniano H₂ — Descomposición LCU:')
print(f'  Número de términos Pauli: {len(H2)}')
lam = sum(abs(c) for c in H2.coeffs)
print(f'  λ = Σ|α_k| = {lam:.4f}  (factor de normalización)')
print(f'  Qubits ancilla para PREPARE: {int(np.ceil(np.log2(len(H2))))}')
print(f'  Overhead de overhead: {lam:.2f}× (probabilidad de éxito 1/λ²)')

# Comparativa LCU vs Trotter
import matplotlib.pyplot as plt

epsilons = np.logspace(-3, 0, 50)  # precisión objetivo

# Trotter: r pasos ≈ t²||H||²/(2ε) → profundidad O(1/ε)
norm_H = max(abs(c) for c in H2.coeffs) * len(H2)
t_sim = 1.0
r_trotter = t_sim**2 * norm_H**2 / (2 * epsilons)

# LCU Taylor: r ≈ log(1/ε)/log(log(1/ε)) → profundidad O(log(1/ε))
r_lcu = np.log(1 / epsilons) / np.log(np.log(1 / epsilons) + 1)

fig, ax = plt.subplots(figsize=(8, 5))
ax.loglog(epsilons, r_trotter, 'r-', lw=2, label='Trotter (orden 1): O(1/ε)')
ax.loglog(epsilons, r_lcu * 10, 'b-', lw=2, label='LCU Taylor: O(log(1/ε))')
ax.set_xlabel('Precisión ε')
ax.set_ylabel('Profundidad de circuito (proporcional)')
ax.set_title('Complejidad de simulación hamiltoniana: Trotter vs LCU')
ax.legend()
ax.grid(alpha=0.3, which='both')
ax.invert_xaxis()
plt.tight_layout()
plt.show()
```

---

## Qubitización y walk operators

La **qubitización** (Low & Chuang 2016) convierte la block encoding de $H$
en un operador de walk $W$ cuyo espectro está relacionado con el de $H$:

$$
\text{Eigenvalores de } W = e^{\pm i \arccos(E_k/\alpha)}
$$

donde $E_k$ son los eigenvalores de $H$. Esto permite extraer eigenvalores
de $H$ mediante QPE aplicada a $W$ en lugar de a $e^{-iHt}$.

```python
import numpy as np

def analisis_qubitizacion(H: np.ndarray, alpha: float) -> dict:
    """
    Dado un Hamiltoniano H y su factor de normalización alpha,
    calcula los eigenvalores del operador de walk qubitizado W.
    
    Eigenvalores de W: exp(±i·arccos(E_k/alpha))
    """
    H_norm = H / alpha
    eigenvals_H = np.linalg.eigvalsh(H)

    # Eigenvalores del walk operator
    eigenvals_W_phases = np.arccos(eigenvals_H / alpha)

    return {
        'E_H': eigenvals_H,
        'alpha': alpha,
        'phases_W': eigenvals_W_phases,
        'E_H_norm': eigenvals_H / alpha,
    }

# Hamiltoniano de Ising 1D (4 sitios)
def ising_1d(n: int, J: float = 1.0, h: float = 0.5) -> np.ndarray:
    """Hamiltoniano de Ising transverso: H = -J Σ ZZ - h Σ X"""
    from functools import reduce
    dim = 2**n
    H = np.zeros((dim, dim))
    sigma_z = np.diag([1., -1.])
    sigma_x = np.array([[0., 1.], [1., 0.]])
    I2 = np.eye(2)

    for i in range(n - 1):
        ops = [I2] * n
        ops[i], ops[i+1] = sigma_z, sigma_z
        H -= J * reduce(np.kron, ops)

    for i in range(n):
        ops = [I2] * n
        ops[i] = sigma_x
        H -= h * reduce(np.kron, ops)

    return H

H_ising = ising_1d(4, J=1.0, h=0.5)
alpha_ising = np.linalg.norm(H_ising, ord=2) * 1.1  # alpha > ||H||

r = analisis_qubitizacion(H_ising, alpha_ising)

print('Qubitización del Hamiltoniano de Ising (4 sitios):')
print(f'alpha = {r["alpha"]:.4f}  (||H|| = {np.linalg.norm(H_ising, ord=2):.4f})')
print(f'\n{"E_k/alpha":>12} | {"Fase W (rad)":>14} | {"E_k (GHz)"}')
print('-' * 45)
for E, phi in zip(r['E_H'], r['phases_W']):
    print(f'{E/r["alpha"]:>12.4f} | {phi:>14.4f} | {E:>10.4f}')

print('\nVentaja: QPE sobre W requiere O(1/ε) queries a W')
print('vs QPE sobre e^(-iHt) que requiere t = O(1/ε) → mismo coste pero sin Trotter')
```

---

**Referencias:**
- Childs, Kothari, Somma, *SIAM J. Comput.* 46, 1920 (2017) — LCU
- Low & Chuang, *Quantum* 3, 163 (2019) — qubitización
- Gilyen, Su, Low, Wiebe, *STOC 2019* — QSVT
- Babbush et al., *npj Quantum Inf.* 5, 92 (2019) — block encoding en química
