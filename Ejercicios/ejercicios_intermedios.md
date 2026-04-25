# Ejercicios Intermedios

Nivel medio. Cubre los módulos 10-19: algoritmos del canon, ruido, información cuántica, corrección de errores y medición avanzada.
Se asume familiaridad con Qiskit básico y álgebra lineal de la sección de ejercicios básicos.

---

## Ejercicio 1 — No-factorizabilidad del estado de Bell

**Módulo:** `01_fundamentos/04_entrelazamiento_y_estados_de_bell.md`

**Enunciado:**
Demuestra que $|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$ no puede escribirse como producto tensorial $|\psi\rangle \otimes |\phi\rangle$.

a) Supón que $|\psi\rangle = a|0\rangle + b|1\rangle$ y $|\phi\rangle = c|0\rangle + d|1\rangle$. Expande el producto tensorial e iguala a $|\Phi^+\rangle$.
b) Muestra que el sistema de ecuaciones $ac=\frac{1}{\sqrt{2}}$, $ad=0$, $bc=0$, $bd=\frac{1}{\sqrt{2}}$ no tiene solución.
c) Verifica computacionalmente que la traza parcial sobre el qubit 1 da un estado mixto:

```python
from qiskit.quantum_info import Statevector, partial_trace
import numpy as np

bell = Statevector([1, 0, 0, 1]) / np.sqrt(2)
rho = bell.to_operator()  # matriz densidad del sistema completo
# Traza parcial sobre qubit 0 (índice 0)
rho_1 = partial_trace(bell, [0])
print("Estado reducido del qubit 1:\n", rho_1.data.round(3))
print("Pureza:", (rho_1.data @ rho_1.data).trace().real.round(4))
```

**Pista:** Si el estado reducido de cualquier subsistema es mixto, el estado global está entrelazado.

**Solución:** `Soluciones/08_informacion_cuantica.md`

---

## Ejercicio 2 — Puerta Z e interferencia

**Módulo:** `01_fundamentos/03_puertas_cuanticas_y_circuitos.md`

**Enunciado:**
Una puerta Z no cambia $P(|0\rangle)$ ni $P(|1\rangle)$ cuando se mide inmediatamente, pero sí modifica la interferencia posterior.

a) Comprueba que $\langle 0|Z|\psi\rangle$ y $\langle 1|Z|\psi\rangle$ tienen el mismo módulo que sin Z para $|\psi\rangle = |+\rangle$.
b) Demuestra que $H·Z·H|0\rangle = |1\rangle$ mientras que $H·H|0\rangle = |0\rangle$. La Z cambia el resultado aunque no altere la distribución de probabilidades antes de la segunda H.
c) Implementa el experimento de interferencia:

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

for with_z in [False, True]:
    qc = QuantumCircuit(1)
    qc.h(0)
    if with_z:
        qc.z(0)
    qc.h(0)
    sv = Statevector.from_instruction(qc)
    label = "H-Z-H" if with_z else "H-H"
    print(f"{label}|0> = {sv}")
```

**Pista:** La fase global no es observable, pero la fase relativa entre $|0\rangle$ y $|1\rangle$ sí lo es.

**Solución:** `Soluciones/01_fundamentos_y_qiskit.md`

---

## Ejercicio 3 — Transpilación y profundidad de circuito

**Módulo:** `02_qiskit_basico/09_qiskit_transpilacion_ruido_y_hardware.md`

**Enunciado:**
Compara cómo afecta el nivel de optimización de la transpilación a la profundidad del circuito.

a) Crea un circuito que prepare $|\Phi^+\rangle$ usando pasos redundantes (H, CNOT, H, H, CNOT, H en distintos qubits).
b) Transpílalo con `optimization_level` 0, 1, 2 y 3, y compara depth y número de puertas.
c) Implementa:

```python
from qiskit import QuantumCircuit, transpile

qc = QuantumCircuit(2)
qc.h(0); qc.cx(0, 1)
qc.h(0); qc.h(0)     # redundante
qc.cx(0, 1); qc.cx(0, 1)  # redundante

for level in range(4):
    t = transpile(qc, basis_gates=['cx', 'u'], optimization_level=level)
    print(f"Level {level}: depth={t.depth()}, cx={t.count_ops().get('cx',0)}, u={t.count_ops().get('u',0)}")
