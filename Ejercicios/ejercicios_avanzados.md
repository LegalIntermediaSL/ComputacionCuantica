# Ejercicios Avanzados

Nivel alto. Cubre los módulos 20-28: algoritmos variacionales, hardware, sistemas abiertos, recursos cuánticos, ZX-Calculus e internet cuántico.
Se asume dominio de los ejercicios básicos e intermedios y experiencia con Qiskit 2.0 Primitives V2.

---

## Ejercicio 1 — VQE para H₂: lazo variacional completo

**Módulo:** `11_algoritmos_variacionales/README.md`

**Enunciado:**
Implementa un VQE completo para estimar la energía del estado fundamental del H₂.

a) Usa el Hamiltoniano simplificado (2 qubits, STO-3G):
   $$H = -1.0523\,II + 0.3979\,ZI - 0.3979\,IZ - 0.0112\,ZZ + 0.1809\,XX$$
b) Implementa el ansatz `EfficientSU2` con `reps=2` y optimizador COBYLA.
c) Compara el resultado con la referencia FCI de $-1.8572$ Ha. ¿Cuántas iteraciones tarda en converger?

```python
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import EfficientSU2
from scipy.optimize import minimize
import numpy as np

H = SparsePauliOp.from_list([
    ("II", -1.0523), ("ZI", 0.3979), ("IZ", -0.3979),
    ("ZZ", -0.0112), ("XX", 0.1809),
])
ansatz = EfficientSU2(2, reps=2, entanglement="linear")
estimator = StatevectorEstimator()
history = []

def cost(params):
    bound = ansatz.assign_parameters(params)
    e = float(estimator.run([(bound, H)]).result()[0].data.evs)
    history.append(e)
    return e

np.random.seed(42)
x0 = np.random.uniform(-np.pi, np.pi, ansatz.num_parameters)
res = minimize(cost, x0, method="COBYLA", options={"maxiter": 500})

print(f"Energía VQE:    {res.fun:.6f} Ha")
print(f"Referencia FCI: -1.857200 Ha")
print(f"Error:          {abs(res.fun + 1.8572)*1000:.3f} mHa")
print(f"Iteraciones:    {len(history)}")
```

d) ¿Qué pasa si reduces a `reps=1`? ¿Puede el ansatz representar el estado fundamental exacto?

**Pista:** La expresividad del ansatz limita la precisión alcanzable. Con `reps=1` el ansatz puede no tener suficientes parámetros para representar el estado fundamental exacto.

**Solución:** `Soluciones/11_12_variacionales_y_aplicaciones.md`

---

## Ejercicio 2 — Código de repetición 3 qubits: bit-flip completo

**Módulo:** `09_correccion_errores/README.md`

**Enunciado:**
Implementa el ciclo completo de corrección de errores para el código de repetición de 3 qubits.

a) Codifica un qubit lógico arbitrario $|\psi_L\rangle = \alpha|000\rangle + \beta|111\rangle$.
b) Aplica errores en uno de los tres qubits con probabilidad $p$ usando un `NoiseModel`.
c) Extrae el síndrome midiendo dos qubits ancilla y aplica la corrección.
d) Compara la tasa de error lógico con y sin corrección en función de $p$:

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, state_fidelity
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
import numpy as np

def encode_and_correct(alpha, beta, p_error, shots=2000):
    errors_corrected = 0
    for _ in range(shots):
        qc = QuantumCircuit(5, 2)  # 3 datos + 2 ancilla
        # Inicializar estado lógico
        qc.initialize([alpha, beta], 0)
        # Codificar
        qc.cx(0, 1); qc.cx(0, 2)
        # Simular error con probabilidad p en cada qubit de datos
        for q in range(3):
            if np.random.random() < p_error:
                qc.x(q)
        # Síndrome
        qc.cx(0, 3); qc.cx(1, 3)  # ancilla 3 = qubit0 XOR qubit1
        qc.cx(1, 4); qc.cx(2, 4)  # ancilla 4 = qubit1 XOR qubit2
        qc.measure([3, 4], [0, 1])
        # (La corrección real requeriría feed-forward clásico)
    return None

# Comparar fidelidad teórica con y sin corrección
p_vals = np.linspace(0, 0.3, 10)
for p in p_vals:
    # Sin corrección: error lógico si cualquier qubit falla
    p_fail_no_qec = 1 - (1 - p)**3
    # Con corrección: error lógico si 2 o más qubits fallan
    p_fail_qec = 3 * p**2 * (1-p) + p**3
    print(f"p={p:.2f}: sin QEC={p_fail_no_qec:.4f}, con QEC={p_fail_qec:.4f}")
