"""
Página 16 — Benchmark Interactivo de Hardware Cuántico 2025
Compara CLOPS, Quantum Volume, T1/T2, error rates y umbrales de corrección de errores.
"""

import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

from tour_guide import show_tour, export_figure_button

st.set_page_config(page_title="Benchmark Hardware Cuántico 2025", layout="wide")
st.title("📊 Benchmark de Hardware Cuántico — 2025")
st.markdown(
    "Compara **tasas de error**, **Quantum Volume**, **CLOPS** y "
    "**tiempos de coherencia** de los principales procesadores cuánticos disponibles."
)

_TOUR_STEPS = [
    {"title": "📊 Hardware Benchmark", "body": "Esta página compara los principales procesadores cuánticos de 2025 con métricas reales de rendimiento: error de puerta, coherencia, QV y CLOPS."},
    {"title": "🔍 Tabla comparativa", "body": "La tabla muestra todos los sistemas. Filtra por plataforma o métrica. El color indica qué tan cerca está cada sistema del umbral de corrección de errores."},
    {"title": "📉 Gráficos de error", "body": "Los paneles muestran la evolución histórica del error de puerta 2Q y la posición relativa de cada sistema respecto al umbral del código de superficie (~1%)."},
    {"title": "⏱ Coherencia vs Velocidad", "body": "Hay un trade-off fundamental: iones trampa tienen T1~1000s pero puertas lentas (ms), superconductores tienen puertas rápidas (ns) pero T1~100μs."},
    {"title": "🏆 QV vs CLOPS", "body": "QV mide complejidad máxima ejecutable. CLOPS mide throughput. Un sistema puede tener alto QV pero bajo CLOPS (iones) o alto CLOPS pero menor QV (superconductores Eagle)."},
]
show_tour("benchmark_hardware", _TOUR_STEPS)

# ── Datos de hardware ───────────────────────────────────────────────────────
HARDWARE_DATA = [
    {
        "Sistema": "IBM Heron r2 (ibm_torino)",
        "Plataforma": "Superconductor",
        "Qubits": 133,
        "T1_us": 325,
        "T2_us": 200,
        "Error_1Q": 5e-5,
        "Error_2Q": 5e-4,
        "Readout_%": 1.0,
        "QV": 1024,
        "CLOPS": 15000,
        "Año_dato": 2025,
    },
    {
        "Sistema": "IBM Eagle r3 (ibm_brisbane)",
        "Plataforma": "Superconductor",
        "Qubits": 127,
        "T1_us": 175,
        "T2_us": 125,
        "Error_1Q": 2e-4,
        "Error_2Q": 5e-3,
        "Readout_%": 2.0,
        "QV": 256,
        "CLOPS": 1500,
        "Año_dato": 2024,
    },
    {
        "Sistema": "Google Willow",
        "Plataforma": "Superconductor",
        "Qubits": 105,
        "T1_us": 80,
        "T2_us": 65,
        "Error_1Q": 1e-4,
        "Error_2Q": 2e-3,
        "Readout_%": 1.0,
        "QV": None,
        "CLOPS": 5000,
        "Año_dato": 2024,
    },
    {
        "Sistema": "Quantinuum H2-1",
        "Plataforma": "Trampa de iones",
        "Qubits": 56,
        "T1_us": 1_000_000,
        "T2_us": 1_000_000,
        "Error_1Q": 3e-5,
        "Error_2Q": 1e-3,
        "Readout_%": 0.1,
        "QV": 524288,
        "CLOPS": 100,
        "Año_dato": 2024,
    },
    {
        "Sistema": "IonQ Forte",
        "Plataforma": "Trampa de iones",
        "Qubits": 35,
        "T1_us": 1_000_000,
        "T2_us": 50_000,
        "Error_1Q": 3e-4,
        "Error_2Q": 2e-3,
        "Readout_%": 0.4,
        "QV": 8192,
        "CLOPS": 200,
        "Año_dato": 2024,
    },
    {
        "Sistema": "QuEra Aquila",
        "Plataforma": "Átomos neutros",
        "Qubits": 256,
        "T1_us": 3_000_000,
        "T2_us": 2_000_000,
        "Error_1Q": None,
        "Error_2Q": 3e-3,
        "Readout_%": 2.0,
        "QV": None,
        "CLOPS": 50,
        "Año_dato": 2024,
    },
]

