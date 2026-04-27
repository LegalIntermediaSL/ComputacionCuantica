# Solución R7 — Fault Tolerance: Umbral del Código de Repetición

**Problema:** [Ejercicios de investigación R7](../../Ejercicios/ejercicios_investigacion.md#problema-r7)

---

## Parte a) — Umbral del código de repetición clásico vs cuántico

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import comb

# ─── Código de repetición de distancia d ─────────────────────────────────────

def p_logical_repetition(p_phys: float, d: int) -> float:
    """
    Tasa de error lógico del código de repetición de distancia d.
    Falla si más de d//2 qubits físicos fallan.
    P_L = Σ_{k=⌊d/2⌋+1}^{d} C(d,k) p^k (1-p)^{d-k}
    """
    t = d // 2  # capacidad de corrección
    p_fail = 0.0
    for k in range(t + 1, d + 1):
        p_fail += comb(d, k, exact=True) * p_phys**k * (1 - p_phys)**(d - k)
    return p_fail


def p_logical_surface(p_phys: float, d: int, A: float = 0.1) -> float:
    """
    Aproximación del error lógico del surface code de distancia d:
    P_L ≈ A · (p/p_th)^⌈d/2⌉ con umbral p_th ≈ 1%
    """
    p_th = 0.01
    return A * (p_phys / p_th) ** ((d + 1) // 2)


# Gráfica: P_L vs p_phys para distintas distancias
p_vals = np.logspace(-3, -0.5, 200)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

for d in [3, 5, 7, 9, 11]:
    p_L = [p_logical_repetition(p, d) for p in p_vals]
    axes[0].loglog(p_vals, p_L, lw=2, label=f'd={d}')

axes[0].loglog(p_vals, p_vals, 'k--', lw=1.5, label='Sin corrección (d=1)')
axes[0].axvline(0.5, color='r', ls=':', lw=1, label='Umbral clásico (p=0.5)')
axes[0].set_xlabel('p_phys'); axes[0].set_ylabel('P_L (error lógico)')
axes[0].set_title('Código de repetición: P_L vs p_phys')
axes[0].legend(fontsize=9); axes[0].grid(alpha=0.3, which='both')

for d in [3, 5, 7, 9]:
    p_L_surf = [p_logical_surface(p, d) for p in p_vals]
    axes[1].semilogy(p_vals * 100, p_L_surf, lw=2, label=f'd={d}')

axes[1].semilogy(p_vals * 100, p_vals, 'k--', lw=1.5, label='Sin corrección')
axes[1].axvline(1.0, color='r', ls='--', lw=2, label='Umbral surface code (1%)')
axes[1].set_xlabel('p_phys (%)'); axes[1].set_ylabel('P_L')
axes[1].set_title('Surface code: P_L vs p_phys'); axes[1].legend(fontsize=9)
axes[1].grid(alpha=0.3, which='both')

plt.tight_layout(); plt.show()

# Umbral numérico para repetición
print('=== Umbral del código de repetición ===')
p_th_rep = 0.5  # Para el código de repetición con canal de bit-flip
print(f'Umbral teórico (repetición): p_th = 0.5 (50%)')
print(f'Umbral teórico (surface code): p_th ≈ 1%')
print(f'Umbral teórico (steane [[7,1,3]]): p_th ≈ 1%')
```

---

## Parte b) — Overhead de qubits físicos

```python
def qubits_fisicos(n_logicos: int, d: int, code: str = 'surface') -> int:
    """Qubits físicos necesarios para n_logicos qubits lógicos con distancia d."""
    if code == 'surface':
        return n_logicos * d**2  # surface code: d² físicos por lógico
    elif code == 'repeticion':
        return n_logicos * d    # código de repetición: d físicos por lógico
    elif code == 'steane':
        return n_logicos * 7    # [[7,1,3]]: siempre 7 por lógico
    else:
        return n_logicos * d**2

# Tabla de overhead
print(f'\n=== Overhead de qubits físicos ===')
print(f'{"Código":>15} | {"d":>4} | {"n_lóg=1":>10} | {"n_lóg=10":>12} | {"n_lóg=1000":>14}')
print('-' * 65)
for code, label in [('surface','Surface'), ('repeticion','Repetición'), ('steane','Steane [[7,1,3]]')]:
    for d in ([3, 5, 7, 9] if code != 'steane' else [3]):
        n1   = qubits_fisicos(1, d, code)
        n10  = qubits_fisicos(10, d, code)
        n1k  = qubits_fisicos(1000, d, code)
        print(f'{label+" d="+str(d):>15} | {d:>4} | {n1:>10} | {n10:>12} | {n1k:>14}')

# Para Shor's algorithm: necesita ~3000 qubits lógicos y p_L < 10^{-15}
print('\n=== Factorizar RSA-2048 con Shor ===')
n_log_shor = 4098  # aproximado (Gidney & Ekera 2021)
p_target = 1e-3 / n_log_shor  # error total < 0.1%
d_needed = int(np.ceil(np.log(p_target / 0.1) / np.log(0.01)))  # aproximado
print(f'Qubits lógicos necesarios: ~{n_log_shor}')
print(f'P_L objetivo por qubit: {p_target:.2e}')
for d in range(3, 30, 2):
    p_L = p_logical_surface(0.001, d)
    if p_L < p_target:
        n_phys = qubits_fisicos(n_log_shor, d, 'surface')
        print(f'Distancia necesaria: d={d} → {n_phys:,} qubits físicos (p_phys=0.1%)')
        break
```

---

## Parte c) — Magic state distillation

```python
def magic_state_distillation_overhead(p_in: float, p_target: float) -> dict:
    """
    Overhead del protocolo 15-to-1 de destilación de estados mágicos.
    Input: 15 estados T con fidelidad p_in → 1 estado T con fidelidad p_target.
    """
    # Una ronda: p_out ≈ 35 * p_in^3  (para p_in << 1)
    rounds = 0
    p_current = p_in
    overhead = 1
    while p_current > p_target:
        p_current = 35 * p_current**3
        overhead *= 15
        rounds += 1
        if rounds > 10:
            break
    return {'rounds': rounds, 'overhead_Tstates': overhead, 'p_final': p_current}

print('\n=== Magic State Distillation 15-to-1 ===')
print(f'{"p_in":>8} | {"p_target":>10} | {"rondas":>8} | {"overhead":>10} | {"p_final":>12}')
print('-' * 60)
for p_in in [0.01, 0.001, 0.0001]:
    for p_target in [1e-6, 1e-9, 1e-12]:
        res = magic_state_distillation_overhead(p_in, p_target)
        print(f'{p_in:>8.4f} | {p_target:>10.2e} | {res["rounds"]:>8} | '
              f'{res["overhead_Tstates"]:>10} | {res["p_final"]:>12.2e}')
```

**Conclusión:** el umbral del código de repetición (bit-flip) es $p_{th}=0.5$, pero el cuántico (surface code) requiere $p_{th}\approx 1\%$ por la necesidad de corregir errores en X y Z simultáneamente. El overhead de qubits físicos crece como $d^2$ para el surface code.

---

## Referencia
Fowler et al., *Surface codes: Towards practical large-scale quantum computation*, PRA 86, 032324 (2012);  
Gidney & Ekera, *How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits*, **Quantum** 5, 433 (2021);  
Bravyi & Kitaev, *Universal quantum computation with ideal Clifford gates and noisy ancillas*, PRA 71, 022316 (2005).
