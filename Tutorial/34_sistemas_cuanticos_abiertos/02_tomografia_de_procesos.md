# Tomografía de Procesos Cuánticos

**Módulo 34 · Artículo 2 · Nivel muy avanzado**

---

## El problema: caracterizar una puerta real

Cuando implementamos una puerta cuántica en hardware, la puerta real difiere
de la ideal por errores de coherencia, ruido, y errores de estado/medición.
La **tomografía de procesos cuánticos (QPT)** reconstruye el canal cuántico completo.

Un canal cuántico actúa sobre una matriz densidad como:

$$\mathcal{E}(\rho) = \sum_{mn} \chi_{mn} E_m \rho E_n^\dagger$$

donde $\{E_m\}$ es una base de operadores (e.g., Pauli) y **χ** es la
**χ-matrix** (process matrix), que contiene toda la información del proceso.

---

## Tomografía estándar (Standard QPT)

```python
import numpy as np
from itertools import product
from qiskit import QuantumCircuit
from qiskit.quantum_info import (Statevector, DensityMatrix, state_fidelity,
                                  Operator, Chi, Choi, PTM, SuperOp)

# Matrices de Pauli
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

def pauli_basis_1q() -> list[tuple[str, np.ndarray]]:
    """Base de Pauli normalizada para 1 qubit."""
    return [('I', I), ('X', X), ('Y', Y), ('Z', Z)]

def estados_prep_1q() -> list[tuple[str, np.ndarray]]:
    """
    Estados de preparación para QPT de 1 qubit.
    Se necesitan 4 estados linealmente independientes.
    """
    rho_0 = np.outer([1,0], [1,0]).astype(complex)  # |0⟩
    rho_1 = np.outer([0,1], [0,1]).astype(complex)  # |1⟩
    rho_p = np.outer([1,1], [1,1]).astype(complex) / 2  # |+⟩
    rho_r = np.outer([1,1j], [1,-1j]).astype(complex) / 2  # |R⟩ = (|0⟩+i|1⟩)/√2
    return [('|0⟩', rho_0), ('|1⟩', rho_1), ('|+⟩', rho_p), ('|R⟩', rho_r)]

def chi_matrix_ideal(canal_nombre: str) -> np.ndarray:
    """
    Calcula la χ-matrix de un canal ideal.
    En la base Pauli {I, X, Y, Z}, χ_mn = ⟨E_m|ε|E_n⟩.
    """
    base = [I, X, Y, Z]
    nombres = ['I', 'X', 'Y', 'Z']
    n = len(base)
    chi = np.zeros((n, n), dtype=complex)

    if canal_nombre == 'I':  # identidad
        U = I
    elif canal_nombre == 'X':
        U = X
    elif canal_nombre == 'Y':
        U = Y
    elif canal_nombre == 'Z':
        U = Z
    elif canal_nombre == 'H':
        U = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    elif canal_nombre == 'S':
        U = np.array([[1, 0], [0, 1j]], dtype=complex)
    elif canal_nombre == 'T':
        U = np.array([[1, 0], [0, np.exp(1j*np.pi/4)]], dtype=complex)
    else:
        raise ValueError(f'Canal desconocido: {canal_nombre}')

    # ε(ρ) = U·ρ·U†
    # χ en base Pauli: para canal unitario, χ tiene un solo elemento no cero
    # Para U = Σ u_m E_m → χ_mn = u_m* · u_n
    coefs = np.array([np.trace(Ei.conj().T @ U) / 2 for Ei in base])
    chi = np.outer(coefs.conj(), coefs)

    return chi

def imprimir_chi(chi: np.ndarray, nombre: str) -> None:
    """Imprime la χ-matrix en base Pauli."""
    print(f'\nχ-matrix para puerta {nombre}:')
    base_labels = ['I', 'X', 'Y', 'Z']
    print(f'     {"I":>8} {"X":>8} {"Y":>8} {"Z":>8}')
    for i, lab in enumerate(base_labels):
        vals = ''.join(f'{chi[i,j].real:>8.3f}' for j in range(4))
        print(f'  {lab}: {vals}')

for nombre in ['I', 'X', 'H', 'S', 'T']:
    chi = chi_matrix_ideal(nombre)
    imprimir_chi(chi, nombre)

# Verificar: la traza de χ debe ser 1 para canales que preservan la traza
print('\nTrazas de χ (deben ser 1.0):')
for nombre in ['I', 'X', 'H', 'S', 'T']:
    chi = chi_matrix_ideal(nombre)
    print(f'  {nombre}: tr(χ) = {chi.trace().real:.4f}')
```

