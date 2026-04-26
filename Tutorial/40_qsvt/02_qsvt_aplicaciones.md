# QSVT: Transformación de Valores Singulares Cuántica

**Módulo 40 · Artículo 2 · Nivel muy avanzado**

---

## El teorema central de QSVT

La QSVT (Gilyen, Su, Low, Wiebe — STOC 2019) establece que, dada una
block encoding $U_A$ de la matriz $A$ con valores singulares $\sigma_k$,
es posible implementar una block encoding de $P(\sigma_k)$ para cualquier
polinomio par o impar de grado $d$ usando **$d$ aplicaciones de $U_A$**:

$$U_A \xrightarrow{\text{QSVT con polinomio }P} U_{P(A)}$$

Los ángulos de QSVT $\{\phi_0, \phi_1, \ldots, \phi_d\}$ codifican el polinomio,
y el circuito alterna rotaciones de fase con $U_A$ y $U_A^\dagger$.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

def qsvt_circuit_depth(d: int) -> int:
    """Profundidad del circuito QSVT para polinomio de grado d."""
    return 2 * d + 1  # d queries a U_A, d a U_A†, + rotaciones de fase

def aproximar_polinomio_qsvt(f_target, x_vals: np.ndarray,
                               grado: int) -> np.ndarray:
    """
    Encuentra los coeficientes del polinomio Chebyshev de grado `grado`
    que mejor aproxima f_target en x_vals ⊂ [-1, 1].
    
    QSVT trabaja en la base de polinomios de Chebyshev T_k(x).
    """
    # Evaluación de Chebyshev
    T = np.zeros((len(x_vals), grado + 1))
    T[:, 0] = 1
    if grado >= 1:
        T[:, 1] = x_vals
    for k in range(2, grado + 1):
        T[:, k] = 2 * x_vals * T[:, k-1] - T[:, k-2]

    # Regresión de mínimos cuadrados
    coeffs, _, _, _ = np.linalg.lstsq(T, f_target(x_vals), rcond=None)
    return coeffs

# Funciones objetivo para QSVT
x = np.linspace(-1, 1, 300)

funciones = {
    'Sign(x)':   (lambda x: np.sign(x + 1e-15), 'red',   'Clasificación cuántica'),
    '1/x':       (lambda x: np.where(np.abs(x) > 0.1, 1/x, 0), 'blue', 'HHL (inversión)'),
    'exp(-x²)':  (lambda x: np.exp(-x**2), 'green', 'Gaussiana (QMC)'),
}

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for ax, (nombre, (f, color, titulo)) in zip(axes, funciones.items()):
    y_target = f(x)
    for grado in [5, 15, 25]:
        coeffs = aproximar_polinomio_qsvt(f, grado)
        # Evaluar el polinomio Chebyshev
        T_eval = np.zeros((len(x), grado + 1))
        T_eval[:, 0] = 1
        if grado >= 1:
            T_eval[:, 1] = x
        for k in range(2, grado + 1):
            T_eval[:, k] = 2 * x * T_eval[:, k-1] - T_eval[:, k-2]
        y_approx = T_eval @ coeffs
        error_max = np.max(np.abs(y_approx - y_target))
        ax.plot(x, y_approx, lw=1.5, label=f'd={grado} (err={error_max:.3f})')

    ax.plot(x, y_target, 'k--', lw=2, alpha=0.5, label='Target')
    ax.set_title(f'{nombre}\n({titulo})')
    ax.set_xlabel('x (valor singular normalizado)')
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    ax.set_ylim(-1.5, 1.5)

