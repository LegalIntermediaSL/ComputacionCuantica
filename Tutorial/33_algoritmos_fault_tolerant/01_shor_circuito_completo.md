# Algoritmo de Shor: Circuito Completo para N=15

**Módulo 33 · Artículo 1 · Nivel muy avanzado**

---

## Estructura del algoritmo

El algoritmo de Shor factoriza N en dos pasos:

1. **Reducción clásica:** si N es par, devuelve 2. Si N es potencia perfecta,
   usa raíz. Elige a ∈ [2, N-2] al azar; si gcd(a, N) > 1, factor encontrado.

2. **Quantum Period Finding (QPF):** encuentra el período r de f(x) = aˣ mod N.
   Una vez r es conocido, gcd(a^{r/2}±1, N) da los factores con alta probabilidad.

```python
from math import gcd, isqrt
import numpy as np

def shor_clasico(N: int, a: int) -> tuple[int, int] | None:
    """
    Parte clásica del algoritmo de Shor.
    Dado que la QPF ha encontrado el periodo r, extrae los factores.
    """
    if N % 2 == 0:
        return 2, N // 2
    for k in range(2, int(np.log2(N)) + 1):
        root = round(N ** (1/k))
        if root ** k == N:
            return root, root  # potencia perfecta

    if gcd(a, N) != 1:
        return gcd(a, N), N // gcd(a, N)

    return None  # la QPF debe encontrar r

def extraer_factores(N: int, a: int, r: int) -> tuple[int, int] | None:
    """Extrae factores de N dado el período r de a^x mod N."""
    if r % 2 == 1:
        return None  # período impar, no sirve
    candidate1 = gcd(a**(r//2) + 1, N)
    candidate2 = gcd(a**(r//2) - 1, N)
    for c in [candidate1, candidate2]:
        if 1 < c < N:
            return c, N // c
    return None

# Para N=15, a=7: el período es r=4
N, a = 15, 7
# Verificación clásica: 7^x mod 15
for x in range(8):
    print(f'  7^{x} mod 15 = {pow(7, x, 15)}')
```

---

## Quantum Period Finding: QPF

QPF usa la Transformada de Fourier Cuántica para encontrar el período de
f(x) = aˣ mod N. El circuito tiene dos registros:

- **Registro x (n₁ qubits):** inicializado en superposición uniforme.
- **Registro f (n₂ qubits):** almacena f(x) = aˣ mod N.

```
|0⟩^n₁ ──H^⊗n₁──────────────── QFT⁻¹ ──[medir]→ x̃ (fracción de r)
                    │
|0⟩^n₂ ───────── Uₐ(aˣ mod N) ───────── [medir] (descartado)
```

### Implementación para N=15, a=7

```python
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT
from qiskit.primitives import StatevectorSampler
import numpy as np

def oracle_a_mod_N(a: int, N: int, power: int, n_count: int) -> QuantumCircuit:
    """
    Puerta controlada-U^power donde U|y⟩ = |a·y mod N⟩.
    Implementación explícita para N=15, a=7 (período 4).
    """
    qc = QuantumCircuit(4)  # 4 qubits para el registro f (0..14 < 16)

    # U para a=7, N=15 es una permutación sobre {1,7,4,13,1,...} con período 4
    # Implementamos la multiplicación modular para potencias específicas
    if a == 7 and N == 15:
        if power % 4 == 1:  # 7^1 mod 15 = 7
            qc.x([0, 1, 2])   # |1⟩ → |7⟩ = |0111⟩
        elif power % 4 == 2:  # 7^2 mod 15 = 4
            qc.x(2)           # |1⟩ → |4⟩ = |0100⟩
        elif power % 4 == 3:  # 7^3 mod 15 = 13
            qc.x([0, 2, 3])   # |1⟩ → |13⟩ = |1101⟩
        # power % 4 == 0: 7^4 mod 15 = 1 → identidad
    return qc

def circuito_shor_n15(a: int = 7) -> QuantumCircuit:
    """Circuito de Shor para N=15 con n_count=8 qubits de conteo."""
    n_count = 8   # qubits de conteo (precisión de QFT)
    n_f     = 4   # qubits para el registro f (2^4 = 16 > N=15)

    qc = QuantumCircuit(n_count + n_f, n_count)

    # Inicializar registro f en |1⟩
    qc.x(n_count)  # q_n_count = qubit 8 → |1⟩

    # Hadamard en registro de conteo
    qc.h(range(n_count))

    # Puertas Controlled-U^{2^j} para j = 0, ..., n_count-1
    for j in range(n_count):
        power = 2**j
        ctrl_u = oracle_a_mod_N(a, 15, power, n_count).control(1)
        qc.append(ctrl_u, [j] + list(range(n_count, n_count + n_f)))

    # QFT inversa sobre el registro de conteo
    qft_inv = QFT(n_count, inverse=True)
    qc.append(qft_inv, range(n_count))

    # Medición
    qc.measure(range(n_count), range(n_count))
    return qc

# Ejecutar
qc_shor = circuito_shor_n15(a=7)
print(f'Circuito de Shor para N=15, a=7:')
print(f'  Qubits totales:  {qc_shor.num_qubits}')
print(f'  Profundidad:     {qc_shor.depth()}')
print(f'  Puertas totales: {qc_shor.size()}')
```