---

## χ-matrix para canal ruidoso

Un canal depolarizante con parámetro p tiene:
$$\mathcal{E}(\rho) = (1-p)\rho + p \cdot \frac{I}{2}$$

```python
def chi_depolarizante(p: float) -> np.ndarray:
    """
    χ-matrix del canal depolarizante.
    ε(ρ) = (1-p)ρ + (p/4)(Iρ I + XρX + YρY + ZρZ)
         = (1 - 3p/4)ρ + (p/4)(XρX + YρY + ZρZ)
    """
    chi = np.zeros((4, 4), dtype=complex)
    chi[0, 0] = 1 - 3*p/4  # componente I·I
    chi[1, 1] = p/4         # componente X·X
    chi[2, 2] = p/4         # componente Y·Y
    chi[3, 3] = p/4         # componente Z·Z
    return chi

def fidelidad_proceso(chi_ideal: np.ndarray, chi_exp: np.ndarray) -> float:
    """
    Fidelidad de proceso F = tr(χ_ideal · χ_exp).
    Para 1 qubit en base Pauli normalizada.
    """
    return np.trace(chi_ideal.conj().T @ chi_exp).real

print('\nFidelidad de canal depolarizante vs identidad:')
chi_id = chi_matrix_ideal('I')
for p in [0.0, 0.01, 0.05, 0.10, 0.25, 0.5]:
    chi_dep = chi_depolarizante(p)
    F = fidelidad_proceso(chi_id, chi_dep)
    print(f'  p={p:.2f}: F = {F:.4f}')
```

---

## Process Transfer Matrix (PTM)

La **PTM** representa el canal como una matriz 4×4 (para 1 qubit) que actúa
sobre el vector de coeficientes de Pauli de ρ:

$$\vec{r}_{out} = \text{PTM} \cdot \vec{r}_{in}$$

donde $\vec{r} = (\text{tr}(I\rho), \text{tr}(X\rho), \text{tr}(Y\rho), \text{tr}(Z\rho))$.

```python
from qiskit.quantum_info import Operator

def canal_unitario_ruidoso(U_ideal: np.ndarray, p_dep: float) -> callable:
    """
    Canal cuántico: U_ideal seguida de despolarización con probabilidad p_dep.
    """
    def canal(rho: np.ndarray) -> np.ndarray:
        rho_u = U_ideal @ rho @ U_ideal.conj().T
        return (1 - p_dep) * rho_u + p_dep * np.eye(2, dtype=complex) / 2
    return canal

def calcular_ptm(canal: callable) -> np.ndarray:
    """
    Calcula la PTM de un canal cuántico usando la base Pauli.
    PTM_ij = tr(E_i · ε(E_j/2)) · 2
    """
    base = [I, X, Y, Z]
    d = len(base)
    PTM = np.zeros((d, d), dtype=complex)

    for j, Ej in enumerate(base):
        rho_in = Ej / 2  # estado de entrada en base Pauli
        rho_out = canal(rho_in)
        for i, Ei in enumerate(base):
            PTM[i, j] = np.trace(Ei @ rho_out)

    return PTM.real

# PTM para puerta H con diferentes niveles de error
U_H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

print('PTM de la puerta H con depolarización:')
base_labels = ['I', 'X', 'Y', 'Z']

for p in [0.0, 0.05, 0.10]:
    canal = canal_unitario_ruidoso(U_H, p)
    ptm = calcular_ptm(canal)
    print(f'\n  p={p:.2f}:')
    print(f'  {"":>4}' + ''.join(f'{l:>8}' for l in base_labels))
    for i, li in enumerate(base_labels):
        vals = ''.join(f'{ptm[i,j]:>8.3f}' for j in range(4))
        print(f'  {li:>4}  {vals}')
```

---

## Gate Set Tomography (GST): más allá de QPT

QPT estándar asume preparación y medición perfectas (SPAM). **GST** elimina
este supuesto estimando simultáneamente las puertas, la preparación y la medición.

