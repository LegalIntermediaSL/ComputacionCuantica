# Spin en Silicio: Qubits CMOS

**Módulo 37 · Artículo 3 · Nivel muy avanzado**

---

## Por qué silicio: la promesa CMOS

Los qubits de espín en silicio son electrones (o huecos) atrapados en puntos
cuánticos definidos por electrodos metálicos sobre Si/SiGe o Si-MOS.

Su principal ventaja: **compatibilidad con la industria semiconductora CMOS**,
lo que podría permitir fabricación masiva a costes de orden de magnitud menor.

```python
import numpy as np
import matplotlib.pyplot as plt

ventajas_spin_si = """
QUBITS DE ESPÍN EN SILICIO: ARGUMENTOS CLAVE
═══════════════════════════════════════════════════════════════════

FÍSICA FAVORABLE:
  → Espín electrónico: qubit natural con dos estados |↑⟩, |↓⟩
  → Si-28 enriquecido: isótopo sin spin nuclear → campo de hiperfina = 0
  → T₂* ≈ 20 ms en Si-28 (récord 2021, Laucht/UNSW/Intel)
  → Tamaño: punto cuántico de ~50 nm → densidades 10⁶ qubits/mm²

COMPATIBILIDAD INDUSTRIAL:
  → Misma litografía que los chips CMOS avanzados (28 nm, 14 nm)
  → Temperatura de operación: 1.2 K (vs 10-20 mK para superconductores)
  → Posibilidad de integrar electrónica de control clásica on-chip
  → Intel, IMEC, TSMC ya fabrican dispositivos experimentales

DESAFÍOS:
  → Variabilidad de fábrica: cada qubit es ligeramente diferente
  → Acoplamiento entre qubits: exchange J muy sensible a voltajes
  → Lectura dispersiva: más lenta que superconductores
  → Operaciones de 2Q: fidelidad actual ~99.5% (vs 99.7% en superconductor top)
"""
print(ventajas_spin_si)
```

---

## Física del punto cuántico: el Hamiltoniano de espín

El Hamiltoniano de un punto cuántico de Si en campo magnético:

$$\hat{H} = g^* \mu_B B_z \hat{S}_z + g^* \mu_B B_{\text{AC}}(t) (\cos\omega t \cdot \hat{S}_x + \sin\omega t \cdot \hat{S}_y)$$

Para dos espines con intercambio $J$:

$$\hat{H}_2 = \hat{H}_1 + \hat{H}_2 + J(t) \hat{\mathbf{S}}_1 \cdot \hat{\mathbf{S}}_2$$

