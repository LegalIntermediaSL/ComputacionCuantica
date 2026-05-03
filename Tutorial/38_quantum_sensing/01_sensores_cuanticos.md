# Sensores Cuánticos y Metrología

**Módulo 38 · Artículo 1 · Nivel muy avanzado**

---

## El límite cuántico de la medición

La mecánica cuántica impone límites fundamentales a la precisión de cualquier medición.
Para N partículas independientes con estrategia clásica:

$$
\Delta\phi_{\text{SQL}} = \frac{1}{\sqrt{N}}
$$

Con entrelazamiento máximo (estados GHZ), se alcanza el **límite de Heisenberg**:

$$
\Delta\phi_{\text{HL}} = \frac{1}{N}
$$

La ventaja cuántica en metrología es una mejora **cuadrática** en precisión.

```python
import numpy as np
import matplotlib.pyplot as plt

# Comparativa SQL vs límite de Heisenberg
N_vals = np.logspace(0, 5, 300)

delta_SQL = 1 / np.sqrt(N_vals)       # límite clásico
delta_HL  = 1 / N_vals                 # límite de Heisenberg
delta_NISQ = 1 / N_vals**(0.7)        # caso intermedio (entrelazamiento parcial)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].loglog(N_vals, delta_SQL,  'b-',  lw=2, label='SQL (clásico): 1/√N')
axes[0].loglog(N_vals, delta_HL,   'r-',  lw=2, label='Heisenberg: 1/N')
axes[0].loglog(N_vals, delta_NISQ, 'g--', lw=2, label='NISQ parcial: 1/N^0.7')
axes[0].fill_between(N_vals, delta_HL, delta_SQL, alpha=0.1, color='green',
                     label='Ventana cuántica')
axes[0].set_xlabel('Número de partículas N')
axes[0].set_ylabel('Precisión Δφ (rad)')
axes[0].set_title('Límites de precisión en metrología cuántica')
axes[0].legend(fontsize=9)
axes[0].grid(alpha=0.3, which='both')

# Ventaja cuántica relativa: SQL/HL = √N
axes[1].loglog(N_vals, np.sqrt(N_vals), 'purple', lw=2)
axes[1].axvline(100,  color='blue',  ls='--', alpha=0.7, label='N=100 (sensor actual)')
axes[1].axvline(1e4,  color='red',   ls='--', alpha=0.7, label='N=10⁴ (futuro)')
axes[1].set_xlabel('N (átomos/fotones)')
axes[1].set_ylabel('Ventaja cuántica (SQL/HL = √N)')
axes[1].set_title('Ventaja cuántica vs tamaño del ensemble')
axes[1].legend(fontsize=9)
axes[1].grid(alpha=0.3, which='both')

plt.tight_layout()
plt.show()
```

---

## Información de Fisher cuántica (QFI)

El Cramér-Rao cuántico establece que la varianza de cualquier estimador
está acotada por la información de Fisher cuántica $F_Q$:

$$
\text{Var}(\hat{\phi}) \geq \frac{1}{N \cdot F_Q[\rho, A]}
$$

Para estado puro $|\psi\rangle$:
$$
F_Q = 4 \left(\langle\psi|\hat{A}^2|\psi\rangle - \langle\psi|\hat{A}|\psi\rangle^2\right) = 4\,\text{Var}(\hat{A})
$$

