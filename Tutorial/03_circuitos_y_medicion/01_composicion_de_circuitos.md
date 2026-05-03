# Composición de circuitos cuánticos

## 1. Puertas compuestas y subcircuitos

Un circuito cuántico en Qiskit es un objeto `QuantumCircuit` al que se añaden puertas secuencialmente. Para circuitos más grandes conviene definir **subcircuitos** reutilizables:

```python
from qiskit import QuantumCircuit

def bloque_swap(n: int) -> QuantumCircuit:
    """Intercambia qubit 0 y qubit n-1 usando tres CNOT."""
    qc = QuantumCircuit(n, name="swap_extremos")
    qc.cx(0, n - 1)
    qc.cx(n - 1, 0)
    qc.cx(0, n - 1)
    return qc

# Componer en un circuito mayor
qc = QuantumCircuit(4)
qc.h(range(4))
qc.compose(bloque_swap(4), inplace=True)
qc.draw("text")
```

`compose` inserta el subcircuito respetando el orden de qubits; `inplace=True` modifica el circuito en lugar de devolver uno nuevo.

## 2. Barreras

Las barreras no afectan la física del circuito, pero impiden que el transpilador fusione puertas a través de ellas y mejoran la legibilidad:

```python
qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.barrier()          # separador visual y de optimización
qc.x(2)
qc.cx(1, 2)
```

Son especialmente útiles para separar la fase de preparación, la fase de oráculo y la fase de medición en algoritmos como Grover o QPE.

## 3. Registros clásicos y medición parcial

Qiskit permite definir registros clásicos con nombres descriptivos y medir solo un subconjunto de qubits:

```python
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

qr = QuantumRegister(3, "q")
cr_ancilla = ClassicalRegister(1, "anc")
cr_datos = ClassicalRegister(2, "dat")

qc = QuantumCircuit(qr, cr_ancilla, cr_datos)
qc.h(qr[0])
qc.cx(qr[0], qr[1])
qc.cx(qr[0], qr[2])
qc.measure(qr[0], cr_ancilla[0])   # medir ancilla por separado
qc.measure(qr[1:3], cr_datos)      # medir qubits de datos
```

La medición parcial permite implementar protocolos como la teleportación cuántica, donde la medición de Bell en el emisor condiciona la corrección en el receptor.

## 4. Puertas parametrizadas

Las puertas `Ry(θ)`, `Rz(φ)` y `U(θ, φ, λ)` aceptan ángulos simbólicos de tipo `Parameter`. Esto es la base de los circuitos variacionales:

```python
from qiskit.circuit import Parameter

theta = Parameter("θ")
phi   = Parameter("φ")

qc = QuantumCircuit(2)
qc.ry(theta, 0)
qc.rz(phi, 1)
qc.cx(0, 1)

# Instanciar con valores concretos
qc_bound = qc.assign_parameters({theta: 0.5, phi: 1.2})
```

El circuito parametrizado puede enviarse completo al transpilador y luego instanciarse para distintos valores sin re-transpilar.

## 5. Estados de Bell

Los cuatro estados de Bell son estados bipartitos máximamente entrelazados:

$$
|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}, \quad
|\Phi^-\rangle = \frac{|00\rangle - |11\rangle}{\sqrt{2}},
$$

$$
|\Psi^+\rangle = \frac{|01\rangle + |10\rangle}{\sqrt{2}}, \quad
|\Psi^-\rangle = \frac{|01\rangle - |10\rangle}{\sqrt{2}}.
$$

En Qiskit se preparan con una puerta H seguida de CNOT, más una corrección de fase/flip opcional:

```python
from qiskit.quantum_info import Statevector
import numpy as np

def bell_state(tipo: str) -> Statevector:
    qc = QuantumCircuit(2)
    if tipo in ("Phi-", "Psi-"):
        qc.z(0)
    if tipo in ("Psi+", "Psi-"):
        qc.x(0)
    qc.h(0)
    qc.cx(0, 1)
    return Statevector(qc)

sv = bell_state("Phi+")
print(np.round(sv.data, 3))   # [0.707, 0, 0, 0.707]
```

Para verificar el entrelazamiento se puede calcular la entropía de von Neumann del estado reducido:

```python
from qiskit.quantum_info import partial_trace, entropy

rho = sv.to_operator()          # DensityMatrix
rho_A = partial_trace(sv, [1])  # traza sobre qubit 1
S = entropy(rho_A, base=2)
print(f"Entropía de entrelazamiento: {S:.4f} ebits")  # → 1.0 ebit
```

Un estado de Bell tiene entropía de entrelazamiento = 1 ebit, el máximo para un par de qubits.

## 6. Circuito de teleportación (esquema)

La teleportación cuántica transmite el estado desconocido de un qubit usando un par de Bell y dos bits clásicos:

```
Alice:  |ψ⟩ ──●── H ──M──╮
               │          │  (2 bits clásicos)
Bell:   |0⟩ ──X──────M──╯──→  corrección en Bob
        |0⟩ ──────────────╯──→  X^m1 Z^m0 ──|ψ⟩
```

La implementación completa se desarrolla en el lab `02_teleportacion_guiada.ipynb`.

## Resumen

| Concepto | API Qiskit | Uso típico |
|---|---|---|
| Subcircuito | `qc.compose(sub, inplace=True)` | Reutilizar bloques |
| Barrera | `qc.barrier()` | Separar fases, guiar transpilador |
| Registro clásico nombrado | `ClassicalRegister(n, "nombre")` | Medición parcial clara |
| Puerta parametrizada | `Parameter("θ")` + `assign_parameters` | VQE, QAOA |
| Estado de Bell | H + CNOT | Entrelazamiento, teleportación, QKD |
