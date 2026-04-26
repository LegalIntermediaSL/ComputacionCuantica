"""Simulador de circuitos con modelos de ruido realistas — comparativa ideal vs. ruidoso."""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from tour_guide import show_tour, export_figure_button

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp
from qiskit.primitives import StatevectorSampler, StatevectorEstimator
from qiskit_aer import AerSimulator
from qiskit_aer.noise import (
    NoiseModel, depolarizing_error, thermal_relaxation_error, ReadoutError
)

st.set_page_config(page_title="Simulador Ruidoso", layout="wide")
st.title("Simulador de circuitos con ruido realista")
st.markdown(
    "Compara el comportamiento **ideal** vs. **ruidoso** de circuitos cuánticos estándar. "
    "Mide TVD, fidelidad de Hellinger y Cross-Entropy Benchmarking score."
)

_TOUR_STEPS = [
    {"title": "Circuito de referencia",
     "body": "Elige el circuito a simular: **Bell** (entrelazamiento máximo), "
             "**QFT 3q** (Transformada de Fourier), **Grover 3q** (búsqueda) o "
             "**QAOA p=1** (optimización). Cada uno tiene una distribución ideal característica."},
    {"title": "Modelo de ruido",
     "body": "Selecciona el modelo: **Despolarizante** (ruido uniforme en todas las puertas), "
             "**T1/T2** (relajación y decoherencia realista, como en superconductores) o "
             "**Error de readout** (confusión en la medición). Puedes combinarlos."},
    {"title": "Parámetros de ruido",
     "body": "Ajusta la **tasa de error por puerta** p (despolarizante) o los tiempos "
             "**T1, T2** en microsegundos. Los valores típicos de IBM son T1~200μs, T2~150μs, "
             "con ciclos de puerta de ~35ns (1Q) y ~100ns (2Q)."},
    {"title": "Distribución ideal vs. ruidosa",
     "body": "El histograma superpone la distribución ideal (barras azules) y la ruidosa "
             "(barras rojas). Con ruido alto, las probabilidades se aplanan hacia la "
             "distribución uniforme (1/2ⁿ por estado)."},
    {"title": "Métricas de calidad",
     "body": "**TVD** (Total Variation Distance): distancia entre distribuciones, 0=idénticas, 1=opuestas. "
             "**Fidelidad Hellinger**: F_H = (Σ√(p_i·q_i))², 1=perfecta. "
             "**XEB score**: Cross-Entropy Benchmarking, mide la correlación con el ideal."},
    {"title": "Exportar figura",
     "body": "Usa el botón '📥 Exportar PNG' para descargar la comparativa como imagen "
             "con los parámetros de ruido incrustados en los metadatos del archivo."},
]
show_tour("simulador_ruidoso", _TOUR_STEPS)

# ─── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Circuito")
    circuito_nombre = st.selectbox(
        "Circuito de referencia",
        ["Bell (2q)", "QFT 3 qubits", "Grover 3q (target |101⟩)", "QAOA p=1 (triángulo)"]
    )

    st.header("Modelo de ruido")
    usar_depolar = st.checkbox("Despolarizante por puerta", value=True)
    p_depolar_1q = st.slider("p error 1Q (%)", 0.0, 5.0, 0.2, 0.05) / 100 if usar_depolar else 0.0
    p_depolar_2q = st.slider("p error 2Q (%)", 0.0, 10.0, 1.0, 0.1) / 100 if usar_depolar else 0.0

    usar_t1t2 = st.checkbox("T1/T2 (relajación térmica)", value=False)
    T1_us = st.slider("T1 (μs)", 10, 500, 200) if usar_t1t2 else 200
    T2_us = st.slider("T2 (μs)", 10, 300, 150) if usar_t1t2 else 150
    t_gate_1q_ns = 35   # ns
    t_gate_2q_ns = 100

    usar_readout = st.checkbox("Error de readout", value=False)
    p_readout = st.slider("p readout error (%)", 0.0, 10.0, 1.0, 0.1) / 100 if usar_readout else 0.0

    shots = st.select_slider("Shots", [512, 1024, 2048, 4096, 8192], value=2048)