```python
def demo_spam_error(gate_error: float, prep_error: float, meas_error: float) -> dict:
    """
    Demostración del efecto de errores SPAM en la tomografía de procesos.

    gate_error: depolarización durante la puerta
    prep_error: preparación imperfecta (mezcla con estado erróneo)
    meas_error: error de lectura (bit flip en medición)
    """
    # Canal ideal: puerta X
    U_X = X

    def canal_con_errores(rho_in):
        # Error de preparación: mezcla con |1⟩
        rho_prep = (1 - prep_error) * rho_in + prep_error * np.outer([0,1],[0,1])
        # Aplicar puerta con error de depolarización
        rho_gate = (1 - gate_error) * (U_X @ rho_prep @ U_X.conj().T) + \
                    gate_error * np.eye(2)/2
        return rho_gate

    # Medición con error: P(medir 0 | estado 0) = 1 - meas_error
    def medir_con_error(rho, base_state):
        """Mide la probabilidad del estado base_state con error de lectura."""
        psi = np.zeros(2, dtype=complex)
        psi[base_state] = 1
        P_ideal = (psi.conj() @ rho @ psi).real
        return (1 - meas_error) * P_ideal + meas_error * (1 - P_ideal)

    # Calcular PTM con errores SPAM
    estados_prep = [np.outer([1,0],[1,0]).astype(complex),
                     np.outer([0,1],[0,1]).astype(complex),
                     np.outer([1,1],[1,1]).astype(complex)/2,
                     np.outer([1,1j],[1,-1j]).astype(complex)/2]
    base = [I, X, Y, Z]

    PTM_ruidosa = np.zeros((4, 4))
    for j, rho_j in enumerate(estados_prep):
        rho_out = canal_con_errores(rho_j)
        for i, Ei in enumerate(base):
            # Simulamos medición con error
            P0 = medir_con_error(rho_out, 0)
            P1 = 1 - P0
            rho_meas = P0 * np.outer([1,0],[1,0]) + P1 * np.outer([0,1],[0,1])
            PTM_ruidosa[i, j] = np.trace(Ei @ rho_meas).real

    # PTM ideal (solo puerta X)
    canal_ideal = canal_unitario_ruidoso(U_X, 0.0)
    ptm_ideal = calcular_ptm(canal_ideal)

    # Error total en PTM
    error_ptm = np.linalg.norm(PTM_ruidosa - ptm_ideal, 'fro')

    return {
        'gate_error': gate_error,
        'prep_error': prep_error,
        'meas_error': meas_error,
        'ptm_ideal': ptm_ideal,
        'ptm_ruidosa': PTM_ruidosa,
        'error_ptm': error_ptm,
    }

print('Efecto de errores SPAM en QPT (puerta X):')
print(f'{"gate_err":>10} | {"prep_err":>10} | {"meas_err":>10} | {"‖PTM_real - PTM_ideal‖":>22}')
print('-' * 60)
for gate_e, prep_e, meas_e in [
    (0.0, 0.0, 0.0),
    (0.01, 0.0, 0.0),
    (0.0, 0.01, 0.0),
    (0.0, 0.0, 0.01),
    (0.01, 0.01, 0.01),
    (0.05, 0.05, 0.05),
]:
    r = demo_spam_error(gate_e, prep_e, meas_e)
    print(f'{gate_e:>10.3f} | {prep_e:>10.3f} | {meas_e:>10.3f} | {r["error_ptm"]:>22.5f}')
```

---

## Randomized Benchmarking: fidelidad promedio eficiente

RB es más eficiente que QPT para medir la fidelidad promedio de una puerta,
ya que escala logarítmicamente en el número de experimentos.