```

e) ¿Cuál es el umbral de error $p_{th}$ por debajo del cual el código ayuda?

**Pista:** El umbral es $p_{th} = 0.5$ para el código de repetición de 3 qubits (error lógico = error físico cuando $3p^2(1-p) + p^3 = p$).

**Solución:** `Soluciones/09_14_correccion_y_surface_codes.md`

---

## Ejercicio 3 — Contracción del vector de Bloch: análisis completo

**Módulo:** `16_canales_cuanticos_y_ruido/README.md`

**Enunciado:**
Cada canal cuántico actúa sobre el vector de Bloch $\vec{r} = (x, y, z)$ de forma característica.

a) Para el canal despolarizante $\mathcal{E}(\rho) = (1-p)\rho + \frac{p}{3}(X\rho X + Y\rho Y + Z\rho Z)$, demuestra analíticamente que $\vec{r} \to (1 - \frac{4p}{3})\vec{r}$.
b) Para el canal de amortiguamiento de amplitud con parámetro $\gamma$, calcula cómo transforman $(x, y, z)$.
c) Compara ambos canales trazando la norma del vector de Bloch en función de $p$ (o $\gamma$):

```python
import numpy as np
import matplotlib.pyplot as plt

def bloch(rho):
    X = np.array([[0,1],[1,0]]); Y = np.array([[0,-1j],[1j,0]]); Z = np.array([[1,0],[0,-1]])
    return np.array([np.trace(rho @ X).real, np.trace(rho @ Y).real, np.trace(rho @ Z).real])

# Estado inicial en el ecuador
rho0 = np.array([[0.5, 0.5],[0.5, 0.5]])  # |+><+|

p_vals = np.linspace(0, 1, 100)
norms_dep, norms_amp = [], []

for p in p_vals:
    X = np.array([[0,1],[1,0]]); Y = np.array([[0,-1j],[1j,0]]); Z = np.array([[1,0],[0,-1]])
    # Despolarizante
    rho_dep = (1-p)*rho0 + (p/3)*(X@rho0@X + Y@rho0@Y + Z@rho0@Z)
    norms_dep.append(np.linalg.norm(bloch(rho_dep)))
    # Amortiguamiento de amplitud
    K0 = np.array([[1,0],[0,np.sqrt(1-p)]]); K1 = np.array([[0,np.sqrt(p)],[0,0]])
    rho_amp = K0@rho0@K0.conj().T + K1@rho0@K1.conj().T
    norms_amp.append(np.linalg.norm(bloch(rho_amp)))

plt.plot(p_vals, norms_dep, label="Despolarizante")
plt.plot(p_vals, norms_amp, label="Amplitud damping")
plt.xlabel("p"); plt.ylabel("|r⃗|"); plt.legend(); plt.show()
```

d) ¿Para qué canal se llega antes al estado de máxima mezcla?

**Pista:** El canal despolarizante alcanza la mezcla máxima en $p=0.75$; el de amplitud, en $p=1$.

**Solución:** `Soluciones/bloque_5_hamiltonianos_y_ruido.md`

---

## Ejercicio 4 — BB84 con detección de espía

**Módulo:** `27_internet_cuantico_and_comunicaciones/README.md`

**Enunciado:**
Implementa el protocolo BB84 completo, incluyendo la detección de un espía (ataque de intercepción y reenvío).

a) Alice envía $n=20$ qubits en bases aleatorias ($Z$ o $X$) con bits aleatorios.
b) Eve intercepta cada qubit, lo mide en una base aleatoria y reenvía su resultado.
c) Bob mide en bases aleatorias.
d) Calcula la tasa de error cuántico de bits (QBER). Sin Eve: QBER ≈ 0. Con Eve: QBER ≈ 25%.

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def bb84_simulate(n=200, eavesdrop=False):
    alice_bits  = np.random.randint(0, 2, n)
    alice_bases = np.random.randint(0, 2, n)  # 0=Z, 1=X
    bob_bases   = np.random.randint(0, 2, n)

    bob_results = []
    for i in range(n):
        qc = QuantumCircuit(1)
        if alice_bits[i] == 1:
            qc.x(0)
        if alice_bases[i] == 1:  # base X
            qc.h(0)

        if eavesdrop:
            eve_base = np.random.randint(0, 2)
            if eve_base == 1:
                qc.h(0)
            sv = Statevector.from_instruction(qc)
            eve_result = np.random.choice([0, 1], p=sv.probabilities())
            qc = QuantumCircuit(1)
            if eve_result == 1:
                qc.x(0)
            if eve_base == 1:
                qc.h(0)

        if bob_bases[i] == 1:
            qc.h(0)
        sv = Statevector.from_instruction(qc)
        bob_results.append(np.random.choice([0, 1], p=sv.probabilities()))

    # Clave compartida: bases iguales
    shared = [(alice_bits[i], bob_results[i])
              for i in range(n) if alice_bases[i] == bob_bases[i]]
    if not shared:
        return 0.0
    qber = sum(a != b for a, b in shared) / len(shared)
    return qber

print(f"QBER sin Eve: {bb84_simulate(500, eavesdrop=False):.4f}")
print(f"QBER con Eve: {bb84_simulate(500, eavesdrop=True):.4f}")
```

