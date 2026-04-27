# Guía IBM Quantum — Plan Gratuito (2025)

Esta guía explica cómo ejecutar circuitos de este repositorio en hardware cuántico real de IBM usando el plan gratuito de IBM Quantum.

## Acceso

1. Registrarse en [quantum.ibm.com](https://quantum.ibm.com) (cuenta gratuita).
2. Obtener el API token en **Account settings → API Token → Copy**.
3. Instalar las dependencias:

```bash
pip install qiskit-ibm-runtime
```

## Configuración del token

```python
from qiskit_ibm_runtime import QiskitRuntimeService

# Primera vez: guardar token permanentemente
QiskitRuntimeService.save_account(
    channel="ibm_quantum",
    token="TU_TOKEN_AQUÍ",
    overwrite=True,
)

# Uso posterior
service = QiskitRuntimeService(channel="ibm_quantum")
```

## Backends disponibles (plan gratuito)

El plan gratuito da acceso a backends de hasta 127 qubits con tiempo de cola variable.

```python
service = QiskitRuntimeService(channel="ibm_quantum")

# Listar backends disponibles
backends = service.backends(operational=True, simulator=False)
for b in backends:
    print(f"{b.name:30s} | qubits: {b.num_qubits:3d} | status: {b.status().status_msg}")

# Elegir el menos ocupado
from qiskit_ibm_runtime import least_busy
backend = service.least_busy(operational=True, simulator=False)
print(f"Backend seleccionado: {backend.name}")
```

## Ejecutar un circuito básico

```python
from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import SamplerV2 as Sampler

# Circuito Bell
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# Transpilar para el backend
qc_t = transpile(qc, backend=backend, optimization_level=3)
print(f"Profundidad transpilada: {qc_t.depth()}")
print(f"Gates de 2Q:             {qc_t.num_nonlocal_gates()}")

# Enviar trabajo
sampler = Sampler(mode=backend)
job = sampler.run([qc_t], shots=4096)
print(f"Job ID: {job.job_id()}")
print("Esperando resultado...")

result = job.result()
counts = result[0].data.c.get_counts()
print(f"Distribución: {counts}")
```

## Ejecutar VQE H₂ en hardware real

Ver el script completo en [`run_on_hardware.py`](../run_on_hardware.py).

```python
from qiskit_ibm_runtime import EstimatorV2 as Estimator, Session

with Session(backend=backend) as session:
    estimator = Estimator(mode=session)
    # ... configurar VQE con estimator.run(...)
```

## Buenas prácticas

### Gestión de colas

```python
# Monitorizar estado del trabajo
from qiskit_ibm_runtime import RuntimeJobStatus

job = sampler.run([qc_t])
status = job.status()

if status == RuntimeJobStatus.QUEUED:
    print(f"Posición en cola: {job.queue_position()}")
    print(f"Tiempo estimado: {job.queue_info().estimated_start_time}")
```

### Guardar y recuperar resultados

```python
import json

# Guardar job_id para recuperar después
job_id = job.job_id()
with open('last_job.txt', 'w') as f:
    f.write(job_id)

# Recuperar trabajo anterior
retrieved_job = service.job(job_id)
if retrieved_job.status() == RuntimeJobStatus.DONE:
    result = retrieved_job.result()
```

### Mitigación de errores (M3)

```python
from qiskit_ibm_runtime import EstimatorV2 as Estimator
from qiskit_ibm_runtime.options import EstimatorOptions

options = EstimatorOptions()
options.resilience_level = 1  # ZNE básico
options.optimization_level = 3

estimator = Estimator(mode=backend, options=options)
```

## Límites del plan gratuito (2025)

| Recurso | Límite gratuito |
|---------|----------------|
| Tiempo de computación mensual | 10 min / mes |
| Número de trabajos | Sin límite (dentro del tiempo) |
| Shots por trabajo | Hasta 100,000 |
| Qubits accesibles | Hasta 127 (Eagle/Heron) |
| Prioridad en cola | Estándar (detrás de premium) |
| Session time | 10 min por sesión |

## Backends recomendados para este curso

| Backend | Qubits | Conectividad | Uso recomendado |
|---------|--------|--------------|-----------------|
| ibm_brisbane | 127 | Heavy-hex | Labs 38-44, QFT |
| ibm_kyiv | 127 | Heavy-hex | VQE, QAOA |
| ibm_sherbrooke | 127 | Heavy-hex | Algoritmos de error correction |

## Solución de problemas frecuentes

**Error: `IBMAccountError: No IBM Quantum account found`**
```python
QiskitRuntimeService.save_account(channel="ibm_quantum", token="...", overwrite=True)
```

**Error de transpilación incompatible**
```python
# Asegurarse de usar basis_gates del backend específico
from qiskit.transpiler import PassManager
qc_t = transpile(qc, backend=backend, basis_gates=backend.basis_gates)
```

**Job en QUEUED por mucho tiempo**
```python
# Cancelar y elegir backend menos ocupado
job.cancel()
backend = service.least_busy(operational=True, simulator=False, min_num_qubits=5)
```

---

*Para documentación completa: [docs.quantum.ibm.com](https://docs.quantum.ibm.com)*
