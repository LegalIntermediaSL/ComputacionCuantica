# Ejercicios Básicos

Nivel de entrada. Cubre los módulos 01-09: qubits, puertas, medición, entrelazamiento y primeros pasos con Qiskit.
Cada ejercicio indica el módulo de teoría relacionado y una pista para no quedarse atascado.

---

## Ejercicio 1 — Normalización de estados

**Módulo:** `01_fundamentos/01_qubits_y_estados.md`

**Enunciado:**
Dado el estado $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$, la condición de normalización exige $|\alpha|^2 + |\beta|^2 = 1$.

a) Verifica si los siguientes estados están normalizados. Si no lo están, normalízalos:
- $|\psi_1\rangle = \frac{1}{\sqrt{2}}|0\rangle + \frac{1}{\sqrt{2}}|1\rangle$
- $|\psi_2\rangle = \frac{1}{2}|0\rangle + \frac{\sqrt{3}}{2}|1\rangle$
- $|\psi_3\rangle = 0.6|0\rangle + 0.6|1\rangle$

b) Para $|\psi_3\rangle$ normalizado, ¿cuál es la probabilidad de medir $|0\rangle$?

**Pista:** La probabilidad de medir $|0\rangle$ es $|\alpha|^2$, no $\alpha$.

**Solución:** `Soluciones/01_fundamentos_y_qiskit.md`

---

## Ejercicio 2 — Probabilidades de medición

**Módulo:** `01_fundamentos/02_superposicion_medicion_y_esfera_de_bloch.md`

**Enunciado:**
Considera el estado $|\psi\rangle = \cos(\theta/2)|0\rangle + e^{i\phi}\sin(\theta/2)|1\rangle$.

a) Calcula $P(|0\rangle)$ y $P(|1\rangle)$ en función de $\theta$.
b) ¿Para qué valor de $\theta$ es la medición completamente aleatoria (50/50)?
c) Verifica tu respuesta con Qiskit:

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

theta = np.pi / 2  # cambia este valor
qc = QuantumCircuit(1)
qc.ry(theta, 0)
sv = Statevector.from_instruction(qc)
print("Probabilidades:", sv.probabilities())
```

**Pista:** $\cos^2(\pi/4) = 1/2$.

**Solución:** `Soluciones/01_fundamentos_y_qiskit.md`

---

## Ejercicio 3 — Acción de la puerta Hadamard

**Módulo:** `01_fundamentos/03_puertas_cuanticas_y_circuitos.md`

**Enunciado:**
La puerta Hadamard tiene la matriz $H = \frac{1}{\sqrt{2}}\begin{pmatrix}1 & 1\\1 & -1\end{pmatrix}$.

a) Calcula algebraicamente $H|0\rangle$, $H|1\rangle$ y $H|+\rangle$.
b) Demuestra que $H^2 = I$ (Hadamard es su propia inversa).
c) Verifica que $HZH = X$ multiplicando las matrices.
d) Comprueba con Qiskit:

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

qc = QuantumCircuit(1)
qc.h(0)
qc.z(0)
qc.h(0)
print("HZH =\n", Operator(qc).data.round(3))
```

**Pista:** $|+\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$, así que $H|+\rangle = |0\rangle$.

**Solución:** `Soluciones/01_fundamentos_y_qiskit.md`

---

## Ejercicio 4 — Vector de Bloch de un estado mixto

**Módulo:** `01_fundamentos/02_superposicion_medicion_y_esfera_de_bloch.md`

**Enunciado:**
Un estado mixto se describe con la matriz de densidad $\rho = p|0\rangle\langle 0| + (1-p)|1\rangle\langle 1|$.

a) Escribe $\rho$ como matriz $2\times 2$ explícita.
b) Calcula el vector de Bloch $\vec{r} = (\langle X\rangle, \langle Y\rangle, \langle Z\rangle)$ donde $\langle A\rangle = \text{Tr}(\rho A)$.
c) ¿Para qué valor de $p$ el vector de Bloch es el origen? ¿Qué significa físicamente?
d) Comprueba con Qiskit:

```python
from qiskit.quantum_info import DensityMatrix, SparsePauliOp
import numpy as np

p = 0.7
rho = DensityMatrix([[p, 0], [0, 1 - p]])
for pauli in ["X", "Y", "Z"]:
    val = rho.expectation_value(SparsePauliOp(pauli))
    print(f"<{pauli}> = {val.real:.4f}")
```

