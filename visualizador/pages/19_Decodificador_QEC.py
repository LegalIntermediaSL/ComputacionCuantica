"""
Página 19 — Decodificador QEC Interactivo
Surface code, síndromes, MWPM y umbral de error.
"""
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
from itertools import product as iproduct
import warnings
warnings.filterwarnings('ignore')

from tour_guide import show_tour, export_figure_button

st.set_page_config(page_title="Decodificador QEC", layout="wide")
st.title("🛡️ Decodificador QEC Interactivo")
st.markdown(
    "Explora la detección y corrección de errores en el surface code. "
    "Introduce errores manualmente, observa los síndromes y compara decodificadores."
)

_TOUR_STEPS = [
    {"title": "🛡️ QEC Interactivo", "body": "Esta página ilustra cómo funcionan los códigos de corrección de errores cuánticos: el surface code, los síndromes y el decodificador MWPM."},
    {"title": "🔲 Surface Code", "body": "El surface code de distancia d tiene d² qubits de datos. Los qubits de ancilla miden los estabilizadores (cuadrados verdes y azules). Un error activa los estabilizadores vecinos."},
    {"title": "📡 Síndromes", "body": "Un síndrome activo (punto rojo) indica que el estabilizador detectó un error en alguno de sus qubits vecinos. El decodificador usa los síndromes para inferir la corrección óptima."},
    {"title": "⚖️ MWPM", "body": "MWPM (Minimum Weight Perfect Matching) empareja los síndromes activos con el matching de peso mínimo. Equivale al camino de errores más probable bajo el modelo de ruido de Pauli independiente."},
    {"title": "📊 Umbral", "body": "El umbral p_th ≈ 1% es la tasa de error físico por debajo de la cual aumentar d reduce P_L. Las curvas de umbral muestran que d mayor siempre gana para p < p_th."},
]
show_tour("decodificador_qec", _TOUR_STEPS)

# ── Helpers ──────────────────────────────────────────────────────────────────

def draw_surface_code(d, errors_x=None, errors_z=None, syndromes_x=None, syndromes_z=None, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(5, 5))
    if errors_x is None: errors_x = set()
    if errors_z is None: errors_z = set()
    if syndromes_x is None: syndromes_x = set()
    if syndromes_z is None: syndromes_z = set()

    # Qubits de datos en posiciones (i,j) para i,j en [0,d-1]
    for i in range(d):
        for j in range(d):
            color = 'white'
            if (i, j) in errors_x: color = 'crimson'
            if (i, j) in errors_z: color = 'steelblue'
            if (i, j) in errors_x and (i, j) in errors_z: color = 'purple'
            circ = plt.Circle((j, d-1-i), 0.3, color=color, ec='black', lw=1.5, zorder=5)
            ax.add_patch(circ)
            ax.text(j, d-1-i, f'{i*d+j}', ha='center', va='center', fontsize=7, zorder=6)

    # Estabilizadores X (caras, cuadrados verdes)
    for i in range(d-1):
        for j in range(d-1):
            face_color = 'red' if (i,j) in syndromes_x else 'palegreen'
            rect = mpatches.FancyBboxPatch((j+0.3, d-2-i+0.3), 0.4, 0.4,
                                           boxstyle="round,pad=0.05", color=face_color,
                                           alpha=0.7, zorder=3)
            ax.add_patch(rect)

    # Estabilizadores Z (vértices entre qubits, cuadrados azules)
    for i in range(1, d):
        for j in range(d-1):
            face_color = 'red' if (i,j) in syndromes_z else 'lightblue'
            rect = mpatches.FancyBboxPatch((j+0.3, d-1-i-0.05), 0.4, 0.4,
                                           boxstyle="round,pad=0.05", color=face_color,
                                           alpha=0.7, zorder=3)
            ax.add_patch(rect)

    ax.set_xlim(-0.5, d-0.5)
    ax.set_ylim(-0.5, d-0.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(f'Surface Code d={d}', fontsize=12)
    return ax

def compute_syndromes_x(d, errors_x):
    """Síndrome X activo si el estabilizador tiene número impar de errores X vecinos."""
    syndromes = set()
    for i in range(d-1):
        for j in range(d-1):
            neighbors = [(i,j),(i,j+1),(i+1,j),(i+1,j+1)]
            count = sum(1 for n in neighbors if n in errors_x)
            if count % 2 == 1:
                syndromes.add((i,j))
    return syndromes

def mwpm_simple(defect_positions, d):
    """MWPM simplificado: matchea pares de síndromes con peso = distancia L1."""
    if len(defect_positions) == 0:
        return []
    if len(defect_positions) % 2 == 1:
        defect_positions = defect_positions + [(-1, -1)]  # borde virtual
    G = nx.Graph()
    for i, p1 in enumerate(defect_positions):
        for j, p2 in enumerate(defect_positions):
            if i < j:
                if p1 == (-1,-1) or p2 == (-1,-1):
                    weight = min(p2[0]+1, d-p2[0], p2[1]+1, d-p2[1]) if p1==(-1,-1) else min(p1[0]+1, d-p1[0], p1[1]+1, d-p1[1])
                else:
                    weight = abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])
                G.add_edge(i, j, weight=weight)
    matching = nx.min_weight_matching(G)
    return [(defect_positions[i], defect_positions[j]) for i, j in matching
            if defect_positions[i] != (-1,-1) and defect_positions[j] != (-1,-1)]

