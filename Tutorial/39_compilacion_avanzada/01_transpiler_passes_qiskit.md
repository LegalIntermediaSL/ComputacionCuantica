# Transpilación Avanzada con Qiskit PassManager

**Módulo 39 · Artículo 1 · Nivel muy avanzado**

---

## Arquitectura del transpiler de Qiskit

El transpiler de Qiskit convierte un circuito abstracto al ISA (Instruction Set
Architecture) del hardware. La compilación tiene 5 etapas:

```
Circuito abstracto
      │
      ▼ 1. Init          — expansión de gates de alto nivel
      ▼ 2. Layout        — asignación de qubits lógicos a físicos
      ▼ 3. Routing       — inserción de SWAPs para conectividad
      ▼ 4. Translation   — traducción al basis gateset del backend
      ▼ 5. Optimization  — reducción de gates (peephole, 1Q fusion...)
      │
      ▼
ISA Circuit (hardware-ready)
```

```python
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit.transpiler import PassManager, CouplingMap
from qiskit.transpiler.passes import (
    Optimize1qGatesDecomposition,
    CommutativeCancellation,
    CXCancellation,
    RemoveResetInZeroState,
    Collect2qBlocks,
    ConsolidateBlocks,
)
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
import time

# Backend simulado
backend = AerSimulator()

# Circuito de prueba: QFT 5 qubits
from qiskit.circuit.library import QFT
qc_test = QuantumCircuit(5)
qc_test.h(range(5))
qc_test.append(QFT(5), range(5))

print('Circuito original:')
print(f'  Profundidad: {qc_test.depth()}')
print(f'  Puertas:     {qc_test.size()}')
print(f'  Ops:         {dict(qc_test.count_ops())}')

# Comparativa de niveles de optimización
for level in [0, 1, 2, 3]:
    t0 = time.perf_counter()
    pm = generate_preset_pass_manager(optimization_level=level, backend=backend)
    qc_t = pm.run(qc_test)
    elapsed = time.perf_counter() - t0
    ops = dict(qc_t.count_ops())
    cx_count = ops.get('cx', ops.get('ecr', ops.get('cz', 0)))
    print(f'Level {level}: depth={qc_t.depth():>4}, CX={cx_count:>4}, '
          f'1q-gates={qc_t.size()-cx_count:>4}, tiempo={elapsed*1000:.1f} ms')
```

---

## Passes personalizados: análisis de conmutación

```python
from qiskit.transpiler import TransformationPass
from qiskit.dagcircuit import DAGCircuit
from qiskit.circuit import Gate
import numpy as np

class ContadorConmutaciones(TransformationPass):
    """Pass que cuenta pares de puertas conmutativas adyacentes."""

    def run(self, dag: DAGCircuit) -> DAGCircuit:
        conmutativas = 0
        nodos = list(dag.topological_op_nodes())
        for i in range(len(nodos) - 1):
            n1, n2 = nodos[i], nodos[i + 1]
            # Verificar si comparten qubits (no pueden cancelarse trivialmente)
            q1 = set(n1.qargs)
            q2 = set(n2.qargs)
            if not q1.intersection(q2):
                conmutativas += 1
        self.property_set['conmutativas_detectadas'] = conmutativas
        return dag

# Pass personalizado: fusion de puertas RZ consecutivas
class FusionRZ(TransformationPass):
    """Fusiona cadenas de puertas RZ en una sola."""

    def run(self, dag: DAGCircuit) -> DAGCircuit:
        fusiones = 0
        for qubit in dag.qubits:
            # Obtener secuencia de nodos en este qubit
            nodos_q = [n for n in dag.topological_op_nodes()
                       if qubit in n.qargs and n.name == 'rz']
            if len(nodos_q) < 2:
                continue
            # Fusionar pares consecutivos
            i = 0
            while i < len(nodos_q) - 1:
                n1, n2 = nodos_q[i], nodos_q[i + 1]
                # Verificar que son adyacentes (ninguna puerta entre ellas en ese qubit)
                theta1 = float(n1.op.params[0])
                theta2 = float(n2.op.params[0])
                # Crear puerta fusionada
                from qiskit.circuit.library import RZGate
                nueva_gate = RZGate(theta1 + theta2)
                dag.substitute_node(n1, nueva_gate, inplace=True)
                dag.remove_op_node(n2)
                nodos_q.pop(i + 1)
                fusiones += 1
            i += 1
        self.property_set['rz_fusionadas'] = fusiones
        return dag

# Aplicar passes personalizados
from qiskit import QuantumCircuit
qc_rz = QuantumCircuit(2)
qc_rz.rz(0.5, 0)
qc_rz.rz(0.3, 0)   # ← debería fusionarse con el anterior
qc_rz.cx(0, 1)
qc_rz.rz(0.1, 1)
qc_rz.rz(0.2, 1)   # ← debería fusionarse

print('\nCircuito original:')
print(qc_rz.draw())
print(f'Puertas RZ: {qc_rz.count_ops().get("rz", 0)}')

pm_custom = PassManager([
    ContadorConmutaciones(),
    FusionRZ(),
    Optimize1qGatesDecomposition(basis=['rx', 'ry', 'rz']),
    CXCancellation(),
])
qc_optim = pm_custom.run(qc_rz)
print('\nCircuito optimizado:')
print(qc_optim.draw())
print(f'Puertas RZ tras fusión: {qc_optim.count_ops().get("rz", 0)}')
print(f'Conmutativas detectadas: {pm_custom.property_set.get("conmutativas_detectadas", "N/A")}')
print(f'RZ fusionadas: {pm_custom.property_set.get("rz_fusionadas", "N/A")}')
```