```python
import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt

# Constantes
mu_B = 0.0578  # meV/T (magnetón de Bohr)
g_Si = 2.0     # factor g en silicio (aproximado)

def hamiltoniano_spin_1q(B_z: float, B_AC_amp: float,
                          omega_drive: float, t: float) -> np.ndarray:
    """
    Hamiltoniano de Rabi para un qubit de espín.
    
    B_z: campo estático (T)
    B_AC_amp: amplitud campo de microondas (T)
    omega_drive: frecuencia de drive (GHz)
    """
    omega_L = g_Si * mu_B * B_z / 1.055e-25  # En GHz (simplificado)
    omega_R = g_Si * mu_B * B_AC_amp / 2
    
    # En el marco rotante a omega_L
    H = np.array([
        [-omega_R * np.cos((omega_drive - omega_L) * t), omega_R],
        [omega_R, omega_R * np.cos((omega_drive - omega_L) * t)]
    ])
    return H

def oscilaciones_rabi(omega_R: float, delta: float, n_puntos: int = 200) -> tuple:
    """
    Simula las oscilaciones de Rabi para un qubit de espín.
    
    omega_R: frecuencia de Rabi (MHz)
    delta: desintonización (MHz)
    """
    omega_eff = np.sqrt(omega_R**2 + delta**2)  # frecuencia efectiva
    t_vals = np.linspace(0, 4 * np.pi / omega_eff, n_puntos)
    
    # P(|1⟩) = (omega_R/omega_eff)² sin²(omega_eff t / 2)
    P_excited = (omega_R / omega_eff)**2 * np.sin(omega_eff * t_vals / 2)**2
    return t_vals, P_excited

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Oscilaciones de Rabi para diferentes desintonizaciones
omega_R = 2 * np.pi  # frecuencia de Rabi normalizada
deltas = [0, 0.5, 1.0, 2.0]

for delta in deltas:
    t_vals, P = oscilaciones_rabi(omega_R, delta)
    axes[0].plot(t_vals, P, lw=2, label=f'δ = {delta:.1f} ω_R')

axes[0].set_xlabel('Tiempo (unidades 1/ω_R)')
axes[0].set_ylabel('P(|↑⟩)')
axes[0].set_title('Oscilaciones de Rabi — Qubit de espín Si')
axes[0].legend(fontsize=9)
axes[0].grid(alpha=0.3)

# T₂ decay: comparativa Si-28 vs Si-nat vs GaAs
t_dephasing = np.linspace(0, 20, 400)  # μs
plataformas_t2 = {
    'GaAs (spin electrón)':   {'T2': 0.01, 'color': 'red'},    # 10 ns
    'Si-nat (electrón)':      {'T2': 0.1,  'color': 'orange'},
    'Si-28 (electrón)':       {'T2': 20.0, 'color': 'blue'},
    'Si-28 (hueco, 2023)':    {'T2': 4.0,  'color': 'purple'},
    'Si-28 (núcleo P, 2020)': {'T2': 35000, 'color': 'green'},  # 35 ms
}

for nombre, params in plataformas_t2.items():
    T2 = params['T2']
    decay = np.exp(-(t_dephasing / T2)**2)  # Gaussiano
    if T2 < 100:
        axes[1].plot(t_dephasing, decay, lw=2, color=params['color'], label=f'{nombre} (T₂={T2} μs)')

axes[1].set_xlabel('Tiempo (μs)')
axes[1].set_ylabel('Coherencia (decay Gaussiano)')
axes[1].set_title('T₂* comparativo — plataformas de espín')
axes[1].legend(fontsize=8, loc='upper right')
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## Acoplamiento de qubits: intercambio J y CNOT

La puerta de 2 qubits en spin-Si se implementa mediante el intercambio $J$ entre
puntos cuánticos adyacentes, controlado por voltaje de barrera $V_B$:

$$J(V_B) = J_0 \exp(-\alpha V_B)$$

```python
import numpy as np
import matplotlib.pyplot as plt

def hamiltoniano_heisenberg(J: float) -> np.ndarray:
    """
    Hamiltoniano de intercambio para dos espines: J S₁·S₂
    Base: |↑↑⟩, |↑↓⟩, |↓↑⟩, |↓↓⟩
    """
    # S₁·S₂ = (1/2)(S₊₁S₋₂ + S₋₁S₊₂) + S_z1 S_z2
    return J * np.array([
        [0.25,  0,     0,     0   ],
        [0,    -0.25,  0.50,  0   ],
        [0,     0.50, -0.25,  0   ],
        [0,     0,     0,     0.25]
    ])

def puerta_sqrt_SWAP(t: float, J: float) -> np.ndarray:
    """
    Evolución unitaria bajo H_exchange durante tiempo t.
    En t = π/2J: √SWAP (genera entrelazamiento)
    En t = π/J:  SWAP
    """
    H = hamiltoniano_heisenberg(J)
    U = np.linalg.matrix_power(
        np.eye(4) - 1j * H * 0.01,  # Euler step pequeño
        int(t / 0.01)
    )
    # Usar exponencial exacta
    from scipy.linalg import expm
    return expm(-1j * H * t)

# Evolución de la fidelidad de CNOT vs tiempo de gate
J_exchange = 20.0  # MHz (típico en Si-Si)
t_CNOT = np.pi / (2 * J_exchange)   # tiempo para √SWAP en unidades ħ=1

