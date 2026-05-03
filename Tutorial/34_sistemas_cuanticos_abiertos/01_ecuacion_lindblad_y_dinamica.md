# Ecuación de Lindblad y Dinámica de Sistemas Abiertos

**Módulo 34 · Artículo 1 · Nivel muy avanzado**

---

## El problema de la decoherencia

Un sistema cuántico S en contacto con un entorno E evoluciona según:

$$
i\hbar \frac{d}{dt}|\Psi_{SE}\rangle = H_{SE}|\Psi_{SE}\rangle
$$

Al trazar sobre E, obtenemos la **ecuación maestra de Lindblad** para la
matriz densidad reducida ρ_S:

$$
\frac{d\rho}{dt} = -\frac{i}{\hbar}[H, \rho] + \sum_k \gamma_k \left(L_k \rho L_k^\dagger - \frac{1}{2}\{L_k^\dagger L_k, \rho\}\right)
$$

donde:
- $L_k$ son los **operadores de salto** (jump operators) que describen los canales de error
- $\gamma_k \geq 0$ son las tasas de decaimiento
- El primer término es la evolución coherente (unitaria)
- El segundo término es la parte disipativa (no unitaria)

```python
import numpy as np
from scipy.linalg import expm
import matplotlib.pyplot as plt

# Matrices de Pauli
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
sigma_plus  = (X + 1j*Y) / 2   # |1⟩⟨0| — raising
sigma_minus = (X - 1j*Y) / 2   # |0⟩⟨1| — lowering

def lindblad_rhs(rho: np.ndarray, H: np.ndarray,
                 ops: list[tuple[complex, np.ndarray]]) -> np.ndarray:
    """
    Lado derecho de la ecuación de Lindblad.

    ops: lista de (gamma_k, L_k)
    """
    drho = -1j * (H @ rho - rho @ H)  # conmutador [H, ρ]

    for gamma, L in ops:
        Ld = L.conj().T
        drho += gamma * (L @ rho @ Ld - 0.5 * (Ld @ L @ rho + rho @ Ld @ L))

    return drho

def integrar_lindblad(rho0: np.ndarray, H: np.ndarray,
                       ops: list[tuple[complex, np.ndarray]],
                       t_max: float, dt: float) -> tuple[np.ndarray, np.ndarray]:
    """Integración de la ecuación de Lindblad por Euler (pedagógico)."""
    t = np.arange(0, t_max, dt)
    rho = rho0.copy().astype(complex)
    historia = [rho.copy()]

    for _ in t[1:]:
        drho = lindblad_rhs(rho, H, ops)
        rho = rho + dt * drho
        # Mantener traza 1 y Hermiticidad
        rho = (rho + rho.conj().T) / 2
        rho /= rho.trace()
        historia.append(rho.copy())

    return t, np.array(historia)

# Ejemplo: decaimiento T1 (relajación de amplitud)
rho0 = np.array([[0, 0], [0, 1]], dtype=complex)  # estado |1⟩
H = np.zeros((2, 2), dtype=complex)                # sin Hamiltoniano

T1 = 1.0  # tiempo de relajación
gamma1 = 1 / T1

ops_t1 = [(gamma1, sigma_minus)]

t, hist_t1 = integrar_lindblad(rho0, H, ops_t1, t_max=4*T1, dt=0.01)
poblacion1 = np.array([rho[1,1].real for rho in hist_t1])
poblacion0 = np.array([rho[0,0].real for rho in hist_t1])

print(f'T1 = {T1} μs')
print(f'Al t=T1: P(|1⟩) = {poblacion1[int(T1/0.01)]:.4f}  (esperado: {np.exp(-1):.4f})')
print(f'Al t=2T1: P(|1⟩) = {poblacion1[int(2*T1/0.01)]:.4f} (esperado: {np.exp(-2):.4f})')
```

---

## Canales principales de decoherencia en qubits superconductores

