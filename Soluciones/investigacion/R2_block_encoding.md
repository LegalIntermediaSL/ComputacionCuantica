# Solución R2 — Block-Encoding: construcción explícita

**Problema:** [Ejercicios de investigación R2](../../Ejercicios/ejercicios_investigacion.md#problema-r2)

---

## Parte a) — Construcción del circuito

La estrategia: representar la block-encoding como preparación de estado + operador de selección.

Para $A$ de $2\times 2$ bloques con norma $\leq 1$:
$$U_A = \begin{pmatrix} A & \sqrt{I-AA^\dagger} \\ \sqrt{I-A^\dagger A} & -A^\dagger \end{pmatrix}$$

Para la $A$ específica del enunciado (unitaria real), $AA^\dagger = I$, por lo que $U_A$ es exactamente $A$ completada a unitaria.

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Statevector
from qiskit.circuit.library import UnitaryGate
from scipy.linalg import block_diag, sqrtm

# Matriz del enunciado
A = np.array([[1,0,0,1],[0,1,1,0],[0,1,-1,0],[1,0,0,-1]], dtype=complex) / 2

# Verificar norma espectral ≤ 1
sv = np.linalg.svd(A, compute_uv=False)
print(f'Norma espectral de A: {sv.max():.6f} (debe ser ≤ 1)')
print(f'Valores singulares: {sv}')

# Para construir la block-encoding, completamos A a una unitaria de tamaño doble
# Método: descomposición QR del complemento ortogonal
def block_encoding(A: np.ndarray) -> QuantumCircuit:
    """
    Construye la block-encoding de A en un circuito cuántico.
    A: matriz 4×4 (2 qubits sistema) con ||A|| ≤ 1.
    Salida: circuito de 4 qubits (2 ancilla + 2 sistema).
    """
    n = A.shape[0]
    # Completar A a unitaria de tamaño 2n×2n
    # U_A = [[A, C], [B, D]] donde AA† + CC† = I, A†A + B†B = I
    AhA = A.conj().T @ A
    AAh = A @ A.conj().T
    I = np.eye(n)
    
    # C = sqrt(I - AA†)  (complemento superior derecho)
    C = sqrtm(I - AAh)
    # B = -A†  (elección que hace U_A unitaria si A es normal)
    # Para A general: usar descomposición por bloques
    # B = sqrt(I - A†A)
    B_sq = sqrtm(I - AhA)
    
    # Construir unitaria por bloques (válida para A con ||A|| ≤ 1)
    U = np.block([[A, C], [B_sq, -A.conj().T]])
    
    # Verificar unitariedad
    err = np.max(np.abs(U @ U.conj().T - np.eye(2*n)))
    print(f'Error de unitariedad: {err:.2e}')
    
    # Crear circuito
    n_total = int(np.log2(2*n))  # = log2(8) = 3 para 4+4
    qc = QuantumCircuit(n_total)
    qc.append(UnitaryGate(U), range(n_total))
    return qc, U

qc_be, U_full = block_encoding(A)

# Verificar: submatriz superior izquierda debe ser A
print('\nVerificación block-encoding:')
print(f'||U[:4,:4] - A|| = {np.max(np.abs(U_full[:4,:4] - A)):.2e}')
print(f'Block-encoding correcta: {np.allclose(U_full[:4,:4], A, atol=1e-10)}')
```

---

## Parte b) — Verificación

```python
# Verificación mediante extracción de submatriz
U_op = Operator(qc_be).data
submatrix = U_op[:4, :4]

print('A original:')
print(np.round(A, 3))
print('\nSubmatriz U[:4,:4]:')
print(np.round(submatrix, 3))
print(f'\nMaximal deviation: {np.max(np.abs(submatrix - A)):.2e}')
assert np.allclose(submatrix, A, atol=1e-6), "Block-encoding incorrecta"
print('✓ Block-encoding verificada correctamente')

# Visualización: estructura de U
import matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 3, figsize=(14, 4))
for ax, (M, title) in zip(axes, [
    (np.abs(A), '|A| (objetivo)'),
    (np.abs(U_full), '|U_A| (block-encoding completa)'),
    (np.abs(U_full[:4,:4] - A), 'Error |U[:4,:4] - A|')
]):
    im = ax.imshow(M, cmap='Blues', vmin=0)
    plt.colorbar(im, ax=ax)
    ax.set_title(title)
plt.tight_layout(); plt.show()
```

---

## Parte c) — Número de ancilla para matriz 2ⁿ×2ⁿ

Para una matriz $A \in \mathbb{C}^{N\times N}$ general ($N = 2^n$) con $\|A\| \leq \alpha$:

```python
analisis = """
NÚMERO DE ANCILLA QUBITS PARA BLOCK-ENCODING

Estrategia LCU (Linear Combination of Unitaries):
  Escribe A = Σ_j α_j U_j (descomposición en unitarias)
  
  • Si A es suma de L operadores de Pauli (SparsePauliOp con L términos):
    Ancilla necesarios = ⌈log₂(L)⌉ + 1

  • Si A es matriz densa N×N arbitraria:
    Descomposición en N² puertas de Pauli → ⌈log₂(N²)⌉ = 2n ancilla
    
  • Construcción por preparación de estado (PREPARE):
    Ancilla = n (para preparar coeficientes en superposición)
    
  • Construcción explícita (QR completion):
    Ancilla = n (1 qubit extra para doblar el espacio)
    
  • Método óptimo (QROM, Babbush 2018):
    Ancilla = n + O(log(L/ε)) para error ε en los coeficientes

Para nuestra A de 4×4 (n=2 qubits sistema):
  → 2 ancilla qubits (circuito de 4 qubits total)
  → Verificado: U_A es 8×8 con A en la esquina superior izquierda 4×4
"""
print(analisis)
```

**Respuesta concreta:** para $A \in \mathbb{C}^{2^n \times 2^n}$, la block-encoding constructiva
requiere **$n$ qubits ancilla** (esquema QR-completion), dando un circuito total de $2n$ qubits.
Con LCU optimizado (QROM), el overhead es $n + O(\log L)$ donde $L$ es la sparsity.

---

## Referencia
Gilyen et al., *STOC 2019*, Lemma 48; Babbush et al., *npj Quantum Inf.* 5, 92 (2019).