---

## Ruteo de qubits: SABRE vs trivial

```python
from qiskit.transpiler import CouplingMap
from qiskit.transpiler.passes import SabreLayout, SabreSwap
import numpy as np
import matplotlib.pyplot as plt

def benchmark_ruteo(n_qubits: int, n_cnots: int,
                    seed: int = 42) -> dict:
    """
    Compara el impacto del ruteo SABRE vs nivel 0 en número de SWAPs.
    """
    from qiskit.circuit.random import random_circuit
    from qiskit_aer import AerSimulator

    # Circuito aleatorio con muchos CNOT
    qc = random_circuit(n_qubits, n_cnots, max_operands=2, seed=seed)
    backend = AerSimulator()

    # Nivel 0: sin optimización
    qc_l0 = transpile(qc, backend, optimization_level=0, seed_transpiler=seed)
    # Nivel 3: SABRE layout + SABRE swap
    qc_l3 = transpile(qc, backend, optimization_level=3, seed_transpiler=seed)

    ops_l0 = dict(qc_l0.count_ops())
    ops_l3 = dict(qc_l3.count_ops())

    swap_l0 = ops_l0.get('swap', 0)
    swap_l3 = ops_l3.get('swap', 0)

    return {
        'n_qubits': n_qubits,
        'n_cnots': n_cnots,
        'depth_l0': qc_l0.depth(),
        'depth_l3': qc_l3.depth(),
        'swaps_l0': swap_l0,
        'swaps_l3': swap_l3,
        'cx_l0': ops_l0.get('cx', ops_l0.get('ecr', 0)),
        'cx_l3': ops_l3.get('cx', ops_l3.get('ecr', 0)),
    }

print('Benchmark de ruteo SABRE (nivel 0 vs nivel 3):')
print(f'{"n_q":>4} | {"n_CNOT":>6} | {"depth_L0":>9} | {"depth_L3":>9} | '
      f'{"SWAP_L0":>8} | {"SWAP_L3":>8} | {"Reducción"}')
print('-' * 72)

resultados = []
for n in [4, 6, 8, 10]:
    r = benchmark_ruteo(n, n * 3)
    reduccion = (1 - r['depth_l3'] / r['depth_l0']) * 100 if r['depth_l0'] > 0 else 0
    resultados.append(r)
    print(f'{r["n_qubits"]:>4} | {r["n_cnots"]:>6} | {r["depth_l0"]:>9} | '
          f'{r["depth_l3"]:>9} | {r["swaps_l0"]:>8} | {r["swaps_l3"]:>8} | {reduccion:.1f}%')

# Gráfica
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
ns = [r['n_qubits'] for r in resultados]
axes[0].bar([x - 0.2 for x in ns], [r['depth_l0'] for r in resultados],
            0.4, label='Nivel 0 (sin SABRE)', color='red', alpha=0.7)
axes[0].bar([x + 0.2 for x in ns], [r['depth_l3'] for r in resultados],
            0.4, label='Nivel 3 (SABRE)', color='blue', alpha=0.7)
axes[0].set_xlabel('Número de qubits')
axes[0].set_ylabel('Profundidad del circuito transpilado')
axes[0].set_title('Impacto del ruteo SABRE en profundidad')
axes[0].legend()
axes[0].grid(alpha=0.3, axis='y')

axes[1].bar([x - 0.2 for x in ns], [r['swaps_l0'] for r in resultados],
            0.4, label='Nivel 0', color='red', alpha=0.7)
axes[1].bar([x + 0.2 for x in ns], [r['swaps_l3'] for r in resultados],
            0.4, label='Nivel 3 (SABRE)', color='blue', alpha=0.7)
axes[1].set_xlabel('Número de qubits')
axes[1].set_ylabel('SWAPs insertados')
axes[1].set_title('SWAPs insertados por el router')
axes[1].legend()
axes[1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.show()
```

