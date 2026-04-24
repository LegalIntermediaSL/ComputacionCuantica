# Mitigación de errores cuánticos: ZNE y PEC

## 1. El problema: ruido sin corrección completa

La corrección de errores cuántica (QEC) requiere un overhead de qubits físicos de $10^3$-$10^4$ por qubit lógico, fuera del alcance del hardware NISQ actual. Mientras tanto, la **mitigación de errores cuánticos** (QEM, Quantum Error Mitigation) ofrece una alternativa: no elimina los errores, pero extrae estimaciones de valores esperados más precisas que los datos ruidosos directos, a costa de un mayor número de shots.

A diferencia de QEC, QEM no protege el estado cuántico durante el cómputo, sino que post-procesa los resultados estadísticos para aproximar lo que se obtendría en un dispositivo ideal.

## 2. Zero-Noise Extrapolation (ZNE)

### 2.1 Principio

ZNE se basa en la observación de que el error de los circuitos NISQ escala con el nivel de ruido del hardware. Si podemos ejecutar el mismo circuito a diferentes niveles de ruido controlados $\lambda_1 < \lambda_2 < \ldots < \lambda_k$, podemos extrapolar el valor esperado al límite de ruido cero $\lambda \to 0$.

Para un observable $O$ con nivel de ruido $\lambda$:
$$
\langle O \rangle_\lambda = \langle O \rangle_0 + a_1\lambda + a_2\lambda^2 + \ldots
$$

Extrapolando a $\lambda = 0$ obtenemos una estimación de $\langle O \rangle_0$ (el valor ideal).

### 2.2 Amplificación de ruido

Para ejecutar a nivel de ruido $\lambda > 1$, se amplifica el ruido físico de forma controlada:

**Folding de puertas (gate folding):** reemplazar cada puerta $U$ por $U U^\dagger U$ (o $U (U^\dagger U)^n$). Esto triplica o quintuplica el error de esa puerta sin cambiar la unitaria neta $U U^\dagger U = U$.

**Folding de circuito completo:** reemplazar el circuito $\mathcal{C}$ por $\mathcal{C} \mathcal{C}^\dagger \mathcal{C}$, multiplicando el error total por 3.

**Stretch factors:** si el factor de amplificación es $c$, el nivel de ruido efectivo es $\lambda_c = c \cdot \lambda_0$.

### 2.3 Extrapolación

Con valores medidos $\langle O \rangle_{\lambda_c}$ para $c = 1, 3, 5, \ldots$, se ajusta un modelo de extrapolación:

**Lineal:** $\langle O \rangle_0 \approx 2\langle O \rangle_1 - \langle O \rangle_3$

**Exponencial:** $\langle O \rangle_\lambda = A e^{-b\lambda} + C$, luego $\langle O \rangle_0 = A + C$

**Richardson extrapolation de orden $k$:**
$$
\langle O \rangle_0 \approx \sum_{j=1}^k c_j \langle O \rangle_{\lambda_j}, \quad \sum_j c_j = 1
$$
con coeficientes $c_j$ determinados por la condición de que la extrapolación sea exacta para polinomios de grado hasta $k-1$.

### 2.4 Implementación con Mitiq

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

# Circuito de prueba: Bell state measurement
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

H = SparsePauliOp.from_list([("ZZ", 1.0)])

# Valor ideal: ⟨ZZ⟩ = 1 para el estado |Φ+⟩
estimator_ideal = StatevectorEstimator()
result_ideal = estimator_ideal.run([(qc, H)]).result()
E_ideal = float(result_ideal[0].data.evs)
print(f"Valor ideal ⟨ZZ⟩ = {E_ideal:.6f}")

# Simular con ruido a diferentes niveles (folding manual)
def fold_gates(circuit: QuantumCircuit, scale_factor: int) -> QuantumCircuit:
    """Folding de circuito: c → c (c† c)^n para scale_factor = 2n+1."""
    if scale_factor == 1:
        return circuit
    n_folds = (scale_factor - 1) // 2
    folded = circuit.copy()
    for _ in range(n_folds):
        folded = folded.compose(circuit.inverse())
        folded = folded.compose(circuit)
    return folded

