"""Dashboard de hardware cuántico — parámetros representativos 2024."""
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

st.set_page_config(page_title="Hardware Dashboard", layout="wide")
st.title("Dashboard de hardware cuántico")
st.markdown(
    "Parámetros representativos de los principales procesadores superconductores "
    "y comparativa de arquitecturas (datos de referencia 2024, no en tiempo real)."
)

# ─── Datos de procesadores IBM ───────────────────────────────────────────────
PROCESADORES = pd.DataFrame([
    {"Procesador": "IBM Falcon (2019)", "Qubits": 27,  "T1_us": 70,  "T2_us": 80,  "F_1q_pct": 99.7, "F_2q_pct": 99.0, "Año": 2019},
    {"Procesador": "IBM Eagle (2021)",  "Qubits": 127, "T1_us": 100, "T2_us": 90,  "F_1q_pct": 99.8, "F_2q_pct": 99.1, "Año": 2021},
    {"Procesador": "IBM Osprey (2022)", "Qubits": 433, "T1_us": 150, "T2_us": 130, "F_1q_pct": 99.9, "F_2q_pct": 99.3, "Año": 2022},
    {"Procesador": "IBM Condor (2023)", "Qubits": 1121,"T1_us": 200, "T2_us": 150, "F_1q_pct": 99.9, "F_2q_pct": 99.4, "Año": 2023},
    {"Procesador": "IBM Heron (2024)",  "Qubits": 133, "T1_us": 300, "T2_us": 200, "F_1q_pct": 99.95,"F_2q_pct": 99.7, "Año": 2024},
    {"Procesador": "Google Sycamore",   "Qubits": 70,  "T1_us": 100, "T2_us": 80,  "F_1q_pct": 99.8, "F_2q_pct": 99.5, "Año": 2023},
    {"Procesador": "Quantinuum H2",     "Qubits": 56,  "T1_us": 1e6, "T2_us": 1e6, "F_1q_pct": 99.99,"F_2q_pct": 99.8, "Año": 2024},
])

with st.sidebar:
    st.header("Filtros")
    mostrar = st.multiselect(
        "Procesadores a mostrar",
        PROCESADORES["Procesador"].tolist(),
        default=PROCESADORES["Procesador"].tolist(),
    )
    metrica = st.selectbox("Métrica principal", ["T1_us", "T2_us", "F_1q_pct", "F_2q_pct", "Qubits"])
    escala_log_T = st.checkbox("Escala log para T1/T2", value=True)

df = PROCESADORES[PROCESADORES["Procesador"].isin(mostrar)].copy()

# ─── KPIs ────────────────────────────────────────────────────────────────────
st.subheader("Comparativa de procesadores")
col1, col2, col3, col4 = st.columns(4)
best_T1 = df.loc[df["T1_us"].idxmax()]
best_F2 = df.loc[df["F_2q_pct"].idxmax()]
most_Q  = df.loc[df["Qubits"].idxmax()]
with col1:
    st.metric("Mejor T1", f"{best_T1['T1_us']:.0f} μs", best_T1["Procesador"])
with col2:
    st.metric("Mejor F(CNOT)", f"{best_F2['F_2q_pct']:.2f}%", best_F2["Procesador"])
with col3:
    st.metric("Más qubits", int(most_Q["Qubits"]), most_Q["Procesador"])
with col4:
    st.metric("Procesadores seleccionados", len(df))

# ─── Tabla ────────────────────────────────────────────────────────────────────
st.dataframe(
    df[["Procesador", "Año", "Qubits", "T1_us", "T2_us", "F_1q_pct", "F_2q_pct"]]
    .rename(columns={"T1_us": "T1 (μs)", "T2_us": "T2 (μs)",
                     "F_1q_pct": "F 1Q (%)", "F_2q_pct": "F 2Q (%)"}),
    use_container_width=True,
)

# ─── Gráficos ────────────────────────────────────────────────────────────────
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("T1 y T2 por procesador")
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(len(df))
    w = 0.35
    b1 = ax.bar(x - w/2, df["T1_us"], w, label="T1 (μs)", color="#3498db")
    b2 = ax.bar(x + w/2, df["T2_us"], w, label="T2 (μs)", color="#e74c3c")
    ax.set_xticks(x)
    ax.set_xticklabels(df["Procesador"], rotation=35, ha="right", fontsize=8)
    ax.set_ylabel("Tiempo (μs)")
    if escala_log_T:
        ax.set_yscale("log")
    ax.legend()
    ax.set_title("Tiempos de coherencia")
    plt.tight_layout()
    st.pyplot(fig)

