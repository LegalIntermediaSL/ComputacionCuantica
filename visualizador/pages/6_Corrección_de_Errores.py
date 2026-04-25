"""Corrección de errores cuánticos interactiva — código de repetición y código de Shor."""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

st.set_page_config(page_title="Corrección de Errores", layout="wide")
st.title("Corrección de errores cuánticos")
st.markdown(
    "Observa cómo los códigos de corrección de errores protegen la información cuántica "
    "frente a errores de bit-flip y phase-flip."
)

# ─── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Parámetros")
    codigo = st.selectbox(
        "Código",
        ["Repetición 3-qubit (bit-flip)", "Repetición 3-qubit (phase-flip)", "Shor 9-qubit"],
    )
    p_error = st.slider("Tasa de error física ε por qubit", 0.0, 0.5, 0.05, step=0.01)
    shots = st.slider("Experimentos (shots)", 200, 5000, 1000, step=200)
    mostrar_circuito = st.checkbox("Mostrar circuito de codificación", value=True)

# ─── Umbral teórico ──────────────────────────────────────────────────────────
p_th_rep = 0.5    # código de repetición 3q
p_th_shor = 0.5   # aprox. para Shor

def p_logico_repeticion(p: float) -> float:
    """Error lógico del código de repetición 3 qubits: falla si ≥2 qubits fallan."""
    return 3 * p**2 * (1 - p) + p**3

def p_logico_shor(p: float) -> float:
    """Estimación del error lógico del código de Shor 9 qubits."""
    # Shor = 3 bloques de fase-flip x 3 bits de repetición
    p_block = p_logico_repeticion(p)
    return p_logico_repeticion(p_block)

# ─── Circuitos ──────────────────────────────────────────────────────────────
def circuito_bit_flip() -> QuantumCircuit:
    qc = QuantumCircuit(3, name="Cod. bit-flip")
    qc.h(0)           # estado |+> a proteger
    qc.cx(0, 1)
    qc.cx(0, 2)
    return qc

def circuito_phase_flip() -> QuantumCircuit:
    qc = QuantumCircuit(3, name="Cod. phase-flip")
    qc.h(0)
    qc.cx(0, 1); qc.cx(0, 2)
    qc.h(0); qc.h(1); qc.h(2)
    return qc

def circuito_shor() -> QuantumCircuit:
    qc = QuantumCircuit(9, name="Cod. Shor")
    qc.h(0)
    # Codificación de phase-flip (3 bloques)
    qc.cx(0, 3); qc.cx(0, 6)
    qc.h(0); qc.h(3); qc.h(6)
    # Codificación de bit-flip dentro de cada bloque
    for base in [0, 3, 6]:
        qc.cx(base, base+1); qc.cx(base, base+2)
    return qc

# ─── Simulación Monte Carlo ──────────────────────────────────────────────────
def simular_errores(codigo_str: str, p: float, n_shots: int):
    """Simula errores y corrección, devuelve (error_sin_qec, error_con_qec)."""
    rng = np.random.default_rng(42)
    errores_logicos_sin = 0
    errores_logicos_con = 0

    if "Shor" in codigo_str:
        n_qubits = 9
    else:
        n_qubits = 3

    for _ in range(n_shots):
        # Generar errores aleatorios
        errores = rng.random(n_qubits) < p

        # Sin QEC: error lógico si el qubit 0 falla (simplificado)
        if errores[0]:
            errores_logicos_sin += 1

        # Con QEC: corrección por mayoría de votos
        if "Shor" in codigo_str:
            # Shor: 3 bloques de 3 qubits, luego corrección externa
            bloques = [errores[i:i+3] for i in range(0, 9, 3)]
            bits_corregidos = []
            for bloque in bloques:
                voto = int(sum(bloque) >= 2)
                bits_corregidos.append(voto)
            error_logico = int(sum(bits_corregidos) >= 2)
        else:
            # Repetición: error lógico si ≥2 qubits fallan
            error_logico = int(sum(errores) >= 2)

        errores_logicos_con += error_logico

    return errores_logicos_sin / n_shots, errores_logicos_con / n_shots