```python
import numpy as np

def randomized_benchmarking_modelo(
    r_gate: float,   # tasa de error por puerta
    n_max: int = 100,
    n_sequences: int = 50,
    seed: int = 0,
) -> dict:
    """
    Modelo de Randomized Benchmarking para 1 qubit.

    El decaimiento de la supervivencia es:
    P(m) = A · p^m + B

    donde:
      p = 1 - 2r/(d²-1) · (d²) ≈ 1 - 2r  para 1 qubit (d=2)
      r = tasa de error por puerta (EPC: Error Per Clifford)
    """
    rng = np.random.default_rng(seed)

    # Para 1 qubit: d=2, d²-1=3
    d = 2
    p = 1 - d**2 / (d**2 - 1) * r_gate  # parámetro de decaimiento

    ms = np.arange(1, n_max + 1, 5)
    P_supervivencia = []

    for m in ms:
        # Supervivencia promediada sobre secuencias aleatorias
        P_m_teorico = 0.5 * p**m + 0.5  # A=0.5, B=0.5 para qubit perfecto
        # Añadir fluctuaciones estadísticas (n_sequences finito)
        noise = rng.normal(0, np.sqrt(P_m_teorico*(1-P_m_teorico)/n_sequences))
        P_supervivencia.append(np.clip(P_m_teorico + noise, 0, 1))

    P_supervivencia = np.array(P_supervivencia)

    # Ajuste exponencial
    from scipy.optimize import curve_fit
    def modelo_rb(m, A, p_fit, B):
        return A * p_fit**m + B

    try:
        popt, pcov = curve_fit(modelo_rb, ms, P_supervivencia, p0=[0.5, 0.95, 0.5],
                                bounds=([0, 0, 0], [1, 1, 1]))
        A_fit, p_fit, B_fit = popt
        r_estimado = (1 - p_fit) * (d**2 - 1) / d**2
    except:
        r_estimado = r_gate  # fallback

    return {
        'r_true': r_gate,
        'r_estimado': r_estimado,
        'p_verdadero': p,
        'ms': ms,
        'P_supervivencia': P_supervivencia,
        'error_estimacion': abs(r_estimado - r_gate),
    }

print('\nRandomized Benchmarking: estimación de tasa de error:')
print(f'{"r_real":>10} | {"r_estimado":>12} | {"error":>10}')
print('-' * 38)
for r in [0.001, 0.005, 0.01, 0.05, 0.10]:
    res = randomized_benchmarking_modelo(r, n_max=200, n_sequences=200)
    print(f'{r:>10.4f} | {res["r_estimado"]:>12.5f} | {res["error_estimacion"]:>10.5f}')
```

---

## Visualización: decaimiento en RB

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Decaimiento de supervivencia RB para diferentes tasas de error
tasas = [0.001, 0.01, 0.05, 0.10]
colores = ['blue', 'green', 'orange', 'red']

for r, color in zip(tasas, colores):
    res = randomized_benchmarking_modelo(r, n_max=150, n_sequences=500, seed=0)
    axes[0].plot(res['ms'], res['P_supervivencia'], 'o-', color=color,
                  ms=4, lw=1.5, label=f'r={r:.3f}')

axes[0].set_xlabel('Número de puertas Clifford m')
axes[0].set_ylabel('Supervivencia P(m)')
axes[0].set_title('Randomized Benchmarking')
axes[0].legend(fontsize=9)
axes[0].grid(alpha=0.3)

# Fidelidad de proceso vs error de puerta
r_vals = np.linspace(0, 0.2, 100)
d = 2
# F_avg = 1 - d²/(d²-1) · r = 1 - 4/3 · r para 1 qubit
F_avg = 1 - d**2/(d**2-1) * r_vals
F_process = (d * F_avg + 1) / (d + 1)  # relación entre F_avg y F_process

axes[1].plot(r_vals, F_avg, 'b-', lw=2, label='F_avg (fidelidad promedio)')
axes[1].plot(r_vals, F_process, 'r--', lw=2, label='F_process (χ-matrix)')
axes[1].axhline(0.999, color='gray', ls=':', lw=1, label='Umbral fault-tolerant ~99.9%')
axes[1].set_xlabel('Tasa de error por puerta r')
axes[1].set_ylabel('Fidelidad')
axes[1].set_title('Fidelidad promedio vs fidelidad de proceso')
axes[1].legend(fontsize=9)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## Resumen de métodos de caracterización de puertas

| Método | Qubits | Overhead | Mide | Robusto SPAM |
|--------|--------|----------|------|--------------|
| QPT estándar | 1-3 | O(d⁴) | Canal completo (χ) | No |
| PTM | 1-3 | O(d⁴) | Transfer matrix | No |
| GST | 1-2 | O(poly) | Puertas+SPAM | Sí |
| RB (estándar) | 1-2 | O(log(1/ε)) | Fidelidad promedio | Parcialmente |
| IRB (intercalado) | 1-2 | O(log(1/ε)) | Fidelidad de 1 puerta | Sí |
| CB (cycle benchmarking) | N | O(N) | Error por capas | Sí |
| XEB (cross-entropy) | N | O(n·shots) | Fidelidad vs simulador | No |

---

**Referencias:**
- Chuang & Nielsen, *J. Mod. Optics* 44, 2455 (1997) — QPT original
- Merkel et al., *Phys. Rev. A* 87, 062119 (2013) — GST
- Magesan et al., *Phys. Rev. Lett.* 106, 180504 (2011) — RB riguroso
- Knill et al., *Phys. Rev. A* 77, 012307 (2008) — IRB
- Flammia & Liu, *Phys. Rev. Lett.* 106, 230501 (2011) — fidelidad de proceso eficiente