**Pista:** El estado de máxima mezcla tiene $\rho = I/2$ y $\vec{r} = \vec{0}$.

**Solución:** `Soluciones/01_fundamentos_y_qiskit.md`

---

## Ejercicio 5 — Estados de Bell

**Módulo:** `01_fundamentos/04_entrelazamiento_y_estados_de_bell.md`

**Enunciado:**
Los cuatro estados de Bell son la base del entrelazamiento bipartito.

a) Construye el estado $|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$ con un circuito Qiskit (H + CNOT).
b) Mide el circuito con 2048 shots. ¿Qué resultados esperas? ¿Aparece $|01\rangle$ o $|10\rangle$?
c) Repite para obtener $|\Psi^-\rangle = \frac{1}{\sqrt{2}}(|01\rangle - |10\rangle)$.

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
sv = Statevector.from_instruction(qc)
print("Estado:", sv)
print("Probabilidades:", sv.probabilities_dict())
```

**Pista:** Para $|\Psi^-\rangle$ necesitas aplicar X y Z después del par H+CNOT.

**Solución:** `Soluciones/01_fundamentos_y_qiskit.md`

---

## Ejercicio 6 — Superposición vs. mezcla

**Módulo:** `01_fundamentos/02_superposicion_medicion_y_esfera_de_bloch.md`

**Enunciado:**
Considera dos situaciones:
- **A:** un qubit en $|+\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$
- **B:** un qubit preparado aleatoriamente en $|0\rangle$ o $|1\rangle$ con probabilidad 1/2 cada uno

a) Escribe la matriz de densidad de cada caso.
b) Ambos dan 50/50 al medir en la base $\{|0\rangle, |1\rangle\}$. ¿Cómo los distinguirías experimentalmente?
c) Calcula la pureza $\text{Tr}(\rho^2)$ para cada caso. ¿Qué indica?

**Pista:** El experimento de distinción requiere medir en la base $\{|+\rangle, |-\rangle\}$.

**Solución:** `Soluciones/01_fundamentos_y_qiskit.md`

---

## Ejercicio 7 — Puertas de fase

**Módulo:** `01_fundamentos/03_puertas_cuanticas_y_circuitos.md`

**Enunciado:**
Las puertas S ($\sqrt{Z}$) y T ($\sqrt{S}$) añaden fases relativas sin cambiar probabilidades de medición en la base computacional.

a) Aplica S a $|+\rangle$ y calcula el estado resultante. ¿En qué estado de la esfera de Bloch termina?
b) Demuestra que $S^2 = Z$ y $T^2 = S$ multiplicando matrices.
c) Verifica con Qiskit que $P(|0\rangle)$ no cambia al aplicar S sobre $|+\rangle$:

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

qc = QuantumCircuit(1)
qc.h(0)
qc.s(0)
sv = Statevector.from_instruction(qc)
print("Estado tras H+S:", sv)
print("P(|0>):", sv.probabilities()[0])
```

**Pista:** $S|+\rangle = |y+\rangle = \frac{1}{\sqrt{2}}(|0\rangle + i|1\rangle)$. Está en el ecuador pero rotado 90°.

**Solución:** `Soluciones/01_fundamentos_y_qiskit.md`

---

## Ejercicio 8 — Circuito de teleportación cuántica

**Módulo:** `02_qiskit_basico/05_qiskit_primeros_pasos.md`

**Enunciado:**
La teleportación cuántica transfiere el estado de un qubit usando un par de Bell y comunicación clásica.

a) Dibuja (o describe) el circuito de teleportación de 3 qubits.
b) Implementa el circuito en Qiskit para teleportar el estado $|+\rangle$:

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

qc = QuantumCircuit(3)
# Preparar estado a teleportar en qubit 0
qc.h(0)
# Par de Bell entre qubits 1 y 2
qc.h(1)
qc.cx(1, 2)
# Protocolo de Bell en qubits 0 y 1
qc.cx(0, 1)
qc.h(0)
# Medición y corrección clásica (simulada sin medir)
qc.cx(1, 2)
qc.cz(0, 2)
sv = Statevector.from_instruction(qc)
print("Estado final del qubit 2:", sv.partial_trace([0, 1]))
```

c) ¿Por qué no viola el principio de no-señalización más rápida que la luz?

**Pista:** Sin la corrección clásica (cx y cz finales), el qubit 2 está en un estado mixto.

**Solución:** `Soluciones/01_fundamentos_y_qiskit.md`

---

## Ejercicio 9 — Transpilación básica

**Módulo:** `02_qiskit_basico/09_qiskit_transpilacion_ruido_y_hardware.md`

**Enunciado:**
La transpilación adapta un circuito abstracto al conjunto de puertas nativas de un backend.

a) Crea un circuito con una puerta CCX (Toffoli) de 3 qubits.
b) Transpílalo con `basis_gates=['cx', 'u']` y compara el número de puertas CNOT antes y después.

```python
from qiskit import QuantumCircuit, transpile

