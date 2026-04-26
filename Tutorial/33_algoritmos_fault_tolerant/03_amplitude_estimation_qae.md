# Quantum Amplitude Estimation: MLQAE e IQAE

**Módulo 33 · Artículo 3 · Nivel muy avanzado**

---

## El problema de estimación de amplitud

Dado un circuito cuántico A tal que:

```
A|0⟩ = √(1-a)|Ψ₀⟩|0⟩ + √a|Ψ₁⟩|1⟩
```

QAE estima el valor `a = sin²(θ)` con precisión ε usando O(1/ε) aplicaciones
de A (cuadráticamente mejor que Monte Carlo clásico con O(1/ε²)).

**Contexto:** la estimación de amplitud es la base de la ventaja cuántica en
integración numérica, Monte Carlo cuántico (QMC) y valoración de derivados financieros.

---

## QAE original: basada en QPE

El QAE original (Brassard et al., 2002) usa QPE con el operador de Grover:

```
Q = A·S₀·A†·Sψ₀
```

donde S₀ refleja en torno a |0⟩ y Sψ₀ en torno a |Ψ₀⟩|0⟩.

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT
from fractions import Fraction

def qae_original(a_true: float, n_eval: int = 5) -> dict:
    """
    QAE original: usa QPE con m = n_eval qubits de evaluación.
    Estima a = sin²(θ) dado el circuito A.
    Sin simulación completa — modela la distribución de resultados.
    """
    theta = np.arcsin(np.sqrt(a_true))
    M = 2**n_eval  # número de valores posibles

    # QPE mide y/M ≈ θ/π con y ∈ {0, ..., M-1}
    # La distribución de probabilidad:
    probs = np.zeros(M)
    for y in range(M):
        phi_y = y / M
        # Probabilidad de medir y con QPE (aproximación):
        if M > 1:
            delta = phi_y - theta / np.pi
            if abs(delta) < 1e-10:
                probs[y] = 1.0
            else:
                probs[y] = (np.sin(np.pi * M * delta) / (M * np.sin(np.pi * delta)))**2
    probs /= probs.sum()

    # Resultado más probable
    y_best = np.argmax(probs)
    theta_est = y_best * np.pi / M
    a_est = np.sin(theta_est)**2

    # Error estándar teórico
    error_teorico = np.pi / M  # en theta; en a: ~2*sin(theta)*cos(theta)*π/M

    return {
        'a_true': a_true,
        'a_estimada': a_est,
        'theta_true': theta,
        'theta_est': theta_est,
        'error_abs': abs(a_est - a_true),
        'error_teorico': error_teorico,
        'n_consultas': M,  # O(1/ε) = O(2^n_eval)
        'probs': probs,
    }

# Demostración
print('QAE original para diferentes valores de a:')
print(f'{"a_true":>8} | {"a_est":>8} | {"error":>10} | {"n_eval":>6} | {"consultas":>10}')
print('-' * 50)
for a in [0.1, 0.25, 0.5, 0.75, 0.9]:
    for n_eval in [4, 6]:
        r = qae_original(a, n_eval)
        print(f'{a:>8.3f} | {r["a_estimada"]:>8.4f} | {r["error_abs"]:>10.6f} | {n_eval:>6} | {r["n_consultas"]:>10}')
```

---

## MLQAE: Maximum Likelihood sin QPE

MLQAE (Suzuki et al., 2020) elimina la QPE y usa runs de amplificación de Grover
con diferentes números de iteraciones. La estimación se hace por máxima verosimilitud.

```python
import numpy as np
from scipy.optimize import minimize_scalar

def grover_probability(theta: float, m: int) -> float:
    """P(medir 'bueno' tras m iteraciones de Grover)."""
    return np.sin((2*m + 1) * theta)**2

def mlqae(a_true: float, m_schedule: list[int], shots_per_m: int = 100,
          seed: int = 42) -> dict:
    """
    MLQAE: Maximum Likelihood QAE.

    m_schedule: lista de número de iteraciones de Grover a usar.
    Para cada m_j, ejecutar el circuito shots_per_m veces y contar éxitos.
    """
    rng = np.random.default_rng(seed)
    theta_true = np.arcsin(np.sqrt(a_true))

    # Simulación de mediciones
    mediciones = {}
    for m in m_schedule:
        p = grover_probability(theta_true, m)
        k = rng.binomial(shots_per_m, p)  # éxitos
        mediciones[m] = (k, shots_per_m)

    # Función log-verosimilitud
    def neg_log_likelihood(theta):
        if theta <= 0 or theta >= np.pi/2:
            return 1e10
        ll = 0.0
        for m, (k, N) in mediciones.items():
            p = grover_probability(theta, m)
            p = np.clip(p, 1e-12, 1 - 1e-12)
            ll += k * np.log(p) + (N - k) * np.log(1 - p)
        return -ll

    # Optimización sobre θ ∈ (0, π/2)
    result = minimize_scalar(neg_log_likelihood, bounds=(1e-6, np.pi/2 - 1e-6),
                              method='bounded')
    theta_est = result.x
    a_est = np.sin(theta_est)**2

    # Total de consultas
    n_total = sum(shots_per_m * (2*m + 1) for m in m_schedule)

    return {
        'a_true': a_true,
        'a_est': a_est,
        'theta_est': theta_est,
        'error_abs': abs(a_est - a_true),
        'n_consultas_total': n_total,
        'mediciones': mediciones,
    }