def measure_with_noise(circuit: QuantumCircuit, observable: SparsePauliOp,
                       p_depol: float = 0.01, shots: int = 8192) -> float:
    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(depolarizing_error(p_depol, 1), ["h"])
    noise_model.add_all_qubit_quantum_error(depolarizing_error(p_depol * 10, 2), ["cx"])

    from qiskit_aer.primitives import Estimator
    estimator_noisy = Estimator(run_options={"noise_model": noise_model, "shots": shots})
    result = estimator_noisy.run([circuit], [observable]).result()
    return float(result.values[0])

# ZNE con Richardson extrapolation (orden 3)
p_noise = 0.02
scale_factors = [1, 3, 5]
E_noisy = []

for c in scale_factors:
    folded = fold_gates(qc, c)
    E_c = measure_with_noise(folded, H, p_depol=p_noise)
    E_noisy.append(E_c)
    print(f"  c={c}: ⟨ZZ⟩_λ={c} = {E_c:.4f}")

# Richardson extrapolation lineal (orden 2)
# E_0 ≈ (c2² * E1 - c1² * E2) / (c2² - c1²)
c1, c2 = scale_factors[0], scale_factors[1]
E_zne_linear = (c2**2 * E_noisy[0] - c1**2 * E_noisy[1]) / (c2**2 - c1**2)
print(f"\nZNE lineal: ⟨ZZ⟩_0 = {E_zne_linear:.4f}")
print(f"Valor ideal: ⟨ZZ⟩_0 = {E_ideal:.4f}")
print(f"Mejora relativa: {abs(E_noisy[0] - E_ideal):.4f} → {abs(E_zne_linear - E_ideal):.4f}")
```

## 3. Probabilistic Error Cancellation (PEC)

### 3.1 Principio

PEC es conceptualmente diferente: en lugar de extrapolar, **representa la operación ideal como una combinación lineal de operaciones ruidosas ejecutables** y estima el valor esperado usando muestreo Monte Carlo.

Si la operación ideal $\mathcal{E}^*$ puede escribirse como:
$$
\mathcal{E}^* = \sum_i \alpha_i \mathcal{O}_i, \quad \alpha_i \in \mathbb{R}, \quad \sum_i |\alpha_i| = \gamma
$$

donde $\mathcal{O}_i$ son operaciones ruidosas realizables en el hardware, entonces:
$$
\langle O \rangle^* = \sum_i \alpha_i \langle O \rangle_i
$$

El coste estadístico de PEC escala como $\gamma^{2n}$ para un circuito de $n$ puertas, donde $\gamma = \sum_i |\alpha_i|$ es el **overhead de sampling**.

### 3.2 Quasi-probability decomposition

Para el canal de error $\mathcal{N}$ (por ejemplo, un canal despolarizante), la inversa $\mathcal{N}^{-1}$ (que "deshace" el error) se descompone en una **cuasi-probabilidad** sobre el conjunto de operaciones de Pauli:

$$
\mathcal{N}^{-1} = \sum_i \eta_i \mathcal{P}_i
$$

donde $\eta_i$ son los coeficientes (pueden ser negativos) y $\mathcal{P}_i$ son canales de Pauli (I, X, Y, Z aplicados con cierta probabilidad). La suma $\gamma = \sum_i |\eta_i|$ determina el overhead.

Para un error despolarizante con tasa $p$:
$$
\gamma = \frac{1}{1 - 4p/3} \approx 1 + \frac{4p}{3}
$$

Para un circuito de $n$ puertas de dos qubits con $p = 0.01$: $\gamma^{2n} = (1 + 4 \cdot 0.01 / 3)^{2n} \approx e^{0.027n}$. Para $n = 100$: $\gamma^{200} \approx 14.7$, un overhead manejable.

### 3.3 Comparativa ZNE vs PEC

| Criterio | ZNE | PEC |
|---|---|---|
| **Sesgo** | Residual (depende del modelo de extrapolación) | Exacto (sin sesgo, asintóticamente) |
| **Varianza** | Baja (pocos evaluaciones adicionales) | Alta ($\propto \gamma^{2n}$) |
| **Conocimiento del ruido** | No requiere modelo detallado | Requiere caracterización precisa |
| **Facilidad de uso** | Alta (pocas líneas de código) | Media (requiere calibración) |
| **Implementación** | Mitiq, Qiskit (built-in) | Mitiq, Pennylane |

### 3.4 Cuándo usar cada método

- **ZNE:** circuitos cortos/medios ($< 50$ puertas), cuando no se dispone de un modelo detallado del error. Rápido de implementar.
- **PEC:** cuando se necesita sesgo nulo y se dispone de caracterización del hardware. Útil para benchmarking de alta precisión.
- **Para NISQ actual:** ZNE es el estándar de facto. IBM Qiskit Runtime incluye ZNE automático como opción de resilience.

## 4. Clifford Data Regression (CDR)

Un tercer método, más reciente, es la **Clifford Data Regression**: ejecutar versiones del circuito con solo puertas Clifford (simulables clásicamente), aprender la relación ruido-ideal con regresión, y aplicar la corrección al circuito con puertas T.

$$
\langle O \rangle^* \approx a \cdot \langle O \rangle_\text{ruidoso} + b
$$

donde $a, b$ se estiman de las ejecuciones Clifford. CDR combina la facilidad de ZNE con una corrección más precisa.

## 5. Implementación en Qiskit Runtime

```python
from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2, Options