# ─── Construcción del circuito ───────────────────────────────────────────────
def build_circuit(nombre: str) -> QuantumCircuit:
    if nombre.startswith("Bell"):
        qc = QuantumCircuit(2)
        qc.h(0); qc.cx(0, 1)
    elif nombre.startswith("QFT"):
        qc = QuantumCircuit(3)
        for j in range(3):
            qc.h(j)
            for k in range(j + 1, 3):
                qc.cp(2 * np.pi / 2 ** (k - j + 1), j, k)
        qc.swap(0, 2)
    elif nombre.startswith("Grover"):
        qc = QuantumCircuit(3)
        qc.h([0, 1, 2])
        # 2 iteraciones Grover para |101>
        for _ in range(2):
            qc.x(1)
            qc.h(2); qc.ccx(0, 1, 2); qc.h(2)
            qc.x(1)
            qc.h([0, 1, 2]); qc.x([0, 1, 2])
            qc.h(2); qc.ccx(0, 1, 2); qc.h(2)
            qc.x([0, 1, 2]); qc.h([0, 1, 2])
    else:  # QAOA
        qc = QuantumCircuit(3)
        gamma, beta = 0.5, 0.3
        qc.h([0, 1, 2])
        for i, j in [(0, 1), (1, 2), (0, 2)]:
            qc.cx(i, j); qc.rz(2 * gamma, j); qc.cx(i, j)
        qc.rx(2 * beta, [0, 1, 2])
    return qc


qc_base = build_circuit(circuito_nombre)
n_qubits = qc_base.num_qubits

# ─── Distribución ideal ──────────────────────────────────────────────────────
sv_ideal = Statevector(qc_base)
probs_ideal = np.abs(sv_ideal.data) ** 2
labels = [format(i, f"0{n_qubits}b") for i in range(2 ** n_qubits)]

# ─── Modelo de ruido ─────────────────────────────────────────────────────────
noise_model = NoiseModel()
has_noise = usar_depolar or usar_t1t2 or usar_readout

if usar_depolar and p_depolar_1q > 0:
    err_1q = depolarizing_error(p_depolar_1q, 1)
    noise_model.add_all_qubit_quantum_error(err_1q, ['h', 'x', 'rz', 'ry', 'rx', 'sx', 's'])
if usar_depolar and p_depolar_2q > 0:
    err_2q = depolarizing_error(p_depolar_2q, 2)
    noise_model.add_all_qubit_quantum_error(err_2q, ['cx', 'cz', 'cp'])
    err_3q = depolarizing_error(min(3 * p_depolar_2q, 0.999), 3)
    noise_model.add_all_qubit_quantum_error(err_3q, ['ccx'])

if usar_t1t2:
    T1_ns = T1_us * 1000
    T2_ns = min(T2_us * 1000, 2 * T1_ns)
    for gate, t_gate in [(['h', 'x', 'rz', 'ry', 'rx'], t_gate_1q_ns),
                         (['cx', 'cz'], t_gate_2q_ns)]:
        for q in range(n_qubits):
            err = thermal_relaxation_error(T1_ns, T2_ns, t_gate)
            for g in gate:
                noise_model.add_quantum_error(err, g, [q])

if usar_readout and p_readout > 0:
    ro_err = ReadoutError([[1 - p_readout, p_readout], [p_readout, 1 - p_readout]])
    for q in range(n_qubits):
        noise_model.add_readout_error(ro_err, [q])

# ─── Simulación ruidosa ──────────────────────────────────────────────────────
qc_meas = qc_base.copy()
qc_meas.measure_all()

if has_noise:
    sim = AerSimulator(noise_model=noise_model)
    from qiskit.compiler import transpile
    qc_t = transpile(qc_meas, sim)
    result_noisy = sim.run(qc_t, shots=shots).result()
    counts_noisy = result_noisy.get_counts()
    probs_noisy = np.array([counts_noisy.get(lb, 0) / shots for lb in labels])
else:
    probs_noisy = probs_ideal.copy()

# ─── Métricas ────────────────────────────────────────────────────────────────
def tvd(p, q):
    return 0.5 * np.sum(np.abs(p - q))

def hellinger_fidelity(p, q):
    return np.sum(np.sqrt(p * q)) ** 2

def xeb_score(p_ideal, p_noisy):
    n = len(p_ideal)
    expected_uniform = 1.0 / n
    xeb = n * np.sum(p_ideal * p_noisy) - 1
    return float(np.clip(xeb, -1.0, 1.0))

tvd_val = tvd(probs_ideal, probs_noisy)
hf_val  = hellinger_fidelity(probs_ideal + 1e-12, probs_noisy + 1e-12)
xeb_val = xeb_score(probs_ideal, probs_noisy)

# ─── Layout principal ────────────────────────────────────────────────────────
col_circ, col_metricas = st.columns([2, 1])

with col_circ:
    st.subheader("Circuito base")
    st.text(qc_base.draw("text"))

with col_metricas:
    st.subheader("Métricas de calidad")
    st.metric("TVD (↓ mejor)", f"{tvd_val:.4f}", delta=None,
              help="Total Variation Distance: 0=idéntico, 1=opuesto")
    st.metric("Fidelidad Hellinger (↑ mejor)", f"{hf_val:.4f}",
              help="1=distribución perfecta, 0=sin solapamiento")
    st.metric("XEB score (↑ mejor)", f"{xeb_val:.4f}",
              help="Cross-Entropy Benchmarking: 1=ideal, 0=ruido total, -1=peor que uniforme")
    if has_noise:
        ruido_desc = []
        if usar_depolar:
            ruido_desc.append(f"Depolar: {p_depolar_1q*100:.2f}%/1Q, {p_depolar_2q*100:.2f}%/2Q")
        if usar_t1t2:
            ruido_desc.append(f"T1={T1_us}μs, T2={T2_us}μs")
        if usar_readout:
            ruido_desc.append(f"Readout: {p_readout*100:.1f}%")
        st.caption(" | ".join(ruido_desc))
    else:
        st.success("Sin ruido — distribución ideal")