```

d) ¿Cuándo conviene usar `optimization_level=3` y cuándo no?

**Pista:** `optimization_level=3` puede tardar más en circuitos grandes pero produce circuitos más eficientes.

**Solución:** `Soluciones/01_fundamentos_y_qiskit.md`

---

## Ejercicio 4 — Bernstein-Vazirani

**Módulo:** `05_algoritmos/README.md`

**Enunciado:**
El algoritmo de Bernstein-Vazirani encuentra en una consulta la cadena oculta $s$ de una función $f(x) = s \cdot x \pmod{2}$.

a) Para $n=3$ y $s = 101_2$, escribe el oráculo como circuito (CNOT donde $s_i = 1$).
b) Implementa el algoritmo completo y verifica que recuperas $s$:

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

s = "101"
n = len(s)

qc = QuantumCircuit(n + 1)
# Estado inicial del qubit ancilla en |->
qc.x(n); qc.h(n)
# Hadamard en todos los qubits de entrada
qc.h(range(n))
# Oráculo: CNOT donde s_i = 1
for i, bit in enumerate(reversed(s)):
    if bit == "1":
        qc.cx(i, n)
# Hadamard final
qc.h(range(n))

sv = Statevector.from_instruction(qc)
print("Amplitudes principales:", sv.probabilities_dict(decimals=3))
```

c) ¿Cuántas consultas necesita un algoritmo clásico para encontrar $s$?

**Pista:** Clásicamente se necesitan $n$ consultas; el algoritmo cuántico solo necesita 1.

**Solución:** `Soluciones/05_algoritmos_clasicos.md`

---

## Ejercicio 5 — Estado global puro, subsistema mixto

**Módulo:** `08_informacion_cuantica/README.md`

**Enunciado:**
Un estado bipartito puro entrelazado produce subsistemas mixtos.

a) Para $|\psi\rangle = \cos\theta|00\rangle + \sin\theta|11\rangle$, calcula la matriz densidad reducida $\rho_A = \text{Tr}_B(|\psi\rangle\langle\psi|)$.
b) Calcula la entropía de von Neumann $S(\rho_A) = -\text{Tr}(\rho_A \log_2 \rho_A)$ en función de $\theta$.
c) ¿Para qué valor de $\theta$ es el entrelazamiento máximo?

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, partial_trace, entropy

thetas = np.linspace(0, np.pi/2, 10)
for theta in thetas:
    qc = QuantumCircuit(2)
    qc.ry(2 * theta, 0)
    qc.cx(0, 1)
    sv = Statevector.from_instruction(qc)
    rho_A = partial_trace(sv, [1])
    S = entropy(rho_A, base=2)
    print(f"θ={np.degrees(theta):.1f}°  S(ρ_A)={S:.4f}")
```

**Pista:** La entropía de entrelazamiento es máxima cuando $\theta = \pi/4$, que da el estado de Bell.

**Solución:** `Soluciones/08_informacion_cuantica.md`

---

## Ejercicio 6 — Canal de desfase y coherencia

**Módulo:** `16_canales_cuanticos_y_ruido/README.md`

**Enunciado:**
El canal de desfase (phase-flip) destruye la coherencia sin cambiar las poblaciones.

a) Aplica el canal de desfase con parámetro $p$ al estado $|+\rangle$:
   $$\mathcal{E}(\rho) = (1-p)\rho + p Z\rho Z$$
b) Calcula los elementos de la matriz densidad resultante en función de $p$.
c) Verifica que las poblaciones $\rho_{00}$ y $\rho_{11}$ no cambian, pero las coherencias $\rho_{01}$ y $\rho_{10}$ sí.

```python
import numpy as np

def phase_flip_channel(rho, p):
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    return (1 - p) * rho + p * (Z @ rho @ Z)

rho_plus = np.array([[0.5, 0.5], [0.5, 0.5]])  # |+><+|

for p in [0.0, 0.25, 0.5, 0.75, 1.0]:
    rho_out = phase_flip_channel(rho_plus, p)
    print(f"p={p}: rho_00={rho_out[0,0].real:.3f}, rho_01={rho_out[0,1].real:.3f}")
```

d) ¿Qué ocurre con el vector de Bloch en cada caso?

**Pista:** El canal de desfase contrae el vector de Bloch en las direcciones X e Y, pero no en Z.

**Solución:** `Soluciones/bloque_5_hamiltonianos_y_ruido.md`

---

## Ejercicio 7 — Entropía de von Neumann

**Módulo:** `08_informacion_cuantica/README.md`

**Enunciado:**
La entropía de von Neumann mide el grado de mezcla de un estado cuántico.

a) Calcula $S(\rho) = -\text{Tr}(\rho \log_2 \rho)$ para:
   - $\rho = |0\rangle\langle 0|$ (estado puro)
   - $\rho = I/2$ (estado de máxima mezcla)
   - $\rho = 0.9|0\rangle\langle 0| + 0.1|1\rangle\langle 1|$

b) Verifica con Qiskit:

```python
from qiskit.quantum_info import DensityMatrix, entropy
import numpy as np

estados = [
    DensityMatrix([[1, 0], [0, 0]]),         # |0><0|
    DensityMatrix([[0.5, 0], [0, 0.5]]),      # I/2
    DensityMatrix([[0.9, 0], [0, 0.1]]),      # estado mixto
]

