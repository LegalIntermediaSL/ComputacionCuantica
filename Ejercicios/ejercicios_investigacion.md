# Ejercicios de Investigación — Nivel Fronteras del Campo

**Módulos 38-40 · 8 problemas · Nivel investigación**

Estos ejercicios conectan con resultados publicados en los últimos cinco años.
Cada problema pide demostrar, implementar o extender un resultado no trivial.
Se espera familiaridad con todos los módulos anteriores.

---

## Problema R1 — QSVT: Aproximación polinómica óptima

La QSVT requiere aproximar una función $f: [-1,1] \to [-1,1]$ con un polinomio
de Chebyshev de paridad definida. El **teorema de Chebyshev** dice que el polinomio
de grado $d$ que minimiza el error uniforme es el polinomio de Chebyshev reescalado.

**Parte a)** Implementa el error de aproximación de Chebyshev para la función
$f(x) = \text{sgn}(x)$ en función del grado $d$ del polinomio (solo grados impares).
Muestra que el error converge como $\varepsilon_d \approx e^{-\pi^2 d / (4 \ln(1/\delta))}$
para $|x| > \delta$.

```python
import numpy as np
import matplotlib.pyplot as plt

def error_aprox_chebyshev(f, d_max: int, x_vals: np.ndarray) -> list[float]:
    """
    Calcula el error de aproximación de Chebyshev de grado d para f en x_vals.
    Devuelve lista de errores máximos para d = 1, 3, 5, ..., d_max.
    """
    errores = []
    # Tu implementación aquí
    # 1. Calcular la base de Chebyshev T_0, T_1, ..., T_d
    # 2. Resolver mínimos cuadrados para coeficientes
    # 3. Evaluar el polinomio y calcular error máximo
    return errores

x = np.linspace(-1, 1, 500)
x_nozero = x[np.abs(x) > 0.1]
f_sgn = lambda x: np.sign(x + 1e-15)

# Plotear error vs grado
# ...
```

**Parte b)** ¿Cuántos queries a $U_A$ necesita QSVT para implementar $\text{sgn}(A)$
con error $\varepsilon = 10^{-4}$ en el rango $\sigma_k \in [0.1, 1]$?

**Parte c)** Compara con el algoritmo LCU-Taylor para la misma función.
¿Cuándo es QSVT más eficiente?

**Referencia:** Martyn et al., *PRX Quantum* 2, 040203 (2021), Sec. IV.

---

## Problema R2 — Block-Encoding: construcción explícita

Dada una matriz dispersa $A \in \mathbb{C}^{4\times 4}$ con $\|A\|_{\max} \leq 1$,
construye su block-encoding en un circuito Qiskit.

**Definición:** $U_A$ es una $(n+a)$-qubit unitaria tal que:
$$(\langle 0|^{\otimes a} \otimes I)\ U_A\ (|0\rangle^{\otimes a} \otimes I) = \frac{A}{\alpha}$$

**Parte a)** Para $A = \frac{1}{2}\begin{pmatrix}1&0&0&1\\0&1&1&0\\0&1&-1&0\\1&0&0&-1\end{pmatrix}$,
verifica que $\|A\| \leq 1$ y construye $U_A$ como circuito de 4 qubits (2 ancilla + 2 sistema).

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
import numpy as np

A = np.array([[1,0,0,1],[0,1,1,0],[0,1,-1,0],[1,0,0,-1]], dtype=complex) / 2

def block_encoding(A: np.ndarray) -> QuantumCircuit:
    """
    Construye la block-encoding de A usando preparación de estado + SWAP test.
    Parámetros: A de 4×4, norma ≤ 1.
    Retorna: circuito de 4 qubits donde los 2 primeros son ancilla.
    """
    # Tu implementación aquí
    pass