e) ¿Por qué Eve no puede copiar el qubit sin perturbarlo? (No-clonación)

**Pista:** Eve introduce QBER ≈ 25% porque acierta la base el 50% de las veces; cuando falla, colapsa el estado a un estado incorrecto.

**Solución:** `Soluciones/bloque_7_hardware_y_pqc.md`

---

## Ejercicio 5 — Simplificación de circuitos con PyZX

**Módulo:** `26_calculo_grafico_y_zx_calculus/README.md`

**Enunciado:**
PyZX permite simplificar circuitos cuánticos usando las reglas de reescritura del ZX-Calculus.

a) Crea un circuito de 4 qubits con puertas redundantes (H-H, CX-CX, etc.).
b) Conviértelo a un diagrama ZX con PyZX y aplica la simplificación `full_reduce`.
c) Compara el número de puertas antes y después:

```python
import pyzx as zx
from qiskit import QuantumCircuit
from qiskit.qasm2 import dumps

# Circuito con redundancias
qc = QuantumCircuit(3)
qc.h(0); qc.h(0)          # H-H = I
qc.cx(0, 1); qc.cx(0, 1)  # CX-CX = I
qc.h(1); qc.cx(1, 2); qc.h(1)
qc.t(0); qc.tdg(0)        # T-T† = I
qc.cx(0, 2); qc.h(2)

print("Puertas originales:", qc.count_ops())

# Exportar a QASM y cargar en PyZX
qasm_str = dumps(qc)
circ = zx.Circuit.from_qasm(qasm_str)
g = circ.to_graph()
zx.simplify.full_reduce(g)
circ_opt = zx.extract_circuit(g)
print("Puertas tras PyZX:", circ_opt.stats())
```

d) ¿Qué reglas de ZX-Calculus se aplican para eliminar las puertas H-H?

**Pista:** La regla de `spider fusion` fusiona arañas del mismo color adyacentes, eliminando pares H-H.

**Solución:** `Soluciones/bloque_6_algoritmos_avanzados.md`

---

## Ejercicio 6 — Mapeo QUBO a Hamiltoniano de Ising

**Módulo:** `12_aplicaciones/02_optimizacion.md`

**Enunciado:**
Los problemas de optimización combinatoria se pueden mapear a Hamiltonianos cuánticos mediante la sustitución $x_i = \frac{1 - Z_i}{2}$.

a) Para $f(x_1, x_2) = 3x_1 + 2x_2 - 5x_1x_2$ con $x_i \in \{0,1\}$, encuentra el mínimo clásico por fuerza bruta.
b) Sustituye $x_i = \frac{1-Z_i}{2}$ y simplifica para obtener el Hamiltoniano de Ising $H = c_0 I + c_1 Z_1 + c_2 Z_2 + c_{12} Z_1 Z_2$.
c) Verifica que el autovector de menor autovalor de $H$ corresponde a la solución óptima:

```python
from qiskit.quantum_info import SparsePauliOp
import numpy as np

# f(x1,x2) = 3x1 + 2x2 - 5*x1*x2
# Tras sustitución: H = 0.25*II - 0.25*ZI - 0.75*IZ + 1.25*ZZ
H = SparsePauliOp.from_list([("II", 0.25), ("ZI", -0.25), ("IZ", -0.75), ("ZZ", 1.25)])
H_mat = H.to_matrix()

evals, evecs = np.linalg.eigh(H_mat)
print("Autovalores:", evals.round(4))
print("Estado de menor energía:", evecs[:, 0].round(3))

# Comparar con fuerza bruta
for x1, x2 in [(0,0),(0,1),(1,0),(1,1)]:
    f = 3*x1 + 2*x2 - 5*x1*x2
    print(f"f({x1},{x2}) = {f}")
```