# Configurar ZNE automático con Qiskit Runtime
# (requiere acceso a IBM Quantum)
# service = QiskitRuntimeService()
# backend = service.backend("ibm_brisbane")

# options = Options()
# options.resilience_level = 2  # Level 2 = ZNE activado
# options.resilience.noise_amplifier = "LocalFoldingAmplifier"
# options.resilience.extrapolator = "RichardsonExtrapolator"

# estimator = EstimatorV2(backend=backend, options=options)
# result = estimator.run([(circuit, observable)]).result()

# Simulación local del concepto:
print("Resilience levels en Qiskit Runtime:")
print("  Level 0: Sin mitigación (ruidoso directo)")
print("  Level 1: TREX (Twirled Readout Error eXtinction) — corrige errores de lectura")
print("  Level 2: ZNE — mitiga errores de puerta")
print("  Level 3: PEC — mitigación sin sesgo (costoso)")
```

## 6. Ideas clave

- La mitigación de errores (QEM) no elimina errores sino que extrae estimaciones estadísticamente más precisas a costa de más shots.
- ZNE ejecuta el circuito a varios niveles de ruido amplificado y extrapola al límite de ruido cero; es el método más usado en NISQ.
- PEC representa la operación ideal como combinación de operaciones ruidosas reales; es exacto pero costoso ($\gamma^{2n}$ overhead).
- Qiskit Runtime ofrece ZNE automático con `resilience_level = 2`.
- La mitigación es esencial para obtener resultados útiles en hardware NISQ hasta que la corrección de errores completa sea alcanzable.

## 7. Ejercicios sugeridos

1. Implementar ZNE con extrapolación lineal para el estado de Bell $|\Phi^+\rangle$ con ruido despolarizante del 2% y comparar la mejora de la estimación de $\langle ZZ \rangle$.
2. Calcular el overhead de sampling de PEC $\gamma^{2n}$ para $p = 0.01$ y $n = 10, 50, 100$ puertas CNOT.
3. Comparar el sesgo residual de ZNE lineal vs extrapolación exponencial para varios niveles de ruido.
4. Aplicar `resilience_level=2` en un simulador ruidoso de Qiskit Aer para un circuito VQE y medir la mejora en la energía estimada.

## Navegación

- Anterior: (inicio del bloque 28)
- Siguiente: [Quantum Machine Learning: kernels y barreras](02_quantum_machine_learning_kernels.md)
