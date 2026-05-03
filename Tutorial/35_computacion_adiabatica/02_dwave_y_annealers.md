# D-Wave y Quantum Annealers

**Módulo 35 · Artículo 2 · Nivel muy avanzado**

---

## El hardware D-Wave: Pegasus y Advantage

D-Wave Advantage (2020) tiene **5000+ qubits** físicos en topología Pegasus P16.
A diferencia de los gate-based, opera directamente sobre el Hamiltoniano de Ising:

$$
H_{D\text{-}Wave} = \frac{A(t)}{2}\left(-\sum_i \sigma_i^x\right) + \frac{B(t)}{2}\left(\sum_i h_i \sigma_i^z + \sum_{i<j} J_{ij} \sigma_i^z \sigma_j^z\right)
$$

El annealing schedule $A(t)/B(t)$ determina la velocidad de transición del
Hamiltoniano transverso al Hamiltoniano de problema.

```python
import numpy as np
import matplotlib.pyplot as plt

def annealing_schedule_dwave(t: np.ndarray, T_anneal: float = 20.0) -> tuple:
    """
    Schedule de annealing simplificado de D-Wave.
    A(t): de alto a cero (campo transverso)
    B(t): de cero a alto (Hamiltoniano de problema)
    t en μs, T_anneal = tiempo total de annealing.
    """
    s = t / T_anneal  # normalizado
    A = 2.0 * (1 - s)**2  # GHz
    B = 2.0 * s**2         # GHz
    return A, B

t_vals = np.linspace(0, 20, 200)
A, B = annealing_schedule_dwave(t_vals)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].plot(t_vals, A, 'b-', lw=2, label='A(t) — campo transverso')
axes[0].plot(t_vals, B, 'r-', lw=2, label='B(t) — Hamiltoniano problema')
axes[0].axvline(10, color='gray', ls='--', alpha=0.5, label='Punto crítico t=T/2')
axes[0].set_xlabel('Tiempo (μs)'); axes[0].set_ylabel('Energía (GHz)')
axes[0].set_title('Schedule de annealing D-Wave (simplificado)')
axes[0].legend(); axes[0].grid(alpha=0.3)

# Ratio A/B: cuando < 1 el problema domina
ratio = A / (B + 1e-10)
axes[1].semilogy(t_vals, ratio, 'g-', lw=2)
axes[1].axhline(1.0, color='k', ls='--', label='A/B = 1')
axes[1].set_xlabel('Tiempo (μs)'); axes[1].set_ylabel('A(t)/B(t)')
axes[1].set_title('Ratio campo transverso / Hamiltoniano de problema')
axes[1].legend(); axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## Embedding: mapeando el problema al grafo Pegasus

Los qubits físicos de D-Wave están conectados en topología Pegasus, no en una
malla completa. Para problemas con mayor conectividad, se necesita **embedding**:
agrupar varios qubits físicos en una **cadena** que representa un qubit lógico.

```python
import numpy as np

def analisis_embedding(n_logicos: int, conectividad: float) -> dict:
    """
    Estima el número de qubits físicos necesarios para embedding en Pegasus.

    Pegasus P16: ~5000 qubits físicos, cada uno conectado a ~15 vecinos.
    
    conectividad: fracción de pares (i,j) con J_ij != 0 en el problema.
    """
    # Conectividad de Pegasus P16: ~15 por qubit → ~37500 cuplers totales
    conectores_pegasus = 37500
    
    # Qubits lógicos necesarios
    pares_logicos = int(conectividad * n_logicos * (n_logicos - 1) / 2)
    
    # Estimar longitud promedio de cadena (heurístico)
    # Para grafos densos: longitud ≈ n_logicos/sqrt(conectores_pegasus)
    longitud_cadena = max(1, int(n_logicos / np.sqrt(conectores_pegasus / n_logicos)))
    
    n_fisicos = n_logicos * longitud_cadena
    conectores_utilizados = pares_logicos
    factible = n_fisicos <= 5000 and conectores_utilizados <= conectores_pegasus

    return {
        'n_logicos': n_logicos,
        'conectividad': conectividad,
        'pares_logicos': pares_logicos,
        'longitud_cadena': longitud_cadena,
        'n_fisicos_est': n_fisicos,
        'factible': factible,
    }

