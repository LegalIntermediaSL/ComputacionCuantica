"""
Página 20 — Compilador Cuántico Paso a Paso
Transpilación, routing, optimización y métricas de circuitos.
"""
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

from qiskit import QuantumCircuit
from qiskit.compiler import transpile
from qiskit.transpiler import CouplingMap
from qiskit.circuit.library import QFT

from tour_guide import show_tour, export_figure_button

st.set_page_config(page_title="Compilador Cuántico", layout="wide")
st.title("⚙️ Compilador Cuántico Paso a Paso")
st.markdown(
    "Observa cómo se transforma un circuito cuántico abstracto al compilarlo para "
    "distintas arquitecturas de hardware: routing de qubits, inserción de SWAPs, "
    "descomposición en puertas nativas y optimización."
)

_TOUR_STEPS = [
    {"title": "⚙️ Compilación Cuántica", "body": "La compilación cuántica convierte un circuito abstracto en instrucciones que puede ejecutar el hardware real. Los pasos principales son: layout, routing, síntesis y optimización."},
    {"title": "🗺️ Layout y Routing", "body": "El hardware tiene conectividad limitada: solo ciertos pares de qubits pueden interactuar. El compilador inserta puertas SWAP para enrutar la interacción al par de qubits físicos adecuado."},
    {"title": "🔧 Optimización", "body": "Tras el routing, el compilador aplica reglas de reescritura (cancelación de puertas, fusión) para reducir la profundidad. Qiskit usa 4 niveles de optimización (0-3)."},
    {"title": "📊 Métricas", "body": "Las métricas clave son: profundidad del circuito, número de puertas 2Q (CX/CZ), número de SWAPs insertados y número de puertas totales. SWAP = 3 CX, por lo que minimizarlos es crítico."},
]
show_tour("compilador_cuantico", _TOUR_STEPS)

# ── Selector de circuito ─────────────────────────────────────────────────────
st.subheader("1. Circuito de Entrada")

col_circ, col_back = st.columns([1, 1])
with col_circ:
    circuit_type = st.selectbox("Circuito de ejemplo", [
        "QFT (4 qubits)",
        "Bell (2 qubits)",
        "GHZ (5 qubits)",
        "Random (4 qubits)",
        "Variacional EfficientSU2 (4 qubits)",
    ])
    opt_level = st.slider("Nivel de optimización Qiskit", 0, 3, 1)

with col_back:
    backend_name = st.selectbox("Arquitectura objetivo", [
        "Heavy-Hex IBM (lineal, 5 qubits)",
        "All-to-all (sin restricciones)",
        "Retícula 2D (2×3)",
        "Cadena lineal (5 qubits)",
    ])

# Construir circuito base
if circuit_type == "QFT (4 qubits)":
    qc_abstract = QFT(4)
elif circuit_type == "Bell (2 qubits)":
    qc_abstract = QuantumCircuit(2)
    qc_abstract.h(0); qc_abstract.cx(0,1)
elif circuit_type == "GHZ (5 qubits)":
    qc_abstract = QuantumCircuit(5)
    qc_abstract.h(0)
    for i in range(4): qc_abstract.cx(i, i+1)
elif circuit_type == "Random (4 qubits)":
    from qiskit.circuit.random import random_circuit
    qc_abstract = random_circuit(4, depth=4, seed=42)
else:  # EfficientSU2
    from qiskit.circuit.library import EfficientSU2
    qc_abstract = EfficientSU2(4, reps=1)
    qc_abstract = qc_abstract.decompose()

# Construir coupling map
n_qubits_hw = max(5, qc_abstract.num_qubits)
if backend_name.startswith("Heavy-Hex"):
    coupling_list = [(0,1),(1,2),(2,3),(3,4)]
    coupling = CouplingMap(couplinglist=coupling_list)
    basis_gates_hw = ['cx','rz','x','sx','id']
elif backend_name.startswith("All-to-all"):
    coupling_list = [(i,j) for i in range(n_qubits_hw) for j in range(n_qubits_hw) if i!=j]
    coupling = CouplingMap(couplinglist=coupling_list)
    basis_gates_hw = ['cx','rz','x','sx','id']
elif backend_name.startswith("Retícula"):
    coupling_list = [(0,1),(1,2),(0,3),(1,4),(2,5),(3,4),(4,5)]
    coupling = CouplingMap(couplinglist=coupling_list)
    basis_gates_hw = ['cx','rz','x','sx','id']
else:  # cadena lineal
    nq = max(5, qc_abstract.num_qubits)
    coupling_list = [(i,i+1) for i in range(nq-1)]
    coupling = CouplingMap(couplinglist=coupling_list)
    basis_gates_hw = ['cx','rz','x','sx','id']

# Transpilación
try:
    qc_transpiled = transpile(
        qc_abstract,
        coupling_map=coupling,
        basis_gates=basis_gates_hw,
        optimization_level=opt_level,
        seed_transpiler=42
    )
    transpile_ok = True
except Exception as e:
    st.error(f"Error en transpilación: {e}")
    transpile_ok = False

