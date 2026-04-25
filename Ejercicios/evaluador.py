"""
Evaluador automático de ejercicios — ComputacionCuantica v1.1

Ejecuta la función del alumno y compara el resultado contra la solución
de referencia. Devuelve un score 0-100 con feedback.

Uso:
    from evaluador import evaluar
    score, feedback = evaluar("basicos", 1, mi_funcion)
"""

import numpy as np
import traceback
from typing import Callable, Any


# ─── Utilidades de comparación ────────────────────────────────────────────────

def _fidelidad(estado1, estado2) -> float:
    """Fidelidad entre dos vectores de estado o matrices densidad."""
    try:
        from qiskit.quantum_info import state_fidelity, Statevector, DensityMatrix
        if hasattr(estado1, '__len__') and not isinstance(estado1, (str, dict)):
            a = np.array(estado1, dtype=complex)
            b = np.array(estado2, dtype=complex)
            # Normalizar
            a /= np.linalg.norm(a)
            b /= np.linalg.norm(b)
            return float(abs(np.dot(a.conj(), b))**2)
        return 0.5
    except Exception:
        return 0.0


def _distribucion_similar(counts1: dict, counts2: dict, tolerancia: float = 0.1) -> bool:
    """Compara dos distribuciones de medición con tolerancia en variación total."""
    todos_estados = set(counts1.keys()) | set(counts2.keys())
    total1 = sum(counts1.values())
    total2 = sum(counts2.values())
    if total1 == 0 or total2 == 0:
        return False
    variacion_total = sum(
        abs(counts1.get(s, 0)/total1 - counts2.get(s, 0)/total2)
        for s in todos_estados
    )
    return variacion_total / 2 < tolerancia  # distancia de variación total


def _energia_cercana(e_alumno: float, e_ref: float, tolerancia_ha: float = 0.05) -> bool:
    """Compara energías en Hartree con tolerancia (criterio químico: 1.6 mHa)."""
    return abs(e_alumno - e_ref) < tolerancia_ha


# ─── Definición de ejercicios de referencia ───────────────────────────────────