qc_be = block_encoding(A)
U = Operator(qc_be).data
# Verificar: la submatriz superior izquierda (4×4) de U debe ser proporcional a A
print("Block-encoding correcta:", np.allclose(U[:4, :4], A, atol=1e-10))
```

**Parte b)** Verifica la correctitud extrayendo la submatriz con `Operator(qc).data[:4,:4]`.

**Parte c)** ¿Cuántos ancilla qubits necesitas para una matriz $2^n \times 2^n$ general?

**Referencia:** Gilyen et al., *STOC 2019*, Lemma 48.

---

## Problema R3 — Barren Plateaus: escalado con qubits

Los barren plateaus hacen que la varianza del gradiente decaiga exponencialmente
con el número de qubits en ansätze aleatorios profundos.

**Teorema (McClean 2018):** Para circuitos 2-diseño con $n$ qubits y profundidad $L$:
$$\text{Var}[\partial_k E] = \mathcal{O}(b^{-n}) \quad b > 1$$

**Parte a)** Verifica experimentalmente el escalado para $n \in \{2, 4, 6, 8\}$ qubits
con el Hamiltoniano Ising 1D. Usa 100 puntos aleatorios por configuración.

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorEstimator

def hamiltoniano_ising(n: int, J: float = 1.0, h: float = 0.5) -> SparsePauliOp:
    """H = -J Σ ZᵢZᵢ₊₁ - h Σ Xᵢ"""
    terms = []
    for i in range(n - 1):
        op = 'I'*i + 'ZZ' + 'I'*(n-i-2)
        terms.append((op, -J))
    for i in range(n):
        op = 'I'*i + 'X' + 'I'*(n-i-1)
        terms.append((op, -h))
    return SparsePauliOp.from_list(terms)

def varianza_gradiente(n: int, n_capas: int, n_samples: int = 100) -> float:
    """Estima Var[∂E/∂θ₀] para un ansatz aleatorio."""
    # Tu implementación aquí
    pass

# Replicar Figura 1 de McClean et al. (2018)
resultados = {}
for n in [2, 4, 6, 8]:
    var = varianza_gradiente(n, n_capas=n, n_samples=100)
    resultados[n] = var
    print(f'n={n}: Var(grad) = {var:.2e}')

# Ajuste exponencial
import scipy.stats
log_vars = [np.log(v) for v in resultados.values()]
slope, intercept, r, p, se = scipy.stats.linregress(list(resultados.keys()), log_vars)
print(f'\nEscalado: Var ∝ exp({slope:.3f}·n), base = {np.exp(slope):.3f}')
print(f'  (Teórico: base = 4/3 ≈ {4/3:.3f} para 2-diseño)')
```

**Parte b)** Compara el escalado con el que predice la teoría de diseños unitarios.

**Parte c)** ¿Cómo mitigarías el barren plateau? Propón y prueba una estrategia
(e.g., inicialización correlacionada, ansatz con estructura local).

**Referencia:** McClean et al., *Nat. Commun.* 9, 4812 (2018).

---

## Problema R4 — Error Mitigation: ZNE vs PEC

Compara Zero-Noise Extrapolation (ZNE) y Probabilistic Error Cancellation (PEC)
para el mismo circuito bajo ruido depolarizante.

**Parte a)** Implementa ZNE manual con amplificación de ruido por *folding* del circuito:
$\mathcal{E}_\lambda(U) = U \cdot (U^\dagger U)^{(\lambda-1)/2}$ para $\lambda = 1, 3, 5$.

