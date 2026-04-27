# Solución R8 — Advantage Cuántica: Complejidad y Lower Bounds

**Problema:** [Ejercicios de investigación R8](../../Ejercicios/ejercicios_investigacion.md#problema-r8)

---

## Parte a) — Clases de complejidad cuántica

```python
# Resumen estructural — no hay código ejecutable para complejidad de Turing
clases = """
JERARQUÍA DE COMPLEJIDAD CUÁNTICA
══════════════════════════════════

P ⊆ BPP ⊆ BQP ⊆ QMA ⊆ PSPACE

Clase   | Modelo          | Problema canónico
────────┼─────────────────┼──────────────────────────────
P       | Clásico det.    | Ordenar, aritméticos
BPP     | Clásico rndm    | Primalidad (antes de AKS)
BQP     | Cuántico poly   | Factorización (Shor), DLP
QMA     | Cuántico + wit  | k-Local Hamiltonian
PSPACE  | Clásico poly-sp | TQBF (cuantificado)

RELACIONES PROBADAS:
  P ⊆ BPP (trivial), P ⊆ BQP (trivial)
  BQP ⊆ PSPACE (Adleman et al. 1997)
  BQP ⊆ PP ⊆ PSPACE

RELACIONES ABIERTAS (problemas del milenio cuántico):
  ¿P = BQP?   (equivalencia cuántico-clásico para todos los problemas)
  ¿BPP = BQP? (¿hay ventaja cuántica universal?)
  ¿NP ⊆ BQP? (¿cuántico resuelve NP en poly tiempo?)
  
EVIDENCIA:
  Relativized: existe oráculo A con BQP^A ⊄ PH^A (Raz & Tal 2019)
  → BQP no está contenido en PH bajo oráculos (fuerte separación)
"""
print(clases)
```

---

## Parte b) — Algoritmos con ventaja cuántica demostrada

```python
import numpy as np
import matplotlib.pyplot as plt

# Tabla de algoritmos con speedup demostrado
algoritmos = [
    {"nombre": "Grover (búsqueda)",      "clasico": "O(N)",       "cuantico": "O(√N)",       "tipo": "Cuadrático", "q_opt": 1e12},
    {"nombre": "Shor (factorización)",   "clasico": "exp(n^{1/3})","cuantico": "O(n³)",       "tipo": "Exponencial","q_opt": 1e6},
    {"nombre": "HHL (sistemas lineales)","clasico": "O(Ns)",      "cuantico": "O(log N·κ²)", "tipo": "Exponencial","q_opt": 1e8},
    {"nombre": "QFT",                    "clasico": "O(N log N)",  "cuantico": "O(log²N)",    "tipo": "Exponencial","q_opt": 1e4},
    {"nombre": "Estimación de amplitud", "clasico": "O(1/ε²)",    "cuantico": "O(1/ε)",      "tipo": "Cuadrático", "q_opt": 1e6},
    {"nombre": "QSVT (general)",         "clasico": "Varía",       "cuantico": "O(poly d)",   "tipo": "Polinómico", "q_opt": 1e5},
    {"nombre": "Simulación Hamiltoniana","clasico": "exp(n)",      "cuantico": "O(poly n)",   "tipo": "Exponencial","q_opt": 1e3},
]

print(f'{"Algoritmo":>28} | {"Clásico":>20} | {"Cuántico":>18} | {"Tipo speedup":>14}')
print('-' * 90)
for a in algoritmos:
    print(f'{a["nombre"]:>28} | {a["clasico"]:>20} | {a["cuantico"]:>18} | {a["tipo"]:>14}')
```

---

## Parte c) — Lower bounds: límites del speedup cuántico

```python
lower_bounds = """
LOWER BOUNDS — LO QUE EL CUÁNTICO NO PUEDE HACER
══════════════════════════════════════════════════

1. GROVER ES ÓPTIMO (Bennett et al. 1997):
   Búsqueda en base desordenada: Ω(√N) consultas (demostrado con polynomial method).
   → Ningún algoritmo cuántico puede ser sub-cuadrático en búsqueda.

2. NP-HARD NO ESTÁ EN BQP (conjeturalmente):
   Si BQP ⊇ NP → PH ⊆ BQP → colapsaría la jerarquía polinómica.
   Evidencia: problema de k-SAT sigue siendo exponencial en cuántico.

3. PARITY TIENE LOWER BOUND Ω(N) (Beals et al. 1998):
   Calcular la paridad de N bits requiere N/2 consultas cuánticas.
   → Grover no ayuda para problemas de paridad.

4. SDIS (Simetría de ruptura):
   Forrelation: máximo speedup posible BQP vs PH (Aaronson & Ambainis 2015).
   Speedup solo en problemas con estructura de "forrelación" (correlación entre Fourier).

5. ORACLE SEPARATION:
   Existe oráculo donde: P ≠ BPP ≠ BQP ≠ QMA ≠ PSPACE
   → Las separaciones son reales bajo oráculos (pero no implican separaciones sin oráculo).

6. DEQUANTIZATION (Tang 2018-2022):
   Muchos algoritmos cuánticos que parecían exponenciales son dequantizables:
   - Recomendación cuántica (HHL-based) → algoritmo clásico O(poly log N)
   - Clustering cuántico → dequantizable
   → La ventaja depende de si el estado cuántico puede prepararse eficientemente.
"""
print(lower_bounds)

# Gráfica: speedup cuántico vs tamaño del problema
N = np.logspace(2, 12, 100)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Tiempo (en unidades de operación básica)
t_grover_q = np.sqrt(N)
t_grover_c = N
t_shor_q   = np.log2(N)**3  # aprox para n = log2(N)
t_shor_c   = np.exp(np.log2(N)**(1/3))

axes[0].loglog(N, t_grover_c, 'r-', lw=2, label='Búsqueda clásica O(N)')
axes[0].loglog(N, t_grover_q, 'b-', lw=2, label='Grover cuántico O(√N)')
axes[0].loglog(N, t_shor_c,   'r--', lw=2, label='Factorización clásica exp(n^{1/3})')
axes[0].loglog(N, t_shor_q,   'b--', lw=2, label='Shor cuántico O(n³)')
axes[0].set_xlabel('Tamaño del problema N'); axes[0].set_ylabel('Tiempo relativo')
axes[0].set_title('Speedup cuántico: Grover y Shor'); axes[0].legend(fontsize=8)
axes[0].grid(alpha=0.3, which='both')

# Crossover point: cuándo el cuántico supera al clásico (considerando overhead constante)
overhead_q = 1000  # overhead físico cuántico (gates, latencia)
t_grover_q_real = overhead_q * np.sqrt(N)
t_grover_c_real = N

crossover = np.where(t_grover_q_real < t_grover_c_real)[0]
N_cross = N[crossover[0]] if len(crossover) > 0 else None

axes[1].loglog(N, t_grover_c_real, 'r-', lw=2, label='Clásico O(N)')
axes[1].loglog(N, t_grover_q_real, 'b-', lw=2, label=f'Grover (overhead ×{overhead_q})')
if N_cross:
    axes[1].axvline(N_cross, color='k', ls=':', lw=1.5, label=f'Crossover N≈{N_cross:.0e}')
axes[1].set_xlabel('N'); axes[1].set_ylabel('Tiempo (con overhead cuántico)')
axes[1].set_title('Crossover cuántico-clásico con overhead realista')
axes[1].legend(fontsize=9); axes[1].grid(alpha=0.3, which='both')

plt.tight_layout(); plt.show()

if N_cross:
    print(f'\nCon overhead cuántico ×{overhead_q}, Grover supera al clásico para N > {N_cross:.0e}')
```

---

## Parte d) — ¿Hay ventaja cuántica práctica hoy?

```python
conclusion = """
CONCLUSIÓN: ESTADO DEL ADVANTAGE CUÁNTICO (2025)
══════════════════════════════════════════════════

DEMOSTRADO TEÓRICAMENTE:
  ✓ Shor (factorización): exponencial, pero necesita QEC
  ✓ Grover (búsqueda): cuadrático, sin QEC
  ✓ HHL (linear systems): exponencial, pero con caveats de dequantization
  ✓ QPE / QFT: exponencial en forma de circuito

DEMOSTRADO EXPERIMENTALMENTE (sin QEC):
  ✓ Quantum Volume ≥ 512 (IBM 2024)
  ✓ XEB > 0 para circuitos de profundidad ≥ 20
  ✓ Repetitive QEC: corrección de errores activa (Google 2023)
  ✗ Ningún cálculo ÚTIL más rápido que el clásico

OUTLOOK REALISTA:
  2025-2027: ventaja en simulación de química (Hamiltoniano Fermi-Hubbard)
  2027-2030: ventaja en estimación de amplitud (finanzas, ML)
  2030+:     ventaja criptográfica (factorización RSA-2048)

REQUISITOS TÉCNICOS:
  Error 2Q: < 0.1% (actual: ~0.3%)
  T₁, T₂:  > 1 ms (actual: ~100-500 μs)
  Qubits:   > 1M (actual: ~1000 físicos, ~10 lógicos corregidos)
"""
print(conclusion)
```

---

## Referencia
Aaronson & Ambainis, *Forrelation: A problem that optimally separates quantum from classical computing*, **STOC** 2015;  
Tang, *A quantum-inspired classical algorithm for recommendation systems*, **STOC** 2019;  
Babbush et al., *Focus beyond quadratic speedups for error-corrected quantum advantage*, **PRX Quantum** 2, 010103 (2021);  
Raz & Tal, *Oracle separation of BQP and PH*, **STOC** 2019.
