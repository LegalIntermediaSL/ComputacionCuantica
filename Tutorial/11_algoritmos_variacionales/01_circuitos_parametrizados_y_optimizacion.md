# Circuitos parametrizados y optimización

## 1. Del circuito fijo al circuito flexible

Los algoritmos cuánticos estudiados hasta ahora (Deutsch-Jozsa, Grover, QFT) tienen una estructura fija: el circuito se diseña una vez y se ejecuta sin modificar sus parámetros. Un **circuito parametrizado** rompe este esquema introduciendo ángulos de rotación como variables continuas:

$$
U(\vec{\theta}) = \prod_k R_k(\theta_k)
$$

donde cada $R_k(\theta_k)$ es típicamente una puerta de rotación como $R_y(\theta) = e^{-i\theta Y/2}$ o $R_z(\theta) = e^{-i\theta Z/2}$. El vector $\vec{\theta} \in \mathbb{R}^d$ define una familia de estados cuánticos:

$$
|\psi(\vec{\theta})\rangle = U(\vec{\theta})|0\rangle^{\otimes n}
$$

Este circuito actúa como un **ansatz**: una plantilla parametrizable que se ajusta iterativamente para preparar el estado cuántico deseado.

## 2. La era NISQ y los circuitos superficiales

El contexto que hace necesarios los circuitos parametrizados es el hardware cuántico actual, conocido como **NISQ (Noisy Intermediate-Scale Quantum)**. Las máquinas disponibles hoy tienen entre decenas y miles de qubits, pero sufren de:

- Tiempos de coherencia limitados ($T_1, T_2$ del orden de microsegundos a milisegundos).
- Tasa de error por puerta de $10^{-3}$ a $10^{-2}$.
- Conectividad reducida entre qubits.

Ejecutar algoritmos como Shor en estas condiciones es inviable: requieren circuitos con miles de puertas CNOT y corrección de errores cuántica completa, que aún no está disponible.

Los circuitos parametrizados ofrecen una alternativa: son **poco profundos** (shallow), con decenas o cientos de puertas, lo que los hace compatibles con el hardware ruidoso actual. La expresividad se recupera mediante la optimización clásica de los parámetros.

## 3. El bucle híbrido cuántico-clásico

Los algoritmos variacionales siguen invariablemente este ciclo de optimización:

```
Inicializar θ₀ (clásico)
    │
    ▼
Preparar |ψ(θ)⟩ en QPU
    │
    ▼
Evaluar ⟨ψ(θ)|O|ψ(θ)⟩ (Estimator)
    │
    ▼
Calcular gradiente ∇_θ f(θ) (clásico)
    │
    ▼
Actualizar θ ← θ - η∇f(θ) (optimizador)
    │
    └── repetir hasta convergencia
```

El procesador cuántico evalúa el valor esperado del observable (una operación que escalaría exponencialmente en un ordenador clásico para estados muy entrelazados). El procesador clásico se encarga de la optimización, que sí puede realizarse eficientemente.

## 4. Gradiente de parámetros: la regla del cambio de parámetro

Para circuitos parametrizados con puertas de la forma $R(\theta) = e^{-i\theta P/2}$ (donde $P$ es un operador de Pauli), el gradiente del valor esperado se puede calcular exactamente con dos evaluaciones del circuito:

$$
\frac{\partial}{\partial \theta_k} \langle O \rangle_\theta = \frac{1}{2} \left[ \langle O \rangle_{\theta_k + \pi/2} - \langle O \rangle_{\theta_k - \pi/2} \right]
$$

Esta es la **regla del cambio de parámetro** (parameter-shift rule). A diferencia de las diferencias finitas, da el gradiente exacto con solo dos evaluaciones adicionales del circuito, sin introducir error de aproximación.

## 5. Implementación en Qiskit

```python
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp
import numpy as np
from scipy.optimize import minimize

# Ansatz parametrizado: capas de Ry y CNOT
def build_ansatz(n_qubits: int, depth: int) -> QuantumCircuit:
    params = ParameterVector('θ', n_qubits * depth)
    qc = QuantumCircuit(n_qubits)
    idx = 0
    for layer in range(depth):
        for q in range(n_qubits):
            qc.ry(params[idx], q)
            idx += 1
        for q in range(n_qubits - 1):
            qc.cx(q, q + 1)
    return qc

n = 2
ansatz = build_ansatz(n, depth=2)
observable = SparsePauliOp("ZZ")  # Medir ⟨Z⊗Z⟩

estimator = StatevectorEstimator()
params = np.random.uniform(-np.pi, np.pi, ansatz.num_parameters)

def cost_function(theta):
    bound_circuit = ansatz.assign_parameters(theta)
    job = estimator.run([(bound_circuit, observable)])
    return job.result()[0].data.evs

# Minimizar el valor esperado de ZZ
result = minimize(cost_function, params, method='COBYLA',
                  options={'maxiter': 500, 'rhobeg': 0.5})
print(f"Valor mínimo: {result.fun:.4f}")
print(f"Convergió: {result.success}")
```

## 6. Problemas de entrenamiento: barren plateaus

Un reto central de los circuitos parametrizados profundos es el fenómeno de los **barren plateaus** (mesetas áridas). Si el ansatz es demasiado expresivo (cubre uniformemente el espacio de Hilbert), el gradiente de la función de coste se vuelve exponencialmente pequeño:

$$
\text{Var}_\theta \left[ \frac{\partial f}{\partial \theta_k} \right] \in O\left(\frac{1}{2^n}\right)
$$

El optimizador clásico no puede orientarse en una superficie tan plana. Las estrategias para mitigarlo incluyen:

- **Ansatz estructurado** (QAOA, UCC): incorporar conocimiento del problema en la arquitectura.
- **Inicialización local**: comenzar con ángulos pequeños cerca de la identidad.
- **Layerwise training**: entrenar el circuito capa a capa.

## 7. Ideas clave

- Un circuito parametrizado define una familia de estados $|\psi(\vec{\theta})\rangle$ ajustable mediante un vector de parámetros $\vec{\theta}$.
- El hardware NISQ requiere circuitos superficiales; los circuitos parametrizados son la herramienta principal en esta era.
- El bucle híbrido cuántico-clásico combina evaluación cuántica de valores esperados con optimización clásica.
- La regla del cambio de parámetro calcula gradientes exactos con dos evaluaciones del circuito.
- Los barren plateaus son el obstáculo principal: gradientes exponencialmente pequeños en ansatz genéricos.

## 8. Ejercicios sugeridos

1. Implementar un ansatz de 3 qubits con profundidad 3 y optimizar el valor esperado de $X \otimes X \otimes X$.
2. Comparar la convergencia del optimizador COBYLA con SPSA para el mismo circuito en presencia de ruido simulado.
3. Calcular numéricamente el gradiente usando la regla del cambio de parámetro para el primer parámetro del ansatz y compararlo con diferencias finitas.
4. Investigar cómo varía la varianza del gradiente con el número de qubits para un ansatz aleatorio de profundidad fija.

## Navegacion

- Anterior: [Noise models y simulacion realista](../10_qiskit_avanzado/03_noise_models_y_simulacion_realista.md)
- Siguiente: [VQE: intuicion y fundamentos](02_vqe_intuicion.md)
