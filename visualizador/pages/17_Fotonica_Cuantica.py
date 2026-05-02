"""
Página 17 — Computación Cuántica Fotónica
Función de Wigner, Boson Sampling, Squeezing y Código GKP.
"""
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import eval_genlaguerre
import warnings
warnings.filterwarnings('ignore')

from tour_guide import show_tour, export_figure_button

st.set_page_config(page_title="Computación Fotónica", layout="wide")
st.title("🔬 Computación Cuántica Fotónica")
st.markdown(
    "Explora los estados cuánticos de la luz, el Boson Sampling y la corrección de errores fotónica "
    "mediante la función de Wigner, el squeezing y el código GKP."
)

_TOUR_STEPS = [
    {"title": "🔬 Fotónica Cuántica", "body": "Esta página cubre los conceptos fundamentales de la computación cuántica fotónica: estados de la luz, boson sampling, squeezing y el código GKP."},
    {"title": "📊 Función de Wigner", "body": "La función de Wigner W(x,p) es la representación cuasi-probabilística de un estado cuántico. Sus valores negativos (en rojo) son una firma de no-clasicidad."},
    {"title": "🎰 Boson Sampling", "body": "Las probabilidades del Boson Sampling son proporcionales al |Perm(U)|². El permanente es #P-duro, lo que hace este problema intractable para computadores clásicos con muchos fotones."},
    {"title": "〰 Squeezing", "body": "El squeezing comprime la varianza en una cuadratura a expensas de la otra, manteniendo el principio de Heisenberg. Un squeezing > 10 dB es necesario para el código GKP tolerante a fallos."},
    {"title": "🛡 Código GKP", "body": "El código GKP codifica un qubit lógico en el oscilador armónico. Corrige errores de desplazamiento |δx| < √π/2 ≈ 0.89. Los estados lógicos son peines de gaussianas con periodo 2√π."},
]
show_tour("fotonica_cuantica", _TOUR_STEPS)

# ── Función de Wigner ────────────────────────────────────────────────────────
st.subheader("1. Función de Wigner")

col1, col2 = st.columns([1, 3])
with col1:
    state_type = st.selectbox(
        "Estado cuántico",
        ["Vacío |0⟩", "1 fotón |1⟩", "2 fotones |2⟩", "3 fotones |3⟩",
         "Coherente |α⟩", "Squeezed S(r)|0⟩"],
    )
    if state_type == "Coherente |α⟩":
        alpha_re = st.slider("Re(α)", -3.0, 3.0, 2.0, 0.1)
        alpha_im = st.slider("Im(α)", -3.0, 3.0, 0.0, 0.1)
    elif state_type == "Squeezed S(r)|0⟩":
        r_sq = st.slider("Squeezing r", 0.0, 2.0, 1.0, 0.05)
        st.info(f"Squeezing: {8.686*r_sq:.1f} dB")