```python
import numpy as np
from scipy.linalg import eigvalsh

def qfi_estado_puro(psi: np.ndarray, A: np.ndarray) -> float:
    """
    Calcula la Información de Fisher Cuántica para estado puro.
    
    QFI = 4 Var(A) = 4(⟨A²⟩ - ⟨A⟩²)
    """
    exp_A  = np.real(psi.conj() @ A @ psi)
    exp_A2 = np.real(psi.conj() @ (A @ A) @ psi)
    return 4 * (exp_A2 - exp_A**2)

def qfi_estado_mixto(rho: np.ndarray, A: np.ndarray) -> float:
    """
    QFI para estado mixto via la fórmula espectral:
    F_Q = 2 Σ_{k,l: λ_k+λ_l>0} (λ_k - λ_l)²/(λ_k + λ_l) |⟨k|A|l⟩|²
    """
    eigvals, eigvecs = np.linalg.eigh(rho)
    n = len(eigvals)
    A_eig = eigvecs.conj().T @ A @ eigvecs  # A en base de eigenvectores de ρ

    F_Q = 0.0
    for k in range(n):
        for l in range(n):
            denom = eigvals[k] + eigvals[l]
            if denom > 1e-12:
                F_Q += 2 * (eigvals[k] - eigvals[l])**2 / denom * np.abs(A_eig[k, l])**2
    return np.real(F_Q)

# Estado GHZ de n qubits: (|0...0⟩ + |1...1⟩)/√2
def estado_ghz(n: int) -> np.ndarray:
    dim = 2**n
    psi = np.zeros(dim, dtype=complex)
    psi[0]    = 1 / np.sqrt(2)   # |0...0⟩
    psi[-1]   = 1 / np.sqrt(2)   # |1...1⟩
    return psi

# Observable: Jz = (1/2) Σ_i σ_z^(i)  (suma de Pauli Z)
def Jz_operator(n: int) -> np.ndarray:
    from functools import reduce
    sigma_z = np.array([[1, 0], [0, -1]], dtype=float) / 2
    I2 = np.eye(2)
    result = np.zeros((2**n, 2**n))
    for i in range(n):
        ops = [I2] * n
        ops[i] = sigma_z
        mat = reduce(np.kron, ops)
        result += mat
    return result

print('QFI para estados separables vs GHZ:')
print(f'{"n":>4} | {"QFI separable":>16} | {"QFI GHZ":>12} | {"Ventaja":>10}')
print('-' * 50)
for n in [1, 2, 3, 4]:
    A = Jz_operator(n)
    # Estado separable: producto de |+⟩
    psi_sep = np.ones(2**n, dtype=complex) / np.sqrt(2**n)
    qfi_sep = qfi_estado_puro(psi_sep, A)

    psi_ghz = estado_ghz(n)
    qfi_ghz = qfi_estado_puro(psi_ghz, A)

    print(f'{n:>4} | {qfi_sep:>16.3f} | {qfi_ghz:>12.3f} | {qfi_ghz/qfi_sep:>10.2f}×')

print('\nEsperado: QFI_GHZ = n² (Heisenberg), QFI_sep = n (SQL)')
```

---

## Relojes atómicos: el sensor más preciso del mundo

Los relojes atómicos operan sobre la transición de hiperfina del Cs-133 (9.192 GHz),
definiendo el segundo SI. Los de ión único (Al⁺, Yb⁺) superan en precisión:

```python
import numpy as np

especificaciones_relojes = """
RELOJES ATÓMICOS: ESTADO DEL ARTE 2024
═══════════════════════════════════════════════════════════════════════

RELOJ DE MICROONDAS (Cs):
  Frecuencia: 9.192 GHz (define el segundo SI)
  Incertidumbre: ~10⁻¹⁶ (SYRTE Paris, NIST-F2)
  Inestabilidad: σ_y(τ) ~ 10⁻¹³/√τ
  Funcionamiento: fuente de Cs fría (0.5 μK), cavidad Ramsey 1 m

RELOJ ÓPTICO DE ION ÚNICO (Al⁺, Yb⁺, Sr⁺):
  Frecuencia: ~10¹⁵ Hz (rango óptico)
  Incertidumbre: ~10⁻¹⁹ (NIST, PTB 2022)
  Ventaja: frecuencia 10⁵× mayor → mismo nº de ciclos, 10⁵× más preciso
  Inestabilidad: σ_y(τ) ~ 10⁻¹⁵/√τ con entrelazamiento

RELOJ DE RED ÓPTICA (Sr, Yb, Hg):
  N átomos en red óptica: promedio estadístico → √N mejora
  Incertidumbre Sr: 2.0 × 10⁻¹⁸ (SYRTE/NIST 2023)
  Ventaja cuántica con entrelazamiento: demostrada en 2021 (Pedrozo-Peñafiel et al.)

RECORD MUNDIAL (2023):
  Reloj óptico Yb (NIST): 8.1 × 10⁻¹⁹ incertidumbre sistemática
  → Deriva < 1 segundo en 40 mil millones de años
  → Detección de cambio gravitacional de 1 mm de altura

APLICACIONES PRÁCTICAS:
  GPS: Cs de 10⁻¹³ → error posición ~1 m
  GPS cuántico (futuro): Yb óptico → error <1 mm
  Detección de materia oscura: variaciones de constantes fundamentales
  Geodesia relativista: Δf/f = gh/c² → medir topografía por relatividad
"""
print(especificaciones_relojes)

# Cálculo: sensibilidad gravitacional de un reloj óptico
g = 9.80665  # m/s²
c = 3e8      # m/s
f_Cs = 9.192e9  # Hz
f_Sr = 4.291e14  # Hz  (reloj de red Sr)

# Δf/f = g·Δh/c²  (relatividad general, desplazamiento gravitacional)
delta_h_vals = np.logspace(-4, 3, 100)  # metros

fig, ax = plt.subplots(figsize=(8, 5))
for nombre, freq, incert, color in [
    ('Cs (microondas)', f_Cs, 1e-16, 'blue'),
    ('Sr red óptica',   f_Sr, 2e-18, 'red'),
]:
    delta_f = freq * g * delta_h_vals / c**2
    incert_abs = incert * freq
    ax.loglog(delta_h_vals, delta_f / freq, lw=2, color=color, label=f'{nombre}')
    ax.axhline(incert, color=color, ls='--', alpha=0.5, label=f'{nombre} (umbral {incert:.0e})')

ax.set_xlabel('Diferencia de altura Δh (m)')
ax.set_ylabel('Δf/f (desplazamiento relativo)')
ax.set_title('Sensibilidad gravitacional de relojes atómicos')
ax.legend(fontsize=9)
ax.grid(alpha=0.3, which='both')
plt.tight_layout()
plt.show()
```

