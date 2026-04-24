"""Grover y QPE paso a paso con visualización del estado cuántico."""
import streamlit as st
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

st.set_page_config(page_title="Algoritmos Paso a Paso", layout="wide")
st.title("Algoritmos cuánticos paso a paso")

algoritmo = st.sidebar.radio("Algoritmo", ["Grover", "QPE (Phase Estimation)"])

# ─── GROVER ─────────────────────────────────────────────────────────────────
if algoritmo == "Grover":
    st.header("Búsqueda de Grover: evolución geométrica")
    st.markdown(
        "Cada iteración del operador de Grover rota el estado un ángulo $2\\theta$ "
        "hacia el estado objetivo $|w\\rangle$. El número óptimo de iteraciones es "
        "$k_{opt} \\approx \\frac{\\pi}{4}\\sqrt{N}$."
    )

    n_qubits = st.sidebar.slider("Número de qubits", 2, 5, 3)
    N = 2 ** n_qubits
    target = st.sidebar.number_input("Estado objetivo (índice)", 0, N - 1, 0)
    max_iter = int(np.ceil(np.pi / 4 * np.sqrt(N))) + 2
    k_iter = st.sidebar.slider("Número de iteraciones", 0, max_iter, 1)

    def grover_oracle(n: int, target: int) -> QuantumCircuit:
        qc = QuantumCircuit(n)
        target_bits = format(target, f"0{n}b")
        for i, bit in enumerate(reversed(target_bits)):
            if bit == "0":
                qc.x(i)
        qc.h(n - 1)
        qc.mcx(list(range(n - 1)), n - 1)
        qc.h(n - 1)
        for i, bit in enumerate(reversed(target_bits)):
            if bit == "0":
                qc.x(i)
        return qc

    def diffusion(n: int) -> QuantumCircuit:
        qc = QuantumCircuit(n)
        qc.h(range(n))
        qc.x(range(n))
        qc.h(n - 1)
        qc.mcx(list(range(n - 1)), n - 1)
        qc.h(n - 1)
        qc.x(range(n))
        qc.h(range(n))
        return qc

    # Calcular probabilidades en cada iteración
    probs_history = []
    qc = QuantumCircuit(n_qubits)
    qc.h(range(n_qubits))
    sv = Statevector.from_instruction(qc)
    probs_history.append(sv.probabilities())

    for _ in range(k_iter):
        oracle_qc = grover_oracle(n_qubits, target)
        diff_qc = diffusion(n_qubits)
        sv = sv.evolve(oracle_qc)
        sv = sv.evolve(diff_qc)
        probs_history.append(sv.probabilities())

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(f"Probabilidades tras {k_iter} iteraciones")
        probs = probs_history[-1]
        fig, ax = plt.subplots(figsize=(10, 4))
        colors = ["#e74c3c" if i == target else "#3498db" for i in range(N)]
        ax.bar([format(i, f"0{n_qubits}b") for i in range(N)], probs, color=colors)
        ax.set_xlabel("Estado")
        ax.set_ylabel("Probabilidad")
        ax.set_title(f"Distribución de probabilidades (objetivo: |{format(target, f'0{n_qubits}b')}⟩)")
        ax.axhline(y=1/N, color="gray", linestyle="--", alpha=0.5, label="Uniforme 1/N")
        ax.legend()
        plt.xticks(rotation=45)
        st.pyplot(fig)

    with col2:
        st.subheader("Evolución de P(target)")
        fig2, ax2 = plt.subplots(figsize=(5, 4))
        p_target = [p[target] for p in probs_history]
        ax2.plot(range(len(p_target)), p_target, "o-", color="#e74c3c")
        ax2.axhline(y=1/N, color="gray", linestyle="--", alpha=0.5)
        ax2.set_xlabel("Iteraciones")
        ax2.set_ylabel("P(|w⟩)")
        ax2.set_title("Probabilidad del estado objetivo")
        ax2.set_ylim(0, 1.05)
        st.pyplot(fig2)

        k_opt = int(np.round(np.pi / 4 * np.sqrt(N)))
        st.metric("k_opt teórico", k_opt)
        st.metric("P(target) actual", f"{probs_history[-1][target]:.4f}")
        angle = np.arcsin(1 / np.sqrt(N))
        st.metric("θ = arcsin(1/√N)", f"{np.degrees(angle):.2f}°")

