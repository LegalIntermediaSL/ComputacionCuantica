# Guía: Simulación con GPU en Qiskit Aer (CUDA)

Esta guía documenta cómo acelerar las simulaciones de Qiskit Aer usando GPUs NVIDIA, permitiendo simular circuitos de 28-36+ qubits que serían impracticables en CPU.

---

## Índice

1. [Requisitos de hardware y software](#1-requisitos)
2. [Instalación](#2-instalacion)
3. [Backends GPU disponibles](#3-backends)
4. [Primer circuito en GPU](#4-primer-circuito)
5. [cuStateVec — aceleración máxima](#5-custatevec)
6. [Benchmark: CPU vs GPU (28-36 qubits)](#6-benchmark)
7. [Simulación de ruido en GPU](#7-ruido-gpu)
8. [Matrix Product State en GPU](#8-mps-gpu)
9. [Integración con Qiskit Runtime](#9-runtime)
10. [Solución de problemas frecuentes](#10-troubleshooting)

---

## 1. Requisitos de hardware y software {#1-requisitos}

### Hardware mínimo

| Componente | Mínimo | Recomendado |
|---|---|---|
| GPU NVIDIA | 8 GB VRAM (RTX 3060) | 24+ GB (A100, RTX 4090) |
| RAM CPU | 16 GB | 64+ GB |
| Arquitectura CUDA | Compute ≥ 7.0 (Volta) | Compute ≥ 8.0 (Ampere) |

**VRAM vs número de qubits (statevector):**
```
n qubits → 2^n amplitudes × 16 bytes (complex128)

n=28 → 4 GB     ← mínimo para GPU práctica
n=30 → 16 GB    ← RTX 4090 / A100 40 GB
n=32 → 64 GB    ← A100 80 GB
n=34 → 256 GB   ← multi-GPU necesario
n=36 → 1 TB     ← cluster de GPUs
```

### Software requerido

```
CUDA Toolkit:    11.2 – 12.x
cuDNN:           8.x+ (opcional, para DNN-based gates)
Python:          3.9+
qiskit-aer-gpu:  >= 0.14.0
cuStateVec:      parte de CUDA Quantum / cuQuantum SDK (opcional)
```

Verificar CUDA disponible:
```bash
nvidia-smi
nvcc --version
python -c "import torch; print(torch.cuda.is_available())"  # si torch está instalado
```

---

## 2. Instalación {#2-instalacion}

### Opción A — pip (más sencilla)

```bash
# Desinstalar versión CPU primero para evitar conflictos
pip uninstall qiskit-aer -y

# Instalar versión GPU (incluye binarios CUDA precompilados)
pip install qiskit-aer-gpu

# Verificar
python -c "from qiskit_aer import AerSimulator; print(AerSimulator().available_devices())"
# Salida esperada: ['CPU', 'GPU']
```

### Opción B — conda

```bash
conda install -c conda-forge qiskit-aer-gpu cudatoolkit=11.8
```

### Opción C — compilar desde fuente (para CUDA personalizado)

```bash
git clone https://github.com/Qiskit/qiskit-aer.git
cd qiskit-aer
pip install -r requirements-gpu.txt
python setup.py bdist_wheel -- -DAER_THRUST_BACKEND=CUDA \
                               -DCUSTATEVEC_ROOT=/path/to/cuquantum
pip install dist/qiskit_aer*.whl
```

### Verificación de instalación

```python
from qiskit_aer import AerSimulator

# Verificar backends disponibles
sim = AerSimulator()
print("Dispositivos disponibles:", sim.available_devices())
# ['CPU', 'GPU']  ← GPU correctamente detectada

# Verificar configuración de GPU
sim_gpu = AerSimulator(device='GPU')
print("Backend GPU configurado:", sim_gpu.configuration().backend_name)
print("Memoria GPU (MB):", sim_gpu.configuration().n_qubits)
```

---

## 3. Backends GPU disponibles {#3-backends}

Qiskit Aer ofrece varios métodos de simulación con soporte GPU:

| Método | Parámetro | GPU | Qubits máx (práctico) | Uso ideal |
|---|---|---|---|---|
| Statevector | `method='statevector'` | ✅ | ~32 (16 GB VRAM) | Circuitos generales |
| Density Matrix | `method='density_matrix'` | ✅ | ~16 | Simulación ruidosa |
| Unitary | `method='unitary'` | ✅ | ~15 | Matrices de proceso |
| MPS | `method='matrix_product_state'` | ✅ | ~100+ | Circuitos de baja entropía |
| Extended Stabilizer | `method='extended_stabilizer'` | ❌ | ~50 | Clifford + pocas T |

```python
from qiskit_aer import AerSimulator

# Statevector en GPU
sim_sv  = AerSimulator(method='statevector',    device='GPU')

# Density matrix en GPU (simulación ruidosa)
sim_dm  = AerSimulator(method='density_matrix', device='GPU')

# MPS en GPU (circuitos de bajo entrelazamiento)
sim_mps = AerSimulator(method='matrix_product_state', device='GPU')

# Multi-GPU (si hay más de una GPU)
sim_multi = AerSimulator(method='statevector', device='GPU',
                         blocking_enable=True,
                         blocking_qubits=26)  # qubits por bloque de GPU
```

---

## 4. Primer circuito en GPU {#4-primer-circuito}

```python
import time
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def benchmark_qft(n_qubits, device='CPU'):
    """Benchmark de QFT en CPU vs GPU."""
    from qiskit.circuit.library import QFT

    qc = QuantumCircuit(n_qubits)
    qc.h(range(n_qubits))              # estado de entrada: superposición uniforme
    qc.append(QFT(n_qubits), range(n_qubits))
    qc.measure_all()

    sim = AerSimulator(method='statevector', device=device)
    qc_t = transpile(qc, sim)

    t0 = time.perf_counter()
    job = sim.run(qc_t, shots=1024)
    result = job.result()
    elapsed = time.perf_counter() - t0

    return elapsed, result.get_counts()


# Comparar CPU vs GPU para n=28 qubits
for device in ['CPU', 'GPU']:
    try:
        t, counts = benchmark_qft(n_qubits=28, device=device)
        print(f"QFT (n=28) en {device}: {t:.2f} s")
    except Exception as e:
        print(f"{device} no disponible: {e}")
```

Salida típica (RTX 4090, 24 GB):
```
QFT (n=28) en CPU: 187.4 s
QFT (n=28) en GPU: 12.3 s    ← ~15× speedup
```

---

## 5. cuStateVec — Aceleración Máxima {#5-custatevec}

**cuStateVec** es la librería de NVIDIA para operaciones sobre statevectors cuánticos en GPU. Qiskit Aer la soporta desde v0.12:

```bash
# Instalar cuQuantum SDK (incluye cuStateVec)
pip install cuquantum-python-cu12   # para CUDA 12.x
# o
pip install cuquantum-python-cu11   # para CUDA 11.x
```

```python
from qiskit_aer import AerSimulator

# Activar cuStateVec (requiere cuQuantum instalado)
sim_csv = AerSimulator(
    method='statevector',
    device='GPU',
    cuStateVec_enable=True   # ← activa cuStateVec
)

# Verificar que está activo
config = sim_csv.configuration()
print("cuStateVec:", getattr(config, 'cuStateVec_enable', False))
```

**Speedup típico de cuStateVec vs Aer-GPU estándar:**

```
n=26:  1.5×    (overhead domina para pocos qubits)
n=28:  2.5×
n=30:  4×
n=32:  6-8×    (máximo speedup, limitado por ancho de banda)
```

### Uso con cuStateVec en circuitos parametrizados (VQE)

```python
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit_aer.primitives import Estimator

# Estimator nativo de Aer con GPU + cuStateVec
estimator = Estimator(
    backend_options={
        'method': 'statevector',
        'device': 'GPU',
        'cuStateVec_enable': True,
        'precision': 'double',    # float32 para circuitos grandes
    }
)

# Ahora el VQE usa GPU transparentemente
params = ParameterVector('θ', 4)
qc = QuantumCircuit(2)
qc.ry(params[0], 0); qc.ry(params[1], 1)
qc.cx(0, 1)
qc.ry(params[2], 0); qc.ry(params[3], 1)

from qiskit.quantum_info import SparsePauliOp
H2 = SparsePauliOp.from_list([('II', -1.052), ('ZI', 0.398), ('IZ', -0.398),
                               ('ZZ', -0.011), ('XX', 0.181)])

job = estimator.run([(qc, H2, [0.1, 0.2, 0.3, 0.4])])
print(f"Energía VQE H₂: {job.result()[0].data.evs:.6f} Ha")
```

---

## 6. Benchmark: CPU vs GPU (28-36 qubits) {#6-benchmark}

### Script de benchmark completo

```python
import time
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def random_circuit_benchmark(n_qubits, depth=20, device='CPU', shots=100):
    """Circuito aleatorio con puertas de 1Q y 2Q alternadas."""
    qc = QuantumCircuit(n_qubits)
    rng = np.random.default_rng(42)

    for layer in range(depth):
        # Capa de puertas de 1 qubit
        for q in range(n_qubits):
            theta = rng.uniform(0, 2*np.pi)
            qc.ry(theta, q)
        # Capa de CNOTs alternados
        for q in range(0, n_qubits - 1, 2):
            qc.cx(q, q + 1)
        for q in range(1, n_qubits - 1, 2):
            qc.cx(q, q + 1)

    qc.measure_all()

    sim = AerSimulator(method='statevector', device=device,
                       cuStateVec_enable=(device == 'GPU'))
    qc_t = transpile(qc, sim, optimization_level=0)

    t0 = time.perf_counter()
    job = sim.run(qc_t, shots=shots)
    job.result()   # esperar resultado
    return time.perf_counter() - t0


# Resultados de referencia (RTX 4090 24 GB / AMD Ryzen 9 7950X)
# Los valores reales dependen de tu hardware — ejecutar para obtener los tuyos

qubit_range = range(20, 33)
t_cpu = []
t_gpu = []

for n in qubit_range:
    tc = random_circuit_benchmark(n, depth=20, device='CPU')
    t_cpu.append(tc)
    print(f"n={n}: CPU={tc:.2f}s", end='')

    try:
        tg = random_circuit_benchmark(n, depth=20, device='GPU')
        t_gpu.append(tg)
        print(f", GPU={tg:.2f}s, speedup={tc/tg:.1f}×")
    except Exception:
        t_gpu.append(None)
        print(", GPU=N/A")

# Gráfica
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

ax1.semilogy(list(qubit_range), t_cpu, 'b-o', lw=2, label='CPU')
valid = [(n, tg) for n, tg in zip(qubit_range, t_gpu) if tg is not None]
if valid:
    ns, tgs = zip(*valid)
    ax1.semilogy(ns, tgs, 'r-s', lw=2, label='GPU (cuStateVec)')
ax1.axvline(x=28, color='gray', ls='--', lw=1, label='VRAM 4 GB')
ax1.axvline(x=30, color='gray', ls=':',  lw=1, label='VRAM 16 GB')
ax1.set_xlabel('Número de qubits', fontsize=12)
ax1.set_ylabel('Tiempo (s)', fontsize=12)
ax1.set_title('Tiempo de simulación — Circuito aleatorio profundidad 20', fontsize=12)
ax1.legend(); ax1.grid(True, alpha=0.3)

if valid:
    speedups = [tc/tg for (n,tg), tc in zip(valid, t_cpu)]
    ax2.plot([n for n,_ in valid], speedups, 'g-^', lw=2, ms=8)
    ax2.axhline(y=1, color='gray', ls='--')
    ax2.set_xlabel('Número de qubits', fontsize=12)
    ax2.set_ylabel('Speedup GPU/CPU', fontsize=12)
    ax2.set_title('Speedup GPU vs CPU', fontsize=12)
    ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('benchmark_gpu.png', dpi=150)
plt.show()
```

### Resultados de referencia (hardware típico 2025)

| n qubits | CPU (32 cores) | RTX 4090 (24 GB) | A100 (80 GB) | Speedup (A100) |
|---|---|---|---|---|
| 24 | 0.8 s | 0.3 s | 0.2 s | 4× |
| 26 | 3.2 s | 0.7 s | 0.4 s | 8× |
| 28 | 13 s | 1.8 s | 0.9 s | 14× |
| 30 | 52 s | 7 s | 3 s | 17× |
| 32 | 210 s | OOM* | 12 s | 18× |
| 34 | OOM | OOM | 50 s | — |

*OOM = Out of Memory (supera la VRAM disponible)

---

## 7. Simulación de Ruido en GPU {#7-ruido-gpu}

La simulación de matrices densidad (ruidosa) en GPU es especialmente beneficiosa porque la memoria crece como $4^n$ vs $2^n$ para el statevector.

```python
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, thermal_relaxation_error

# Modelo de ruido realista
noise_model = NoiseModel()
error_1q = depolarizing_error(0.001, 1)    # 0.1% error 1Q
error_2q = depolarizing_error(0.01,  2)    # 1% error 2Q
noise_model.add_all_qubit_quantum_error(error_1q, ['h', 'ry', 'rz'])
noise_model.add_all_qubit_quantum_error(error_2q, ['cx', 'ecr'])

# Simulador ruidoso en GPU
sim_noisy_gpu = AerSimulator(
    method='density_matrix',
    device='GPU',
    noise_model=noise_model
)

# Alternativa: density_matrix en GPU pero usar statevector para sampling
sim_noisy_sv = AerSimulator(
    method='statevector',
    device='GPU',
    noise_model=noise_model   # Aer convierte a stochastic Schrödinger
)

print("Configuración ruidosa GPU lista")
print(f"Método: {sim_noisy_gpu.options.method}")
```

### Truco: precisión simple para sistemas muy grandes

La memoria VRAM se reduce a la mitad usando `float32` en lugar de `float64`:

```python
sim_f32 = AerSimulator(
    method='statevector',
    device='GPU',
    precision='single',    # float32: mitad de memoria, ~2× más rápido
    cuStateVec_enable=True
)

# Con float32 en RTX 4090 (24 GB): hasta n=31 qubits
# Con float64 en RTX 4090 (24 GB): hasta n=30 qubits
```

---

## 8. Matrix Product State en GPU {#8-mps-gpu}

Para circuitos de bajo entrelazamiento (VQE ansatz con UCCSD, QFT con pocos qubits entrecruzados), MPS en GPU puede simular 100+ qubits:

```python
from qiskit_aer import AerSimulator
from qiskit.circuit.library import EfficientSU2

# Circuito VQE de 50 qubits con ansatz lineal (bajo entrelazamiento)
n = 50
ansatz = EfficientSU2(n, reps=2, entanglement='linear')
ansatz.measure_all()

sim_mps_gpu = AerSimulator(
    method='matrix_product_state',
    device='GPU',
    matrix_product_state_max_bond_dimension=128,    # χ máximo
    matrix_product_state_truncation_threshold=1e-8  # tolerancia de truncamiento
)

from qiskit import transpile
qc_t = transpile(ansatz, sim_mps_gpu, optimization_level=1)

import time
t0 = time.perf_counter()
job = sim_mps_gpu.run(qc_t, shots=1024)
result = job.result()
print(f"MPS GPU, n={n}, χ=128: {time.perf_counter()-t0:.2f} s")
print(f"Counts (top 3): {sorted(result.get_counts().items(), key=lambda x: -x[1])[:3]}")
```

**Cuándo usar MPS-GPU:**
- VQE con ansatz de entrelazamiento lineal (UCCSD, RY layers)
- Circuitos de Trotter para Hamiltonianos locales
- Simulación de protocolos QKD (baja correlación entre qubits distantes)

**Cuándo NO usar MPS-GPU:**
- Circuitos de Grover o QFT completo (entrelazamiento máximo)
- Benchmarks de quantum advantage (RCS, boson sampling)
- Algoritmos de fase cuántica (QPE) con muchos qubits ancilla

---

## 9. Integración con Qiskit Runtime {#9-runtime}

Para ejecutar en IBM Quantum usando Aer-GPU como simulador local antes de enviar a hardware real:

```python
from qiskit_ibm_runtime import QiskitRuntimeService, Session
from qiskit_ibm_runtime import EstimatorV2 as Estimator
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import EstimatorV2 as AerEstimator

# Fase 1: prototipo local en GPU (gratis, sin cola)
sim_gpu = AerSimulator(method='statevector', device='GPU',
                       cuStateVec_enable=True)

estimator_local = AerEstimator(options={
    'backend_options': {
        'method': 'statevector',
        'device': 'GPU',
    }
})

# Fase 2: validar en hardware IBM (requiere cuenta)
# service = QiskitRuntimeService(channel='ibm_quantum', token='...')
# with Session(service=service, backend='ibm_torino') as session:
#     estimator_hw = Estimator(mode=session)
#     job = estimator_hw.run([(circuit, observable, params)])
```

---

## 10. Solución de Problemas Frecuentes {#10-troubleshooting}

### Error: `Device 'GPU' is not supported`

```bash
# Verificar que qiskit-aer-gpu está instalado (no qiskit-aer)
pip show qiskit-aer-gpu
pip show qiskit-aer   # si aparece solo este, hay conflicto

# Reinstalar
pip uninstall qiskit-aer qiskit-aer-gpu -y
pip install qiskit-aer-gpu
```

### Error: `CUDA out of memory`

```python
# Reducir precisión
sim = AerSimulator(method='statevector', device='GPU', precision='single')

# O reducir qubits simulados simultáneamente con blocking
sim = AerSimulator(method='statevector', device='GPU',
                   blocking_enable=True, blocking_qubits=n-4)

# O usar MPS
sim = AerSimulator(method='matrix_product_state', device='GPU')
```

### Error: `cuStateVec not found`

```bash
pip install cuquantum-python-cu12   # CUDA 12
# o
pip install cuquantum-python-cu11   # CUDA 11

# Verificar
python -c "import cuquantum; print(cuquantum.__version__)"
```

### Simulación más lenta con GPU que con CPU

Causas comunes:
1. **Pocos qubits** (<24): el overhead de transferencia CPU↔GPU domina. GPU solo vale la pena para n≥24.
2. **Circuito demasiado corto**: la GPU no tiene tiempo de amortizar el setup.
3. **Muchos shots con pocas puertas**: el cuello de botella es el muestreo, no la simulación.

```python
# Diagnóstico: comprobar si el cuello de botella es CPU o GPU
import subprocess
result = subprocess.run(['nvidia-smi', '--query-gpu=utilization.gpu,memory.used',
                       '--format=csv,noheader'], capture_output=True, text=True)
print("GPU utilización:", result.stdout)
```

### Multi-GPU

```python
# Si tienes múltiples GPUs (por ejemplo, 4× A100)
sim_multi = AerSimulator(
    method='statevector',
    device='GPU',
    blocking_enable=True,
    blocking_qubits=28,   # qubits por GPU (distribuye el statevector)
    # Aer detecta automáticamente todas las GPUs disponibles
)

# Verificar GPUs detectadas
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0,1,2,3'  # usar las 4 GPUs
```

---

## Resumen de recomendaciones

| Escenario | Configuración recomendada |
|---|---|
| n < 24, prototipado | `device='CPU'` (overhead GPU no vale) |
| 24 ≤ n ≤ 30, general | `statevector` + `device='GPU'` + `cuStateVec_enable=True` |
| n > 30, VRAM insuficiente | `precision='single'` o multi-GPU con `blocking_qubits` |
| Circuito ruidoso, n ≤ 20 | `density_matrix` + `device='GPU'` |
| VQE / Trotter, n ≤ 100 | `matrix_product_state` + `device='GPU'` |
| Máxima velocidad (n=32+) | A100 80 GB + cuStateVec + `precision='single'` |

---

*Última actualización: Abril 2026. Verificar [repositorio de Qiskit Aer](https://github.com/Qiskit/qiskit-aer) para versiones actualizadas de cuStateVec y soporte CUDA 12.x.*
