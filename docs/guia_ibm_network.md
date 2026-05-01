# Guía IBM Quantum Network — Tokens, Colas y Mitigación (2025)

Esta guía cubre la gestión segura de credenciales, selección dinámica de backends y buenas prácticas para ejecutar experimentos en IBM Quantum dentro del plan Open (10 min/mes).

---

## Credenciales: nunca hardcodear el token

### Variables de entorno (recomendado)

```bash
# ~/.zshrc o ~/.bashrc
export IBM_QUANTUM_TOKEN="tu_token_aqui"
```

```python
import os
from qiskit_ibm_runtime import QiskitRuntimeService

token = os.environ.get("IBM_QUANTUM_TOKEN")
if token is None:
    raise EnvironmentError("Define IBM_QUANTUM_TOKEN en tu entorno")

service = QiskitRuntimeService(channel="ibm_quantum", token=token)
```

### Guardar cuenta una sola vez (token cifrado en disco)

```python
# Solo la primera vez — guarda en ~/.qiskit/qiskit-ibm.json (cifrado)
QiskitRuntimeService.save_account(
    channel="ibm_quantum",
    token=os.environ["IBM_QUANTUM_TOKEN"],
    overwrite=True,
)

# Usos posteriores: sin token explícito
service = QiskitRuntimeService(channel="ibm_quantum")
```

### `.env` con python-dotenv (proyectos locales)

```bash
# .env  ← añadir a .gitignore
IBM_QUANTUM_TOKEN=tu_token_aqui
```

```python
from dotenv import load_dotenv
load_dotenv()
service = QiskitRuntimeService(channel="ibm_quantum",
                                token=os.environ["IBM_QUANTUM_TOKEN"])
```

---

## Selección dinámica del backend menos congestionado

### `least_busy` básico

```python
# Backend real menos ocupado con al menos 5 qubits
backend = service.least_busy(
    operational=True,
    simulator=False,
    min_num_qubits=5,
)
print(f"Backend seleccionado: {backend.name} ({backend.num_qubits} qubits)")
```

### Filtrar por familia de procesador

```python
# Solo backends Eagle/Heron (127+ qubits, heavy-hex)
backends_127 = service.backends(
    operational=True,
    simulator=False,
    min_num_qubits=127,
)
backend = min(backends_127, key=lambda b: b.status().pending_jobs)
print(f"Backend 127q menos ocupado: {backend.name}")
print(f"  Jobs en cola: {backend.status().pending_jobs}")
```

### Comparar varios backends

```python
candidates = service.backends(operational=True, simulator=False)
print(f"{'Backend':<30} {'Qubits':>6} {'Cola':>6} {'Estado'}")
print("-" * 60)
for b in sorted(candidates, key=lambda x: x.status().pending_jobs):
    st = b.status()
    print(f"{b.name:<30} {b.num_qubits:>6} {st.pending_jobs:>6}  {st.status_msg}")
```

---

## Estimación del tiempo de cola

```python
import datetime

backend = service.least_busy(operational=True, simulator=False)
status  = backend.status()

print(f"Backend:        {backend.name}")
print(f"Jobs en cola:   {status.pending_jobs}")

# Enviar trabajo y monitorizar posición
job = sampler.run([qc_t], shots=1024)
print(f"Job ID: {job.job_id()}")

# Polling de posición en cola
import time
while job.status().name not in ("DONE", "ERROR", "CANCELLED"):
    try:
        info = job.queue_info()
        pos  = job.queue_position()
        eta  = info.estimated_start_time if info else None
        print(f"  Posición en cola: {pos} | ETA: {eta}", end="\r")
    except Exception:
        pass
    time.sleep(15)

print(f"\nEstado final: {job.status().name}")
```

---

## Mitigación de errores con M3 (readout mitigation)

M3 corrige errores de lectura (*readout errors*) sin coste adicional de shots hardware.

### Con SamplerV2

```python
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_ibm_runtime.options import SamplerOptions

options = SamplerOptions()
options.dynamical_decoupling.enable = True   # suprime errores de decoherencia
options.twirling.enable_gates = True         # Pauli twirling en puertas 2Q

sampler = Sampler(mode=backend, options=options)
job = sampler.run([qc_t], shots=4096)
result = job.result()
counts = result[0].data.c.get_counts()
```

