# HHL: Algoritmo Cuántico para Sistemas Lineales

**Módulo 33 · Artículo 2 · Nivel muy avanzado**

---

## El problema: Ax = b

Dado un sistema de ecuaciones lineales Ax = b donde:
- A es una matriz Hermítica de N×N (N = 2^n)
- b es un vector conocido
- x es el vector solución desconocido

El objetivo de HHL es preparar el estado cuántico |x⟩ ∝ A⁻¹|b⟩.

**Complejidad clásica:** O(N·κ) con gradiente conjugado, donde κ = λ_max/λ_min
es el número de condición. Para N=10⁶ y κ=10⁶: O(10¹²) operaciones.

**Complejidad HHL (Harrow, Hassidim, Lloyd 2009):** O(log(N)·κ²·poly(1/ε))
— exponencialmente mejor en N, pero **polinomial en κ** (a veces peor que CG).

---

## Estructura del circuito HHL

```
|0⟩^n_c ──── QPE(A) ──── [rotación 1/λ] ──── QPE†(A) ──── [medir ancilla=1]
                │                                  │
|b⟩    ──── unitario ───────────────────────────────────── → |x⟩
                │
ancilla ──── Ry(2·arcsin(C/λ)) ────────────────────────────
```

Los pasos son:
1. **Codificación de b:** preparar |b⟩ = Σ b_j |j⟩.
2. **QPE(A):** estimar eigenvalores λ_j de A en un registro auxiliar.
3. **Rotación condicional:** rotar una ancilla en ángulo 2·arcsin(C/λ_j).
4. **QPE†(A):** descomputar el registro de eigenvalores.
5. **Post-selección:** medir ancilla = 1 → el registro principal contiene |x⟩.

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import PhaseEstimation
from qiskit.quantum_info import Statevector

def hhl_2x2(A: np.ndarray, b: np.ndarray, n_clock: int = 4) -> dict:
    """
    HHL para sistema 2×2 con A Hermítica.
    Implementación didáctica — no escalable pero ilustra todos los pasos.

    A debe ser Hermítica, b normalizado.
    """
    assert A.shape == (2, 2), "Solo para sistemas 2×2"
    assert abs(np.linalg.norm(b) - 1.0) < 1e-10, "b debe estar normalizado"

    # Solución clásica de referencia
    x_clasico = np.linalg.solve(A, b)
    x_clasico_norm = x_clasico / np.linalg.norm(x_clasico)

    # Eigenvalores y eigenvectores
    eigenvals, eigenvecs = np.linalg.eigh(A)
    kappa = abs(eigenvals[-1]) / abs(eigenvals[0])

    # En HHL el circuito real necesita Hamiltonian simulation e(iAt)
    # Aquí verificamos la lógica clásica del algoritmo
    # El estado solución en base de eigenvectores:
    # |b⟩ = Σ β_j |u_j⟩  →  A⁻¹|b⟩ = Σ β_j/λ_j |u_j⟩

    beta = eigenvecs.T @ b  # coeficientes de b en base de eigenvectores
    x_hhl_coefs = beta / eigenvals
    x_hhl = eigenvecs @ x_hhl_coefs
    x_hhl_norm = x_hhl / np.linalg.norm(x_hhl)

    fidelidad = abs(np.dot(x_hhl_norm.conj(), x_clasico_norm))**2

    return {
        'kappa': kappa,
        'eigenvalores': eigenvals,
        'solucion_clasica': x_clasico,
        'solucion_hhl': x_hhl,
        'fidelidad': fidelidad,
    }

# Ejemplo: A = [[3/2, 1/2], [1/2, 3/2]], b = [1, 0]/‖‖
A = np.array([[1.5, 0.5], [0.5, 1.5]])
b = np.array([1.0, 0.0])

r = hhl_2x2(A, b)
print(f'Sistema 2×2: κ = {r["kappa"]:.2f}')
print(f'Eigenvalores: {r["eigenvalores"]}')
print(f'Solución clásica: {r["solucion_clasica"]}')
print(f'Solución HHL:     {r["solucion_hhl"]}')
print(f'Fidelidad: {r["fidelidad"]:.6f}')
```

---

## QPE para la simulación hamiltoniana

La clave de HHL es la simulación e^{iAt}: A actúa como Hamiltoniano durante tiempo t.

```python
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT
import numpy as np

