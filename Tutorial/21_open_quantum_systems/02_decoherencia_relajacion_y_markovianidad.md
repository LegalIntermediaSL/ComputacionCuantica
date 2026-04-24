# Decoherencia, relajación y tiempos de coherencia

## 1. Decoherencia: la barrera entre lo cuántico y lo clásico

La **decoherencia** es el proceso por el cual un estado cuántico en superposición pierde sus propiedades de interferencia al interactuar con el entorno. Es el mecanismo fundamental que hace que los objetos macroscópicos se comporten de forma clásica.

Para un qubit en el estado $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$, la matriz de densidad inicial es:

$$
\rho = \begin{pmatrix} |\alpha|^2 & \alpha\beta^* \\ \alpha^*\beta & |\beta|^2 \end{pmatrix}
$$

Los elementos diagonales $|\alpha|^2$ y $|\beta|^2$ son las **poblaciones** (probabilidades de $|0\rangle$ y $|1\rangle$). Los elementos fuera de la diagonal $\alpha\beta^*$ y $\alpha^*\beta$ son las **coherencias**, que cuantifican la superposición cuántica.

Bajo decoherencia, las coherencias se atenúan exponencialmente mientras las poblaciones evolucionan más lentamente. Cuando las coherencias se anulan, $\rho$ se convierte en una mezcla diagonal:

$$
\rho \to \begin{pmatrix} |\alpha|^2 & 0 \\ 0 & |\beta|^2 \end{pmatrix}
$$

Este estado no tiene interferencia: es equivalente a una distribución de probabilidad clásica.

## 2. Tiempo de relajación $T_1$

El tiempo $T_1$ (tiempo de relajación longitudinal o tiempo de vida del estado excitado) es el tiempo característico de decaimiento de la población del estado $|1\rangle$:

$$
\rho_{11}(t) = \rho_{11}(0) \cdot e^{-t/T_1}
$$

Físicamente, $T_1$ mide cuánto tarda el qubit en emitir su energía al entorno y caer al estado fundamental $|0\rangle$. En procesadores superconductores, $T_1$ está limitado por:

- Radiación espontánea hacia los cables de control.
- Absorción por materiales dieléctricos con pérdidas.
- Fluctuaciones de flujo magnético (two-level systems en la unión de Josephson).

Valores típicos en hardware actual: $T_1 \sim 50$-$500 \,\mu s$.

## 3. Tiempo de coherencia $T_2$

El tiempo $T_2$ (tiempo de desfase transversal) mide la pérdida de coherencia entre $|0\rangle$ y $|1\rangle$:

$$
\rho_{01}(t) = \rho_{01}(0) \cdot e^{-t/T_2}
$$

La desigualdad fundamental:

$$
T_2 \leq 2T_1
$$

garantiza que la pérdida de coherencia (al menos por relajación) no puede ser más lenta que la relajación de la población.

La diferencia $\frac{1}{T_2} - \frac{1}{2T_1}$ mide el **desfase puro** ($T_\phi$):

$$
\frac{1}{T_2} = \frac{1}{2T_1} + \frac{1}{T_\phi}
$$

El desfase puro es causado por fluctuaciones de baja frecuencia en la frecuencia de transición del qubit (fluctuaciones de $1/f$ en el flujo magnético, ruido de carga).

**Experimento de Hahn echo:** aplicando una puerta $X$ en el punto medio de la evolución ($t/2$), se revierten los efectos de las fluctuaciones de frecuencia estáticas. El tiempo de desfase medido con echo se denomina $T_2^E$ y satisface $T_2 \leq T_2^E \leq 2T_1$.

## 4. Curvas de decaimiento y medición experimental

| Experimento | Cantidad medida | Tiempo medido |
|---|---|---|
| Inversion-recovery | $\rho_{11}(t)$ tras $X$ | $T_1$ |
| Ramsey | Oscilación de coherencia | $T_2^*$ (sin echo) |
| Hahn echo | Oscilación con $\pi$-pulso central | $T_2^E$ |
| CPMG (Carr-Purcell) | Echo múltiple | $T_2^\text{CPMG}$ |