d) ¿A qué bitstring corresponde el autovector de mínima energía?

**Pista:** El estado $|11\rangle$ en la convención de Qiskit ($Z|1\rangle = -|1\rangle$) corresponde a $x_1=x_2=1$.

**Solución:** `Soluciones/11_12_variacionales_y_aplicaciones.md`

---

## Ejercicio 7 — Ecuación de Lindblad y sistemas abiertos

**Módulo:** `21_open_quantum_systems/README.md`

**Enunciado:**
La ecuación maestra de Lindblad describe la evolución de un sistema cuántico abierto:
$$\dot{\rho} = -i[H,\rho] + \sum_k \left(L_k\rho L_k^\dagger - \frac{1}{2}\{L_k^\dagger L_k, \rho\}\right)$$

a) Para un qubit con $H = \frac{\omega}{2}Z$ y operador de salto $L = \sqrt{\gamma}\sigma_-$ (relajación), integra numéricamente la ecuación para $t \in [0, 5/\gamma]$.
b) Muestra que $\langle Z\rangle(t) \to -1$ (estado fundamental) con constante de tiempo $1/\gamma$.

```python
import numpy as np
from scipy.integrate import solve_ivp

omega, gamma = 1.0, 0.5
H = omega/2 * np.array([[1,0],[0,-1]], dtype=complex)
Lm = np.sqrt(gamma) * np.array([[0,0],[1,0]], dtype=complex)  # sigma_-

def lindblad_rhs(t, rho_flat):
    rho = rho_flat.reshape(2, 2)
    comm = -1j * (H @ rho - rho @ H)
    dissip = Lm @ rho @ Lm.conj().T - 0.5 * (Lm.conj().T @ Lm @ rho + rho @ Lm.conj().T @ Lm)
    return (comm + dissip).flatten()

rho0 = np.array([[1,0],[0,0]], dtype=complex)  # |0><0|
sol = solve_ivp(lindblad_rhs, [0, 10/gamma], rho0.flatten(),
                t_eval=np.linspace(0, 10/gamma, 200))

Z = np.array([[1,0],[0,-1]])
Z_expect = [np.trace(sol.y[:,i].reshape(2,2) @ Z).real for i in range(sol.y.shape[1])]
print("⟨Z⟩ inicial:", Z_expect[0], "  final:", Z_expect[-1])
```

c) ¿Qué representa físicamente $\gamma$? ¿Cómo se relaciona con $T_1$?

**Pista:** $\gamma = 1/T_1$. El tiempo $T_1$ es la vida media de la excitación del qubit.

**Solución:** `Soluciones/16_21_canales_y_sistemas_abiertos.md`

---

## Ejercicio 8 — Tomografía de estados (QST)

**Módulo:** `19_tomografia_y_caracterizacion/README.md`

**Enunciado:**
La tomografía de estados cuánticos reconstruye la matriz densidad $\rho$ midiendo en múltiples bases.

a) Para 2 qubits, se necesitan $3^2 = 9$ configuraciones de bases. ¿Cuántos parámetros reales tiene $\rho$ para $n$ qubits?
b) Prepara el estado $|\Phi^+\rangle$ y reconstruye su matriz densidad midiendo en las 9 bases de Pauli:

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp, DensityMatrix, state_fidelity
import numpy as np

# Preparar |Φ+>
qc = QuantumCircuit(2)
qc.h(0); qc.cx(0, 1)

# Medir en todas las combinaciones de Pauli (9 bases)
paulis = ["II", "IX", "IY", "IZ", "XI", "XX", "XY", "XZ", "YI",
          "YX", "YY", "YZ", "ZI", "ZX", "ZY", "ZZ"]

estimator = StatevectorEstimator()
obs = [SparsePauliOp(p) for p in paulis]
results = estimator.run([(qc, o) for o in obs]).result()
expectations = {p: float(results[i].data.evs) for i, p in enumerate(paulis)}

# Reconstruir rho: rho = sum_P <P> * P / 4
rho_reconstructed = sum(v * SparsePauliOp(k).to_matrix() / 4
                        for k, v in expectations.items())

