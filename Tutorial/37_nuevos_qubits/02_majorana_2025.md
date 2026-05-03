# Qubits de Majorana: Estado del Arte 2025

**Módulo 37 · Artículo 2 · Nivel muy avanzado**

---

## Fermiones de Majorana: física fundamental

Un fermión de Majorana es su propio antipartícula: $\gamma = \gamma^\dagger$.
En materia condensada, los modos de Majorana emergen como excitaciones de borde
en superconductores topológicos.

El modelo más simple (Kitaev 1D, 2001):

$$
\hat{H} = -\mu \sum_j c_j^\dagger c_j - t \sum_j (c_j^\dagger c_{j+1} + \text{h.c.}) - \Delta \sum_j (c_j c_{j+1} + \text{h.c.})
$$

En la fase topológica ($|\mu| < 2t$), los modos de Majorana $\gamma_L, \gamma_R$
se localizan en los extremos y forman un qubit no-local:

$$
\hat{f} = \frac{1}{2}(\gamma_L + i \gamma_R), \qquad \hat{n}_f = \hat{f}^\dagger \hat{f} \in \{0, 1\}
$$

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh

def kitaev_chain(mu: float, t: float, Delta: float, N: int) -> np.ndarray:
    """
    Construye el Hamiltoniano BdG de la cadena de Kitaev.
    
    Retorna la matriz 2N×2N en base de Nambu (c, c†).
    """
    H_BdG = np.zeros((2 * N, 2 * N), dtype=complex)

    for j in range(N):
        # Término químico: -μ(c†c - 1/2)
        H_BdG[j, j]     = -mu / 2
        H_BdG[j + N, j + N] = mu / 2

    for j in range(N - 1):
        # Hopping: -t c†_{j+1} c_j
        H_BdG[j, j + 1] = -t
        H_BdG[j + 1, j] = -t
        H_BdG[j + N, j + N + 1] = t
        H_BdG[j + N + 1, j + N] = t

        # Pareo: Δ c_j c_{j+1}
        H_BdG[j, j + N + 1] = Delta
        H_BdG[j + N + 1, j] = Delta.conjugate()
        H_BdG[j + 1, j + N] = -Delta
        H_BdG[j + N, j + 1] = -Delta.conjugate()

    return H_BdG

# Diagrama de fase: gap vs μ
t = 1.0; Delta = 0.5; N = 50
mu_vals = np.linspace(-3, 3, 200)
gaps = []
for mu in mu_vals:
    H = kitaev_chain(mu, t, Delta, N)
    eigvals = np.sort(np.real(eigh(H, eigvals_only=True)))
    # Gap = mínima energía positiva
    pos_vals = eigvals[eigvals > 1e-10]
    gaps.append(pos_vals[0] if len(pos_vals) > 0 else 0)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].plot(mu_vals / t, gaps, 'b-', lw=2)
axes[0].axvline(-2, color='red', ls='--', alpha=0.7, label='μ = ±2t (transición)')
axes[0].axvline(2, color='red', ls='--', alpha=0.7)
axes[0].fill_betweenx([0, max(gaps)], -2, 2, alpha=0.1, color='green', label='Fase topológica')
axes[0].set_xlabel('μ / t')
axes[0].set_ylabel('Gap de energía (unidades t)')
axes[0].set_title('Gap vs μ: cadena de Kitaev (N=50)')
axes[0].legend()
axes[0].grid(alpha=0.3)

# Funciones de onda de los modos de Majorana en fase topológica
mu_topo = 0.0  # centro de la fase topológica
H_topo = kitaev_chain(mu_topo, t, Delta, N)
eigvals_t, eigvecs_t = eigh(H_topo)

# Modo de Majorana: eigenvalor más cercano a cero
idx_zero = np.argmin(np.abs(eigvals_t))
mode_L = np.abs(eigvecs_t[:N, idx_zero])**2   # componente de electrón
mode_R = np.abs(eigvecs_t[:N, idx_zero - 1])**2 if idx_zero > 0 else mode_L[::-1]

sites = np.arange(N)
axes[1].bar(sites, mode_L, alpha=0.7, color='blue', label='Modo γ_L (Majorana izq.)')
axes[1].bar(sites, mode_R, alpha=0.7, color='red', label='Modo γ_R (Majorana der.)')
axes[1].set_xlabel('Sitio de la cadena')
axes[1].set_ylabel('|ψ|²')
axes[1].set_title('Localización de modos de Majorana en los extremos')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## Por qué Majorana → qubit topológico

La información cuántica almacenada en los modos de Majorana está **no-localmente
distribuida**: no hay operador local que pueda medir el qubit.