En general: $T_2^* \leq T_2^E \leq T_2^\text{CPMG} \leq 2T_1$.

## 5. Implicaciones para el diseño de algoritmos

Los tiempos de coherencia imponen restricciones directas sobre los circuitos ejecutables:

**Profundidad máxima de circuito:** si cada puerta de 2 qubits toma tiempo $t_\text{gate}$, el número máximo de capas antes de que el error sea significativo es:

$$
d_\text{max} \approx \frac{T_2}{t_\text{gate}}
$$

Para $T_2 = 100\,\mu s$ y $t_\text{gate} = 300\,ns$ (CNOT): $d_\text{max} \approx 333$ puertas CNOT.

**Complejidad de algoritmo:** el algoritmo de Shor para RSA-2048 requiere $\sim 10^8$ puertas CNOT. Sin corrección de errores, es inalcanzable con hardware actual ($T_2/t_\text{gate} \sim 10^2$-$10^3$).

## 6. Simulación de la decoherencia en Qiskit

```python
from qiskit import QuantumCircuit
from qiskit_aer.noise import thermal_relaxation_error, NoiseModel
from qiskit_aer import AerSimulator
import numpy as np
import matplotlib.pyplot as plt

# Simular curva T1: inicio en |1>, medir en función del tiempo
T1 = 100e-6  # 100 μs
T2 = 80e-6   # 80 μs
times = np.linspace(0, 5*T1, 50)

p1_values = []
backend = AerSimulator()

for t in times:
    noise_model = NoiseModel()
    t_error = thermal_relaxation_error(T1, T2, t, excited_state_population=0)
    noise_model.add_all_qubit_quantum_error(t_error, ['id'])

    qc = QuantumCircuit(1, 1)
    qc.x(0)        # Preparar |1>
    qc.id(0)       # Identidad con ruido (simula evolución temporal)
    qc.measure(0, 0)

    job = backend.run(qc, noise_model=noise_model, shots=2048)
    counts = job.result().get_counts()
    p1 = counts.get('1', 0) / 2048
    p1_values.append(p1)

# Ajuste teórico: P(1) = exp(-t/T1)
t1_fit = np.exp(-times / T1)
print(f"T1 extraído de la curva: {T1*1e6:.1f} μs")
print(f"Error medio entre simulación y teoría: {np.mean(np.abs(np.array(p1_values) - t1_fit)):.4f}")
```

## 7. Ideas clave

- La decoherencia destruye las coherencias off-diagonal de $\rho$, eliminando la interferencia cuántica.
- $T_1$ mide la relajación de la población del estado excitado; $T_2$ mide la pérdida de coherencia.
- Siempre $T_2 \leq 2T_1$; el desfase puro aporta la diferencia.
- Los tiempos de coherencia limitan directamente la profundidad de circuito ejecutable sin corrección de errores.
- Las secuencias de refocalización (Hahn echo, CPMG) pueden extender $T_2$ mitigando el ruido de baja frecuencia.

## 8. Ejercicios sugeridos

1. Calcular $T_\phi$ dado $T_1 = 150\,\mu s$ y $T_2 = 80\,\mu s$.
2. Implementar un experimento de Ramsey en Qiskit Aer con desfase puro y medir $T_2^*$.
3. Estimar el tiempo máximo de simulación (circuito) para un procesador con $T_2 = 200\,\mu s$ y puertas CNOT de $200\,ns$.
4. Explicar físicamente por qué el experimento de Hahn echo es insensible al ruido estático de baja frecuencia pero sí al ruido de alta frecuencia.

## Navegacion

- Anterior: [Lindblad y dinamica efectiva](01_lindblad_y_dinamica_efectiva.md)
- Siguiente: [Coherencia, entrelazamiento y utilidad](../22_recursos_cuanticos/01_coherencia_entrelazamiento_y_utilidad.md)
