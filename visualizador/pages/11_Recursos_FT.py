"""
Página 11 — Estimador de Recursos Fault-Tolerant
Calcula qubits físicos, profundidad y tiempo para algoritmos FT.
"""

import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from tour_guide import show_tour

st.set_page_config(page_title="Estimador de Recursos FT", layout="wide")
st.title("🔭 Estimador de Recursos Fault-Tolerant")
st.markdown(
    "Estima los **qubits físicos**, **profundidad lógica** y **tiempo de ejecución** "
    "necesarios para ejecutar algoritmos cuánticos en hardware fault-tolerant."
)

_TOUR_STEPS = [
    {"title": "🔭 Estimador FT", "body": "Calcula los recursos reales necesarios para ejecutar algoritmos en hardware cuántico fault-tolerant: surface code, magic state distillation y overhead total."},
    {"title": "⚙️ Parámetros de hardware", "body": "La tasa de error física p determina la distancia d del surface code y el overhead de qubits. Arrastra para ver cómo cambian los requisitos."},
    {"title": "🎯 Selección de algoritmo", "body": "Cada algoritmo tiene un perfil de recursos diferente. Shor RSA-2048 es el más exigente; circuitos pequeños son viables antes."},
    {"title": "📊 Tabla de recursos", "body": "Compara qubits lógicos, físicos y tiempo de ejecución entre algoritmos para el mismo hardware."},
    {"title": "🗺️ Mapa de viabilidad", "body": "El gráfico muestra cuándo cada algoritmo se vuelve factible al mejorar la tasa de error física."},
]
show_tour("recursos_ft", _TOUR_STEPS)

# ---------------------------------------------------------------------------
# Modelos de recursos
# ---------------------------------------------------------------------------

def distancia_surface_code(p_fisico: float, p_logico_objetivo: float,
                            A: float = 0.1) -> int:
    """Distancia mínima d tal que p_L ≈ A·(p/p_th)^((d+1)/2) ≤ p_L_obj."""
    p_th = 0.01  # umbral del surface code
    if p_fisico >= p_th:
        return None
    ratio = p_fisico / p_th
    # Despejar d: log(p_L/A) = (d+1)/2 · log(ratio)
    if ratio >= 1 or ratio <= 0:
        return None
    d = 2 * np.log(p_logico_objetivo / A) / np.log(ratio) - 1
    d = max(3, int(np.ceil(d)))
    if d % 2 == 0:
        d += 1  # d debe ser impar
    return d

def qubits_por_logico(d: int) -> int:
    """Qubits físicos por qubit lógico en surface code: 2d²."""
    return 2 * d * d