def hhl_circuito_2x2(t: float = np.pi, n_clock: int = 3) -> QuantumCircuit:
    """
    Circuito HHL completo para A = [[1.5, 0.5], [0.5, 1.5]], b = |0⟩.

    - 1 qubit para b (registro de sistema)
    - n_clock qubits para eigenvalores (registro de fase)
    - 1 qubit ancilla para la rotación 1/λ

    Eigenvalores de A: λ₁=1, λ₂=2.
    Con t = π: las fases son e^{i·1·π} = -1 y e^{i·2·π} = 1.
    → La QPE mide 1/2 y 1 en el registro de fase.
    """
    n_sys    = 1  # qubit del sistema
    n_anc    = 1  # ancilla para rotación

    # Total qubits: n_sys + n_clock + n_anc
    qc = QuantumCircuit(n_sys + n_clock + n_anc, n_anc)

    q_sys   = 0
    q_clk   = list(range(1, 1 + n_clock))
    q_anc   = n_clock + 1

    # Preparar |b⟩ = |0⟩ (ya está en |0⟩)
    # Para b = [1/√2, 1/√2]: qc.h(q_sys)

    # Hadamard en registro de fase
    qc.h(q_clk)

    # Controlled-e^{iAt·2^j} para j = 0..n_clock-1
    # Para A con λ₁=1, λ₂=2, t=π:
    #   e^{iAt}|u₁⟩ = e^{iπ}|u₁⟩ = -|u₁⟩  (fase π  → 1/2 del rango 2π)
    #   e^{iAt}|u₂⟩ = e^{2iπ}|u₂⟩ = |u₂⟩   (fase 2π → 0 mod 2π)
    #
    # Los eigenvectores son |u₁⟩=(|0⟩-|1⟩)/√2, |u₂⟩=(|0⟩+|1⟩)/√2
    # e^{iAt} en la base computacional es:
    #   exp(iπ * [[1.5, 0.5],[0.5, 1.5]]) ← usamos Z y I descomposición
    #
    # A = (3/2)I + (1/2)Z en espacio de 1 qubit
    # e^{iAt} = e^{i(3/2)πt} * e^{i(1/2)Zt}
    #
    # Para A = 1.5·I + 0.5·Z:
    # e^{iAt} = e^{1.5it} * Rz(-t)  (fase global + Rz)

    for j, q_j in enumerate(q_clk):
        power = 2**j
        theta = t * power  # ángulo para Rz en la simulación hamiltoniana
        # Controlled-e^{iA·t·2^j}:
        # Fase global e^{i·1.5·theta}: no controlable directamente, se ignora en estado puro
        # Parte unitaria: Controlled-Rz(-theta)
        qc.crz(-theta, q_j, q_sys)
        # Fase controlada adicional por la parte de identidad
        qc.cp(1.5 * theta, q_j, q_sys)

    # QFT inversa en el registro de fase
    qc.append(QFT(n_clock, inverse=True), q_clk)

    # --- Rotación condicional 1/λ (ancilla) ---
    # El registro de fase tiene ahora |λ̃⟩ en representación binaria.
    # Para λ=1: medimos 2^{n-1}/2^n = 1/2 → 1 en el bit más significativo.
    # Para λ=2: medimos 0 (fase entera).
    # La rotación Ry(2·arcsin(C/λ)) con C=1: C/λ₁=1, C/λ₂=0.5
    #
    # Implementación simplificada: Ry controlado por qubit de fase MSB
    # En el caso completo se necesita circuito de reciproco modular.
    C = 1.0
    # Para λ=2 (qubit MSB=1): θ = 2·arcsin(C/2) = 2·arcsin(0.5) = π/3
    # Para λ=1 (qubit MSB=0, bit siguiente=1): θ = 2·arcsin(1/1) = π
    theta_lambda2 = 2 * np.arcsin(C / 2)
    theta_lambda1 = 2 * np.arcsin(C / 1)

    # Rotación condicional en ancilla (simplificada para λ=2)
    qc.cry(theta_lambda2, q_clk[-1], q_anc)

    # Medición de ancilla
    qc.measure(q_anc, 0)

    # QPE inversa (descomputar)
    qc.append(QFT(n_clock, inverse=False), q_clk)

    # Controlled-e^{-iAt·2^j} inverso
    for j, q_j in enumerate(q_clk):
        power = 2**j
        theta = t * power
        qc.cp(-1.5 * theta, q_j, q_sys)
        qc.crz(theta, q_j, q_sys)

    qc.h(q_clk)

    return qc

qc_hhl = hhl_circuito_2x2()
print(f'Circuito HHL 2×2:')
print(f'  Qubits totales: {qc_hhl.num_qubits}')
print(f'  Profundidad:    {qc_hhl.depth()}')
print(f'  Puertas:        {qc_hhl.size()}')
```

---

## Ventaja cuántica de HHL: el análisis honesto

HHL promete una aceleración exponencial en N, pero con condiciones estrictas:

```python
import numpy as np
import matplotlib.pyplot as plt

