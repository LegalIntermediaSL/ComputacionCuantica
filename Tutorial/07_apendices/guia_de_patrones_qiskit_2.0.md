# Guía de Patrones Estándar en Qiskit 2.0 (Primitives V2)

Con la llegada de Qiskit 1.0+, el flujo de trabajo ha migrado de los antiguos `Backends` y `execute()` hacia un modelo basado en **Primitivas V2**. Esta guía resume los patrones que debes usar en este repositorio.

## 1. El Flujo de Trabajo Moderno

Cualquier experimento debe seguir estos 4 pasos:
1. **Construcción:** Crear el circuito con `QuantumCircuit`.
2. **Transpilación:** Adaptar el circuito al hardware/simulador con `transpile()`.
3. **Optimización:** (Opcional) Usar `PassManager` o ZX-Calculus.
4. **Ejecución:** Usar `SamplerV2` (para conteos) o `EstimatorV2` (para observables).

## 2. Patrón de SamplerV2 (Counts)

Si necesitas saber cuántas veces sale "00" o "11":
```python
from qiskit.primitives import SamplerV2
from qiskit_aer import AerSimulator

# 1. Preparar
sim = AerSimulator()
qc_transpiled = transpile(qc, sim)

# 2. Ejecutar
sampler = SamplerV2()
job = sampler.run([(qc_transpiled)])
result = job.result()[0] # Primer (y único) PUB
counts = result.data.meas.get_counts()
```

## 3. Patrón de EstimatorV2 (Observables)

Si necesitas el valor esperado de un operador (ej: Energía):
```python
from qiskit.primitives import EstimatorV2
from qiskit.quantum_info import SparsePauliOp

# 1. Definir Observable
obs = SparsePauliOp(["ZZ", "XX"])

# 2. Ejecutar
estimator = EstimatorV2()
job = estimator.run([(qc_transpiled, obs)])
ev = job.result()[0].data.evs
```

## 4. Mejores Prácticas
- **Usa siempre `SparsePauliOp`**: Es más eficiente que las matrices densas.
- **Evita `Aer.get_backend()`**: Utiliza directamente `AerSimulator()`.
- **Transpila siempre**: Incluso para simuladores ideales, la transpilación asegura que el circuito sea válido para la pila de ejecución V2.