rho_ideal = DensityMatrix.from_instruction(qc)
F = state_fidelity(DensityMatrix(rho_reconstructed), rho_ideal)
print(f"Fidelidad de tomografía: {F:.6f}")
```

c) ¿Por qué la tomografía escala exponencialmente con el número de qubits?

**Pista:** Para $n$ qubits, la matriz densidad tiene $4^n - 1$ parámetros reales independientes.

**Solución:** `Soluciones/17_18_19_medicion_complejidad_y_tomografia.md`

---

## Ejercicio 9 — QAOA para MaxCut: análisis del paisaje de coste

**Módulo:** `11_algoritmos_variacionales/README.md`

**Enunciado:**
Analiza el paisaje de la función de coste de QAOA para un grafo de 4 nodos.

a) Para un grafo de ciclo $C_4$ (aristas 0-1, 1-2, 2-3, 3-0) con $p=1$ capa, calcula el valor esperado de $H_C$ como función de $(\gamma, \beta)$.
b) Traza el mapa de calor de $\langle H_C\rangle(\gamma, \beta)$ y encuentra el máximo.

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp
import numpy as np
import matplotlib.pyplot as plt

edges = [(0,1),(1,2),(2,3),(3,0)]
n = 4
terms = [("I"*n, len(edges)*0.5)]
for i,j in edges:
    p = list("I"*n); p[n-1-i]="Z"; p[n-1-j]="Z"
    terms.append(("".join(p), -0.5))
H_C = SparsePauliOp.from_list(terms)

estimator = StatevectorEstimator()
g_vals = np.linspace(0, np.pi, 20)
b_vals = np.linspace(0, np.pi/2, 20)
landscape = np.zeros((len(g_vals), len(b_vals)))

for i, g in enumerate(g_vals):
    for j, b in enumerate(b_vals):
        qc = QuantumCircuit(n)
        qc.h(range(n))
        for u, v in edges:
            qc.rzz(2*g, u, v)
        for q in range(n):
            qc.rx(2*b, q)
        val = float(estimator.run([(qc, H_C)]).result()[0].data.evs)
        landscape[i, j] = val

plt.imshow(landscape, origin='lower', aspect='auto',
           extent=[0, np.pi/2, 0, np.pi])
plt.colorbar(label="⟨H_C⟩")
plt.xlabel("β"); plt.ylabel("γ"); plt.title("Paisaje QAOA C₄, p=1")
plt.show()
print(f"Máximo ⟨H_C⟩ = {landscape.max():.4f} (teórico MaxCut = {len(edges)})")
```

c) ¿Por qué aumentar $p$ mejora la aproximación pero hace más difícil la optimización?

**Pista:** El paisaje de coste de QAOA tiene barrancos exponencialmente estrechos para $p$ grande (problema de "barren plateaus").

**Solución:** `Soluciones/11_12_variacionales_y_aplicaciones.md`

---

## Ejercicio 10 — Complejidad BQP y límites del cómputo cuántico

**Módulo:** `18_complejidad_cuantica/README.md`

**Enunciado:**
La clase BQP contiene los problemas decidibles en tiempo polinómico por una computadora cuántica con error acotado.

a) Explica por qué el hecho de explorar $2^n$ estados en superposición NO implica que BQP = NP.
b) Para el problema de factorización de $N = p \cdot q$, estima el número de puertas cuánticas necesarias en el algoritmo de Shor para $N$ de 2048 bits (RSA-2048).
c) Calcula cuántos qubits lógicos requeriría ejecutar Shor para RSA-2048 asumiendo el modelo de superficie codes con umbral del 1%:

```python
import numpy as np

# Estimaciones para Shor en RSA-2048
n_bits = 2048

# Qubits lógicos (estimación de Gidney & Ekerå 2021)
n_logical = 4098  # aprox. 4n para RSA-n bits

# Puertas Toffoli requeridas (dominan el coste)
toffoli_count = 3 * n_bits**3  # O(n^3) aproximado
print(f"Puertas Toffoli estimadas: {toffoli_count:.2e}")

# Con surface codes: cada qubit lógico requiere ~1000 qubits físicos
# para alcanzar la tasa de error necesaria con p_phys ~ 0.1%
distance_needed = 27  # código de distancia 27
qubits_per_logical = 2 * distance_needed**2
n_physical = n_logical * qubits_per_logical
print(f"Qubits lógicos:  {n_logical}")
print(f"Qubits físicos:  {n_physical:,}")
print(f"Mejores chips actuales: ~1000-2000 qubits físicos")
print(f"Factor que falta: {n_physical / 1000:.0f}x")
```

d) ¿Por qué este cálculo muestra que el riesgo para RSA-2048 no es inminente?

**Pista:** El número de qubits físicos necesarios (~millones) supera en varios órdenes de magnitud lo disponible hoy (~miles).

**Solución:** `Soluciones/17_18_19_medicion_complejidad_y_tomografia.md`
