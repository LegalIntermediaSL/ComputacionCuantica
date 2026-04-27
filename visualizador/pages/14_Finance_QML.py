"""
Página 14 — Finance & QML Dashboard
Portafolios cuánticos, QAE Monte Carlo y kernel cuántico interactivo.
"""

import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp
from qiskit.primitives import StatevectorEstimator
from scipy.optimize import minimize

from tour_guide import show_tour, export_figure_button

st.set_page_config(page_title="Finance & QML Dashboard", layout="wide")
st.title("💹 Quantum Finance & QML Dashboard")
st.markdown(
    "Explora **optimización de portafolios cuántica** con QAOA y compara "
    "**kernels cuánticos vs clásicos** para clasificación."
)

_TOUR_STEPS = [
    {"title": "💹 Quantum Finance", "body": "QAOA puede resolver problemas de optimización discreta como la selección de portafolio (qué activos comprar) mapeando la función objetivo media-varianza a un Hamiltoniano de Ising."},
    {"title": "📈 Optimización de portafolio", "body": "Selecciona el número de activos disponibles y la aversión al riesgo λ. El problema binario es: min -μ·x + λ·x^T·Σ·x con x∈{0,1}^n, resuelto con QAOA p=1."},
    {"title": "🔬 Kernel cuántico", "body": "El ZZFeatureMap mapea datos clásicos a un espacio de Hilbert cuántico. El kernel K(x,x') = |⟨ϕ(x')|ϕ(x)⟩|² puede superar al RBF en datos con estructura cuántica."},
    {"title": "📊 Comparativa de kernels", "body": "Compara KTA (Kernel-Target Alignment) del cuántico vs RBF. Un KTA alto indica que el kernel se alinea bien con las etiquetas y generalizará mejor."},
    {"title": "🖼️ Exportar", "body": "Descarga el gráfico de frontera eficiente o el heatmap del kernel como PNG."},
]
show_tour("finance_qml", _TOUR_STEPS)