---

## Interpretación de resultados: fracciones continuas

La medición da x̃/2^n ≈ k/r. Para obtener r, usamos el **algoritmo de fracciones continuas**.

```python
from fractions import Fraction

def fracciones_continuas(phi: float, n_bits: int, N: int) -> int | None:
    """
    Encuentra el período r dado phi ≈ k/r (fracción de la QFT).
    phi es el resultado de la medición normalizado por 2^n_bits.
    """
    frac = Fraction(phi).limit_denominator(N)
    r = frac.denominator
    return r if r > 0 else None

# Para N=15, a=7: los resultados de la QFT son 0, 64, 128, 192 (de 256 posibles)
n_count = 8
resultados_esperados = [0, 64, 128, 192]

print('\nInterpretación de resultados de QFT:')
print(f'{"Medición":>8} | {"phi":>8} | {"k/r aprox":>12} | {"r candidato":>12}')
print('-' * 50)
for m in resultados_esperados:
    phi = m / (2**n_count)
    frac = Fraction(phi).limit_denominator(15)
    r = frac.denominator
    print(f'{m:>8} | {phi:>8.4f} | {str(frac):>12} | {r:>12}')

# Extracción de factores con r=4
r = 4
print(f'\nPeríodo encontrado: r = {r}')
factores = extraer_factores(15, 7, r)
print(f'Factores de 15: {factores}')
```

---

## Recursos reales del algoritmo de Shor

### Para N de n bits (n = ⌈log₂N⌉):

| Recurso | Fórmula | N=15 (n=4) | RSA-512 (n=512) | RSA-2048 (n=2048) |
|---|---|---|---|---|
| Qubits lógicos | ~2n + 3 | 11 | ~1027 | ~4099 |
| Qubits físicos (d=25) | ~2000×n | 8000 | ~1M | ~4M |
| Puertas T | ~8n³ | 512 | ~1.7×10⁹ | ~6.9×10¹⁰ |
| Tiempo (1μs/puerta) | ~8n³ μs | 0.5 ms | 28 min | 19 horas |

```python
import numpy as np

def recursos_shor(n_bits: int, T1_us: float = 200, t_ciclo_us: float = 1.0,
                  d_codigo: int = 25, overhead_fisico: int = 2000) -> dict:
    """Estima recursos fault-tolerant para Shor con n bits."""
    n_qubits_logicos = 2*n_bits + 3
    n_T_gates        = 8 * n_bits**3
    n_qubits_fisicos = overhead_fisico * d_codigo * n_qubits_logicos
    t_total_us       = n_T_gates * t_ciclo_us
    t_total_horas    = t_total_us / 3.6e9

    # Verificar que T_total << T1 del qubit lógico
    T1_logico_us = T1_us * (1/0.001)**(d_codigo // 2)  # mejora exponencial
    n_ciclos      = t_total_us / t_ciclo_us

    return {
        'n_bits': n_bits,
        'q_logicos': n_qubits_logicos,
        'q_fisicos': n_qubits_fisicos,
        'T_gates': n_T_gates,
        't_horas': t_total_horas,
        'factible_T2': t_total_us < T1_logico_us,
    }

print(f'\nEstimación de recursos para Shor:')
print(f'{"N":>12} | {"n":>6} | {"q_log":>7} | {"q_fis":>10} | {"T_gates":>12} | {"Tiempo":>12}')
print('-' * 70)
for N_val in [15, 2**16, 2**128, 2**512, 2**2048]:
    n = int(np.ceil(np.log2(N_val)))
    r = recursos_shor(n)
    t_str = f'{r["t_horas"]:.1f}h' if r["t_horas"] < 1000 else f'{r["t_horas"]/8760:.1f}años'
    print(f'{N_val:>12.2e} | {n:>6} | {r["q_logicos"]:>7} | {r["q_fisicos"]:>10.2e} | {r["T_gates"]:>12.2e} | {t_str:>12}')
```

---

## El algoritmo de Shor honestamente: ¿cuándo es útil?

**RSA-2048** se usa actualmente en el 95% de las conexiones TLS.
Para romperlo con Shor en tiempo útil (< 24 horas):

- Se necesitan ~4000 qubits **lógicos** con error lógico < 10⁻¹⁰.
- Con código de superficie d=25 y p_físico = 0.1%: **~20 millones de qubits físicos**.
- A velocidad de ciclo de 1 μs: **~7 horas** de computación.

El plazo de amenaza real: los expertos estiman que RSA-2048 estará en riesgo
cuando se logren **1000+ qubits lógicos** de alta calidad, estimado en 2030-2035.

---

**Referencias:**
- Shor, *FOCS* 1994 — algoritmo original
- Kitaev, *Russ. Math. Surv.* 52, 1191 (1997) — QPE moderno
- Beauregard, *Quantum Inf. Comput.* 3, 175 (2003) — circuito eficiente
- Gidney & Ekerå, *Quantum* 5, 433 (2021) — análisis de recursos modernos