EJERCICIOS = {
    # ── Básicos ──────────────────────────────────────────────────────────────
    ("basicos", 1): {
        "titulo": "Crear estado |+⟩ con puerta H",
        "descripcion": "Implementa un circuito de 1 qubit que prepare |+⟩ = H|0⟩.",
        "tipo": "circuito",
        "referencia": lambda: _circuito_hadamard(),
        "verificar": lambda alumno, ref: _verificar_circuito_1q(alumno, [0.5, 0.5]),
        "pista": "Aplica la puerta Hadamard sobre el qubit 0.",
    },
    ("basicos", 2): {
        "titulo": "Estado de Bell |Φ+⟩",
        "descripcion": "Prepara el estado de Bell |Φ+⟩ = (|00⟩+|11⟩)/√2.",
        "tipo": "circuito",
        "referencia": lambda: _circuito_bell(),
        "verificar": lambda alumno, ref: _verificar_distribucion_bell(alumno),
        "pista": "H en qubit 0, luego CNOT con control en 0 y objetivo en 1.",
    },
    ("basicos", 3): {
        "titulo": "Rotación Rz(π/3)",
        "descripcion": "Aplica Rz(π/3) al estado |+⟩ y devuelve el vector de estado.",
        "tipo": "estado",
        "referencia": lambda: _estado_rz_sobre_hadamard(np.pi/3),
        "verificar": lambda alumno, ref: _verificar_estado(alumno, ref),
        "pista": "Primero H, luego Rz(π/3).",
    },
    ("basicos", 4): {
        "titulo": "Teleportación cuántica",
        "descripcion": "Implementa el circuito completo de teleportación de 1 qubit.",
        "tipo": "circuito_3q",
        "referencia": lambda: _circuito_teleportacion(),
        "verificar": lambda alumno, ref: _verificar_teleportacion(alumno),
        "pista": "Preparar par de Bell, aplicar protocolo, corregir con mediciones clásicas.",
    },
    ("basicos", 5): {
        "titulo": "Valor esperado de Z",
        "descripcion": "Calcula ⟨Z⟩ para el estado |+⟩. Debe ser 0.",
        "tipo": "valor",
        "referencia": lambda: 0.0,
        "verificar": lambda alumno, ref: _verificar_valor(alumno, ref, tol=0.05),
        "pista": "Crea |+⟩ con H y usa expectation_value(SparsePauliOp('Z')).",
    },

    # ── Intermedios ───────────────────────────────────────────────────────────
    ("intermedios", 1): {
        "titulo": "QFT de 3 qubits",
        "descripcion": "Implementa la Transformada Cuántica de Fourier para 3 qubits.",
        "tipo": "unitario",
        "referencia": lambda: _qft_matrix(3),
        "verificar": lambda alumno, ref: _verificar_unitario(alumno, ref),
        "pista": "Usa H + puertas de fase controladas CRZ(π/2^k) para cada qubit.",
    },
    ("intermedios", 2): {
        "titulo": "VQE energía H₂",
        "descripcion": "Minimiza ⟨H_H2⟩ y obtén una energía dentro de 50 mHa de -1.8572 Ha.",
        "tipo": "energia",
        "referencia": lambda: -1.8572,
        "verificar": lambda alumno, ref: _verificar_valor(alumno, ref, tol=0.05),
        "pista": "Usa EfficientSU2 como ansatz y StatevectorEstimator.",
    },
    ("intermedios", 3): {
        "titulo": "CNOT entre qubits no adyacentes",
        "descripcion": "Implementa CNOT entre qubits 0 y 2 usando solo CNOT entre adyacentes.",
        "tipo": "circuito",
        "referencia": lambda: _cnot_no_adyacente(),
        "verificar": lambda alumno, ref: _verificar_unitario_2(alumno, ref),
        "pista": "Necesitas SWAP para mover el qubit control al adyacente del objetivo.",
    },

    # ── Avanzados ──────────────────────────────────────────────────────────────
    ("avanzados", 1): {
        "titulo": "Código de repetición 3-qubit",
        "descripcion": "Implementa codificación y corrección del código de repetición 3-qubit.",
        "tipo": "circuito",
        "referencia": lambda: _codigo_repeticion_3q(),
        "verificar": lambda alumno, ref: _verificar_circuito_qec(alumno),
        "pista": "Codifica |0_L⟩=|000⟩, introduce error de bit-flip, mide síndromes.",
    },
    ("avanzados", 2): {
        "titulo": "Phase gadget ZZ de 3 qubits",
        "descripcion": "Implementa exp(-iπ/6 · Z⊗Z⊗Z) y verifica la equivalencia matricial.",
        "tipo": "unitario_3q",
        "referencia": lambda: _phase_gadget_ref(3, np.pi/3),
        "verificar": lambda alumno, ref: _verificar_unitario_3q(alumno, ref),
        "pista": "CNOT-tree desde qubit 0 hasta 2, Rz(π/3) en qubit 2, CNOT-tree inverso.",
    },
}


# ─── Funciones de referencia ──────────────────────────────────────────────────

def _circuito_hadamard():
    from qiskit import QuantumCircuit
    qc = QuantumCircuit(1)
    qc.h(0)
    return qc

def _circuito_bell():
    from qiskit import QuantumCircuit
    qc = QuantumCircuit(2)
    qc.h(0); qc.cx(0, 1)
    return qc

def _estado_rz_sobre_hadamard(angle):
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector
    qc = QuantumCircuit(1)
    qc.h(0); qc.rz(angle, 0)
    return Statevector.from_instruction(qc).data

def _circuito_teleportacion():
    from qiskit import QuantumCircuit
    qc = QuantumCircuit(3, 2)
    qc.h(1); qc.cx(1, 2)
    qc.cx(0, 1); qc.h(0)
    qc.measure([0, 1], [0, 1])
    qc.cx(1, 2); qc.cz(0, 2)
    return qc

