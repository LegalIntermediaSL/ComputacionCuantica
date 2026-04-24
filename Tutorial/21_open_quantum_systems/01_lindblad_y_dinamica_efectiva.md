# La ecuación de Lindblad y la dinámica de sistemas abiertos

## 1. Sistemas cuánticos abiertos

Un sistema cuántico abierto es un sistema $S$ en contacto con un entorno (baño térmico) $B$. La evolución del sistema compuesto $S+B$ es unitaria, pero la evolución del subsistema $S$ por sí solo no lo es.

Si el estado del sistema compuesto es $\rho_{SB}$, el estado reducido del sistema es:

$$
\rho_S = \text{Tr}_B(\rho_{SB})
$$

La evolución de $\rho_S$ es, en general, un canal cuántico CPTP. Para describir la evolución temporal continua del sistema abierto, necesitamos una **ecuación maestra**.

## 2. La aproximación de Markov

En muchos sistemas físicos, el entorno tiene una memoria temporal $\tau_B$ mucho más corta que la escala temporal de relajación del sistema $\tau_S$:

$$
\tau_B \ll \tau_S
$$

Esta condición se denomina **aproximación de Markov**: el baño "olvida" la correlación con el sistema rápidamente, y la evolución futura del sistema solo depende de su estado actual, no de su historia.

La aproximación de Markov permite derivar una ecuación de evolución local en el tiempo para $\rho_S$, sin necesidad de seguir la dinámica completa del baño.

## 3. La ecuación maestra de Lindblad

Bajo la aproximación de Markov y la aproximación de acoplamiento débil (Born), la ecuación maestra más general que preserva la positividad completa y la traza es la **ecuación de Lindblad** (Gorini-Kossakowski-Sudarshan-Lindblad, 1976):

$$
\frac{d\rho}{dt} = -\frac{i}{\hbar}[H_S, \rho] + \sum_k \gamma_k \left( L_k \rho L_k^\dagger - \frac{1}{2}\{L_k^\dagger L_k, \rho\} \right)
$$

Los dos términos tienen interpretaciones claras:

**Término coherente:** $-\frac{i}{\hbar}[H_S, \rho]$ es la ecuación de von Neumann para la evolución unitaria bajo el Hamiltoniano del sistema $H_S$.

**Término disipativo (Lindblad):** $\sum_k \gamma_k \mathcal{L}(L_k)[\rho]$, donde $\mathcal{L}(L)[\rho] = L\rho L^\dagger - \frac{1}{2}\{L^\dagger L, \rho\}$ es el **superoperador de Lindblad**. Los operadores $L_k$ son los **operadores de salto** (jump operators) que describen los canales de disipación, y $\gamma_k > 0$ son las tasas de relajación.

## 4. Operadores de salto y procesos físicos

Los operadores de salto $L_k$ capturan los procesos físicos que acoplan el sistema al baño:

**Relajación $T_1$ (amortiguamiento de amplitud):** el qubit decae de $|1\rangle$ a $|0\rangle$. Operador de salto: $L = \sigma_- = |0\rangle\langle 1|$. La tasa $\gamma = 1/T_1$.

$$
\mathcal{L}(\sigma_-)[\rho] = \sigma_- \rho \sigma_-^\dagger - \frac{1}{2}\{\sigma_+\sigma_-, \rho\}
$$

**Desfase $T_2$ (dephasing):** pérdida de coherencia sin cambio de población. Operador de salto: $L = \sigma_z/\sqrt{2}$. La tasa $\gamma_\phi = 1/T_2 - 1/(2T_1)$.

**Absorción (para bañ caliente):** el qubit absorbe energía del baño, $|0\rangle \to |1\rangle$. Operador de salto: $L = \sigma_+$. Tasa $\gamma n_\text{th}$ donde $n_\text{th}$ es el número de ocupación térmico.

## 5. Solución estacionaria: equilibrio térmico

Para el sistema de dos niveles con relajación a temperatura $T$, la solución estacionaria de la ecuación de Lindblad es el estado de Gibbs:

$$
\rho_\infty = \frac{e^{-H_S/k_BT}}{Z}, \quad Z = \text{Tr}(e^{-H_S/k_BT})
$$

Para $T \to 0$: $\rho_\infty = |0\rangle\langle 0|$ (estado fundamental).
Para $T \to \infty$: $\rho_\infty = I/2$ (mezcla máxima).

## 6. Implementación en Qiskit Aer