t_vals = np.linspace(0, 2 * t_CNOT, 100)
fid_vals = []

# Estado inicial |↑↓⟩ = base[1]
psi0 = np.array([0, 1, 0, 0], dtype=complex)

for t in t_vals:
    from scipy.linalg import expm
    U = expm(-1j * hamiltoniano_heisenberg(J_exchange) * t)
    psi_t = U @ psi0
    # Fidelidad con estado de Bell (↑↓ + ↓↑)/√2
    bell = np.array([0, 1, 1, 0]) / np.sqrt(2)
    fid_vals.append(abs(bell.conj() @ psi_t)**2)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].plot(t_vals * J_exchange / np.pi, fid_vals, 'b-', lw=2)
axes[0].axvline(0.5, color='red', ls='--', alpha=0.7, label='t = π/2J (√SWAP → Bell)')
axes[0].set_xlabel('t·J / π')
axes[0].set_ylabel('Fidelidad con estado de Bell')
axes[0].set_title('Generación de entrelazamiento por intercambio J')
axes[0].legend()
axes[0].grid(alpha=0.3)

# J vs voltaje de barrera (modelo exponencial)
V_barrier = np.linspace(-0.1, 0.3, 200)  # V (offset)
J_max = 50.0  # MHz
alpha = 20.0  # (1/V)
J_vals = J_max * np.exp(-alpha * V_barrier)

axes[1].semilogy(V_barrier * 1000, J_vals, 'r-', lw=2)
axes[1].axhline(20, color='blue', ls='--', alpha=0.7, label='J = 20 MHz (típico)')
axes[1].axhline(0.1, color='gray', ls=':', alpha=0.7, label='J << δ (qubits desacoplados)')
axes[1].set_xlabel('Voltaje de barrera (mV)')
axes[1].set_ylabel('Intercambio J (MHz)')
axes[1].set_title('Sintonización de J mediante voltaje')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## Roadmap: Intel, IMEC, y el camino al millón de qubits

```python
roadmap_spin_si = """
ROADMAP SPIN-SI 2024-2032
══════════════════════════════════════════════════════════════════

INTEL — Horse Ridge II + Tunnel Falls:
  2024: Chip 12 qubits, error 1Q < 0.1%, error 2Q < 1%
  2026: 100 qubits, integración parcial con electrónica 28 nm
  2028: 1000 qubits en un chip, error mitigation on-chip
  2032: 1M qubits físicos → ~10k qubits lógicos (objetivo)

IMEC (Bélgica) — programa EU Quantum Flagship:
  Plataforma Si-MOS 300 mm wafer (mismo proceso que memoria DRAM)
  Objetivo: uniformidad de qubits < 5% varianza en parámetros clave
  Colaboraciones: CEA-Leti, IQM, QuTech

QuTech (Delft) — plataforma Si/SiGe:
  Demostración de 6 qubits en array lineal (2022)
  Error 2Q medido: 99.5% fidelidad
  Acoplamiento mediante punto cuántico mediador

UNSW Sydney (Morello group):
  Qubits de spin nuclear de P en Si: T₂ = 35 ms (récord)
  Spin de electrón de P: T₂* = 1 ms
  Lectura de carga + spin: >99% fidelidad

FECHAS CLAVE RECIENTES:
  2021: Intel demuestra 300 mm Si qubit wafer
  2022: QuTech 6-qubit array, fidelidad 99.5%
  2023: Google (spin resonance): T₂ > 1 ms en Si/SiGe
  2024: Intel Tunnel Falls 12 qubits, chip fabricado en fab Intel

TEMPERATURA DE OPERACIÓN:
  Si-spin: 1-4 K (criostat de helio 4 accesible)
  vs Superconductor: 10-20 mK (dilution refrigerator, 10× más costoso)
  Ventaja térmica: puede acoplarse con electrónica CMOS a 4 K
"""
print(roadmap_spin_si)
```

