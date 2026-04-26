# Aplicaciones de Quantum Sensing

**Módulo 38 · Artículo 2 · Nivel muy avanzado**

---

## Gravímetros cuánticos: midiendo g con átomos

Los interferómetros atómicos de materia (átomos de Rb o Cs lanzados como fuente de
onda) miden la aceleración gravitacional con sensibilidad de 10⁻⁹ g.

```python
import numpy as np
import matplotlib.pyplot as plt

# Interferómetro atómico tipo Mach-Zehnder (secuencia π/2 - π - π/2)
# La fase acumulada es: Φ = k_eff · g · T²
# k_eff = 2k_laser (doble fotón), T = tiempo entre pulsos

def fase_gravimetro(g: float, k_eff: float, T: float) -> float:
    """Fase interferométrica: Φ = k_eff · g · T²"""
    return k_eff * g * T**2

def sensibilidad_gravimetro(k_eff: float, T: float, C: float,
                             N: float, tau: float) -> float:
    """
    Sensibilidad de un gravímetro atómico.
    
    δg = 1 / (k_eff · T² · C · √(N · tau))
    
    C: contraste de la franja (0-1)
    N: átomos por ciclo
    tau: tiempo de integración (s)
    """
    return 1 / (k_eff * T**2 * C * np.sqrt(N * tau))

# Parámetros típicos (Rb-87, doble fotón Raman)
lambda_laser = 780e-9  # m (Rb-87 D2)
k_eff = 2 * 2 * np.pi / lambda_laser
g0 = 9.80665  # m/s²

T_vals = np.array([0.01, 0.05, 0.1, 0.2, 0.5])  # s
N_atm = 1e6   # átomos
C = 0.5       # contraste típico
tau = 1.0     # 1 segundo de integración

print('Parámetros del gravímetro cuántico (Rb-87, Raman):')
print(f'k_eff = {k_eff:.3e} m⁻¹')
print(f'\n{"T (s)":>8} | {"Δg (µGal)":>12} | {"Δg/g":>12}')
print('-' * 38)
for T in T_vals:
    delta_g = sensibilidad_gravimetro(k_eff, T, C, N_atm, tau)
    print(f'{T:>8.3f} | {delta_g*1e8:>12.2f} | {delta_g/g0:>12.2e}')

# 1 μGal = 10⁻⁸ m/s² — referencia: variación de g por 3 cm de altura ≈ 1 μGal

# Gráfica: sensibilidad vs tiempo de vuelo T
T_range = np.logspace(-2, 0, 200)
sens_vals = [sensibilidad_gravimetro(k_eff, T, 0.5, 1e6, 1.0) for T in T_range]

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].loglog(T_range, np.array(sens_vals) * 1e8, 'b-', lw=2)
axes[0].axhline(1,   color='red',   ls='--', label='1 μGal (variación: +3 cm)')
axes[0].axhline(0.1, color='green', ls='--', label='0.1 μGal (objetivo FT)')
axes[0].set_xlabel('Tiempo de vuelo T (s)')
axes[0].set_ylabel('Sensibilidad (μGal/√Hz)')
axes[0].set_title('Sensibilidad del gravímetro cuántico vs T')
axes[0].legend(fontsize=9)
axes[0].grid(alpha=0.3, which='both')

# Aplicaciones: mapa gravitacional
x = np.linspace(0, 10, 100)
y = np.linspace(0, 10, 100)
X, Y = np.meshgrid(x, y)

# Perturbación gravitacional de un objeto masivo enterrado
# Δg ∝ ρ·V / r² (simplificado)
def delta_g_subsurface(X, Y, x0, y0, depth, mass_contrast):
    r = np.sqrt((X - x0)**2 + (Y - y0)**2 + depth**2)
    return mass_contrast * 6.674e-11 / r**2

g_map = delta_g_subsurface(X, Y, 5, 5, 2, 1e10)
g_map += 0.02 * np.random.randn(*X.shape)  # ruido sensor

im = axes[1].contourf(X, Y, g_map * 1e8, levels=20, cmap='RdBu_r')
plt.colorbar(im, ax=axes[1], label='Δg (μGal)')
axes[1].set_title('Mapa gravitacional cuántico (objeto enterrado a 2 m)')
axes[1].set_xlabel('x (m)'); axes[1].set_ylabel('y (m)')

plt.tight_layout()
plt.show()
```

---

## Navegación inercial cuántica

Los acelerómetros e giróscopos cuánticos pueden reemplazar los sistemas GPS
en entornos sin señal (submarinos, espacio profundo, interiores).