```python
def canal_completo_qubit(T1: float, T2: float, rho0: np.ndarray,
                          t_max: float) -> dict:
    """
    Simula la dinámica completa de un qubit con T1 y T2.

    T1: tiempo de relajación (energía)
    T2: tiempo de decoherencia (fase)
    T_phi = (1/T2 - 1/(2*T1))^{-1}: tiempo de desfase puro

    Operadores de salto:
      - sigma_minus con tasa γ₁ = 1/T1 (relajación)
      - Z con tasa γ_phi/2 = 1/T_phi / 2 (desfase puro)
    """
    gamma1   = 1 / T1
    T_phi    = 1 / (1/T2 - 1/(2*T1)) if 1/T2 > 1/(2*T1) else np.inf
    gamma_phi = 1 / T_phi if T_phi < np.inf else 0

    ops = [(gamma1, sigma_minus)]
    if gamma_phi > 0:
        ops.append((gamma_phi / 2, Z))  # desfase puro

    H = np.zeros((2,2), dtype=complex)
    t, hist = integrar_lindblad(rho0, H, ops, t_max=t_max, dt=0.005)

    return {
        'T1': T1, 'T2': T2,
        't': t,
        'rho_hist': hist,
        'P1': np.array([r[1,1].real for r in hist]),
        'coherencia': np.array([abs(r[0,1]) for r in hist]),
    }

# Parámetros típicos de qubit superconductor transmon moderno
r_mod  = canal_completo_qubit(T1=100e-6, T2=150e-6,
                               rho0=np.array([[0.5, 0.5],[0.5, 0.5]], dtype=complex),
                               t_max=300e-6)

# Qubit de 2020 (menos avanzado)
r_2020 = canal_completo_qubit(T1=50e-6, T2=60e-6,
                               rho0=np.array([[0.5, 0.5],[0.5, 0.5]], dtype=complex),
                               t_max=200e-6)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

for ax, r, label, color in [
    (axes[0], r_mod, 'Transmon moderno\n(T1=100μs, T2=150μs)', 'blue'),
    (axes[0], r_2020, 'Transmon 2020\n(T1=50μs, T2=60μs)', 'red'),
]:
    t_us = r['t'] * 1e6
    ax.plot(t_us, r['P1'], '-', lw=2, color=color, label=label + ' P(|1⟩)')
    ax.plot(t_us, r['coherencia'], '--', lw=2, color=color, alpha=0.6,
            label=label + ' |ρ₀₁|')

axes[0].set_xlabel('Tiempo (μs)')
axes[0].set_ylabel('Probabilidad / Coherencia')
axes[0].set_title('Dinámica de decoherencia T1/T2')
axes[0].legend(fontsize=8)
axes[0].grid(alpha=0.3)

# Comparación T1 y T2 vs años
años = [2010, 2013, 2016, 2019, 2022, 2024]
T1_us = [1, 5, 30, 80, 150, 300]
T2_us = [1, 5, 25, 60, 200, 350]

axes[1].semilogy(años, T1_us, 'b-o', lw=2, ms=7, label='T1 (μs)')
axes[1].semilogy(años, T2_us, 'r-s', lw=2, ms=7, label='T2 (μs)')
axes[1].set_xlabel('Año')
axes[1].set_ylabel('Tiempo de coherencia (μs)')
axes[1].set_title('Evolución histórica de T1 y T2 en transmons')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## Termalización: el estado de Gibbs

A temperatura T, el sistema converge al estado de Gibbs:

$$
\rho_{eq} = \frac{e^{-H/k_BT}}{\text{tr}(e^{-H/k_BT})}
$$

```python
def estado_gibbs(H: np.ndarray, T_K: float) -> np.ndarray:
    """
    Estado de Gibbs ρ = exp(-H/kT) / Z para temperatura T_K en Kelvin.
    H en unidades de energía (eV, JouleS, etc. — consistente con kB).
    Para transmons: H en frecuencia, kB·T en frecuencia.
    """
    kB = 1.0  # unidades reducidas
    rho_unorm = expm(-H / (kB * T_K))
    return rho_unorm / rho_unorm.trace()

# Transmon: separación de energía ωq/(2π) = 5 GHz
# kB·T a temperatura de dilución: 20 mK → kBT ≈ 0.4 GHz
omega_q = 5.0   # GHz
kBT     = 0.4   # GHz (20 mK)

H_qubit = (omega_q / 2) * Z  # en unidades de GHz

rho_gibbs = estado_gibbs(H_qubit, T_K=kBT)
print(f'Estado de Gibbs a T={kBT/0.02:.0f} mK (kBT={kBT} GHz):')
print(f'  P(|0⟩) = {rho_gibbs[0,0].real:.6f}')
print(f'  P(|1⟩) = {rho_gibbs[1,1].real:.6f}')
print(f'  Población térmica del estado |1⟩: {rho_gibbs[1,1].real*100:.4f}%')
print(f'  (Con enfriamiento activo se puede reducir a < 0.1%)')

