# Quantum Machine Learning: kernels cuánticos y barreras

## 1. El paisaje del QML

El **Quantum Machine Learning** (QML) es uno de los campos más prometedores y, a la vez, más susceptibles al hype del área cuántica. La promesa es que los circuitos cuánticos pueden representar características de datos de alta dimensión de forma ineficiente para un computador clásico, ofreciendo una ventaja en tareas de aprendizaje.

Sin embargo, los resultados teóricos de los últimos años han establecido límites importantes: la ventaja cuántica en ML no está garantizada para todos los problemas, y los llamados **barren plateaus** (mesetas áridas) son un obstáculo fundamental en muchos enfoques.

## 2. Kernels cuánticos

### 2.1 El método del kernel en ML clásico

En el aprendizaje automático clásico (SVM, regresión de kernel), el truco del kernel permite clasificar datos no lineales sin calcular explícitamente el mapa de características $\phi(x)$. Solo se necesita la función de kernel:

$$
k(x, x') = \langle \phi(x), \phi(x') \rangle
$$

Para datos cuánticos, la idea es usar un circuito cuántico $U(x)$ como mapa de características, codificando el dato clásico $x$ en un estado cuántico $|x\rangle = U(x)|0\rangle$.

### 2.2 El kernel cuántico

El **kernel cuántico** entre dos datos $x$ y $x'$ se define como el solapamiento de sus estados cuánticos:

$$
k(x, x') = |\langle 0|U^\dagger(x') U(x)|0\rangle|^2
$$

