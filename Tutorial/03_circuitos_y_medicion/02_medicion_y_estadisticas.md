# Medición cuántica y estadísticas

## 1. El postulado de la medición

Medir el qubit $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$ en la base computacional $\{|0\rangle, |1\rangle\}$ produce:

- resultado 0 con probabilidad $p_0 = |\alpha|^2$, colapsando el estado a $|0\rangle$
- resultado 1 con probabilidad $p_1 = |\beta|^2$, colapsando el estado a $|1\rangle$

con $p_0 + p_1 = 1$. La medición es irreversible: destruye la superposición.

## 2. Medición en distintas bases de Pauli

La base computacional estándar es la base Z ($\{|0\rangle, |1\rangle\}$). Para medir en otras bases hay que aplicar un cambio de base antes de la medición estándar:

| Base | Autoestados | Cambio de base |
|---|---|---|
| Z | $\|0\rangle, \|1\rangle$ | ninguno |
| X | $\|+\rangle = \frac{\|0\rangle+\|1\rangle}{\sqrt{2}},\ \|-\rangle$ | H antes de medir |
| Y | $\|+i\rangle = \frac{\|0\rangle+i\|1\rangle}{\sqrt{2}},\ \|-i\rangle$ | S†·H antes de medir |

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def medir_en_base(estado: QuantumCircuit, base: str) -> QuantumCircuit:
    qc = estado.copy()
    n = qc.num_qubits
    if base == "X":
        qc.h(range(n))
    elif base == "Y":
        qc.sdg(range(n))
        qc.h(range(n))
    qc.measure_all()
    return qc
```

Medir el estado $|+\rangle = H|0\rangle$ en base X siempre da resultado 0 (autoestado con autovalor +1); en base Z da 0 o 1 con igual probabilidad.

## 3. El papel de los shots

Con $N$ shots (repeticiones) la frecuencia observada $\hat{p}$ converge a la probabilidad real $p$ con error estándar:

$$
\sigma_{\hat{p}} = \sqrt{\frac{p(1-p)}{N}} \leq \frac{1}{2\sqrt{N}}.
$$

Para $N = 1024$ shots, $\sigma \lesssim 1.6\%$. Para error $< 0.1\%$ se necesitan $N \gtrsim 250\,000$ shots.

```python
from qiskit.primitives import StatevectorSampler
import numpy as np

qc = QuantumCircuit(1)
qc.h(0)
qc.measure_all()

sampler = StatevectorSampler()
job = sampler.run([qc], shots=8192)
result = job.result()
counts = result[0].data.meas.get_counts()

p_0 = counts.get("0", 0) / 8192
p_1 = counts.get("1", 0) / 8192
sigma = np.sqrt(0.25 / 8192)
print(f"p(0) = {p_0:.4f} ± {sigma:.4f}")  # ≈ 0.500 ± 0.006
```

## 4. Distribuciones de probabilidad

Para un circuito de $n$ qubits la medición produce una distribución sobre $2^n$ cadenas de bits. Qiskit devuelve:

- **`counts`**: diccionario `{bitstring: frecuencia}` — conveniente para pocos resultados dominantes
- **`probabilities()`**: vector de probabilidades ideales (sin shots) a partir de `Statevector`

```python
from qiskit.quantum_info import Statevector

qc_ghz = QuantumCircuit(3)
qc_ghz.h(0)
qc_ghz.cx(0, 1)
qc_ghz.cx(0, 2)

sv = Statevector(qc_ghz)
probs = sv.probabilities_dict()
print(probs)   # {'000': 0.5, '111': 0.5}
```

El estado GHZ $\frac{|000\rangle + |111\rangle}{\sqrt{2}}$ tiene solo dos resultados posibles, cada uno con probabilidad 0.5.

## 5. Error estocástico vs. error sistemático

| Fuente de error | Naturaleza | Reducción |
|---|---|---|
| Shots finitos | Estocástico, $\propto 1/\sqrt{N}$ | Aumentar shots |
| Ruido de puerta | Sistemático (depolarizante, T1/T2) | Mitigación de errores (ZNE, PEC) |
| Readout error | Sistemático (confusión 0↔1) | Matrices de calibración (M3) |
| Transpilación | Determinista (puertas extra) | Nivel de optimización 2-3 |

Con el simulador `StatevectorSampler` el único error es el estocástico (shots). Con hardware real todos los errores se superponen.

## 6. Valor esperado de un observable

Para calcular $\langle \psi | O | \psi \rangle$ sin simular explícitamente la distribución se usa el `StatevectorEstimator`:

```python
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

# Observable ZZ: correlación entre qubits 0 y 1
obs = SparsePauliOp("ZZ")
estimator = StatevectorEstimator()
job = estimator.run([(qc, obs)])
ev = job.result()[0].data.evs
print(f"⟨ZZ⟩ = {ev:.4f}")   # → −1.0 para estado |Φ−⟩ o +1.0 para |Φ+⟩
```

Para el estado de Bell $|\Phi^+\rangle$ el valor esperado de ZZ es $+1$: los dos qubits siempre miden el mismo valor.

## Resumen

- Medir en base X/Y requiere un cambio de base antes de la medición estándar.
- El error estadístico decrece como $1/\sqrt{N}$; para alta precisión hay que aumentar los shots o usar el estimador analítico.
- `StatevectorSampler` → distribución de bits; `StatevectorEstimator` → valor esperado de observable.
- El ruido del hardware añade error sistemático que requiere técnicas de mitigación.
