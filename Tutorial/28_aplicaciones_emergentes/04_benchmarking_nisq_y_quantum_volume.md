# Benchmarking NISQ: Quantum Volume, CLOPS y Mirror Circuits

## 1. El problema de medir rendimiento cuántico

Comparar procesadores cuánticos no es trivial. El número de qubits es una métrica engañosa: un chip de 50 qubits de alta fidelidad supera a uno de 1000 qubits con alta tasa de error. Se necesitan métricas que integren qubits, conectividad, fidelidad de puertas y tiempo de coherencia en una sola cifra.

Las tres métricas más adoptadas en la era NISQ son:

| Métrica | Creador | Qué mide |
|---|---|---|
| Quantum Volume (QV) | IBM (2018) | Profundidad efectiva de circuitos aleatorios |
| CLOPS | IBM (2021) | Velocidad de ejecución de circuitos parametrizados |
| Mirror Circuits | Sandia (2022) | Fidelidad de circuitos de profundidad variable |

---

## 2. Quantum Volume

### 2.1 Definición

El Quantum Volume $V_Q = 2^n$ donde $n$ es el mayor número de qubits tal que un procesador puede ejecutar correctamente circuitos cuadrados aleatorios de $n$ qubits y $n$ capas, distinguiéndolos del ruido con al menos un 67% de éxito (umbral $2/3$).

**Circuito de QV:** para $n$ qubits y $d = n$ capas:
1. Permutación aleatoria de qubits.
2. Capa de puertas SU(4) aleatorias en pares de qubits.
3. Medición en la base computacional.

El objetivo es que la distribución de salida del hardware sea indistinguible del resultado ideal simulado clásicamente.

### 2.2 Criterio de éxito

Para una instancia del circuito de QV con $m$ muestras, el heavy output probability (HOP) es:
$$
\hat{h} = \frac{|\{x : p_{\text{ideal}}(x) > \text{mediana}\} \cap \text{salidas observadas}|}{m}
$$

Se acepta que el procesador pasa el test si $\hat{h} > 2/3$ con confianza estadística $> 97.5\%$.

### 2.3 Cálculo con Qiskit

```python
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import random_unitary, Statevector
from qiskit_aer import AerSimulator
import numpy as np

def qv_circuit(n: int, seed: int = 0) -> QuantumCircuit:
    """Genera un circuito de Quantum Volume de n qubits."""
    rng = np.random.default_rng(seed)
    qc = QuantumCircuit(n)
    for _ in range(n):  # n capas
        perm = rng.permutation(n)
        for k in range(n // 2):
            i, j = int(perm[2*k]), int(perm[2*k+1])
            U = random_unitary(4, seed=rng.integers(0, 10000)).data
            qc.unitary(U, [i, j])
    return qc

n = 4
qc = qv_circuit(n, seed=42)

# Distribución ideal
sv = Statevector.from_instruction(qc)
probs_ideal = sv.probabilities()
median_prob = np.median(probs_ideal)
heavy_outputs = set(np.where(probs_ideal > median_prob)[0])

# Simulación ruidosa
sim_noisy = AerSimulator(noise_model=None)  # reemplazar con NoiseModel real
qc_m = qc.copy(); qc_m.measure_all()
result = sim_noisy.run(qc_m, shots=2000).result()
counts = result.get_counts()
total = sum(counts.values())

hop = sum(counts.get(format(s, f"0{n}b"), 0) for s in heavy_outputs) / total
print(f"Heavy Output Probability (HOP): {hop:.4f}")
print(f"Pasa QV-{2**n}: {hop > 2/3}")
```

### 2.4 Evolución del QV en IBM

| Año | Procesador | QV |
|---|---|---|
| 2019 | IBM Q 5 | 8 |
| 2020 | Falcon r4 | 32 |
| 2021 | Falcon r5.11 | 128 |
| 2022 | Eagle r3 | 512 |
| 2023 | Heron r1 | 25000 (estimado) |

Quantinuum H1-1 alcanzó QV = 32768 en 2023 gracias a las altísimas fidelidades de los iones atrapados.

---

## 3. CLOPS: Circuit Layer Operations Per Second

### 3.1 Definición

CLOPS mide la **velocidad de ejecución** de circuitos parametrizados, relevante para algoritmos variacionales (VQE, QAOA) donde se ejecutan miles de instancias del mismo circuito con distintos parámetros.

$$
\text{CLOPS} = \frac{M \cdot K \cdot S \cdot D}{T}
$$

donde:
- $M$: número de actualizaciones de parámetros
- $K$: número de circuitos por actualización
- $S$: shots por circuito
- $D$: capas de puertas del circuito de referencia (QV con $n=100$)
- $T$: tiempo total de ejecución

### 3.2 Valores representativos (2023-2024)

| Procesador | CLOPS |
|---|---|
| IBM Eagle (2022) | ~2800 |
| IBM Heron (2024) | ~5000 |
| Quantinuum H2 | ~200 (lento por iones, pero alta fidelidad) |