# Simulación de termalización Lindblad hacia Gibbs
def operadores_termalizacion(gamma_up: float, gamma_down: float):
    """
    Operadores de salto para termalización a temperatura finita.
    gamma_down = γ₁ · n_th (absorción del baño)
    gamma_up   = γ₁ · (n_th + 1) (emisión al baño)
    donde n_th = 1/(exp(ω/kBT) - 1)
    """
    n_th = 1 / (np.exp(omega_q / kBT) - 1) if kBT > 0 else 0
    gamma_base = 1 / 50.0  # 1/T1 en GHz

    g_down = gamma_base * (n_th + 1)
    g_up   = gamma_base * n_th
    return [(g_down, sigma_minus), (g_up, sigma_plus)]

ops_term = operadores_termalizacion(0, 0)

# Empezar en estado excitado y termalizarlo
rho_excitado = np.array([[0, 0], [0, 1]], dtype=complex)
t_term, hist_term = integrar_lindblad(rho_excitado, H_qubit, ops_term,
                                        t_max=200, dt=0.5)
P1_term = np.array([r[1,1].real for r in hist_term])

print(f'\nTermalización: P(|1⟩) final = {P1_term[-1]:.6f}')
print(f'Estado de Gibbs esperado:      {rho_gibbs[1,1].real:.6f}')
```

---

## Ecuación de Lindblad en superespacio

Para circuitos cuánticos, la ecuación de Lindblad se puede vectorizar
usando el **superoperador** (Liouvilliano):

$$
\frac{d|\rho\rangle\rangle}{dt} = \mathcal{L}|\rho\rangle\rangle
$$

donde $|\rho\rangle\rangle$ es el vector densidad en la representación de espacio de Liouville.

```python
def liouvilliano(H: np.ndarray,
                  ops: list[tuple[complex, np.ndarray]]) -> np.ndarray:
    """
    Calcula la supermatriz Liouvilliana L tal que dρ/dt = L·vec(ρ).
    Dimensión: (d²×d²) para d×d sistema.
    """
    d = H.shape[0]
    I_d = np.eye(d, dtype=complex)

    # Parte coherente: -i[H,ρ] → -i(H⊗I - I⊗H^T)
    L = -1j * (np.kron(H, I_d) - np.kron(I_d, H.T))

    # Parte disipativa: para cada L_k
    for gamma, Lk in ops:
        Ld = Lk.conj().T
        LdL = Ld @ Lk
        L += gamma * (np.kron(Lk, Lk.conj())
                      - 0.5 * np.kron(I_d, LdL.T)
                      - 0.5 * np.kron(LdL, I_d))

    return L

def evolucionar_liouvilliano(rho0: np.ndarray, L: np.ndarray,
                               t_vals: np.ndarray) -> list[np.ndarray]:
    """Evoluciona ρ(t) = exp(L·t) · vec(ρ0)."""
    d = rho0.shape[0]
    rho_vec0 = rho0.flatten()
    historico = []
    for t in t_vals:
        rho_vec_t = expm(L * t) @ rho_vec0
        rho_t = rho_vec_t.reshape(d, d)
        historico.append(rho_t)
    return historico

# Ejemplo: decaimiento T1 + desfase puro T_phi
T1_us, T2_us = 100e-6, 80e-6
T_phi = 1 / (1/T2_us - 1/(2*T1_us))
gamma1, gamma_phi = 1/T1_us, 1/T_phi

H_z = 0 * Z  # sin drive
ops_full = [(gamma1, sigma_minus), (gamma_phi/2, Z)]

L = liouvilliano(H_z, ops_full)

# Eigenvalores del Liouvilliano = tasas de decaimiento
eigenvals = np.linalg.eigvals(L)
eigenvals_sorted = sorted(eigenvals, key=lambda x: abs(x.real))

print('Eigenvalores del Liouvilliano (tasas de decaimiento):')
print(f'  λ₀ = 0 (estado estacionario)')
for ev in eigenvals_sorted[1:]:
    if abs(ev.real) > 1e-12:
        tau = -1/ev.real if ev.real < 0 else np.inf
        print(f'  λ = {ev:.4e}  (τ ≈ {tau*1e6:.2f} μs)')