st.divider()

# ─── Histograma comparativo ──────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 4))

x = np.arange(len(labels))
width = 0.4
ax = axes[0]
bars_i = ax.bar(x - width/2, probs_ideal, width, label="Ideal", color="#3498db", alpha=0.85)
bars_n = ax.bar(x + width/2, probs_noisy, width, label="Ruidoso", color="#e74c3c", alpha=0.85)
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45, fontsize=9)
ax.set_xlabel("Estado de salida")
ax.set_ylabel("Probabilidad")
ax.set_title(f"Distribución: {circuito_nombre}")
ax.legend()
ax.grid(alpha=0.3, axis="y")

# Diferencia
ax2 = axes[1]
diff = probs_noisy - probs_ideal
colors_diff = ["#e74c3c" if d > 0 else "#2ecc71" for d in diff]
ax2.bar(x, diff, color=colors_diff, alpha=0.85)
ax2.axhline(0, color="black", linewidth=0.8, linestyle="--")
ax2.set_xticks(x)
ax2.set_xticklabels(labels, rotation=45, fontsize=9)
ax2.set_xlabel("Estado de salida")
ax2.set_ylabel("Δ probabilidad (ruidoso − ideal)")
ax2.set_title(f"Desviación del ruido (TVD={tvd_val:.3f})")
ax2.grid(alpha=0.3, axis="y")
ax2.text(0.02, 0.95, "Rojo: exceso\nVerde: déficit", transform=ax2.transAxes,
         fontsize=8, verticalalignment="top",
         bbox=dict(boxstyle="round", facecolor="white", alpha=0.7))

plt.tight_layout()
st.pyplot(fig)

params_export = {
    "circuito": circuito_nombre, "shots": shots,
    "tvd": round(tvd_val, 4), "hellinger": round(hf_val, 4), "xeb": round(xeb_val, 4),
    "depolar_1q": p_depolar_1q, "depolar_2q": p_depolar_2q,
    "T1_us": T1_us if usar_t1t2 else None,
    "T2_us": T2_us if usar_t1t2 else None,
    "readout_err": p_readout if usar_readout else None,
}
export_figure_button(fig, f"simulador_{circuito_nombre[:5].replace(' ', '_')}", params_export)
plt.close(fig)

# ─── Análisis de ruido vs. shots ─────────────────────────────────────────────
with st.expander("Análisis: TVD vs. tasa de error (sweep)"):
    st.markdown(
        "Muestra cómo evoluciona la TVD al aumentar el error despolarizante de 1Q, "
        "manteniendo el resto de parámetros fijos."
    )
    p_sweep = np.linspace(0, 0.05, 30)
    tvd_sweep = []
    for p_val in p_sweep:
        nm_sw = NoiseModel()
        nm_sw.add_all_qubit_quantum_error(depolarizing_error(p_val, 1),
                                          ['h', 'x', 'rz', 'ry', 'rx', 'sx'])
        if p_val > 0:
            nm_sw.add_all_qubit_quantum_error(depolarizing_error(min(5*p_val, 0.5), 2),
                                              ['cx', 'cz'])
            nm_sw.add_all_qubit_quantum_error(depolarizing_error(min(15*p_val, 0.999), 3),
                                              ['ccx'])
        sim_sw = AerSimulator(noise_model=nm_sw)
        from qiskit.compiler import transpile as tp2
        qc_sw = tp2(qc_meas, sim_sw)
        counts_sw = sim_sw.run(qc_sw, shots=1024).result().get_counts()
        p_noisy_sw = np.array([counts_sw.get(lb, 0) / 1024 for lb in labels])
        tvd_sweep.append(tvd(probs_ideal, p_noisy_sw))

    fig2, ax3 = plt.subplots(figsize=(8, 3))
    ax3.plot(p_sweep * 100, tvd_sweep, 'o-', color='#8e44ad', lw=2, ms=5)
    ax3.axvline(p_depolar_1q * 100, color='red', linestyle='--', alpha=0.6,
                label=f"Configuración actual ({p_depolar_1q*100:.2f}%)")
    ax3.set_xlabel("Error despolarizante 1Q (%)")
    ax3.set_ylabel("TVD")
    ax3.set_title("TVD vs. tasa de error de puerta")
    ax3.legend(); ax3.grid(alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)