# ── 1. Surface Code Interactivo ───────────────────────────────────────────────
st.subheader("1. Surface Code Interactivo — Introduce Errores")

col_ctrl, col_plot = st.columns([1, 2])
with col_ctrl:
    d_sc = st.selectbox("Distancia d", [3, 5], index=0)
    n_q = d_sc * d_sc
    st.markdown(f"**{n_q} qubits de datos**, {(d_sc-1)*(d_sc-1)} estabilizadores X, {(d_sc-1)*(d_sc-1)} Z")
    st.markdown("**Errores X (flip de bit):**")
    errors_x_sel = set()
    cols_err = st.columns(d_sc)
    for i in range(d_sc):
        for j in range(d_sc):
            with cols_err[j]:
                if st.checkbox(f"q{i*d_sc+j}", key=f"ex_{i}_{j}"):
                    errors_x_sel.add((i, j))
    show_correction = st.checkbox("Mostrar corrección MWPM", value=True)

with col_plot:
    syn_x = compute_syndromes_x(d_sc, errors_x_sel)
    matching = mwpm_simple(list(syn_x), d_sc) if show_correction and syn_x else []

    fig_sc, ax_sc = plt.subplots(figsize=(5, 5))
    draw_surface_code(d_sc, errors_x=errors_x_sel, syndromes_x=syn_x, ax=ax_sc)

    # Dibujar matching MWPM
    for (p1, p2) in matching:
        x1, y1 = p1[1]+0.5, d_sc-1.5-p1[0]
        x2, y2 = p2[1]+0.5, d_sc-1.5-p2[0]
        ax_sc.annotate("", xy=(x2,y2), xytext=(x1,y1),
                        arrowprops=dict(arrowstyle="-", color='purple', lw=2, ls='--'))

    from matplotlib.lines import Line2D
    legend_elements = [
        mpatches.Patch(color='crimson', label='Error X'),
        mpatches.Patch(color='palegreen', label='Estab. X (no activo)'),
        mpatches.Patch(color='red', alpha=0.7, label='Síndrome activo'),
        Line2D([0],[0], color='purple', lw=2, ls='--', label='Corrección MWPM'),
    ]
    ax_sc.legend(handles=legend_elements, loc='upper right', fontsize=7)
    st.pyplot(fig_sc)
    plt.close(fig_sc)
    export_figure_button(fig_sc, "surface_code.png")

if syn_x:
    st.warning(f"**{len(syn_x)} síndromes activos** en posiciones {sorted(syn_x)}")
    if matching:
        st.success(f"MWPM propone {len(matching)} corrección(es): {matching}")
else:
    st.success("Sin síndromes activos — no se detectan errores.")

# ── 2. Umbral del Surface Code ────────────────────────────────────────────────
st.subheader("2. Curva de Umbral P_L vs p")

col_th1, col_th2 = st.columns([1, 3])
with col_th1:
    d_list = st.multiselect("Distancias a comparar", [3,5,7,9], default=[3,5,7])
    n_trials_th = st.slider("Simulaciones por punto", 500, 3000, 1000, 500)
    p_th_theory = st.number_input("Umbral teórico p_th (%)", value=1.0, step=0.1)

