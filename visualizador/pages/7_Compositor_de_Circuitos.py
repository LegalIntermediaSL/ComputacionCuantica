"""Compositor de circuitos cuánticos interactivo."""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp
from qiskit.visualization import plot_bloch_multivector
from qiskit.primitives import StatevectorSampler

st.set_page_config(page_title="Compositor de Circuitos", layout="wide")
st.title("Compositor de circuitos cuánticos")
st.markdown(
    "Construye tu propio circuito cuántico añadiendo puertas qubit a qubit. "
    "El estado y las probabilidades se actualizan en tiempo real."
)

# ─── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Configuración")
    n_qubits = st.slider("Número de qubits", 1, 4, 2)
    shots = st.slider("Shots de medición", 256, 4096, 1024, step=256)

    st.divider()
    st.header("Añadir puerta")
    tipo_puerta = st.selectbox(
        "Puerta",
        ["H", "X", "Y", "Z", "S", "T", "Sdg", "Tdg",
         "RX", "RY", "RZ", "CNOT", "CZ", "SWAP", "CCX"],
    )

    qubit_1 = st.selectbox("Qubit objetivo", list(range(n_qubits)), key="q1")

    angulo = None
    if tipo_puerta in ["RX", "RY", "RZ"]:
        angulo = st.slider("Ángulo (rad)", -float(np.pi), float(np.pi), float(np.pi/2), step=0.05)

    qubit_2 = None
    if tipo_puerta in ["CNOT", "CZ", "SWAP"]:
        opciones_q2 = [q for q in range(n_qubits) if q != qubit_1]
        if opciones_q2:
            qubit_2 = st.selectbox("Qubit control/objetivo 2", opciones_q2, key="q2")
        else:
            st.warning("Necesitas ≥2 qubits para puertas de 2 qubits.")

    qubit_3 = None
    if tipo_puerta == "CCX":
        opciones_q2 = [q for q in range(n_qubits) if q != qubit_1]
        opciones_q3 = [q for q in range(n_qubits) if q != qubit_1]
        if len(opciones_q2) >= 2 and n_qubits >= 3:
            qubit_2 = st.selectbox("Qubit control 2", opciones_q2, key="q2ccx")
            qubit_3 = st.selectbox("Qubit objetivo (CCX)", [q for q in opciones_q3 if q != qubit_2], key="q3ccx")
        else:
            st.warning("CCX requiere ≥3 qubits.")

    col_add, col_reset = st.columns(2)
    add_gate = col_add.button("➕ Añadir", use_container_width=True, type="primary")
    reset = col_reset.button("🗑 Reset", use_container_width=True)

# ─── Estado de la sesión ─────────────────────────────────────────────────────
if "gates" not in st.session_state or reset:
    st.session_state.gates = []
if "n_qubits_prev" not in st.session_state:
    st.session_state.n_qubits_prev = n_qubits
if st.session_state.n_qubits_prev != n_qubits:
    st.session_state.gates = []
    st.session_state.n_qubits_prev = n_qubits

# Añadir puerta al historial
if add_gate:
    entrada = {
        "tipo": tipo_puerta,
        "q1": qubit_1,
        "q2": qubit_2,
        "q3": qubit_3,
        "angulo": angulo,
    }
    # Validaciones
    if tipo_puerta in ["CNOT", "CZ", "SWAP"] and qubit_2 is None:
        st.sidebar.error("Selecciona un segundo qubit.")
    elif tipo_puerta == "CCX" and (qubit_2 is None or qubit_3 is None):
        st.sidebar.error("CCX requiere 3 qubits.")
    else:
        st.session_state.gates.append(entrada)

# ─── Construir circuito ──────────────────────────────────────────────────────
def build_circuit(gates: list, n: int) -> QuantumCircuit:
    qc = QuantumCircuit(n)
    for g in gates:
        t, q1, q2, q3, ang = g["tipo"], g["q1"], g["q2"], g["q3"], g["angulo"]
        if t == "H":      qc.h(q1)
        elif t == "X":    qc.x(q1)
        elif t == "Y":    qc.y(q1)
        elif t == "Z":    qc.z(q1)
        elif t == "S":    qc.s(q1)
        elif t == "T":    qc.t(q1)
        elif t == "Sdg":  qc.sdg(q1)
        elif t == "Tdg":  qc.tdg(q1)
        elif t == "RX":   qc.rx(ang, q1)
        elif t == "RY":   qc.ry(ang, q1)
        elif t == "RZ":   qc.rz(ang, q1)
        elif t == "CNOT" and q2 is not None: qc.cx(q1, q2)
        elif t == "CZ"   and q2 is not None: qc.cz(q1, q2)
        elif t == "SWAP" and q2 is not None: qc.swap(q1, q2)
        elif t == "CCX"  and q2 is not None and q3 is not None: qc.ccx(q1, q2, q3)
    return qc

qc = build_circuit(st.session_state.gates, n_qubits)

# ─── Historial de puertas ────────────────────────────────────────────────────
col_hist, col_export = st.columns([2, 1])