plt.suptitle('Aproximación polinómica para QSVT', fontsize=12, y=1.02)
plt.tight_layout()
plt.show()
```

---

## Casos especiales de QSVT

```python
casos_qsvt = """
QSVT COMO MARCO UNIFICADOR DE ALGORITMOS CUÁNTICOS
═══════════════════════════════════════════════════════════════════

Algoritmo → Función P(σ) aplicada por QSVT:

┌──────────────────────┬──────────────────────┬─────────────────────┐
│ Algoritmo            │ Función P(σ)          │ Complejidad         │
├──────────────────────┼──────────────────────┼─────────────────────┤
│ Grover search        │ Sign(x)               │ O(√N) queries       │
│ QPE (phase estim.)   │ e^(iθ) → θ extrac.   │ O(1/ε)              │
│ HHL (Ax=b)           │ 1/x (inversión)       │ O(κ/ε) polylog(N)   │
│ Sim. hamiltoniana    │ e^(-ixτ)              │ O(τ·||H||_max·log N)│
│ Monte Carlo cuántico │ √x (amplitud estim.)  │ O(1/ε) cuadrático   │
│ Eigenvalue filter    │ θ(x - μ) (escalón)   │ O(1/gap) queries    │
│ Singular value filter│ Paso en σ_k           │ O(d) queries a U_A  │
└──────────────────────┴──────────────────────┴─────────────────────┘

CONSTRUCCIÓN DEL CIRCUITO QSVT:
  Dado el polinomio P de grado d con ángulos φ₀,...,φ_d:
  
  W_QSVT = e^(iφ₀Π̃) · U_A · e^(iφ₁Π) · U_A† · e^(iφ₂Π̃) · ... · U_A · e^(iφ_dΠ)
  
  donde Π = |0⟩⟨0| ⊗ I_sys  (proyector en el ancilla)
        Π̃ = I_anc ⊗ |0⟩⟨0|  (dual)
  
  Profundidad: 2d queries a U_A + d rotaciones de fase → O(d)
  
CÁLCULO DE ÁNGULOS φ_k:
  Dado el polinomio P (en base Chebyshev), los ángulos se obtienen
  resolviendo un sistema no lineal (Haah 2019, Lin & Tong 2022).
  Herramientas: pyqsp, qsppack, QSVT-via-poly.
"""
print(casos_qsvt)
```

---

## Implementación: QSVT para HHL (inversión de matrices)

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def hhl_via_qsvt_schema(kappa: float, epsilon: float) -> dict:
    """
    Analiza los requisitos de QSVT para resolver Ax=b via inversión.
    
    kappa: número de condición de A
    epsilon: precisión objetivo
    
    QSVT aplica P(σ) = 1/σ truncado en [1/kappa, 1]
    usando el polinomio de aproximación de Chebyshev de grado d.
    """
    # Grado necesario para aproximar 1/x en [1/kappa, 1] con error ε
    # d ≈ kappa · log(kappa/ε) / 2  (cota de Chebyshev)
    d = int(np.ceil(kappa * np.log(kappa / epsilon) / 2))
    
    # Queries a U_A (block encoding de A)
    n_queries = 2 * d + 1
    
    # Overhead de amplificación: la proyección post-QSVT tiene probabilidad ~1/kappa²
    # Requiere amplificación de amplitud: O(kappa) rondas adicionales
    overhead_amplif = int(np.ceil(kappa))
    total_queries = n_queries * overhead_amplif
    
    return {
        'kappa': kappa,
        'epsilon': epsilon,
        'grado_poly': d,
        'queries_QSVT': n_queries,
        'overhead_ampliflicacion': overhead_amplif,
        'queries_total': total_queries,
        'profundidad_circuito': total_queries,
    }

print('Análisis de requisitos QSVT para HHL:')
print(f'{"κ":>6} | {"ε":>8} | {"grado d":>8} | {"queries":>10} | {"profundidad"}')
print('-' * 55)
for kappa in [2, 5, 10, 100]:
    for eps in [0.01, 0.001]:
        r = hhl_via_qsvt_schema(kappa, eps)
        print(f'{kappa:>6} | {eps:>8.3f} | {r["grado_poly"]:>8} | '
              f'{r["queries_total"]:>10} | {r["profundidad_circuito"]}')

# Comparativa vs clásico
print('\nComparativa con solver clásico (CG iterativo):')
print('  Clásico CG:  O(N · kappa · log(1/ε))  operaciones')
print('  HHL/QSVT:    O(kappa · poly-log(N/ε)) queries a U_A')
print('  Condición para ventaja: acceso eficiente a U_A (QRAM o estructura)')
print('  Aplicaciones reales: sistemas dispersos, ML, PDEs discretizadas')
```