---

## Qubits de hueco en silicio: la revolución del hole spin

```python
import numpy as np
import matplotlib.pyplot as plt

hole_spin_2024 = """
HOLE SPIN QUBITS — EL CAMINO RÁPIDO A GATES ULTRARRÁPIDAS
═══════════════════════════════════════════════════════════════════

FÍSICA DE HUECOS vs ELECTRONES:
  → Huecos: banda de valencia, espín efectivo J=3/2 (heavy hole)
  → Acoplamiento espín-órbita FUERTE (a diferencia del electrón)
  → Ventaja: puertas eléctricas directas (sin líneas de microondas)
  → Desventaja: susceptibilidad a ruido de carga

RESULTADOS 2022-2024:
  Fraunhofer/TU München (Kataoka 2023):
    → Puerta 1Q a 35 MHz (electrónica directa)
    → Error < 0.1% por puerta (>99.9% fidelidad)
    → T₂ = 4 μs en Ge/Si nanowire
  
  Delft (QuTech, Sammak 2024):
    → 2×2 array de huecos en Ge/Si
    → Error 2Q = 1.2%  
    → Escalabilidad demostrada en 4 qubits
  
  UNSW (Laucht group):
    → Si-MOS hole qubit: T₂ = 5 μs
    → Integración con readout RF compacto

PLATAFORMAS HOLE QUBIT:
  1. Si-MOS: compatible con CMOS estándar
  2. Ge/Si core-shell nanowire: acoplamiento SO más fuerte
  3. Ge/SiGe het.: alta mobilidad, Ge puro sin spin nuclear
  4. Si/SiGe het. (holes): intermedio, T₂ moderado

VELOCIDAD DE PUERTAS:
  Electrón spin (EDSR): ~10 MHz  (100 ns/gate)
  Hueco spin (directo): ~100 MHz  (10 ns/gate)  ← 10× más rápido
  Superconductor:       ~250 MHz  (4 ns/gate)
"""
print(hole_spin_2024)

# Comparativa velocidad vs coherencia
fig, ax = plt.subplots(figsize=(8, 6))

plataformas = {
    'Si-electrón\n(EDSR)':      {'v_gate_MHz': 10,  'T2_us': 500,  'color': 'blue',   'marker': 'o', 'size': 150},
    'Si-hueco\n(MOS)':          {'v_gate_MHz': 80,  'T2_us': 5,    'color': 'cyan',   'marker': 's', 'size': 150},
    'Ge/Si-hueco\n(nanowire)':  {'v_gate_MHz': 100, 'T2_us': 4,    'color': 'purple', 'marker': '^', 'size': 150},
    'Ge/SiGe-hueco':            {'v_gate_MHz': 50,  'T2_us': 10,   'color': 'magenta','marker': 'D', 'size': 150},
    'Transmon\n(SC)':           {'v_gate_MHz': 250, 'T2_us': 200,  'color': 'red',    'marker': '*', 'size': 200},
    'Fluxonium\n(SC)':          {'v_gate_MHz': 50,  'T2_us': 1000, 'color': 'darkred','marker': 'P', 'size': 200},
}

for nombre, params in plataformas.items():
    n_gates = params['v_gate_MHz'] * 1e6 * params['T2_us'] * 1e-6
    ax.scatter(params['v_gate_MHz'], params['T2_us'], 
               s=params['size'], c=params['color'],
               marker=params['marker'], label=f'{nombre} ({n_gates:.0f} gates/T₂)',
               edgecolors='black', linewidth=0.5, zorder=5)

# Líneas de número constante de puertas por T₂
for n_g in [100, 1000, 10000]:
    v = np.logspace(0.5, 3, 100)
    T2 = n_g / (v * 1e6) * 1e6  # en μs
    ax.loglog(v, T2, '--', alpha=0.3, color='gray')
    ax.text(v[-1] * 0.5, T2[-1], f'{n_g} gates/T₂', fontsize=7, color='gray')

ax.set_xlabel('Velocidad de puerta (MHz)')
ax.set_ylabel('T₂ (μs)')
ax.set_title('Speed vs Coherence — Plataformas de qubit 2024\n(más arriba y más a la derecha es mejor)')
ax.legend(fontsize=7, loc='lower left', ncol=2)
ax.grid(alpha=0.3, which='both')
ax.set_xscale('log')
ax.set_yscale('log')
plt.tight_layout()
plt.show()
```