df = pd.DataFrame(HARDWARE_DATA)

# ── Filtros ────────────────────────────────────────────────────────────────
col_filter1, col_filter2 = st.columns(2)
with col_filter1:
    plataformas = ["Todas"] + sorted(df["Plataforma"].unique())
    plataforma_sel = st.selectbox("Filtrar por plataforma", plataformas)
with col_filter2:
    metrica_color = st.selectbox(
        "Colorear por métrica",
        ["Error_2Q", "QV", "CLOPS", "T1_us"],
    )

df_filtered = df if plataforma_sel == "Todas" else df[df["Plataforma"] == plataforma_sel]

# ── Tabla con formato ──────────────────────────────────────────────────────
st.subheader("Tabla comparativa")


def fmt_sci(x):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "N/A"
    return f"{x:.1e}"


def fmt_t1(us):
    if us >= 1_000_000:
        return f"{us/1_000_000:.0f} s"
    elif us >= 1_000:
        return f"{us/1_000:.0f} ms"
    return f"{us:.0f} μs"


display_df = df_filtered.copy()
display_df["Error 1Q"] = display_df["Error_1Q"].apply(fmt_sci)
display_df["Error 2Q"] = display_df["Error_2Q"].apply(fmt_sci)
display_df["T1"] = display_df["T1_us"].apply(fmt_t1)
display_df["T2"] = display_df["T2_us"].apply(fmt_t1)
display_df["Readout"] = display_df["Readout_%"].apply(lambda x: f"{x:.1f}%" if x else "N/A")
display_df["QV"] = display_df["QV"].apply(lambda x: f"{int(x):,}" if x else "N/A")
display_df["CLOPS"] = display_df["CLOPS"].apply(lambda x: f"{int(x):,}")

st.dataframe(
    display_df[["Sistema", "Plataforma", "Qubits", "T1", "T2", "Error 1Q", "Error 2Q", "Readout", "QV", "CLOPS"]],
    use_container_width=True,
    hide_index=True,
)

# ── Gráficos ───────────────────────────────────────────────────────────────
st.subheader("Comparativa visual")

tab1, tab2, tab3, tab4 = st.tabs(["Error 2Q vs Umbral", "QV vs CLOPS", "Coherencia", "Evolución histórica"])

PLATFORM_COLORS = {
    "Superconductor": "#4C72B0",
    "Trampa de iones": "#DD8452",
    "Átomos neutros": "#55A868",
}

with tab1:
    st.markdown("El **umbral del código de superficie** (~1%) y del **código tórico** (~10.9%) se indican como líneas de referencia.")
    fig, ax = plt.subplots(figsize=(10, 5))

    df_plot = df_filtered.dropna(subset=["Error_2Q"])
    colors = [PLATFORM_COLORS.get(p, "gray") for p in df_plot["Plataforma"]]
    bars = ax.barh(df_plot["Sistema"], df_plot["Error_2Q"] * 100, color=colors, alpha=0.85, edgecolor="white")

    # Umbrales
    ax.axvline(1.0, color="red", ls="--", lw=2, label="Umbral surface code (~1%)")
    ax.axvline(10.9, color="orange", ls="--", lw=1.5, label="Umbral tórico ideal (~10.9%)")
    ax.axvline(0.1, color="green", ls=":", lw=1.5, label="Objetivo FT (~0.1%)")

    ax.set_xlabel("Error de puerta 2Q (%)", fontsize=11)
    ax.set_title("Error de puerta 2Q — Comparativa 2025", fontsize=12)
    ax.legend(loc="lower right", fontsize=9)
    ax.set_xscale("log")

    # Leyenda de plataformas
    for plat, color in PLATFORM_COLORS.items():
        ax.bar(0, 0, color=color, alpha=0.85, label=plat)
    ax.legend(loc="lower right", fontsize=9)
    plt.tight_layout()

    export_figure_button(fig, "error_2q_comparativa.png")
    st.pyplot(fig)