tab1, tab2 = st.tabs(["💹 Portafolio QAOA", "🔬 Kernel Cuántico"])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — PORTAFOLIO QAOA
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    st.subheader("Optimización de portafolio con QAOA")
    col_ctrl, col_res = st.columns([1, 2])

    with col_ctrl:
        n_activos = st.slider("Número de activos", 3, 6, 4)
        risk_aversion = st.slider("Aversión al riesgo λ", 0.1, 2.0, 0.5, 0.1)
        p_qaoa = st.slider("Capas QAOA (p)", 1, 3, 1)
        seed_finance = st.number_input("Semilla aleatoria", 0, 999, 42)

    rng = np.random.default_rng(int(seed_finance))
    nombres = ["Tech", "Energy", "Finance", "Health", "Consumer", "Utilities"][:n_activos]

    # Datos sintéticos: retornos y correlación
    mu = rng.uniform(0.05, 0.15, n_activos)
    vol = rng.uniform(0.10, 0.25, n_activos)
    corr = np.eye(n_activos)
    for i in range(n_activos):
        for j in range(i+1, n_activos):
            c = rng.uniform(0.1, 0.6)
            corr[i, j] = corr[j, i] = c
    sigma_mat = np.outer(vol, vol) * corr

    # QUBO → Hamiltoniano Ising
    def portfolio_hamiltonian(mu, sigma_mat, lam):
        n = len(mu)
        terms = []
        # Diagonal: -μ_i·Z_i/2 + λ·Σ_ii/4
        for i in range(n):
            coef = -mu[i] / 2 + lam * sigma_mat[i, i] / 4
            terms.append(('I'*i + 'Z' + 'I'*(n-i-1), coef))
        # Off-diagonal: λ·Σ_ij/4·Z_iZ_j
        for i in range(n):
            for j in range(i+1, n):
                coef = lam * sigma_mat[i, j] / 4
                op = 'I'*i + 'Z' + 'I'*(j-i-1) + 'Z' + 'I'*(n-j-1)
                terms.append((op, coef))
        return SparsePauliOp.from_list(terms)

    H_port = portfolio_hamiltonian(mu, sigma_mat, risk_aversion)

    # QAOA p=1 simplificado: barrer gamma,beta
    def qaoa_expectation(params, H, n):
        gammas = params[:p_qaoa]
        betas  = params[p_qaoa:]
        qc = QuantumCircuit(n)
        qc.h(range(n))
        for layer in range(p_qaoa):
            # Cost layer
            for i in range(n):
                for j in range(i+1, n):
                    coef = float(risk_aversion * sigma_mat[i, j] / 4)
                    if abs(coef) > 1e-10:
                        qc.cx(i, j); qc.rz(2 * gammas[layer] * coef, j); qc.cx(i, j)
            # Mixer layer
            for q in range(n):
                qc.rx(2 * betas[layer], q)
        sv = Statevector(qc)
        return sv.expectation_value(H).real

    result = minimize(
        lambda p: qaoa_expectation(p, H_port, n_activos),
        x0=np.random.uniform(0, np.pi, 2*p_qaoa),
        method='COBYLA', options={'maxiter': 200}
    )

    # Mejor solución binaria
    qc_opt = QuantumCircuit(n_activos)
    qc_opt.h(range(n_activos))
    gammas_opt = result.x[:p_qaoa]; betas_opt = result.x[p_qaoa:]
    for layer in range(p_qaoa):
        for i in range(n_activos):
            for j in range(i+1, n_activos):
                coef = float(risk_aversion * sigma_mat[i, j] / 4)
                if abs(coef) > 1e-10:
                    qc_opt.cx(i, j); qc_opt.rz(2*gammas_opt[layer]*coef, j); qc_opt.cx(i, j)
        for q in range(n_activos):
            qc_opt.rx(2*betas_opt[layer], q)

    sv_opt = Statevector(qc_opt)
    probs = np.abs(sv_opt.data)**2
    best_idx = int(np.argmax(probs))
    best_bits = format(best_idx, f'0{n_activos}b')
    seleccion = [nombres[i] for i, b in enumerate(reversed(best_bits)) if b == '1']

    retorno_sel = float(np.dot([int(b) for b in reversed(best_bits)], mu))
    riesgo_sel  = float(np.dot([int(b) for b in reversed(best_bits)],
                               sigma_mat @ [int(b) for b in reversed(best_bits)]))

    with col_res:
        st.markdown(f"**Activos seleccionados:** {', '.join(seleccion) if seleccion else 'Ninguno'}")
        m1, m2, m3 = st.columns(3)
        m1.metric("Retorno esperado", f"{retorno_sel*100:.1f}%")
        m2.metric("Riesgo (varianza)", f"{riesgo_sel:.4f}")
        m3.metric("Ratio Sharpe aprox.", f"{retorno_sel/max(riesgo_sel**0.5, 1e-6):.2f}")

        # Gráfica distribución de probabilidades QAOA
        fig_q, ax_q = plt.subplots(figsize=(8, 3.5))
        top_k = 8
        top_idx = np.argsort(probs)[-top_k:][::-1]
        labels = [format(i, f'0{n_activos}b') for i in top_idx]
        colors = ['#1f77b4' if i == best_idx else '#aec7e8' for i in top_idx]
        ax_q.bar(range(top_k), probs[top_idx], color=colors, edgecolor='k', lw=0.5)
        ax_q.set_xticks(range(top_k)); ax_q.set_xticklabels(labels, rotation=45, fontsize=9)
        ax_q.set_ylabel("Probabilidad"); ax_q.set_title("Top estados QAOA (azul = seleccionado)")
        ax_q.grid(alpha=0.25, axis='y')
        plt.tight_layout(); st.pyplot(fig_q)
        export_figure_button(fig_q, "qaoa_portfolio.png")

    # Frontera eficiente
    st.subheader("Frontera eficiente (Markowitz clásica)")
    n_pt = 100
    retornos_fe = []; riesgos_fe = []
    for lam_fe in np.linspace(0.01, 5.0, n_pt):
        # Greedy: seleccionar activos con mayor ratio μ/σ² dado λ
        scores = mu - lam_fe * np.diag(sigma_mat)
        sel = (scores > 0).astype(float)
        if sel.sum() == 0:
            sel[np.argmax(scores)] = 1.0
        r = float(np.dot(sel, mu)); v = float(sel @ sigma_mat @ sel)
        retornos_fe.append(r); riesgos_fe.append(np.sqrt(v))

    fig_fe, ax_fe = plt.subplots(figsize=(8, 4))
    ax_fe.plot(riesgos_fe, [r*100 for r in retornos_fe], 'b-', lw=2, label='Frontera eficiente')
    ax_fe.scatter([riesgo_sel**0.5], [retorno_sel*100], c='red', s=120, zorder=5, label='QAOA')
    ax_fe.set_xlabel("Riesgo (σ)"); ax_fe.set_ylabel("Retorno esperado (%)")
    ax_fe.set_title("Frontera eficiente + selección QAOA"); ax_fe.legend(); ax_fe.grid(alpha=0.3)
    plt.tight_layout(); st.pyplot(fig_fe)
    export_figure_button(fig_fe, "frontera_eficiente.png")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — KERNEL CUÁNTICO
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.subheader("Kernel cuántico ZZFeatureMap vs RBF")

    col_kctrl, col_kres = st.columns([1, 2])
    with col_kctrl:
        n_samples_k = st.slider("Puntos de entrenamiento", 20, 60, 30, step=5)
        noise_k     = st.slider("Ruido en los datos", 0.05, 0.30, 0.12, step=0.05)
        reps_k      = st.slider("Repeticiones ZZFeatureMap", 1, 3, 2)
        seed_k      = st.number_input("Semilla (kernel)", 0, 999, 7, key="seed_k")

    from sklearn.datasets import make_moons
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.svm import SVC
    from sklearn.metrics import accuracy_score
    from sklearn.model_selection import train_test_split

    X_k, y_k = make_moons(n_samples=n_samples_k, noise=float(noise_k), random_state=int(seed_k))
    scaler_k = MinMaxScaler((0, np.pi))
    X_ks = scaler_k.fit_transform(X_k)
    X_tr, X_te, y_tr, y_te = train_test_split(X_ks, y_k, test_size=0.3, random_state=42)

    @st.cache_data(show_spinner=False)
    def compute_quantum_kernel(X1, X2, reps):
        def zz_fm(x, reps):
            d = len(x)
            qc = QuantumCircuit(d)
            for _ in range(reps):
                for i in range(d):
                    qc.h(i); qc.rz(2*x[i], i)
                for i in range(d):
                    for j in range(i+1, d):
                        v = 2*(np.pi-x[i])*(np.pi-x[j])
                        qc.cx(i,j); qc.rz(v,j); qc.cx(i,j)
            return qc
        K = np.zeros((len(X1), len(X2)))
        svs = [Statevector(zz_fm(x, reps)) for x in X2]
        for i, xi in enumerate(X1):
            sv_i = Statevector(zz_fm(xi, reps))
            for j, sv_j in enumerate(svs):
                K[i, j] = abs(sv_j.inner(sv_i))**2
        return K

    with st.spinner("Calculando kernel cuántico…"):
        K_tr = compute_quantum_kernel(tuple(map(tuple, X_tr)), tuple(map(tuple, X_tr)), reps_k)
        K_te = compute_quantum_kernel(tuple(map(tuple, X_te)), tuple(map(tuple, X_tr)), reps_k)

    svm_q   = SVC(kernel='precomputed').fit(K_tr, y_tr)
    svm_rbf = SVC(kernel='rbf', gamma='scale').fit(X_tr, y_tr)

    acc_q   = accuracy_score(y_te, svm_q.predict(K_te))
    acc_rbf = accuracy_score(y_te, svm_rbf.predict(X_te))

    def kta(K, y):
        Y = np.outer(2*y-1, 2*y-1).astype(float)
        return np.sum(K*Y) / (np.linalg.norm(K,'fro') * np.linalg.norm(Y,'fro') + 1e-12)

    K_rbf_mat = np.exp(-0.5 * np.sum((X_tr[:,None]-X_tr[None,:])**2, axis=-1))
    kta_q   = kta(K_tr, y_tr)
    kta_rbf = kta(K_rbf_mat, y_tr)

    with col_kres:
        df_acc = pd.DataFrame({
            "Modelo": ["Kernel cuántico (ZZFeatureMap)", "Kernel RBF"],
            "Accuracy test": [f"{acc_q:.3f}", f"{acc_rbf:.3f}"],
            "KTA": [f"{kta_q:.4f}", f"{kta_rbf:.4f}"]
        })
        st.dataframe(df_acc, use_container_width=True)

        fig_k, axes_k = plt.subplots(1, 2, figsize=(10, 4))

        # Heatmap del kernel cuántico
        n_show = min(20, len(K_tr))
        im = axes_k[0].imshow(K_tr[:n_show, :n_show], cmap='Blues', vmin=0, vmax=1)
        plt.colorbar(im, ax=axes_k[0])
        axes_k[0].set_title(f'Kernel cuántico K[i,j]\n(primeros {n_show} puntos)')
        axes_k[0].set_xlabel('j'); axes_k[0].set_ylabel('i')

        # Comparativa KTA
        axes_k[1].bar(['Cuántico', 'RBF'], [kta_q, kta_rbf],
                       color=['royalblue', 'tomato'], edgecolor='k')
        axes_k[1].set_ylabel('Kernel Target Alignment')
        axes_k[1].set_title('KTA: cuántico vs RBF\n(mayor = mejor alineación con etiquetas)')
        axes_k[1].grid(alpha=0.3, axis='y')

        plt.tight_layout(); st.pyplot(fig_k)
        export_figure_button(fig_k, "kernel_cuantico_kta.png")

    with st.expander("📚 ¿Cuándo supera el kernel cuántico al RBF?"):
        st.markdown("""
**Ventaja teórica** (Huang et al., *Nature Commun.* 2021):
- El kernel cuántico supera al RBF cuando los datos tienen **estructura cuántica intrínseca**.
- Para datos clásicos estándar (moons, circles), el RBF suele ser competitivo.

**Métricas:**
- **KTA > 0**: el kernel se alinea con las etiquetas → buena generalización.
- **KTA cuántico > KTA RBF**: usar kernel cuántico.
- **Barren plateaus**: para muchas repeticiones, el KTA → 0 exponencialmente (Thanasilp 2022).

**Coste computacional:**
- Kernel cuántico: O(N² · 2^d) — solo práctico para N ≤ 200 y d ≤ 8.
- Para datasets grandes: usar quantum feature map con circuitos de profundidad fija.
""")