print('Estimación de embedding en D-Wave Advantage (Pegasus P16):')
print(f'{"N_log":>6} | {"Conect.":>8} | {"Pares":>8} | {"Cadena":>7} | {"N_físicos":>10} | {"Factible"}')
print('-' * 60)
for n in [10, 50, 100, 200, 500]:
    for k in [0.3, 0.7]:
        r = analisis_embedding(n, k)
        ok = '✅' if r['factible'] else '❌'
        print(f'{n:>6} | {k:>8.1f} | {r["pares_logicos"]:>8} | '
              f'{r["longitud_cadena"]:>7} | {r["n_fisicos_est"]:>10} | {ok}')
```

---

## Comparativa: D-Wave vs Simulated Annealing vs QAOA

```python
from scipy.optimize import minimize
import numpy as np

def simulated_annealing(Q: np.ndarray, T_init: float = 2.0,
                         T_final: float = 0.01, n_steps: int = 5000,
                         seed: int = 0) -> dict:
    """
    Simulated Annealing clásico para minimizar x^T Q x, x ∈ {0,1}^n.
    """
    rng = np.random.default_rng(seed)
    n = Q.shape[0]
    x = rng.integers(0, 2, n)  # solución inicial aleatoria

    def energy(x):
        return float(x @ Q @ x)

    E = energy(x)
    E_best = E
    x_best = x.copy()

    T = T_init
    alpha = (T_final / T_init) ** (1 / n_steps)

    for step in range(n_steps):
        # Flip aleatorio
        i = rng.integers(n)
        x_new = x.copy(); x_new[i] = 1 - x_new[i]
        E_new = energy(x_new)
        dE = E_new - E

        if dE < 0 or rng.random() < np.exp(-dE / T):
            x = x_new; E = E_new
            if E < E_best:
                E_best = E; x_best = x.copy()
        T *= alpha

    return {'x': x_best, 'E': E_best, 'n_steps': n_steps}

def brute_force_qubo(Q: np.ndarray) -> dict:
    """Fuerza bruta para QUBO pequeño."""
    n = Q.shape[0]
    best_E, best_x = np.inf, None
    for mask in range(2**n):
        x = np.array([(mask >> k) & 1 for k in range(n)])
        E = float(x @ Q @ x)
        if E < best_E:
            best_E = E; best_x = x.copy()
    return {'x': best_x, 'E': best_E}

# Problema QUBO aleatorio
rng_prob = np.random.default_rng(42)
n = 12  # tamaño manejable para brute-force y SA
Q_prob = rng_prob.integers(-3, 4, (n, n)).astype(float)
Q_prob = (Q_prob + Q_prob.T) / 2  # simetrizar

# Solución exacta
r_exact = brute_force_qubo(Q_prob)
print(f'QUBO {n}×{n}: E_exacto = {r_exact["E"]:.2f}')

# Comparativa SA con diferentes tiempos
print(f'\n{"Algoritmo":>20} | {"E_obtenida":>12} | {"Gap vs óptimo":>14} | {"Tiempo (prop.)"}')
print('-' * 65)
for n_pasos in [100, 1000, 5000, 10000]:
    r = simulated_annealing(Q_prob, n_steps=n_pasos)
    gap = r['E'] - r_exact['E']
    print(f'{"SA":>10} ({n_pasos:>5} pasos) | {r["E"]:>12.2f} | {gap:>14.2f} | ×{n_pasos//100}')