for rho in estados:
    S = entropy(rho, base=2)
    pureza = (rho.data @ rho.data).trace().real
    print(f"S={S:.4f}  Pureza={pureza:.4f}")
```

c) ¿Cuál es el rango de $S$ para un sistema de 1 qubit?

**Pista:** $S = 0$ para estados puros y $S = 1$ para el estado de máxima mezcla (1 qubit).

**Solución:** `Soluciones/08_informacion_cuantica.md`

---

## Ejercicio 8 — Iteraciones óptimas de Grover

**Módulo:** `05_algoritmos/README.md`

**Enunciado:**
El número óptimo de iteraciones de Grover es $k \approx \frac{\pi}{4}\sqrt{N/M}$, donde $M$ es el número de soluciones.

a) Calcula $k_{opt}$ para $n = 4$ qubits ($N=16$) con $M = 1$ solución.
b) Implementa Grover para $n=4$ y compara la probabilidad de éxito en $k=1$, $k=k_{opt}$ y $k=2k_{opt}$ iteraciones:

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

n = 4
N = 2**n
target = 5  # estado objetivo

def grover_oracle(n, target):
    qc = QuantumCircuit(n)
    bits = format(target, f"0{n}b")
    for i, b in enumerate(reversed(bits)):
        if b == "0":
            qc.x(i)
    qc.h(n-1); qc.mcx(list(range(n-1)), n-1); qc.h(n-1)
    for i, b in enumerate(reversed(bits)):
        if b == "0":
            qc.x(i)
    return qc

def diffusion(n):
    qc = QuantumCircuit(n)
    qc.h(range(n)); qc.x(range(n))
    qc.h(n-1); qc.mcx(list(range(n-1)), n-1); qc.h(n-1)
    qc.x(range(n)); qc.h(range(n))
    return qc

k_opt = int(round(np.pi / 4 * np.sqrt(N)))
for k in [1, k_opt, 2 * k_opt]:
    qc = QuantumCircuit(n)
    qc.h(range(n))
    sv = Statevector.from_instruction(qc)
    for _ in range(k):
        sv = sv.evolve(grover_oracle(n, target))
        sv = sv.evolve(diffusion(n))
    print(f"k={k}: P(target)={sv.probabilities()[target]:.4f}")
```

**Pista:** Sobrepasar $k_{opt}$ reduce la probabilidad de éxito — Grover oscila, no converge.

**Solución:** `Soluciones/05_algoritmos_clasicos.md`

---

## Ejercicio 9 — StatevectorEstimator y Hamiltonianos

**Módulo:** `10_qiskit_avanzado/README.md`

**Enunciado:**
El `StatevectorEstimator` permite calcular el valor esperado de cualquier observable definido como `SparsePauliOp`.

a) Define el Hamiltoniano de Heisenberg $H = J(X\otimes X + Y\otimes Y + Z\otimes Z)$ con $J=1$.
b) Calcula su energía esperada para el estado $|\Phi^+\rangle$ y para $|00\rangle$.
c) ¿Cuál es el estado de menor energía (autovalor mínimo)?

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp
import numpy as np

H = SparsePauliOp.from_list([("XX", 1.0), ("YY", 1.0), ("ZZ", 1.0)])

# Estado de Bell |Φ+>
qc_bell = QuantumCircuit(2)
qc_bell.h(0); qc_bell.cx(0, 1)

# Estado |00>
qc_00 = QuantumCircuit(2)

estimator = StatevectorEstimator()
result = estimator.run([(qc_bell, H), (qc_00, H)]).result()
print(f"<H> en |Φ+>  = {result[0].data.evs:.4f}")
print(f"<H> en |00>  = {result[1].data.evs:.4f}")

# Autovalores exactos
print("Autovalores H:", np.linalg.eigvalsh(H.to_matrix()).round(3))
```

**Pista:** El estado de menor energía del Hamiltoniano de Heisenberg es el estado singlete $|\Psi^-\rangle$.

**Solución:** `Soluciones/bloque_5_hamiltonianos_y_ruido.md`

---

## Ejercicio 10 — Código de repetición (corrección de errores)

**Módulo:** `09_correccion_errores/README.md`

**Enunciado:**
El código de repetición de 3 qubits protege contra un error de bit-flip en un qubit.

a) Codifica $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$ en $\alpha|000\rangle + \beta|111\rangle$ con dos CNOT.
b) Aplica un error $X$ en el qubit 1 (con probabilidad $p = 0.3$ en la simulación).
c) Implementa la detección del síndrome y la corrección:

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

# Codificación del qubit lógico |+>
qc = QuantumCircuit(3)
qc.h(0)            # prepara |+> en qubit 0
qc.cx(0, 1)        # codifica: |+00> -> (|000>+|111>)/√2
qc.cx(0, 2)

# Simular error en qubit 1
qc.x(1)

# Síndrome: comparar qubits por pares
# Ancilla no incluida aquí; usamos Statevector para inspeccionar
sv = Statevector.from_instruction(qc)
print("Estado tras error:", sv)

# Corrección: mayoría de votos (si qubits 0 y 2 coinciden pero difieren de 1, corregir 1)
qc.cx(1, 2)        # síndrome bit (qubit 2 = qubit1 XOR qubit2)
# En un circuito real se mediría el síndrome en qubits ancilla
print("El qubit erróneo es el 1. Aplicar X(1) para corregir.")
```

