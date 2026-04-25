"""Esfera de Bloch e impacto del ruido — página original mejorada."""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, DensityMatrix, SparsePauliOp
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

    st.header("Trayectoria")
    modo_trayectoria = st.selectbox(
        "Animar barriendo",
        ["Ninguna", "θ (latitud, 0 → actual)", "φ (longitud, 0 → actual)",
         "Espiral θ+φ", "Ruido creciente (p: 0 → actual)"],
    )
    n_frames = st.slider("Puntos de trayectoria", 10, 80, 40)

# --- Estado ideal ---
qc = QuantumCircuit(1)
qc.u(theta, phi, 0, 0)
sv_ideal = Statevector.from_instruction(qc)
rho_ideal = DensityMatrix(sv_ideal)

# Bloch vector ideal
r_ideal = np.array([
    sv_ideal.expectation_value(SparsePauliOp("X")).real,
    sv_ideal.expectation_value(SparsePauliOp("Y")).real,
    sv_ideal.expectation_value(SparsePauliOp("Z")).real,
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

# --- Trayectoria 3D ---
st.divider()
st.subheader("Trayectoria del vector de Bloch")

def bloch_point(th, ph):
    return np.array([np.sin(th)*np.cos(ph), np.sin(th)*np.sin(ph), np.cos(th)])

def apply_noise_to_point(th, ph, canal_n, p_n):
    r = bloch_point(th, ph)
    if canal_n == "Despolarizante":
        return r * (1 - 4*p_n/3)
    elif canal_n == "Amortiguamiento de amplitud":
        return np.array([r[0]*np.sqrt(1-p_n), r[1]*np.sqrt(1-p_n), r[2]*(1-p_n) + p_n])
    elif canal_n == "Desfase puro":
        return np.array([r[0]*np.sqrt(1-p_n), r[1]*np.sqrt(1-p_n), r[2]])
    return r

if modo_trayectoria == "Ninguna":
    st.info("Selecciona un modo de trayectoria en la barra lateral para visualizarla.")
else:
    # Generar puntos de la trayectoria
    t_vals = np.linspace(0, 1, n_frames)
    if modo_trayectoria == "θ (latitud, 0 → actual)":
        puntos = [bloch_point(theta * t, phi) for t in t_vals]
    elif modo_trayectoria == "φ (longitud, 0 → actual)":
        puntos = [bloch_point(theta, phi * t) for t in t_vals]
    elif modo_trayectoria == "Espiral θ+φ":
        puntos = [bloch_point(theta * t, phi * t) for t in t_vals]
    else:  # Ruido creciente
        puntos = [apply_noise_to_point(theta, phi, canal, p_ruido * t) for t in t_vals]

    puntos = np.array(puntos)
    xs, ys, zs = puntos[:, 0], puntos[:, 1], puntos[:, 2]

    # Dibujar esfera de Bloch 3D con trayectoria
    fig_traj = plt.figure(figsize=(6, 6))
    ax = fig_traj.add_subplot(111, projection="3d")

    # Esfera semitransparente
    u = np.linspace(0, 2*np.pi, 40)
    v = np.linspace(0, np.pi, 40)
    ax.plot_surface(
        np.outer(np.cos(u), np.sin(v)),
        np.outer(np.sin(u), np.sin(v)),
        np.outer(np.ones(40), np.cos(v)),
        alpha=0.08, color="steelblue",
    )
    # Círculos de referencia (ecuador y meridianos)
    circle = np.linspace(0, 2*np.pi, 100)
    ax.plot(np.cos(circle), np.sin(circle), 0, "k-", alpha=0.15, linewidth=0.8)
    ax.plot(np.cos(circle), np.zeros(100), np.sin(circle), "k-", alpha=0.15, linewidth=0.8)
    ax.plot(np.zeros(100), np.cos(circle), np.sin(circle), "k-", alpha=0.15, linewidth=0.8)

    # Ejes
    for vec, lbl in [([1,0,0],"X"), ([0,1,0],"Y"), ([0,0,1],"Z")]:
        ax.quiver(0,0,0,*vec, length=1.15, color="gray", alpha=0.4, linewidth=0.8)
        ax.text(vec[0]*1.25, vec[1]*1.25, vec[2]*1.25, lbl, fontsize=9, color="gray")

    # Polos
    ax.text(0, 0,  1.15, "|0⟩", fontsize=9, ha="center", color="#333")
    ax.text(0, 0, -1.25, "|1⟩", fontsize=9, ha="center", color="#333")

    # Trayectoria con gradiente de color
    for i in range(len(xs)-1):
        alpha = 0.3 + 0.7 * i / len(xs)
        ax.plot(xs[i:i+2], ys[i:i+2], zs[i:i+2],
                color=plt.cm.plasma(i / len(xs)), linewidth=2, alpha=alpha)

    # Punto inicial, final y vector actual
    ax.scatter(*puntos[0],  color="#3498db", s=60, zorder=5, label="Inicio")
    ax.scatter(*puntos[-1], color="#e74c3c", s=80, zorder=5, label="Fin")
    ax.quiver(0,0,0, r_ideal[0], r_ideal[1], r_ideal[2],
              color="#e74c3c", linewidth=2, arrow_length_ratio=0.15)

    ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2); ax.set_zlim(-1.2, 1.2)
    ax.set_box_aspect([1,1,1])
    ax.set_title(f"Trayectoria: {modo_trayectoria}", fontsize=10)
    ax.legend(loc="upper left", fontsize=8)
    ax.axis("off")

    col_traj, col_traj_info = st.columns([1, 1])
    with col_traj:
        st.pyplot(fig_traj)
        plt.close(fig_traj)
    with col_traj_info:
        st.markdown(f"""
        **Modo:** {modo_trayectoria}
        - **Puntos:** {n_frames}
        - **Inicio:** ({xs[0]:.3f}, {ys[0]:.3f}, {zs[0]:.3f})
        - **Fin:** ({xs[-1]:.3f}, {ys[-1]:.3f}, {zs[-1]:.3f})
        - **|r| inicio:** {np.linalg.norm(puntos[0]):.4f}
        - **|r| fin:** {np.linalg.norm(puntos[-1]):.4f}

        La barra de color (azul → amarillo → rojo) indica el progreso de la trayectoria.
        """)

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