```

---

## Dinámica en el régimen de acoplamiento fuerte: modelo de Jaynes-Cummings

El Hamiltoniano de Jaynes-Cummings describe un qubit acoplado a un modo de cavidad:

$$
H_{JC} = \omega_c a^\dagger a + \frac{\omega_q}{2}\sigma_z + g(a\sigma_+ + a^\dagger\sigma_-)
$$

```python
def hamiltonian_jaynes_cummings(omega_c: float, omega_q: float,
                                  g: float, n_fock: int = 5) -> np.ndarray:
    """
    Hamiltoniano de Jaynes-Cummings en espacio de Fock truncado.

    n_fock: número máximo de fotones en la cavidad.
    Espacio: |n⟩_cavidad ⊗ |q⟩_qubit, dim = 2*n_fock
    """
    d_cav = n_fock
    d_tot = 2 * d_cav

    # Operador de aniquilación del modo cavidad
    a = np.zeros((d_cav, d_cav), dtype=complex)
    for i in range(1, d_cav):
        a[i-1, i] = np.sqrt(i)
    ad = a.conj().T

    # Identidades
    I_cav  = np.eye(d_cav, dtype=complex)
    I_qubit = np.eye(2, dtype=complex)

    # Hamiltoniano
    H_cav  = omega_c * np.kron(ad @ a, I_qubit)
    H_qubit = (omega_q / 2) * np.kron(I_cav, Z)
    H_int  = g * (np.kron(a, sigma_plus) + np.kron(ad, sigma_minus))

    return H_cav + H_qubit + H_int

# Parámetros típicos de cQED (circuit QED)
omega_c = 2*np.pi * 6.0   # GHz
omega_q = 2*np.pi * 5.0   # GHz
g       = 2*np.pi * 0.1   # GHz (acoplamiento fuerte: g >> κ, γ)

H_jc = hamiltonian_jaynes_cummings(omega_c, omega_q, g, n_fock=5)
E_jc = np.linalg.eigvalsh(H_jc)

print('Espectro Jaynes-Cummings (n_fock=5):')
print(f'  Energías (unidades: GHz·2π):')
for i, E in enumerate(E_jc[:6]):
    print(f'    E_{i} = {E/(2*np.pi):.4f} GHz')

# Splitting de vacío (vacuum Rabi splitting)
vrs = 2 * g / (2*np.pi)
print(f'\n  Vacuum Rabi splitting: 2g = {vrs:.3f} GHz')
print(f'  Condición acoplamiento fuerte: 2g >> κ, γ')
```

---

## Resumen: parámetros de decoherencia y su origen físico

| Canal | Operador L_k | Origen físico | Control |
|-------|-------------|---------------|---------|
| Relajación T1 | σ₋ | Emisión espontánea al entorno | Distancia al sustrato, geometría |
| Desfase puro T_φ | σ_z | Ruido de 1/f en flux/carga | Puntos dulces, diseño del qubit |
| Dispersión de fotones | a | Pérdidas de la cavidad | Factor Q del resonador |
| Absorción térmica | σ₊ | Temperatura efectiva del entorno | Enfriamiento, filtros |
| Error de medición | — | Amplificador cuántico | Amplificadores paramétricos |

```python
print('\nTabla de T1 en distintas plataformas hardware (2024):')
print(f'{"Plataforma":>25} | {"T1 típico":>12} | {"T2 típico":>12} | {"Año récord"}')
print('-' * 65)
plataformas = [
    ('Transmon (SC)',      '100-400 μs', '150-500 μs', '2024'),
    ('Fluxonium (SC)',     '1-10 ms',    '200-500 μs', '2024'),
    ('Iones atrapados',   '10-100 s',   '1-10 s',     '2023'),
    ('Spin electrón Si',  '10-100 ms',  '1-100 ms',   '2024'),
    ('NV center en C',    '1-10 ms',    '1-10 ms',    '2022'),
    ('Átomo neutral Rydberg', '100-500 ms', '1-100 ms', '2023'),
]
for nombre, t1, t2, año in plataformas:
    print(f'{nombre:>25} | {t1:>12} | {t2:>12} | {año}')
```

---

**Referencias:**
- Lindblad, *Comm. Math. Phys.* 48, 119 (1976) — ecuación maestra
- Breuer & Petruccione, *The Theory of Open Quantum Systems* (2002) — referencia canónica
- Krantz et al., *Appl. Phys. Rev.* 6, 021318 (2019) — decoherencia en transmons
- Blais et al., *Rev. Mod. Phys.* 93, 025005 (2021) — cQED, JC, Lindblad