def complejidad_hhl(N: int, kappa: float, epsilon: float) -> dict:
    """Complejidad de HHL vs métodos clásicos."""
    n = int(np.log2(N))

    # HHL: O(log(N) · κ² / ε)
    hhl = np.log2(N) * kappa**2 / epsilon

    # Gradiente Conjugado clásico: O(N · √κ · log(1/ε))
    cg = N * np.sqrt(kappa) * np.log(1/epsilon)

    # Direct (LU factorization): O(N^3)
    lu = N**3

    return {
        'N': N, 'kappa': kappa,
        'HHL': hhl,
        'CG_clasico': cg,
        'LU': lu,
        'hhl_gana_vs_CG': hhl < cg,
    }

print('Comparativa HHL vs Gradiente Conjugado:')
print(f'{"N":>10} | {"κ":>8} | {"HHL":>15} | {"CG":>15} | {"HHL gana?":>10}')
print('-' * 65)
for N in [100, 1000, 10000, 100000]:
    for kappa in [10, 100, 1000]:
        r = complejidad_hhl(N, kappa, epsilon=1e-6)
        print(f'{N:>10} | {kappa:>8} | {r["HHL"]:>15.2e} | {r["CG_clasico"]:>15.2e} | {str(r["hhl_gana_vs_CG"]):>10}')
    print()
```

### Las cuatro condiciones para que HHL tenga ventaja real

```python
condiciones_hhl = {
    '1. b debe codificarse eficientemente': {
        'descripcion': 'Preparar |b⟩ desde el vector clásico b cuesta O(N) en general.',
        'cuando_se_cumple': 'Si b tiene estructura sparse o se puede generar por circuito.',
        'coste': 'O(log N) si existe oráculo eficiente para |b⟩',
    },
    '2. A debe tener acceso cuántico eficiente (QRAM)': {
        'descripcion': 'La simulación hamiltoniana e^{iAt} requiere acceso a A.',
        'cuando_se_cumple': 'Si A es sparse con s entradas no cero por fila.',
        'coste': 'O(s · log²N / ε) con QRAM',
    },
    '3. Solo necesitas expectation values de |x⟩': {
        'descripcion': 'HHL da |x⟩, no el vector clásico x. Leer x cuesta O(N).',
        'cuando_se_cumple': 'Si el resultado es ⟨x|M|x⟩ para algún observador M.',
        'coste': 'O(1) si M es simple; O(N) si necesitas x completo',
    },
    '4. κ debe ser polinomial en log(N)': {
        'descripcion': 'HHL escala como κ² → si κ=√N, no hay ventaja sobre CG.',
        'cuando_se_cumple': 'Matrices bien condicionadas; precondicionamiento efectivo.',
        'ventaja_real': 'Solo cuando κ = O(poly(log N))',
    },
}

print('\n=== CONDICIONES PARA VENTAJA CUÁNTICA DE HHL ===\n')
for cond, info in condiciones_hhl.items():
    print(f'[{cond}]')
    for k, v in info.items():
        print(f'  {k}: {v}')
    print()
```

---

## Aplicaciones reales y sus limitaciones

```python
aplicaciones_hhl = [
    {
        'aplicacion': 'Machine Learning cuántico (QLS en regresión lineal)',
        'N_tipico': '10^6 - 10^9',
        'kappa_tipico': '10^3 - 10^6',
        'problema_1': 'QRAM no existe aún con escala práctica',
        'problema_2': 'Leer el resultado requiere O(N) → elimina ventaja',
        'veredicto': '❌ Sin ventaja práctica en general',
    },
    {
        'aplicacion': 'Simulación de fluidos (Navier-Stokes linealizado)',
        'N_tipico': '10^6',
        'kappa_tipico': 'Re (Reynolds) ~ 10^6',
        'problema_1': 'κ = Re hace que κ² sea enorme',
        'problema_2': 'Los fluidos turbulentos no son lineales',
        'veredicto': '⚠️  Solo para flujos laminares de baja Re',
    },
    {
        'aplicacion': 'Criptoanálisis (sistemas lineales sobre F_q)',
        'N_tipico': '2^512',
        'kappa_tipico': 'Variable',
        'problema_1': 'El modelo de black-box no aplica directamente',
        'problema_2': 'Shor es más relevante para criptografía',
        'veredicto': '⚠️  Nicho muy específico',
    },
    {
        'aplicacion': 'Portfolio optimization (QLS en finanzas)',
        'N_tipico': '10^3 - 10^4',
        'kappa_tipico': '10^2 - 10^3',
        'problema_1': 'N pequeño → ventaja exponencial no aplica',
        'problema_2': 'CG ya es muy rápido en este tamaño',
        'veredicto': '❌ CG clásico es suficiente',
    },
]