```python
propiedades_qubit_majorana = """
QUBIT DE MAJORANA: PROPIEDADES FUNDAMENTALES
═══════════════════════════════════════════════════════════════════

CODIFICACIÓN NO-LOCAL:
  |0⟩_M ↔ n_f = 0  (γ_L, γ_R no ocupados)
  |1⟩_M ↔ n_f = 1  (modo fermirónico ocupado)
  
  Operadores lógicos:
    Z̄ = iγ_L γ_R   (paridad del modo no-local)
    X̄ = γ_L          (fusión de Majoranas)
  
  Ningún operador LOCAL puede medir Z̄ → protegido frente a errores locales

PUERTAS POR BRAIDÍNG (anyones no-abelianos):
  Mover γ₁ alrededor de γ₂ aplica la puerta unitaria:
  U₁₂ = exp(π γ₁ γ₂ / 4) = (1 + γ₁ γ₂) / √2
  
  Esta unitaria es TOPOLÓGICA: solo depende de la topología del braidíng,
  no de los detalles de la trayectoria → protegida frente a errores de control
  
  Conjunto de puertas por braidíng: {H, S, CNOT} (no universal)
  Puertas T: necesitan magic state distillation (no topológicas)

OVERHEAD DE CORRECCIÓN DE ERRORES:
  Estimado teórico: ~10× menor que transmon en surface code
  (Microsoft apunta a qubit lógico con 10-100 físicos vs 1000 en transmon)

ESTADO 2025:
  → Microsoft anunció "Topological Core" en Febrero 2025
  → Medición del gap topológico en nanowire InAs-Al
  → Qubits de Majorana demostrados como dispositivos de 2 estados
  → Tiempo de coherencia: μs (mejorando)
"""
print(propiedades_qubit_majorana)
```

---

## Implementaciones físicas: nanowires y plataformas alternativas

```python
import numpy as np
import matplotlib.pyplot as plt

# Condiciones para el gap topológico en nanowire semiconductor-superconductor
# H = (k²/2m - μ)τ_z + α_R k σ_y τ_z + B σ_x + Δ_0 τ_x
# Transición topológica cuando: B_c = √(μ² + Δ_0²)

def diagrama_fase_nanowire(mu_range, Delta_0: float = 0.25):
    """
    Diagrama de fase para nanowire InAs-Al.
    mu: potencial químico (meV)
    Delta_0: gap superconductor inducido (meV)
    B_c: campo magnético crítico (meV)
    """
    mu = np.linspace(mu_range[0], mu_range[1], 300)
    B_c = np.sqrt(mu**2 + Delta_0**2)  # campo crítico
    return mu, B_c

mu, B_c = diagrama_fase_nanowire([-2, 2], Delta_0=0.25)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Diagrama de fase (μ, B)
axes[0].plot(mu, B_c, 'b-', lw=2, label='B_c = √(μ²+Δ₀²)')
axes[0].fill_between(mu, B_c, 5, alpha=0.2, color='green', label='Fase topológica (B > B_c)')
axes[0].fill_between(mu, 0, B_c, alpha=0.2, color='red', label='Fase trivial (B < B_c)')
axes[0].set_xlabel('Potencial químico μ (meV)')
axes[0].set_ylabel('Campo Zeeman B (meV)')
axes[0].set_title('Diagrama de fase: nanowire InAs-Al')
axes[0].legend(fontsize=9)
axes[0].grid(alpha=0.3)
axes[0].set_ylim(0, 2)

# Comparativa de plataformas Majorana
plataformas_majorana = {
    'InAs-Al nanowire\n(Microsoft)': {
        'madurez': 7, 'T_coh_us': 10, 'escalab': 5, 'color': 'blue'
    },
    'InSb-Al nanowire\n(Delft)': {
        'madurez': 6, 'T_coh_us': 5, 'escalab': 4, 'color': 'cyan'
    },
    'Topological insulator\n(Bi₂Se₃-Nb)': {
        'madurez': 4, 'T_coh_us': 1, 'escalab': 3, 'color': 'purple'
    },
    'Planar Josephson\njunction (MIT)': {
        'madurez': 5, 'T_coh_us': 3, 'escalab': 7, 'color': 'orange'
    },
    'Ferromagnet-SC\n(Fe/Pb)': {
        'madurez': 3, 'T_coh_us': 0.1, 'escalab': 2, 'color': 'brown'
    },
}

nombres = list(plataformas_majorana.keys())
madureces = [v['madurez'] for v in plataformas_majorana.values()]
escalabs = [v['escalab'] for v in plataformas_majorana.values()]
colores = [v['color'] for v in plataformas_majorana.values()]
t_cohs = [v['T_coh_us'] for v in plataformas_majorana.values()]

scatter = axes[1].scatter(madureces, escalabs, s=[t * 50 for t in t_cohs],
                          c=colores, alpha=0.8, edgecolors='black', lw=1)
for i, nombre in enumerate(nombres):
    axes[1].annotate(nombre, (madureces[i], escalabs[i]),
                    textcoords='offset points', xytext=(5, 5), fontsize=7)
axes[1].set_xlabel('Madurez tecnológica (1-10)')
axes[1].set_ylabel('Potencial de escalabilidad (1-10)')
axes[1].set_title('Plataformas Majorana 2025\n(tamaño = T_coherencia en μs)')
axes[1].grid(alpha=0.3)
axes[1].set_xlim(1, 10)
axes[1].set_ylim(1, 10)

plt.tight_layout()
plt.show()
```

---

## Microsoft Topological Core: anuncio 2025

