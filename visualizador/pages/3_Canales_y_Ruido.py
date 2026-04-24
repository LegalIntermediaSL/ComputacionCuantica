"""Comparador de modelos de ruido: contracción de la esfera de Bloch."""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from qiskit.quantum_info import DensityMatrix

st.set_page_config(page_title="Canales y Ruido", layout="wide")
st.title("Modelos de ruido: contracción de la esfera de Bloch")
st.markdown(
    "Cada canal cuántico actúa sobre el vector de Bloch $\\vec{r} = (x, y, z)$ "
    "contrayéndolo de forma característica. Compara hasta 4 canales simultáneamente."
)


def apply_channel(rho: np.ndarray, canal: str, p: float) -> np.ndarray:
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    I = np.eye(2, dtype=complex)

    if canal == "Ninguno":
        return rho
    elif canal == "Despolarizante":
        return (1 - p) * rho + (p / 3) * (X @ rho @ X + Y @ rho @ Y + Z @ rho @ Z)
    elif canal == "Bit-flip":
        return (1 - p) * rho + p * (X @ rho @ X)
    elif canal == "Phase-flip":
        return (1 - p) * rho + p * (Z @ rho @ Z)
    elif canal == "Bit-phase-flip":
        return (1 - p) * rho + p * (Y @ rho @ Y)
    elif canal == "Amplitud damping":
        K0 = np.array([[1, 0], [0, np.sqrt(1 - p)]])
        K1 = np.array([[0, np.sqrt(p)], [0, 0]])
        return K0 @ rho @ K0.conj().T + K1 @ rho @ K1.conj().T
    elif canal == "Phase damping":
        K0 = np.array([[1, 0], [0, np.sqrt(1 - p)]])
        K1 = np.array([[0, 0], [0, np.sqrt(p)]])
        return K0 @ rho @ K0.conj().T + K1 @ rho @ K1.conj().T
    return rho


def bloch_vector(rho: np.ndarray):
    return np.array([
        2 * rho[0, 1].real,
        2 * rho[0, 1].imag,
        (rho[0, 0] - rho[1, 1]).real,
    ])


CANALES = ["Ninguno", "Despolarizante", "Bit-flip", "Phase-flip",
           "Bit-phase-flip", "Amplitud damping", "Phase damping"]

COLORES = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12"]

with st.sidebar:
    st.header("Configuración")
    theta = st.slider("θ estado inicial", 0.0, float(np.pi), np.pi / 4, step=0.05)
    phi   = st.slider("φ estado inicial", 0.0, float(2 * np.pi), 0.0, step=0.05)

    st.subheader("Canal 1")
    c1 = st.selectbox("Canal 1", CANALES, index=1, key="c1")
    p1 = st.slider("p₁", 0.0, 1.0, 0.0, key="p1")

    st.subheader("Canal 2")
    c2 = st.selectbox("Canal 2", CANALES, index=6, key="c2")
    p2 = st.slider("p₂", 0.0, 1.0, 0.0, key="p2")

    st.subheader("Canal 3")
    c3 = st.selectbox("Canal 3", CANALES, index=5, key="c3")
    p3 = st.slider("p₃", 0.0, 1.0, 0.0, key="p3")

    rango_p = st.slider("Rango p para curvas", 0.0, 1.0, (0.0, 1.0), step=0.05)

# Estado inicial
alpha = np.cos(theta / 2)
beta  = np.sin(theta / 2) * np.exp(1j * phi)
sv    = np.array([alpha, beta])
rho0  = np.outer(sv, sv.conj())
r0    = bloch_vector(rho0)

channels_to_plot = [(c1, p1, COLORES[1]), (c2, p2, COLORES[2]), (c3, p3, COLORES[3])]

# ─── Tabla de fidelidades ───
st.subheader("Fidelidades y normas del vector de Bloch")

rows = []
for nombre, p, _ in channels_to_plot:
    rho_out = apply_channel(rho0, nombre, p)
    r_out   = bloch_vector(rho_out)
    rho_sqrt = np.linalg.matrix_power(rho0, 1)  # aproximación
    F = float(np.abs(np.sqrt(np.sqrt(rho0)) @ rho_out @ np.sqrt(rho0)).trace() ** 2)
    pureza  = float(np.trace(rho_out @ rho_out).real)
    norm    = float(np.linalg.norm(r_out))
    rows.append({
        "Canal": nombre,
        "p": f"{p:.2f}",
        "|r⃗|": f"{norm:.4f}",
        "Pureza": f"{pureza:.4f}",
    })

import pandas as pd
st.dataframe(pd.DataFrame(rows), use_container_width=True)

# ─── Curvas de contracción vs p ───
st.subheader("Contracción del vector de Bloch en función de p")

p_vals = np.linspace(rango_p[0], rango_p[1], 100)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

for nombre, _, color in channels_to_plot:
    if nombre == "Ninguno":
        continue
    norms = []
    fids  = []
    for pv in p_vals:
        rho_out = apply_channel(rho0, nombre, pv)
        norms.append(np.linalg.norm(bloch_vector(rho_out)))
        rho_sq  = np.sqrt(np.abs(rho0))
        fid_val = np.abs(np.trace(
            np.linalg.matrix_power(
                rho_sq @ rho_out @ rho_sq, 1
            )
        ))
        fids.append(np.trace(rho_out @ rho_out).real)
    axes[0].plot(p_vals, norms, color=color, label=nombre)
    axes[1].plot(p_vals, fids, color=color, label=nombre)

axes[0].set_xlabel("p")
axes[0].set_ylabel("|r⃗|")
axes[0].set_title("Norma del vector de Bloch")
axes[0].legend()
axes[0].set_ylim(0, 1.05)

axes[1].set_xlabel("p")
axes[1].set_ylabel("Tr(ρ²)")
axes[1].set_title("Pureza del estado")
axes[1].legend()
axes[1].set_ylim(0, 1.05)

st.pyplot(fig)

# ─── Descripción analítica ───
with st.expander("Descripción analítica de cada canal"):
    st.markdown(
        r"""
        | Canal | Acción sobre el vector de Bloch $\vec{r}=(x,y,z)$ |
        |---|---|
        | Despolarizante | $\vec{r} \to (1-\frac{4p}{3})\vec{r}$ (contracción isotrópica) |
        | Bit-flip | $x \to x$, $y \to (1-2p)y$, $z \to (1-2p)z$ |
        | Phase-flip | $x \to (1-2p)x$, $y \to (1-2p)y$, $z \to z$ |
        | Bit-phase-flip | $x \to (1-2p)x$, $y \to y$, $z \to (1-2p)z$ |
        | Amplitud damping | $x \to \sqrt{1-p}\,x$, $y \to \sqrt{1-p}\,y$, $z \to (1-p)z + p$ |
        | Phase damping | $x \to \sqrt{1-p}\,x$, $y \to \sqrt{1-p}\,y$, $z \to z$ |
        """
    )

st.caption("Tutorial: módulos 16_canales_cuanticos_y_ruido y 21_open_quantum_systems")