```python
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp
import numpy as np

def fold_circuit(qc: QuantumCircuit, scale_factor: int) -> QuantumCircuit:
    """
    Amplificación de ruido por folding: U → U(U†U)^((λ-1)/2)
    scale_factor: 1, 3, 5 (debe ser impar)
    """
    assert scale_factor % 2 == 1, "scale_factor debe ser impar"
    qc_folded = qc.copy()
    extra = (scale_factor - 1) // 2
    for _ in range(extra):
        qc_folded.compose(qc.inverse(), inplace=True)
        qc_folded.compose(qc, inplace=True)
    return qc_folded

def zne_extrapolacion(E_vals: list[float], lambdas: list[int],
                      metodo: str = 'Richardson') -> float:
    """
    Extrapolación a λ=0 usando los valores E(λ).
    Métodos: 'Richardson' (polinómica), 'exponencial'
    """
    # Tu implementación aquí
    pass

# Circuito de prueba: Bell state con observable ZZ
qc = QuantumCircuit(2)
qc.h(0); qc.cx(0, 1)
H_obs = SparsePauliOp.from_list([('ZZ', 1.0)])

# Valor ideal
from qiskit.quantum_info import Statevector
psi = Statevector(qc)
E_ideal = psi.expectation_value(H_obs).real

# Simular con ruido y ZNE
p_err = 0.02
nm = NoiseModel()
nm.add_all_qubit_quantum_error(depolarizing_error(p_err, 1), ['h'])
nm.add_all_qubit_quantum_error(depolarizing_error(p_err*3, 2), ['cx'])

sim = AerSimulator(noise_model=nm)
# ... continúa la implementación

print(f'E ideal:    {E_ideal:.4f}')
# print(f'E ruidoso:  {E_ruidoso:.4f}')
# print(f'E ZNE:      {E_zne:.4f}')
```

**Parte b)** Calcula la mejora en fidelidad de ZNE vs sin mitigación para distintos
niveles de ruido $p \in [0.001, 0.05]$.

**Parte c)** Discute cuándo ZNE falla (ruido no perturbativo) y qué ventaja tiene PEC.

**Referencia:** Temme et al., *PRL* 119, 180509 (2017); Endo et al., *PRX* 8, 031027 (2018).

---

## Problema R5 — Quantum Sensing: límite de Heisenberg vs SQL

El límite cuántico de Cramér-Rao establece la precisión máxima de estimación de
un parámetro $\phi$ mediante $N$ copias de un estado cuántico.

**Parte a)** Muestra analítica y numéricamente que:
- **SQL** (Standard Quantum Limit): $\Delta\phi \geq 1/\sqrt{N}$ usando $N$ qubits en producto.
- **HL** (Heisenberg Limit): $\Delta\phi \geq 1/N$ usando el estado GHZ de $N$ qubits.

```python
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def qfi_estado_puro(psi: np.ndarray, H_generador: np.ndarray) -> float:
    """
    Información Cuántica de Fisher para estado puro |ψ⟩ y generador H.
    QFI = 4·(⟨H²⟩ - ⟨H⟩²) = 4·Var[H]
    """
    exp_H  = (psi.conj() @ H_generador @ psi).real
    exp_H2 = (psi.conj() @ (H_generador @ H_generador) @ psi).real
    return 4 * (exp_H2 - exp_H**2)

def estado_ghz(n: int) -> np.ndarray:
    """Estado GHZ de n qubits: (|00...0⟩ + |11...1⟩)/√2"""
    psi = np.zeros(2**n, dtype=complex)
    psi[0] = psi[-1] = 1 / np.sqrt(2)
    return psi

def generador_fase(n: int) -> np.ndarray:
    """H = Σᵢ Zᵢ/2 — genera rotaciones de fase en cada qubit"""
    from qiskit.quantum_info import SparsePauliOp
    terms = [('I'*i + 'Z' + 'I'*(n-i-1), 0.5) for i in range(n)]
    return SparsePauliOp.from_list(terms).to_matrix().real

N_vals = range(1, 9)
qfi_producto, qfi_ghz = [], []

for n in N_vals:
    H = generador_fase(n)
    # Estado producto |+⟩^⊗n
    plus = np.array([1, 1]) / np.sqrt(2)
    psi_prod = plus
    for _ in range(n - 1):
        psi_prod = np.kron(psi_prod, plus)
    qfi_producto.append(qfi_estado_puro(psi_prod, H))
    qfi_ghz.append(qfi_estado_puro(estado_ghz(n), H))

print(f'{"n":>3} | {"QFI prod":>10} | {"QFI GHZ":>10} | {"SQL 1/n":>10} | {"HL 1/n²":>10}')
print('-' * 52)
for n, qf_p, qf_g in zip(N_vals, qfi_producto, qfi_ghz):
    print(f'{n:>3} | {qf_p:>10.3f} | {qf_g:>10.3f} | {1/n:>10.4f} | {1/n**2:>10.6f}')
```