with col_hist:
    st.subheader("Puertas añadidas")
    if not st.session_state.gates:
        st.info("Aún no has añadido puertas. El estado inicial es |0…0⟩.")
    else:
        for i, g in enumerate(st.session_state.gates):
            label = f"`{g['tipo']}`"
            if g["angulo"] is not None:
                label += f"({g['angulo']:.3f})"
            label += f" → q{g['q1']}"
            if g["q2"] is not None:
                label += f", q{g['q2']}"
            if g["q3"] is not None:
                label += f", q{g['q3']}"
            st.markdown(f"{i+1}. {label}")

        if st.button("Eliminar última puerta"):
            st.session_state.gates.pop()
            st.rerun()

with col_export:
    st.subheader("Código Qiskit")
    lines = [f"from qiskit import QuantumCircuit",
             f"qc = QuantumCircuit({n_qubits})"]
    for g in st.session_state.gates:
        t, q1, q2, q3, ang = g["tipo"], g["q1"], g["q2"], g["q3"], g["angulo"]
        if t == "H":      lines.append(f"qc.h({q1})")
        elif t == "X":    lines.append(f"qc.x({q1})")
        elif t == "Y":    lines.append(f"qc.y({q1})")
        elif t == "Z":    lines.append(f"qc.z({q1})")
        elif t == "S":    lines.append(f"qc.s({q1})")
        elif t == "T":    lines.append(f"qc.t({q1})")
        elif t == "Sdg":  lines.append(f"qc.sdg({q1})")
        elif t == "Tdg":  lines.append(f"qc.tdg({q1})")
        elif t == "RX":   lines.append(f"qc.rx({ang:.4f}, {q1})")
        elif t == "RY":   lines.append(f"qc.ry({ang:.4f}, {q1})")
        elif t == "RZ":   lines.append(f"qc.rz({ang:.4f}, {q1})")
        elif t == "CNOT" and q2 is not None: lines.append(f"qc.cx({q1}, {q2})")
        elif t == "CZ"   and q2 is not None: lines.append(f"qc.cz({q1}, {q2})")
        elif t == "SWAP" and q2 is not None: lines.append(f"qc.swap({q1}, {q2})")
        elif t == "CCX"  and q2 is not None and q3 is not None:
            lines.append(f"qc.ccx({q1}, {q2}, {q3})")
    st.code("\n".join(lines), language="python")

# ─── Visualización ───────────────────────────────────────────────────────────
st.divider()
sv = Statevector.from_instruction(qc)

tab1, tab2, tab3 = st.tabs(["Diagrama del circuito", "Esfera de Bloch", "Mediciones"])

with tab1:
    if qc.num_qubits > 0 and len(st.session_state.gates) > 0:
        fig_qc, ax_qc = plt.subplots(figsize=(max(6, len(st.session_state.gates)*1.2 + 2), n_qubits + 1))
        qc.draw("mpl", ax=ax_qc, style="iqp", fold=-1)
        st.pyplot(fig_qc)
        plt.close(fig_qc)
    else:
        st.info("Añade puertas para ver el diagrama del circuito.")

with tab2:
    fig_bloch = plot_bloch_multivector(sv)
    st.pyplot(fig_bloch)
    plt.close(fig_bloch)

    # Vector de Bloch (solo para 1 qubit)
    if n_qubits == 1:
        cols_b = st.columns(3)
        for pauli, col in zip(["X", "Y", "Z"], cols_b):
            val = sv.expectation_value(SparsePauliOp(pauli)).real
            col.metric(f"⟨{pauli}⟩", f"{val:.4f}")

with tab3:
    # Histograma de probabilidades teóricas
    probs = sv.probabilities_dict(decimals=4)
    labels = list(probs.keys())
    values = list(probs.values())

    fig_hist, ax_hist = plt.subplots(figsize=(max(6, len(labels)*0.6 + 2), 4))
    colors = ["#3498db" if v == max(values) else "#85c1e9" for v in values]
    ax_hist.bar(labels, values, color=colors)
    ax_hist.set_xlabel("Estado")
    ax_hist.set_ylabel("Probabilidad")
    ax_hist.set_title("Distribución de probabilidades (teórico)")
    plt.xticks(rotation=45)
    st.pyplot(fig_hist)
    plt.close(fig_hist)

    # Simulación con shots
    st.subheader(f"Simulación con {shots} shots")
    qc_m = qc.copy()
    qc_m.measure_all()
    sampler = StatevectorSampler()
    result = sampler.run([qc_m], shots=shots).result()
    counts = result[0].data.meas.get_counts()

    fig_counts, ax_counts = plt.subplots(figsize=(max(6, len(counts)*0.6 + 2), 4))
    sorted_counts = dict(sorted(counts.items()))
    ax_counts.bar(sorted_counts.keys(),
                  [v/shots for v in sorted_counts.values()],
                  color="#2ecc71")
    ax_counts.set_xlabel("Estado medido")
    ax_counts.set_ylabel("Frecuencia relativa")
    ax_counts.set_title(f"Distribución empírica ({shots} shots)")
    plt.xticks(rotation=45)
    st.pyplot(fig_counts)
    plt.close(fig_counts)

    # Estadísticas
    st.caption(f"Profundidad del circuito: {qc.depth()} | "
               f"Número de puertas: {sum(qc.count_ops().values())} | "
               f"Dimensión del espacio de Hilbert: 2^{n_qubits} = {2**n_qubits}")

st.caption("Tutorial: módulos 01-04 (fundamentos) y 02 (Qiskit básico)")
