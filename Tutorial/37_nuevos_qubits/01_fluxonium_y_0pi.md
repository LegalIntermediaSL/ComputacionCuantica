# Fluxonium y el Qubit 0-π

**Módulo 37 · Artículo 1 · Nivel muy avanzado**

---

## El problema del transmon: escasez de anarmonicidad

El transmon estándar sacrifica anarmonicidad por protección frente al ruido de
carga. Su espectro de energía:

$$E_n = \sqrt{8 E_J E_C} \left(n + \tfrac{1}{2}\right) - \frac{E_C}{12} + O(e^{-\sqrt{8E_J/E_C}})$$

Con $E_J / E_C \approx 50$, la anarmonicidad es solo $\alpha \approx -E_C \approx -200$ MHz.
Esto limita la velocidad de puerta ($T_{\text{gate}} \gtrsim 1/|\alpha|$) y complica
la selección de transiciones en espectroscopía.

```python
import numpy as np
import matplotlib.pyplot as plt

def espectro_transmon(Ej_Ec_ratio: float, n_niveles: int = 6) -> np.ndarray:
    """
    Calcula los niveles de energía del transmon en unidades de E_C.
    Usa la expansión perturbativa en el límite E_J/E_C >> 1.
    """
    r = Ej_Ec_ratio
    E_plasma = np.sqrt(8 * r)  # frecuencia de plasma en unidades E_C
    niveles = []
    for n in range(n_niveles):
        # Expansión Mathieu: E_n ≈ E_plasma*(n+½) - E_C*(6n²+6n+3)/12
        E_n = E_plasma * (n + 0.5) - (6 * n**2 + 6 * n + 3) / 12
        niveles.append(E_n)
    return np.array(niveles)

# Espectros para diferentes ratios
ratios = [10, 20, 50, 100]
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

for r in ratios:
    nivs = espectro_transmon(r)
    # Anarmonicidad: ω₂₁ - ω₁₀
    omega_10 = nivs[1] - nivs[0]
    omega_21 = nivs[2] - nivs[1]
    anarmon = omega_21 - omega_10
    print(f'E_J/E_C = {r:>4}: ω₁₀ = {omega_10:.3f} E_C, α = {anarmon:.3f} E_C')

# Graficar anarmonicidad vs ratio
x_ratios = np.logspace(0.5, 3, 200)
anarmoni = []
for r in x_ratios:
    nivs = espectro_transmon(r)
    anarmoni.append((nivs[2] - nivs[1]) - (nivs[1] - nivs[0]))

axes[0].semilogx(x_ratios, anarmoni, 'b-', lw=2)
axes[0].axhline(-1, color='gray', ls='--', alpha=0.5, label='α = -E_C (mín. transmon)')
axes[0].axvline(50, color='red', ls=':', alpha=0.7, label='E_J/E_C ≈ 50 (típico)')
axes[0].set_xlabel('E_J / E_C')
axes[0].set_ylabel('Anarmonicidad (unidades E_C)')
axes[0].set_title('Anarmonicidad del transmon')
axes[0].legend()
axes[0].grid(alpha=0.3)

# Ruido de carga vs ratio
sens_carga = np.exp(-np.sqrt(2 * x_ratios / np.pi))  # ∝ exp(-√(8E_J/E_C))
axes[1].loglog(x_ratios, sens_carga / sens_carga[0], 'r-', lw=2, label='Sensibilidad al ruido de carga')
axes[1].set_xlabel('E_J / E_C')
axes[1].set_ylabel('Sensibilidad relativa')
axes[1].set_title('Trade-off: anarmonicidad vs protección de carga')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## Fluxonium: el qubit de inducción grande

El fluxonium reemplaza la conexión DC del transmon por un array de N junctions
que actúa como inductancia lineal grande $E_L$. El Hamiltoniano es:

$$\hat{H}_{\text{flux}} = 4E_C \hat{n}^2 - E_J \cos(\hat{\varphi} - \varphi_{\text{ext}}) + \frac{E_L}{2} \hat{\varphi}^2$$

Con $E_L \ll E_J \ll E_C^{-1}$ (régimen heavy fluxonium), se obtiene:

- **Anarmonicidad** $|\alpha| > 1$ GHz (frente a ~200 MHz en transmon)
- **T₁ > 1 ms** (récord 2023: T₁ = 1.48 ms, MIT Lincoln Lab)
- **Protección dual**: frente a ruido de carga ($E_J/E_C \gg 1$) Y frente a ruido de flujo (a semiciclo $\varphi_{\text{ext}} = \pi/2$)

```python
import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt

def hamiltonian_fluxonium(Ec: float, Ej: float, El: float,
                           phi_ext: float, n_fock: int = 30) -> np.ndarray:
    """
    Hamiltoniano del fluxonium en la base de carga (truncado).
    
    Ec: energía de carga (GHz)
    Ej: energía Josephson (GHz)
    El: energía inductiva (GHz)
    phi_ext: flujo externo (en unidades de Φ₀/2π)
    n_fock: truncación de la base
    """
    dim = 2 * n_fock + 1
    n_vals = np.arange(-n_fock, n_fock + 1)

    # Término cinético: 4 E_C n²
    H_charge = np.diag(4 * Ec * n_vals**2)

    # Término inductivo: E_L/2 * φ² con φ → i∂/∂n en base de carga
    # φ_mn = i(n-m) * π/(N+1) — aproximación de diferencias finitas
    # Usamos la forma de oscilador armónico para El: E_L φ²/2
    # En la base de carga, φ = i(∂/∂n) se discretiza como:
    phi_phase = np.pi / (n_fock + 1)
    phi_matrix = np.zeros((dim, dim))
    for i in range(dim):
        for j in range(dim):
            if i != j:
                phi_matrix[i, j] = phi_phase * (1j / (n_vals[i] - n_vals[j]))
    # Simplificado: usar El/2 * (n_vals * delta_phi)²
    # La representación correcta usa la base de oscilador de plasmon
    delta_phi = np.sqrt(2 * Ec / El) if El > 0 else 0
    H_inductive = np.diag(El / 2 * (n_vals * delta_phi)**2)

    # Término Josephson: -E_J cos(φ - φ_ext)
    # En base de carga: cos(φ - φ_ext)|n⟩ ∝ (|n+1⟩ + |n-1⟩)/2 * e^(±i φ_ext)
    H_josephson = np.zeros((dim, dim), dtype=complex)
    for i in range(dim - 1):
        H_josephson[i, i+1] = -Ej / 2 * np.exp(1j * phi_ext)
        H_josephson[i+1, i] = -Ej / 2 * np.exp(-1j * phi_ext)

    return (H_charge + H_inductive + H_josephson).real

# Parámetros típicos de fluxonium (heavy)
Ec = 1.0   # GHz
Ej = 4.0   # GHz
El = 0.9   # GHz (energía inductiva pequeña → heavy fluxonium)

phi_ext_vals = np.linspace(0, 2 * np.pi, 100)
energias_vs_phi = []

for phi in phi_ext_vals:
    H = hamiltonian_fluxonium(Ec, Ej, El, phi, n_fock=20)
    eigvals = np.sort(np.linalg.eigvalsh(H))[:5]
    energias_vs_phi.append(eigvals - eigvals[0])

energias_vs_phi = np.array(energias_vs_phi)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Espectro vs flujo
for k in range(1, 4):
    axes[0].plot(phi_ext_vals / np.pi, energias_vs_phi[:, k],
                lw=2, label=f'|{k}⟩ - |0⟩')
axes[0].axvline(1.0, color='red', ls='--', alpha=0.7, label='Sweet spot (φ=π)')
axes[0].set_xlabel('Flujo externo (unidades π)')
axes[0].set_ylabel('Frecuencia (GHz)')
axes[0].set_title('Espectro fluxonium vs flujo externo')
axes[0].legend(fontsize=9)
axes[0].grid(alpha=0.3)

# Comparativa transmon vs fluxonium
sistemas = {
    'Transmon\n(E_J/E_C=50)': {'anarmon': -0.2, 'T1_ms': 0.1, 'color': 'blue'},
    'Fluxonium\n(heavy)': {'anarmon': -1.5, 'T1_ms': 1.0, 'color': 'red'},
    'Fluxonium\n(sweet spot)': {'anarmon': -2.0, 'T1_ms': 1.48, 'color': 'darkred'},
}

nombres = list(sistemas.keys())
anarmonis = [v['anarmon'] for v in sistemas.values()]
t1s = [v['T1_ms'] for v in sistemas.values()]
colores = [v['color'] for v in sistemas.values()]