**Parte b)** Implementa la estimación de fase con interferómetro de Ramsey para $N=4$ qubits
y muestra que el estado GHZ alcanza el límite de Heisenberg.

**Parte c)** ¿Cuándo es prácticamente alcanzable el HL? Discute el efecto de la decoherencia.

**Referencia:** Giovannetti et al., *Science* 306, 1330 (2004); Degen et al., *RMP* 89, 035002 (2017).

---

## Problema R6 — Quantum Machine Learning: kernel cuántico vs clásico

Los métodos de kernel cuántico proponen ventajas computacionales en ciertos
problemas de clasificación. Estudia en qué condiciones son superiores.

**Parte a)** Implementa un clasificador basado en kernel cuántico para datos 2D.
El kernel es $k(x_i, x_j) = |\langle\phi(x_i)|\phi(x_j)\rangle|^2$ donde
$|\phi(x)\rangle$ es el feature map cuántico ZZFeatureMap.

```python
import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def feature_map_zzfm(x: np.ndarray, reps: int = 2) -> QuantumCircuit:
    """
    ZZFeatureMap simplificado: RZ + ZZ entanglement.
    x: vector de características de dimensión 2.
    """
    qc = QuantumCircuit(2)
    for _ in range(reps):
        for i, xi in enumerate(x):
            qc.h(i)
            qc.rz(2 * xi, i)
        qc.cx(0, 1)
        qc.rz(2 * (np.pi - x[0]) * (np.pi - x[1]), 1)
        qc.cx(0, 1)
    return qc

def kernel_cuantico(X: np.ndarray) -> np.ndarray:
    """Gram matrix del kernel cuántico para el dataset X."""
    n = len(X)
    K = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            sv_i = Statevector(feature_map_zzfm(X[i]))
            sv_j = Statevector(feature_map_zzfm(X[j]))
            K[i, j] = K[j, i] = abs(sv_i.inner(sv_j))**2
    return K

# Generar dataset no linealmente separable (anillos concéntricos)
rng = np.random.default_rng(42)
n_samples = 80
r_inner = rng.uniform(0, 0.5, n_samples // 2)
r_outer = rng.uniform(0.8, 1.2, n_samples // 2)
theta_i = rng.uniform(0, 2*np.pi, n_samples // 2)
theta_o = rng.uniform(0, 2*np.pi, n_samples // 2)

X_inner = np.column_stack([r_inner * np.cos(theta_i), r_inner * np.sin(theta_i)])
X_outer = np.column_stack([r_outer * np.cos(theta_o), r_outer * np.sin(theta_o)])
X = np.vstack([X_inner, X_outer])
y = np.array([0]*40 + [1]*40)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Tu implementación: comparar kernel cuántico vs RBF clásico
# K_train = kernel_cuantico(X_train)
# clf_q = SVC(kernel='precomputed').fit(K_train, y_train)
```

**Parte b)** Compara la precisión del kernel cuántico vs SVM con kernel RBF clásico.

**Parte c)** ¿El kernel cuántico ofrece ventaja? ¿En qué condiciones esperarías que sí?
Discute el concepto de *quantum kernel advantage* (Liu et al., 2021).

**Referencia:** Havlíček et al., *Nature* 567, 209 (2019); Liu et al., *Nat. Phys.* 17, 1013 (2021).

---

## Problema R7 — Fault Tolerance: umbral del código de repetición

El umbral de corrección de errores es la tasa de error física por debajo de la cual
la corrección de errores mejora la fidelidad lógica al aumentar la distancia.

**Parte a)** Para el código de repetición de distancia $d$ bajo ruido de bit-flip con
probabilidad $p$, la probabilidad de error lógico es:

$$p_L(d, p) = \sum_{k=\lceil d/2 \rceil}^{d} \binom{d}{k} p^k (1-p)^{d-k}$$

Calcula y grafica $p_L$ vs $p$ para $d = 3, 5, 7, 9$ e identifica el umbral.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import comb