qc = QuantumCircuit(3)
qc.ccx(0, 1, 2)
print("Circuito original — profundidad:", qc.depth())

qc_t = transpile(qc, basis_gates=['cx', 'u'], optimization_level=3)
print("Transpilado — profundidad:", qc_t.depth())
print("Puertas CNOT:", qc_t.count_ops().get('cx', 0))
```

c) ¿Por qué es importante minimizar las puertas CNOT en hardware real?

**Pista:** La fidelidad de una puerta CNOT en hardware superconductor es típicamente 99-99.5%, mientras que una puerta de 1 qubit supera el 99.9%.

**Solución:** `Soluciones/01_fundamentos_y_qiskit.md`

---

## Ejercicio 10 — Álgebra lineal: producto tensorial

**Módulo:** `01_fundamentos/06_algebra_lineal_minima_para_computacion_cuantica.md`

**Enunciado:**
El producto tensorial $\otimes$ combina espacios de Hilbert de múltiples qubits.

a) Calcula $|0\rangle \otimes |1\rangle$ y $|+\rangle \otimes |+\rangle$ explícitamente como vectores de 4 componentes.
b) Demuestra que $|+\rangle \otimes |+\rangle = \frac{1}{2}(|00\rangle + |01\rangle + |10\rangle + |11\rangle)$.
c) Verifica con Qiskit:

```python
from qiskit.quantum_info import Statevector
import numpy as np

s0 = Statevector([1, 0])       # |0>
s1 = Statevector([0, 1])       # |1>
sp = Statevector([1, 1]) / np.sqrt(2)  # |+>

print("|0> x |1> =", s0.expand(s1))
print("|+> x |+> =", sp.expand(sp))
```

**Pista:** `Statevector.expand(other)` calcula $|\psi\rangle \otimes |other\rangle$.

**Solución:** `Soluciones/01_fundamentos_y_qiskit.md`

---

## Ejercicio 11 — Sampler y estadística de medición

**Módulo:** `02_qiskit_basico/08_qiskit_simuladores_estado_y_resultados.md`

**Enunciado:**
El `StatevectorSampler` simula mediciones de un circuito cuántico.

a) Prepara el estado $|\psi\rangle = \cos(30°)|0\rangle + \sin(30°)|1\rangle$ y mídelo con 1024 shots.
b) Compara la frecuencia empírica con la probabilidad teórica.
c) Repite con 100 y 10000 shots. ¿Cómo converge el error estadístico?

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
import numpy as np

angle = np.radians(60)  # RY rota por angle/2, así que usamos 60° para 30°
qc = QuantumCircuit(1, 1)
qc.ry(angle, 0)
qc.measure(0, 0)

sampler = StatevectorSampler()
for shots in [100, 1024, 10000]:
    result = sampler.run([qc], shots=shots).result()
    counts = result[0].data.c.get_counts()
    p0_emp = counts.get('0', 0) / shots
    print(f"shots={shots}: P(0) empírico={p0_emp:.4f}, teórico={np.cos(angle/2)**2:.4f}")
```

**Pista:** El error estadístico escala como $1/\sqrt{N}$ con el número de shots.

**Solución:** `Soluciones/01_fundamentos_y_qiskit.md`

---

## Ejercicio 12 — Interferencia cuántica

**Módulo:** `01_fundamentos/07_algoritmos_cuanticos_introductorios.md`

**Enunciado:**
La interferencia cuántica es el mecanismo central de la ventaja cuántica.

a) Aplica el circuito H-Z-H a $|0\rangle$ y calcula el estado final paso a paso.
b) ¿Qué ocurre si mides justo después de la primera H, antes de Z? ¿Es lo mismo que aplicar el circuito completo?
c) Compara los resultados de medir en distinto orden:

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

# Circuito completo antes de medir
qc1 = QuantumCircuit(1)
qc1.h(0)
qc1.z(0)
qc1.h(0)
print("H-Z-H|0> =", Statevector.from_instruction(qc1))

