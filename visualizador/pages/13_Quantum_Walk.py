"""
Página 13 — Quantum Walk Interactivo
Visualiza DTQW (discreto) y CTQW (continuo) con controles en tiempo real.
Compara propagación balística cuántica vs difusión clásica.
"""

import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from tour_guide import show_tour, export_figure_button

st.set_page_config(page_title="Quantum Walk Interactivo", layout="wide")
st.title("🚶 Quantum Walk Interactivo")
st.markdown(
    "Explora la **propagación cuántica** en una línea y compárala con el random walk clásico. "
    "El quantum walk es **balístico** (σ ∝ t) vs el clásico **difusivo** (σ ∝ √t)."
)

_TOUR_STEPS = [
    {"title": "🚶 Quantum Walk", "body": "El quantum walk discreto (DTQW) usa un 'qubit moneda' para decidir la dirección. La interferencia cuántica produce una distribución bimodal muy diferente al random walk clásico."},
    {"title": "🎲 Tipo de moneda", "body": "La moneda cuántica es una puerta unitaria 2×2. Hadamard produce distribución simétrica bimodal. Y (Pauli-Y) produce distribución asimétrica. Grover minimiza la reflexión."},
    {"title": "🕐 Pasos de tiempo", "body": "Controla cuántos pasos da el walker. El ancho σ crece como t/√2 (balístico) vs √t del clásico. A t=50 pasos, el cuántico es ≈7× más ancho."},
    {"title": "📊 Comparativa balístico vs difusivo", "body": "El gráfico σ(t) muestra el crecimiento de la desviación estándar. La línea cuántica (σ≈t/√2) supera siempre a la clásica (σ≈√t)."},
    {"title": "🌊 Continuos (CTQW)", "body": "El quantum walk continuo evoluciona como e^{-iAt} donde A es la matriz de adyacencia. No necesita moneda — la interferencia surge de la dinámica hamiltoniana."},
    {"title": "🖼️ Exportar", "body": "Descarga la distribución como PNG para incluirla en reportes."},
]
show_tour("quantum_walk", _TOUR_STEPS)

# ─────────────────────────────────────────────────────────────────────────────
# Controles laterales
# ─────────────────────────────────────────────────────────────────────────────
st.sidebar.header("⚙️ Configuración")

modo = st.sidebar.radio("Tipo de walk", ["DTQW (discreto)", "CTQW (continuo)"])

N = st.sidebar.slider("Tamaño de la línea (nodos)", 40, 300, 120, step=20)
T = st.sidebar.slider("Pasos / tiempo", 5, 80, 40)

moneda_nombre = st.sidebar.selectbox(
    "Moneda cuántica (solo DTQW)",
    ["Hadamard", "Pauli-Y", "Grover (2×2)", "DFT"],
    disabled=(modo == "CTQW (continuo)")
)

estado_inicial = st.sidebar.selectbox(
    "Estado inicial",
    ["|0⟩ (sesgado izquierda)", "i|1⟩ (sesgado derecha)", "(|0⟩+i|1⟩)/√2 (simétrico)"]
)

mostrar_clasico = st.sidebar.checkbox("Superponer random walk clásico", value=True)
mostrar_sigma = st.sidebar.checkbox("Mostrar evolución de σ(t)", value=True)

# ─────────────────────────────────────────────────────────────────────────────
# Monedas cuánticas
# ─────────────────────────────────────────────────────────────────────────────
def get_coin(nombre: str) -> np.ndarray:
    if nombre == "Hadamard":
        return np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    elif nombre == "Pauli-Y":
        return np.array([[0, -1j], [1j, 0]])
    elif nombre == "Grover (2×2)":
        return np.array([[-1, 2], [2, -1]]) / np.sqrt(5) * np.sqrt(5/5)  # Grover 2D
    else:  # DFT
        return np.array([[1, 1], [1, -1]]) / np.sqrt(2) * np.exp(1j * np.pi / 4)

def get_initial_coin(nombre: str) -> np.ndarray:
    if "|0⟩" in nombre:
        return np.array([1.0, 0.0], dtype=complex)
    elif "i|1⟩" in nombre:
        return np.array([0.0, 1j], dtype=complex)
    else:
        return np.array([1.0, 1j], dtype=complex) / np.sqrt(2)

