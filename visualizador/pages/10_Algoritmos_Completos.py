"""
Página 10 — Simulador de Algoritmos Completos
Visualiza la evolución del vector de estado paso a paso para algoritmos cuánticos canónicos.
"""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from tour_guide import show_tour

st.set_page_config(page_title="Algoritmos Completos", layout="wide")
st.title("🔬 Simulador de Algoritmos Completos")
st.markdown("Ejecuta el circuito **paso a paso** y observa cómo evoluciona el vector de estado.")

_TOUR_STEPS = [
    ("🔬 Simulador de Algoritmos", "Elige un algoritmo y simúlalo paso a paso para ver cómo evoluciona el estado cuántico en cada puerta."),
    ("📋 Selección de algoritmo", "Cada algoritmo tiene su circuito canónico. Puedes ajustar parámetros como el número de qubits o el estado objetivo."),
    ("⏭️ Control de pasos", "Usa el deslizador 'Paso' para avanzar o retroceder en el circuito. El estado se recalcula en tiempo real."),
    ("📊 Distribución de probabilidad", "El histograma muestra |amplitud|² para cada estado base. Es lo que mediría un detector real."),
    ("🌐 Amplitudes complejas", "La tabla muestra amplitudes reales e imaginarias: cada estado base tiene una amplitud compleja α con |α|²=probabilidad."),
    ("🔗 Entrelazamiento", "Observa cómo las puertas de 2 qubits (CNOT, CZ) crean correlaciones — los estados de múltiples qubits no se pueden factorizar."),
]

show_tour("algoritmos_completos", _TOUR_STEPS)

# ---------------------------------------------------------------------------
# Definición de los algoritmos
# ---------------------------------------------------------------------------

def circuito_deutsch_jozsa(n: int = 3, funcion: str = "balanceada") -> QuantumCircuit:
    """Deutsch-Jozsa: distingue función constante de balanceada."""
    qc = QuantumCircuit(n + 1)
    qc.x(n)              # ancilla en |1⟩
    qc.h(range(n + 1))   # Hadamard en todos
    if funcion == "balanceada":
        qc.cx(0, n)      # oráculo balanceado: f(x) = x₀
    # Constante: oráculo = identidad
    qc.h(range(n))       # Hadamard inverso en registro
    qc.measure_all() if False else None  # no medir para ver estado
    return qc

def circuito_grover(n: int = 3, target: int = 5) -> QuantumCircuit:
    """Grover para n qubits con oráculo que marca |target⟩."""
    from math import floor, pi, sqrt
    qc = QuantumCircuit(n)
    qc.h(range(n))

    n_iter = max(1, floor(pi / 4 * sqrt(2**n)))
    target_bits = [(target >> k) & 1 for k in range(n)]

    for _ in range(n_iter):
        # Oráculo: flip de fase en |target⟩
        for q in range(n):
            if target_bits[q] == 0:
                qc.x(q)
        qc.h(n-1)
        qc.mcx(list(range(n-1)), n-1)
        qc.h(n-1)
        for q in range(n):
            if target_bits[q] == 0:
                qc.x(q)
        # Difusor
        qc.h(range(n))
        qc.x(range(n))
        qc.h(n-1)
        qc.mcx(list(range(n-1)), n-1)
        qc.h(n-1)
        qc.x(range(n))
        qc.h(range(n))

    return qc

def circuito_qft(n: int = 4) -> QuantumCircuit:
    """Transformada de Fourier Cuántica sobre n qubits."""
    from qiskit.circuit.library import QFT
    qc = QuantumCircuit(n)
    qc.h(0)              # estado inicial no trivial
    qc.append(QFT(n), range(n))
    return qc

def circuito_teleportacion() -> QuantumCircuit:
    """Teletransportación cuántica de |+⟩."""
    qc = QuantumCircuit(3)
    qc.h(0)              # preparar |+⟩ en q0
    qc.h(1)              # par EPR
    qc.cx(1, 2)
    qc.cx(0, 1)          # Bell measurement
    qc.h(0)
    # Correcciones condicionales (simuladas unitariamente)
    qc.cx(1, 2)
    qc.cz(0, 2)
    return qc

def circuito_bernstein_vazirani(n: int = 4, secreto: int = 0b1011) -> QuantumCircuit:
    """Bernstein-Vazirani: encuentra el secreto s tal que f(x)=s·x."""
    qc = QuantumCircuit(n + 1)
    qc.x(n)
    qc.h(range(n + 1))
    # Oráculo: f(x) = s·x = XOR de bits donde s_i = 1
    for i in range(n):
        if (secreto >> i) & 1:
            qc.cx(i, n)
    qc.h(range(n))
    return qc