---

## Integración criogénica: electrónica on-chip a 4 K

```python
cryo_integration = """
INTEGRACIÓN CRIOGÉNICA: EL CUELLO DE BOTELLA DE ESCALABILIDAD
═══════════════════════════════════════════════════════════════════

PROBLEMA ACTUAL (transmon Y spin-Si):
  → Cada qubit necesita 5-10 líneas de control (RF, DC, flux)
  → A 1000 qubits: 5000-10000 cables al criostato = imposible
  → Potencia disipada por cables: >> presupuesto de enfriamiento

SOLUCIÓN: Electronics on-chip criogénica

SUPERCONDUCTOR (10-20 mK):
  → Electrónica en el mismo chip no es viable a 10 mK
  → Controladores a 4 K (HEMT amplifiers, custom ASIC)
  → Cables coaxiales del 4K al qubit: aún muchos

SPIN-SI (1-4 K):
  → Electrónica CMOS funciona a 4 K !
  → Intel: SoC HorsRidge II en 22nm FFL, operación a 4K
    - 32 canales RF por chip
    - Ruido de fase < -100 dBc/Hz
  → IQM: control chip a 4K para qubits superconductores
  → Visión a largo plazo: qubit + control en el mismo chip

POTENCIA DISPONIBLE EN CRIOSTATO:
  Dilution fridge (10 mK): ~20 μW (presupuesto mínimo)
  He-4 (4 K):             ~1 W    (50× más generoso)
  
  → Si-spin a 4K: mucho más margen para electrónica on-chip
  → Ventaja clara de spin-Si sobre superconductores en escalabilidad

TIMELINE DE INTEGRACIÓN:
  2024: 32 qubits + control ASIC 4K (Intel/QuTech)
  2026: 256 qubits + control parcialmente integrado
  2028: 1024 qubits, control 80% on-chip a 4K
  2030: 10k qubits con control criogénico completo
"""
print(cryo_integration)
```

---

## Estado del arte consolidado: plataformas de spin 2025

| Plataforma | T₁ | T₂* | Gate 1Q | Gate 2Q | Fab | TRL |
|---|---|---|---|---|---|---|
| Si/SiGe electrón | 100 ms | 1 ms | 99.9% | 99.5% | QuTech/Intel | 4 |
| Si-MOS electrón | 50 ms | 20 ms | 99.9% | 99.0% | Intel/UNSW | 5 |
| Ge/Si hueco | 1 ms | 4 μs | 99.8% | 98.8% | TU München | 3 |
| Ge/SiGe hueco | 5 ms | 10 μs | 99.5% | 98.5% | Delft | 3 |
| Si-P nuclear | >1 s | 35 ms | 99.7% | 98.0% | UNSW | 3 |

*(TRL: Technology Readiness Level, 1-9)*

---

**Referencias:**
- Loss & DiVincenzo, *PRA* 57, 120 (1998) — propuesta original spin qubit
- Veldhorst et al., *Nature Nanotech.* 9, 981 (2014) — qubit Si-MOS
- Watson et al., *Nature* 555, 633 (2018) — 2-qubit en Si/SiGe
- Hendrickx et al., *Nature* 591, 580 (2021) — 4-qubit Ge/Si
- Zwerver et al., *Nature Electronics* 5, 184 (2022) — Intel Si-MOS
- Laucht et al., *Science Advances* 7, eabg9158 (2021) — T₂ = 20 ms
- Struck et al., *npj QI* 6, 40 (2020) — Si isotópicamente enriquecido