with col_th2:
    @st.cache_data
    def compute_threshold_curves(d_list, n_trials):
        p_vals = np.linspace(0.01, 0.15, 12)
        results = {}
        for d in d_list:
            pL = []
            H = np.zeros((d-1, d), dtype=int)
            for i in range(d-1): H[i,i]=1; H[i,i+1]=1
            for p in p_vals:
                errors = 0
                for _ in range(n_trials):
                    err = (np.random.random(d) < p).astype(int)
                    syn = (H @ err) % 2
                    # Corrección simple: lookup para código cadena
                    syn_pos = [i for i,s in enumerate(syn) if s==1]
                    corr = np.zeros(d, dtype=int)
                    if len(syn_pos) % 2 == 0 and len(syn_pos) > 0:
                        for k in range(0, len(syn_pos), 2):
                            for q in range(syn_pos[k], syn_pos[k+1]):
                                corr[q] ^= 1
                    residual = (err + corr) % 2
                    if residual.sum() % 2 == 1: errors += 1
                pL.append(errors / n_trials)
            results[d] = (p_vals, np.array(pL))
        return results

    curves = compute_threshold_curves(tuple(d_list), n_trials_th)
    colors_th = ['steelblue','darkorange','mediumseagreen','crimson']
    fig_th, ax_th = plt.subplots(figsize=(7,4))
    for (d, (pv, pL)), col in zip(curves.items(), colors_th):
        ax_th.semilogy(pv*100, np.maximum(pL, 1e-4), 'o-', color=col, lw=2, label=f'd = {d}')
    ax_th.axvline(p_th_theory, color='black', ls='--', lw=2, label=f'p_th = {p_th_theory}%')
    ax_th.set_xlabel('Tasa de error físico p (%)'); ax_th.set_ylabel('P_L (log)')
    ax_th.set_title('Umbral del Surface Code — Código Cadena 1D'); ax_th.legend()
    ax_th.grid(True, which='both', alpha=0.3)
    st.pyplot(fig_th)
    plt.close(fig_th)
    export_figure_button(fig_th, "qec_threshold.png")

# ── 3. Overhead Surface Code vs qLDPC ────────────────────────────────────────
st.subheader("3. Comparativa Overhead: Surface Code vs qLDPC")

import pandas as pd
df_overhead = pd.DataFrame([
    {'Código': 'Surface d=3',  'n': 18,  'k': 1,  'd_code': 3,  'n/k': 18,  'Tipo': 'Surface'},
    {'Código': 'Surface d=5',  'n': 50,  'k': 1,  'd_code': 5,  'n/k': 50,  'Tipo': 'Surface'},
    {'Código': 'Surface d=7',  'n': 98,  'k': 1,  'd_code': 7,  'n/k': 98,  'Tipo': 'Surface'},
    {'Código': 'Surface d=11', 'n': 242, 'k': 1,  'd_code': 11, 'n/k': 242, 'Tipo': 'Surface'},
    {'Código': 'BB [[72,12,6]]','n': 72, 'k': 12, 'd_code': 6,  'n/k': 6,   'Tipo': 'qLDPC'},
    {'Código': 'BB [[144,12,12]]','n':144,'k':12, 'd_code': 12, 'n/k': 12,  'Tipo': 'qLDPC'},
    {'Código': 'HP [[800,25,20]]','n':800,'k':25,'d_code': 20, 'n/k': 32,  'Tipo': 'qLDPC'},
])
st.dataframe(df_overhead, use_container_width=True)

fig_ov, ax_ov = plt.subplots(figsize=(8, 4))
colors_ov = ['steelblue' if t=='Surface' else 'darkorange' for t in df_overhead['Tipo']]
bars_ov = ax_ov.bar(df_overhead['Código'], df_overhead['n/k'], color=colors_ov)
ax_ov.axhline(12, color='red', ls='--', lw=2, label='Target: 12 qubits/lógico (BB [[144,12,12]])')
ax_ov.set_ylabel('Qubits físicos por lógico (n/k)')
ax_ov.set_title('Overhead: Surface Code vs qLDPC (Bivariate Bicycle)')
plt.setp(ax_ov.get_xticklabels(), rotation=20, ha='right', fontsize=8)
from matplotlib.patches import Patch
ax_ov.legend(handles=[Patch(color='steelblue',label='Surface Code'),
                       Patch(color='darkorange',label='qLDPC'),
                       plt.Line2D([0],[0],color='red',ls='--',label='Target 12×')])
plt.tight_layout(); st.pyplot(fig_ov); plt.close(fig_ov)
st.info("Los códigos BB [[144,12,12]] necesitan **~28× menos** qubits físicos que surface code d=11 para capacidad lógica equivalente.")