# Circuito con colapso intermedio (simulado)
qc2 = QuantumCircuit(1)
qc2.h(0)
# Aquí el estado colapsa a |0> o |1> con prob. 50/50
qc2.z(0)
qc2.h(0)
print("Estado sin colapso intermedio (referencia):", Statevector.from_instruction(qc2))
```

d) Explica por qué H-Z-H = X usando el resultado de la Ejercicio 3c.

**Pista:** La interferencia destructiva elimina la amplitud de $|1\rangle$ en H-Z-H.

**Solución:** `Soluciones/01_fundamentos_y_qiskit.md`

---

## Ejercicio 13 — Medición en distintas bases

**Módulo:** `02_qiskit_basico/08_qiskit_simuladores_estado_y_resultados.md`

**Enunciado:**
Medir en la base $\{|+\rangle, |-\rangle\}$ equivale a aplicar H antes de medir en la base computacional.

a) Prepara $|+\rangle$ y mídelo en la base $\{|+\rangle, |-\rangle\}$. ¿Cuál es el resultado esperado?
b) Prepara $|-\rangle$ y mídelo en la misma base.
c) Implementa ambas mediciones con Qiskit:

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

# Medir |+> en base X
qc = QuantumCircuit(1, 1)
qc.h(0)       # prepara |+>
qc.h(0)       # rota a base computacional
qc.measure(0, 0)

sampler = StatevectorSampler()
result = sampler.run([qc], shots=2048).result()
print("Medir |+> en base X:", result[0].data.c.get_counts())
```

**Pista:** Si el estado es un autovector de la base de medición, el resultado es determinista.

**Solución:** `Soluciones/01_fundamentos_y_qiskit.md`

---

## Ejercicio 14 — Producto interno y ortogonalidad

**Módulo:** `01_fundamentos/06_algebra_lineal_minima_para_computacion_cuantica.md`

**Enunciado:**
Dos estados son ortogonales si su producto interno es cero: $\langle\psi|\phi\rangle = 0$.

a) Verifica que $\langle 0|1\rangle = 0$ y que $\langle +|-\rangle = 0$.
b) Calcula $|\langle +|0\rangle|^2$. ¿Qué interpretación tiene?
c) Demuestra que $\{|0\rangle, |1\rangle\}$ y $\{|+\rangle, |-\rangle\}$ son ambas bases ortonormales.

```python
import numpy as np

ket0 = np.array([1, 0])
ket1 = np.array([0, 1])
ketp = np.array([1, 1]) / np.sqrt(2)
ketm = np.array([1, -1]) / np.sqrt(2)

print("<0|1> =", np.dot(ket0.conj(), ket1))
print("<+|-> =", np.dot(ketp.conj(), ketm))
print("|<+|0>|² =", abs(np.dot(ketp.conj(), ket0))**2)
```

**Pista:** $|\langle +|0\rangle|^2 = 1/2$ es la probabilidad de medir $|+\rangle$ en el estado $|0\rangle$.

**Solución:** `Soluciones/01_fundamentos_y_qiskit.md`

---

## Ejercicio 15 — Estimator y valores esperados

**Módulo:** `02_qiskit_basico/08_qiskit_simuladores_estado_y_resultados.md`

**Enunciado:**
El `StatevectorEstimator` calcula $\langle\psi|O|\psi\rangle$ para un observable O.

a) Prepara el estado $|\psi\rangle = R_y(\pi/3)|0\rangle$ y calcula $\langle Z\rangle$, $\langle X\rangle$ e $\langle Y\rangle$.
b) Verifica que $\langle X\rangle^2 + \langle Y\rangle^2 + \langle Z\rangle^2 = 1$ (estado puro).
c) Implementa:

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp
import numpy as np

qc = QuantumCircuit(1)
qc.ry(np.pi / 3, 0)

estimator = StatevectorEstimator()
observables = [SparsePauliOp("X"), SparsePauliOp("Y"), SparsePauliOp("Z")]
results = estimator.run([(qc, obs) for obs in observables]).result()

vals = [float(r.data.evs) for r in results]
print(f"<X>={vals[0]:.4f}, <Y>={vals[1]:.4f}, <Z>={vals[2]:.4f}")
print(f"|r|² = {sum(v**2 for v in vals):.6f}")
```

**Pista:** El vector de Bloch de un estado puro siempre tiene norma 1.

**Solución:** `Soluciones/01_fundamentos_y_qiskit.md`