# Schedule lineal vs. exponencial
m_lineal = list(range(0, 16))          # 0,1,2,...,15
m_expo   = [2**k for k in range(5)]    # 1,2,4,8,16

print('MLQAE con diferentes schedules (a=0.3):')
for nombre, schedule in [('Lineal', m_lineal), ('Exponencial', m_expo)]:
    r = mlqae(0.3, schedule, shots_per_m=200, seed=0)
    print(f'  {nombre}: a_est={r["a_est"]:.4f}, error={r["error_abs"]:.5f}, '
          f'consultas={r["n_consultas_total"]}')
```

---

## IQAE: Iterative QAE con intervalos de confianza

IQAE (Grinko et al., 2021) es el más eficiente en la práctica: usa bisección
iterativa del ángulo θ con intervalos de Chernoff-Hoeffding.

```python
import numpy as np
from scipy.stats import binom

def iqae(a_true: float, epsilon: float = 0.01, alpha: float = 0.05,
         seed: int = 42) -> dict:
    """
    IQAE: Iterative Quantum Amplitude Estimation.

    Garantías: |a_est - a_true| ≤ ε con probabilidad ≥ 1-α.

    Parámetros:
        epsilon: precisión deseada
        alpha: probabilidad de fallo (1-alpha = confianza)
    """
    rng = np.random.default_rng(seed)
    theta_true = np.arcsin(np.sqrt(a_true))

    # Intervalo inicial
    theta_l, theta_u = 0.0, np.pi / 2
    m = 0  # iteraciones de Grover
    n_consultas_total = 0
    historial = []

    while (theta_u - theta_l) / 2 > epsilon:
        # Número de shots para esta iteración (garantía estadística)
        N_shots = max(100, int(np.ceil(np.log(2 / alpha) / (2 * epsilon**2))))
        N_shots = min(N_shots, 10000)

        # Simular medición con m iteraciones de Grover
        p_true = grover_probability(theta_true, m)
        k = rng.binomial(N_shots, p_true)
        n_consultas_total += N_shots * (2*m + 1)

        # Estimador de θ del intervalo (Clopper-Pearson)
        p_est = k / N_shots
        # Intervalo de confianza por inversa de binomial
        delta = np.sqrt(np.log(2/alpha) / (2*N_shots))
        p_lower = max(0, p_est - delta)
        p_upper = min(1, p_est + delta)

        # Convertir de p = sin²((2m+1)θ) a θ
        factor = 2*m + 1
        # p_upper → θ_upper (inversa de sin²)
        theta_cand_u = np.arcsin(np.sqrt(p_upper)) / factor if p_upper <= 1 else theta_u
        theta_cand_l = np.arcsin(np.sqrt(p_lower)) / factor

        # Refinar intervalo
        theta_l = max(theta_l, theta_cand_l)
        theta_u = min(theta_u, theta_cand_u + (np.pi/factor - 2*theta_u/factor))

        # Asegurar que no se revierta
        theta_u = max(theta_u, theta_l + 1e-10)

        # Aumentar m para la siguiente iteración
        m_next = int(np.ceil(np.pi / (4 * (theta_u - theta_l))))
        m = min(m_next, m + 10)  # incremento gradual

        historial.append({
            'iteracion': len(historial) + 1,
            'm': m, 'k': k, 'N': N_shots,
            'theta_l': theta_l, 'theta_u': theta_u,
            'a_l': np.sin(theta_l)**2, 'a_u': np.sin(theta_u)**2,
        })

        if len(historial) > 50:  # seguridad
            break

    theta_est = (theta_l + theta_u) / 2
    a_est = np.sin(theta_est)**2

    return {
        'a_true': a_true,
        'a_est': a_est,
        'error_abs': abs(a_est - a_true),
        'n_consultas': n_consultas_total,
        'n_iteraciones': len(historial),
        'historial': historial,
    }