```python
comparativa_inercial = """
SISTEMAS DE NAVEGACIÓN INERCIAL: CUÁNTICO vs CLÁSICO
═══════════════════════════════════════════════════════════════════

GIRÓSCOPO LÁSER (CLÁSICO — REFERENCIA):
  Deriva: ~0.01°/h (sistemas militares top)
  Sensibilidad: ~10⁻⁸ rad/s/√Hz
  Tecnología: interferómetro Sagnac con láser
  Coste: $10-100k

GIRÓSCOPO CUÁNTICO (ATOM INTERFEROMETER):
  Deriva: ~0.0001°/h (demostrado en lab, 2022)
  Sensibilidad: ~6×10⁻¹⁰ rad/s/√Hz (100× mejor)
  Tecnología: átomos Rb lanzados en bucle cuadrado (área A)
  Fase Sagnac: Φ_Sagnac = 2m·Ω·A / ħ
  Coste actual: $1M+ (lab), objetivo <$100k (2030)

GIRÓSCOPO NV-CENTER:
  Detecta campo magnético de la rotación terrestre
  Sensibilidad: ~1 nrad/s/√Hz (actual), 1 prad/s/√Hz (objetivo)
  Ventaja: estado sólido, funciona a temperatura ambiente
  Desventaja: necesita escudado magnético

ACELERÓMETRO CUÁNTICO vs CLÁSICO:
  Clásico MEMS:  δa ~ 10⁻⁶ g/√Hz  (IMU comercial)
  Clásico criog: δa ~ 10⁻⁹ g/√Hz  (GRACE Follow-On)
  Cuántico (lab): δa ~ 10⁻¹⁰ g/√Hz (factor 10 mejor)

DERIVA DE NAVEGACIÓN ACUMULADA (sin GPS):
  MEMS comercial:  ~1 km/h de deriva
  INS militar top: ~1 m/h de deriva
  Cuántico (2030): ~1 mm/h de deriva (objetivo)
"""
print(comparativa_inercial)
```

---

## LIGO y los límites cuánticos de la óptica

El interferómetro LIGO mide desplazamientos de 10⁻¹⁹ m — más pequeño que un
protón — usando luz en un estado cuántico especial (squeezed light).

```python
import numpy as np
import matplotlib.pyplot as plt

def ruido_shot_ligo(P_laser: float, lambda_: float,
                     eta: float = 0.9) -> float:
    """
    Ruido shot (imprecisión cuántica) de un interferómetro óptico.
    
    δx_shot = √(ħω / 2ηP) / (ω/c · L_bragg)
    Simplificado: δx ~ λ/(2π) · 1/√(N_ph)
    
    P_laser: potencia en cavidad (W)
    lambda_: longitud de onda (m)
    eta: eficiencia de detección
    """
    hbar = 1.055e-34
    omega = 2 * np.pi * 3e8 / lambda_
    N_ph_per_s = eta * P_laser / (hbar * omega)
    return lambda_ / (2 * np.pi * np.sqrt(N_ph_per_s))

def ruido_radiacion_ligo(P_laser: float, lambda_: float,
                          m_mirror: float, f: float) -> float:
    """
    Ruido de presión de radiación (back-action cuántico).
    
    δx_BA = (ħω/(c·λ)) · 1/(m·(2πf)²) · √(P/ħω)
    """
    hbar = 1.055e-34
    omega = 2 * np.pi * 3e8 / lambda_
    return np.sqrt(hbar * P_laser / omega) / (m_mirror * (2 * np.pi * f)**2 * 3e8 / lambda_)

# Parámetros LIGO O4
lambda_LIGO = 1064e-9   # m
P_circulante = 250e3    # W (potencia en cavidad)
m_espejo = 40.0         # kg
eta = 0.9

freqs = np.logspace(1, 3, 200)  # 10-1000 Hz

shot_noise   = ruido_shot_ligo(P_circulante, lambda_LIGO, eta) * np.ones_like(freqs)
ba_noise     = np.array([ruido_radiacion_ligo(P_circulante, lambda_LIGO, m_espejo, f) for f in freqs])
total_noise  = np.sqrt(shot_noise**2 + ba_noise**2)

# Con squeezed light: reduce shot por factor e^(-r), aumenta BA por e^r (óptimo r~10 dB)
r_squeeze = np.log(10**(10/20))  # 10 dB de squeezing
shot_sq  = shot_noise * np.exp(-r_squeeze)
ba_sq    = ba_noise * np.exp(r_squeeze)
total_sq = np.sqrt(shot_sq**2 + ba_sq**2)

fig, ax = plt.subplots(figsize=(10, 6))
ax.loglog(freqs, shot_noise * 1e21,  'b--', lw=1.5, alpha=0.7, label='Shot noise (sin squeeze)')
ax.loglog(freqs, ba_noise * 1e21,    'r--', lw=1.5, alpha=0.7, label='Back-action (sin squeeze)')
ax.loglog(freqs, total_noise * 1e21, 'b-',  lw=2.5, label='Total (sin squeeze)')
ax.loglog(freqs, total_sq * 1e21,    'g-',  lw=2.5, label='Total (10 dB squeezed light)')
ax.set_xlabel('Frecuencia (Hz)')
ax.set_ylabel('Sensibilidad (m/√Hz) × 10²¹')
ax.set_title('LIGO: límites cuánticos y squeezed light')
ax.legend(fontsize=9)
ax.grid(alpha=0.3, which='both')
ax.set_xlim(10, 1000)
plt.tight_layout()
plt.show()

print(f'\nSQL de posición para LIGO:')
print(f'  Ruido shot (sin squeeze):  {shot_noise[0]*1e21:.2f} × 10⁻²¹ m/√Hz')
print(f'  Ruido shot (10dB squeeze): {shot_sq[0]*1e21:.2f} × 10⁻²¹ m/√Hz')
print(f'  Reducción de ruido: {shot_noise[0]/shot_sq[0]:.1f}×')
```

