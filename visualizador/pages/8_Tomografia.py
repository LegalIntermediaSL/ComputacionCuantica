"""Tomografía de estados cuánticos — reconstrucción de la matriz densidad."""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, DensityMatrix, SparsePauliOp

st.set_page_config(page_title="Tomografía de Estados", layout="wide")
st.title("Tomografía de estados cuánticos")
st.markdown(
    "La tomografía reconstruye la **matriz de densidad** ρ de un qubit midiendo en las "
    "tres bases de Pauli (X, Y, Z). Con ruido añadido se observa cómo la reconstrucción "
    "diverge del estado ideal."
)

# ─── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Estado a preparar")
    tipo_estado = st.selectbox(
        "Tipo de estado",
        ["|0⟩", "|1⟩", "|+⟩ (superposición X)", "|i⟩ (superposición Y)",
         "Estado de Bell |Φ+⟩", "Personalizado (θ, φ)"],
    )
    if "Personalizado" in tipo_estado:
        theta = st.slider("θ", 0.0, float(np.pi), float(np.pi/3), step=0.05)
        phi   = st.slider("φ", 0.0, float(2*np.pi), 0.0, step=0.05)
    else:
        theta, phi = 0.0, 0.0

    st.header("Ruido de medición")
    p_readout = st.slider("Error de readout p (flip 0↔1)", 0.0, 0.3, 0.0, step=0.01)
    shots = st.slider("Shots por base", 512, 8192, 2048, step=256)

# ─── Preparar estado de referencia ─────────────────────────────────────────
def make_state(tipo: str, th: float, ph: float):
    qc = QuantumCircuit(1)
    if tipo == "|0⟩":
        pass
    elif tipo == "|1⟩":
        qc.x(0)
    elif "|+⟩" in tipo:
        qc.h(0)
    elif "|i⟩" in tipo:
        qc.h(0); qc.s(0)
    elif "Personalizado" in tipo:
        qc.u(th, ph, 0, 0)
    return Statevector.from_instruction(qc)

is_bell = "Bell" in tipo_estado

if is_bell:
    qc_bell = QuantumCircuit(2)
    qc_bell.h(0); qc_bell.cx(0, 1)
    sv = Statevector.from_instruction(qc_bell)
    rho_ideal = DensityMatrix(sv)
    # Para visualización tomamos traza parcial del qubit 0
    rho_1q = DensityMatrix(sv).partial_trace([1])
    n_qubits = 2
else:
    sv = make_state(tipo_estado, theta, phi)
    rho_ideal = DensityMatrix(sv)
    rho_1q = rho_ideal
    n_qubits = 1

# ─── Tomografía simulada ────────────────────────────────────────────────────
def medicion_ruidosa(sv_state, base: str, shots_n: int, p_ro: float):
    """Simula medición en la base dada con error de readout."""
    # Convertir base: X → rotar con H, Y → rotar con Sdg H, Z → sin rotación
    qc_m = QuantumCircuit(1)
    if base == "X":
        qc_m.h(0)
    elif base == "Y":
        qc_m.sdg(0); qc_m.h(0)
    # Estado tras rotación
    sv_rot = sv_state.evolve(qc_m)
    prob_0 = abs(sv_rot[0])**2
    prob_1 = abs(sv_rot[1])**2

    # Añadir error de readout
    p0_efectivo = (1 - p_ro) * prob_0 + p_ro * prob_1
    p1_efectivo = (1 - p_ro) * prob_1 + p_ro * prob_0

    # Simular shots
    rng = np.random.default_rng(42)
    resultados = rng.choice([0, 1], size=shots_n, p=[p0_efectivo, p1_efectivo])
    n0 = np.sum(resultados == 0)
    n1 = shots_n - n0
    # <σ> = P(0) - P(1)
    return (n0 - n1) / shots_n

if not is_bell:
    sv_tomo = sv
else:
    # Para Bell: tomar primer qubit
    qc_q0 = QuantumCircuit(1)
    qc_q0.h(0)
    sv_tomo = Statevector.from_instruction(qc_q0)  # traza parcial → mezcla max

