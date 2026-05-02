"""
Página 18 — Átomos Neutros y Arrays de Rydberg
Array 2D configurable, diagrama de fases, evolución temporal y MAX-CUT.
"""
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.linalg import eigh, expm
import warnings
warnings.filterwarnings('ignore')

from tour_guide import show_tour, export_figure_button

st.set_page_config(page_title="Rydberg Arrays", layout="wide")
st.title("⚛️ Átomos Neutros y Arrays de Rydberg")
st.markdown(
    "Explora la física de los qubits de Rydberg: interacción van der Waals, bloqueo cuántico, "
    "diagrama de fases, evolución temporal y optimización combinatoria (MAX-CUT)."
)

_TOUR_STEPS = [
    {"title": "⚛️ Rydberg Arrays", "body": "Los átomos neutros atrapados en pinzas ópticas forman uno de los mejores procesadores cuánticos para simulación y optimización. QuEra, Pasqal y Atom Computing lideran esta plataforma."},
    {"title": "🔵 Array 2D", "body": "Visualiza la posición de los átomos y el radio de bloqueo. Dos átomos dentro del radio no pueden estar simultáneamente en el estado Rydberg — la base del 2-qubit gate."},
    {"title": "📊 Diagrama de Fases", "body": "Variando Ω y Δ se obtiene una fase atómica (todos en |g⟩), una fase Rydberg (todos en |r⟩), y una fase cristalina Z2 (alternancia |gr...⟩) separadas por transiciones cuánticas de fase."},
    {"title": "⏱ Evolución Temporal", "body": "Partiendo del estado Z2, el sistema oscila mostrando renacimientos de fidelidad — evidencia de quantum many-body scars que desafían la termalización según la hipótesis ETH."},
    {"title": "🔗 MAX-CUT", "body": "El problema MAX-CUT se mapea a la fase de Rydberg: los átomos en |r⟩ forman el corte máximo. Para grafos donde el radio de bloqueo cubre exactamente las aristas, el estado fundamental resuelve MAX-CUT."},
]
show_tour("rydberg_arrays", _TOUR_STEPS)

# ── Helpers ──────────────────────────────────────────────────────────────────

def op_on_site(op, site, N):
    ops = [np.eye(2)] * N
    ops[site] = op
    result = ops[0]
    for o in ops[1:]:
        result = np.kron(result, o)
    return result

def build_pxp_H(N, Omega=1.0):
    sx = np.array([[0,1],[1,0]], dtype=complex)
    P0 = np.array([[1,0],[0,0]], dtype=complex)
    P1 = np.array([[0,0],[0,1]], dtype=complex)
    dim = 2**N
    H = np.zeros((dim, dim), dtype=complex)
    for i in range(N):
        left  = op_on_site(P0, (i-1) % N, N)
        drive = op_on_site(sx, i, N)
        right = op_on_site(P0, (i+1) % N, N)
        H += (Omega/2) * left @ drive @ right
    return H

def build_rydberg_H_small(N, Omega, Delta, C6=100.0, a=1.0):
    sx = np.array([[0,1],[1,0]], dtype=complex)
    nR = np.array([[0,0],[0,1]], dtype=complex)
    H = np.zeros((2**N, 2**N), dtype=complex)
    for i in range(N):
        H += (Omega/2) * op_on_site(sx, i, N)
        H -= Delta * op_on_site(nR, i, N)
    for i in range(N-1):
        for j in range(i+1, N):
            dist = abs(i - j) * a
            Uij = C6 / dist**6
            H += Uij * (op_on_site(nR, i, N) @ op_on_site(nR, j, N))
    return H

# ── 1. Array 2D ──────────────────────────────────────────────────────────────
st.subheader("1. Array 2D — Posición y Radio de Bloqueo")

col1, col2 = st.columns([1, 3])
with col1:
    Lx = st.slider("Columnas", 2, 5, 3)
    Ly = st.slider("Filas", 2, 5, 3)
    spacing = st.slider("Espaciado (μm)", 3.0, 10.0, 5.0, 0.5)
    Omega_arr = st.slider("Ω/2π (MHz) array", 0.5, 3.0, 1.0, 0.1)
    C6_arr = st.number_input("C₆ (GHz·μm⁶)", value=862690.0, format="%.0f")
    r_block = (C6_arr / (Omega_arr * 1e3)) ** (1/6)
    st.metric("Radio de bloqueo r_b", f"{r_block:.2f} μm")