---

## Magnetómetros NV-center: sensores cuánticos en diamante

Los centros de nitrógeno-vacante (NV) en diamante son sistemas de espín S=1
que actúan como magnetómetros con resolución nanométrica a temperatura ambiente.

```python
import numpy as np
import matplotlib.pyplot as plt

# Hamiltoniano NV-center en campo magnético B
def hamiltoniano_NV(B_z: float, B_x: float = 0.0,
                    D: float = 2.87e9, gamma_e: float = 28.0e9) -> np.ndarray:
    """
    Hamiltoniano del NV-center (base |ms=-1⟩, |ms=0⟩, |ms=+1⟩).
    
    D: splitting de desdoblamiento cero (2.87 GHz)
    gamma_e: razón giromagnética electrónica (28 MHz/mT)
    B_z: campo en el eje NV (T)
    B_x: campo transverso (T)
    """
    # En unidades GHz
    D_GHz = D / 1e9
    gamma_B_z = gamma_e * B_z / 1e9   # en GHz

    # Operadores de espín S=1
    Sz = np.diag([-1, 0, 1], 0).astype(complex)
    Sz2 = Sz @ Sz
    Sx = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=complex) / np.sqrt(2)

    H = D_GHz * Sz2 + gamma_B_z * Sz + (gamma_e * B_x / 1e9) * Sx
    return H

# Espectro de frecuencias de transición vs campo B
B_vals = np.linspace(0, 5e-3, 200)  # 0-5 mT
freqs_minus = []
freqs_plus  = []

for B in B_vals:
    H = hamiltoniano_NV(B)
    eigvals = np.sort(np.linalg.eigvalsh(H))
    # Transiciones |0⟩ → |±1⟩
    E0 = eigvals[1]   # ms=0 es el nivel intermedio
    Em = eigvals[0]   # ms=-1
    Ep = eigvals[2]   # ms=+1
    freqs_minus.append(abs(E0 - Em))
    freqs_plus.append(abs(Ep - E0))

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].plot(B_vals * 1e3, freqs_minus, 'b-', lw=2, label='f(|0⟩→|−1⟩)')
axes[0].plot(B_vals * 1e3, freqs_plus,  'r-', lw=2, label='f(|0⟩→|+1⟩)')
axes[0].axvline(0, color='gray', ls='--', alpha=0.5)
axes[0].set_xlabel('Campo magnético B (mT)')
axes[0].set_ylabel('Frecuencia de transición (GHz)')
axes[0].set_title('Espectro ODMR del NV-center vs campo B')
axes[0].legend()
axes[0].grid(alpha=0.3)

# Sensibilidad del magnetómetro NV
# η = (δf/δB)⁻¹ · δf_min  donde δf_min ~ 1/(T₂* √N)
T2star_vals = np.logspace(-6, -3, 100)   # T₂* en segundos (ns a ms)
N_photons = 1e4   # fotones detectados por segundo
gamma_e_Hz_T = 28e9  # Hz/T

# Sensibilidad: η ~ 1/(γ_e T₂* √(N_ph T₂*))
sensitivity = 1 / (gamma_e_Hz_T * np.sqrt(N_photons * T2star_vals**3))

axes[1].loglog(T2star_vals * 1e6, sensitivity * 1e12, 'g-', lw=2)
axes[1].axhline(1,    color='blue', ls='--', label='1 pT/√Hz (SQUID criogénico)')
axes[1].axhline(1e3,  color='red',  ls='--', label='1 nT/√Hz (ref. NV típico)')
axes[1].set_xlabel('T₂* (μs)')
axes[1].set_ylabel('Sensibilidad (pT/√Hz)')
axes[1].set_title('Sensibilidad NV-center vs tiempo de coherencia')
axes[1].legend(fontsize=9)
axes[1].grid(alpha=0.3, which='both')

plt.tight_layout()
plt.show()
```