d) ¿Por qué este código NO protege contra errores de phase-flip?

**Pista:** El código de Shor (9 qubits) combina códigos de bit-flip y phase-flip.

**Solución:** `Soluciones/09_14_correccion_y_surface_codes.md`

---

## Ejercicio 11 — Trotterización y error de conmutación

**Módulo:** `15_hamiltonianos_y_evolucion_temporal/README.md`

**Enunciado:**
La fórmula de Trotter aproxima $e^{-i(A+B)t} \approx (e^{-iA\Delta t}e^{-iB\Delta t})^N$ con $\Delta t = t/N$.

a) Para $H = Z\otimes I + I\otimes Z + 0.5\cdot X\otimes X$ y $t=1$, compara la evolución exacta con Trotter para $N = 1, 5, 20$ pasos.
b) Calcula la fidelidad entre el estado exacto y el Trotter aproximado en cada caso.

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp, state_fidelity
from scipy.linalg import expm
import numpy as np

H = SparsePauliOp.from_list([("ZI", 1.0), ("IZ", 1.0), ("XX", 0.5)])
H_mat = H.to_matrix()
t = 1.0

# Estado inicial |+0>
sv0 = Statevector([1, 0, 1, 0]) / np.sqrt(2)

# Evolución exacta
U_exact = expm(-1j * H_mat * t)
sv_exact = Statevector(U_exact @ sv0.data)

for N in [1, 5, 20]:
    dt = t / N
    # Trotter: e^{-i Z⊗I dt} e^{-i I⊗Z dt} e^{-i XX*0.5 dt}
    qc = QuantumCircuit(2)
    qc.initialize(sv0.data)
    for _ in range(N):
        qc.rz(2 * dt, 0)
        qc.rz(2 * dt, 1)
        qc.rxx(2 * 0.5 * dt, 0, 1)
    sv_trotter = Statevector.from_instruction(qc)
    F = state_fidelity(sv_exact, sv_trotter)
    print(f"N={N:2d}: Fidelidad = {F:.6f}")
```

**Pista:** El error de Trotter escala como $O(\Delta t^2)$ por paso, así que $N$ pasos dan error total $O(t^2/N)$.

**Solución:** `Soluciones/15_20_hamiltonianos_y_evolucion.md`

---

## Ejercicio 12 — POVM y medición generalizada

**Módulo:** `17_medicion_avanzada_y_observables/README.md`

**Enunciado:**
Un POVM (Positive Operator-Valued Measure) permite distinguir estados no ortogonales con cierta probabilidad.

a) Considera el POVM de discriminación óptima entre $|0\rangle$ y $|+\rangle$ con tres elementos:
   $$M_0 = \frac{\sqrt{2}}{1+\sqrt{2}}|-\rangle\langle -|, \quad M_+ = \frac{\sqrt{2}}{1+\sqrt{2}}|1\rangle\langle 1|, \quad M_? = I - M_0 - M_+$$
b) Calcula $p(M_0|0\rangle)$, $p(M_+|0\rangle)$ y $p(M_?|0\rangle)$.
c) Verifica que los operadores POVM son positivos semidefinidos y suman la identidad:

```python
import numpy as np

ket0 = np.array([1, 0])
ket1 = np.array([0, 1])
ketm = np.array([1, -1]) / np.sqrt(2)

c = np.sqrt(2) / (1 + np.sqrt(2))
M0 = c * np.outer(ketm, ketm.conj())
Mp = c * np.outer(ket1, ket1.conj())
Mq = np.eye(2) - M0 - Mp

print("M0 + Mp + M? = I?", np.allclose(M0 + Mp + Mq, np.eye(2)))

for name, M in [("M0", M0), ("M+", Mp), ("M?", Mq)]:
    p_given_0 = (ket0.conj() @ M @ ket0).real
    print(f"p({name}||0>) = {p_given_0:.4f}")
```

**Pista:** Un POVM con $M_?$ "inconcluyente" permite identificar con certeza cuando el resultado es $M_0$ o $M_+$.

**Solución:** `Soluciones/17_18_19_medicion_complejidad_y_tomografia.md`