with col2:
    xs = np.array([i * spacing for i in range(Lx) for _ in range(Ly)])
    ys = np.array([j * spacing for _ in range(Lx) for j in range(Ly)])

    fig_arr, ax_arr = plt.subplots(figsize=(5, 4))
    # Draw blockade circles between first atom and its neighbors
    for i in range(len(xs)):
        for j in range(i+1, len(xs)):
            dist = np.sqrt((xs[i]-xs[j])**2 + (ys[i]-ys[j])**2)
            if dist <= r_block:
                ax_arr.plot([xs[i],xs[j]], [ys[i],ys[j]], 'r-', lw=1.5, alpha=0.5)
    for xi, yi in zip(xs, ys):
        circle = plt.Circle((xi, yi), r_block/2, color='steelblue', alpha=0.08)
        ax_arr.add_patch(circle)
    ax_arr.scatter(xs, ys, s=120, c='steelblue', zorder=5, edgecolors='navy')
    ax_arr.set_aspect('equal')
    ax_arr.set_xlabel("x (μm)"); ax_arr.set_ylabel("y (μm)")
    ax_arr.set_title(f"Array {Lx}×{Ly}, r_b = {r_block:.1f} μm")
    blocked = sum(1 for i in range(len(xs)) for j in range(i+1, len(xs))
                  if np.sqrt((xs[i]-xs[j])**2+(ys[i]-ys[j])**2) <= r_block)
    ax_arr.text(0.03, 0.93, f"Pares bloqueados: {blocked}", transform=ax_arr.transAxes,
                fontsize=9, bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    st.pyplot(fig_arr)
    plt.close(fig_arr)
    export_figure_button(fig_arr, "rydberg_array.png")

# ── 2. Diagrama de fases ──────────────────────────────────────────────────────
st.subheader("2. Diagrama de Fases (N=4 cadena)")

col_ph1, col_ph2 = st.columns([1, 3])
with col_ph1:
    N_ph = 4
    n_pts = st.slider("Resolución", 15, 40, 25)
    C6_ph = st.slider("C₆ (nn, u.a.)", 10.0, 300.0, 100.0, 10.0)
    st.info("Ω varía en filas, Δ en columnas. Color = ⟨n_Ryd⟩ por sitio.")

with col_ph2:
    nR_op = np.array([[0,0],[0,1]], dtype=complex)
    Om_vals = np.linspace(0.5, 3.0, n_pts)
    De_vals = np.linspace(-2.0, 6.0, n_pts)
    nryd_map = np.zeros((n_pts, n_pts))
    z2_map   = np.zeros((n_pts, n_pts))

    nR_total = sum(op_on_site(nR_op, i, N_ph) for i in range(N_ph)) / N_ph
    for ii, Om in enumerate(Om_vals):
        for jj, De in enumerate(De_vals):
            H = build_rydberg_H_small(N_ph, Om, De, C6=C6_ph)
            evals, evecs = eigh(H)
            gs = evecs[:, 0]
            nryd_map[ii, jj] = np.real(gs @ nR_total @ gs)

    fig_ph, ax_ph = plt.subplots(figsize=(6, 4.5))
    im_ph = ax_ph.pcolormesh(De_vals, Om_vals, nryd_map, cmap='plasma', shading='auto')
    plt.colorbar(im_ph, ax=ax_ph, label="⟨n_Ryd⟩ / sitio")
    ax_ph.set_xlabel("Δ/2π (u.a.)"); ax_ph.set_ylabel("Ω/2π (u.a.)")
    ax_ph.set_title(f"Diagrama de fases — N={N_ph}, C₆={C6_ph:.0f}")
    ax_ph.axvline(0, color='white', ls='--', lw=1, alpha=0.7)
    st.pyplot(fig_ph)
    plt.close(fig_ph)
    export_figure_button(fig_ph, "rydberg_phase_diagram.png")

st.info("⟨n_Ryd⟩≈0: fase atómica  |  ⟨n_Ryd⟩≈0.5: fase Z2 cristalina  |  ⟨n_Ryd⟩≈1: fase Rydberg")

# ── 3. Evolución temporal — scars ─────────────────────────────────────────────
st.subheader("3. Evolución Temporal y Quantum Many-Body Scars (PXP)")

col_t1, col_t2 = st.columns([1, 3])
with col_t1:
    N_sc = st.selectbox("N átomos (PXP)", [4, 6], index=0)
    Omega_sc = st.slider("Ω (PXP)", 0.5, 2.0, 1.0, 0.1)
    t_max = st.slider("Tiempo máximo", 5.0, 30.0, 20.0, 1.0)
    n_t = 200

with col_t2:
    H_pxp = build_pxp_H(N_sc, Omega_sc)
    evals_p, evecs_p = eigh(H_pxp)
    # Z2 state: alternating |1010...⟩
    z2_idx = int("".join(["10"*(N_sc//2)][:N_sc]), 2)
    psi0 = np.zeros(2**N_sc, dtype=complex)
    psi0[z2_idx] = 1.0

    ts = np.linspace(0, t_max, n_t)
    overlaps = np.abs(evecs_p.conj().T @ psi0)**2
    fidelities = np.array([
        abs(sum(overlaps * np.exp(-1j*evals_p*t)))**2
        for t in ts
    ])

    nR_pxp = sum(op_on_site(nR_op, i, N_sc) for i in range(N_sc)) / N_sc
    n_ryd_t = np.array([
        np.real((evecs_p @ (np.exp(-1j*evals_p*t) * overlaps**0.5) @
                 evecs_p.conj().T @ nR_pxp @
                 evecs_p @ (np.exp(-1j*evals_p*t) * overlaps**0.5) @
                 evecs_p.conj().T).diagonal().sum())
        for t in ts
    ])
    # Simpler: compute ⟨nRyd⟩(t) directly
    n_ryd_t = []
    for t in ts:
        c = evecs_p.T.conj() @ psi0
        c_t = c * np.exp(-1j * evals_p * t)
        psi_t = evecs_p @ c_t
        n_ryd_t.append(np.real(psi_t.conj() @ nR_pxp @ psi_t))
    n_ryd_t = np.array(n_ryd_t)

    fig_sc, axes_sc = plt.subplots(2, 1, figsize=(8, 5), sharex=True)
    axes_sc[0].plot(ts, fidelities, color='steelblue', lw=1.5)
    axes_sc[0].set_ylabel("F(t) = |⟨Z2|ψ(t)⟩|²")
    axes_sc[0].set_title(f"PXP N={N_sc}, Ω={Omega_sc:.1f} — Revivals del estado Z2")
    axes_sc[0].axhline(1/(2**N_sc), color='gray', ls=':', label="Promedio ETH")
    axes_sc[0].legend(fontsize=8)

    axes_sc[1].plot(ts, n_ryd_t, color='darkorange', lw=1.5)
    axes_sc[1].set_ylabel("⟨n_Ryd⟩/sitio"); axes_sc[1].set_xlabel("t (ℏ/u.a.)")
    axes_sc[1].set_title("Oscilación de población Rydberg")

    plt.tight_layout()
    st.pyplot(fig_sc)
    plt.close(fig_sc)
    export_figure_button(fig_sc, "rydberg_scars.png")

# ── 4. MAX-CUT ───────────────────────────────────────────────────────────────
st.subheader("4. MAX-CUT con Bloqueo Rydberg (6 nodos)")

st.markdown(
    "Para un grafo de 6 nodos en disposición circular, el estado de mínima energía del Hamiltoniano "
    "de Rydberg resuelve MAX-CUT cuando el radio de bloqueo cubre exactamente las aristas."
)

N_mc = 6
angles = np.linspace(0, 2*np.pi, N_mc, endpoint=False)
R_mc = 1.0
xs_mc = R_mc * np.cos(angles)
ys_mc = R_mc * np.sin(angles)

spacing_mc = 2 * R_mc * np.sin(np.pi/N_mc)
edges = [(i, (i+1)%N_mc) for i in range(N_mc)]

col_mc1, col_mc2 = st.columns(2)
with col_mc1:
    fig_mc, ax_mc = plt.subplots(figsize=(4, 4))
    for i, j in edges:
        ax_mc.plot([xs_mc[i], xs_mc[j]], [ys_mc[i], ys_mc[j]], 'k-', lw=2)
    colors = ['steelblue', 'darkorange', 'steelblue', 'darkorange', 'steelblue', 'darkorange']
    labels = ['|r⟩' if c=='darkorange' else '|g⟩' for c in colors]
    ax_mc.scatter(xs_mc, ys_mc, s=200, c=colors, zorder=5, edgecolors='black')
    for i, (x, y, lbl) in enumerate(zip(xs_mc, ys_mc, labels)):
        ax_mc.text(x*1.18, y*1.18, f"{i}:{lbl}", ha='center', va='center', fontsize=9)
    cut_count = sum(1 for i,j in edges if colors[i] != colors[j])
    ax_mc.set_aspect('equal'); ax_mc.axis('off')
    ax_mc.set_title(f"MAX-CUT alternante: {cut_count}/{len(edges)} aristas cortadas")
    p0 = mpatches.Patch(color='steelblue', label='|g⟩ — ground')
    p1 = mpatches.Patch(color='darkorange', label='|r⟩ — Rydberg')
    ax_mc.legend(handles=[p0, p1], loc='upper right', fontsize=8)
    st.pyplot(fig_mc)
    plt.close(fig_mc)

with col_mc2:
    st.markdown(f"""
**Configuración MAX-CUT alternante:**
- Nodos pares → |g⟩ (ground)
- Nodos impares → |r⟩ (Rydberg)
- Aristas cortadas: **{cut_count}/{len(edges)}** (= MAX-CUT para ciclo C₆)

**Bloqueo de Rydberg:**
- Pares vecinos separados: {spacing_mc:.2f} u.a.
- Para r_b ≈ {spacing_mc:.2f} μm, vecinos están bloqueados
- Estado |rgrgrg⟩ es el estado de máxima independencia

**Comparativa:**
| Algoritmo | Corte | Tiempo |
|-----------|-------|--------|
| Rydberg analógico | 6/6 | < 1 μs |
| QAOA p=1 | ~5/6 | variable |
| Clásico greedy | ~5/6 | O(n²) |
""")

# ── 5. Resumen de plataformas ─────────────────────────────────────────────────
st.subheader("5. Plataformas de Átomos Neutros — 2025")

import pandas as pd
data_plat = {
    "Empresa": ["QuEra (Aquila)", "Pasqal", "Atom Computing", "Infleqtion", "MIT/Harvard"],
    "Qubits": ["256→10 000 lógicos", "~300", "~1180", "~100", "~200"],
    "Fidelidad CZ": [">99.5%", ">99%", ">99%", ">99%", ">99.5%"],
    "T_coherencia": ["~1 s", "~0.5 s", "~1 s", "~0.5 s", "~10 s"],
    "Característica": [
        "Primer QC neutral-atom con >1000 qubits lógicos (2024)",
        "Arrays 2D+3D, microwaves + Rydberg hybrid",
        "Alcinium (Al) atoms — 1180 qubits (2023)",
        "Hibrid atom-optical chip platform",
        "Erasure qubits + FPGA real-time feedback",
    ]
}
df_plat = pd.DataFrame(data_plat)
st.dataframe(df_plat, use_container_width=True)

st.markdown("""
**Lecturas recomendadas:**
- Bernien et al. (2017) — *Probing many-body dynamics on a 51-atom quantum simulator*. Nature 551.
- Semeghini et al. (2021) — *Probing topological spin liquids on a programmable quantum simulator*. Science 374.
- Ebadi et al. (2022) — *Quantum optimization of maximum independent set*. Science 376.
- Bluvstein et al. (2024) — *Logical quantum processor based on reconfigurable atom arrays*. Nature 626.
""")