---

## Interferometría de Ramsey: el protocolo estándar

```python
import numpy as np

def interferometria_ramsey(t_libre: float, omega_0: float,
                            delta: float, T2star: float,
                            n_shots: int = 1000) -> float:
    """
    Simula un experimento de interferometría de Ramsey.
    
    Protocolo: π/2 → evolución libre → π/2 → medida
    
    t_libre: tiempo de evolución libre (s)
    omega_0: frecuencia de resonancia (rad/s)
    delta: desintonización (rad/s)
    T2star: tiempo de decoherencia (s)
    
    Retorna: P(|1⟩)
    """
    # Amplitud de coherencia con decoherencia gaussiana
    coherencia = np.exp(-(t_libre / T2star)**2 / 2)

    # Probabilidad de estado excitado
    P_exc = 0.5 * (1 - coherencia * np.cos(delta * t_libre))

    # Añadir ruido de proyección cuántica
    counts = np.random.binomial(n_shots, P_exc)
    return counts / n_shots

# Secuencia de Ramsey: barrer tiempo libre
omega_0 = 2 * np.pi * 1e9   # 1 GHz
delta   = 2 * np.pi * 1e4   # desintonización 10 kHz
T2star  = 1e-4               # 100 μs

t_vals = np.linspace(0, 5 / (delta / (2 * np.pi)), 200)  # barrer 5 períodos
P_exc_vals = [interferometria_ramsey(t, omega_0, delta, T2star) for t in t_vals]

fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(t_vals * 1e6, P_exc_vals, 'b.', ms=4, alpha=0.6)
# Curva teórica
t_th = np.linspace(0, t_vals[-1], 1000)
P_th = 0.5 * (1 - np.exp(-(t_th / T2star)**2 / 2) * np.cos(delta * t_th))
ax.plot(t_th * 1e6, P_th, 'r-', lw=2, label='Teórico')
ax.set_xlabel('Tiempo libre τ (μs)')
ax.set_ylabel('P(|1⟩)')
ax.set_title(f'Interferometría de Ramsey — δ = {delta/(2*np.pi)/1e3:.0f} kHz, T₂* = {T2star*1e6:.0f} μs')
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# Sensibilidad en función del tiempo de interrogación
print('\nSensibilidad de Ramsey vs tiempo libre:')
print('Óptimo cuando δτ ≈ π/2 (pendiente máxima de la franja)')
tau_opt = np.pi / (2 * delta)
print(f'τ_óptimo = {tau_opt*1e6:.2f} μs')
print(f'Sensibilidad ~ 1/(δ·T₂*·√N_shots) = {1/(delta*T2star*np.sqrt(1000)):.4e} rad/√Hz')
```

---

**Referencias:**
- Giovannetti, Lloyd, Maccone, *Science* 306, 1330 (2004) — ventaja cuántica en metrología
- Degen, Reinhard, Cappellaro, *Rev. Mod. Phys.* 89, 035002 (2017) — quantum sensing review
- Pedrozo-Peñafiel et al., *Nature* 588, 414 (2020) — entrelazamiento en reloj óptico
- Ludlow et al., *Rev. Mod. Phys.* 87, 637 (2015) — relojes ópticos
- Rondin et al., *Rep. Prog. Phys.* 77, 056503 (2014) — NV-center magnetometría
