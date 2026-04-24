"""Esfera de Bloch e impacto del ruido — página original mejorada."""
import streamlit as st
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, DensityMatrix
from qiskit.visualization import plot_bloch_multivector, plot_histogram
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, phase_damping_error

st.set_page_config(page_title="Esfera de Bloch", layout="wide")
st.title("Esfera de Bloch e impacto del ruido")
st.markdown(
    "Manipula el estado de un qubit con los ángulos de Bloch y observa cómo "
    "distintos canales de ruido degradan el estado."
)

# --- Controles ---
with st.sidebar:
    st.header("Estado inicial")
    theta = st.slider("θ (latitud, 0=|0⟩ π=|1⟩)", 0.0, float(np.pi), 0.0, step=0.05)
    phi   = st.slider("φ (longitud, 0=|+⟩ π=|-⟩)", 0.0, float(2*np.pi), 0.0, step=0.05)

    st.header("Canal de ruido")
    canal = st.selectbox(
        "Tipo de canal",
        ["Ninguno", "Despolarizante", "Amortiguamiento de amplitud", "Desfase puro"],
    )
    p_ruido = st.slider("Parámetro de ruido p (o γ)", 0.0, 1.0, 0.0, step=0.01)
    shots   = st.slider("Shots de medición", 256, 4096, 1024, step=256)

# --- Estado ideal ---
qc = QuantumCircuit(1)
qc.u(theta, phi, 0, 0)
sv_ideal = Statevector.from_instruction(qc)
rho_ideal = DensityMatrix(sv_ideal)

# Bloch vector ideal
r_ideal = np.array([
    sv_ideal.expectation_value("X").real,
    sv_ideal.expectation_value("Y").real,
    sv_ideal.expectation_value("Z").real,
])

# --- Aplicar canal de ruido a la matriz de densidad ---
rho_data = rho_ideal.data.copy()

if canal == "Despolarizante" and p_ruido > 0:
    I = np.eye(2)
    X = np.array([[0,1],[1,0]])
    Y = np.array([[0,-1j],[1j,0]])
    Z = np.array([[1,0],[0,-1]])
    rho_data = (1 - p_ruido) * rho_data + (p_ruido/3) * (
        X @ rho_data @ X + Y @ rho_data @ Y + Z @ rho_data @ Z
    )
elif canal == "Amortiguamiento de amplitud" and p_ruido > 0:
    K0 = np.array([[1, 0], [0, np.sqrt(1 - p_ruido)]])
    K1 = np.array([[0, np.sqrt(p_ruido)], [0, 0]])
    rho_data = K0 @ rho_data @ K0.conj().T + K1 @ rho_data @ K1.conj().T
elif canal == "Desfase puro" and p_ruido > 0:
    K0 = np.array([[1, 0], [0, np.sqrt(1 - p_ruido)]])
    K1 = np.array([[0, 0], [0, np.sqrt(p_ruido)]])
    rho_data = K0 @ rho_data @ K0.conj().T + K1 @ rho_data @ K1.conj().T

rho_ruidoso = DensityMatrix(rho_data)
sv_ruidoso_bloch = rho_ruidoso

r_ruidoso = np.array([
    (rho_data[0,1] + rho_data[1,0]).real,
    (1j * (rho_data[0,1] - rho_data[1,0])).real,
    (rho_data[0,0] - rho_data[1,1]).real,
])

# --- Layout ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Estado ideal")
    fig_ideal = plot_bloch_multivector(sv_ideal)
    st.pyplot(fig_ideal)
    st.caption(
        f"r⃗ = ({r_ideal[0]:.3f}, {r_ideal[1]:.3f}, {r_ideal[2]:.3f})  "
        f"|r⃗| = {np.linalg.norm(r_ideal):.3f}"
    )

with col2:
    st.subheader(f"Estado tras canal: {canal}")
    fig_ruidoso = plot_bloch_multivector(rho_ruidoso)
    st.pyplot(fig_ruidoso)
    norm_r = np.linalg.norm(r_ruidoso)
    st.caption(
        f"r⃗ = ({r_ruidoso[0]:.3f}, {r_ruidoso[1]:.3f}, {r_ruidoso[2]:.3f})  "
        f"|r⃗| = {norm_r:.3f}"
    )
    if norm_r < 0.01:
        st.error("Estado de máxima mezcla: toda la información cuántica se ha perdido.")

with col3:
    st.subheader("Probabilidades de medición")
    qc_m = qc.copy()
    qc_m.measure_all()

    noise_model = NoiseModel()
    if canal == "Despolarizante" and p_ruido > 0:
        noise_model.add_all_qubit_quantum_error(depolarizing_error(p_ruido, 1), ["u"])
    elif canal == "Desfase puro" and p_ruido > 0:
        noise_model.add_all_qubit_quantum_error(phase_damping_error(p_ruido), ["u"])

    sim = AerSimulator()
    job = sim.run(qc_m, noise_model=noise_model if canal != "Ninguno" else None, shots=shots)
    counts = job.result().get_counts()
    from qiskit.visualization import plot_histogram
    st.pyplot(plot_histogram(counts))

# --- Métricas ---
st.divider()
col_m1, col_m2, col_m3 = st.columns(3)
fidelidad = float(np.abs(np.trace(np.sqrt(np.sqrt(rho_ideal.data) @ rho_data @ np.sqrt(rho_ideal.data))))**2)
with col_m1:
    st.metric("Fidelidad F(ρ_ideal, ρ_ruido)", f"{fidelidad:.4f}")
with col_m2:
    pureza = float(np.trace(rho_data @ rho_data).real)
    st.metric("Pureza Tr(ρ²)", f"{pureza:.4f}", delta=f"{pureza - 1.0:.4f}")
with col_m3:
    contraccion = float(np.linalg.norm(r_ruidoso) / max(np.linalg.norm(r_ideal), 1e-9))
    st.metric("Contracción |r_ruidoso|/|r_ideal|", f"{contraccion:.4f}")

st.caption("Tutorial: módulos 01_fundamentos y 16_canales_cuanticos_y_ruido")