def overhead_magic_states(n_T: int, p_fisico: float) -> dict:
    """
    Overhead de destilación de estados T (protocolo 15→1).
    Cada estado T requiere ~100-400 qubits físicos adicionales.
    """
    # Fidelidad del estado T crudo: p_T ≈ 35 p_fisico (para distancia 3)
    p_T_raw = min(0.499, 35 * p_fisico)
    # Destilación 15→1: p_T' ≈ 35 p_T³ (iterativa)
    p_T_distilled = 35 * p_T_raw**3
    n_rounds = 1
    while p_T_distilled > 1e-10 and n_rounds < 4:
        if p_T_distilled < 1e-15:
            break
        p_T_distilled = 35 * p_T_distilled**3
        n_rounds += 1
    qubits_T_factory = 300 * n_rounds  # estimado por fábrica T
    return {
        'n_T_gates': n_T,
        'n_factories': max(1, n_T // 100),
        'qubits_por_factory': qubits_T_factory,
        'total_qubits_T': qubits_T_factory * max(1, n_T // 100),
    }

ALGORITMOS = {
    "Bell (2q)": {
        "n_logicos": 2, "T_count": 0, "CX_logico": 1, "profundidad": 2,
        "descripcion": "Estado de Bell — circuito de prueba",
    },
    "Grover (10q, N=1024)": {
        "n_logicos": 10, "T_count": 140, "CX_logico": 80, "profundidad": 200,
        "descripcion": "Búsqueda Grover en N=1024 elementos (~√N iteraciones)",
    },
    "QFT (20q)": {
        "n_logicos": 20, "T_count": 0, "CX_logico": 190, "profundidad": 400,
        "descripcion": "Transformada de Fourier Cuántica — bloque de Shor/QPE",
    },
    "VQE H₂ (2q, ansatz)": {
        "n_logicos": 4, "T_count": 8, "CX_logico": 4, "profundidad": 20,
        "descripcion": "VQE para H₂ con ansatz UCCSD (4 qubits JW)",
    },
    "Shor RSA-512": {
        "n_logicos": 1024, "T_count": 4e9, "CX_logico": 2e9, "profundidad": 1e9,
        "descripcion": "Factorización RSA-512 (~10¹² puertas totales)",
    },
    "Shor RSA-2048": {
        "n_logicos": 4096, "T_count": 3e12, "CX_logico": 2e12, "profundidad": 8e11,
        "descripcion": "Factorización RSA-2048 (ruptura de cifrado actual)",
    },
    "QPE química FeMoco": {
        "n_logicos": 200, "T_count": 4e10, "CX_logico": 2e10, "profundidad": 5e9,
        "descripcion": "Estimación de energía FeMoco (nitrogenasa) — interés farmacéutico",
    },
    "HHL (100×100)": {
        "n_logicos": 30, "T_count": 1e6, "CX_logico": 5e5, "profundidad": 2e5,
        "descripcion": "Inversión de sistema lineal 100×100 (con QRAM)",
    },
}

# ---------------------------------------------------------------------------
# Interfaz
# ---------------------------------------------------------------------------

col_params, col_resultado = st.columns([1, 2])

with col_params:
    st.subheader("⚙️ Parámetros de hardware")

    p_fisico = st.select_slider(
        "Tasa de error física p",
        options=[0.0001, 0.0003, 0.001, 0.003, 0.01],
        value=0.001,
        format_func=lambda x: f"{x:.4f} ({x*100:.2f}%)",
    )

    frecuencia_puerta = st.slider(
        "Frecuencia de puerta física (MHz)", 0.1, 10.0, 1.0, 0.1
    )

    n_qubits_hw = st.number_input(
        "Qubits físicos disponibles", min_value=100, max_value=10_000_000,
        value=100_000, step=10_000,
    )

    algoritmo = st.selectbox("Algoritmo", list(ALGORITMOS.keys()))
    info_algo = ALGORITMOS[algoritmo]
    st.info(info_algo["descripcion"])

# Cálculos
p_th = 0.01
p_logico_obj = 1e-12  # error lógico objetivo por circuito

d = distancia_surface_code(p_fisico, p_logico_obj)
if d is None:
    with col_resultado:
        st.error(f"p_físico = {p_fisico:.4f} ≥ umbral p_th = {p_th:.3f}. No hay corrección de errores posible.")
    st.stop()

q_por_logico = qubits_por_logico(d)
n_logicos = info_algo["n_logicos"]
T_count   = info_algo["T_count"]
T_magic   = overhead_magic_states(int(T_count), p_fisico)
profundidad_logica = info_algo["profundidad"]

q_computacion = n_logicos * q_por_logico
q_T_factories = T_magic["total_qubits_T"]
q_total = q_computacion + q_T_factories

# Tiempo estimado (suponiendo 1 µs por ciclo de corrección de errores)
t_ciclo_s = 1e-6 / frecuencia_puerta
t_total_s = profundidad_logica * d * t_ciclo_s  # cada puerta lógica: d ciclos físicos
t_total_h = t_total_s / 3600

factible = q_total <= n_qubits_hw

with col_resultado:
    st.subheader("📊 Estimación de recursos")

    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Distancia del código d", d)
    col_m2.metric("Qubits físicos por lógico", f"{q_por_logico:,}")
    col_m3.metric("Factible con hardware", "✅ Sí" if factible else "❌ No")

    col_m4, col_m5, col_m6 = st.columns(3)
    col_m4.metric("Qubits lógicos", f"{n_logicos:,}")
    col_m5.metric("Qubits totales (incl. T)", f"{q_total:,.0f}")
    col_m6.metric("Tiempo estimado", f"{t_total_h:.2g} h" if t_total_h > 0.001 else f"{t_total_s:.2g} s")

    if not factible:
        deficit = q_total - n_qubits_hw
        st.warning(f"Faltan {deficit:,.0f} qubits físicos para ejecutar este algoritmo.")

    # Desglose
    with st.expander("🔍 Desglose detallado"):
        desglose = {
            "Parámetro": [
                "Distancia d", "Qubits por lógico (2d²)",
                "Qubits computación", "T-gates", "Fábricas T",
                "Qubits fábricas T", "Qubits TOTAL",
                "Profundidad lógica", "Tiempo total",
            ],
            "Valor": [
                d, q_por_logico,
                f"{q_computacion:,.0f}", f"{T_count:.2e}",
                T_magic["n_factories"], f"{q_T_factories:,.0f}",
                f"{q_total:,.0f}", f"{profundidad_logica:.2e}",
                f"{t_total_h:.3g} h",
            ],
        }
        st.dataframe(pd.DataFrame(desglose), use_container_width=True)

    # Comparativa de todos los algoritmos
    st.subheader("🗺️ Tabla comparativa de algoritmos")
    rows = []
    for nombre, info in ALGORITMOS.items():
        d_i = distancia_surface_code(p_fisico, p_logico_obj)
        if d_i is None:
            continue
        q_i = info["n_logicos"] * qubits_por_logico(d_i) + overhead_magic_states(int(info["T_count"]), p_fisico)["total_qubits_T"]
        factible_i = q_i <= n_qubits_hw
        t_i = info["profundidad"] * d_i * t_ciclo_s / 3600
        rows.append({
            "Algoritmo": nombre,
            "Qubits lógicos": f'{info["n_logicos"]:,}',
            "Qubits físicos totales": f'{q_i:,.0f}',
            "Tiempo (h)": f'{t_i:.2g}',
            "Factible": "✅" if factible_i else "❌",
        })
    df_comp = pd.DataFrame(rows)
    st.dataframe(df_comp, use_container_width=True)

    # Gráfica: qubits totales vs p_físico para cada algoritmo
    st.subheader("📈 Requisitos vs tasa de error física")
    p_vals = [0.0001, 0.0003, 0.001, 0.003]
    fig, ax = plt.subplots(figsize=(10, 5))

    colores = plt.cm.tab10(np.linspace(0, 1, min(8, len(ALGORITMOS))))
    for (nombre_a, info_a), color in zip(list(ALGORITMOS.items())[:8], colores):
        qs = []
        ps_valid = []
        for p in p_vals:
            d_p = distancia_surface_code(p, p_logico_obj)
            if d_p is None:
                continue
            q_p = info_a["n_logicos"] * qubits_por_logico(d_p)
            qs.append(q_p)
            ps_valid.append(p)
        if qs:
            label = nombre_a if len(nombre_a) < 25 else nombre_a[:22] + "..."
            ax.semilogy([p * 100 for p in ps_valid], qs, 'o-',
                       color=color, lw=2, ms=6, label=label)

    ax.axhline(n_qubits_hw, color='red', ls='--', lw=2,
               label=f'Hardware disponible ({n_qubits_hw:,}q)')
    ax.set_xlabel("Tasa de error física p (%)")
    ax.set_ylabel("Qubits físicos requeridos")
    ax.set_title("Requisitos de qubits vs calidad del hardware")
    ax.legend(fontsize=7, loc='upper left')
    ax.grid(alpha=0.3, which='both')
    st.pyplot(fig)
    plt.close(fig)