```python
microsoft_2025 = """
MICROSOFT TOPOLOGICAL CORE — FEBRERO 2025
══════════════════════════════════════════════════════════════════

ANUNCIO OFICIAL (Nature, Febrero 2025):
  Microsoft anunció la demostración del "Topological Qubit" basado en
  nanowires InAs recubiertos con Al, con las siguientes características:

  ✅ Medición del gap topológico ≥ 30 μeV (confirmado)
  ✅ Tiempo de vida del estado de paridad: ~0.1 ms
  ✅ Dispositivo de 6 modos de Majorana (3 pares lógicos)
  ✅ Lectura por reflectometría de microondas

  CONTEXTO HISTÓRICO:
    2018: Paper Nature retractado (Mourik et al. seguimiento)
    2021: Paper Science 373 retractado (Kouwenhoven group)
    2023: Microsoft Papers Nature Physics — nuevos protocolos de validación
    2025: Anuncio del "Topological Core" — primera demostración robusta

  LO QUE SE DEMOSTRÓ:
    → Qubit de paridad estable (no coherencia cuántica completa aún)
    → Gap topológico medible y reproducible
    → Arquitectura compatible con integración 2D

  LO QUE FALTA:
    ❌ Demostración de superposición cuántica coherente de Majorana
    ❌ Braidíng universal de anyones
    ❌ Escalado a múltiples qubits lógicos

DEBATE CIENTÍFICO:
  Varios grupos (Akhmerov, Das Sarma) señalan que:
  → Los experimentos son compatibles con Andreev bound states triviales
  → El gap topológico no implica modos de Majorana sin más evidencia
  → Se necesita interferometría de no-abelianos para confirmación definitiva

EVALUACIÓN HONESTA 2025:
  ┌─────────────────────────────────────────────────────────────┐
  │ Los qubits de Majorana son prometedores pero NO están listos │
  │ para computación cuántica fault-tolerant hoy.               │
  │ Microsoft ha hecho progreso real pero el camino es largo.   │
  │ Horizonte realista para qubits Majorana funcionales: 2030+  │
  └─────────────────────────────────────────────────────────────┘
"""
print(microsoft_2025)
```

---

## Comparativa topológica vs superconductor convencional

```python
import numpy as np

def analisis_overhead_fault_tolerant(
    p_fisico: float,        # tasa de error físico
    p_threshold: float,     # umbral del código
    d_logico: int = 1000    # número de operaciones lógicas objetivo
) -> dict:
    """
    Estima el overhead de corrección de errores para lograr
    una tasa de error lógica de 10⁻¹² en p_logico operaciones.
    
    Basado en el modelo de umbral del surface code.
    """
    if p_fisico >= p_threshold:
        return {'viable': False}

    # Tasa de error lógica: p_L ≈ A (p/p_th)^((d+1)/2)
    # Para p_L = 10^-12, despejamos d:
    A = 0.1  # prefactor típico
    p_ratio = p_fisico / p_threshold
    target_p_L = 1e-12 / d_logico

    # d: distancia del código
    d = int(np.ceil(2 * np.log(target_p_L / A) / np.log(p_ratio) - 1))
    d = max(d, 3)

    # Qubits físicos por qubit lógico en surface code: ~2d²
    qubits_por_logico = 2 * d**2

    return {
        'viable': True,
        'p_fisico': p_fisico,
        'distancia_d': d,
        'qubits_por_logico': qubits_por_logico,
        'p_L': A * p_ratio**((d + 1) // 2),
    }

print('Overhead de corrección de errores (surface code):')
print(f'{"Plataforma":>20} | {"p_fís":>7} | {"d":>4} | {"q/lógico":>10} | {"p_L estimada"}')
print('-' * 65)

plataformas = [
    ('Transmon (top)',      1e-3, 1e-2),
    ('Transmon (promedio)', 3e-3, 1e-2),
    ('Fluxonium (1Q)',      1e-4, 1e-2),
    ('Majorana (proyect.)', 1e-4, 3e-2),  # umbral mayor por topología
    ('Spin-Si (proyect.)',  1e-3, 1e-2),
]

for nombre, p_fis, p_th in plataformas:
    r = analisis_overhead_fault_tolerant(p_fis, p_th)
    if r['viable']:
        print(f'{nombre:>20} | {p_fis:>7.0e} | {r["distancia_d"]:>4} | '
              f'{r["qubits_por_logico"]:>10} | {r["p_L"]:.2e}')
    else:
        print(f'{nombre:>20} | {p_fis:>7.0e} | {"N/A":>4} | {"∞":>10} | (sobre umbral)')
```

---

**Referencias:**
- Kitaev, *Physics-Uspekhi* 44, 131 (2001) — cadena de Kitaev
- Mourik et al., *Science* 336, 1003 (2012) — primera evidencia experimental
- Microsoft Azure Quantum, *Nature* (Feb 2025) — Topological Core
- Nayak et al., *Rev. Mod. Phys.* 80, 1083 (2008) — anyones no-abelianos
- Das Sarma, *npj Quantum Inf.* 9, 8 (2023) — evaluación crítica
- Akhmerov et al., arXiv:2303.xxxxx (2023) — protocolo de validación topológica