# Medir en X, Y, Z
x_meas = medicion_ruidosa(sv_tomo if not is_bell else Statevector([1/np.sqrt(2), 1/np.sqrt(2)]),
                          "X", shots, p_readout)
y_meas = medicion_ruidosa(sv_tomo if not is_bell else Statevector([1/np.sqrt(2), 1j/np.sqrt(2)]),
                          "Y", shots, p_readout)
z_meas = medicion_ruidosa(sv_tomo if not is_bell else Statevector([1/np.sqrt(2), 0]),
                          "Z", shots, p_readout)

if is_bell:
    # Traza parcial de Bell sobre qubit 0 → estado máximamente mixto
    x_meas = np.random.normal(0, 1/np.sqrt(shots))
    y_meas = np.random.normal(0, 1/np.sqrt(shots))
    z_meas = np.random.normal(0, 1/np.sqrt(shots))

# Reconstrucción: ρ = (I + rx·X + ry·Y + rz·Z) / 2
rx, ry, rz = x_meas, y_meas, z_meas
I  = np.eye(2)
Px = np.array([[0,1],[1,0]], dtype=complex)
Py = np.array([[0,-1j],[1j,0]], dtype=complex)
Pz = np.array([[1,0],[0,-1]], dtype=complex)

rho_tomo = (I + rx*Px + ry*Py + rz*Pz) / 2

# Proyectar al semidefinido positivo si el ruido lo saca fuera
eigvals, eigvecs = np.linalg.eigh(rho_tomo)
eigvals_clipped = np.clip(eigvals, 0, None)
if eigvals_clipped.sum() > 0:
    eigvals_clipped /= eigvals_clipped.sum()
rho_tomo_psd = eigvecs @ np.diag(eigvals_clipped) @ eigvecs.conj().T

# ─── Métricas ───────────────────────────────────────────────────────────────
rho_ref = rho_1q.data

def fidelidad_bures(rho1, rho2):
    sqrt1 = np.array([[np.sqrt(max(v,0)) if abs(v)>1e-12 else 0
                       for v in np.linalg.eigvalsh(rho1)]])
    from scipy.linalg import sqrtm
    sqrt_r1 = sqrtm(rho1)
    M = sqrt_r1 @ rho2 @ sqrt_r1
    return float(np.real(np.trace(sqrtm(M)))**2)

try:
    from scipy.linalg import sqrtm as _sqrtm
    F = fidelidad_bures(rho_ref, rho_tomo_psd)
except Exception:
    F = float(np.real(np.trace(rho_ref @ rho_tomo_psd)))

pureza_ideal = float(np.real(np.trace(rho_ref @ rho_ref)))
pureza_tomo  = float(np.real(np.trace(rho_tomo_psd @ rho_tomo_psd)))
r_bloch_tomo = np.array([rx, ry, rz])

# ─── Layout principal ────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

# ── Vector de Bloch ideal ───
with col1:
    st.subheader("Vector de Bloch ideal")
    if not is_bell:
        obs = {"X": SparsePauliOp("X"), "Y": SparsePauliOp("Y"), "Z": SparsePauliOp("Z")}
        r_ideal = np.array([float(sv.expectation_value(obs[k]).real) for k in ["X","Y","Z"]])
    else:
        r_ideal = np.zeros(3)
    from qiskit.visualization import plot_bloch_multivector
    try:
        fig_b = plot_bloch_multivector(rho_1q)
        st.pyplot(fig_b)
        plt.close()
    except Exception:
        st.info("Estado de Bell: qubit individual en mezcla máxima (centro de la esfera)")
    st.caption(f"r⃗ = ({r_ideal[0]:.3f}, {r_ideal[1]:.3f}, {r_ideal[2]:.3f})  |r⃗| = {np.linalg.norm(r_ideal):.3f}")