def circuito_shor_n15() -> QuantumCircuit:
    """Circuito simplificado de Shor para N=15, a=7 (versión compacta)."""
    n_count = 4
    n_f = 4
    qc = QuantumCircuit(n_count + n_f)
    qc.x(n_count)         # registro f en |1⟩
    qc.h(range(n_count))  # Hadamard en conteo
    # Oracle simplificado (no la versión completa — a efectos pedagógicos)
    for j in range(n_count):
        if j % 4 == 0:
            qc.cx(j, n_count + 1)
        elif j % 4 == 1:
            qc.cx(j, n_count + 2)
        elif j % 4 == 2:
            qc.cx(j, n_count)
    # QFT inversa (simplificada)
    from qiskit.circuit.library import QFT
    qc.append(QFT(n_count, inverse=True), range(n_count))
    return qc

ALGORITMOS = {
    "Bell (2q)": lambda: _bell_circuit(),
    "Deutsch-Jozsa (3q, balanceada)": lambda: circuito_deutsch_jozsa(3, "balanceada"),
    "Deutsch-Jozsa (3q, constante)": lambda: circuito_deutsch_jozsa(3, "constante"),
    "Bernstein-Vazirani (s=1011)": lambda: circuito_bernstein_vazirani(4, 0b1011),
    "Grover (3q, target=|101⟩)": lambda: circuito_grover(3, 0b101),
    "QFT (4q)": lambda: circuito_qft(4),
    "Teletransportación": lambda: circuito_teleportacion(),
    "Shor N=15 (compacto)": lambda: circuito_shor_n15(),
}

def _bell_circuit() -> QuantumCircuit:
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    return qc

# ---------------------------------------------------------------------------
# Descomposición en pasos
# ---------------------------------------------------------------------------

def descomponer_pasos(qc: QuantumCircuit) -> list[tuple[str, QuantumCircuit]]:
    """Devuelve una lista de (etiqueta, subcircuito) para cada puerta."""
    pasos = [("Inicio |0...0⟩", QuantumCircuit(qc.num_qubits))]
    qc_acum = QuantumCircuit(qc.num_qubits)

    for instruccion in qc.decompose(reps=2).data:
        gate = instruccion.operation
        qubits = [qc.find_bit(q).index for q in instruccion.qubits]
        nombre = gate.name.upper()
        if gate.params:
            nombre += f"({', '.join(f'{p:.3f}' for p in gate.params)})"
        etiqueta = f"{nombre} @ q{qubits}"

        # Añadir instrucción al circuito acumulado
        qc_acum = qc_acum.copy()
        qc_acum.append(gate, qubits)

        pasos.append((etiqueta, qc_acum.copy()))

    return pasos

# ---------------------------------------------------------------------------
# Interfaz
# ---------------------------------------------------------------------------

col1, col2 = st.columns([1, 2])

with col1:
    algo_nombre = st.selectbox("Algoritmo", list(ALGORITMOS.keys()))
    qc_full = ALGORITMOS[algo_nombre]()
    pasos = descomponer_pasos(qc_full)

    paso_idx = st.slider("Paso", 0, len(pasos) - 1, 0)
    etiqueta_paso, qc_paso = pasos[paso_idx]

    st.info(f"**Paso {paso_idx}/{len(pasos)-1}:** `{etiqueta_paso}`")

    # Circuito completo
    st.markdown("**Circuito completo:**")
    st.text(str(qc_full.draw(fold=60)))

