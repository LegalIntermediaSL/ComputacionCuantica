# Solución R5 — Quantum Sensing: QFI y Límite de Heisenberg

**Problema:** [Ejercicios de investigación R5](../../Ejercicios/ejercicios_investigacion.md#problema-r5)

---

## Parte a) — QFI para distintos estados de prueba

```python
import numpy as np
import matplotlib.pyplot as plt
from qiskit.quantum_info import SparsePauliOp

def qfi_puro(psi: np.ndarray, H: np.ndarray) -> float:
    """QFI = 4(⟨H²⟩ - ⟨H⟩²) para estado puro."""
    exp_H  = (psi.conj() @ H @ psi).real
    exp_H2 = (psi.conj() @ (H @ H) @ psi).real
    return 4 * (exp_H2 - exp_H**2)

def generador_Jz(n: int) -> np.ndarray:
    """Generador colectivo Jz = Σ Zi/2 en espacio de 2^n dimensiones."""
    terms = [('I'*i + 'Z' + 'I'*(n-i-1), 0.5) for i in range(n)]
    return SparsePauliOp.from_list(terms).to_matrix().real

# ─── Estados de prueba ───────────────────────────────────────────────────────
results = {}

for n in [2, 4, 6, 8]:
    H = generador_Jz(n)
    
    # 1. Estado GHZ: (|0...0⟩ + |1...1⟩)/√2  → QFI = n² (Heisenberg)
    psi_ghz = np.zeros(2**n, dtype=complex)
    psi_ghz[0] = psi_ghz[-1] = 1/np.sqrt(2)
    
    # 2. Estado producto |+⟩^⊗n               → QFI = n (SQL estándar)
    plus = np.array([1, 1]) / np.sqrt(2)
    psi_prod = plus
    for _ in range(n-1):
        psi_prod = np.kron(psi_prod, plus)
    
    # 3. Estado |↑↑...↑⟩ (separable polarizado) → QFI = 0
    psi_pol = np.zeros(2**n, dtype=complex)
    psi_pol[0] = 1.0
    
    qfi_ghz  = qfi_puro(psi_ghz, H)
    qfi_prod = qfi_puro(psi_prod, H)
    qfi_pol  = qfi_puro(psi_pol, H)
    
    results[n] = (qfi_ghz, qfi_prod, qfi_pol)
    print(f'n={n}: QFI_GHZ={qfi_ghz:.1f} (teór={n**2}), '
          f'QFI_prod={qfi_prod:.4f} (teór={n:.1f}), '
          f'QFI_pol={qfi_pol:.4f} (teór=0)')

# Gráfica: QFI vs n
n_vals = list(results.keys())
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].plot(n_vals, [results[n][0] for n in n_vals], 'b-o', ms=8, lw=2, label='GHZ (entrelazado)')
axes[0].plot(n_vals, [results[n][1] for n in n_vals], 'g-s', ms=8, lw=2, label='Producto |+⟩^n (SQL)')
axes[0].plot(n_vals, [n**2 for n in n_vals], 'b--', lw=1, alpha=0.5, label='n² (Heisenberg)')
axes[0].plot(n_vals, n_vals, 'g--', lw=1, alpha=0.5, label='n (SQL)')
axes[0].set_xlabel('Número de qubits n'); axes[0].set_ylabel('QFI')
axes[0].set_title('QFI: Heisenberg vs SQL'); axes[0].legend(); axes[0].grid(alpha=0.3)

axes[1].semilogy(n_vals, [results[n][0] for n in n_vals], 'b-o', ms=8, lw=2, label='GHZ ∝ n²')
axes[1].semilogy(n_vals, [results[n][1] for n in n_vals], 'g-s', ms=8, lw=2, label='Producto ∝ n')
axes[1].set_xlabel('n'); axes[1].set_ylabel('QFI (log)')
axes[1].set_title('Escalado QFI (log)'); axes[1].legend(); axes[1].grid(alpha=0.3, which='both')

plt.tight_layout(); plt.show()
```

**Resultado clave:** $F_Q[\text{GHZ}] = n^2$ (límite de Heisenberg), $F_Q[|+\rangle^{\otimes n}] = n$ (SQL).

---

## Parte b) — Interferómetro de Ramsey y estimación de fase

```python
def ramsey_interferometer(phi: float, t: float, n: int = 1, state: str = 'product') -> float:
    """
    Probabilidad P(|0...0⟩) tras interferómetro de Ramsey:
    H^n → Rz(phi·t)^n → H^n (o GHZ version)
    """
    if state == 'product':
        # P(|0...0⟩) = cos^(2n)(phi·t/2) para estado producto
        return np.cos(phi * t / 2) ** (2 * n)
    else:  # GHZ
        # Señal de franja con franja n veces más fina
        return (np.cos(n * phi * t / 2)**2)

# Señal de Ramsey para n=1,2,4 fotones/qubits
phi_true = 0.5  # frecuencia a estimar
t = np.linspace(0, 4*np.pi, 500)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

for n, color in zip([1, 2, 4], ['blue', 'green', 'red']):
    P_prod = ramsey_interferometer(phi_true, t, n, 'product')
    P_ghz  = ramsey_interferometer(phi_true, t, n, 'GHZ')
    axes[0].plot(t, P_prod, lw=1.5, color=color, label=f'n={n} (producto)')
    axes[1].plot(t, P_ghz,  lw=1.5, color=color, ls='--', label=f'n={n} (GHZ)')

axes[0].set_title('Ramsey: estados producto'); axes[0].set_xlabel('t'); axes[0].set_ylabel('P(|0...0⟩)')
axes[0].legend(); axes[0].grid(alpha=0.3)
axes[1].set_title('Ramsey: estados GHZ (super-resolución n×)'); axes[1].set_xlabel('t')
axes[1].legend(); axes[1].grid(alpha=0.3)
plt.tight_layout(); plt.show()

# Cramér-Rao: σ(φ) ≥ 1/√(N·F_Q)
N_shots = 1000
print('\n=== Cota Cramér-Rao (N=1000 mediciones) ===')
print(f'{"Estado":>12} | {"n":>4} | {"F_Q":>8} | {"σ_CR(φ)":>12}')
print('-' * 45)
for n in [1, 2, 4, 8, 16]:
    H_mat = generador_Jz(n) if n <= 6 else None
    fq_ghz = float(n**2)
    fq_sql  = float(n)
    print(f'{"GHZ":>12} | {n:>4} | {fq_ghz:>8.1f} | {1/np.sqrt(N_shots*fq_ghz):>12.6f}')
    print(f'{"Producto":>12} | {n:>4} | {fq_sql:>8.1f} | {1/np.sqrt(N_shots*fq_sql):>12.6f}')
print(f'\nVentaja Heisenberg vs SQL a n=16: {np.sqrt(16):.2f}×')
```

---

## Parte c) — Efecto del ruido en la QFI

```python
def qfi_dephasing(n: int, gamma_t: float, state: str = 'GHZ') -> float:
    """
    QFI bajo canal de dephasing (γ·t = tasa de decoherencia).
    Para GHZ: F_Q = n² · exp(-2n·γ·t)
    Para producto: F_Q = n · exp(-2·γ·t)
    """
    if state == 'GHZ':
        return n**2 * np.exp(-2 * n * gamma_t)
    else:
        return n * np.exp(-2 * gamma_t)

gamma_t_vals = np.linspace(0, 1.0, 100)
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

for n in [2, 4, 8]:
    fq_ghz  = [qfi_dephasing(n, gt, 'GHZ') for gt in gamma_t_vals]
    fq_prod = [qfi_dephasing(n, gt, 'product') for gt in gamma_t_vals]
    axes[0].plot(gamma_t_vals, fq_ghz,  lw=2, label=f'GHZ n={n}')
    axes[0].plot(gamma_t_vals, fq_prod, lw=1.5, ls='--', label=f'Prod n={n}')

axes[0].set_xlabel('γ·t (decoherencia)'); axes[0].set_ylabel('F_Q')
axes[0].set_title('QFI vs dephasing'); axes[0].legend(fontsize=8); axes[0].grid(alpha=0.3)

# Cruce: GHZ supera SQL solo para γ·t < ln(n)/(n-1)
n_arr = np.arange(2, 20)
gamma_cruce = np.log(n_arr) / (n_arr - 1)
axes[1].plot(n_arr, gamma_cruce, 'r-o', ms=6, lw=2)
axes[1].set_xlabel('n qubits'); axes[1].set_ylabel('γ·t máximo para ventaja GHZ')
axes[1].set_title('GHZ supera SQL solo para γt < ln(n)/(n-1)'); axes[1].grid(alpha=0.3)

plt.tight_layout(); plt.show()

print('\nConclusion: para n grande, GHZ requiere γt → 0 para mantener ventaja.')
print('Optimo ruidoso: n_opt ≈ 1/(2γt) qubits entrelazados.')
```

**Conclusión:** el límite de Heisenberg ($F_Q = n^2$) solo es alcanzable con ruido muy pequeño. Para $\gamma t > \ln(n)/(n-1)$, el estado producto supera al GHZ en presencia de dephasing.

---

## Referencia
Giovannetti et al., *Quantum limits to dynamical evolution*, PRA 67, 052109 (2003); Escher et al., *General framework for estimating the ultimate precision limit in noisy quantum-enhanced metrology*, **Nature Physics** 7, 406 (2011); Tóth & Apellaniz, *Multipartite entanglement and high-precision metrology*, J. Phys. A 47, 424006 (2014).
