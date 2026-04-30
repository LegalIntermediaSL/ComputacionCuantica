# Módulo 44 — Computación Cuántica Distribuida: Repetidores y Redes

Este módulo cubre la arquitectura y los protocolos necesarios para construir redes cuánticas de largo alcance: desde la purificación de Bell pairs hasta los repetidores cuánticos de segunda y tercera generación.

---

## Índice

1. [Por qué hace falta la DQC](#1-motivacion)
2. [Bell pairs sobre canal ruidoso](#2-bell-pairs)
3. [Purificación: BBPSSW y DEJMPS](#3-purificacion)
4. [Repetidores cuánticos de primera generación](#4-repetidores-1g)
5. [Repetidores de segunda y tercera generación](#5-repetidores-2g-3g)
6. [Quantum memory: fidelidad vs tiempo](#6-memoria)
7. [MDI-QKD y TF-QKD](#7-mdi-tf-qkd)
8. [Métricas de red cuántica](#8-metricas)
9. [Hoja de ruta: SEQC / QuICnet 2025-2035](#9-hoja-de-ruta)
10. [Conexiones con módulos anteriores](#10-conexiones)

---

## 1. Motivación — ¿Por qué DQC? {#1-motivacion}

Un procesador cuántico monolítico enfrenta dos barreras físicas:

1. **Escala de conectividad:** los errores de puerta de 2 qubits crecen con la distancia física en el chip. Un surface code de distancia d=31 requiere ~2000 qubits físicos — más de lo que tienen los chips actuales con fidelidad útil.

2. **Decoherencia vs tamaño:** aumentar el número de qubits físicos en un solo criostato aumenta el crosstalk y la disipación. La alternativa es **modularizar**: varios procesadores pequeños y altamente coherentes conectados por enlaces cuánticos.

```
┌─────────────────────────────────────────────────────────┐
│           Red cuántica distribuida (visión)             │
│                                                         │
│  [QPU A]──────Bell pairs──────[QPU B]                   │
│     │                            │                      │
│  Memoria                      Memoria                   │
│  cuántica                     cuántica                  │
│     │                            │                      │
│  [QPU C]──────Bell pairs──────[QPU D]                   │
│                                                         │
│  Operaciones lógicas entre QPU via teleportación        │
└─────────────────────────────────────────────────────────┘
```

**Protocolos clave que necesitamos:**
- Generar Bell pairs de alta fidelidad entre nodos distantes
- Purificarlos cuando la fidelidad es insuficiente
- Almacenarlos en memorias cuánticas mientras esperamos el resto de la red
- Ejecutar gates no locales via teleportación de estado o gate teleportation

---

## 2. Bell Pairs sobre Canal Ruidoso {#2-bell-pairs}

### El canal de fibra óptica

La atenuación de la fibra óptica es ~0.2 dB/km a 1550 nm. Para 100 km:

```
Transmisividad: η = 10^(-0.2 × 100 / 10) = 10^(-2) = 1%
```

Esto significa que solo 1 de cada 100 fotones llega. No se puede amplificar clásicamente (el teorema de no-clonación lo prohíbe).

### Estado Werner: modelo de ruido para Bell pairs

El estado Werner con parámetro F (fidelidad con el estado de Bell |Φ⁺⟩) es:

```
ρ_W(F) = F |Φ⁺⟩⟨Φ⁺| + (1-F)/3 (|Φ⁻⟩⟨Φ⁻| + |Ψ⁺⟩⟨Ψ⁺| + |Ψ⁻⟩⟨Ψ⁻|)
```

En forma matricial en la base {|00⟩, |01⟩, |10⟩, |11⟩}:

```
        ⎡(1+2F)/4    0         0      (2F-1)/4 ⎤
ρ_W  =  ⎢   0     (1-F)/4     0         0     ⎥
        ⎢   0        0      (1-F)/4      0     ⎥
        ⎣(2F-1)/4   0         0      (1+2F)/4 ⎦
         (×1/... normalización implícita)
```

Para F = 1 → estado puro |Φ⁺⟩. Para F = 1/4 → estado maximalmente mezclado.

**Umbral de entrelazamiento:** F > 1/2 es necesario para que el estado sea entrelazado (violación de desigualdad de Bell requiere F > (1+1/√2)/2 ≈ 0.853).

### Generación de Bell pairs: protocolo de emisión con fotón

```
Nodo A                        Canal                      Nodo B
  │                             │                           │
  ├─ |ψ⟩_A ─── CNOT ──────────────── fotón entrelazado ───►│
  │           └─ qubit_A                                    │
  │                                                 Bell measurement
  │◄────────────────── resultado clásico ─────────────────  │
  │                                                         │
  └─ corrección local ──────────────────────────────────────┘
```

La fidelidad degrada con la distancia L:
```
F(L) ≈ 1 - (1 - F_0) × L / L_0
```
donde L_0 ~ 20 km es la longitud de coherencia típica en fibra y F_0 la fidelidad de la fuente.

---

## 3. Purificación: BBPSSW y DEJMPS {#3-purificacion}

La purificación toma **dos pares de baja fidelidad** y produce **un par de mayor fidelidad** consumiendo el otro.

### Protocolo BBPSSW (Bennett et al. 1996)

```
Entrada:  ρ₁ ⊗ ρ₂  con fidelidad F₁ = F₂ = F
Salida:   ρ' con fidelidad F' > F  (con probabilidad P_éxito)
```

**Circuito:**

```
Nodo A:                           Nodo B:
|a₁⟩ ──── CNOT ────── M_Z         |b₁⟩ ──── CNOT ────── M_Z
|a₂⟩ ──── (ctrl) ─────────        |b₂⟩ ──── (ctrl) ─────────
                                    │
                    comparar resultados via canal clásico
```

Si ambos resultados son iguales (éxito), el par (a₁, b₁) tiene fidelidad:

```
F'_BBPSSW = F² + ((1-F)/3)²
             ─────────────────────────────
             F² + 2F(1-F)/3 + 5((1-F)/3)²

P_éxito = F² + 2F(1-F)/3 + 5((1-F)/3)²
```

Para F = 0.75:
- F' ≈ 0.856
- P_éxito ≈ 0.594

### Protocolo DEJMPS (Deutsch et al. 1996)

DEJMPS aplica rotaciones locales antes de los CNOT para maximizar F' para estados Werner:

```python
# Circuito DEJMPS (Nodo A)
def dejmps_nodo_a(qc, a1, a2):
    qc.ry(np.pi / 2, a1)   # rotación σy en qubit de trabajo
    qc.cx(a1, a2)           # CNOT: a1 controla a2
    qc.ry(-np.pi / 2, a1)  # rotación inversa
    qc.measure(a2, ...)     # medir qubit sacrificado

# Circuito DEJMPS (Nodo B) — rotación opuesta
def dejmps_nodo_b(qc, b1, b2):
    qc.ry(-np.pi / 2, b1)
    qc.cx(b1, b2)
    qc.ry(np.pi / 2, b1)
    qc.measure(b2, ...)
```

Fidelidad tras una ronda DEJMPS para estado Werner(F):

```
F'_DEJMPS = (F² + ((1-F)/3)²) / P_éxito

P_éxito = F² + 2F(1-F)/3 + 5((1-F)/3)²  ← igual que BBPSSW
```

**DEJMPS supera a BBPSSW** para F < 0.5 (estados menos puros) gracias a las rotaciones locales que reorientan el ruido antes de la medición.

### Convergencia iterativa

Aplicando k rondas de purificación:

```
F_0 = 0.60 → F_1 = 0.72 → F_2 = 0.83 → F_3 = 0.92 → F_4 = 0.97 → ...
```

Cada ronda consume la mitad de los pares. Para llegar de F=0.6 a F>0.99 se necesitan ~5 rondas, consumiendo 2⁵ = 32 pares originales por par purificado.

```python
def fidelidad_bbpssw(F):
    """Una ronda BBPSSW: devuelve (F', P_exito)."""
    p = (1 - F) / 3
    num = F**2 + p**2
    denom = F**2 + 2*F*p + 5*p**2
    return num / denom, denom

def simular_purificacion(F0, n_rondas):
    F = F0
    pares_consumidos = 1
    for k in range(n_rondas):
        F, P = fidelidad_bbpssw(F)
        pares_consumidos *= 2
        print(f"  Ronda {k+1}: F = {F:.4f}, P_éxito = {P:.4f}, "
              f"pares originales consumidos = {pares_consumidos}")
    return F
```

---

## 4. Repetidores Cuánticos de Primera Generación {#4-repetidores-1g}

### El problema de la distancia

Sin repetidores, la tasa de generación de Bell pairs cae exponencialmente:

```
R(L) ∝ η(L) = 10^(-αL/10)   [pares/s]
```

Para 1000 km con α = 0.2 dB/km: R ∝ 10^(-20) ≈ 10^(-20) por segundo — inútil.

### Arquitectura de repetidor de 1G (Briegel-Dür-Cirac-Zoller, 1998)

La idea central: dividir el enlace en N segmentos más cortos, generar entrelazamiento local y luego **swapear** (entanglement swapping) para extenderlo.

```
A ──[M₁]────[M₂]────[M₃]────[M₄]── B
   L/N     L/N     L/N     L/N

Paso 1: generar Bell pair en cada segmento A-M₁, M₁-M₂, ...
Paso 2: entanglement swap en M₁: Bell measurement en (qubit_A, qubit_M₂)
        → A queda entrelazado con M₂
Paso 3: repetir hasta A ↔ B
```

**Entanglement swapping:** si (A, M) y (M, B) son Bell pairs,
una medición de Bell en los dos qubits de M produce una Bell pair entre A y B.

```python
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def entanglement_swap():
    """Circuito de entanglement swapping: (a,m1) y (m2,b) → (a,b)."""
    qr = QuantumRegister(4, 'q')  # a, m1, m2, b
    cr = ClassicalRegister(2, 'c')
    qc = QuantumCircuit(qr, cr)

    # Preparar Bell pair (a, m1)
    qc.h(qr[0]); qc.cx(qr[0], qr[1])
    # Preparar Bell pair (m2, b)
    qc.h(qr[2]); qc.cx(qr[2], qr[3])

    # Bell measurement en (m1, m2) — el swap
    qc.cx(qr[1], qr[2])
    qc.h(qr[1])
    qc.measure(qr[1], cr[0])
    qc.measure(qr[2], cr[1])

    # Corrección de Pauli en b según resultado
    with qc.if_else((cr[0], 1)):
        qc.x(qr[3])
    with qc.if_else((cr[1], 1)):
        qc.z(qr[3])

    return qc
```

### Tasa de generación con N segmentos

La tasa con N segmentos y memoria perfecta es:

```
R_N(L) ∝ η(L/N)^(1/2) / N   [pares/s]

Optimizando N: N_opt ≈ √(αL / (2 ln 2))
R_max ∝ exp(-√(αL × 2 ln 2))   → exponencial atenuada a sub-exponencial
```

Para L = 1000 km, N_opt ≈ 10-20 repetidores, mejora de ~10^10 sobre sin repetidores.

---

## 5. Repetidores de Segunda y Tercera Generación {#5-repetidores-2g-3g}

### Generación 1G — Limitaciones

- Requiere muchas rondas de purificación (memoria cuántica usada muchas veces)
- La fidelidad de la memoria degrada: F(t) ≈ e^(-t/T_mem)
- Throughput limitado por la latencia del canal clásico (ida y vuelta ~ L/c)

### Generación 2G — Memoria + QEC local

En lugar de purificar par a par, cada nodo almacena los qubits en un **código corrector de errores** local:

```
Nodo repetidor 2G:
  ├── Interfaz óptica (fotones) ────────── genera Bell pairs raw
  ├── Conversión de frecuencia (1550nm → frecuencia de memoria)
  ├── Memoria cuántica (NV en diamante, iones de tierras raras)
  │     T_mem ~ segundos a minutos
  └── QPU local (corrección de errores + medición de Bell)
```

El QEC local tolera errores de memoria sin consumir más pares, reduciendo el overhead de purificación de exponencial a polinomial.

### Generación 3G — Fallo tolerante, sin comunicación clásica de ida/vuelta

Los repetidores de 3G usan **teleportación basada en QEC** sin esperar confirmación clásica:

```
Tasa teórica 3G: R(L) ∝ 1/L   (solo atenuación lineal, sin overhead exponencial)
```

**Plataformas candidatas para 3G:**
- NV en diamante: T₂ ~ 1 s (temperatura ambiente), pero baja eficiencia de emisión fotónica (~3%)
- Iones de Er³⁺ en cristal: T₂ ~ 6 s, compatible con fibra (1550 nm)
- Átomos neutrales en cavidades: T₂ ~ 100 s, alta eficiencia (>90%)

---

## 6. Quantum Memory: Fidelidad vs Tiempo {#6-memoria}

### Modelo de decoherencia de memoria

Una memoria cuántica con tiempo de coherencia T₂ evoluciona como un canal de dephasing:

```
ρ(t) = (1 - p(t)) ρ(0) + p(t) Z ρ(0) Z†

p(t) = (1 - e^(-t/T₂)) / 2
```

La fidelidad con el estado inicial:

```
F(t) = ⟨ψ₀|ρ(t)|ψ₀⟩ = 1 - p(t) = (1 + e^(-t/T₂)) / 2
```

Para un estado de Bell almacenado en ambos qubits (decoherencia independiente):

```
F_Bell(t) ≈ ((1 + e^(-t/T₂)) / 2)²  ≈  e^(-2t/T₂)  para t << T₂
```

### Requisito de memoria para repetidor de N segmentos

El tiempo de espera máximo (esperando que todos los segmentos generen un par exitoso):

```
t_espera ≈ L/(N × c) × H_N   donde H_N = 1 + 1/2 + ... + 1/N ≈ ln(N) + γ_E
```

Requisito de memoria: T_mem >> t_espera ≈ (L/c) × ln(N) / N

Para L=1000 km, N=10, c=2×10⁸ m/s: t_espera ≈ 0.5 ms × 3.5 ≈ 2 ms → T_mem >> 2 ms.
En la práctica se necesita T_mem > 1 s para N practicable.

```python
import numpy as np

def fidelidad_memoria(t, T2):
    """Fidelidad de Bell pair almacenado durante tiempo t."""
    return ((1 + np.exp(-t / T2)) / 2)**2

def tiempo_espera_repetidor(L_km, N, c=2e5):
    """Tiempo esperado de espera (ms) para que N segmentos completen."""
    L_m = L_km * 1e3
    t_base = L_m / (N * c * 1e3)  # segundos
    H_N = sum(1/k for k in range(1, N+1))
    return t_base * H_N  # segundos

# Requisitos de memoria para distintas arquitecturas
print("Análisis de requisitos de memoria cuántica:")
print(f"{'N':>4} {'t_esp (ms)':>12} {'F_NV (T₂=1s)':>14} {'F_Er (T₂=6s)':>14}")
for N in [5, 10, 20, 50]:
    t = tiempo_espera_repetidor(1000, N)
    F_NV = fidelidad_memoria(t, T2=1.0)
    F_Er = fidelidad_memoria(t, T2=6.0)
    print(f"{N:>4} {t*1000:>12.2f} {F_NV:>14.4f} {F_Er:>14.4f}")
```

---

## 7. MDI-QKD y TF-QKD {#7-mdi-tf-qkd}

### Limitación de BB84 a distancia

BB84 estándar requiere que Alice envíe fotones directamente a Bob. La tasa cae como:

```
R_BB84 ∝ η(L) = 10^(-αL/10)
```

Además, un detector espía en el canal puede atacar ("detector side-channel attack").

### Measurement-Device-Independent QKD (MDI-QKD, Lo et al. 2012)

Elimina los ataques al detector moviendo la medición a un nodo intermedio sin confianza:

```
Alice ──── fotones ────► Charlie (sin confianza) ◄──── fotones ──── Bob
                               │
                        Bell measurement
                        (publica resultados)
```

Alice y Bob preparan estados BB84 independientemente. Charlie hace una medición de Bell y publica el resultado. Solo cuando la proyección es exitosa (~50%) Alice y Bob comparten una clave.

**Tasa:**
```
R_MDI ∝ η(L/2)²   → mejora vs η(L) pero sigue siendo sub-óptima
```

### Twin-Field QKD (TF-QKD, Lucamarini et al. 2018)

TF-QKD logra una tasa proporcional a η(L/2) en vez de η(L/2)² mediante interferencia de campo óptico:

```
R_TF ∝ √η(L/2) = √(10^(-αL/20))   → raíz cuadrada de la atenuación total
```

Esto rompe el **límite de repetidor sin memoria** (PLOB bound): ningún protocolo sin memoria cuántica puede superar √η(L).

```
Límite PLOB: -log₂(1-η) ≈ η / ln(2)   [bits/uso de canal]
TF-QKD logra: ~√η  → supera PLOB para L > ~200 km
```

**Implementaciones experimentales (2023-2025):**
- Toshiba/Cambridge: 605 km en fibra estándar, 2.7×10⁻⁴ bits/seg
- USTC: 1002 km con fibra ultra-baja pérdida (0.16 dB/km)

---

## 8. Métricas de Red Cuántica {#8-metricas}

### Tasa de generación de Bell pairs (BGR)

```
BGR [pares/s] = intentos/s × P_éxito × P_detección × P_memoria
```

- `intentos/s` ≈ repetición del láser (1 MHz típico)
- `P_éxito` ≈ η(L/N) para cada segmento
- `P_detección` ≈ eficiencia del detector (80-95% para SNSPDs)
- `P_memoria` ≈ eficiencia de escritura en memoria (30-90%)

### Fidelidad del enlace (Link Fidelity)

Fidelidad promedio del estado entrelazado distribuido, teniendo en cuenta:
1. Ruido del canal
2. Decoherencia de memoria durante t_espera
3. Errores de puertas locales (purificación, swap)

```
F_link = F_canal × F_mem(t_espera) × F_gate^N_gates
```

### Distancia cuántica efectiva

```
D_eff = max{L : BGR(L) > R_min  y  F_link(L) > F_min}
```

Valores típicos de umbral: R_min = 1 par/s, F_min = 0.90.

### Capacidad cuántica del canal

Para un canal depolarizante con parámetro de error p:

```
Q(p) = max(0, 1 - H(p) - p·log₂(3) - (1-p)·log₂(1-p))
```

Donde H(p) = -p·log₂(p) - (1-p)·log₂(1-p) es la entropía binaria.
Q(p) > 0 requiere p < p_th ≈ 0.189 (umbral de canal cuántico).

---

## 9. Hoja de Ruta: SEQC / QuICnet 2025-2035 {#9-hoja-de-ruta}

### Estado del arte 2025

| Plataforma | T_mem | Eficiencia de escritura | Integración fotónica |
|---|---|---|---|
| NV en diamante | ~1 s (300K), ~60 s (4K) | ~70% (4K) | Baja (emisión difusa) |
| Er³⁺:Y₂SiO₅ | ~6 s | ~90% | Compatible 1550 nm |
| Rb en celda cálida | ~1 ms | ~95% | Alta (cavidad) |
| Sr (reloj óptico) | ~100 s | ~99% | En desarrollo |
| Iones trampa (Ca⁺) | ~50 s | ~99.9% | Baja (requiere vacío) |

### Hoja de ruta SEQC (Quantum Internet Alliance)

```
2025: Entrelazamiento punto a punto fiable (F > 0.95, BGR > 100 pares/s)
      Demostración de repetidores 1G en lab (<10 km)

2027: Repetidores 1G en ciudad (<50 km), teleportación de estado
      QKD metropolitana MDI a 200+ km

2029: Repetidores 2G (QEC local), red de 3-5 nodos
      TF-QKD a 1000+ km reproducible

2032: Repetidores 3G, primera red cuántica nacional
      Computación distribuida entre QPUs separados > 100 km

2035: Internet cuántico continental (QuICnet Europe / US Quantum Internet)
      BQP distribuido: QPU + red > 1000 qubits lógicos efectivos
```

### Desafíos abiertos

1. **Transducción de frecuencia eficiente:** conversión microondas (superconductores) ↔ óptico (1550 nm) con < 1 fotón de ruido añadido. Mejor resultado 2024: eficiencia ~10⁻³.

2. **Interfaz spin-fotón en sólidos:** NV tiene baja eficiencia de emisión en cero-fonón (~3%). Alternativas: centros SiV (15%), defectos en hBN (~40%).

3. **Sincronización de relojes cuánticos:** los protocolos requieren sincronización sub-nanosegundo entre nodos distantes.

4. **Integración en chip:** pasar de setups ópticos en mesa a chips fotónicos integrados (PIC) con memorias, detectores y fuentes en el mismo chip.

---

## 10. Conexiones con módulos anteriores {#10-conexiones}

| Concepto | Módulo relacionado |
|---|---|
| Entrelazamiento y Bell states | Módulo 03 |
| Teleportación de estado cuántico | Módulo 03 |
| Corrección de errores (surface code) | Módulo 09, 29 |
| Canales de Kraus y decoherencia | Módulo 16 |
| Sistemas abiertos (Lindblad, T₁/T₂) | Módulo 21 |
| DQC básico (BB84, E91, BQC) | Lab 42 / Módulo 07 |
| QKD (BB84, CHSH, repetidores simples) | Lab 37 |
| Redes cuánticas avanzadas | Módulo 27 |
| Internet cuántico (hoja de ruta) | Módulo 37 |

### Código de ejemplo integrador: red de 3 nodos

```python
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
import numpy as np

def red_tres_nodos():
    """
    Red A-M-B: genera Bell pair A-M, Bell pair M-B,
    hace entanglement swap en M para obtener Bell pair A-B.
    Luego purifica si la fidelidad no es suficiente.
    """
    # 4 qubits: a (qubit de A), m1 (qubit de M para el par AM),
    #           m2 (qubit de M para el par MB), b (qubit de B)
    qr = QuantumRegister(4, 'q')
    cr = ClassicalRegister(4, 'c')
    qc = QuantumCircuit(qr, cr)

    # Paso 1: generar Bell pair (a, m1)
    qc.h(qr[0])
    qc.cx(qr[0], qr[1])

    # Paso 2: generar Bell pair (m2, b)
    qc.h(qr[2])
    qc.cx(qr[2], qr[3])

    qc.barrier()

    # Paso 3: entanglement swap en nodo M (Bell measurement en m1, m2)
    qc.cx(qr[1], qr[2])
    qc.h(qr[1])
    qc.measure(qr[1], cr[0])
    qc.measure(qr[2], cr[1])

    # Paso 4: correcciones de Pauli en B
    with qc.if_else((cr[0], 1)):
        qc.x(qr[3])
    with qc.if_else((cr[1], 1)):
        qc.z(qr[3])

    # Ahora (a, b) comparten un Bell pair

    # Verificar: medir en base Bell
    qc.cx(qr[0], qr[3])
    qc.h(qr[0])
    qc.measure(qr[0], cr[2])
    qc.measure(qr[3], cr[3])

    return qc


# El resultado esperado: cr[2] == cr[3] siempre (estado Bell)
qc = red_tres_nodos()
print(qc.draw('text'))
print(f"Profundidad del circuito: {qc.depth()}")
print(f"Operaciones: {qc.count_ops()}")
```

---

## Resumen

| Concepto | Fórmula clave |
|---|---|
| Estado Werner | ρ_W(F) = F|Φ⁺⟩⟨Φ⁺| + (1-F)/3 × resto |
| BBPSSW fidelidad | F' = (F² + p²) / (F² + 2Fp + 5p²), p=(1-F)/3 |
| Fidelidad memoria | F(t) = ((1+e^(-t/T₂))/2)² |
| Tasa repetidor 1G | R ∝ exp(-√(αL·2ln2)) vs R ∝ η(L) sin repetidores |
| Límite PLOB | C(η) ≈ η/ln2 bits/uso |
| TF-QKD | R ∝ √η(L/2) — supera PLOB sin memoria cuántica |
| Umbral canal cuántico | p < p_th ≈ 0.189 para Q(p) > 0 |

---

*Módulo 44 · Computación Cuántica Distribuida: Repetidores y Redes · v5.3*  
*Prereqs: Módulos 03, 09, 21, 27, 37, Lab 42*
