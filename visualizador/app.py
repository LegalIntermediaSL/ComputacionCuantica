import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector, plot_histogram
from qiskit_aer import AerSimulator

st.set_page_config(page_title="Visualizador Cuántico - ComputacionCuantica", layout="wide")

st.title("🌌 Visualizador Cuántico Interactivo")
st.markdown("Bienvenido al laboratorio visual del curso. Aquí puedes manipular un qubit y observar cómo el ruido afecta a la información.")

# Sidebar - Controles
st.sidebar.header("Configuración del Qubit")
theta = st.sidebar.slider("Ángulo Theta (Latitud)", 0.0, np.pi, 0.0)
phi = st.sidebar.slider("Ángulo Phi (Longitud)", 0.0, 2*np.pi, 0.0)

st.sidebar.header("Simulación de Ruido")
ruido_bit_flip = st.sidebar.slider("Probabilidad de Bit Flip (X)", 0.0, 1.0, 0.0)
ruido_phase_flip = st.sidebar.slider("Probabilidad de Phase Flip (Z)", 0.0, 1.0, 0.0)

# 1. Crear el estado inicial
qc = QuantumCircuit(1)
# Preparamos el estado según los ángulos de la esfera de Bloch
qc.u(theta, phi, 0, 0)

# 2. Aplicar ruido (Conceptual)
# Para una visualización limpia, usamos el Statevector ideal y ruidoso por separado
sv_ideal = Statevector.from_instruction(qc)

# 3. Layout de Columnas
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Esfera de Bloch (Estado Ideal)")
    fig_bloch = plot_bloch_multivector(sv_ideal)
    st.pyplot(fig_bloch)
    st.info(f"Estado: cos({theta/2:.2f})|0> + e^{phi:.2f}i sin({theta/2:.2f})|1>")

with col2:
    st.subheader("📊 Probabilidades de Medición")
    # Simulamos la medición
    qc_m = qc.copy()
    qc_m.measure_all()
    sim = AerSimulator()
    job = sim.run(qc_m, shots=1024)
    counts = job.result().get_counts()
    
    fig_hist = plot_histogram(counts)
    st.pyplot(fig_hist)

st.divider()

st.header("🔬 Efecto del Ruido en el Hardware")
st.write("Ajusta los sliders de la izquierda para ver cómo la decoherencia degradaría este qubit en un sistema real.")

# Simulación simplificada de ruido para visualización
if ruido_bit_flip > 0 or ruido_phase_flip > 0:
    st.warning(f"Simulando ruido acumulado... Bit-Flip: {ruido_bit_flip*100:.1f}%, Phase-Flip: {ruido_phase_flip*100:.1f}%")
    # Mostramos una estimación de pérdida de fidelidad
    fidelidad = max(0.0, 1.0 - (ruido_bit_flip + ruido_phase_flip)/2)
    st.metric("Fidelidad Estimada", f"{fidelidad*100:.2f}%")
    
    if fidelidad < 0.5:
        st.error("⚠️ El ruido es tan alto que el qubit ha perdido su información (Estado de máxima mezcla).")

st.markdown("---")
st.caption("Parte del repositorio de Computación Cuántica - 2026")