with col2:
    N = 150
    xv = np.linspace(-4, 4, N)
    pv = np.linspace(-4, 4, N)
    Xg, Pg = np.meshgrid(xv, pv)

    if state_type.startswith("Vacío"):
        n_fock = 0
        W = ((-1)**n_fock / np.pi) * np.exp(-2*(Xg**2+Pg**2)) * eval_genlaguerre(n_fock, 0, 4*(Xg**2+Pg**2))
        title = "|0⟩ — Estado de Vacío"
    elif "1 fotón" in state_type:
        n_fock = 1
        r2 = 2*(Xg**2+Pg**2)
        W = ((-1)**n_fock / np.pi) * np.exp(-r2) * eval_genlaguerre(n_fock, 0, 2*r2)
        title = "|1⟩ — 1 Fotón"
    elif "2 fotones" in state_type:
        n_fock = 2
        r2 = 2*(Xg**2+Pg**2)
        W = ((-1)**n_fock / np.pi) * np.exp(-r2) * eval_genlaguerre(n_fock, 0, 2*r2)
        title = "|2⟩ — 2 Fotones"
    elif "3 fotones" in state_type:
        n_fock = 3
        r2 = 2*(Xg**2+Pg**2)
        W = ((-1)**n_fock / np.pi) * np.exp(-r2) * eval_genlaguerre(n_fock, 0, 2*r2)
        title = "|3⟩ — 3 Fotones"
    elif "Coherente" in state_type:
        alpha = alpha_re + 1j*alpha_im
        W = (1/np.pi) * np.exp(-2*((Xg - alpha.real)**2 + (Pg - alpha.imag)**2))
        title = f"|α={alpha_re:.1f}+{alpha_im:.1f}i⟩ — Estado Coherente"
    else:
        r_val = r_sq
        W = (1/np.pi) * np.exp(-2*(Xg**2 * np.exp(2*r_val) + Pg**2 * np.exp(-2*r_val)))
        title = f"S(r={r_sq:.2f})|0⟩ — Estado Squeezed ({8.686*r_sq:.1f} dB)"

    fig, ax = plt.subplots(figsize=(5, 4))
    vmax = max(abs(W.min()), abs(W.max()), 1e-9)
    im = ax.pcolormesh(Xg, Pg, W, cmap='RdBu', vmin=-vmax, vmax=vmax, shading='auto')
    plt.colorbar(im, ax=ax, label="W(x,p)")
    ax.set_xlabel("x (cuadratura)"); ax.set_ylabel("p (cuadratura)")
    ax.set_title(title, fontsize=10)
    if W.min() < -1e-6:
        ax.text(0.03, 0.93, "W < 0 : no clásico", transform=ax.transAxes,
                fontsize=9, color='red', fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    st.pyplot(fig)
    plt.close(fig)
    export_figure_button(fig, "wigner.png")

st.metric("W mínimo", f"{W.min():.4f}", delta=None)
st.info("Los valores negativos de W son una firma inequívoca de no-clasicidad — solo aparecen en estados cuánticos genuinos.")

# ── Squeezing ────────────────────────────────────────────────────────────────
st.subheader("2. Squeezing — Varianzas de Cuadraturas")

r_max = st.slider("Squeezing máximo r", 0.5, 3.0, 2.0, 0.1)
r_vals = np.linspace(0, r_max, 200)
var_x  = 0.5 * np.exp(-2*r_vals)
var_p  = 0.5 * np.exp(+2*r_vals)
r_dB   = 8.686 * r_vals

fig2, axes2 = plt.subplots(1, 2, figsize=(10, 4))
axes2[0].semilogy(r_dB, var_x, 'steelblue', lw=2, label="Var(X) — comprimida")
axes2[0].semilogy(r_dB, var_p, 'darkorange', lw=2, label="Var(P) — amplificada")
axes2[0].axhline(0.5, color='gray', ls=':', lw=1.5, label="Vacío")
axes2[0].axvline(10, color='red', ls='--', lw=1.5, label="Umbral GKP (10 dB)")
axes2[0].axvline(15, color='purple', ls=':', lw=1.5, label="Récord experimental (15 dB)")
axes2[0].set_xlabel("Squeezing (dB)"); axes2[0].set_ylabel("Varianza")
axes2[0].set_title("Varianzas de cuadraturas tras squeezing"); axes2[0].legend(fontsize=9)

axes2[1].plot(r_dB, var_x * var_p, 'mediumseagreen', lw=2)
axes2[1].axhline(0.25, color='red', ls='--', lw=2, label="Min. Heisenberg = 1/4")
axes2[1].set_xlabel("Squeezing (dB)"); axes2[1].set_ylabel("Var(X) · Var(P)")
axes2[1].set_title("Principio de incertidumbre — constante"); axes2[1].legend()
plt.tight_layout()
st.pyplot(fig2)
plt.close(fig2)

# ── Código GKP ───────────────────────────────────────────────────────────────
st.subheader("3. Código GKP — Corrección de Errores")

col_a, col_b = st.columns([1, 2])
with col_a:
    Delta_gkp = st.slider("Anchura gaussiana Δ (1/squeezing)", 0.1, 0.6, 0.25, 0.01)
    delta_err = st.slider("Error de desplazamiento δx", 0.0, 1.5, 0.3, 0.05)
    threshold = np.sqrt(np.pi) / 2
    corregible = abs(delta_err) < threshold
    st.metric("Umbral GKP √π/2", f"{threshold:.4f}")
    if corregible:
        st.success(f"δx = {delta_err:.2f} ✓ Corregible")
    else:
        st.error(f"δx = {delta_err:.2f} ✗ No corregible")

with col_b:
    x_gkp = np.linspace(-9, 9, 2000)
    step = 2 * np.sqrt(np.pi)

    def gkp_state(x, logical, Delta, N=7):
        offset = 0.0 if logical == 0 else np.sqrt(np.pi)
        psi = sum(np.exp(-0.5*((x - n*step - offset)/Delta)**2)
                  for n in range(-N, N+1))
        return psi / np.sqrt(np.trapz(psi**2, x))

    psi0 = gkp_state(x_gkp, 0, Delta_gkp)
    psi1 = gkp_state(x_gkp, 1, Delta_gkp)
    psi0_err = gkp_state(x_gkp - delta_err, 0, Delta_gkp)

    fig3, axes3 = plt.subplots(1, 2, figsize=(10, 4))
    axes3[0].fill_between(x_gkp, psi0**2, alpha=0.6, color='steelblue', label="|0_L⟩")
    axes3[0].fill_between(x_gkp, psi1**2, alpha=0.6, color='darkorange', label="|1_L⟩")
    axes3[0].set_title(f"Estados lógicos GKP (Δ={Delta_gkp:.2f})")
    axes3[0].set_xlabel("x"); axes3[0].set_ylabel("|ψ(x)|²")
    axes3[0].set_xlim([-8, 8]); axes3[0].legend()

    axes3[1].fill_between(x_gkp, psi0**2, alpha=0.3, color='steelblue', label="|0_L⟩ ideal")
    axes3[1].fill_between(x_gkp, psi0_err**2, alpha=0.7,
                          color='crimson' if not corregible else 'mediumseagreen',
                          label=f"Con error δx={delta_err:.2f}")
    axes3[1].axvline(threshold, color='purple', ls='--', lw=1.5,
                     label=f"±√π/2 = ±{threshold:.2f}")
    axes3[1].axvline(-threshold, color='purple', ls='--', lw=1.5)
    axes3[1].set_title(f"Error {'(corregible)' if corregible else '(NO corregible)'}")
    axes3[1].set_xlabel("x"); axes3[1].set_ylabel("|ψ(x)|²")
    axes3[1].set_xlim([-8, 8]); axes3[1].legend(fontsize=9)
    plt.tight_layout()
    st.pyplot(fig3)
    plt.close(fig3)

# ── Tabla comparativa de plataformas ────────────────────────────────────────
st.subheader("4. Plataformas Fotónicas — Comparativa 2025")

import pandas as pd
data_hw = {
    "Sistema": ["PsiQuantum (Si-Ph)", "Xanadu Borealis (CV)", "Quandela (QD)",
                "QuiX 20-modo", "IBM Heron r2 (ref)", "IonQ Forte (ref)"],
    "Plataforma": ["Fotónica DV", "Fotónica CV", "Fotónica DV",
                   "Fotónica DV", "Superconductor", "Iones trampa"],
    "Error 2Q (%)": [">2", "~1", "~2", "~3", "0.3", "0.1"],
    "Temperatura": ["Ambiente", "Ambiente", "4 K", "Ambiente", "15 mK", "UHV"],
    "Velocidad puerta": ["~ns", "~µs", "~ns-µs", "~ns", "30 ns", "600 µs"],
    "Característica clave": [
        "Escalado fotónico masivo (FBQC)",
        "Ventaja cuántica demostrada (Borealis 2022)",
        "Eficiencia extracción >95% (puntos cuánticos)",
        "Pérdidas ultrabajas (<0.1 dB/cm)",
        "Menor error 2Q superconductor comercial",
        "Coherencia >1 min, conectividad total",
    ]
}
df_hw = pd.DataFrame(data_hw)
st.dataframe(df_hw, use_container_width=True)

st.markdown("""
**Lecturas recomendadas:**
- Knill, Laflamme & Milburn (2001) — *Linear optical quantum computing*. Nature 409.
- Zhong et al. (2020) — *Quantum computational advantage using photons*. Science 370.
- Gottesman, Kitaev & Preskill (2001) — *Encoding a qubit in an oscillator*. PRA 64.
- Bourassa et al. (2021) — *Blueprint for a scalable photonic fault-tolerant QC*. Quantum 5.
""")