```python
from qiskit import QuantumCircuit
from qiskit_aer import QasmSimulator, AerSimulator
from qiskit_aer.noise import NoiseModel
from qiskit_aer.quantum_info import SuperOp
import numpy as np

# Simular la ecuación de Lindblad con Qiskit Aer
# Qiskit Aer puede resolver la ecuación de Lindblad directamente
# para modelos de ruido definidos via NoiseModel

from qiskit_aer.noise import thermal_relaxation_error

# Parámetros físicos representativos
T1 = 100e-6   # 100 microsegundos
T2 = 80e-6    # 80 microsegundos
time = 10e-6  # Tiempo de evolución: 10 microsegundos

# Canal de relajación térmica para t = 10 μs, T1 = 100 μs, T2 = 80 μs
thermal_error = thermal_relaxation_error(T1, T2, time, excited_state_population=0)

# Aplicar el canal al estado |1>
from qiskit.quantum_info import DensityMatrix
import qiskit.quantum_info as qi

# Canal de amortiguamiento de amplitud para tiempo 'time'
gamma = 1 - np.exp(-time / T1)
p_dephase = 0.5 * (1 - np.exp(-time / T2))

rho_1 = np.array([[0, 0], [0, 1]])  # Estado |1>

# Aplicar amortiguamiento de amplitud
K0 = np.array([[1, 0], [0, np.sqrt(1 - gamma)]])
K1 = np.array([[0, np.sqrt(gamma)], [0, 0]])
rho_after = K0 @ rho_1 @ K0.T.conj() + K1 @ rho_1 @ K1.T.conj()

print(f"Estado |1> tras t = {time*1e6:.1f} μs:")
print(f"  Poblaciones: P(0) = {rho_after[0,0].real:.4f}, P(1) = {rho_after[1,1].real:.4f}")
print(f"  Coherencias: ρ_01 = {rho_after[0,1]:.4f}")
print(f"  (Esperado P(1) = exp(-t/T1) = {np.exp(-time/T1):.4f})")
```

## 7. Más allá de Markov: efectos de memoria

En algunos sistemas (centros NV en diamante, moléculas en entornos biológicos), la escala de tiempo del baño $\tau_B$ no es mucho menor que $\tau_S$. En este caso, la aproximación de Markov falla y se necesitan ecuaciones maestras **no-Markovianas**.

Los sistemas no-Markovianos exhiben:
- **Renacimiento de coherencia:** coherencias que reaparecen después de haberse disipado.
- **Back-flow de información:** el sistema recupera información que había perdido en el baño.
- **Correlaciones temporales:** el estado futuro depende de la historia, no solo del estado actual.

Estas características son de interés en biología cuántica (fotosíntesis, navegación magnética de aves) y en el diseño de memorias cuánticas.

## 8. Ideas clave

- La ecuación de Lindblad describe la evolución temporal de sistemas cuánticos abiertos bajo las aproximaciones de Markov y Born.
- Combina evolución coherente ($[H_S, \rho]$) y disipación (operadores de salto $L_k$ con tasas $\gamma_k$).
- Los operadores de salto $\sigma_-$ y $\sigma_z$ capturan relajación $T_1$ y desfase $T_2$ respectivamente.
- La solución estacionaria a temperatura $T$ es el estado de Gibbs.
- Cuando la aproximación de Markov falla (escala de tiempo del baño comparable a la del sistema), aparecen efectos no-Markovianos como renacimiento de coherencia.

## 9. Ejercicios sugeridos

1. Resolver la ecuación de Lindblad para un qubit con solo desfase ($L = \sigma_z$, $\gamma = 1/T_2$) partiendo del estado $|+\rangle$ y calcular las coherencias en función del tiempo.
2. Verificar que el estado de Gibbs $\rho_\infty = e^{-H/k_BT}/Z$ satisface $d\rho_\infty/dt = 0$ bajo la ecuación de Lindblad con relajación y absorción.
3. Implementar el canal de relajación térmica en Qiskit Aer y medir la curva de decaimiento del estado $|1\rangle$ para distintos valores de $T_1$.
4. Describir un experimento físico donde la aproximación de Markov podría fallar y qué señal experimental lo evidenciaría.

## Navegacion

- Anterior: [Simulacion digital frente a analogica](../20_simulacion_cuantica_avanzada/02_simulacion_digital_frente_a_analogica.md)
- Siguiente: [Decoherencia, relajacion y markovianidad](02_decoherencia_relajacion_y_markovianidad.md)