# ── Visualización comparativa ─────────────────────────────────────────────────
st.subheader("2. Comparativa: Antes y Después de Compilar")

if transpile_ok:
    col_before, col_after = st.columns(2)

    with col_before:
        st.markdown("**Circuito abstracto:**")
        fig_abs, ax_abs = plt.subplots(figsize=(6, 3))
        qc_abstract.decompose().draw(output='mpl', ax=ax_abs, fold=15, style={'fontsize': 8})
        st.pyplot(fig_abs); plt.close(fig_abs)
        st.metric("Profundidad", qc_abstract.decompose().depth())
        st.metric("Puertas 2Q", sum(1 for inst in qc_abstract.decompose().data if len(inst.qubits)==2))

    with col_after:
        st.markdown(f"**Circuito compilado (opt. nivel {opt_level}):**")
        fig_tr, ax_tr = plt.subplots(figsize=(6, 3))
        qc_transpiled.draw(output='mpl', ax=ax_tr, fold=15, style={'fontsize': 8})
        st.pyplot(fig_tr); plt.close(fig_tr)
        st.metric("Profundidad", qc_transpiled.depth())
        st.metric("Puertas 2Q", qc_transpiled.count_ops().get('cx', 0))

    # ── Métricas detalladas ──────────────────────────────────────────────────
    st.subheader("3. Métricas de Compilación")

    ops_before = qc_abstract.decompose().count_ops()
    ops_after  = qc_transpiled.count_ops()
    n_swap = ops_after.get('swap', 0)
    n_cx_before = sum(v for k,v in ops_before.items() if '2' in str(len(k)) or k in ('cx','cz','ecr'))
    n_cx_after  = ops_after.get('cx', 0)

    metrics_before = {
        'Profundidad': qc_abstract.decompose().depth(),
        'Puertas totales': sum(ops_before.values()),
        'Puertas 2Q': sum(1 for inst in qc_abstract.decompose().data if len(inst.qubits)==2),
        'SWAPs insertados': 0,
        'Qubits': qc_abstract.num_qubits,
    }
    metrics_after = {
        'Profundidad': qc_transpiled.depth(),
        'Puertas totales': sum(ops_after.values()),
        'Puertas 2Q': n_cx_after,
        'SWAPs insertados': n_swap,
        'Qubits': qc_transpiled.num_qubits,
    }

    import pandas as pd
    df_metrics = pd.DataFrame({'Antes': metrics_before, 'Después': metrics_after})
    df_metrics['Δ (%)'] = ((df_metrics['Después'] - df_metrics['Antes']) / (df_metrics['Antes'] + 1e-10) * 100).round(1)
    st.dataframe(df_metrics, use_container_width=True)

    # ── Comparativa por nivel de optimización ────────────────────────────────
    st.subheader("4. Impacto del Nivel de Optimización")

    @st.cache_data
    def compare_opt_levels(circuit_str, backend_coupling):
        results = []
        for lvl in range(4):
            try:
                qc_t = transpile(
                    eval(circuit_str),
                    coupling_map=CouplingMap(couplinglist=backend_coupling),
                    basis_gates=['cx','rz','x','sx','id'],
                    optimization_level=lvl, seed_transpiler=42
                )
                results.append({
                    'Nivel': lvl, 'Profundidad': qc_t.depth(),
                    'CX': qc_t.count_ops().get('cx',0),
                    'Total puertas': sum(qc_t.count_ops().values()),
                })
            except:
                results.append({'Nivel': lvl, 'Profundidad': 0, 'CX': 0, 'Total puertas': 0})
        return results

    coupling_tuple = tuple(tuple(p) for p in coupling_list[:20])
    ghz5 = QuantumCircuit(5)
    ghz5.h(0)
    for i in range(4): ghz5.cx(i,i+1)
    opt_results = []
    for lvl in range(4):
        try:
            qc_t = transpile(ghz5, coupling_map=CouplingMap(couplinglist=list(coupling_tuple)),
                             basis_gates=['cx','rz','x','sx','id'],
                             optimization_level=lvl, seed_transpiler=42)
            opt_results.append({
                'Nivel': lvl, 'Profundidad': qc_t.depth(),
                'CX': qc_t.count_ops().get('cx',0),
                'Total': sum(qc_t.count_ops().values()),
            })
        except:
            opt_results.append({'Nivel': lvl, 'Profundidad': 0, 'CX': 0, 'Total': 0})

    df_opt = pd.DataFrame(opt_results)
    fig_opt, axes_opt = plt.subplots(1, 3, figsize=(10, 3))
    for ax, col in zip(axes_opt, ['Profundidad', 'CX', 'Total']):
        ax.bar(df_opt['Nivel'], df_opt[col], color='steelblue')
        ax.set_xlabel('Nivel de optimización'); ax.set_ylabel(col)
        ax.set_title(f'{col} (GHZ 5Q, {backend_name[:15]})')
        ax.set_xticks([0,1,2,3])
    plt.tight_layout(); st.pyplot(fig_opt); plt.close(fig_opt)

    st.info("El nivel 3 aplica optimizaciones más agresivas (síntesis de puertas, commutation analysis) pero tarda más en compilar.")