# ─────────────────────────────────────────────────────────────────────────────
# DTQW
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def run_dtqw(N: int, T: int, coin_name: str, init_coin: tuple) -> tuple:
    """Devuelve (probs_final, sigma_t, probs_clasico)."""
    C = get_coin(coin_name)
    c0 = np.array(init_coin, dtype=complex)

    x0 = N // 2
    psi = np.zeros(2 * N, dtype=complex)
    psi[2 * x0]     = c0[0]
    psi[2 * x0 + 1] = c0[1]
    psi /= np.linalg.norm(psi)

    pos = np.arange(N) - x0
    sigma_vals = []

    for _ in range(T):
        psi_new = np.zeros(2 * N, dtype=complex)
        for x in range(N):
            after = C @ psi[2*x:2*x+2]
            psi_new[2*((x+1) % N)]     += after[0]
            psi_new[2*((x-1) % N) + 1] += after[1]
        psi = psi_new
        probs = np.array([abs(psi[2*x])**2 + abs(psi[2*x+1])**2 for x in range(N)])
        mean = np.sum(probs * pos)
        sigma_vals.append(float(np.sqrt(np.sum(probs * pos**2) - mean**2)))

    probs_final = np.array([abs(psi[2*x])**2 + abs(psi[2*x+1])**2 for x in range(N)])

    # Clásico: distribución binomial centrada
    p_clasico = np.zeros(N)
    from scipy.stats import binom
    for xi, xval in enumerate(pos):
        k = xval + T
        if 0 <= k <= 2 * T and k % 2 == T % 2:
            p_clasico[xi] = binom.pmf(k // 2, T, 0.5) * (2 if k != 0 else 1)
    norm_c = p_clasico.sum()
    if norm_c > 0:
        p_clasico /= norm_c

    return probs_final, sigma_vals, p_clasico, pos.tolist()

# ─────────────────────────────────────────────────────────────────────────────
# CTQW
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def run_ctqw(N: int, T: int) -> tuple:
    """CTQW en línea con condiciones periódicas."""
    A = np.zeros((N, N))
    for i in range(N - 1):
        A[i, i+1] = A[i+1, i] = 1.0
    A[0, N-1] = A[N-1, 0] = 1.0  # periódico

    eigvals, eigvecs = np.linalg.eigh(A)
    x0 = N // 2
    pos = np.arange(N) - x0

    psi0 = np.zeros(N, dtype=complex)
    psi0[x0] = 1.0

    snapshots = []
    sigma_vals = []
    t_snap = max(1, T // 5)

    for t in range(1, T + 1):
        coeffs = eigvecs.conj().T @ psi0
        psi_t = eigvecs @ (coeffs * np.exp(-1j * eigvals * t))
        probs = np.abs(psi_t) ** 2
        mean = np.sum(probs * pos)
        sigma_vals.append(float(np.sqrt(np.sum(probs * pos**2) - mean**2)))
        if t % t_snap == 0:
            snapshots.append((t, probs.tolist()))

    return snapshots, sigma_vals, pos.tolist()

# ─────────────────────────────────────────────────────────────────────────────
# Ejecución y gráficas
# ─────────────────────────────────────────────────────────────────────────────
init_tuple = tuple(get_initial_coin(estado_inicial).tolist())

if modo == "DTQW (discreto)":
    with st.spinner("Simulando DTQW…"):
        probs, sigma_t, p_clasico, pos = run_dtqw(N, T, moneda_nombre, init_tuple)
    pos = np.array(pos)

    # ── Figura principal: distribución
    fig, axes = plt.subplots(1, 2 if mostrar_sigma else 1, figsize=(13 if mostrar_sigma else 7, 5))
    if not mostrar_sigma:
        axes = [axes]

    ax0 = axes[0]
    ax0.bar(pos, probs, width=1.0, color='royalblue', alpha=0.75, label=f'DTQW ({moneda_nombre})')
    if mostrar_clasico:
        ax0.plot(pos, p_clasico, 'r--', lw=1.5, label='Random walk clásico')
    ax0.set_xlabel("Posición")
    ax0.set_ylabel("Probabilidad")
    ax0.set_title(f"DTQW t={T} · N={N} nodos")
    ax0.legend(fontsize=9)
    ax0.set_xlim(-N//2, N//2)
    ax0.grid(alpha=0.25)

    if mostrar_sigma:
        ax1 = axes[1]
        t_arr = np.arange(1, T + 1)
        ax1.plot(t_arr, sigma_t, 'b-o', ms=3, lw=1.8, label='σ DTQW (balístico)')
        ax1.plot(t_arr, t_arr / np.sqrt(2), 'b--', lw=1, alpha=0.5, label='t/√2 (teórico)')
        if mostrar_clasico:
            ax1.plot(t_arr, np.sqrt(t_arr), 'r-s', ms=3, lw=1.8, label='σ clásico (√t)')
        ax1.set_xlabel("Tiempo t")
        ax1.set_ylabel("Desviación estándar σ(t)")
        ax1.set_title("Crecimiento balístico vs difusivo")
        ax1.legend(fontsize=9)
        ax1.grid(alpha=0.25)

    plt.tight_layout()
    st.pyplot(fig)
    export_figure_button(fig, "dtqw_distribucion.png")

    # Métricas
    c1, c2, c3 = st.columns(3)
    sigma_final = sigma_t[-1]
    sigma_clasico = np.sqrt(T)
    c1.metric("σ cuántico (t)", f"{sigma_final:.1f}")
    c2.metric("σ clásico (√t)", f"{sigma_clasico:.1f}")
    c3.metric("Ventaja balística", f"{sigma_final/sigma_clasico:.2f}×")

else:  # CTQW
    with st.spinner("Simulando CTQW…"):
        snapshots, sigma_t, pos = run_ctqw(N, T)
    pos = np.array(pos)

    fig, axes = plt.subplots(1, 2 if mostrar_sigma else 1, figsize=(13 if mostrar_sigma else 7, 5))
    if not mostrar_sigma:
        axes = [axes]

    ax0 = axes[0]
    cmap = plt.cm.Blues
    for i, (t_snap, probs) in enumerate(snapshots):
        color = cmap(0.3 + 0.7 * i / max(len(snapshots) - 1, 1))
        ax0.plot(pos, probs, lw=1.5, color=color, label=f"t={t_snap}")
    ax0.set_xlabel("Posición")
    ax0.set_ylabel("Probabilidad")
    ax0.set_title(f"CTQW en línea circular N={N}")
    ax0.legend(fontsize=8)
    ax0.grid(alpha=0.25)

    if mostrar_sigma:
        ax1 = axes[1]
        t_arr = np.arange(1, T + 1)
        ax1.plot(t_arr, sigma_t, 'g-o', ms=3, lw=1.8, label='σ CTQW')
        if mostrar_clasico:
            ax1.plot(t_arr, np.sqrt(t_arr), 'r-s', ms=3, lw=1.8, label='σ clásico (√t)')
        ax1.set_xlabel("Tiempo t"); ax1.set_ylabel("σ(t)")
        ax1.set_title("Crecimiento σ — CTQW")
        ax1.legend(fontsize=9); ax1.grid(alpha=0.25)

    plt.tight_layout()
    st.pyplot(fig)
    export_figure_button(fig, "ctqw_distribucion.png")

    c1, c2 = st.columns(2)
    c1.metric("σ CTQW final", f"{sigma_t[-1]:.1f}")
    c2.metric("σ clásico (√t)", f"{np.sqrt(T):.1f}")

# ─────────────────────────────────────────────────────────────────────────────
# Sección educativa
# ─────────────────────────────────────────────────────────────────────────────
with st.expander("📚 Teoría: ¿por qué es balístico?"):
    st.markdown(r"""
**Random walk cuántico discreto (DTQW)**

El walker tiene estado $|\psi\rangle = \sum_x (a_x|x,\uparrow\rangle + b_x|x,\downarrow\rangle)$.
En cada paso aplica la moneda $C$ y luego el shift condicional:
$$S|\uparrow\rangle|x\rangle = |\uparrow\rangle|x+1\rangle, \quad S|\downarrow\rangle|x\rangle = |\downarrow\rangle|x-1\rangle$$

La **interferencia cuántica** entre ramas hace que la varianza crezca como:
$$\sigma^2(t) \approx \frac{t^2}{2} \quad \Rightarrow \quad \sigma(t) \approx \frac{t}{\sqrt{2}}$$

vs el clásico $\sigma(t) = \sqrt{t}$. Para $t=50$: cuántico $\approx 35$, clásico $\approx 7$.

**Random walk cuántico continuo (CTQW)**

El CTQW en grafo $G$ evoluciona como $|\psi(t)\rangle = e^{-iAt}|\psi(0)\rangle$ donde $A$ es la matriz de adyacencia. Los autovectores de $A$ se propagan con fase $e^{-i\lambda_k t}$, creando interferencias que también producen propagación balística en líneas y mallas.

**Aplicaciones:**
- **Búsqueda cuántica**: Childs et al. (2003) — CTQW en K_N encuentra el elemento marcado en $O(\sqrt{N})$
- **Algoritmos de grafos**: transitividad, bipartismo en $O(\sqrt{n})$ pasos
- **Transporte cuántico**: eficiencia en redes biológicas (fotosíntesis)
""")