with col_g2:
    st.subheader("Fidelidad de puertas")
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.scatter(df["F_1q_pct"], df["F_2q_pct"],
                s=df["Qubits"] / 3, alpha=0.8, color="#8e44ad",
                edgecolors="black", linewidths=0.5)
    for _, row in df.iterrows():
        ax2.annotate(row["Procesador"].split()[1] if " " in row["Procesador"] else row["Procesador"],
                     (row["F_1q_pct"], row["F_2q_pct"]),
                     textcoords="offset points", xytext=(5, 5), fontsize=7)
    ax2.set_xlabel("Fidelidad 1Q (%)")
    ax2.set_ylabel("Fidelidad 2Q (%)")
    ax2.set_title("Fidelidades (tamaño ∝ nº qubits)")
    plt.tight_layout()
    st.pyplot(fig2)

# ─── Tendencia histórica ─────────────────────────────────────────────────────
st.subheader("Tendencia histórica de T1 (IBM)")
ibm = PROCESADORES[PROCESADORES["Procesador"].str.startswith("IBM")]

fig3, ax3 = plt.subplots(figsize=(10, 4))
ax3.plot(ibm["Año"], ibm["T1_us"], "o-", color="#3498db", linewidth=2, markersize=8)
for _, row in ibm.iterrows():
    ax3.annotate(f"{row['T1_us']} μs",
                 (row["Año"], row["T1_us"]),
                 textcoords="offset points", xytext=(5, 8), fontsize=9)
ax3.set_xlabel("Año")
ax3.set_ylabel("T1 (μs)")
ax3.set_title("Mejora de T1 en procesadores IBM (2019-2024)")
ax3.set_xticks(ibm["Año"])
ax3.grid(alpha=0.3)
st.pyplot(fig3)

# ─── Comparativa de arquitecturas ────────────────────────────────────────────
st.subheader("Comparativa de arquitecturas cuánticas")
arq_data = pd.DataFrame([
    {"Arquitectura": "Superconductores", "T2": "50-400 μs",  "F_2Q": ">99%",   "Qubits": "~1000",  "T_puerta_2Q": "100-500 ns", "T_operación": "~20 mK"},
    {"Arquitectura": "Iones atrapados",  "T2": "1-100 s",    "F_2Q": ">99.9%", "Qubits": "~50",    "T_puerta_2Q": "0.1-10 ms",  "T_operación": "μK"},
    {"Arquitectura": "Rydberg",          "T2": "~ms",        "F_2Q": ">99%",   "Qubits": "~1000",  "T_puerta_2Q": "~μs",        "T_operación": "μK"},
    {"Arquitectura": "NV en diamante",   "T2": "ms-s",       "F_2Q": "~95%",   "Qubits": "~10",    "T_puerta_2Q": "~μs",        "T_operación": "Amb./mK"},
    {"Arquitectura": "Fotónica",         "T2": "∞ (tránsito)","F_2Q": "Prob.", "Qubits": "~100s",  "T_puerta_2Q": "N/A",        "T_operación": "Ambiente"},
])
st.dataframe(arq_data, use_container_width=True)

# ─── Calculadora de utilidad ─────────────────────────────────────────────────
st.subheader("Calculadora de profundidad máxima de circuito")
col_c1, col_c2 = st.columns(2)
with col_c1:
    T2_calc = st.number_input("T2 del procesador (μs)", 10.0, 1e6, 200.0, step=10.0)
    t_gate  = st.number_input("Duración de puerta CNOT (ns)", 10.0, 10000.0, 300.0, step=10.0)
with col_c2:
    d_max = T2_calc * 1000 / t_gate  # T2 en ns / t_gate en ns
    st.metric("Profundidad máxima (sin QEC)", f"{d_max:.0f} puertas CNOT")
    shots_rabi = int(T2_calc * 1000 / t_gate)
    eficiencia = min(1.0, d_max / 1000)
    st.metric("Fracción de Shor RSA-2048 (10⁸ gates)", f"{d_max/1e8*100:.6f}%")

st.caption("Tutorial: módulos 23_hardware_fisico_y_arquitecturas y 14_surface_codes")