---

## Simulación hamiltoniana óptima con QSVT

```python
import numpy as np

def recursos_sim_hamiltoniana(
    n_qubits: int,
    H_norm: float,    # ||H||_max
    t: float,         # tiempo de simulación
    epsilon: float,   # precisión
    metodo: str       # 'Trotter-2', 'LCU-Taylor', 'QSVT'
) -> dict:
    """
    Estima los recursos para simular exp(-iHt) con diferentes métodos.
    """
    N = 2**n_qubits
    
    if metodo == 'Trotter-2':
        # Trotter orden 2: r ~ t² ||H||² / (2ε)
        r = int(np.ceil(t**2 * H_norm**2 / (2 * epsilon)))
        queries = r * n_qubits  # cada paso Trotter: O(n) puertas de 2 qubits
        
    elif metodo == 'LCU-Taylor':
        # LCU de Taylor: d ~ t ||H|| · e · log(t||H||/ε)
        lam = H_norm * N  # norma LCU (caso genérico)
        d = int(np.ceil(np.e * lam * t * np.log(lam * t / epsilon)))
        queries = d
        
    elif metodo == 'QSVT':
        # QSVT optimal: d ~ t ||H|| + log(1/ε)
        d = int(np.ceil(t * H_norm + np.log(1 / epsilon)))
        queries = 2 * d + 1
    
    return {
        'metodo': metodo,
        'queries': queries,
        'epsilon': epsilon,
    }

print('Comparativa de métodos para simulación hamiltoniana:')
print(f'  n=10 qubits, t=10, ||H||=1, ε=0.001')
print(f'\n{"Método":>15} | {"Queries a U_A":>14}')
print('-' * 35)
for metodo in ['Trotter-2', 'LCU-Taylor', 'QSVT']:
    r = recursos_sim_hamiltoniana(10, 1.0, 10.0, 0.001, metodo)
    print(f'{r["metodo"]:>15} | {r["queries"]:>14}')

# Escalar en t
t_vals = np.logspace(0, 3, 100)
fig, ax = plt.subplots(figsize=(9, 5))
for metodo, color in [('Trotter-2', 'red'), ('LCU-Taylor', 'orange'), ('QSVT', 'blue')]:
    qs = [recursos_sim_hamiltoniana(10, 1.0, t, 0.001, metodo)['queries'] for t in t_vals]
    ax.loglog(t_vals, qs, color=color, lw=2, label=metodo)

ax.set_xlabel('Tiempo de simulación t')
ax.set_ylabel('Queries a U_A (profundidad)')
ax.set_title('Complejidad de simulación hamiltoniana vs t')
ax.legend()
ax.grid(alpha=0.3, which='both')
plt.tight_layout()
plt.show()

print('\nVentaja de QSVT:')
print('  Escala linealmente en t (Trotter cuadrático → exponencial en error)')
print('  Log en 1/ε (vs polinomial en Trotter)')
print('  Óptimo: no existe método con menos queries (Lower bound de Haah 2021)')
```

---

**Referencias:**
- Gilyen, Su, Low, Wiebe, *STOC 2019* — QSVT original
- Low & Chuang, *Quantum* 3, 163 (2019) — qubitización
- Martyn, Rossi, Tan, Chuang, *PRX Quantum* 2, 040203 (2021) — tutorial QSVT
- Lin & Tong, *PRX Quantum* 3, 010318 (2022) — near-optimal QSVT
- Babbush et al., *npj Quantum Inf.* 5, 92 (2019) — QSVT en química cuántica
