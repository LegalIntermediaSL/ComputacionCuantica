# Operadores de Kraus, decoherencia y modelos de ruido

## 1. Los canales de ruido fundamentales

La práctica experimental con procesadores cuánticos superconductores ha identificado tres tipos de ruido dominantes, cada uno con su representación en operadores de Kraus.

## 2. Canal de desfase (phase-flip o dephasing)

El canal de desfase modela la pérdida de coherencia entre $|0\rangle$ y $|1\rangle$ sin cambiar las poblaciones. Con probabilidad $p$ el estado sufre un error $Z$:

$$
\mathcal{E}_\phi(\rho) = (1-p)\rho + p Z\rho Z
$$

Los operadores de Kraus son $K_0 = \sqrt{1-p}\,I$ y $K_1 = \sqrt{p}\,Z$.

Efecto sobre la matriz de densidad:

$$
\begin{pmatrix} \rho_{00} & \rho_{01} \\ \rho_{10} & \rho_{11} \end{pmatrix} \to \begin{pmatrix} \rho_{00} & (1-2p)\rho_{01} \\ (1-2p)\rho_{10} & \rho_{11} \end{pmatrix}
$$

Las poblaciones ($\rho_{00}$, $\rho_{11}$) no cambian; las coherencias ($\rho_{01}$, $\rho_{10}$) se amortiguan. Este canal describe el tiempo $T_2$ en hardware real.

## 3. Canal de amortiguamiento de amplitud (amplitude damping)

El canal de amortiguamiento de amplitud modela la relajación espontánea: el qubit decae desde $|1\rangle$ a $|0\rangle$ con probabilidad $\gamma$. Modela el tiempo $T_1$.

Los operadores de Kraus son:

$$
K_0 = \begin{pmatrix} 1 & 0 \\ 0 & \sqrt{1-\gamma} \end{pmatrix}, \quad K_1 = \begin{pmatrix} 0 & \sqrt{\gamma} \\ 0 & 0 \end{pmatrix}
$$

Efecto sobre el estado:

$$
\rho \to \begin{pmatrix} \rho_{00} + \gamma\rho_{11} & \sqrt{1-\gamma}\,\rho_{01} \\ \sqrt{1-\gamma}\,\rho_{10} & (1-\gamma)\rho_{11} \end{pmatrix}
$$

El estado $|1\rangle$ decae gradualmente hacia $|0\rangle$. Las coherencias también se amortiguan como $\sqrt{1-\gamma}$.

## 4. Canal de bit-flip

El canal de bit-flip modela errores de tipo $X$ (inversión de bit) con probabilidad $p$:

$$
\mathcal{E}_{BF}(\rho) = (1-p)\rho + p X\rho X
$$

Operadores de Kraus: $K_0 = \sqrt{1-p}\,I$, $K_1 = \sqrt{p}\,X$.

## 5. Relación entre canales y tiempos de coherencia

En hardware superconductor, los parámetros de los canales de ruido están relacionados con los tiempos de coherencia medibles:

$$
\gamma = 1 - e^{-t/T_1}, \quad p_\phi = \frac{1}{2}\left(1 - e^{-t/T_2^*}\right)
$$

donde $T_2^* \leq 2T_1$ (por la desigualdad de relajación-desfase).

Para los mejores procesadores superconductores actuales (2025):
- $T_1 \sim 100\text{–}500 \,\mu s$
- $T_2^* \sim 50\text{–}200 \,\mu s$
- $T_2^{\text{echo}} \sim 100\text{–}400 \,\mu s$ (con secuencias de refocalización)

## 6. Modelos de ruido en Qiskit Aer

```python
from qiskit_aer.noise import (NoiseModel, depolarizing_error,
                               amplitude_damping_error, phase_damping_error)
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.primitives import StatevectorSampler

# Parámetros representativos de hardware superconductor
T1 = 100e-6      # 100 microsegundos
T2 = 80e-6       # 80 microsegundos
gate_time = 50e-9  # Tiempo de puerta de 1 qubit: 50 ns
cx_time = 300e-9   # Tiempo de puerta CX: 300 ns

# Calcular parámetros de ruido para tiempo de puerta
gamma_1q = 1 - np.exp(-gate_time / T1)
gamma_2q = 1 - np.exp(-cx_time / T1)
p_dephase_1q = 0.5 * (1 - np.exp(-gate_time / T2))

import numpy as np

noise_model = NoiseModel()

# Error de 1 qubit: amortiguamiento + desfase
amp_error = amplitude_damping_error(gamma_1q)
deph_error = phase_damping_error(p_dephase_1q)
combined_1q = amp_error.compose(deph_error)
noise_model.add_all_qubit_quantum_error(combined_1q, ['u1', 'u2', 'u3', 'rx', 'ry', 'rz', 'h'])

# Error de 2 qubits: despolarización
depol_cx = depolarizing_error(0.01, 2)  # 1% de error por CNOT
noise_model.add_all_qubit_quantum_error(depol_cx, ['cx'])

# Probar el modelo de ruido
backend = AerSimulator(noise_model=noise_model)

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

job = backend.run(qc, shots=8192)
counts = job.result().get_counts()
print(f"Estado de Bell con ruido: {counts}")
# Sin ruido esperaríamos solo 00 y 11; con ruido aparecen 01 y 10
```

## 7. Mitigación de errores

Dado que el ruido no puede eliminarse completamente en hardware NISQ, se usan técnicas de **mitigación de errores** para mejorar los resultados:

**Zero Noise Extrapolation (ZNE):** ejecutar el circuito a distintos niveles de ruido amplificado y extrapolar al límite de ruido cero.

**Probabilistic Error Cancellation (PEC):** representar el canal sin ruido como combinación lineal de canales ruidosos y usar muestreo estocástico para cancelar el error.

**Measurement Error Mitigation:** corregir los errores de lectura (readout errors) mediante una matriz de calibración.

## 8. Ideas clave

- El canal de desfase amortigua las coherencias sin cambiar las poblaciones; modela $T_2$.
- El canal de amortiguamiento de amplitud modela la relajación $T_1$: el qubit decae de $|1\rangle$ a $|0\rangle$.
- Los tiempos de coherencia $T_1$ y $T_2$ determinan los parámetros de los canales de Kraus.
- Qiskit Aer permite simular circuitos con modelos de ruido realistas usando `NoiseModel`.
- La mitigación de errores (ZNE, PEC) reduce el sesgo de los resultados sin corrección de errores completa.

## 9. Ejercicios sugeridos

1. Calcular los operadores de Kraus del canal de amortiguamiento de amplitud para $\gamma = 0.1$ y verificar la condición de completitud.
2. Simular el circuito de Bell con el modelo de ruido y medir la distancia entre la distribución ideal y la ruidosa.
3. Implementar el canal de desfase manualmente y verificar que solo afecta a las coherencias off-diagonal de $\rho$.
4. Calcular $T_1$ efectivo de un procesador dado que la fidelidad del estado $|1\rangle$ cae a $1/e$ en 80 μs.

## Navegacion

- Anterior: [Canales cuanticos: intuicion y representacion](01_canales_cuanticos_intuicion_y_representacion.md)
- Siguiente: [Proyectores, valores esperados y varianza](../17_medicion_avanzada_y_observables/01_proyectores_valores_esperados_y_varianza.md)