def _qft_matrix(n):
    from qiskit.circuit.library import QFT
    from qiskit.quantum_info import Operator
    return Operator(QFT(n)).data

def _cnot_no_adyacente():
    from qiskit import QuantumCircuit
    qc = QuantumCircuit(3)
    qc.cx(0, 1); qc.cx(1, 2); qc.cx(0, 1)
    return qc

def _codigo_repeticion_3q():
    from qiskit import QuantumCircuit
    qc = QuantumCircuit(3)
    qc.cx(0, 1); qc.cx(0, 2)
    return qc

def _phase_gadget_ref(n, alpha):
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Operator
    qc = QuantumCircuit(n)
    for i in range(n-1):
        qc.cx(i, i+1)
    qc.rz(alpha, n-1)
    for i in range(n-2, -1, -1):
        qc.cx(i, i+1)
    return Operator(qc).data


# ─── Funciones de verificación ────────────────────────────────────────────────

def _verificar_circuito_1q(alumno_fn, probs_esperadas):
    try:
        from qiskit.quantum_info import Statevector
        qc = alumno_fn()
        sv = Statevector.from_instruction(qc)
        probs = [abs(a)**2 for a in sv.data]
        ok = all(abs(p - e) < 0.05 for p, e in zip(probs, probs_esperadas))
        return 100 if ok else 30, "OK" if ok else f"Probabilidades incorrectas: {probs}"
    except Exception as e:
        return 0, f"Error: {e}"

def _verificar_distribucion_bell(alumno_fn):
    try:
        from qiskit import QuantumCircuit
        from qiskit.quantum_info import Statevector
        qc = alumno_fn()
        sv = Statevector.from_instruction(qc)
        probs = {f"{i:0{qc.num_qubits}b}": abs(a)**2 for i, a in enumerate(sv.data)}
        p00 = probs.get('00', 0)
        p11 = probs.get('11', 0)
        ok = abs(p00 - 0.5) < 0.05 and abs(p11 - 0.5) < 0.05
        return (100, "Estado de Bell correcto") if ok else (40, f"p(00)={p00:.3f}, p(11)={p11:.3f}")
    except Exception as e:
        return 0, f"Error: {e}"

def _verificar_estado(alumno_fn, ref):
    try:
        resultado = alumno_fn()
        arr = np.array(resultado, dtype=complex)
        arr /= np.linalg.norm(arr)
        ref_arr = np.array(ref, dtype=complex)
        ref_arr /= np.linalg.norm(ref_arr)
        fid = abs(np.dot(arr.conj(), ref_arr))**2
        score = int(fid * 100)
        return score, f"Fidelidad: {fid:.4f}"
    except Exception as e:
        return 0, f"Error: {e}"

def _verificar_teleportacion(alumno_fn):
    try:
        qc = alumno_fn()
        tiene_medicion = qc.num_clbits >= 2
        tiene_3q = qc.num_qubits >= 3
        ok = tiene_medicion and tiene_3q
        return (80, "Estructura correcta (verificación completa requiere simulación)") if ok else (20, "Faltan mediciones o qubits")
    except Exception as e:
        return 0, f"Error: {e}"

def _verificar_valor(alumno_fn, ref, tol=0.01):
    try:
        val = float(alumno_fn())
        err = abs(val - ref)
        if err < tol:
            return 100, f"Correcto: {val:.6f} (error {err:.2e})"
        elif err < tol * 10:
            return 60, f"Aproximado: {val:.6f} vs {ref:.6f}"
        else:
            return 0, f"Incorrecto: {val:.6f} vs {ref:.6f}"
    except Exception as e:
        return 0, f"Error: {e}"

