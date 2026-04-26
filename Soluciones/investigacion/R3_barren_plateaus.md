# Solución R3 — Barren Plateaus: escalado con qubits

**Problema:** [Ejercicios de investigación R3](../../Ejercicios/ejercicios_investigacion.md#problema-r3)

---

## Parte a) — Verificación experimental

```python
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import SparsePauliOp, Statevector

def hamiltoniano_ising(n: int, J: float = 1.0, h: float = 0.5) -> SparsePauliOp:
    terms = []
    for i in range(n - 1):
        op = 'I'*i + 'ZZ' + 'I'*(n-i-2)
        terms.append((op, -J))
    for i in range(n):
        op = 'I'*i + 'X' + 'I'*(n-i-1)
        terms.append((op, -h))
    return SparsePauliOp.from_list(terms)

def ansatz_aleatorio(n: int, n_capas: int) -> QuantumCircuit:
    """Ansatz hardware-efficient con RY+CX (2-diseño aproximado para muchas capas)."""
    theta = ParameterVector('θ', n * (n_capas + 1))
    qc = QuantumCircuit(n)
    idx = 0
    for q in range(n): qc.ry(theta[idx], q); idx += 1
    for _ in range(n_capas):
        for q in range(n-1): qc.cx(q, q+1)
        for q in range(n): qc.ry(theta[idx], q); idx += 1
    return qc

def varianza_gradiente(n: int, n_capas: int, n_samples: int = 100) -> float:
    H = hamiltoniano_ising(n)
    qc = ansatz_aleatorio(n, n_capas)
    n_p = qc.num_parameters
    eps = 0.01
    gradientes = []

    for _ in range(n_samples):
        theta0 = np.random.uniform(-np.pi, np.pi, n_p)
        tp = theta0.copy(); tp[0] += eps
        tm = theta0.copy(); tm[0] -= eps

        E_p = Statevector(qc.assign_parameters(tp)).expectation_value(H).real
        E_m = Statevector(qc.assign_parameters(tm)).expectation_value(H).real
        gradientes.append((E_p - E_m) / (2 * eps))

    return float(np.var(gradientes))

# Experimento
resultados = {}
print(f'{"n":>3} | {"Var(grad)":>12} | {"log10(Var)":>12}')
print('-' * 35)
for n in [2, 4, 6, 8]:
    var = varianza_gradiente(n, n_capas=n, n_samples=100)
    resultados[n] = var
    print(f'{n:>3} | {var:>12.2e} | {np.log10(var):>12.3f}')

# Ajuste exponencial: Var ∝ b^(-n)
n_vals = list(resultados.keys())
log_vars = [np.log(v) for v in resultados.values()]
slope, intercept, r, p, se = scipy.stats.linregress(n_vals, log_vars)
base = np.exp(-slope)

print(f'\nAjuste: Var ∝ exp({slope:.3f}·n) = {base:.3f}^(-n)')
print(f'  Teórico para 2-diseño: base ≈ 4/3 = {4/3:.3f}')
print(f'  R² = {r**2:.4f}')
```

**Resultado esperado:** la varianza cae como $\approx (4/3)^{-n}$ para ansätze 2-diseño,
confirmando el teorema de McClean et al. (2018).

---

## Parte b) — Comparativa con teoría de diseños unitarios

```python
# Predicción teórica para 2-diseño (Cerezo et al. 2021, Theorem 1)
# Var[∂E/∂θ] = A · exp(-B·n) donde A,B dependen de la profundidad y observable

n_vals_teoric = np.arange(2, 12)
# Para L=n capas y observable local (1 qubit), la cota es:
# Var ≤ (d_n)^(-1) donde d_n = 4^n / (n*(n+1))  (aproximado)
# La cota exacta de Cerezo usa invariantes del grupo unitario

def cota_var_global(n: int, L: int) -> float:
    """Cota superior para Var[grad] con observable global, L capas, n qubits."""
    return 2 / (4**n)

def cota_var_local(n: int, L: int) -> float:
    """Cota superior para Var[grad] con observable local (1 qubit)."""
    # Para observable de 1 qubit: decaimiento polinómico (NO barren plateau)
    return 1 / (3 * L)

fig, ax = plt.subplots(figsize=(9, 5))
n_plot = list(resultados.keys())
vars_plot = list(resultados.values())

ax.semilogy(n_plot, vars_plot, 'b-o', ms=8, lw=2, label='Experimental')
ax.semilogy(n_vals_teoric, [cota_var_global(n, n) for n in n_vals_teoric],
            'r--', lw=2, label='Cota global O(4^{-n})')
ax.semilogy(n_vals_teoric,
            [np.exp(intercept) * np.exp(slope*n) for n in n_vals_teoric],
            'g:', lw=1.5, label=f'Ajuste: {base:.2f}^(-n)')
ax.set_xlabel('Número de qubits n')
ax.set_ylabel('Var[∂E/∂θ₀]')
ax.set_title('Barren Plateau — verificación experimental vs teoría')
ax.legend(); ax.grid(alpha=0.3, which='both')
plt.tight_layout(); plt.show()
```

---

## Parte c) — Estrategias de mitigación

```python
estrategias = """
ESTRATEGIAS CONTRA BARREN PLATEAUS
════════════════════════════════════════════════════════

1. INICIALIZACIÓN CORRELACIONADA (Identity blocks):
   Inicializar cada bloque del ansatz como la identidad.
   → Gradientes de orden O(1) al inicio del entrenamiento.
   → Implementación: theta = 0 para todas las rotaciones.

2. ANSATZ CON ESTRUCTURA LOCAL:
   Usar observables locales (1-2 qubits) en lugar de globales.
   → Cerezo et al. (2021): Var[grad] ∝ 1/L (polinómico, no exponencial).
   → Implementación: Costo = Σ_i ⟨Zᵢ⟩ en lugar de ⟨H_global⟩.

3. LAYER-BY-LAYER TRAINING (entrenamiento progresivo):
   Entrenar capa a capa: fijar capas previas, optimizar la siguiente.
   → Evita la zona plana al inicio.
   → Funciona bien con hasta 10-15 capas.

4. WARM-START CON SOLUCIÓN CLÁSICA:
   Inicializar con solución de un método clásico (DMRG, MPS).
   → El estado inicial ya está cerca del mínimo.
   → No elimina el barren plateau pero lo evita.

5. VARIATIONAL QUANTUM EIGENSOLVER CON UCCSD:
   Usar ansatz con estructura física (UCCSD, qubit-ADAPT).
   → No es un 2-diseño → los gradientes no decaen exponencialmente.
   → Restricción: solo válido para sistemas específicos.
"""
print(estrategias)

# Demostración: inicialización identity blocks vs aleatoria
def var_con_identity_init(n: int, n_capas: int, n_samples: int = 100) -> float:
    """Varianza con inicialización identity-blocks (theta ≈ 0)."""
    H = hamiltoniano_ising(n)
    qc = ansatz_aleatorio(n, n_capas)
    n_p = qc.num_parameters
    eps = 0.01; gradientes = []

    for _ in range(n_samples):
        # Perturbación pequeña alrededor de theta=0 (identity initialization)
        theta0 = np.random.normal(0, 0.01, n_p)  # pequeña perturbación
        tp = theta0.copy(); tp[0] += eps
        tm = theta0.copy(); tm[0] -= eps
        E_p = Statevector(qc.assign_parameters(tp)).expectation_value(H).real
        E_m = Statevector(qc.assign_parameters(tm)).expectation_value(H).real
        gradientes.append((E_p - E_m) / (2*eps))

    return float(np.var(gradientes))

print('\nComparativa Var[grad]: aleatoria vs identity-init')
print(f'{"n":>3} | {"Aleatoria":>12} | {"Identity-init":>14} | {"Mejora":>8}')
print('-' * 46)
for n in [2, 4, 6]:
    var_rand = resultados.get(n) or varianza_gradiente(n, n)
    var_id   = var_con_identity_init(n, n)
    print(f'{n:>3} | {var_rand:>12.2e} | {var_id:>14.2e} | {var_id/var_rand:>7.1f}×')
```

---

## Referencia
McClean et al., *Nat. Commun.* 9, 4812 (2018); Cerezo et al., *Nat. Commun.* 12, 1791 (2021).