# ─── QPE ────────────────────────────────────────────────────────────────────
else:
    st.header("Phase Estimation (QPE): distribución de probabilidades")
    st.markdown(
        "QPE estima la fase $\\phi$ de un unitario $U|u\\rangle = e^{2\\pi i \\phi}|u\\rangle$ "
        "con $t$ qubits de conteo. La probabilidad de estimar la fase correcta es "
        "$P \\geq 8/\\pi^2 \\approx 0.81$ para $t$ suficiente."
    )

    t = st.sidebar.slider("Qubits de conteo (t)", 2, 8, 4)
    phi_real = st.sidebar.slider("Fase real φ (0 a 1)", 0.0, 1.0, 0.25, step=0.01)

    def qpe_circuit(t: int, phi: float) -> QuantumCircuit:
        qc = QuantumCircuit(t + 1, t)
        qc.h(range(t))
        qc.x(t)
        for j in range(t):
            angle = 2 * np.pi * phi * (2 ** j)
            qc.cp(angle, j, t)
        # QFT†
        for j in range(t // 2):
            qc.swap(j, t - 1 - j)
        for j in range(t):
            qc.h(j)
            for k in range(j + 1, t):
                qc.cp(-np.pi / (2 ** (k - j)), j, k)
        qc.measure(range(t), range(t))
        return qc

    from qiskit_aer import AerSimulator
    qc_qpe = qpe_circuit(t, phi_real)
    sim = AerSimulator()
    job = sim.run(qc_qpe, shots=4096)
    counts = job.result().get_counts()

    # Calcular las fases estimadas
    phases = {}
    total_shots = sum(counts.values())
    for bitstring, count in counts.items():
        decimal = int(bitstring, 2) / (2 ** t)
        phases[decimal] = phases.get(decimal, 0) + count / total_shots

    most_likely = max(phases, key=phases.get)
    error = abs(most_likely - phi_real)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Distribución de fases estimadas")
        fig, ax = plt.subplots(figsize=(10, 4))
        sorted_phases = sorted(phases.items())
        ax.bar([f"{p:.3f}" for p, _ in sorted_phases],
               [prob for _, prob in sorted_phases],
               color="#8e44ad")
        ax.axvline(x=str(f"{phi_real:.3f}"), color="red", linestyle="--", alpha=0.7,
                   label=f"φ real = {phi_real:.3f}")
        ax.set_xlabel("Fase estimada φ̃")
        ax.set_ylabel("Probabilidad")
        ax.set_title(f"QPE con t={t} qubits de conteo")
        ax.legend()
        plt.xticks(rotation=45)
        st.pyplot(fig)

    with col2:
        st.subheader("Métricas")
        precision = 1 / (2 ** t)
        st.metric("Precisión teórica 1/2^t", f"{precision:.6f}")
        st.metric("Fase real φ", f"{phi_real:.4f}")
        st.metric("Fase estimada φ̃", f"{most_likely:.4f}")
        st.metric("Error |φ - φ̃|", f"{error:.4f}",
                  delta=f"{'dentro' if error <= precision else 'fuera'} de 1/2^t")
        st.metric("P(mejor estimación)", f"{phases[most_likely]:.4f}")

    st.info(
        f"Con t={t} qubits, la resolución de fase es 1/2^{t} = {precision:.6f}. "
        f"El pico de probabilidad se encuentra en φ̃ = {most_likely:.4f}."
    )

st.caption("Tutorial: módulo 05_algoritmos")