# ─── Interfaz principal ──────────────────────────────────────────────────────
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Circuito de codificación")
    if mostrar_circuito:
        if "Shor" in codigo:
            qc_viz = circuito_shor()
        elif "phase-flip" in codigo:
            qc_viz = circuito_phase_flip()
        else:
            qc_viz = circuito_bit_flip()

        try:
            fig_circ, ax_circ = plt.subplots(figsize=(7, 3))
            qc_viz.draw("mpl", ax=ax_circ, style="iqp")
            st.pyplot(fig_circ)
            plt.close(fig_circ)
        except Exception:
            st.code(qc_viz.draw("text"), language="text")

    # Métricas para p actual
    if "Shor" in codigo:
        p_L = p_logico_shor(p_error)
        n_q = 9
        desc = "[[9,1,3]] — protege contra 1 error X o Z en cualquier qubit"
    else:
        p_L = p_logico_repeticion(p_error)
        n_q = 3
        desc = "[[3,1,1]] — protege contra 1 error de bit-flip o phase-flip"

    st.info(f"**{codigo}** · {desc}")
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Qubits físicos", n_q)
    col_m2.metric("Error lógico p_L", f"{p_L:.4f}")
    col_m3.metric("Reducción vs. sin QEC", f"{(1 - p_L/max(p_error,1e-9))*100:.1f}%"
                  if p_error > 0 else "—")

with col2:
    st.subheader("Error lógico vs. error físico")
    p_vals = np.linspace(0, 0.5, 200)

    if "Shor" in codigo:
        p_L_vals = [p_logico_shor(p) for p in p_vals]
    else:
        p_L_vals = [p_logico_repeticion(p) for p in p_vals]

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(p_vals, p_vals, "--", color="gray", alpha=0.6, label="Sin QEC (p_L = ε)")
    ax.plot(p_vals, p_L_vals, color="#e74c3c", linewidth=2, label="Con QEC")
    ax.axvline(x=p_error, color="#3498db", linestyle=":", linewidth=1.5,
               label=f"ε actual = {p_error:.2f}")
    ax.scatter([p_error], [p_logico_shor(p_error) if "Shor" in codigo
                           else p_logico_repeticion(p_error)],
               color="#e74c3c", s=80, zorder=5)
    ax.set_xlabel("Error físico ε")
    ax.set_ylabel("Error lógico $p_L$")
    ax.set_title("Curva de protección del código")
    ax.legend(); ax.grid(alpha=0.3)
    ax.set_xlim(0, 0.5); ax.set_ylim(0, 0.5)

    # Zona de protección
    ax.fill_between(p_vals, p_vals, p_L_vals,
                    where=[pL < p for pL, p in zip(p_L_vals, p_vals)],
                    alpha=0.15, color="green", label="Zona protegida")
    st.pyplot(fig)
    plt.close(fig)

# ─── Simulación estadística ──────────────────────────────────────────────────
st.divider()
st.subheader("Simulación estadística de errores")

if st.button("Simular errores", type="primary"):
    with st.spinner(f"Simulando {shots} experimentos..."):
        p_sin, p_con = simular_errores(codigo, p_error, shots)

    col_s1, col_s2, col_s3 = st.columns(3)
    col_s1.metric("Error empírico sin QEC", f"{p_sin:.4f}",
                  delta=f"teórico: {p_error:.4f}", delta_color="off")
    col_s2.metric("Error empírico con QEC", f"{p_con:.4f}",
                  delta=f"teórico: {p_logico_shor(p_error) if 'Shor' in codigo else p_logico_repeticion(p_error):.4f}",
                  delta_color="off")
    mejora = (p_sin - p_con) / max(p_sin, 1e-9) * 100
    col_s3.metric("Mejora relativa", f"{mejora:.1f}%",
                  delta="QEC ayuda" if p_error < 0.5 else "sobre umbral")

# ─── Descripción analítica ──────────────────────────────────────────────────
st.divider()
with st.expander("Fórmulas del error lógico"):
    st.markdown(
        r"""
        **Código de repetición 3-qubit:**
        $$p_L = 3\varepsilon^2(1-\varepsilon) + \varepsilon^3 = \binom{3}{2}\varepsilon^2(1-\varepsilon) + \binom{3}{3}\varepsilon^3$$

        El QEC ayuda cuando $p_L < \varepsilon$, es decir, para $\varepsilon < 0.5$ (umbral).

        **Código de Shor 9-qubit:**
        $$p_L^{\text{Shor}} \approx p_L^{\text{rep}}\left(p_L^{\text{rep}}(\varepsilon)\right)$$

        Concatenar dos códigos de repetición suprime el error más agresivamente cerca del umbral.

        **Código de superficie distancia d (modelo general):**
        $$p_L \approx A \left(\frac{\varepsilon}{\varepsilon_{th}}\right)^{\lceil d/2 \rceil}, \quad \varepsilon_{th} \approx 1\%$$
        """
    )

st.caption("Tutorial: módulos 09_correccion_errores, 14_surface_codes y 29_fault_tolerant_computing")