### Con EstimatorV2 (observables)

```python
from qiskit_ibm_runtime import EstimatorV2 as Estimator
from qiskit_ibm_runtime.options import EstimatorOptions

options = EstimatorOptions()
options.resilience_level = 1   # ZNE básico (extrapolación de ruido cero)
options.optimization_level = 3

estimator = Estimator(mode=backend, options=options)
job = estimator.run([(ansatz_t, hamiltonian, [theta_opt])])
E = float(job.result()[0].data.evs)
print(f"Energía con mitigación ZNE: {E:.6f} Ha")
```

### Niveles de resiliencia disponibles

| Nivel | Técnica | Overhead | Cuándo usar |
|-------|---------|----------|-------------|
| 0 | Sin mitigación | 1× | Benchmarking, circuitos muy cortos |
| 1 | DD + Twirling + ZNE básico | ~2× shots | **Recomendado para la mayoría de labs** |
| 2 | ZNE con amplificación de ruido | ~3-5× shots | Experimentos de precisión media |

---

## Límites del plan Open (2025)

| Recurso | Límite |
|---------|--------|
| Tiempo de CPU cuántica | **10 min / mes** |
| Trabajos simultáneos | 3 por cuenta |
| Shots por trabajo | Hasta 100 000 |
| Tiempo de sesión | 10 min por sesión |
| Qubits accesibles | Hasta 127 (Eagle, Heron) |
| Prioridad en cola | Estándar (detrás de Premium/Dedicated) |

### Estrategias para maximizar el uso del plan gratuito

1. **Optimizar en simulador primero** (`--simulator-only`) y enviar a hardware solo el experimento final.
2. **Warm-start**: usar los parámetros óptimos del simulador como punto de partida para reducir iteraciones en hardware.
3. **Circuitos cortos**: transpilación a nivel 3 (`optimization_level=3`) reduce profundidad ~40%.
4. **Batching**: agrupar varios trabajos en una sola sesión para compartir el overhead de inicialización.
5. **Shots justos**: 4096 shots es suficiente para la mayoría de los labs; 1024 para exploración.

```python
# Estimar coste antes de enviar
from qiskit import transpile

qc_t = transpile(qc, backend=backend, optimization_level=3)
n_2q = qc_t.num_nonlocal_gates()
depth = qc_t.depth()

# Tiempo estimado por shot en hardware IBM (aprox.)
t_shot_us = depth * 0.5 + n_2q * 0.3   # microsegundos (estimación empírica)
t_total_s = t_shot_us * shots * 1e-6

print(f"Profundidad:    {depth}")
print(f"Gates 2Q:       {n_2q}")
print(f"Tiempo est.:    {t_total_s:.2f} s  ({t_total_s/60:.3f} min del límite mensual)")
```

---

## Recuperar un trabajo anterior

```python
# Guardar job_id tras enviar
job = sampler.run([qc_t], shots=4096)
job_id = job.job_id()
print(f"Job ID guardado: {job_id}")

# En otra sesión: recuperar resultado
service = QiskitRuntimeService(channel="ibm_quantum")
old_job = service.job(job_id)

if old_job.status().name == "DONE":
    result = old_job.result()
    counts = result[0].data.c.get_counts()
    print(f"Resultado recuperado: {counts}")
else:
    print(f"Estado: {old_job.status().name}")
```

---

## Labs recomendados para hardware real

| Lab | Descripción | Qubits mínimos | Tiempo est. |
|-----|-------------|---------------|-------------|
| Lab 01 (Grover 2q) | Verificación de amplificación | 2 | < 5 s |
| Lab 05 (QFT 3q) | Estimación de fase | 3 | < 10 s |
| Lab 39 (VQE H₂ + ZNE) | Química cuántica con mitigación | 2 | ~30 s |
| `run_on_hardware.py` | VQE completo con warm-start | 2 | ~2 min |

---

*Para documentación completa: [docs.quantum.ibm.com](https://docs.quantum.ibm.com)*
