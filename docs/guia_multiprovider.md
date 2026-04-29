# Guía Multi-Provider — IonQ, Quantinuum y más allá de IBM

Esta guía documenta cómo ejecutar los laboratorios del curso en hardware cuántico de **IonQ**, **Quantinuum** y otros proveedores usando Qiskit y sus extensiones oficiales.

---

## Índice

1. [Ecosistema de proveedores 2025](#1-ecosistema)
2. [IonQ via Amazon Braket](#2-ionq-braket)
3. [Quantinuum via Azure Quantum](#3-quantinuum-azure)
4. [IonQ via Qiskit (directo)](#4-ionq-qiskit)
5. [Pasqal (átomos neutros) via Azure](#5-pasqal)
6. [Comparativa práctica: cuándo usar cada plataforma](#6-comparativa)
7. [Mitigación de errores multi-provider](#7-mitigacion)
8. [Ejemplo: VQE H₂ en IonQ Aria](#8-ejemplo-vqe)
9. [Costes y planes gratuitos 2025](#9-costes)

---

## 1. Ecosistema de proveedores 2025

```
┌─────────────────────────────────────────────────────────┐
│                   Tu código Qiskit                       │
└──────────┬──────────────────────┬───────────────────────┘
           │                      │
    ┌──────▼──────┐        ┌──────▼──────┐
    │  IBM Quantum │        │ Azure Quantum│
    │  (Heron r2) │        │  (Quantinuum │
    │  ibm_torino  │        │   H2-1, IQM) │
    └─────────────┘        └─────────────┘
           │
    ┌──────▼──────┐        ┌─────────────┐
    │Amazon Braket │        │  IonQ Cloud  │
    │(IonQ, Rigetti│        │  (directo)   │
    │ QuEra, OQC) │        └─────────────┘
    └─────────────┘
```

### Resumen de acceso

| Proveedor | Plataforma de acceso | Plan gratuito | Qiskit nativo |
|-----------|---------------------|---------------|---------------|
| IBM Quantum (Heron) | ibm_quantum directo | ✅ 10 min/mes | ✅ QiskitRuntimeService |
| IonQ (Aria, Forte) | Amazon Braket / IonQ Cloud | ❌ | ⚠️ via plugin |
| Quantinuum (H2-1) | Azure Quantum | ❌ (créditos) | ⚠️ via plugin |
| QuEra (Aquila) | Amazon Braket | ❌ | ⚠️ via plugin |
| Pasqal (Fresnel) | Azure Quantum | ❌ | ⚠️ via plugin |

---

## 2. IonQ via Amazon Braket

### Configuración

```bash
pip install amazon-braket-sdk qiskit-braket-provider
```

```python
from braket.aws import AwsDevice
from qiskit_braket_provider import BraketProvider

# Configurar credenciales AWS (en ~/.aws/credentials o variables de entorno)
# AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION

provider = BraketProvider()
backend = provider.get_backend("ionq_aria_1")

# Verificar disponibilidad
print(backend.status())
print(f"Qubits: {backend.num_qubits}")
print(f"Operaciones nativas: {backend.operation_names}")
```

### Circuito mínimo

```python
from qiskit import QuantumCircuit, transpile

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

# Transpilar a puertas nativas de IonQ (MS gate, GPi, GPi2)
qc_transpiled = transpile(qc, backend=backend, optimization_level=3)
print(f"Profundidad transpilada: {qc_transpiled.depth()}")
print(f"Puertas nativas: {qc_transpiled.count_ops()}")

# Ejecutar (requiere créditos AWS)
job = backend.run(qc_transpiled, shots=1024)
result = job.result()
counts = result.get_counts()
print(counts)
```

### Puertas nativas de IonQ (Aria)

| Puerta Qiskit | Puerta IonQ | Descripción |
|---------------|-------------|-------------|
| `rx(θ)`, `ry(θ)` | `GPi2(φ)` | Rotación de 1 qubit |
| `rz(θ)` | `virtual Z` | Rotación virtual (sin coste) |
| `cx` | `MS(φ₁, φ₂)` | Mølmer-Sørensen (all-to-all) |
| `h` | `GPi2 + virtual Z` | Hadamard compuesto |

**Ventaja clave de iones:** all-to-all connectivity — no hay SWAP overhead para qubits distantes.

---

## 3. Quantinuum via Azure Quantum

### Configuración

```bash
pip install azure-quantum qiskit-azure-quantum
```

```python
from azure.quantum import Workspace
from azure.quantum.qiskit import AzureQuantumProvider

workspace = Workspace(
    subscription_id="<tu-subscription>",
    resource_group="<tu-resource-group>",
    name="<tu-workspace>",
    location="eastus"
)

provider = AzureQuantumProvider(workspace)
backend = provider.get_backend("quantinuum.qpu.h2-1")

print(f"Qubits: {backend.num_qubits}")
print(f"Fidelidad 2Q típica: ~1×10⁻³ (la mejor disponible comercialmente)")
```

### Ejecución con emulador (gratis)

Quantinuum ofrece un **emulador** H1-1E/H2-1E que reproduce el ruido del hardware real sin coste adicional (dentro de los créditos de Azure):

```python
# Usar emulador H2-1E para pruebas gratuitas
backend_emulator = provider.get_backend("quantinuum.sim.h2-1e")

qc = QuantumCircuit(4)
qc.h(0)
for k in range(3):
    qc.cx(k, k+1)
qc.measure_all()

job = backend_emulator.run(qc, shots=100)  # 100 shots = bajo coste HQC
result = job.result()
print(result.get_counts())
```

### Sistema de créditos HQC (Quantinuum)

Quantinuum usa **H-Series Quantum Credits (HQC)**:

```
HQC = (n_shots × circuit_cost) / 5000
circuit_cost ≈ n_1Q_gates + 10 × n_2Q_gates
```

Ejemplo: VQE H₂ (50 términos Pauli, 10 parámetros, 100 shots/iter, 200 iter):
- HQC ≈ 200 × 100 × (30 + 10×10) / 5000 = **2600 HQC/sesión**
- Plan starter gratuito de Azure: 10,000 HQC

---

## 4. IonQ via Qiskit directo

IonQ ofrece acceso directo via su propia API sin necesidad de AWS:

```bash
pip install qiskit-ionq
```

```python
from qiskit_ionq import IonQProvider

# Token en https://cloud.ionq.com/settings/tokens
provider = IonQProvider(token="<tu-api-token>")

# Listar backends disponibles
for backend in provider.backends():
    print(backend.name(), backend.status())

backend = provider.get_backend("ionq_qpu.aria-1")

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

# Ejecutar en simulador IonQ primero (gratis)
sim = provider.get_backend("ionq_simulator")
job_sim = sim.run(qc, shots=1024)
print("Simulador:", job_sim.result().get_counts())

# En hardware real (requiere créditos)
job_hw = backend.run(qc, shots=100)
print("Hardware:", job_hw.result().get_counts())
```

### Noise model de IonQ para simulación local

```python
from qiskit_ionq import IonQProvider
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel

provider = IonQProvider(token="<token>")
ionq_backend = provider.get_backend("ionq_qpu.aria-1")

# Construir noise model de Aer a partir de las propiedades del backend
noise_model = NoiseModel.from_backend(ionq_backend)
local_sim = AerSimulator(noise_model=noise_model)

# Ahora simular localmente con ruido realista de IonQ
job = local_sim.run(qc, shots=1024)
print("Simulación con ruido IonQ:", job.result().get_counts())
```

---

## 5. Pasqal (átomos neutros) via Azure

```bash
pip install azure-quantum[pasqal]
```

```python
from azure.quantum.qiskit import AzureQuantumProvider

provider = AzureQuantumProvider(workspace)
backend_pasqal = provider.get_backend("pasqal.sim.emu-tn")  # emulador

# Nota: Pasqal usa Pulser nativo, no circuitos de puertas
# Para compatibilidad con Qiskit se usa la capa de traducción
# Los circuitos se limitan a profundidad baja y conectividad 2D
```

**Caso de uso de Pasqal:** simulación de modelos de Ising en geometría 2D arbitraria (aquila-style), optimización combinatoria con posicionamiento de átomos.

---

## 6. Comparativa práctica: cuándo usar cada plataforma

| Caso de uso | Recomendación | Razón |
|-------------|---------------|-------|
| Prototipado rápido / muchos shots | IBM Eagle/Heron | CLOPS ~15,000, plan gratuito |
| Alta fidelidad de puerta, bajo shot count | Quantinuum H2-1 | Menor error 2Q comercialmente disponible |
| All-to-all connectivity, n<40 | IonQ Forte | Sin SWAP overhead, T1~1s |
| Optimización combinatoria 2D | QuEra / Pasqal | Conectividad dinámica, n~100-256 |
| Desarrollo y debugging | Simuladores Aer / IonQ sim | Gratis, reproducible |

### Criterio de selección por tipo de circuito

```python
def recommend_backend(n_qubits, circuit_depth, n_shots, required_2q_fidelity):
    if required_2q_fidelity < 1e-3 and n_qubits <= 56:
        return "Quantinuum H2-1 (mejor fidelidad)"
    elif n_qubits <= 35 and circuit_depth < 50:
        return "IonQ Forte (all-to-all, alta coherencia)"
    elif n_shots > 10_000 and n_qubits <= 133:
        return "IBM Heron r2 (mayor throughput)"
    elif n_qubits > 100:
        return "QuEra Aquila o IBM (mayor escala)"
    else:
        return "IBM Eagle r3 (equilibrio coste/rendimiento)"
```

---

## 7. Mitigación de errores multi-provider

Todos los proveedores soportan **Zero-Noise Extrapolation (ZNE)** via Qiskit:

```python
from qiskit_ibm_runtime import EstimatorV2, Options

# En IBM: ZNE nativo via Qiskit Runtime
options = Options()
options.resilience_level = 2  # ZNE automático

# Para IonQ y Quantinuum: ZNE manual con folding
def fold_circuit(qc: QuantumCircuit, scale_factor: int) -> QuantumCircuit:
    """Amplifica el ruido aplicando gates y sus inversas scale_factor veces."""
    qc_folded = QuantumCircuit(*qc.qregs, *qc.cregs)
    for instruction in qc.data:
        qc_folded.append(instruction)
        for _ in range(scale_factor - 1):
            # Añadir pares Gate-Gate† para amplificar ruido
            qc_folded.append(instruction.operation.inverse(), instruction.qubits)
            qc_folded.append(instruction)
    return qc_folded


def zne_extrapolate(E_noisy: list, scale_factors: list) -> float:
    """Extrapolación Richardson a ruido cero."""
    from numpy.polynomial import polynomial as P
    coeffs = P.polyfit(scale_factors, E_noisy, deg=min(2, len(scale_factors)-1))
    return float(P.polyval(0, coeffs))
```

---

## 8. Ejemplo: VQE H₂ en IonQ Aria

```python
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import SparsePauliOp
from scipy.optimize import minimize

# Hamiltoniano H₂ en R=0.735 Å (STO-3G, JW mapping)
H2_op = SparsePauliOp.from_list([
    ('II', -1.0523732),
    ('ZI', 0.3979374),
    ('IZ', -0.3979374),
    ('ZZ', -0.0112802),
    ('XX', 0.1809270),
])

# Ansatz RY (compatible con puertas IonQ)
def h2_ansatz(n_params: int = 4) -> QuantumCircuit:
    params = ParameterVector('θ', n_params)
    qc = QuantumCircuit(2)
    qc.ry(params[0], 0)
    qc.ry(params[1], 1)
    qc.cx(0, 1)
    qc.ry(params[2], 0)
    qc.ry(params[3], 1)
    return qc


# En simulador local (sin créditos)
from qiskit.primitives import StatevectorEstimator
estimator = StatevectorEstimator()
qc = h2_ansatz()

energy_history = []
def cost(params):
    job = estimator.run([(qc, H2_op, [params])])
    E = float(job.result()[0].data.evs)
    energy_history.append(E)
    return E

import numpy as np
result = minimize(cost, np.zeros(4), method='COBYLA',
                  options={'maxiter': 300})

print(f"VQE H₂ local: E = {result.fun:.6f} Ha")
print(f"Referencia FCI: -1.137270 Ha")
print(f"Error: {abs(result.fun - (-1.137270)):.2e} Ha")

# Para ejecutar en IonQ real, reemplazar estimator:
# from qiskit_ionq import IonQProvider
# provider = IonQProvider(token="...")
# backend = provider.get_backend("ionq_qpu.aria-1")
# estimator = Estimator(backend=backend)
```

---

## 9. Costes y planes gratuitos 2025

### IBM Quantum (gratuito)

```
Plan Open (gratuito):
  - 10 minutos de tiempo de ejecución/mes en backends reales
  - Acceso a ibm_brisbane, ibm_kyiv, ibm_sherbrooke (Eagle r3, 127Q)
  - Sin acceso a Heron r2 (requiere plan pagado)
  - Simuladores ilimitados (AerSimulator local)

Plan Lite (gratuito con límites):
  - 20 minutos/mes en backends premium
  - Acceso prioritario a Heron r2

Registro: https://quantum.ibm.com
```

### IonQ Cloud

```
Plan Starter (gratuito con registro):
  - $300 USD en créditos iniciales (≈ 300 tareas en simulador)
  - Simulador ionq_simulator ilimitado (gratis)
  - Hardware: ~$0.00035/shot en Aria ($35 por 100,000 shots)

Registro: https://cloud.ionq.com
```

### Azure Quantum (Quantinuum)

```
Plan Free:
  - $200 USD en créditos de Azure para nuevas cuentas
  - Cuantinuum emulador H1-1E: ~1 HQC por circuito típico
  - Hardware H2-1: ~65 HQC por circuito típico

Registro: https://azure.microsoft.com/en-us/products/quantum
```

### Amazon Braket (IonQ, QuEra, Rigetti)

```
Plan gratuito:
  - $300 USD en créditos AWS para nuevas cuentas
  - IonQ simulador: gratis (SV1, TN1)
  - IonQ hardware: $0.01/task + $0.00035/shot (Aria)
  - QuEra Aquila: $0.01/task + $0.01/shot

Registro: https://aws.amazon.com/braket
```

---

*Última actualización: Abril 2026. Los planes y precios cambian frecuentemente — verificar las webs oficiales de cada proveedor.*
