# Solución R4 — Error Mitigation: ZNE vs PEC

**Problema:** [Ejercicios de investigación R4](../../Ejercicios/ejercicios_investigacion.md#problema-r4)

---

## Parte a) — Implementación ZNE con Richardson extrapolation

```python
import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit.quantum_info import SparsePauliOp, Statevector

# ----- Circuito de prueba: Bell state -----
qc = QuantumCircuit(2)
qc.h(0); qc.cx(0, 1)
H_obs = SparsePauliOp.from_list([('ZZ', 1.0)])

E_ideal = Statevector(qc).expectation_value(H_obs).real  # = 1.0

# ----- Folding -----
def fold_circuit(qc: QuantumCircuit, scale_factor: int) -> QuantumCircuit:
    """
    Amplificación de ruido por circuit folding: U → U(U†U)^((λ-1)/2)
    scale_factor: entero impar ≥ 1
    """
    assert scale_factor >= 1 and scale_factor % 2 == 1
    qc_f = qc.copy()
    n_extra = (scale_factor - 1) // 2
    qc_inv = qc.inverse()
    for _ in range(n_extra):
        qc_f.compose(qc_inv, inplace=True)
        qc_f.compose(qc, inplace=True)
    return qc_f

# ----- Simulación ruidosa -----
def E_ruidoso(qc: QuantumCircuit, p_err: float, shots: int = 8192) -> float:
    nm = NoiseModel()
    nm.add_all_qubit_quantum_error(depolarizing_error(p_err, 1), ['h', 'rx', 'ry', 'rz'])
    nm.add_all_qubit_quantum_error(depolarizing_error(p_err * 5, 2), ['cx'])
    sim = AerSimulator(noise_model=nm)

    qc_meas = qc.copy(); qc_meas.measure_all()
    qc_t = transpile(qc_meas, sim, optimization_level=0)
    counts = sim.run(qc_t, shots=shots).result().get_counts()

    # Expectación ZZ: P(00) + P(11) - P(01) - P(10)
    total = sum(counts.values())
    E = sum(v * (1 if k.count('1') % 2 == 0 else -1) for k, v in counts.items()) / total
    return float(E)

# ----- Extrapolación de Richardson -----
def zne_richardson(lambdas: list, E_vals: list) -> float:
    """
    Extrapolación polinómica de Richardson a λ=0.
    Fórmula exacta para λ=1,3,5: extrapolación cuadrática.
    """
    from numpy.polynomial import polynomial as P
    coeffs = np.polyfit(lambdas, E_vals, len(lambdas) - 1)
    return float(np.polyval(coeffs, 0))  # evaluar en λ=0

# ----- Experimento -----
p_err = 0.01
lambdas = [1, 3, 5]

E_vals = [E_ruidoso(fold_circuit(qc, lam), p_err) for lam in lambdas]
E_zne = zne_richardson(lambdas, E_vals)

print(f'E_ideal:          {E_ideal:.4f}')
print(f'E_ruidoso (λ=1):  {E_vals[0]:.4f}  (error = {abs(E_vals[0]-E_ideal):.4f})')
print(f'E_ruidoso (λ=3):  {E_vals[1]:.4f}')
print(f'E_ruidoso (λ=5):  {E_vals[2]:.4f}')
print(f'E_ZNE:            {E_zne:.4f}  (error = {abs(E_zne-E_ideal):.4f})')
print(f'Mejora ZNE:       {abs(E_vals[0]-E_ideal)/max(1e-10,abs(E_zne-E_ideal)):.1f}×')
```

---

## Parte b) — Mejora de fidelidad vs nivel de ruido

```python
p_vals = np.linspace(0.001, 0.05, 20)
errores_brutos = []
errores_zne = []
SHOTS = 4096

for p in p_vals:
    E_raw = E_ruidoso(qc, p, SHOTS)
    E_f3  = E_ruidoso(fold_circuit(qc, 3), p, SHOTS)
    E_f5  = E_ruidoso(fold_circuit(qc, 5), p, SHOTS)
    E_z   = zne_richardson([1, 3, 5], [E_raw, E_f3, E_f5])
    errores_brutos.append(abs(E_raw - E_ideal))
    errores_zne.append(abs(E_z - E_ideal))

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].semilogy(p_vals*100, errores_brutos, 'r-o', ms=5, lw=2, label='Sin mitigación')
axes[0].semilogy(p_vals*100, errores_zne,   'b-s', ms=5, lw=2, label='ZNE (Richardson λ=1,3,5)')
axes[0].set_xlabel('Error depolarizante p (%)'); axes[0].set_ylabel('|E - E_ideal|')
axes[0].set_title('ZNE: error mitigado vs sin mitigar'); axes[0].legend(); axes[0].grid(alpha=0.3, which='both')

mejora = [e_b/max(1e-10, e_z) for e_b, e_z in zip(errores_brutos, errores_zne)]
axes[1].plot(p_vals*100, mejora, 'g-o', ms=5, lw=2)
axes[1].axhline(1, color='k', ls='--', lw=0.8, label='Sin mejora')
axes[1].set_xlabel('Error depolarizante p (%)'); axes[1].set_ylabel('Factor de mejora')
axes[1].set_title('Factor de mejora ZNE'); axes[1].legend(); axes[1].grid(alpha=0.3)

plt.tight_layout(); plt.show()
print(f'\nMejora media: {np.mean(mejora):.1f}× | Mejor: {max(mejora):.1f}× a p={p_vals[np.argmax(mejora)]*100:.1f}%')
```

---

## Parte c) — Cuándo falla ZNE y ventajas de PEC

```python
analisis_pec = """
LIMITACIONES DE ZNE:
════════════════════

1. RUIDO NO PERTURBATIVO (p > 5%):
   El folding asume que E(λ) es polinómica en λ.
   Para p grande, el circuito plegado (λ=5) tiene 5× más ruido → 
   la extrapolación diverge en lugar de converger.
   Regla empírica: ZNE funciona bien para p < 3%.

2. PROFUNDIDAD ALTA:
   Para circuitos profundos, fold(qc, 5) puede tener error total > 50%.
   Los puntos de extrapolación caen en el régimen saturado (~0).

3. RUIDO NO MARKOVIANO:
   Circuit folding asume ruido sin memoria entre capas.
   En hardware real, el ruido correlacionado viola este supuesto.

4. OVERHEAD DE SHOTS:
   ZNE requiere λ conjuntos de mediciones → λ× más shots.
   Con λ=1,3,5: 3× más shots para la misma precisión estadística.

VENTAJAS DE PEC (Probabilistic Error Cancellation):
════════════════════════════════════════════════════

PEC es unbiased: cancela el ruido de forma exacta (en el límite de shots ∞).

  Idea: representar la operación ideal U como combinación lineal
  de operaciones ruidosas accesibles:
  U_ideal = Σ_i c_i · Ε_i  con c_i reales (posiblemente negativos)

  Overhead de muestreo: γ = (Σ_i |c_i|)² ≈ e^{2λ_max·p·n_gates}
  
  Para p=1%, 100 puertas: γ ≈ e^{2} ≈ 7.4× más shots.
  
Comparativa:
┌─────────────────┬───────────────────┬─────────────────────┐
│ Propiedad       │ ZNE               │ PEC                 │
├─────────────────┼───────────────────┼─────────────────────┤
│ Sesgo           │ Residual (bias)   │ Zero bias (exacto)  │
│ Overhead shots  │ × λ_max           │ × γ (exponencial)   │
│ Implementación  │ Simple (folding)  │ Compleja (tomografía│
│                 │                   │ del canal de error) │
│ Ruido no-Mark.  │ Falla             │ Funciona (con tomo) │
│ Mejor caso      │ p < 3%, L < 50   │ p < 1%, L < 20      │
└─────────────────┴───────────────────┴─────────────────────┘

CONCLUSIÓN:
  • ZNE: rápido, fácil, funciona bien para p < 3%.
  • PEC: más preciso pero costoso en shots; preferible para circuitos cortos
         donde la exactitud importa más que el overhead.
  • Combinación óptima: ZNE para reducir el error grueso; PEC para refinamiento.
"""
print(analisis_pec)
```

---

## Referencia
Temme et al., *PRL* 119, 180509 (2017); Endo et al., *PRX* 8, 031027 (2018);
van den Berg et al., *Nat. Phys.* 19, 1116 (2023).