En la práctica, se estima midiendo la probabilidad de medir $|0\rangle$ en el circuito $U^\dagger(x') U(x)$.

### 2.3 Circuitos de codificación de datos

**ZZ Feature Map** (Havlíček et al., 2019): codifica cada característica $x_i$ en la fase de rotaciones de un qubit, y cruza las características con términos ZZ:

$$
U(x) = \prod_{l=1}^{d} U_\phi(x) H^{\otimes n}
$$

donde $U_\phi(x) = \exp\left(i \sum_{j \in [n]} x_j Z_j + \sum_{jk \in S} (\pi - x_j)(\pi - x_k) Z_j Z_k\right)$.

```python
from qiskit.circuit.library import ZZFeatureMap
from qiskit.quantum_info import Statevector
import numpy as np

n_features = 2
n_reps = 2

feature_map = ZZFeatureMap(feature_dimension=n_features, reps=n_reps)
print(f"ZZFeatureMap: {feature_map.num_qubits} qubits, {feature_map.num_parameters} params")
print(feature_map.decompose().draw())

# Calcular el kernel cuántico entre dos puntos
x1 = np.array([0.5, 1.2])
x2 = np.array([0.8, 0.3])

qc_x1 = feature_map.assign_parameters(x1)
qc_x2 = feature_map.assign_parameters(x2)

sv1 = Statevector.from_instruction(qc_x1)
sv2 = Statevector.from_instruction(qc_x2)

kernel_val = abs(sv1.inner(sv2))**2
print(f"\nk(x1, x2) = |⟨x2|x1⟩|² = {kernel_val:.4f}")
```

### 2.4 Quantum Kernel Estimation (QKE)

Para $m$ datos de entrenamiento, se necesita calcular $O(m^2)$ entradas del kernel. Cada entrada requiere ejecutar el circuito $U^\dagger(x') U(x)$ con $O(1/\epsilon^2)$ shots para precisión $\epsilon$.

Esto ya es un bottleneck: para $m = 1000$ datos y $\epsilon = 0.01$, se necesitan $\sim 10^{10}$ shots, lo que es impracticable en hardware actual.

```python
from qiskit.primitives import StatevectorSampler
import numpy as np

def quantum_kernel_matrix(feature_map, X_data: np.ndarray) -> np.ndarray:
    """Calcula la matriz de Gram del kernel cuántico (simulación exacta)."""
    m = len(X_data)
    K = np.zeros((m, m))

    for i in range(m):
        for j in range(i, m):
            qc_xi = feature_map.assign_parameters(X_data[i])
            qc_xj = feature_map.assign_parameters(X_data[j])
            sv_i  = Statevector.from_instruction(qc_xi)
            sv_j  = Statevector.from_instruction(qc_xj)
            K[i, j] = abs(sv_i.inner(sv_j))**2
            K[j, i] = K[i, j]

    return K

# Dataset de prueba: XOR
X_train = np.array([[0.1, 0.1], [0.1, 0.9], [0.9, 0.1], [0.9, 0.9]])
y_train = np.array([-1, 1, 1, -1])

K = quantum_kernel_matrix(feature_map, X_train)
print("Matriz de Gram K:")
print(np.round(K, 3))
```

## 3. Redes neuronales cuánticas (QNN)

### 3.1 Parametrized Quantum Circuits como modelos

Un **circuit cuántico parametrizado** (PQC) puede verse como un modelo de aprendizaje: los parámetros $\vec{\theta}$ son los pesos, los datos de entrada $x$ se codifican en el circuito, y el valor esperado de un observable es la predicción.

$$
f(\vec{\theta}, x) = \langle 0 | U^\dagger(x, \vec{\theta}) O U(x, \vec{\theta}) | 0 \rangle
$$

El entrenamiento minimiza la función de pérdida:

$$
\mathcal{L}(\vec{\theta}) = \frac{1}{m}\sum_{i=1}^m \ell(f(\vec{\theta}, x_i), y_i)
$$

con gradientes calculados por la **regla del cambio de parámetro** (parameter-shift rule).

### 3.2 Implementación con Qiskit

```python
from qiskit import QuantumCircuit
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp
from scipy.optimize import minimize
import numpy as np

def build_qnn(n_qubits: int, n_reps: int):
    """QNN = ZZ feature map + RealAmplitudes ansatz."""
    feature_map = ZZFeatureMap(n_qubits, reps=1)
    ansatz = RealAmplitudes(n_qubits, reps=n_reps)
    qc = QuantumCircuit(n_qubits)
    qc.compose(feature_map, inplace=True)
    qc.compose(ansatz, inplace=True)
    return qc, feature_map.parameters, ansatz.parameters

n_qubits = 2
qc, data_params, weight_params = build_qnn(n_qubits, n_reps=2)
print(f"QNN: {qc.num_qubits} qubits, {len(data_params)} data params, {len(weight_params)} weights")

# Observable: Z en el primer qubit (clasificación binaria)
observable = SparsePauliOp.from_list([("IZ", 1.0)])
estimator = StatevectorEstimator()

# Datos: XOR en [0, π]
X_train = np.array([[0.1, 0.1], [0.1, 2.8], [2.8, 0.1], [2.8, 2.8]]) * np.pi / 3
y_train = np.array([-1, 1, 1, -1])

def predict(x: np.ndarray, weights: np.ndarray) -> float:
    params = dict(zip(list(data_params) + list(weight_params),
                      list(x) + list(weights)))
    bound = qc.assign_parameters(params)
    result = estimator.run([(bound, observable)]).result()
    return float(result[0].data.evs)

def loss(weights: np.ndarray) -> float:
    preds = np.array([predict(x, weights) for x in X_train])
    return float(np.mean((preds - y_train)**2))

np.random.seed(42)
w0 = np.random.uniform(-np.pi, np.pi, len(weight_params))
result = minimize(loss, w0, method="COBYLA", options={"maxiter": 200})
print(f"Loss final: {result.fun:.4f}")
```

## 4. Barren Plateaus: el obstáculo fundamental

### 4.1 El problema

Los **barren plateaus** (McClear et al., 2018) son el mayor obstáculo teórico para el QML. El fenómeno: para circuitos cuánticos aleatorios profundos, el gradiente de la función de pérdida se concentra exponencialmente cerca de cero en casi todos los puntos del espacio de parámetros.

**Resultado formal:** para un ansatz 2-design de $n$ qubits y profundidad $L$:

$$
\text{Var}\left[\frac{\partial \mathcal{L}}{\partial \theta_k}\right] \leq \frac{1}{b^n}
$$

donde $b$ es un entero que depende de la arquitectura. Los gradientes se hacen exponencialmente pequeños con el número de qubits, haciendo que el entrenamiento sea exponencialmente difícil.

### 4.2 Causas

1. **Profundidad del circuito:** circuitos más profundos forman 2-designs, produciendo barren plateaus globales.
2. **Entrelazamiento global:** demasiado entrelazamiento entre qubits produce estados "demasiado mezclados" localmente, anulando los gradientes.
3. **Funciones de pérdida globales:** medir un observable que actúa sobre todos los qubits (vs. uno que actúa solo sobre un subconjunto).

### 4.3 Estrategias para mitigar barren plateaus

- **Localización de la función de pérdida:** usar observables que actúen sobre pocos qubits (~1-2) en lugar de observables globales.
- **Inicialización estructurada:** inicializar los parámetros cercanos a un valor conocido (identidad) en lugar de aleatoriamente.
- **Entrenamiento por capas:** entrenar el circuito capa por capa, comenzando desde las capas más cercanas a la salida.
- **MERA y ansätze geométricamente locales:** diseñar ansätze que eviten el entrelazamiento de largo alcance.

### 4.4 ¿Tiene el QML ventaja cuántica real?

La pregunta es abierta. Resultados recientes (Huang et al., 2022) muestran que:
- Los kernels cuánticos tienen ventaja **si y solo si** el problema es duro para algoritmos clásicos en términos del kernel.
- Para la mayoría de datasets de ML del mundo real (imágenes, texto, tabular), los kernels clásicos (RBF, polinomial) son iguales o mejores en la práctica actual.
- La ventaja cuántica en ML requiere datos que tengan estructura cuántica natural (distribuciones de estados cuánticos, salidas de otros circuitos cuánticos).

## 5. Ideas clave

- Los kernels cuánticos codifican datos en estados cuánticos y miden su solapamiento; son el enfoque más fundamentado teóricamente para QML.
- Las QNN son PQCs entrenados con gradientes (parameter-shift), pero sufren de barren plateaus en circuitos profundos.
- Los barren plateaus hacen que los gradientes se anulen exponencialmente con el número de qubits: este es el mayor obstáculo práctico del QML.
- La ventaja cuántica en ML requiere datos con estructura cuántica intrínseca; para datos clásicos convencionales, los algoritmos cuánticos no tienen ventaja demostrada.
- Las estrategias de mitigación (localización de observables, inicialización estructurada, entrenamiento por capas) pueden aliviar pero no eliminar los barren plateaus.

## 6. Ejercicios sugeridos

1. Calcular la matriz de Gram del kernel cuántico para el dataset XOR con 4 puntos y verificar que el SVM cuántico lo clasifica correctamente.
2. Simular la aparición de barren plateaus: medir la varianza del gradiente de una QNN aleatoria en función del número de qubits (2, 4, 6, 8) y verificar la escala exponencial.
3. Comparar la fidelidad de clasificación de un kernel cuántico (ZZ Feature Map) con la de un kernel RBF clásico en el dataset breast cancer de sklearn.
4. Implementar la estrategia de "localización de la pérdida" y comparar la varianza del gradiente frente a una función de pérdida global.

## Navegación

- Anterior: [Mitigación de errores cuánticos: ZNE y PEC](01_error_mitigation_zne_pec.md)
- Siguiente: [Ventaja cuántica demostrada: experimentos reales](03_ventaja_cuantica_demostrada.md)
