"""Optimizador VQE / QAOA interactivo con Qiskit Aer."""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator, StatevectorSampler
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import EfficientSU2

st.set_page_config(page_title="VQE / QAOA Interactivo", layout="wide")
st.title("VQE y QAOA interactivos")

modo = st.sidebar.radio("Algoritmo", ["VQE", "QAOA MaxCut"])

# ─── VQE ────────────────────────────────────────────────────────────────────
if modo == "VQE":
    st.header("VQE: algoritmo variacional cuántico del autovalor")
    st.markdown(
        "VQE minimiza $\\langle\\psi(\\vec{\\theta})|H|\\psi(\\vec{\\theta})\\rangle \\geq E_0$ "
        "variando los parámetros del ansatz con un optimizador clásico."
    )

    with st.sidebar:
        st.subheader("Hamiltoniano H₂ (simplificado)")
        coef_II = st.number_input("Coef. II", value=-1.0523, format="%.4f")
        coef_ZI = st.number_input("Coef. ZI", value=0.3979, format="%.4f")
        coef_IZ = st.number_input("Coef. IZ", value=-0.3979, format="%.4f")
        coef_ZZ = st.number_input("Coef. ZZ", value=-0.0112, format="%.4f")
        coef_XX = st.number_input("Coef. XX", value=0.1809, format="%.4f")
        reps_ansatz = st.slider("Profundidad ansatz (reps)", 1, 4, 2)
        max_iter   = st.slider("Iteraciones máximas", 20, 500, 100)
        optimizadores = st.multiselect(
            "Optimizadores a comparar",
            ["COBYLA", "SPSA", "Nelder-Mead"],
            default=["COBYLA"],
        )

    H = SparsePauliOp.from_list([
        ("II", coef_II), ("ZI", coef_ZI), ("IZ", coef_IZ),
        ("ZZ", coef_ZZ), ("XX", coef_XX),
    ])
    n_qubits = 2
    ansatz = EfficientSU2(n_qubits, reps=reps_ansatz, entanglement="linear")
    estimator = StatevectorEstimator()

    def make_cost_fn(history):
        def cost_fn(params):
            bound = ansatz.assign_parameters(params)
            result = estimator.run([(bound, H)]).result()
            e = float(result[0].data.evs)
            history.append(e)
            return e
        return cost_fn

    def spsa_minimize(cost_fn, x0, max_iter, a=0.2, c=0.1):
        """SPSA simplificado (Simultaneous Perturbation Stochastic Approximation)."""
        x = x0.copy()
        history = []
        for k in range(1, max_iter + 1):
            ak = a / (k + 1) ** 0.602
            ck = c / k ** 0.101
            delta = np.random.choice([-1, 1], size=len(x))
            f_plus  = cost_fn(x + ck * delta)
            f_minus = cost_fn(x - ck * delta)
            grad = (f_plus - f_minus) / (2 * ck * delta)
            x -= ak * grad
            history.append(cost_fn(x))
        return x, min(history)

    if st.button("Ejecutar VQE"):
        if not optimizadores:
            st.warning("Selecciona al menos un optimizador.")
            st.stop()

        resultados = {}
        colors_opt = {"COBYLA": "#3498db", "SPSA": "#e74c3c", "Nelder-Mead": "#2ecc71"}

        with st.spinner("Optimizando..."):
            for opt_name in optimizadores:
                hist = []
                cost = make_cost_fn(hist)
                np.random.seed(42)
                x0 = np.random.uniform(-np.pi, np.pi, ansatz.num_parameters)

                if opt_name == "SPSA":
                    x_opt, e_min = spsa_minimize(cost, x0, max_iter)
                    class FakeResult:
                        fun = e_min
                        success = True
                    res = FakeResult()
                else:
                    method = "cobyla" if opt_name == "COBYLA" else "Nelder-Mead"
                    res = minimize(cost, x0, method=method,
                                   options={"maxiter": max_iter,
                                            **({"rhobeg": 0.5} if opt_name == "COBYLA" else {})})
                resultados[opt_name] = {"history": hist, "res": res}

        col1, col2 = st.columns([2, 1])
        with col1:
            fig, ax = plt.subplots(figsize=(9, 4))
            for opt_name, data in resultados.items():
                color = colors_opt.get(opt_name, "#8e44ad")
                ax.plot(data["history"], color=color, linewidth=1.5, label=opt_name)
                ax.axhline(y=data["res"].fun, color=color, linestyle="--", alpha=0.4)
            ax.axhline(y=-1.8572, color="black", linestyle=":", alpha=0.6, label="FCI ref. −1.8572 Ha")
            ax.set_xlabel("Iteración")
            ax.set_ylabel("⟨H⟩ (Hartree)")
            ax.set_title("Curva de convergencia VQE — comparativa de optimizadores")
            ax.legend(); ax.grid(alpha=0.2)
            st.pyplot(fig)

        with col2:
            best_opt = min(resultados, key=lambda k: resultados[k]["res"].fun)
            res = resultados[best_opt]["res"]
            energy_history = resultados[best_opt]["history"]
            st.metric("Mejor optimizador", best_opt)
            st.metric("Energía mínima encontrada", f"{res.fun:.6f} Ha")
            st.metric("Iteraciones realizadas", len(energy_history))
            st.metric("Convergencia", "Sí" if res.success else "No (max_iter)")
            # Valor teórico para H₂ (STO-3G): ~ -1.8572 Ha
            st.metric("Referencia H₂ (FCI, STO-3G)", "≈ -1.8572 Ha")
            error = abs(res.fun - (-1.8572))
            st.metric("Error frente a FCI", f"{error:.6f} Ha")
    else:
        st.info("Ajusta los parámetros y pulsa **Ejecutar VQE** para iniciar la optimización.")