with col2:
    # Calcular statevector
    sv = Statevector(qc_paso)
    n = sv.num_qubits
    N = 2**n

    amplitudes = sv.data
    probs = np.abs(amplitudes)**2
    labels = [f"|{format(i, f'0{n}b')}⟩" for i in range(N)]

    tab1, tab2, tab3 = st.tabs(["📊 Distribución", "🔢 Amplitudes", "📐 Diagrama"])

    with tab1:
        fig, ax = plt.subplots(figsize=(10, 4))
        colores = ['#2196F3' if p > 0.01 else '#BDBDBD' for p in probs]
        ax.bar(range(N), probs, color=colores, edgecolor='white', linewidth=0.5)
        ax.set_xticks(range(N))
        ax.set_xticklabels(labels, rotation=45 if N > 8 else 0, fontsize=max(7, 10-n))
        ax.set_ylabel("Probabilidad")
        ax.set_ylim(0, 1.05)
        ax.set_title(f"Distribución de probabilidad — {etiqueta_paso}")
        ax.grid(axis='y', alpha=0.3)
        # Anotar probabilidades no triviales
        for i, p in enumerate(probs):
            if p > 0.05:
                ax.text(i, p + 0.02, f'{p:.2f}', ha='center', fontsize=8)
        st.pyplot(fig)
        plt.close(fig)

    with tab2:
        import pandas as pd
        df = pd.DataFrame({
            'Estado': labels,
            'Re(α)': np.real(amplitudes).round(4),
            'Im(α)': np.imag(amplitudes).round(4),
            '|α|²': probs.round(4),
            'Fase (°)': np.degrees(np.angle(amplitudes)).round(1),
        })
        # Filtrar estados con probabilidad no nula
        df_vis = df[df['|α|²'] > 1e-6].reset_index(drop=True)
        st.dataframe(df_vis, use_container_width=True)
        st.caption(f"Mostrando {len(df_vis)} de {N} estados con probabilidad > 10⁻⁶")

        # Norma
        norma = np.linalg.norm(amplitudes)
        color_norma = "🟢" if abs(norma - 1.0) < 1e-6 else "🔴"
        st.metric("Norma del estado", f"{norma:.8f}", help="Debe ser exactamente 1.0")
        st.write(f"{color_norma} {'OK' if abs(norma-1.0)<1e-6 else 'Error de normalización'}")

    with tab3:
        # Diagrama de fases (diagrama de Argand)
        fig2, axes2 = plt.subplots(1, 2, figsize=(12, 4))

        # Argand diagram
        ax_arg = axes2[0]
        theta_circle = np.linspace(0, 2*np.pi, 100)
        ax_arg.plot(np.cos(theta_circle), np.sin(theta_circle), 'k--', alpha=0.2, lw=1)
        for i, (a, label) in enumerate(zip(amplitudes, labels)):
            if abs(a)**2 > 0.005:
                ax_arg.annotate('', xy=(a.real, a.imag), xytext=(0, 0),
                                arrowprops=dict(arrowstyle='->', color=f'C{i%10}', lw=2))
                ax_arg.text(a.real*1.1, a.imag*1.1, label, fontsize=8, color=f'C{i%10}')
        ax_arg.set_xlim(-1.3, 1.3); ax_arg.set_ylim(-1.3, 1.3)
        ax_arg.axhline(0, color='k', lw=0.5); ax_arg.axvline(0, color='k', lw=0.5)
        ax_arg.set_xlabel("Re(α)"); ax_arg.set_ylabel("Im(α)")
        ax_arg.set_title("Diagrama de Argand (amplitudes)")
        ax_arg.set_aspect('equal')
        ax_arg.grid(alpha=0.2)

        # Progreso de pasos
        ax_prog = axes2[1]
        pasos_probs = []
        for _, qc_p in pasos:
            sv_p = Statevector(qc_p)
            pasos_probs.append(np.abs(sv_p.data)**2)

        pasos_probs = np.array(pasos_probs)
        for i in range(min(N, 8)):  # máximo 8 estados para claridad
            ax_prog.plot(range(len(pasos)), pasos_probs[:, i],
                        label=labels[i], lw=1.5, marker='o', ms=3)
        ax_prog.axvline(paso_idx, color='red', ls='--', alpha=0.7, lw=1.5)
        ax_prog.set_xlabel("Paso"); ax_prog.set_ylabel("Probabilidad")
        ax_prog.set_title("Evolución de probabilidades por paso")
        ax_prog.legend(fontsize=7, loc='upper right')
        ax_prog.grid(alpha=0.3)

        st.pyplot(fig2)
        plt.close(fig2)

# Información del circuito
with st.expander("ℹ️ Información del circuito"):
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Qubits", qc_full.num_qubits)
    col_b.metric("Profundidad", qc_full.depth())
    col_c.metric("Puertas totales", qc_full.size())

    descripciones = {
        "Bell (2q)": "Estado de Bell |Φ+⟩ = (|00⟩+|11⟩)/√2. Entrelazamiento máximo.",
        "Deutsch-Jozsa (3q, balanceada)": "Distingue función constante vs balanceada con 1 sola consulta (clásico necesita 2^(n-1)+1).",
        "Grover (3q, target=|101⟩)": "Búsqueda cuántica en O(√N) consultas. El estado marcado se amplifica.",
        "QFT (4q)": "Transformada de Fourier Cuántica — base del algoritmo de Shor y QPE.",
        "Teletransportación": "Transmisión de estado cuántico usando par EPR + 2 bits clásicos.",
        "Shor N=15 (compacto)": "Versión compacta para demostración. El circuito real requiere 12 qubits y oracle completo.",
        "Bernstein-Vazirani (s=1011)": "Encuentra el secreto s en UNA consulta. Clásico necesita n consultas.",
        "Deutsch-Jozsa (3q, constante)": "Para función constante, todos los qubits del registro vuelven a |0⟩.",
    }
    if algo_nombre in descripciones:
        st.info(descripciones[algo_nombre])