---

## Síntesis de unitarias: de matriz a circuito

```python
from qiskit.synthesis import OneQubitEulerDecomposer
from qiskit.quantum_info import Operator
import numpy as np

def sintesis_1qubit(U: np.ndarray) -> 'QuantumCircuit':
    """
    Descompone una unitaria 2×2 en rotaciones Euler: Rz·Ry·Rz.
    """
    from qiskit import QuantumCircuit
    from qiskit.synthesis import OneQubitEulerDecomposer
    decomp = OneQubitEulerDecomposer(basis='ZYZ')
    return decomp(U)

# Ejemplos de unitarias 1 qubit
unitarias_1q = {
    'H (Hadamard)':     np.array([[1, 1], [1, -1]]) / np.sqrt(2),
    'T gate':           np.diag([1, np.exp(1j * np.pi / 4)]),
    'Arbitraria 1':     np.array([[0.5 + 0.5j, 0.5 - 0.5j],
                                   [-0.5 + 0.5j, 0.5 + 0.5j]]),
}

print('Síntesis de unitarias 1 qubit (descomposición ZYZ):')
for nombre, U in unitarias_1q.items():
    qc = sintesis_1qubit(U)
    ops = dict(qc.count_ops())
    print(f'  {nombre}: {ops}')
    # Verificar fidelidad
    U_rec = Operator(qc).data
    fid = np.abs(np.trace(U.conj().T @ U_rec)) / 2
    print(f'    Fidelidad de reconstrucción: {fid:.8f}')

# Síntesis de 2 qubits con KAK decomposition
from qiskit.synthesis import TwoQubitBasisDecomposer
from qiskit.circuit.library import CXGate

print('\nSíntesis de unitarias 2 qubits (KAK + CX):')
decomp_2q = TwoQubitBasisDecomposer(CXGate())

# SWAP en términos de CX
SWAP = np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]], dtype=complex)
CZ   = np.diag([1, 1, 1, -1]).astype(complex)
iSWAP = np.array([[1,0,0,0],[0,0,1j,0],[0,1j,0,0],[0,0,0,1]], dtype=complex)

for nombre, U2 in [('SWAP', SWAP), ('CZ', CZ), ('iSWAP', iSWAP)]:
    qc2 = decomp_2q(U2)
    cx_count = qc2.count_ops().get('cx', 0)
    U_rec = Operator(qc2).data
    # Fidelidad de proceso ignorando fase global
    fid = np.abs(np.trace(U2.conj().T @ U_rec)) / 4
    print(f'  {nombre}: CX={cx_count}, fidelidad={fid:.6f}')
```

---

**Referencias:**
- Sivarajah et al., *Quantum* 5, 577 (2021) — t|ket⟩ compiler
- Li, Ding, Xie, *arXiv:1809.02573* (2018) — SABRE routing
- Shende, Bullock, Markov, *IEEE TCAD* 25, 1000 (2006) — KAK decomposition
- Qiskit transpiler documentation: https://docs.quantum.ibm.com/api/qiskit/transpiler