# ─── QAOA MaxCut ────────────────────────────────────────────────────────────
else:
    st.header("QAOA para MaxCut")
    st.markdown(
        "QAOA resuelve el problema MaxCut en grafos. El Hamiltoniano de coste es "
        "$H_C = \\frac{1}{2}\\sum_{(i,j)\\in E}(I - Z_iZ_j)$. "
        "Cada capa QAOA añade parámetros $(\\gamma_l, \\beta_l)$."
    )

    with st.sidebar:
        st.subheader("Grafo")
        n_nodes = st.slider("Nodos", 3, 6, 4)
        p_layers = st.slider("Capas p", 1, 4, 1)
        max_iter_qaoa = st.slider("Iteraciones máximas", 20, 300, 100)

    st.subheader("Definir aristas del grafo")
    cols_edge = st.columns(4)
    edges = []
    edge_options = [(i, j) for i in range(n_nodes) for j in range(i+1, n_nodes)]
    for k, (i, j) in enumerate(edge_options):
        col = cols_edge[k % 4]
        if col.checkbox(f"({i},{j})", value=(k < n_nodes - 1), key=f"e{i}{j}"):
            edges.append((i, j))

    if not edges:
        st.warning("Añade al menos una arista.")
        st.stop()

    # Visualizar grafo
    fig_g, ax_g = plt.subplots(figsize=(4, 3))
    angles = np.linspace(0, 2 * np.pi, n_nodes, endpoint=False)
    pos = {i: (np.cos(a), np.sin(a)) for i, a in enumerate(angles)}
    for i, j in edges:
        ax_g.plot([pos[i][0], pos[j][0]], [pos[i][1], pos[j][1]], "k-", linewidth=2)
    for i in range(n_nodes):
        ax_g.scatter(*pos[i], s=400, color="#3498db", zorder=5)
        ax_g.text(pos[i][0], pos[i][1], str(i), ha="center", va="center",
                  fontsize=12, color="white", fontweight="bold")
    ax_g.set_xlim(-1.5, 1.5); ax_g.set_ylim(-1.5, 1.5)
    ax_g.axis("off"); ax_g.set_title(f"Grafo ({n_nodes} nodos, {len(edges)} aristas)")
    col_graph, col_run = st.columns([1, 2])
    col_graph.pyplot(fig_g)

    def build_maxcut_qaoa(n: int, edg, p: int) -> QuantumCircuit:
        from qiskit.circuit import ParameterVector
        gammas = ParameterVector("γ", p)
        betas  = ParameterVector("β", p)
        qc = QuantumCircuit(n)
        qc.h(range(n))
        for layer in range(p):
            for i, j in edg:
                qc.rzz(2 * gammas[layer], i, j)
            for q in range(n):
                qc.rx(2 * betas[layer], q)
        return qc, gammas, betas

    def maxcut_hamiltonian(n: int, edg):
        terms = [("I" * n, 0.0)]
        for i, j in edg:
            paulis = list("I" * n)
            paulis[n - 1 - i] = "Z"
            paulis[n - 1 - j] = "Z"
            terms.append(("".join(paulis), -0.5))
        terms[0] = ("I" * n, len(edg) * 0.5)
        return SparsePauliOp.from_list(terms)

    if col_run.button("Ejecutar QAOA"):
        with st.spinner("Optimizando QAOA..."):
            qc_qaoa, gammas, betas = build_maxcut_qaoa(n_nodes, edges, p_layers)
            H_C = maxcut_hamiltonian(n_nodes, edges)
            estimator = StatevectorEstimator()
            history = []

            def qaoa_cost(params):
                bound = qc_qaoa.assign_parameters(params)
                result = estimator.run([(bound, H_C)]).result()
                val = -float(result[0].data.evs)
                history.append(-val)
                return val

            np.random.seed(0)
            x0 = np.random.uniform(0, np.pi, 2 * p_layers)
            res = minimize(qaoa_cost, x0, method="COBYLA",
                           options={"maxiter": max_iter_qaoa})

        col_conv, col_result = st.columns([2, 1])
        with col_conv:
            fig_conv, ax_conv = plt.subplots(figsize=(9, 4))
            ax_conv.plot(history, color="#8e44ad")
            ax_conv.axhline(y=-res.fun, color="#e74c3c", linestyle="--",
                            label=f"⟨H_C⟩_max = {-res.fun:.4f}")
            ax_conv.set_xlabel("Iteración"); ax_conv.set_ylabel("⟨H_C⟩")
            ax_conv.set_title("Curva de convergencia QAOA"); ax_conv.legend()
            st.pyplot(fig_conv)

        with col_result:
            max_cut_theory = len(edges)
            approx_ratio   = -res.fun / max_cut_theory
            st.metric("⟨H_C⟩ máximo encontrado", f"{-res.fun:.4f}")
            st.metric("Corte máximo teórico", max_cut_theory)
            st.metric("Ratio de aproximación", f"{approx_ratio:.4f}")
            st.metric("Parámetros optimizados γ", str([f"{v:.3f}" for v in res.x[:p_layers]]))
            st.metric("Parámetros optimizados β", str([f"{v:.3f}" for v in res.x[p_layers:]]))

        # Distribución del estado final
        st.subheader("Distribución de probabilidades del estado óptimo")
        qc_final = qc_qaoa.assign_parameters(res.x)
        qc_final.measure_all()
        sampler = StatevectorSampler()
        sample_result = sampler.run([qc_final], shots=2048).result()
        counts = sample_result[0].data.meas.get_counts()
        top_states = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:8]
        fig_dist, ax_dist = plt.subplots(figsize=(9, 3))
        ax_dist.bar([s for s, _ in top_states], [c/2048 for _, c in top_states], color="#2ecc71")
        ax_dist.set_xlabel("Bitstring (asignación de corte)"); ax_dist.set_ylabel("Probabilidad")
        ax_dist.set_title("Top estados del estado QAOA óptimo")
        st.pyplot(fig_dist)
    else:
        col_run.info("Pulsa **Ejecutar QAOA** para iniciar la optimización.")

st.caption("Tutorial: módulo 11_algoritmos_variacionales")