x = np.arange(len(nombres))
width = 0.35
axes[1].bar(x - width/2, [-a for a in anarmonis], width, label='|α| (GHz)',
            color=colores, alpha=0.7)
ax2 = axes[1].twinx()
ax2.bar(x + width/2, t1s, width, label='T₁ (ms)',
        color=[c + '80' for c in ['0000FF', 'FF0000', '8B0000']], alpha=0.5,
        color=colores, alpha=0.4)
axes[1].set_xticks(x)
axes[1].set_xticklabels(nombres, fontsize=9)
axes[1].set_ylabel('Anarmonicidad |α| (GHz)', color='blue')
ax2.set_ylabel('T₁ (ms)', color='red')
axes[1].set_title('Transmon vs Fluxonium')
axes[1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.show()
```

---

## Resultados experimentales: fluxonium en 2024

```python
resultados_fluxonium_2024 = """
RESULTADOS EXPERIMENTALES FLUXONIUM (2023-2024)
═════════════════════════════════════════════════════════════════════

MIT Lincoln Laboratory (Oliver group):
  T₁ = 1.48 ms  (5 GHz, sweet spot)
  T₂* = 0.27 ms
  Error de puerta 1Q: 0.001% (10× mejor que transmon top)
  Ref: Nguyen et al., PRX Quantum 3, 037001 (2022)

IBM — Fluxonium en cadena (2023):
  T₁ > 0.5 ms consistente en 4 qubits
  Error CNOT: 0.5% (comparable a transmon top)
  Desafío: acoplar sin degradar T₁

Princeton (Houck group):
  Fluxonium 2D array: 5×5 qubits
  Error 1Q < 0.01%  (benchmark)
  Error 2Q ~ 0.3%   (aún por mejorar vs transmon)

VENTAJAS vs TRANSMON:
  ✅ T₁ 10-100× mayor
  ✅ Anarmonicidad 5-10× mayor → puertas más rápidas y selectivas
  ✅ Sweet spot: sensibilidad mínima al ruido de flujo
  ✅ Mejor coherencia a frecuencias de operación más bajas (<1 GHz)

DESAFÍOS:
  ❌ Acoplamiento más complejo (frecuencias bajas, ej. 50-500 MHz)
  ❌ Readout más difícil (frecuencia < 1 GHz)
  ❌ Puertas 2Q: T₂ limitado por el baño de bosones del array
  ❌ Fabricación: array de N junctions adicional

PERSPECTIVA:
  Threshold de error fault-tolerant para surface code: ~1%
  Fluxonium ya supera este umbral para puertas 1Q
  Puertas 2Q de fluxonium: objetivo ~0.1% para 2026-2027
"""
print(resultados_fluxonium_2024)
```

---

## El qubit 0-π: protección topológica por diseño

El qubit 0-π fue propuesto por Kitaev (2006) y Dempster et al. (2014).
Su Hamiltoniano tiene una simetría discreta que protege tanto frente a ruido
de carga como de flujo de forma **exponencial** en el parámetro del circuito:

$$\hat{H}_{0\pi} = \frac{(2e)^2}{2C_J} \hat{n}_\theta^2 + \frac{(2e)^2}{2C_\phi} \hat{n}_\phi^2 - 2E_J \cos\theta \cos\phi + E_L \phi^2$$

Las dos variables $\theta$ y $\phi$ se desacoplan en el límite de protección:
- $\theta$: oscilador de plasma (ruido de carga)
- $\phi$: potencial de doble pozo (qubit)

```python
import numpy as np
import matplotlib.pyplot as plt

def potencial_0pi(phi: np.ndarray, theta: float, Ej: float, El: float) -> np.ndarray:
    """Potencial efectivo del qubit 0-π en la coordenada φ."""
    return -2 * Ej * np.cos(theta) * np.cos(phi) + El * phi**2

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

phi_vals = np.linspace(-3 * np.pi, 3 * np.pi, 400)
Ej_vals = [1.0, 5.0, 10.0]
El = 0.1

# Potencial para diferentes E_J
ax = axes[0]
for Ej in Ej_vals:
    V = potencial_0pi(phi_vals, theta=0, Ej=Ej, El=El)
    ax.plot(phi_vals / np.pi, V, lw=2, label=f'E_J = {Ej} GHz')
ax.set_xlabel('φ / π')
ax.set_ylabel('Energía (GHz)')
ax.set_title('Potencial 0-π (θ=0)')
ax.legend(fontsize=9)
ax.grid(alpha=0.3)

# Separación exponencial de niveles
Ej_scan = np.linspace(1, 15, 100)
# En el límite de protección: ΔE ≈ Δ₀ exp(-a√(E_J/E_L))
gap_ratio = np.exp(-2.0 * np.sqrt(Ej_scan / El))
gap_ratio /= gap_ratio[0]  # normalizar

axes[1].semilogy(Ej_scan, gap_ratio, 'b-', lw=2)
axes[1].set_xlabel('E_J (GHz)')
axes[1].set_ylabel('ΔE / ΔE₀ (log)')
axes[1].set_title('Supresión exponencial del splitting de estados')
axes[1].grid(alpha=0.3)
axes[1].set_title('Protección exponencial del qubit 0-π')

# Comparativa de sensibilidades (esquemático)
plataformas = ['Transmon', 'Fluxonium\n(sweet spot)', 'Qubit 0-π']
sensib_carga = [1e-3, 1e-5, 1e-9]    # Δf/∂ng (Hz/e, escala relativa)
sensib_flujo = [1e-3, 1e-6, 1e-9]    # Δf/∂Φ (Hz/Φ₀, escala relativa)

x = np.arange(len(plataformas))
width = 0.35
axes[2].bar(x - width/2, np.log10(sensib_carga), width, label='Sensib. a carga (log₁₀)', color='blue', alpha=0.7)
axes[2].bar(x + width/2, np.log10(sensib_flujo), width, label='Sensib. a flujo (log₁₀)', color='red', alpha=0.7)
axes[2].set_xticks(x)
axes[2].set_xticklabels(plataformas, fontsize=9)
axes[2].set_ylabel('log₁₀(sensibilidad relativa)')
axes[2].set_title('Protección frente a ruido (menor = mejor)')
axes[2].legend(fontsize=9)
axes[2].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.show()
```

---

## Estado del arte 2024: qubit 0-π

```python
estado_arte_0pi = """
QUBIT 0-π: ESTADO DEL ARTE 2024
═══════════════════════════════════════════════════════════════════

TEORÍA (confirmada):
  Propuesta original: Kitaev (2006), Ioffe & Feigelman (2002)
  Diseño circuital: Brooks, Kitaev, Preskill (2013)
  Hamiltoniano 0-π: Dempster et al., PRB 90, 094518 (2014)

EXPERIMENTO (Larson/Yale/Harvard 2019-2023):
  Groszkowski et al., npj QI 4, 16 (2018) — código del Hamiltoniano
  Gyenis et al., PRX Quantum 2, 010339 (2021):
    → Primer qubit 0-π experimental
    → T₁ = 1.6 ms, T_φ = 25 μs
    → Coherencia limitada por diseño no optimizado

  Zhu et al., 2022 (arXiv:2207.00452):
    → Demostración de la protección dual
    → Sensibilidad al ruido 100× menor que transmon

DESAFÍOS ACTUALES:
  ❌ Diseño de puertas en qubits protegidos:
     La misma simetría que protege dificulta las operaciones
     ("dilemma": si está totalmente protegido, no se puede operar)
  ❌ Readout: las transiciones están suprimidas (misma protección)
  ❌ Escalabilidad: circuito complejo, 4 elementos por qubit mínimo

PERSPECTIVA:
  El qubit 0-π es más un hito teórico que una plataforma inmediata.
  Informa el diseño de qubits bifluxon, gatemon, cos(2φ), etc.
  Horizonte de hardware: 2028-2032 para dispositivos funcionales.
"""
print(estado_arte_0pi)
```

---

**Referencias:**
- Koch et al., *PRA* 76, 042319 (2007) — transmon original
- Nguyen et al., *PRX Quantum* 3, 037001 (2022) — fluxonium T₁ = 1.48 ms
- Gyenis et al., *PRX Quantum* 2, 010339 (2021) — qubit 0-π experimental
- Brooks, Kitaev, Preskill, *PRA* 87, 052306 (2013) — teoría 0-π
- Krantz et al., *APR* 6, 021318 (2019) — review superconducting qubits