print('APLICACIONES DE HHL Y SU VIABILIDAD:')
print('-' * 80)
for app in aplicaciones_hhl:
    print(f'\n{app["aplicacion"]}')
    print(f'  N: {app["N_tipico"]}, κ: {app["kappa_tipico"]}')
    print(f'  Problema 1: {app["problema_1"]}')
    print(f'  Problema 2: {app["problema_2"]}')
    print(f'  Veredicto: {app["veredicto"]}')
```

---

## Recursos fault-tolerant para HHL

```python
import numpy as np

def recursos_hhl(N: int, kappa: float, epsilon: float,
                 s_sparse: int = 10) -> dict:
    """
    Estimación de recursos para HHL fault-tolerant.

    N: dimensión del sistema
    kappa: número de condición
    epsilon: precisión deseada en la solución
    s_sparse: número de entradas no cero por fila de A
    """
    n = int(np.ceil(np.log2(N)))
    n_clock = int(np.ceil(np.log2(kappa / epsilon)))  # qubits para QPE

    # Qubits lógicos
    n_qubits_sistema = n
    n_qubits_fase    = n_clock
    n_qubits_anc     = 1
    q_total = n_qubits_sistema + n_qubits_fase + n_qubits_anc

    # Puertas T (estimación)
    # QPE necesita ~O(s·log²N·n_clock) puertas Toffoli
    T_gates_qpe = s_sparse * (n**2) * n_clock
    T_gates_rot = n_clock  # rotaciones C/λ
    T_gates_total = 2 * T_gates_qpe + T_gates_rot  # QPE + QPE†

    # Overhead fault-tolerant (d=25)
    q_fisicos = 2000 * 25 * q_total
    t_total_us = T_gates_total * 1.0  # 1 μs por puerta T

    return {
        'N': N, 'n': n, 'kappa': kappa,
        'n_clock': n_clock,
        'q_logicos': q_total,
        'q_fisicos': q_fisicos,
        'T_gates': T_gates_total,
        't_horas': t_total_us / 3.6e9,
    }

print(f'\nRecursos HHL fault-tolerant (s=10 sparse, ε=10⁻⁶):')
print(f'{"N":>10} | {"κ":>8} | {"n_clk":>6} | {"q_log":>7} | {"q_fis":>10} | {"T_gates":>12} | {"Tiempo"}')
print('-' * 75)
for N in [2**10, 2**20, 2**30]:
    for kappa in [100, 10000]:
        r = recursos_hhl(N, kappa, 1e-6)
        t = f'{r["t_horas"]:.1f}h' if r["t_horas"] < 1000 else f'{r["t_horas"]/8760:.1f}años'
        print(f'{N:>10.2e} | {kappa:>8} | {r["n_clock"]:>6} | {r["q_logicos"]:>7} | {r["q_fisicos"]:>10.2e} | {r["T_gates"]:>12.2e} | {t}')
```

---

## El veredicto honesto sobre HHL

```
┌─────────────────────────────────────────────────────────────────┐
│  HHL TIENE VENTAJA EXPONENCIAL cuando TODAS se cumplen:         │
│                                                                  │
│  ✅  N >> 1 (millones de variables)                              │
│  ✅  κ = O(poly(log N)) — sistema bien condicionado              │
│  ✅  Existe oráculo cuántico eficiente para A y b                │
│  ✅  Solo necesitas ⟨x|M|x⟩, no el vector completo x            │
│  ✅  La precisión ε no necesita ser exponencialmente pequeña     │
│                                                                  │
│  En la práctica, estas condiciones raramente se cumplen todas.   │
│  Los mejores candidatos: simulación de física de muchos cuerpos, │
│  sistemas lineales con estructura algebraica conocida, y         │
│  subroutinas de algoritmos cuánticos más grandes.                │
└─────────────────────────────────────────────────────────────────┘
```

---

**Referencias:**
- Harrow, Hassidim & Lloyd, *Phys. Rev. Lett.* 103, 150502 (2009) — HHL original
- Aaronson, *Nature Phys.* 11, 291 (2015) — "Read the fine print" (crítica honesta)
- Childs et al., *SIAM J. Comp.* 46, 1920 (2017) — quantum linear systems survey
- Babbush et al., *npj Quantum Inf.* 7, 173 (2021) — análisis de recursos FT para HHL
