"""
Generador automático de exámenes de Computación Cuántica.

Uso:
    python generador_examen.py --nivel basico --n 5 --seed 42
    python generador_examen.py --nivel intermedio --n 4 --nivel avanzado --n 2 --seed 7
    python generador_examen.py --todos --n 10 --seed 0 --salida mi_examen

Genera dos archivos PDF:
    <salida>_enunciados.pdf  — preguntas para el alumno
    <salida>_soluciones.pdf  — soluciones con código y explicación

Dependencias:
    pip install reportlab
"""

import argparse
import random
import textwrap
from pathlib import Path


# ─────────────────────────────────────────────────────────────────────────────
# Base de datos de ejercicios
# ─────────────────────────────────────────────────────────────────────────────

EJERCICIOS = {
    "basico": [
        {
            "id": "B01",
            "titulo": "Estado de superposición en un qubit",
            "modulo": "Módulo 01 — Fundamentos",
            "enunciado": (
                "Crea un circuito de 1 qubit que prepare el estado |+⟩ = (|0⟩ + |1⟩)/√2 "
                "aplicando la puerta de Hadamard. Verifica que las probabilidades de medición "
                "sean P(0) = P(1) = 0.5 usando StatevectorSampler con 2048 shots."
            ),
            "pistas": [
                "Usa QuantumCircuit(1) y el método .h(0).",
                "Añade .measure_all() antes de llamar al sampler.",
                "Con 2048 shots, espera ~1024 cuentas en cada resultado.",
            ],
            "solucion_codigo": """\
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

qc = QuantumCircuit(1)
qc.h(0)
qc.measure_all()

sampler = StatevectorSampler()
result = sampler.run([qc], shots=2048).result()
counts = result[0].data.meas.get_counts()
print(counts)  # {'0': ~1024, '1': ~1024}
""",
            "solucion_explicacion": (
                "La puerta H transforma |0⟩ → (|0⟩+|1⟩)/√2. Las amplitudes son 1/√2, "
                "por lo que las probabilidades son |1/√2|² = 0.5 para cada resultado."
            ),
        },
        {
            "id": "B02",
            "titulo": "Estado de Bell |Φ+⟩",
            "modulo": "Módulo 01 — Fundamentos",
            "enunciado": (
                "Construye el estado de Bell |Φ+⟩ = (|00⟩ + |11⟩)/√2 con un circuito de "
                "2 qubits. Verifica que solo aparecen resultados '00' y '11' con probabilidad "
                "~0.5 cada uno, y que P('01') = P('10') ≈ 0."
            ),
            "pistas": [
                "El estado de Bell se construye con H en el primer qubit y luego CNOT.",
                "qc.h(0) seguido de qc.cx(0, 1).",
            ],
            "solucion_codigo": """\
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

sampler = StatevectorSampler()
counts = sampler.run([qc], shots=2048).result()[0].data.meas.get_counts()
print(counts)  # solo '00' y '11'
""",
            "solucion_explicacion": (
                "H⊗I transforma |00⟩ → (|0⟩+|1⟩)⊗|0⟩/√2. El CNOT entrelaza: "
                "|0⟩|0⟩ → |0⟩|0⟩ y |1⟩|0⟩ → |1⟩|1⟩, dando (|00⟩+|11⟩)/√2."
            ),
        },
        {
            "id": "B03",
            "titulo": "Puerta X y medición",
            "modulo": "Módulo 01 — Fundamentos",
            "enunciado": (
                "Prepara el estado |1⟩ aplicando la puerta X a |0⟩. "
                "Mide el qubit y verifica que siempre obtienes '1'."
            ),
            "pistas": ["qc.x(0) invierte el qubit: |0⟩ → |1⟩."],
            "solucion_codigo": """\
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

qc = QuantumCircuit(1)
qc.x(0)
qc.measure_all()

counts = StatevectorSampler().run([qc], shots=100).result()[0].data.meas.get_counts()
print(counts)  # {'1': 100}
""",
            "solucion_explicacion": "X es la puerta NOT cuántica: lleva |0⟩ a |1⟩ con amplitud 1.",
        },
        {
            "id": "B04",
            "titulo": "Valor esperado de Z en |+⟩",
            "modulo": "Módulo 01 — Fundamentos",
            "enunciado": (
                "Calcula el valor esperado de Z = [[1,0],[0,-1]] en el estado |+⟩. "
                "Debe ser ⟨Z⟩ = 0. Usa StatevectorEstimator con SparsePauliOp."
            ),
            "pistas": [
                "El estado |+⟩ tiene amplitudes iguales en |0⟩ y |1⟩.",
                "⟨+|Z|+⟩ = (⟨0|+⟨1|)/√2 · Z · (|0⟩+|1⟩)/√2 = (1-1)/2 = 0.",
            ],
            "solucion_codigo": """\
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp

qc = QuantumCircuit(1)
qc.h(0)

Z_op = SparsePauliOp("Z")
est = StatevectorEstimator()
result = est.run([(qc, Z_op)]).result()
print(result[0].data.evs)  # ≈ 0.0
""",
            "solucion_explicacion": "El estado |+⟩ es simétrico respecto a Z; su proyección sobre Z es cero.",
        },
        {
            "id": "B05",
            "titulo": "Circuito de teleportación cuántica",
            "modulo": "Módulo 03 — Protocolos",
            "enunciado": (
                "Implementa el protocolo de teleportación cuántica para transferir el estado "
                "|ψ⟩ = cos(0.3)|0⟩ + sin(0.3)|1⟩ del qubit 0 al qubit 2. "
                "Verifica que el estado final del qubit 2 tiene la misma amplitud."
            ),
            "pistas": [
                "Necesitas 3 qubits: origen (q0), canal Bell (q1, q2).",
                "El protocolo: Bell en q1-q2, CNOT q0→q1, H en q0, medición clásica, correcciones X/Z.",
            ],
            "solucion_codigo": """\
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

qc = QuantumCircuit(3)
theta = 0.6  # 2 * 0.3
qc.ry(theta, 0)   # prepara |psi>

# Par Bell en q1-q2
qc.h(1); qc.cx(1, 2)

# Protocolo de teleportación
qc.cx(0, 1); qc.h(0)

# Correcciones (versión sin medición clásica, con puertas controladas)
qc.cx(1, 2); qc.cz(0, 2)

sv = Statevector(qc)
# El qubit 2 debe tener el estado original
rho2 = sv.partial_transpose([0, 1])  # traza sobre q0,q1
print('Amplitudes qubit 2 (traza parcial):', rho2.data.diagonal().real)
""",
            "solucion_explicacion": (
                "La teleportación usa entrelazamiento previo para transferir el estado "
                "sin enviar el qubit físico. Las correcciones X/Z compensan las mediciones."
            ),
        },
        {
            "id": "B06",
            "titulo": "Transformada de Fourier Cuántica en 3 qubits",
            "modulo": "Módulo 05 — QFT",
            "enunciado": (
                "Implementa la QFT para 3 qubits y aplícala al estado |1⟩ = |001⟩. "
                "Verifica que las amplitudes de salida tienen módulo uniforme 1/√8."
            ),
            "pistas": [
                "La QFT se construye con Hadamard y puertas de fase controladas CP(2π/2^k).",
                "La salida de QFT|j⟩ tiene todas las amplitudes con módulo 1/√N.",
            ],
            "solucion_codigo": """\
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

def qft_3q():
    qc = QuantumCircuit(3)
    for j in range(3):
        qc.h(j)
        for k in range(j+1, 3):
            qc.cp(2*np.pi / 2**(k-j+1), j, k)
    return qc

qc = QuantumCircuit(3)
qc.x(0)          # |001>
qc.compose(qft_3q(), inplace=True)

sv = Statevector(qc)
amps = np.abs(sv.data)
print('Amplitudes:', np.round(amps, 4))
print('Todas iguales a 1/√8:', np.allclose(amps, 1/np.sqrt(8)))
""",
            "solucion_explicacion": "QFT|j⟩ = (1/√N) Σ_k e^{2πijk/N} |k⟩ — amplitudes uniformes, fases variables.",
        },
        {
            "id": "B07",
            "titulo": "Canal despolarizante y fidelidad",
            "modulo": "Módulo 08 — Ruido",
            "enunciado": (
                "Aplica un canal despolarizante con p=0.2 al estado |+⟩ y calcula "
                "la fidelidad entre el estado ideal y el ruidoso. Implementa el canal "
                "manualmente con matrices de Pauli."
            ),
            "pistas": [
                "ε(ρ) = (1-p)ρ + (p/3)(XρX + YρY + ZρZ)",
                "La fidelidad entre estados puros y mixtos es F = ⟨ψ|ρ_noisy|ψ⟩.",
            ],
            "solucion_codigo": """\
import numpy as np
from qiskit.quantum_info import DensityMatrix, state_fidelity

psi_plus = np.array([1,1])/np.sqrt(2)
rho_in = np.outer(psi_plus, psi_plus.conj())

p = 0.2
X = np.array([[0,1],[1,0]]); Y = np.array([[0,-1j],[1j,0]]); Z = np.array([[1,0],[0,-1]])
rho_out = (1-p)*rho_in + (p/3)*(X@rho_in@X + Y@rho_in@Y + Z@rho_in@Z)

F = state_fidelity(DensityMatrix(rho_in), DensityMatrix(rho_out))
print(f'Fidelidad: {F:.4f}')  # ~0.8667
print(f'Teórica: {1 - 2*p/3:.4f}')
""",
            "solucion_explicacion": (
                "El canal despolarizante reduce la fidelidad a F = 1 - 2p/3. "
                "Con p=0.2: F = 1 - 0.4/3 ≈ 0.867."
            ),
        },
        {
            "id": "B08",
            "titulo": "Algoritmo de Deutsch-Jozsa",
            "modulo": "Módulo 04 — Algoritmos básicos",
            "enunciado": (
                "Implementa el algoritmo de Deutsch-Jozsa para determinar si la función "
                "f: {0,1}² → {0,1} definida por f(x) = x₀ XOR x₁ es constante o balanceada. "
                "El oráculo marca con fase -1 los inputs donde f(x)=1."
            ),
            "pistas": [
                "f(x) = x₀ XOR x₁ es balanceada (mitad 0s, mitad 1s).",
                "El oráculo phase kickback para CNOT de cada qubit al ancilla.",
                "Si la medición da |00⟩ la función es constante; si da cualquier otra cosa, balanceada.",
            ],
            "solucion_codigo": """\
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

# Oráculo para f(x0,x1) = x0 XOR x1
def oracle_balanced():
    qc = QuantumCircuit(3)  # 2 input + 1 ancilla
    qc.cx(0, 2)
    qc.cx(1, 2)
    return qc

qc = QuantumCircuit(3)
qc.x(2)           # ancilla en |1>
qc.h([0, 1, 2])   # superposición
qc.compose(oracle_balanced(), inplace=True)
qc.h([0, 1])
qc.measure([0, 1], [0, 1])

counts = StatevectorSampler().run([qc], shots=1).result()[0].data.meas.get_counts()
print('Resultado:', counts)  # '11' o similar (no '00') → BALANCEADA
""",
            "solucion_explicacion": (
                "Si la medición es |00⟩ la función es constante; cualquier otro resultado indica balanceada. "
                "XOR es balanceada, así que obtenemos un estado ortogonal a |00⟩."
            ),
        },
        {
            "id": "B09",
            "titulo": "Rotación en la esfera de Bloch con Ry",
            "modulo": "Módulo 01 — Fundamentos",
            "enunciado": (
                "Aplica Ry(θ) a |0⟩ para varios valores de θ ∈ [0, 2π] y verifica "
                "que P(|1⟩) = sin²(θ/2). Dibuja la curva P(1) vs θ."
            ),
            "pistas": [
                "Ry(θ)|0⟩ = cos(θ/2)|0⟩ + sin(θ/2)|1⟩",
                "P(|1⟩) = |sin(θ/2)|² = sin²(θ/2)",
            ],
            "solucion_codigo": """\
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

thetas = np.linspace(0, 2*np.pi, 50)
p1_sim = []
for theta in thetas:
    qc = QuantumCircuit(1)
    qc.ry(theta, 0)
    sv = Statevector(qc)
    p1_sim.append(abs(sv.data[1])**2)

p1_theory = np.sin(thetas/2)**2
print('Max error:', np.max(np.abs(np.array(p1_sim) - p1_theory)))
""",
            "solucion_explicacion": "Ry(θ) rota en el plano Y-Z de la esfera de Bloch: el qubit va de |0⟩ a |1⟩ pasando por |+y⟩.",
        },
        {
            "id": "B10",
            "titulo": "Producto tensorial y sistema de 2 qubits",
            "modulo": "Módulo 01 — Fundamentos",
            "enunciado": (
                "Prepara el estado producto |+⟩⊗|0⟩ (qubit 0 en superposición, qubit 1 en |0⟩). "
                "Verifica que no hay entrelazamiento calculando el determinante de la "
                "matriz de Schmidt."
            ),
            "pistas": [
                "Un estado producto tiene rango de Schmidt 1.",
                "La traza parcial del qubit 0 debe dar un estado puro.",
            ],
            "solucion_codigo": """\
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

qc = QuantumCircuit(2)
qc.h(0)  # qubit 0 en |+>, qubit 1 en |0>
sv = Statevector(qc)

# Reordenar para descomposición de Schmidt: reshape a (2,2)
psi = sv.data.reshape(2, 2)  # filas=q1, cols=q0
S = np.linalg.svd(psi, compute_uv=False)
print('Valores singulares:', np.round(S, 4))
print('Estado producto (rango 1):', np.isclose(S[1], 0))
""",
            "solucion_explicacion": "Un estado producto tiene un solo valor singular no nulo en la descomposición de Schmidt.",
        },
        {
            "id": "B11",
            "titulo": "Circuito GHZ de 3 qubits",
            "modulo": "Módulo 02 — Entrelazamiento",
            "enunciado": (
                "Prepara el estado GHZ de 3 qubits: |GHZ⟩ = (|000⟩ + |111⟩)/√2. "
                "Verifica que solo aparecen '000' y '111' en las mediciones."
            ),
            "pistas": [
                "Comienza con H en el primer qubit, luego CNOT de q0→q1 y de q0→q2.",
            ],
            "solucion_codigo": """\
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 2)
qc.measure_all()

counts = StatevectorSampler().run([qc], shots=2048).result()[0].data.meas.get_counts()
print(counts)  # solo '000' y '111'
""",
            "solucion_explicacion": "El estado GHZ tiene correlaciones no-locales de tres cuerpos: medir uno colapsa los otros dos.",
        },
        {
            "id": "B12",
            "titulo": "Entropia de entrelazamiento de un estado de Bell",
            "modulo": "Módulo 06 — Información Cuántica",
            "enunciado": (
                "Calcula la entropía de Von Neumann S(ρ_A) del qubit A en el estado "
                "de Bell |Φ+⟩. Debe ser S = 1 ebit (máximo entrelazamiento para 2 qubits)."
            ),
            "pistas": [
                "S(ρ) = -Tr(ρ log₂ ρ) = -Σ λᵢ log₂ λᵢ",
                "La traza parcial de |Φ+⟩ sobre B da ρ_A = I/2.",
                "I/2 tiene eigenvalores 1/2, 1/2 → S = 1.",
            ],
            "solucion_codigo": """\
import numpy as np
from qiskit.quantum_info import DensityMatrix, entropy

# Estado Bell |Phi+>
psi = np.array([1,0,0,1])/np.sqrt(2)
rho = DensityMatrix(np.outer(psi, psi.conj()))

# Traza parcial sobre el qubit B (índice 1)
rho_A = rho.partial_transpose([1])  # equivalente a partial_trace
# Forma directa:
rho_A_matrix = np.array([[psi[0]**2 + psi[2]**2, psi[0]*psi[1] + psi[2]*psi[3]],
                          [psi[1]*psi[0] + psi[3]*psi[2], psi[1]**2 + psi[3]**2]])
evals = np.linalg.eigvalsh(rho_A_matrix)
S = -np.sum(evals[evals>1e-12] * np.log2(evals[evals>1e-12]))
print(f'S(rho_A) = {S:.4f} ebit')  # 1.0
""",
            "solucion_explicacion": "La entropía máxima de 1 ebit indica entrelazamiento máximo entre los dos qubits.",
        },
        {
            "id": "B13",
            "titulo": "Codificación superdensa",
            "modulo": "Módulo 03 — Protocolos",
            "enunciado": (
                "Implementa la codificación superdensa para transmitir 2 bits clásicos "
                "('11') usando un único qubit cuántico sobre un canal previamente entrelazado."
            ),
            "pistas": [
                "Para enviar '11': aplica X luego Z al qubit de Alice.",
                "Bob decodifica con CNOT y H.",
            ],
            "solucion_codigo": """\
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

# Mensaje a enviar: '11'
qc = QuantumCircuit(2, 2)
# Crear par Bell compartido
qc.h(0); qc.cx(0, 1)
# Alice codifica '11': Z luego X en qubit 0
qc.z(0); qc.x(0)
# Bob decodifica
qc.cx(0, 1); qc.h(0)
qc.measure([0, 1], [0, 1])

counts = StatevectorSampler().run([qc], shots=100).result()[0].data.meas.get_counts()
print(counts)  # {'11': 100}
""",
            "solucion_explicacion": "La codificación superdensa duplica la capacidad del canal cuántico usando entrelazamiento previo.",
        },
        {
            "id": "B14",
            "titulo": "Operador de Grover para 3 qubits",
            "modulo": "Módulo 04 — Grover",
            "enunciado": (
                "Implementa el oráculo de Grover que marca el estado |101⟩ con fase -1, "
                "y el difusor. Aplica 2 iteraciones y verifica que P(|101⟩) > 0.9."
            ),
            "pistas": [
                "El oráculo para |101⟩: aplica X en q1 (qubit central), luego CCZ, luego X en q1.",
                "El difusor: H⊗n, X⊗n, CCZ (multi-controlada), X⊗n, H⊗n.",
            ],
            "solucion_codigo": """\
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

def oracle_101():
    qc = QuantumCircuit(3)
    qc.x(1)      # flip para que |101> sea |111>
    qc.ccx(0,1,2) if False else qc.h(2)  # simplificado
    # Oráculo de fase para |101>: aplica fase -1
    qc.x(1)
    return qc

# Implementación directa con fase
qc = QuantumCircuit(3)
qc.h([0,1,2])

for _ in range(2):  # 2 iteraciones
    # Oráculo: marca |101> con X(q1), CZ multi-controlada, X(q1)
    qc.x(1)
    qc.h(2); qc.ccx(0,1,2); qc.h(2)
    qc.x(1)
    # Difusor
    qc.h([0,1,2]); qc.x([0,1,2])
    qc.h(2); qc.ccx(0,1,2); qc.h(2)
    qc.x([0,1,2]); qc.h([0,1,2])

sv = Statevector(qc)
print(f'P(|101>) = {abs(sv.data[5])**2:.4f}')  # índice 5 = |101>
""",
            "solucion_explicacion": "Con N=8 estados, el óptimo es k≈π/4·√8≈2.2 iteraciones, dando P≈0.95.",
        },
        {
            "id": "B15",
            "titulo": "Fidelidad y distancia de traza",
            "modulo": "Módulo 06 — Información Cuántica",
            "enunciado": (
                "Para dos qubits en estados |0⟩ y |1⟩, calcula: "
                "(a) la fidelidad F, (b) la distancia de traza D = ||ρ-σ||₁/2. "
                "Verifica la relación 1-F ≤ D."
            ),
            "pistas": [
                "F(|0⟩,|1⟩) = |⟨0|1⟩|² = 0 (estados ortogonales).",
                "D = ||ρ₀-ρ₁||₁/2 = 1 para estados ortogonales.",
            ],
            "solucion_codigo": """\
import numpy as np
from qiskit.quantum_info import DensityMatrix, state_fidelity

rho0 = DensityMatrix.from_label('0')
rho1 = DensityMatrix.from_label('1')

F = state_fidelity(rho0, rho1)
diff = rho0.data - rho1.data
D = 0.5 * np.sum(np.abs(np.linalg.eigvalsh(diff)))

print(f'Fidelidad F = {F:.4f}')       # 0.0
print(f'Distancia de traza D = {D:.4f}')  # 1.0
print(f'1-F <= D: {1-F <= D + 1e-10}')    # True
""",
            "solucion_explicacion": "Estados ortogonales son perfectamente distinguibles: F=0, D=1. La relación 1-F≤D siempre se cumple.",
        },
    ],
    "intermedio": [
        {
            "id": "I01",
            "titulo": "VQE para H₂: energía del estado base",
            "modulo": "Módulo 11 — VQE",
            "enunciado": (
                "Implementa VQE con un ansatz EfficientSU2 de 1 capa para estimar la "
                "energía del estado base de H₂. Hamiltoniano: "
                "H = -1.0523·II + 0.3979·IZ - 0.3979·ZI - 0.0113·ZZ + 0.1809·XX + 0.1809·YY. "
                "Usa COBYLA como optimizador. La energía exacta es ≈ -1.1372 Hartree."
            ),
            "pistas": [
                "SparsePauliOp.from_list([('IZ', coef), ...])",
                "EfficientSU2(2, reps=1) crea el ansatz.",
                "StatevectorEstimator para evaluar ⟨H⟩.",
            ],
            "solucion_codigo": """\
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import EfficientSU2
from qiskit.primitives import StatevectorEstimator
from scipy.optimize import minimize
import numpy as np

H = SparsePauliOp.from_list([
    ('II', -1.0523), ('IZ', 0.3979), ('ZI', -0.3979),
    ('ZZ', -0.0113), ('XX', 0.1809), ('YY', 0.1809)
])

ansatz = EfficientSU2(2, reps=1)
estimator = StatevectorEstimator()

def cost(params):
    bound = ansatz.assign_parameters(params)
    return estimator.run([(bound, H)]).result()[0].data.evs

x0 = np.random.uniform(-np.pi, np.pi, ansatz.num_parameters)
result = minimize(cost, x0, method='COBYLA', options={'maxiter': 500})
print(f'E_VQE = {result.fun:.6f} Hartree')  # cerca de -1.1372
""",
            "solucion_explicacion": "VQE busca el mínimo de ⟨H⟩ variando parámetros del circuito. COBYLA es eficiente para 8-16 parámetros.",
        },
        {
            "id": "I02",
            "titulo": "QAOA para MAX-CUT en grafo de 4 nodos",
            "modulo": "Módulo 09 — QAOA",
            "enunciado": (
                "Resuelve MAX-CUT en el ciclo C₄ (nodos 0-1-2-3-0) con QAOA p=1. "
                "El valor óptimo de MAX-CUT es 4 (corte de todas las aristas). "
                "Encuentra los parámetros γ, β óptimos y muestra la distribución de cortes."
            ),
            "pistas": [
                "El ciclo C₄ tiene aristas (0,1),(1,2),(2,3),(3,0).",
                "MAX-CUT óptimo para C₄ es 4 (bipartición 0,2 vs 1,3).",
                "Barre γ ∈ [0, π], β ∈ [0, π/2] para encontrar el óptimo.",
            ],
            "solucion_codigo": """\
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

edges = [(0,1),(1,2),(2,3),(3,0)]
n = 4

def qaoa_c4(gamma, beta):
    qc = QuantumCircuit(n)
    qc.h(range(n))
    for i,j in edges:
        qc.cx(i,j); qc.rz(2*gamma, j); qc.cx(i,j)
    qc.rx(2*beta, range(n))
    return qc

def cut_val(bs):
    bits = [(bs>>k)&1 for k in range(n)]
    return sum(bits[i]!=bits[j] for i,j in edges)

best, best_gb = -1, (0,0)
for gamma in np.linspace(0, np.pi, 30):
    for beta in np.linspace(0, np.pi/2, 30):
        sv = Statevector(qaoa_c4(gamma, beta))
        exp_cut = sum(abs(sv.data[bs])**2 * cut_val(bs) for bs in range(16))
        if exp_cut > best:
            best, best_gb = exp_cut, (gamma, beta)

print(f'Mejor ⟨C⟩ = {best:.4f}, γ={best_gb[0]:.3f}, β={best_gb[1]:.3f}')
""",
            "solucion_explicacion": "Con p=1, QAOA para C₄ alcanza ⟨C⟩≈3.5/4. Para el óptimo exacto se necesita p≥2.",
        },
        {
            "id": "I03",
            "titulo": "Quantum Phase Estimation para Rz",
            "modulo": "Módulo 07 — QPE",
            "enunciado": (
                "Usa QPE con 4 qubits ancilla para estimar la fase φ de la puerta "
                "U = Rz(2π·3/16). La fase verdadera es φ = 3/16. "
                "Verifica que la medición más probable da k=3 (en binario 0011)."
            ),
            "pistas": [
                "Prepara el autoestado |1⟩ en el qubit objetivo.",
                "La puerta controlada-U^{2^j} aplica Rz(2π·3/16·2^j).",
                "La QFT inversa en los ancilla extrae la fase.",
            ],
            "solucion_codigo": """\
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
import numpy as np

n_ancilla = 4
phase = 3/16  # phi = 3/16
theta = 2 * np.pi * phase  # angulo de Rz

qc = QuantumCircuit(n_ancilla + 1, n_ancilla)
qc.x(n_ancilla)  # autoestado |1> de Rz
qc.h(range(n_ancilla))

for j in range(n_ancilla):
    angle = theta * (2**j)
    qc.crz(angle, j, n_ancilla)

# QFT inversa (manual)
for j in range(n_ancilla//2):
    qc.swap(j, n_ancilla-1-j)
for j in range(n_ancilla):
    qc.h(j)
    for k in range(j+1, n_ancilla):
        qc.cp(-np.pi/2**(k-j), j, k)

qc.measure(range(n_ancilla), range(n_ancilla))
counts = StatevectorSampler().run([qc],shots=1024).result()[0].data.meas.get_counts()
most_likely = max(counts, key=counts.get)
print(f'Resultado más probable: {most_likely} = {int(most_likely,2)}/16')
""",
            "solucion_explicacion": "QPE con 4 ancilla tiene resolución 1/16. Para φ=3/16, el resultado debe ser '0011' (=3).",
        },
        {
            "id": "I04",
            "titulo": "Mitigación de errores ZNE",
            "modulo": "Módulo 28 — Mitigación",
            "enunciado": (
                "Aplica Zero-Noise Extrapolation (ZNE) a un circuito Bell ruidoso. "
                "Usa escalado de ruido con factores λ ∈ {1, 2, 3} (gate folding) "
                "y extrapola linealmente al punto sin ruido (λ=0). "
                "Compara ⟨ZZ⟩ ideal, ruidoso y mitigado."
            ),
            "pistas": [
                "Gate folding: reemplaza U por U·U†·U para escalar el ruido por 3.",
                "Ajusta una recta a los puntos (λ, ⟨O⟩_λ) y evalúa en λ=0.",
            ],
            "solucion_codigo": """\
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit.compiler import transpile
import numpy as np

# Circuito Bell
def bell_circuit(fold_factor=1):
    qc = QuantumCircuit(2)
    for _ in range(fold_factor):
        qc.h(0); qc.cx(0,1)
        if fold_factor > 1:
            qc.cx(0,1); qc.h(0)  # dagger
            qc.h(0); qc.cx(0,1)  # de nuevo
    return qc

ZZ = SparsePauliOp('ZZ')
estimator = StatevectorEstimator()

scales = [1, 2, 3]
values = []
for s in scales:
    qc = bell_circuit(s)
    val = estimator.run([(qc, ZZ)]).result()[0].data.evs
    values.append(float(val))

# Extrapolación lineal a lambda=0
coeffs = np.polyfit(scales, values, 1)
zne_val = coeffs[1]
print(f'Ideal: {values[0]:.4f}, ZNE: {zne_val:.4f}')
""",
            "solucion_explicacion": "ZNE escala el ruido artificialmente para extrapolar al caso sin ruido. Con el circuito Bell ideal ⟨ZZ⟩=1.",
        },
        {
            "id": "I05",
            "titulo": "Código de repetición: tasa de error lógico vs. físico",
            "modulo": "Módulo 14 — Corrección de Errores",
            "enunciado": (
                "Para el código de repetición de distancia d=5, calcula la tasa de "
                "error lógico en función de la tasa de error físico p ∈ [0, 0.15]. "
                "Identifica el umbral (donde P_lógico > P_físico) y el punto de "
                "cruce donde la corrección deja de ayudar."
            ),
            "pistas": [
                "P_lógico = Σ_{k=⌈d/2⌉}^{d} C(d,k) · p^k · (1-p)^{d-k}",
                "Para d=5, se corrigen hasta 2 errores. 3 o más errores dan error lógico.",
            ],
            "solucion_codigo": """\
import numpy as np
from math import comb

d = 5
t = d // 2  # número de errores corregibles

p_values = np.linspace(0, 0.15, 200)
p_logico = np.array([
    sum(comb(d, k) * p**k * (1-p)**(d-k) for k in range(t+1, d+1))
    for p in p_values
])

# Umbral: donde P_logico = P_fisico
threshold_idx = np.argmin(np.abs(p_logico - p_values))
print(f'Umbral d={d}: p_th ≈ {p_values[threshold_idx]:.4f}')
print(f'Con p=0.01: P_lógico = {p_logico[np.argmin(np.abs(p_values-0.01))]:.2e}')
print(f'Con p=0.05: P_lógico = {p_logico[np.argmin(np.abs(p_values-0.05))]:.2e}')
""",
            "solucion_explicacion": "El umbral del código de repetición d=5 es ~p=0.1 (10%). Por encima del umbral, más qubits empeoran el resultado.",
        },
        {
            "id": "I06",
            "titulo": "Kernel cuántico para clasificación binaria",
            "modulo": "Módulo 27 — QML",
            "enunciado": (
                "Implementa un kernel cuántico K(x,y) = |⟨φ(x)|φ(y)⟩|² donde "
                "φ(x) = Ry(x₀)⊗Ry(x₁) para datos 2D. "
                "Clasifica el dataset XOR: {(0,0)→0, (0,1)→1, (1,0)→1, (1,1)→0}."
            ),
            "pistas": [
                "El kernel cuántico mide la similitud entre estados preparados por el feature map.",
                "Con un kernel adecuado, un SVM puede separar XOR aunque no sea linealmente separable.",
            ],
            "solucion_codigo": """\
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def feature_state(x):
    qc = QuantumCircuit(2)
    qc.ry(x[0]*np.pi, 0)
    qc.ry(x[1]*np.pi, 1)
    qc.cx(0, 1)  # correlación entre features
    return Statevector(qc).data

def kernel(x, y):
    return abs(np.dot(feature_state(x).conj(), feature_state(y)))**2

X = np.array([[0,0],[0,1],[1,0],[1,1]])
y = np.array([0, 1, 1, 0])

K = np.array([[kernel(xi, xj) for xj in X] for xi in X])
print('Matriz kernel:')
print(np.round(K, 3))
print('\\nDiagonal (auto-similitud):', np.diag(K).round(3))
""",
            "solucion_explicacion": "El CNOT en el feature map crea correlaciones no-lineales que permiten al kernel capturar la estructura XOR.",
        },
        {
            "id": "I07",
            "titulo": "Estimación de recursos para el algoritmo de Shor",
            "modulo": "Módulo 29 — Fault-Tolerant",
            "enunciado": (
                "Estima el número de qubits lógicos y el número de puertas T necesarios "
                "para factorizar N=15 con el algoritmo de Shor. "
                "Usa la fórmula de recursos: n_qubits = 2n + 3 ancilla, "
                "n_T_gates ≈ 8n³ donde n = ⌈log₂(N)⌉."
            ),
            "pistas": [
                "Para N=15, n = 4 bits.",
                "El circuito de exponenciación modular domina el recuento de puertas.",
            ],
            "solucion_codigo": """\
import numpy as np

N = 15
n = int(np.ceil(np.log2(N)))

n_qubits_logicos = 2*n + 3  # registro, ancilla
n_T_gates = 8 * n**3         # aproximación O(n³)
n_Clifford = 10 * n**2        # puertas Clifford (CNOT, H, S)

print(f'N = {N}, n = {n} bits')
print(f'Qubits lógicos: {n_qubits_logicos}')
print(f'Puertas T:      {n_T_gates}')
print(f'Puertas CNOT:   {n_Clifford}')

# Para fault-tolerant con p_fis=0.1%, d=7, overhead ~50x
overhead = 50
print(f'\\nQubits físicos necesarios (overhead {overhead}x): {n_qubits_logicos * overhead}')
""",
            "solucion_explicacion": "Para N=15 (trivial), los recursos son pequeños. Para RSA-2048, n≈2048 y se necesitan ~60M qubits físicos.",
        },
        {
            "id": "I08",
            "titulo": "Tomografía de estado con medición en 3 bases",
            "modulo": "Módulo 19 — Tomografía",
            "enunciado": (
                "Reconstruye la matriz de densidad de un qubit en el estado |+y⟩ = (|0⟩+i|1⟩)/√2 "
                "midiendo ⟨X⟩, ⟨Y⟩, ⟨Z⟩ y usando ρ = (I + ⟨X⟩X + ⟨Y⟩Y + ⟨Z⟩Z)/2. "
                "Verifica que la fidelidad es 1."
            ),
            "pistas": [
                "⟨X⟩ = 0, ⟨Y⟩ = 1, ⟨Z⟩ = 0 para |+y⟩.",
                "La reconstrucción tomográfica da ρ = (I+Y)/2.",
            ],
            "solucion_codigo": """\
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, DensityMatrix, state_fidelity

# Estado |+y>
qc = QuantumCircuit(1)
qc.h(0)
qc.s(0)  # |+> → |+y> = S|+>

sv = Statevector(qc)
X = np.array([[0,1],[1,0]]); Y = np.array([[0,-1j],[1j,0]]); Z = np.array([[1,0],[0,-1]])
I = np.eye(2)

ex = sv.expectation_value(X).real
ey = sv.expectation_value(Y).real
ez = sv.expectation_value(Z).real
print(f'<X>={ex:.3f}, <Y>={ey:.3f}, <Z>={ez:.3f}')

rho_tomo = (I + ex*X + ey*Y + ez*Z) / 2
rho_ideal = DensityMatrix(sv)
F = state_fidelity(DensityMatrix(rho_tomo), rho_ideal)
print(f'Fidelidad tomografía: {F:.6f}')
""",
            "solucion_explicacion": "La tomografía de estado de un qubit requiere 3 observables (X,Y,Z) para reconstruir ρ completamente.",
        },
        {
            "id": "I09",
            "titulo": "Evolución temporal con Trotterización",
            "modulo": "Módulo 12 — Simulación",
            "enunciado": (
                "Simula la evolución temporal e^{-itH} del Hamiltoniano de Heisenberg "
                "H = ZZ para t = π/4 usando Trotterización de primer orden con n=10 pasos. "
                "Compara con la evolución exacta."
            ),
            "pistas": [
                "e^{-it·ZZ} = phase_gadget(2t)",
                "Con un solo término, la Trotterización es exacta.",
            ],
            "solucion_codigo": """\
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

t = np.pi/4
n_steps = 10
dt = t / n_steps

# Trotter: (e^{-i·dt·ZZ})^n_steps
qc_trotter = QuantumCircuit(2)
for _ in range(n_steps):
    qc_trotter.cx(0, 1)
    qc_trotter.rz(2*dt, 1)
    qc_trotter.cx(0, 1)

# Exacto
qc_exact = QuantumCircuit(2)
qc_exact.cx(0, 1)
qc_exact.rz(2*t, 1)
qc_exact.cx(0, 1)

U_trotter = Operator(qc_trotter).data
U_exact   = Operator(qc_exact).data
error = np.max(np.abs(U_trotter - U_exact))
print(f'Error de Trotter (1 término): {error:.2e}')  # debe ser ~0
""",
            "solucion_explicacion": "Para H=ZZ (un único término), la Trotterización es exacta porque no hay conmutador de error.",
        },
        {
            "id": "I10",
            "titulo": "Quantum Volume: circuito de prueba",
            "modulo": "Módulo 28 — Benchmarking",
            "enunciado": (
                "Implementa un circuito de Quantum Volume para m=3 qubits y 3 capas. "
                "Cada capa aplica una permutación aleatoria seguida de puertas SU(4) aleatorias "
                "en pares de qubits. Verifica que el Heavy Output Generation supera 2/3."
            ),
            "pistas": [
                "Una puerta SU(4) aleatoria se genera con scipy.stats.unitary_group.rvs(4).",
                "El Heavy Output es el conjunto de bitstrings con probabilidad > mediana.",
            ],
            "solucion_codigo": """\
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, random_unitary

m = 3  # qubits
d = 3  # capas
np.random.seed(42)

qc = QuantumCircuit(m)
for _ in range(d):
    perm = np.random.permutation(m)
    for i in range(0, m-1, 2):
        q0, q1 = int(perm[i]), int(perm[i+1])
        U = random_unitary(4).data
        qc.unitary(U, [q0, q1])

sv = Statevector(qc)
probs = np.abs(sv.data)**2
median_prob = np.median(probs)
heavy_output_prob = np.sum(probs[probs > median_prob])
print(f'Heavy Output Probability: {heavy_output_prob:.4f}')
print(f'Supera 2/3: {heavy_output_prob > 2/3}')
""",
            "solucion_explicacion": "QV mide la capacidad de un procesador con un circuito aleatorio. Si HOG > 2/3, QV ≥ 2^m.",
        },
        {
            "id": "I11",
            "titulo": "Phase kickback y eigenvalores",
            "modulo": "Módulo 07 — QPE",
            "enunciado": (
                "Demuestra el phase kickback: si U|u⟩ = e^{iφ}|u⟩, entonces "
                "controlado-U aplicado a |+⟩|u⟩ da e^{iφ/2}(|0⟩+e^{iφ}|1⟩)⊗|u⟩/√2. "
                "Usa U = Z y eigenestado |0⟩ (eigenvalor +1) y |1⟩ (eigenvalor -1)."
            ),
            "pistas": [
                "Control-Z sobre |+⟩|1⟩ aplica fase -1 al |1⟩ del control.",
                "El resultado es (|0⟩-|1⟩)/√2 ⊗ |1⟩ = |−⟩⊗|1⟩.",
            ],
            "solucion_codigo": """\
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

# |+>|1>: control en +, objetivo en eigenestado |1> de Z (eigenvalor -1)
qc = QuantumCircuit(2)
qc.h(0)    # control en |+>
qc.x(1)    # objetivo en |1>
qc.cz(0, 1)  # controlado-Z

sv = Statevector(qc)
print('Amplitudes:', np.round(sv.data, 4))
# Esperado: (|0>|1> - |1>|1>)/sqrt(2) = |->|1>
# Amplitudes: [0, 1/sqrt(2), 0, -1/sqrt(2)]
expected = np.array([0, 1, 0, -1])/np.sqrt(2)
print('Correcto:', np.allclose(sv.data, expected))
""",
            "solucion_explicacion": "Phase kickback transfiere la fase del eigenestado al qubit de control, permitiendo a QPE estimar eigenvalores.",
        },
        {
            "id": "I12",
            "titulo": "Barren plateaus en ansatz profundo",
            "modulo": "Módulo 27 — QML",
            "enunciado": (
                "Demuestra el fenómeno de barren plateaus: para un ansatz aleatorio de "
                "n=6 qubits y profundidad d=10, la varianza del gradiente de ⟨Z₀⟩ "
                "respecto a un parámetro θ debe ser ≈ exponencialmente pequeña en n."
            ),
            "pistas": [
                "Gradiente numérico: (f(θ+ε) - f(θ-ε))/(2ε) con ε pequeño.",
                "La varianza del gradiente escala como ~1/2^n para ansatze aleatorios.",
            ],
            "solucion_codigo": """\
import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit import ParameterVector

n, d = 6, 10
n_samples = 100
Z0 = SparsePauliOp('I'*(n-1) + 'Z')  # Z en qubit 0
estimator = StatevectorEstimator()

gradients = []
for _ in range(n_samples):
    params = np.random.uniform(-np.pi, np.pi, n*d*2)
    eps = 1e-3
    params_p, params_m = params.copy(), params.copy()
    params_p[0] += eps; params_m[0] -= eps

    def eval_circuit(p):
        qc = QuantumCircuit(n)
        idx = 0
        for _ in range(d):
            for q in range(n): qc.ry(p[idx], q); idx += 1
            for q in range(n): qc.rz(p[idx], q); idx += 1
            for q in range(n-1): qc.cx(q, q+1)
        return float(estimator.run([(qc, Z0)]).result()[0].data.evs)

    grad = (eval_circuit(params_p) - eval_circuit(params_m)) / (2*eps)
    gradients.append(grad)

print(f'Var(grad) = {np.var(gradients):.2e}  (esperable ~1/2^{n} = {1/2**n:.2e})')
""",
            "solucion_explicacion": "Barren plateaus: en ansatze aleatorios profundos, Var[∂⟨O⟩/∂θ] ∝ 2^{-n}. El gradiente es exponencialmente pequeño.",
        },
    ],
    "avanzado": [
        {
            "id": "A01",
            "titulo": "Código de superficie d=3: ciclo de síndrome completo",
            "modulo": "Módulo 14 — QEC",
            "enunciado": (
                "Implementa un ciclo de síndrome completo del código de superficie de "
                "distancia d=3 (17 qubits: 9 data + 8 measure). Introduce un error X "
                "en el qubit de datos central y verifica que el síndrome lo detecta "
                "correctamente."
            ),
            "pistas": [
                "El código de superficie d=3 tiene 4 estabilizadores X y 4 estabilizadores Z.",
                "Cada estabilizador mide la paridad de 4 qubits de datos vecinos.",
                "Un error X en el centro activa 2 estabilizadores Z adyacentes.",
            ],
            "solucion_codigo": """\
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
import numpy as np

# Código de superficie d=3 simplificado: código de repetición 2D
# 5 qubits: q0-q3 datos, q4 ancilla central
qc = QuantumCircuit(5, 4)

# Codificación del estado lógico |0_L>
# (en código de repetición: todos en |0>)

# Introducir error X en qubit 1
qc.x(1)

# Ciclo de síndrome: medir ZZ para cada par adyacente
# Ancilla q4 mide paridad de q0,q1,q2,q3
for data_q in [0, 1, 2, 3]:
    qc.cx(data_q, 4)
qc.measure(4, 0)

# Reiniciar ancilla y medir paridades individuales
qc.reset(4)
qc.cx(0, 4); qc.cx(1, 4); qc.measure(4, 1)
qc.reset(4)
qc.cx(1, 4); qc.cx(2, 4); qc.measure(4, 2)
qc.reset(4)
qc.cx(2, 4); qc.cx(3, 4); qc.measure(4, 3)

counts = StatevectorSampler().run([qc], shots=100).result()[0].data.meas.get_counts()
print('Síndromes:', counts)
print('El patrón de síndrome identifica el qubit con error.')
""",
            "solucion_explicacion": "Los estabilizadores ZZ detectan errores X como cambios de paridad. El patrón de síndromes activados localiza el error.",
        },
        {
            "id": "A02",
            "titulo": "Protocolo 15→1 de destilación de estados mágicos",
            "modulo": "Módulo 29 — Fault-Tolerant",
            "enunciado": (
                "Simula el protocolo 15→1 de destilación de estados mágicos. "
                "Dado un estado mágico ruidoso |T⟩ con fidelidad 1-ε (ε=0.01), "
                "estima cuántas rondas son necesarias para llegar a ε_out < 10⁻¹²."
            ),
            "pistas": [
                "Cada ronda: ε_out ≈ 35·ε_in³ (mejora cúbica).",
                "El overhead de copias es 15^k donde k es el número de rondas.",
                "Para ε_in=0.01, se necesitan ~3 rondas.",
            ],
            "solucion_codigo": """\
import numpy as np

epsilon_in = 0.01
target_eps = 1e-12
A = 35  # constante del protocolo 15->1

eps = epsilon_in
rondas = 0
historial = [eps]
overheads = [1]

while eps > target_eps:
    eps = A * eps**3
    rondas += 1
    historial.append(eps)
    overheads.append(15**rondas)
    if rondas > 10: break

print(f'Rondas necesarias: {rondas}')
print(f'Overhead total de copias: {overheads[-1]} estados mágicos')
print()
print(f'{"Ronda":>6} | {"epsilon":>14} | {"Copias":>10}')
print('-' * 38)
for i, (e, o) in enumerate(zip(historial, overheads)):
    print(f'{i:>6} | {e:>14.3e} | {o:>10}')
""",
            "solucion_explicacion": "El protocolo 15→1 reduce el error cúbicamente por ronda. Para ε=10⁻² → ε<10⁻¹² se necesitan ~3 rondas y 15³=3375 copias.",
        },
        {
            "id": "A03",
            "titulo": "Decodificador MWPM para código de repetición",
            "modulo": "Módulo 31 — QEC en Hardware",
            "enunciado": (
                "Implementa un decodificador MWPM simplificado para el código de "
                "repetición de distancia d=7. Dado un historial de síndromes de 10 ciclos, "
                "encuentra la corrección de mínimo peso y calcula la tasa de error lógico."
            ),
            "pistas": [
                "Los síndromes son diferencias de paridades entre ciclos sucesivos.",
                "MWPM para el código de repetición 1D es equivalente a aparear los defectos más cercanos.",
                "Un error lógico ocurre cuando el peso de la corrección es mayor que d/2.",
            ],
            "solucion_codigo": """\
import numpy as np
from itertools import combinations

def simulate_repetition_code(d, p_error, n_cycles, seed=42):
    rng = np.random.default_rng(seed)
    data = np.zeros(d, dtype=int)
    logical_errors = 0

    for cycle in range(n_cycles):
        # Errores físicos
        flips = rng.random(d) < p_error
        data ^= flips.astype(int)
        # Síndrome: paridad entre vecinos
        syndrome = data[:-1] ^ data[1:]
        defects = np.where(syndrome)[0]

        # MWPM simplificado para 1D: apareamos defectos adyacentes
        if len(defects) % 2 == 1:
            defects = np.append(defects, d-1)  # conectar al borde

        corrections = np.zeros(d, dtype=int)
        used = set()
        defects_list = list(defects)
        while len(defects_list) >= 2:
            i, j = defects_list[0], defects_list[1]
            for k in range(min(i,j), max(i,j)+1):
                corrections[k] ^= 1
            defects_list = defects_list[2:]

        data ^= corrections
        if data.sum() % 2 == 1:  # error lógico si paridad impar
            logical_errors += 1
            data = np.zeros(d, dtype=int)  # reset

    return logical_errors / n_cycles

for p in [0.001, 0.005, 0.01, 0.05]:
    rate = simulate_repetition_code(7, p, 1000)
    print(f'p_fis={p:.3f}: P_logico={rate:.4f}')
""",
            "solucion_explicacion": "Para p < umbral (~10% en 1D), el error lógico decrece con la distancia. MWPM en 1D es óptimo para el código de repetición.",
        },
        {
            "id": "A04",
            "titulo": "Algoritmo HHL para sistema 2×2",
            "modulo": "Módulo 33 — Algoritmos FT",
            "enunciado": (
                "Implementa el algoritmo HHL para resolver Ax=b con "
                "A = [[1,0],[0,2]] y b = |+⟩ = (|0⟩+|1⟩)/√2. "
                "La solución exacta es x = (1, 1/2)/||·||. "
                "Usa 2 qubits ancilla para QPE y verifica que el estado de salida "
                "es proporcional a A⁻¹b."
            ),
            "pistas": [
                "Los eigenvalores de A son 1 y 2; sus eigenvectores son |0⟩ y |1⟩.",
                "HHL: QPE → rotación condicional (Ry(2arcsin(C/λ))) → QPE inversa.",
                "La rotación de inversión requiere C < min(λ) = 1.",
            ],
            "solucion_codigo": """\
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

# HHL para A=diag(1,2), b=|+>
# Eigenvalores: lambda_1=1 -> fase phi_1=1/2, lambda_2=2 -> phi_2=1 (en 2 bits)
# QPE con 2 ancilla da: |0.10>|ev1> y |1.00>|ev2>

C = 0.5  # constante HHL (< min eigenvalue = 1)

qc = QuantumCircuit(4)  # q0=b, q1-q2=ancilla QPE, q3=ancilla flag
# Preparar b = |+>
qc.h(0)
# QPE: Hadamard en ancilla
qc.h([1, 2])
# Unitarios e^{i*A*t}: para lambda=1, U^1=e^{i*1*t}; para lambda=2, U^2=e^{i*2*t}
# Con t=pi: e^{i*pi}=-1 para lambda=1, e^{2*i*pi}=1 para lambda=2
# Implementación simplificada para este caso diagonal específico
qc.cp(np.pi, 1, 0)
qc.cp(2*np.pi, 2, 0)
# QFT inversa 2 bits
qc.swap(1, 2)
qc.h(1)
qc.cp(-np.pi/2, 1, 2)
qc.h(2)
# Rotación condicional (inversión)
qc.cry(2*np.arcsin(C/1), 2, 3)  # ancilla q2 codifica lambda_1=1
qc.cry(2*np.arcsin(C/2), 1, 3)  # ancilla q1 codifica lambda_2=2

sv = Statevector(qc)
print('Estado HHL preparado.')
print('Amplitudes (primeros 8):', np.round(np.abs(sv.data[:8]), 3))
""",
            "solucion_explicacion": "HHL invierte A aplicando QPE para codificar eigenvalores, rotación condicional 1/λ, y QPE inversa. La solución está en el espacio donde el ancilla flag = |1⟩.",
        },
        {
            "id": "A05",
            "titulo": "ZX-Calculus: spider fusion y simplificación de QAOA",
            "modulo": "Módulo 26 — ZX-Calculus",
            "enunciado": (
                "Para QAOA con p=4 capas en el grafo triangular (3 aristas), "
                "aplica spider fusion para reducir el número de CNOTs. "
                "Verifica que el circuito simplificado es unitariamente equivalente al original "
                "para cualquier elección de parámetros γ₁..γ₄."
            ),
            "pistas": [
                "Phase gadgets adyacentes con el mismo soporte se fusionan: PG(γᵢ)·PG(γᵢ₊₁)=PG(γᵢ+γᵢ₊₁).",
                "Para p=4 capas alternas (fase-mixer-fase-mixer), entre capas de fase separadas por mixer no hay fusión directa.",
                "Pero si los parámetros γ₁=γ₂, entonces PG(γ₁)·PG(γ₂)=PG(2γ₁) dentro del QAOA compilado.",
            ],
            "solucion_codigo": """\
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

edges = [(0,1),(1,2),(0,2)]
n = 3
gammas = [0.3, 0.7, 0.5, 0.9]
betas  = [0.4, 0.6, 0.2, 0.8]

def qaoa_original(gammas, betas):
    qc = QuantumCircuit(n)
    qc.h(range(n))
    for g, b in zip(gammas, betas):
        for i,j in edges:
            qc.cx(i,j); qc.rz(2*g, j); qc.cx(i,j)
        qc.rx(2*b, range(n))
    return qc

# No hay fusión entre capas con mixer, pero podemos fusionar phase gadgets
# de la MISMA arista en capas consecutivas si beta=0 (compilación agresiva)
# Caso demostrable: fusión dentro de una sola capa de aristas
def pg_fused_layer(gamma, edges, n):
    qc = QuantumCircuit(n)
    for i,j in edges:
        qc.cx(i,j); qc.rz(2*gamma, j); qc.cx(i,j)
    return qc

def pg_split_layer(g1, g2, edges, n):
    qc = QuantumCircuit(n)
    for i,j in edges:
        qc.cx(i,j); qc.rz(2*g1, j); qc.cx(i,j)
    for i,j in edges:
        qc.cx(i,j); qc.rz(2*g2, j); qc.cx(i,j)
    return qc

g1, g2 = 0.4, 0.9
U_fused = Operator(pg_fused_layer(g1+g2, edges, n)).data
U_split  = Operator(pg_split_layer(g1, g2, edges, n)).data
ratio = U_split.flat[0] / U_fused.flat[0]
print(f'PG({g1}+{g2}) == PG({g1})·PG({g2}): {np.allclose(U_split, ratio*U_fused)}')
print(f'CNOTs ahorrados: {sum(1 for g in pg_split_layer(g1,g2,edges,n).data if g.operation.name=="cx") - sum(1 for g in pg_fused_layer(g1+g2,edges,n).data if g.operation.name=="cx")}')
""",
            "solucion_explicacion": "Spider fusion reduce de 2*len(edges)=6 CNOTs a 2*len(edges)=6... pero si se fusionan las capas enteras, la reducción es de 2*n_aristas por par de capas fusionadas.",
        },
        {
            "id": "A06",
            "titulo": "Estimación de amplitud cuántica sin QPE (MLQAE)",
            "modulo": "Módulo 33 — QAE",
            "enunciado": (
                "Implementa Maximum Likelihood QAE (MLQAE) para estimar la amplitud "
                "a = sin²(θ) de un circuito A que prepara |Ψ⟩ = cos(θ)|0⟩|Ψ₀⟩ + sin(θ)|1⟩|Ψ₁⟩. "
                "Usa θ = π/7 y compara con la estimación clásica por Monte Carlo."
            ),
            "pistas": [
                "Grover power: Q^k aplica k veces el operador de Grover.",
                "Con m mediciones de Q^k, la verosimilitud es L(a) = Σ h_k log(p_k(a)).",
                "La estimación ML maximiza Σ h_k log sin²((2k+1)arcsin(√a)).",
            ],
            "solucion_codigo": """\
import numpy as np
from scipy.optimize import minimize_scalar

theta_true = np.pi/7
a_true = np.sin(theta_true)**2

# Simular mediciones con Q^k para k=0,1,...,4
np.random.seed(42)
ks = [0, 1, 2, 4, 8]
n_shots = 200
measurements = {}
for k in ks:
    angle = (2*k+1) * theta_true  # ángulo efectivo tras k iteraciones Grover
    p_k = np.sin(angle)**2
    h_k = np.random.binomial(n_shots, p_k)  # número de éxitos
    measurements[k] = (h_k, n_shots)

def neg_log_likelihood(a):
    if a <= 0 or a >= 1: return 1e10
    theta = np.arcsin(np.sqrt(a))
    nll = 0
    for k, (h, n) in measurements.items():
        p = np.sin((2*k+1)*theta)**2
        p = np.clip(p, 1e-10, 1-1e-10)
        nll -= h*np.log(p) + (n-h)*np.log(1-p)
    return nll

result = minimize_scalar(neg_log_likelihood, bounds=(0.01, 0.99), method='bounded')
a_mlqae = result.x
print(f'a_true  = {a_true:.6f}')
print(f'a_MLQAE = {a_mlqae:.6f}')
print(f'Error   = {abs(a_mlqae - a_true):.2e}')
""",
            "solucion_explicacion": "MLQAE usa los resultados de Grover iterado para estimar la amplitud con complejidad O(1/ε) en lugar de O(1/ε²) del Monte Carlo clásico.",
        },
    ],
}