with tab2:
    st.markdown("**Quantum Volume** (complejidad ejecutable) vs **CLOPS** (throughput). Nota: Google usa XEB en lugar de QV.")
    df_qv = df_filtered.dropna(subset=["QV"])

    fig, ax = plt.subplots(figsize=(9, 5))
    for _, row in df_qv.iterrows():
        color = PLATFORM_COLORS.get(row["Plataforma"], "gray")
        ax.scatter(row["CLOPS"], row["QV"], s=150, color=color, zorder=3,
                   label=row["Plataforma"] if row["Plataforma"] not in [t.get_label() for t in ax.get_children()] else "")
        ax.annotate(row["Sistema"].split("(")[0].strip(),
                    (row["CLOPS"], row["QV"]),
                    textcoords="offset points", xytext=(8, 4), fontsize=8)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("CLOPS (circuitos/segundo)", fontsize=11)
    ax.set_ylabel("Quantum Volume", fontsize=11)
    ax.set_title("QV vs CLOPS — Frontera rendimiento/throughput", fontsize=12)
    ax.grid(True, which="both", alpha=0.3)

    handles = [plt.scatter([], [], color=c, s=100, label=p) for p, c in PLATFORM_COLORS.items()]
    ax.legend(handles=handles, fontsize=9)
    plt.tight_layout()

    export_figure_button(fig, "qv_vs_clops.png")
    st.pyplot(fig)

with tab3:
    st.markdown("**T1** (tiempo de relajación de energía) y **T2** (tiempo de decoherencia de fase). Los iones tienen tiempos ~10⁴× mayores que superconductores.")
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    df_t = df_filtered.copy()
    df_t["T1_ms"] = df_t["T1_us"] / 1000
    df_t["T2_ms"] = df_t["T2_us"] / 1000
    colors_t = [PLATFORM_COLORS.get(p, "gray") for p in df_t["Plataforma"]]

    axes[0].barh(df_t["Sistema"], df_t["T1_ms"], color=colors_t, alpha=0.85)
    axes[0].set_xscale("log")
    axes[0].set_xlabel("T1 (ms)", fontsize=10)
    axes[0].set_title("Tiempo de relajación T1", fontsize=11)
    axes[0].grid(True, axis="x", alpha=0.3)

    axes[1].barh(df_t["Sistema"], df_t["T2_ms"], color=colors_t, alpha=0.85)
    axes[1].set_xscale("log")
    axes[1].set_xlabel("T2 (ms)", fontsize=10)
    axes[1].set_title("Tiempo de decoherencia T2", fontsize=11)
    axes[1].grid(True, axis="x", alpha=0.3)

    plt.tight_layout()
    export_figure_button(fig, "coherencia_t1_t2.png")
    st.pyplot(fig)