def p_logica_repeticion(d: int, p: float) -> float:
    """P error lógico para código de repetición de distancia d."""
    t = (d - 1) // 2  # capacidad correctora
    return sum(comb(d, k, exact=True) * p**k * (1-p)**(d-k)
               for k in range(t+1, d+1))

p_vals = np.linspace(0, 0.5, 200)
fig, ax = plt.subplots(figsize=(8, 5))

for d in [3, 5, 7, 9, 11]:
    p_L = [p_logica_repeticion(d, p) for p in p_vals]
    ax.semilogy(p_vals, p_L, lw=2, label=f'd = {d}')

ax.axvline(0.5, color='gray', ls=':', lw=0.8)
ax.semilogy(p_vals, p_vals, 'k--', lw=1.5, label='Sin corrección (d=1)')
ax.set_xlabel('Tasa de error física p')
ax.set_ylabel('Tasa de error lógica p_L')
ax.set_title('Umbral del código de repetición')
ax.legend(); ax.grid(alpha=0.3, which='both')
ax.set_xlim(0, 0.5); ax.set_ylim(1e-8, 1)

# Encontrar umbral numéricamente
# El umbral es donde p_L(d=3, p) = p
# Tu código aquí
plt.tight_layout(); plt.show()
```

**Parte b)** Implementa el decodificador de mínima distancia para el código de
repetición y verifica el umbral experimentalmente con el simulador de Qiskit.

**Parte c)** Explica por qué el umbral del surface code (~1%) es más relevante en la práctica.

---

## Problema R8 — Advantage cuántica: complejidad y lower bounds

Analiza el speedup cuántico real vs afirmado en tres algoritmos.

**Parte a)** **Grover con oracle desconocido**: si tienes $M$ soluciones de $N$ posibles,
el número óptimo de iteraciones es $k^* = \lfloor \frac{\pi}{4}\sqrt{N/M} \rfloor$.
Implementa búsqueda con $M > 1$ y muestra que la probabilidad de éxito oscila.

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def grover_multi_target(n: int, targets: list[int], n_iter: int) -> dict:
    """
    Grover con múltiples targets. Devuelve distribución de probabilidad.
    n: número de qubits (N = 2^n posibles)
    targets: lista de índices marcados
    n_iter: número de iteraciones
    """
    # Tu implementación aquí
    pass

N = 64; n = 6
targets_list = [1, 5]  # M=2 targets
k_opt = int(np.floor(np.pi/4 * np.sqrt(N/len(targets_list))))

resultados_iter = {}
for k in range(0, k_opt*3):
    dist = grover_multi_target(n, targets_list, k)
    p_success = sum(dist.get(format(t,'06b'), 0) for t in targets_list) if dist else 0
    resultados_iter[k] = p_success

import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(list(resultados_iter.keys()), list(resultados_iter.values()), 'b-o', ms=4)
ax.axvline(k_opt, color='r', ls='--', label=f'k* = {k_opt}')
ax.set_xlabel('Iteraciones Grover'); ax.set_ylabel('P(éxito)')
ax.set_title(f'Grover multi-target: N={N}, M={len(targets_list)}')
ax.legend(); ax.grid(alpha=0.3); plt.tight_layout(); plt.show()
```

**Parte b)** Muestra que el **Quantum Approximate Optimization Algorithm (QAOA)** con $p=1$
no puede superar la cota de 0.75 de MAX-CUT en grafos 3-regulares (Farhi et al., 2014).
Genera 10 grafos 3-regulares aleatorios y mide la razón de aproximación QAOA vs clásico.

**Parte c)** Discute el problema **BQP vs BPP**: ¿qué tipo de problemas crees que
tienen ventaja cuántica exponencial demostrada? ¿Cuál es el estado del arte en 2024?

**Referencia:** Grover (1996); Farhi et al. (2014); Bravyi et al., *Nat. Phys.* 14, 1021 (2018).

---

## Notas generales

- Los problemas R1-R4 son directamente implementables con Qiskit + NumPy.
- Los problemas R5-R8 requieren síntesis de literatura y pensamiento crítico.
- Soluciones parciales son válidas; lo importante es el razonamiento.
- Soluciones completas en `Soluciones/investigacion/`.