---

## 4. Mirror Circuits

### 4.1 Principio

Los mirror circuits permiten estimar la fidelidad de circuitos de profundidad arbitraria sin necesidad de comparar con un simulador clásico (lo que escala exponencialmente).

El circuito espejo de $\mathcal{C}$ es:
$$
\mathcal{C}_{\text{mirror}} = \mathcal{C}^{\dagger} \cdot P \cdot \mathcal{C}
$$

donde $P$ es una capa de Pauli aleatorios. El resultado debería ser determinista (el estado final se puede calcular eficientemente). La fidelidad se estima comparando salidas observadas con salidas esperadas.

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import random_clifford, Statevector
import numpy as np

def mirror_circuit(n: int, depth: int, seed: int = 0) -> QuantumCircuit:
    """Circuito espejo de Clifford de n qubits y profundidad depth."""
    rng = np.random.default_rng(seed)
    qc = QuantumCircuit(n)
    layers = []
    for _ in range(depth):
        cliff = random_clifford(n, seed=int(rng.integers(0, 10000)))
        qc.append(cliff.to_instruction(), range(n))
        layers.append(cliff)
    # Capa de Pauli aleatorio
    for q in range(n):
        pauli = rng.choice(["id", "x", "y", "z"])
        getattr(qc, pauli)(q) if pauli != "id" else None
    # Inverso del circuito
    for cliff in reversed(layers):
        qc.append(cliff.adjoint().to_instruction(), range(n))
    return qc

qc_mirror = mirror_circuit(n=3, depth=5, seed=0)
sv = Statevector.from_instruction(qc_mirror)
print("Estado final (debe ser determinista):", sv.probabilities().round(3))
```

### 4.2 Ventaja sobre QV

| Aspecto | Quantum Volume | Mirror Circuits |
|---|---|---|
| Profundidad máxima testeable | Limitada por simulación clásica | Ilimitada |
| Overhead de shots | Moderado | Bajo |
| Verificación | Comparación con simulador | Autocontenida |
| Sensibilidad a errores | Alta | Alta |

---

## 5. Supremacía cuántica vs. ventaja cuántica práctica

### 5.1 Supremacía cuántica (2019-2023)

**Google Sycamore (2019):** circuito de muestreo aleatorio cuántico (RCS) de 53 qubits, 20 ciclos. Google afirmó que el mejor algoritmo clásico conocido tardaría 10.000 años. IBM rebatió en semanas usando técnicas de compresión tensorial.

**Problema:** las tareas de "supremacía" (RCS, Boson Sampling) no tienen aplicación práctica directa. Son difíciles de verificar clásicamente, pero tampoco sirven para resolver problemas útiles.

### 5.2 Ventaja cuántica práctica: estado en 2024

| Tarea | Mejor resultado cuántico | Estado actual |
|---|---|---|
| Simulación de Ising 2D | IBM Eagle 127q (2023) | Ventaja estrecha con técnicas de mitigación |
| Optimización combinatoria | QAOA p=1-3 | Aún por debajo de heurísticas clásicas |
| QML (clasificación) | Variational classifiers | Sin ventaja demostrada con datos clásicos |
| Química (FeMoco) | VQE parcial | Reqiere corrección de errores completa |
| Factorización (Shor) | RSA-48 (demo) | Sin amenaza práctica para RSA-2048 |

### 5.3 Google Willow (2024)

En diciembre 2024, Google anunció Willow: 105 qubits superconductores con tasa de error por debajo del umbral de corrección de errores en el código de superficie. Logros:

- Error lógico que **decrece** al aumentar el tamaño del código (por primera vez debajo del umbral en hardware real).
- Circuito de RCS que requeriría $10^{25}$ años en el mejor supercomputador clásico actual.
- Primera demostración experimental de escalado subcrítico de errores.

---

## 6. Métricas emergentes (2024-2025)

**Algorithmic Qubit (AQ):** propuesto por Quantinuum, mide el mayor número de qubits en los que se puede ejecutar correctamente un algoritmo de referencia (Bernstein-Vazirani escalado).

**Layer Fidelity:** fidelidad promedio por capa de puertas, descomponiendo circuitos largos en capas individuales medibles.

**EPLG (Error Per Layered Gate):** error promedio por puerta en capas paralelas, más informativo que el error de puerta individual.

---

## 7. Resumen

La evaluación del rendimiento cuántico ha madurado de métricas simples (número de qubits, T1) a benchmarks integrales. El Quantum Volume captura la interacción entre fidelidad, conectividad y profundidad; CLOPS mide la utilidad práctica para algoritmos variacionales; los mirror circuits permiten testear circuitos más profundos de lo que es simulable clásicamente. La brecha entre "supremacía" técnica y ventaja cuántica práctica sigue siendo el reto central de la era NISQ.

---

*← [03 Ventaja cuántica demostrada](03_ventaja_cuantica_demostrada.md) | [05 Perspectivas y hoja de ruta →](05_perspectivas_y_hoja_de_ruta.md)*