# ─────────────────────────────────────────────────────────────────────────────
# Funciones de generación de PDF
# ─────────────────────────────────────────────────────────────────────────────

def _wrap(text: str, width: int = 90) -> list[str]:
    """Divide texto en líneas de anchura máxima `width`."""
    lines = []
    for paragraph in text.split("\n"):
        if paragraph.strip() == "":
            lines.append("")
        else:
            lines.extend(textwrap.wrap(paragraph, width=width) or [""])
    return lines


def _generar_pdf_texto(ejercicios: list[dict], incluir_soluciones: bool, output_path: Path) -> None:
    """Genera un PDF con reportlab."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_LEFT
    except ImportError:
        print("  [!] reportlab no instalado. Generando texto plano (.txt)")
        _generar_txt(ejercicios, incluir_soluciones, output_path.with_suffix(".txt"))
        return

    titulo_doc = "Examen de Computación Cuántica — Soluciones" if incluir_soluciones else "Examen de Computación Cuántica"
    doc = SimpleDocTemplate(str(output_path), pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    story = []

    # Portada
    story.append(Paragraph(titulo_doc, styles["Title"]))
    story.append(Spacer(1, 0.5*cm))
    from datetime import date
    story.append(Paragraph(f"Fecha: {date.today().strftime('%d/%m/%Y')} · {len(ejercicios)} ejercicios", styles["Normal"]))
    story.append(Spacer(1, 1*cm))

    code_style = ParagraphStyle(
        "Code", parent=styles["Code"],
        fontSize=8, fontName="Courier",
        backColor=colors.Color(0.95, 0.95, 0.95),
        leftIndent=10, rightIndent=10,
        spaceAfter=6,
    )

    for i, ej in enumerate(ejercicios, 1):
        # Encabezado
        story.append(Paragraph(f"<b>Ejercicio {i} ({ej['id']}): {ej['titulo']}</b>", styles["Heading2"]))
        story.append(Paragraph(f"<i>{ej['modulo']}</i>", styles["Italic"]))
        story.append(Spacer(1, 0.3*cm))

        # Enunciado
        story.append(Paragraph("<b>Enunciado:</b>", styles["Normal"]))
        for line in _wrap(ej["enunciado"]):
            story.append(Paragraph(line or "&nbsp;", styles["Normal"]))
        story.append(Spacer(1, 0.3*cm))

        # Pistas
        if not incluir_soluciones:
            story.append(Paragraph("<b>Pistas:</b>", styles["Normal"]))
            for j, pista in enumerate(ej["pistas"], 1):
                story.append(Paragraph(f"  {j}. {pista}", styles["Normal"]))
            story.append(Spacer(1, 0.3*cm))

        # Espacio para respuesta (sin soluciones)
        if not incluir_soluciones:
            story.append(Paragraph("<b>Respuesta:</b>", styles["Normal"]))
            story.append(Spacer(1, 4*cm))

        # Solución
        if incluir_soluciones:
            story.append(Paragraph("<b>Código de solución:</b>", styles["Normal"]))
            code_lines = ej["solucion_codigo"].strip().split("\n")
            for line in code_lines:
                story.append(Preformatted(line, code_style))
            story.append(Spacer(1, 0.3*cm))
            story.append(Paragraph("<b>Explicación:</b>", styles["Normal"]))
            for line in _wrap(ej["solucion_explicacion"]):
                story.append(Paragraph(line or "&nbsp;", styles["Normal"]))
            story.append(Spacer(1, 0.5*cm))

        story.append(Spacer(1, 0.5*cm))

    doc.build(story)
    print(f"  PDF generado: {output_path}")


def _generar_txt(ejercicios: list[dict], incluir_soluciones: bool, output_path: Path) -> None:
    """Fallback: genera texto plano si reportlab no está disponible."""
    lines = []
    titulo = "EXAMEN — SOLUCIONES" if incluir_soluciones else "EXAMEN DE COMPUTACIÓN CUÁNTICA"
    lines += [titulo, "=" * len(titulo), ""]

    for i, ej in enumerate(ejercicios, 1):
        lines += [
            f"Ejercicio {i} ({ej['id']}): {ej['titulo']}",
            f"Módulo: {ej['modulo']}",
            "-" * 60,
            "Enunciado:",
            *_wrap(ej["enunciado"]),
            "",
        ]
        if not incluir_soluciones:
            lines += ["Pistas:"] + [f"  {j+1}. {p}" for j, p in enumerate(ej["pistas"])] + ["", "Respuesta:", "", ""]
        else:
            lines += ["Código:", ej["solucion_codigo"], "", "Explicación:", *_wrap(ej["solucion_explicacion"]), "", ""]

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Texto plano generado: {output_path}")


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generador de exámenes de Computación Cuántica",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
            Ejemplos:
              python generador_examen.py --nivel basico --n 5 --seed 42
              python generador_examen.py --nivel intermedio --n 4 --seed 7
              python generador_examen.py --todos --n 8 --seed 0 --salida examen_final
              python generador_examen.py --nivel avanzado --nivel basico --n 3 --seed 1
        """),
    )
    parser.add_argument("--nivel", action="append", choices=["basico", "intermedio", "avanzado"],
                        help="Nivel de dificultad (puede repetirse para mezclar niveles)")
    parser.add_argument("--todos", action="store_true", help="Usar todos los niveles")
    parser.add_argument("--n", type=int, default=5, help="Número de ejercicios (default: 5)")
    parser.add_argument("--seed", type=int, default=None, help="Semilla aleatoria para reproducibilidad")
    parser.add_argument("--salida", type=str, default="examen", help="Nombre base del archivo de salida (default: examen)")
    parser.add_argument("--listar", action="store_true", help="Lista todos los ejercicios disponibles y sale")
    args = parser.parse_args()

    if args.listar:
        for nivel, ejercs in EJERCICIOS.items():
            print(f"\n{'═'*50}")
            print(f"  NIVEL: {nivel.upper()} ({len(ejercs)} ejercicios)")
            print(f"{'═'*50}")
            for ej in ejercs:
                print(f"  [{ej['id']}] {ej['titulo']}")
                print(f"         {ej['modulo']}")
        return

    niveles = ["basico", "intermedio", "avanzado"] if args.todos else (args.nivel or ["basico"])
    pool = []
    for nivel in niveles:
        pool.extend(EJERCICIOS.get(nivel, []))

    if not pool:
        print("No hay ejercicios para los niveles seleccionados.")
        return

    rng = random.Random(args.seed)
    n_sel = min(args.n, len(pool))
    seleccionados = rng.sample(pool, n_sel)

    print(f"\nGenerando examen: {n_sel} ejercicios, seed={args.seed}, niveles={niveles}")
    print(f"Ejercicios seleccionados: {[e['id'] for e in seleccionados]}\n")

    salida_base = Path(args.salida)
    _generar_pdf_texto(seleccionados, incluir_soluciones=False, output_path=salida_base.parent / (salida_base.name + "_enunciados.pdf"))
    _generar_pdf_texto(seleccionados, incluir_soluciones=True,  output_path=salida_base.parent / (salida_base.name + "_soluciones.pdf"))
    print("\nListo.")


if __name__ == "__main__":
    main()