def _verificar_unitario(alumno_fn, ref):
    try:
        from qiskit.quantum_info import Operator
        U_alumno = np.array(alumno_fn(), dtype=complex)
        U_ref = np.array(ref, dtype=complex)
        fid = abs(np.trace(U_alumno.conj().T @ U_ref)) / U_ref.shape[0]
        score = int(min(fid, 1.0) * 100)
        return score, f"Fidelidad unitaria: {fid:.4f}"
    except Exception as e:
        return 0, f"Error: {e}"

def _verificar_unitario_2(alumno_fn, ref):
    return _verificar_unitario(alumno_fn, ref)

def _verificar_unitario_3q(alumno_fn, ref):
    return _verificar_unitario(alumno_fn, ref)

def _verificar_circuito_qec(alumno_fn):
    try:
        qc = alumno_fn()
        tiene_3q = qc.num_qubits >= 3
        tiene_cx = qc.count_ops().get('cx', 0) >= 2
        ok = tiene_3q and tiene_cx
        return (80, "Estructura de codificación detectada") if ok else (20, "Faltan CNOTs o qubits")
    except Exception as e:
        return 0, f"Error: {e}"


# ─── Función principal de evaluación ─────────────────────────────────────────

def evaluar(nivel: str, numero: int, funcion_alumno: Callable) -> tuple[int, str]:
    """
    Evalúa la solución del alumno.

    Args:
        nivel: 'basicos', 'intermedios' o 'avanzados'
        numero: número del ejercicio (1-indexado)
        funcion_alumno: función que devuelve el resultado del alumno

    Returns:
        (score: int 0-100, feedback: str)
    """
    clave = (nivel, numero)
    if clave not in EJERCICIOS:
        return 0, f"Ejercicio ({nivel}, {numero}) no encontrado. Disponibles: {list(EJERCICIOS.keys())}"

    ejercicio = EJERCICIOS[clave]
    print(f"\n{'='*60}")
    print(f"Evaluando: {ejercicio['titulo']}")
    print(f"Nivel: {nivel.capitalize()} · Nº {numero}")
    print(f"{'='*60}")

    try:
        ref = ejercicio['referencia']
        score, mensaje = ejercicio['verificar'](funcion_alumno, ref)
    except Exception:
        score = 0
        mensaje = f"Error al ejecutar tu solución:\n{traceback.format_exc()}"

    # Feedback formateado
    if score >= 90:
        nivel_feedback = "EXCELENTE"
        emoji = "🎯"
    elif score >= 70:
        nivel_feedback = "BIEN"
        emoji = "✅"
    elif score >= 40:
        nivel_feedback = "PARCIALMENTE CORRECTO"
        emoji = "⚠️"
    else:
        nivel_feedback = "INCORRECTO"
        emoji = "❌"

    feedback = f"{emoji} {nivel_feedback} — Score: {score}/100\n{mensaje}"

    if score < 90:
        feedback += f"\n\nPista: {ejercicio['pista']}"

    print(feedback)
    return score, feedback


def listar_ejercicios():
    """Muestra todos los ejercicios disponibles."""
    print("Ejercicios disponibles:")
    niveles = ['basicos', 'intermedios', 'avanzados']
    for nivel in niveles:
        ejercs = [(k, v) for k, v in EJERCICIOS.items() if k[0] == nivel]
        if ejercs:
            print(f"\n  {nivel.capitalize()}:")
            for (_, num), ej in sorted(ejercs, key=lambda x: x[0][1]):
                print(f"    {num}. {ej['titulo']}")


if __name__ == "__main__":
    listar_ejercicios()

    print("\n\n--- Demo de evaluación ---")

    # Solución correcta del ejercicio básico 1
    def mi_estado_mas():
        from qiskit import QuantumCircuit
        qc = QuantumCircuit(1)
        qc.h(0)
        return qc

    score, fb = evaluar("basicos", 1, mi_estado_mas)

    # Solución incorrecta
    def estado_incorrecto():
        from qiskit import QuantumCircuit
        qc = QuantumCircuit(1)
        qc.x(0)  # produce |1⟩, no |+⟩
        return qc

    score2, fb2 = evaluar("basicos", 1, estado_incorrecto)