# ── Matriz densidad ideal (visual) ───
with col2:
    st.subheader("Matriz densidad ideal ρ")
    fig_m, axes = plt.subplots(1, 2, figsize=(6, 3))
    for ax, data, title in zip(axes,
                                [rho_ref.real, rho_ref.imag],
                                ["Re(ρ)", "Im(ρ)"]):
        im = ax.imshow(data, cmap="RdBu", vmin=-1, vmax=1)
        ax.set_xticks([0,1]); ax.set_yticks([0,1])
        ax.set_xticklabels(["|0⟩","|1⟩"]); ax.set_yticklabels(["⟨0|","⟨1|"])
        ax.set_title(title)
        for i in range(2):
            for j in range(2):
                ax.text(j, i, f"{data[i,j]:.2f}", ha="center", va="center",
                        fontsize=9, color="black" if abs(data[i,j]) < 0.5 else "white")
    plt.colorbar(im, ax=axes, fraction=0.04)
    plt.tight_layout()
    st.pyplot(fig_m); plt.close(fig_m)

# ── Matriz densidad reconstruida ───
with col3:
    st.subheader("ρ reconstruida (tomografía)")
    fig_t, axes_t = plt.subplots(1, 2, figsize=(6, 3))
    for ax, data, title in zip(axes_t,
                                [rho_tomo_psd.real, rho_tomo_psd.imag],
                                ["Re(ρ_tomo)", "Im(ρ_tomo)"]):
        im_t = ax.imshow(data, cmap="RdBu", vmin=-1, vmax=1)
        ax.set_xticks([0,1]); ax.set_yticks([0,1])
        ax.set_xticklabels(["|0⟩","|1⟩"]); ax.set_yticklabels(["⟨0|","⟨1|"])
        ax.set_title(title)
        for i in range(2):
            for j in range(2):
                ax.text(j, i, f"{data[i,j]:.2f}", ha="center", va="center",
                        fontsize=9, color="black" if abs(data[i,j]) < 0.5 else "white")
    plt.colorbar(im_t, ax=axes_t, fraction=0.04)
    plt.tight_layout()
    st.pyplot(fig_t); plt.close(fig_t)

# ─── Métricas en columnas ────────────────────────────────────────────────────
st.divider()
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Fidelidad F(ρ_ideal, ρ_tomo)", f"{F:.4f}")
m2.metric("Pureza ideal Tr(ρ²)", f"{pureza_ideal:.4f}")
m3.metric("Pureza tomografía Tr(ρ²)", f"{pureza_tomo:.4f}")
m4.metric("|r⃗| tomografía", f"{np.linalg.norm(r_bloch_tomo):.4f}")
m5.metric("Shots totales usados", f"{shots * 3:,}")

# ─── Gráfico de barras: valores esperados medidos ────────────────────────────
st.divider()
st.subheader("Valores esperados medidos en cada base")

if not is_bell:
    obs = {"X": SparsePauliOp("X"), "Y": SparsePauliOp("Y"), "Z": SparsePauliOp("Z")}
    r_ideal_plot = [float(sv.expectation_value(obs[k]).real) for k in ["X","Y","Z"]]
else:
    r_ideal_plot = [0.0, 0.0, 0.0]

bases = ["⟨X⟩", "⟨Y⟩", "⟨Z⟩"]
vals_ideal = r_ideal_plot
vals_tomo  = [rx, ry, rz]

fig_bar, ax_bar = plt.subplots(figsize=(8, 4))
x = np.arange(3)
w = 0.35
ax_bar.bar(x - w/2, vals_ideal, w, label="Ideal (analítico)", color="#3498db", alpha=0.85)
ax_bar.bar(x + w/2, vals_tomo,  w, label=f"Medido ({shots} shots/base)", color="#e74c3c", alpha=0.85)
ax_bar.set_xticks(x); ax_bar.set_xticklabels(bases, fontsize=13)
ax_bar.set_ylabel("Valor esperado ⟨σ⟩")
ax_bar.set_ylim(-1.15, 1.15)
ax_bar.axhline(y=0, color="gray", alpha=0.3)
ax_bar.set_title("Comparativa ideal vs. medición tomográfica")
ax_bar.legend()
ax_bar.grid(axis="y", alpha=0.3)
st.pyplot(fig_bar); plt.close(fig_bar)

# ─── Visualización 3D del vector de Bloch tomografíado ──────────────────────
st.divider()
st.subheader("Vector de Bloch: ideal vs. reconstruido")