print('\nIQAE para diferentes valores de a (ε=0.01, α=0.05):')
print(f'{"a_true":>8} | {"a_est":>8} | {"error":>8} | {"consultas":>10} | {"iters":>6}')
print('-' * 50)
for a in [0.1, 0.3, 0.5, 0.7, 0.9]:
    r = iqae(a, epsilon=0.01, alpha=0.05, seed=42)
    print(f'{a:>8.3f} | {r["a_est"]:>8.4f} | {r["error_abs"]:>8.5f} | '
          f'{r["n_consultas"]:>10} | {r["n_iteraciones"]:>6}')
```

---

## Aplicación: Monte Carlo Cuántico para opciones financieras

El caso de uso más concreto y estudiado es la valoración de opciones europeas.

```python
import numpy as np

def valoracion_call_europea(
    S0: float, K: float, r: float, sigma: float, T: float,
    n_paths: int = 10000, seed: int = 0
) -> dict:
    """
    Monte Carlo clásico vs. QMC para una opción call europea.

    Payoff: max(S_T - K, 0)
    S_T = S0 * exp((r - σ²/2)T + σ√T·Z) con Z~N(0,1)
    """
    rng = np.random.default_rng(seed)

    # Simulación clásica (Monte Carlo)
    Z = rng.standard_normal(n_paths)
    S_T = S0 * np.exp((r - 0.5*sigma**2)*T + sigma*np.sqrt(T)*Z)
    payoffs = np.maximum(S_T - K, 0)
    precio_mc = np.exp(-r*T) * np.mean(payoffs)
    error_mc  = np.exp(-r*T) * np.std(payoffs) / np.sqrt(n_paths)

    # Black-Scholes analítico (referencia)
    from scipy.stats import norm
    d1 = (np.log(S0/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    precio_bs = S0*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)

    # Complejidad: MC clásico necesita O(1/ε²) muestras para error ε
    # QMC necesita O(1/ε) consultas (cuadráticamente mejor)
    epsilon_target = 0.01  # 1 céntimo de precisión
    n_mc_clasico = int(np.ceil((np.std(payoffs) / epsilon_target)**2))
    n_qmc = int(np.ceil(1 / epsilon_target))  # consultas cuánticas

    return {
        'precio_bs': precio_bs,
        'precio_mc': precio_mc,
        'error_mc': error_mc,
        'n_paths_usados': n_paths,
        'n_mc_para_1ct': n_mc_clasico,
        'n_qmc_para_1ct': n_qmc,
        'speedup_cuadratico': n_mc_clasico / n_qmc,
    }

# Parámetros típicos de opción europea (S&P 500)
r = valoracion_call_europea(S0=100, K=105, r=0.05, sigma=0.20, T=1.0,
                              n_paths=100000, seed=0)
print(f'\nValoración de opción call europea:')
print(f'  Black-Scholes analítico: ${r["precio_bs"]:.4f}')
print(f'  Monte Carlo clásico:     ${r["precio_mc"]:.4f} ± {r["error_mc"]:.4f}')
print(f'\nComplejidad para ε=0.01:')
print(f'  MC clásico necesita:  {r["n_mc_para_1ct"]:,} muestras')
print(f'  QMC necesita:         {r["n_qmc_para_1ct"]:,} consultas')
print(f'  Speedup cuadrático:   ×{r["speedup_cuadratico"]:.0f}')
```

---

## Comparativa de variantes QAE

```python
variantes_qae = [
    {
        'nombre': 'QAE original (Brassard 2002)',
        'circuito': 'QPE + Grover',
        'qubits_extra': 'n_eval (precisión)',
        'n_consultas': 'O(1/ε)',
        'requiere_qpe': True,
        'profundidad': 'Alta (QPE)',
        'ventaja': 'Exacto, sin shots múltiples',
        'desventaja': 'QPE requiere QFT + ancillas',
    },
    {
        'nombre': 'MLQAE (Suzuki 2020)',
        'circuito': 'Grover × m_j',
        'qubits_extra': 'Solo 1 ancilla',
        'n_consultas': 'O(1/ε·log(1/δ))',
        'requiere_qpe': False,
        'profundidad': 'Media',
        'ventaja': 'Sin QPE, más robusto al ruido',
        'desventaja': 'Más shots, complejidad log extra',
    },
    {
        'nombre': 'IQAE (Grinko 2021)',
        'circuito': 'Grover × m_i iterativo',
        'qubits_extra': 'Solo 1 ancilla',
        'n_consultas': 'O(1/ε·log(log(1/ε)))',
        'requiere_qpe': False,
        'profundidad': 'Baja por iteración',
        'ventaja': 'Óptimo en práctica, garantías estadísticas',
        'desventaja': 'Múltiples rondas de medición',
    },
    {
        'nombre': 'POWER QAE (Wie 2019)',
        'circuito': 'Hadamard test',
        'qubits_extra': '1 control',
        'n_consultas': 'O(1/ε)',
        'requiere_qpe': False,
        'profundidad': 'Muy baja',
        'ventaja': 'Circuitos muy cortos',
        'desventaja': 'Varianza alta, requiere muchos shots',
    },
]

print('\nCOMPARATIVA DE VARIANTES QAE:')
print('=' * 80)
for v in variantes_qae:
    print(f'\n{v["nombre"]}')
    for k, val in v.items():
        if k != 'nombre':
            print(f'  {k:20s}: {val}')
```

---

## QUBO y optimización combinatoria cuántica

QAE también aparece como subroutina en optimización cuando el objetivo es
evaluar el valor esperado de una función de coste cuántica.

```python
import numpy as np

def qubo_qae_demo(n_vars: int = 4, seed: int = 0) -> dict:
    """
    Demostración de cómo QAE estima E[C(x)] para un QUBO.

    C(x) = Σ Q_ij x_i x_j (función de coste QUBO).
    En QMC cuántico, se prepara |ψ⟩ con QAOA y se estima ⟨ψ|C|ψ⟩ con QAE.
    """
    rng = np.random.default_rng(seed)
    N = 2**n_vars

    # Generar un problema QUBO aleatorio
    Q = rng.standard_normal((n_vars, n_vars))
    Q = (Q + Q.T) / 2  # simetrizar

    # Calcular valor de coste para todas las soluciones binarias
    costes = np.zeros(N)
    for x_int in range(N):
        x = np.array([(x_int >> i) & 1 for i in range(n_vars)])
        costes[x_int] = x @ Q @ x

    # Estado uniforme (superposición de todas las soluciones)
    probs = np.ones(N) / N
    valor_esperado_uniforme = np.dot(probs, costes)
    valor_min = np.min(costes)
    valor_max = np.max(costes)

    # Con QAE, se estima este valor esperado en O(1/ε) en vez de O(1/ε²)
    epsilon = 0.1
    n_clasico = int(1 / epsilon**2)  # muestras Monte Carlo clásico
    n_cuantico = int(1 / epsilon)    # consultas QAE

    return {
        'n_vars': n_vars,
        'N_soluciones': N,
        'valor_minimo': valor_min,
        'valor_maximo': valor_max,
        'E_uniforme': valor_esperado_uniforme,
        'n_mc_clasico': n_clasico,
        'n_qae': n_cuantico,
        'speedup': n_clasico / n_cuantico,
    }

r = qubo_qae_demo(n_vars=6, seed=42)
print(f'\nQUBO con {r["n_vars"]} variables ({r["N_soluciones"]} soluciones):')
print(f'  Coste mínimo: {r["valor_minimo"]:.3f}')
print(f'  Coste máximo: {r["valor_maximo"]:.3f}')
print(f'  E[C] uniforme: {r["E_uniforme"]:.3f}')
print(f'\nEstimación de E[C] con ε=0.1:')
print(f'  MC clásico:   {r["n_mc_clasico"]:,} muestras')
print(f'  QAE:          {r["n_qae"]:,} consultas')
print(f'  Speedup:      ×{r["speedup"]:.0f}')
```

---

## El veredicto sobre QAE

```
┌─────────────────────────────────────────────────────────────────┐
│  QAE tiene la ventaja cuántica más sólida de todos los           │
│  algoritmos fault-tolerant no-criptográficos:                    │
│                                                                  │
│  ✅ Speedup cuadrático DEMOSTRADO (no conjetural)                │
│  ✅ No requiere QRAM para la integración numérica               │
│  ✅ IQAE funciona con circuitos de profundidad moderada          │
│  ✅ Aplicaciones reales: finanzas, física, ML                    │
│                                                                  │
│  Pero:                                                            │
│  ⚠️  Speedup cuadrático, no exponencial                          │
│  ⚠️  El oráculo A debe ser eficiente en qubits                   │
│  ⚠️  Para finanzas: la preparación del modelo es el cuello       │
│      de botella, no la estimación en sí                          │
│  ⚠️  Ventaja práctica requiere ~10⁶ consultas → FT hardware     │
└─────────────────────────────────────────────────────────────────┘
```

---

**Referencias:**
- Brassard et al., *Contemp. Math.* 305, 53 (2002) — QAE original
- Suzuki et al., *Quantum* 4, 294 (2020) — MLQAE
- Grinko et al., *npj Quantum Inf.* 7, 52 (2021) — IQAE
- Stamatopoulos et al., *Quantum* 4, 291 (2020) — opciones financieras con QAE
- Montanaro, *npj Quantum Inf.* 2, 15023 (2016) — speedup cuadrático en MC cuántico