---

## Radar cuántico: mito vs realidad

```python
radar_cuantico_debate = """
RADAR CUÁNTICO: EVALUACIÓN HONESTA 2024
═══════════════════════════════════════════════════════════════════

PROPUESTA ORIGINAL (Lloyd 2008):
  Usar pares EPR de fotones (signal + idler) para iluminar objetivos.
  La correlación cuántica permite detectar el objetivo con menos fotones
  que el radar clásico → ventaja en entornos ruidosos (AWGN).

RESULTADOS TEÓRICOS:
  → Ventaja cuántica teórica: SNR_quantum / SNR_clásico ≈ e^(2r) - 1
    donde r es el parámetro de squeezing (r ~ 1 → ventaja ~6 dB)
  → Requiere preservar correlaciones cuánticas durante viaje ida/vuelta

PROBLEMAS EXPERIMENTALES:
  ❌ Decoherencia: los fotones pierden correlaciones en ~1 cm en aire
     (choque con moléculas cada ~65 nm a presión atmosférica)
  ❌ Temperatura: a 300 K, el ruido térmico de RF domina totalmente
     sobre correlaciones cuánticas de un par de fotones
  ❌ Rango: demostraciones experimentales: distancias de cm, no km
  ❌ Frecuencia: la ventaja teórica requiere microondas (<10 GHz),
     donde la longitud de onda impide resolución angular útil

EXPERIMENTOS REALES (2020-2024):
  → Shapiro et al. (MIT): ventaja cuántica demostrada a 1 metro, 7 GHz
    en condiciones de laboratorio con ruido térmico reducido
  → Barzanjeh et al. (IST Austria 2020): primer radar cuántico
    de microondas, funcionamiento a 20 mK (criogénico)
  → Luong et al. (2020): radar cuántico de 2 GHz, rango de 1 m

CONCLUSIÓN HONESTA:
  ┌────────────────────────────────────────────────────────────┐
  │ El radar cuántico tiene fundamento teórico sólido, pero   │
  │ sus ventajas son ~6 dB en condiciones extremadamente       │
  │ favorables. La decoherencia ambiental elimina la ventaja  │
  │ en condiciones de campo real (temperatura, rango > 1 m).  │
  │ No es una tecnología de defensa viable en el horizonte    │
  │ de 10-15 años con la física actual.                       │
  └────────────────────────────────────────────────────────────┘
"""
print(radar_cuantico_debate)
```

---

**Referencias:**
- Giovannetti, Lloyd, Maccone, *Phys. Rev. Lett.* 96, 010401 (2006) — SQL vs HL
- Peters, Chung, Chu, *Nature* 400, 849 (1999) — primer gravímetro atómico
- Gustavson, Bouyer, Kasevich, *PRL* 78, 2046 (1997) — giróscopo atómico
- Tse et al. (*LIGO*), *PRL* 123, 231107 (2019) — squeezed light en LIGO
- Barzanjeh et al., *Science Advances* 6, eabb0451 (2020) — radar cuántico