print(f'{"Brute force":>20} | {r_exact["E"]:>12.2f} | {"0.00":>14} | ×(2^n)')
print('\nD-Wave resolvería esto en ~20 μs (incluyendo embedding)')
```

---

## Quantum Annealing vs Thermal Annealing: ¿hay ventaja cuántica?

```python
evidencia_ventaja = """
=== ¿D-Wave tiene ventaja cuántica sobre SA clásico? ===

HALLAZGOS EXPERIMENTALES (2024):

1. Troyer & Boixo (Science 2014): 
   - D-Wave 2X fue comparado con SA optimizado
   - Resultado: SA fue 10x más rápido en muchos problemas
   - Tunneling cuántico existe, pero SA también puede hacer "saltos"

2. King et al. (Science 2023):
   - D-Wave mostró ventaja en modelos de Ising específicos con
     ALTA CONECTIVIDAD que favorecen el tunneling
   - Ventaja sobre métodos SA/SQA clásicos en ≈ 10x para algunos casos

3. Boixo et al. (Nature Physics 2014):
   - Las correlaciones cuánticas de D-Wave son medibles
   - Pero la correlación con la ventaja en rendimiento es débil

CONCLUSIÓN HONESTA:
- D-Wave SÍ opera cuánticamente (tunneling demostrado)
- La ventaja práctica depende FUERTEMENTE del problema
- Para problemas genéricos, SA bien optimizado es competitivo
- Mejores candidatos: Ising spin glasses con topología Pegasus nativa

ALTERNATIVAS CLÁSICAS COMPARABLES:
- Simulated Annealing (SA): O(n²) por paso, implementación simple
- Simulated Quantum Annealing (SQA): emula D-Wave con MC
- Tabu Search: con frecuencia supera a D-Wave en benchmarks
- Tensor networks: para problemas con bajo entrelazamiento
"""
print(evidencia_ventaja)
```

---

## D-Wave Ocean SDK: interfaz de programación

```python
# Interfaz de D-Wave Ocean SDK (requiere acceso a la nube D-Wave)
# Este código muestra el patrón de uso, pero requiere credenciales LEAP

dwave_example_code = """
import dimod
from dwave.system import DWaveSampler, EmbeddingComposite

# Definir el problema QUBO
Q = {(0, 0): -1, (1, 1): -1, (0, 1): 2}

# Sampler de D-Wave con embedding automático
sampler = EmbeddingComposite(DWaveSampler())

# Resolver
sampleset = sampler.sample_qubo(Q, num_reads=1000, annealing_time=20)

# Resultados
best = sampleset.first
print(f'Solución óptima: {dict(best.sample)}')
print(f'Energía: {best.energy}')
print(f'Número de ocurrencias: {best.num_occurrences}')

# Acceso a respuesta cuántica simulada (sin acceso real a D-Wave)
# dimod.SimulatedAnnealingSampler — alternativa clásica
"""

print('Interfaz D-Wave Ocean SDK:')
print(dwave_example_code)

# Alternativa local con dimod (sin acceso a D-Wave)
try:
    import dimod
    Q_local = {(0, 0): -1, (1, 1): -1, (0, 1): 2}
    sampler = dimod.SimulatedAnnealingSampler()
    ss = sampler.sample_qubo(Q_local, num_reads=100)
    print('Resultado con SimulatedAnnealingSampler (local):')
    print(f'  Mejor solución: {dict(ss.first.sample)}, E={ss.first.energy}')
except ImportError:
    print('(dimod no instalado — instalar con: pip install dimod)')
```

---

## Estado del arte 2024: ¿cuándo usar D-Wave?

| Criterio | D-Wave Advantage | SA/SQA Clásico | QAOA (gate-based) |
|----------|-----------------|----------------|-------------------|
| Tamaño del problema | 5000+ qubits lógicos (con embedding) | Sin límite de memoria | < 100 qubits hoy |
| Tiempo de annealing | 20-2000 μs | Segundos-horas | Minutos-horas |
| Garantía de óptimo | No | No | No |
| Coste | $0.02/problema (nube) | Hardware CPU propio | IBM/Google cloud |
| Mejor caso | Ising nativo con baja conectividad | Cualquier QUBO | QUBO con buen ansatz |
| Peor caso | Problemas con alta conectividad / embedding largo | Paisajes muy rugosos | Circuitos muy profundos |

**Recomendación práctica:**
1. Para **investigación sobre ventaja cuántica**: D-Wave es valioso.
2. Para **producción hoy**: SA/Tabu/Gurobi son mejores en la mayoría de casos.
3. Para **problemas con estructura Pegasus nativa**: D-Wave gana claramente.
4. Para **el futuro (2030+)**: gate-based fault-tolerant con QAE superará a todos.

---

**Referencias:**
- Johnson et al., *Nature* 473, 194 (2011) — primer D-Wave comercial
- Boixo et al., *Nature Physics* 10, 218 (2014) — evidencia de tunneling
- King et al., *Science* 373, 1068 (2021) — simulación de spin glass
- King et al., *Science* 382, 1177 (2023) — ventaja en modelos específicos
- Hauke et al., *Nat. Phys.* 16, 10 (2020) — perspectivas de quantum annealing