fig_3d = plt.figure(figsize=(6, 6))
ax3d = fig_3d.add_subplot(111, projection="3d")

# Esfera
u = np.linspace(0, 2*np.pi, 40)
v = np.linspace(0, np.pi, 40)
ax3d.plot_surface(
    np.outer(np.cos(u), np.sin(v)),
    np.outer(np.sin(u), np.sin(v)),
    np.outer(np.ones(40), np.cos(v)),
    alpha=0.07, color="steelblue",
)
circle = np.linspace(0, 2*np.pi, 100)
ax3d.plot(np.cos(circle), np.sin(circle), 0, "k-", alpha=0.12, linewidth=0.8)
ax3d.plot(np.cos(circle), np.zeros(100), np.sin(circle), "k-", alpha=0.12, linewidth=0.8)
ax3d.plot(np.zeros(100), np.cos(circle), np.sin(circle), "k-", alpha=0.12, linewidth=0.8)

for vec, lbl in [([1,0,0],"X"), ([0,1,0],"Y"), ([0,0,1],"Z")]:
    ax3d.quiver(0,0,0,*vec, length=1.15, color="gray", alpha=0.35, linewidth=0.8)
    ax3d.text(vec[0]*1.28, vec[1]*1.28, vec[2]*1.28, lbl, fontsize=9, color="gray")
ax3d.text(0, 0,  1.18, "|0⟩", fontsize=9, ha="center", color="#333")
ax3d.text(0, 0, -1.28, "|1⟩", fontsize=9, ha="center", color="#333")

# Vector ideal
ri = r_ideal if not is_bell else np.zeros(3)
if np.linalg.norm(ri) > 0.01:
    ax3d.quiver(0,0,0, ri[0],ri[1],ri[2], color="#3498db", linewidth=2.5,
                arrow_length_ratio=0.15, label="Ideal")

# Vector tomografíado
rt = r_bloch_tomo
if np.linalg.norm(rt) > 0.01:
    ax3d.quiver(0,0,0, rt[0],rt[1],rt[2], color="#e74c3c", linewidth=2.5,
                arrow_length_ratio=0.15, label="Tomografía")

ax3d.set_xlim(-1.2, 1.2); ax3d.set_ylim(-1.2, 1.2); ax3d.set_zlim(-1.2, 1.2)
ax3d.set_box_aspect([1,1,1])
ax3d.set_title("Esfera de Bloch", fontsize=10)
ax3d.legend(loc="upper left", fontsize=8)
ax3d.axis("off")
st.pyplot(fig_3d); plt.close(fig_3d)

# ─── Teoría expandible ───────────────────────────────────────────────────────
with st.expander("Fundamento teórico de la tomografía"):
    st.markdown(r"""
    **Representación de Bloch:**
    $$\rho = \frac{1}{2}(I + r_x X + r_y Y + r_z Z), \quad r_i = \langle \sigma_i \rangle = \text{Tr}(\sigma_i \rho)$$

    **Protocolo de tomografía:**
    1. Preparar el estado ρ repetidamente.
    2. Medir en base Z (sin rotación) → estimar $\langle Z \rangle$.
    3. Medir en base X (aplicar H antes) → estimar $\langle X \rangle$.
    4. Medir en base Y (aplicar Sdg·H antes) → estimar $\langle Y \rangle$.
    5. Reconstruir: $r_i = \langle \sigma_i \rangle$.

    **Error estadístico:** Con $N$ shots por base, $\delta r_i \sim 1/\sqrt{N}$.

    **Proyección al semidefinido positivo:** el ruido puede producir $r_x^2+r_y^2+r_z^2 > 1$
    (no físico). Se corrige proyectando los autovalores negativos de $\rho$ a cero y renormalizando.

    **Fidelidad de Bures:**
    $$F(\rho, \sigma) = \left[\text{Tr}\sqrt{\sqrt{\rho}\,\sigma\,\sqrt{\rho}}\right]^2$$
    """)

st.caption("Tutorial: módulos 17_medicion_avanzada_y_observables y 19_tomografia_y_caracterizacion")