with tab4:
    st.markdown("Evolución del error de puerta 2Q a lo largo del tiempo. La mejora ha sido de ~20× en 6 años para superconductores.")

    hist_data = {
        "Año": [2019, 2021, 2023, 2025],
        "IBM Eagle/Heron": [1e-2, 7e-3, 5e-3, 5e-4],
        "Google Sycamore/Willow": [6e-3, 5e-3, 3e-3, 2e-3],
        "IonQ": [5e-3, 3e-3, 2e-3, 1e-3],
        "Quantinuum": [None, 2e-3, 1.5e-3, 1e-3],
    }

    fig, ax = plt.subplots(figsize=(10, 5))
    linestyles = ["-o", "-s", "-^", "-D"]
    for (col, ls) in zip(list(hist_data.keys())[1:], linestyles):
        vals = hist_data[col]
        años = hist_data["Año"]
        # Filtrar None
        valid = [(a, v) for a, v in zip(años, vals) if v is not None]
        if valid:
            ax.semilogy([a for a, v in valid], [v for a, v in valid],
                        ls, lw=2, ms=8, label=col)

    ax.axhline(0.01, color="red", ls="--", alpha=0.7, label="Umbral surface code 1%")
    ax.axhline(0.001, color="green", ls=":", alpha=0.7, label="Objetivo FT 0.1%")
    ax.set_xlabel("Año", fontsize=11)
    ax.set_ylabel("Error puerta 2Q", fontsize=11)
    ax.set_title("Evolución del error de puerta 2Q (2019–2025)", fontsize=12)
    ax.legend(fontsize=9)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0e}"))
    ax.set_xticks([2019, 2021, 2023, 2025])
    ax.grid(True, which="both", alpha=0.3)
    plt.tight_layout()

    export_figure_button(fig, "evolucion_error_historica.png")
    st.pyplot(fig)

# ── Calculadora de overhead FT ─────────────────────────────────────────────
st.subheader("🔧 Calculadora de overhead fault-tolerant")
st.markdown("¿Cuántos qubits físicos necesitas para proteger 1 qubit lógico con el código de superficie?")

col_calc1, col_calc2, col_calc3 = st.columns(3)
with col_calc1:
    p_phys = st.slider("Error físico p (%)", min_value=0.05, max_value=2.0, value=0.1, step=0.05) / 100
with col_calc2:
    target_logical = st.select_slider(
        "Error lógico objetivo P_L",
        options=[1e-3, 1e-4, 1e-6, 1e-9, 1e-12],
        value=1e-6,
        format_func=lambda x: f"10^{int(np.log10(x))}",
    )
with col_calc3:
    p_th = st.number_input("Umbral del código p_th (%)", value=1.0, min_value=0.5, max_value=5.0, step=0.1) / 100

if p_phys >= p_th:
    st.error(f"⚠️ p_físico ({p_phys*100:.2f}%) ≥ umbral ({p_th*100:.1f}%). No hay corrección posible.")
else:
    ratio = p_phys / p_th
    # P_L ≈ A * (p/p_th)^((d+1)/2), A ≈ 0.1, d = L
    # Despejar d: log(P_L/A) / log(ratio) = (d+1)/2
    import math
    A = 0.1
    d_needed = max(3, 2 * math.ceil(math.log(target_logical / A) / math.log(ratio)) - 1)
    if d_needed % 2 == 0:
        d_needed += 1  # distancia impar
    qubits_physical = 2 * d_needed**2 - 1  # fórmula surface code estándar

    col_r1, col_r2, col_r3, col_r4 = st.columns(4)
    col_r1.metric("Distancia mínima d", d_needed)
    col_r2.metric("Qubits físicos", f"{qubits_physical:,}")
    col_r3.metric("Overhead (÷ 1 qubit lógico)", f"×{qubits_physical:,}")
    col_r4.metric("P_L estimada", f"≤ 10^{int(np.log10(target_logical))}")

    st.info(
        f"Con error físico **p = {p_phys*100:.2f}%** y código de superficie (umbral {p_th*100:.1f}%), "
        f"se necesita distancia **d = {d_needed}** → **{qubits_physical:,} qubits físicos** "
        f"para mantener 1 qubit lógico con $P_L \\leq 10^{{{int(np.log10(target_logical))}}}$."
    )

# ── Nota al pie ─────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "Datos actualizados a abril 2025. Las métricas de hardware cuántico cambian frecuentemente. "
    "Fuentes: IBM Quantum, Google Quantum AI, IonQ, Quantinuum, QuEra. "
    "Ver `docs/error_rates_2025.md` para referencias primarias."
)
