"""
Página 12 — Landscape de Parámetros VQE/QAOA
Visualiza el paisaje de energía, barren plateaus y comparativa de optimizadores.
"""

import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time

from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorEstimator
from scipy.optimize import minimize

from tour_guide import show_tour

st.set_page_config(page_title="Landscape de Parámetros", layout="wide")
st.title("🗺️ Landscape de Parámetros VQE/QAOA")
st.markdown(
    "Explora el **paisaje de energía** de circuitos variacionales, detecta "
    "**barren plateaus** y compara el rendimiento de diferentes optimizadores."
)

_TOUR_STEPS = [
    {"title": "🗺️ Landscape de parámetros", "body": "El 'energy landscape' muestra cómo varía la energía esperada al cambiar los parámetros del circuito. Un buen landscape tiene mínimos claros; un barren plateau es plano y dificulta la optimización."},
    {"title": "🎯 Selección de Hamiltoniano", "body": "Elige entre H₂, Ising, MAX-CUT u otro sistema. Cada uno tiene un landscape distinto con más o menos estructura."},
    {"title": "📉 Barren Plateau detector", "body": "A medida que el circuito crece en profundidad y qubits, los gradientes se vuelven exponencialmente pequeños. Este panel mide la varianza del gradiente."},
    {"title": "🏃 Comparativa de optimizadores", "body": "COBYLA, SPSA y Adam tienen perfiles muy distintos en landscapes ruidosos. SPSA es robusto al ruido cuántico; Adam es rápido en landscapes suaves."},
    {"title": "🖼️ Exportación", "body": "Descarga el landscape como PNG con el camino de optimización superpuesto."},
]
show_tour("landscape_params", _TOUR_STEPS)

# ---------------------------------------------------------------------------
# Hamiltonianos disponibles
# ---------------------------------------------------------------------------

HAMILTONIANOS = {
    "H₂ (2 qubits, JW)": SparsePauliOp.from_list([
        ('II', -1.0523732), ('IZ', 0.3979374),
        ('ZI', -0.3979374), ('ZZ', -0.0112801), ('XX', 0.1809312),
    ]),
    "Ising 1D (3 qubits)": SparsePauliOp.from_list([
        ('ZZI', -1.0), ('IZZ', -1.0),
        ('XII', -0.5), ('IXI', -0.5), ('IIX', -0.5),
    ]),
    "MAX-CUT triángulo (3 qubits)": SparsePauliOp.from_list([
        ('ZZI', -0.5), ('IZZ', -0.5), ('ZIZ', -0.5),
        ('III', 1.5),
    ]),
    "ZZ + X (2 qubits)": SparsePauliOp.from_list([
        ('ZZ', -1.0), ('XI', 0.5), ('IX', 0.5),
    ]),
}

# ---------------------------------------------------------------------------
# Ansätze
# ---------------------------------------------------------------------------

def ansatz_ry_cx(n_qubits: int, n_capas: int) -> QuantumCircuit:
    """Ansatz RY + CX en capas (hardware efficient)."""
    n_params = n_qubits * n_capas
    theta = ParameterVector('θ', n_params)
    qc = QuantumCircuit(n_qubits)
    idx = 0
    for _ in range(n_capas):
        for q in range(n_qubits):
            qc.ry(theta[idx], q)
            idx += 1
        for q in range(n_qubits - 1):
            qc.cx(q, q + 1)
    return qc

# ---------------------------------------------------------------------------
# Interfaz
# ---------------------------------------------------------------------------

col_ctrl, col_plot = st.columns([1, 2])

with col_ctrl:
    st.subheader("⚙️ Configuración")
    hamiltoniano_nombre = st.selectbox("Hamiltoniano", list(HAMILTONIANOS.keys()))
    H = HAMILTONIANOS[hamiltoniano_nombre]
    n_qubits = H.num_qubits

    n_capas = st.slider("Capas del ansatz", 1, 4, 1)
    ansatz = ansatz_ry_cx(n_qubits, n_capas)
    n_params = ansatz.num_parameters
    st.info(f"Ansatz: {n_qubits}q × {n_capas} capas = **{n_params} parámetros**")

    tab_landscape, tab_plateau, tab_optim = st.tabs(
        ["🗺️ Landscape 2D", "📉 Barren Plateau", "🏃 Optimizadores"]
    )

estimator = StatevectorEstimator()

def energia(params: np.ndarray) -> float:
    params_arr = np.array(params, dtype=float)
    result = estimator.run([(ansatz, H, params_arr)]).result()
    return float(result[0].data.evs)

with col_plot:
    with tab_landscape:
        st.subheader("Landscape de energía 2D")
        if n_params >= 2:
            param_idx_x = st.selectbox("Eje X — parámetro", range(n_params), format_func=lambda i: f"θ[{i}]")
            param_idx_y = st.selectbox("Eje Y — parámetro", range(n_params), index=min(1, n_params-1), format_func=lambda i: f"θ[{i}]")
            n_puntos = st.slider("Resolución de la cuadrícula", 10, 30, 15)

            base_params = np.zeros(n_params)
            x_vals = np.linspace(-np.pi, np.pi, n_puntos)
            y_vals = np.linspace(-np.pi, np.pi, n_puntos)

            with st.spinner("Calculando landscape..."):
                Z = np.zeros((n_puntos, n_puntos))
                param_grid = np.zeros((n_puntos * n_puntos, n_params))
                for i, x in enumerate(x_vals):
                    for j, y in enumerate(y_vals):
                        p = base_params.copy()
                        p[param_idx_x] = x
                        p[param_idx_y] = y
                        param_grid[i * n_puntos + j] = p

                # Batch evaluation
                pub = (ansatz, H, param_grid)
                result_grid = estimator.run([pub]).result()
                E_flat = result_grid[0].data.evs
                Z = E_flat.reshape(n_puntos, n_puntos)

            fig, ax = plt.subplots(figsize=(7, 6))
            XX, YY = np.meshgrid(x_vals, y_vals)
            cf = ax.contourf(XX, YY, Z.T, levels=25, cmap='RdBu_r')
            plt.colorbar(cf, ax=ax, label='⟨H⟩')
            ax.contour(XX, YY, Z.T, levels=25, colors='k', linewidths=0.3, alpha=0.3)
            ax.set_xlabel(f'θ[{param_idx_x}] (rad)')
            ax.set_ylabel(f'θ[{param_idx_y}] (rad)')
            ax.set_title(f'Landscape ⟨{hamiltoniano_nombre}⟩')
            ax.axhline(0, color='white', lw=0.5, alpha=0.5)
            ax.axvline(0, color='white', lw=0.5, alpha=0.5)
            # Marcar mínimo
            min_idx = np.unravel_index(np.argmin(Z), Z.shape)
            ax.plot(x_vals[min_idx[0]], y_vals[min_idx[1]], 'w*', ms=15, label=f'Mín: {Z.min():.3f}')
            ax.legend(fontsize=9)
            st.pyplot(fig)
            plt.close(fig)
            st.caption(f"E mínimo = {Z.min():.4f} | E máximo = {Z.max():.4f} | Rango = {Z.max()-Z.min():.4f}")
        else:
            st.info("Aumenta el número de capas para tener ≥2 parámetros.")

    with tab_plateau:
        st.subheader("Barren Plateau Detector")
        st.markdown("La varianza del gradiente decae exponencialmente con el número de qubits en circuitos aleatorios.")

        n_samples = st.slider("Muestras para estimar varianza", 20, 100, 40)
        max_depth = st.slider("Profundidad máxima de circuito", 1, 5, 3)

        if st.button("▶ Analizar barren plateau"):
            with st.spinner("Estimando varianza del gradiente..."):
                resultados_bp = []
                for capas in range(1, max_depth + 1):
                    ansatz_bp = ansatz_ry_cx(n_qubits, capas)
                    n_p = ansatz_bp.num_parameters
                    gradientes = []
                    eps = 0.01
                    for _ in range(n_samples):
                        theta0 = np.random.uniform(-np.pi, np.pi, n_p)
                        theta_p = theta0.copy(); theta_p[0] += eps
                        theta_m = theta0.copy(); theta_m[0] -= eps

                        E_p = float(estimator.run([(ansatz_bp, H, theta_p)]).result()[0].data.evs)
                        E_m = float(estimator.run([(ansatz_bp, H, theta_m)]).result()[0].data.evs)
                        gradientes.append((E_p - E_m) / (2 * eps))

                    var_grad = np.var(gradientes)
                    resultados_bp.append({'capas': capas, 'var_grad': var_grad,
                                          'mean_grad': np.mean(np.abs(gradientes))})

            fig, ax = plt.subplots(figsize=(8, 4))
            capas_vals = [r['capas'] for r in resultados_bp]
            vars_vals = [r['var_grad'] for r in resultados_bp]
            ax.semilogy(capas_vals, vars_vals, 'b-o', lw=2, ms=8, label='Var(∂E/∂θ₀)')
            ax.set_xlabel('Número de capas (profundidad)')
            ax.set_ylabel('Varianza del gradiente (log)')
            ax.set_title(f'Barren Plateau — {hamiltoniano_nombre} ({n_qubits}q)')
            ax.legend()
            ax.grid(alpha=0.3)
            st.pyplot(fig)
            plt.close(fig)

            if vars_vals[-1] < vars_vals[0] * 0.1:
                st.warning("⚠️ Barren plateau detectado: la varianza del gradiente cayó >10× con la profundidad.")
            else:
                st.success("✅ Sin barren plateau severo en este rango de profundidad.")

    with tab_optim:
        st.subheader("Comparativa de optimizadores")

        optimizadores = st.multiselect(
            "Optimizadores",
            ["COBYLA", "SLSQP", "Nelder-Mead"],
            default=["COBYLA", "SLSQP"],
        )
        max_iter = st.slider("Máx. iteraciones", 50, 300, 100)
        n_runs = st.slider("Ejecuciones (semillas distintas)", 1, 5, 3)

        if st.button("▶ Comparar optimizadores"):
            resultados_optim = {o: [] for o in optimizadores}

            with st.spinner("Optimizando..."):
                for seed in range(n_runs):
                    theta0 = np.random.default_rng(seed).uniform(-np.pi, np.pi, n_params)
                    for opt in optimizadores:
                        trayectoria = []
                        def cost_traj(p):
                            E = energia(p)
                            trayectoria.append(E)
                            return E

                        t0 = time.perf_counter()
                        res = minimize(cost_traj, theta0, method=opt,
                                       options={'maxiter': max_iter, 'xatol': 1e-6, 'fatol': 1e-6})
                        elapsed = time.perf_counter() - t0
                        resultados_optim[opt].append({
                            'E_final': res.fun,
                            'n_iter': len(trayectoria),
                            'tiempo_s': elapsed,
                            'trayectoria': trayectoria,
                            'seed': seed,
                        })

            # Gráfica de convergencia
            fig, axes = plt.subplots(1, 2, figsize=(12, 5))
            colores = {'COBYLA': 'blue', 'SLSQP': 'red', 'Nelder-Mead': 'green', 'SPSA': 'orange'}

            for opt in optimizadores:
                color = colores.get(opt, 'gray')
                for run in resultados_optim[opt]:
                    axes[0].plot(run['trayectoria'], color=color, alpha=0.5, lw=1)
                # Media de trayectorias (interpolada al mínimo de iteraciones)
                min_len = min(len(r['trayectoria']) for r in resultados_optim[opt])
                traj_arr = np.array([r['trayectoria'][:min_len] for r in resultados_optim[opt]])
                axes[0].plot(np.mean(traj_arr, axis=0), color=color, lw=2.5, label=f'{opt} (media)')

            axes[0].set_xlabel('Evaluación de la función de coste')
            axes[0].set_ylabel('⟨H⟩')
            axes[0].set_title('Convergencia de optimizadores')
            axes[0].legend()
            axes[0].grid(alpha=0.3)

            # Tabla resumen
            resumen = []
            for opt in optimizadores:
                E_finals = [r['E_final'] for r in resultados_optim[opt]]
                tiempos = [r['tiempo_s'] for r in resultados_optim[opt]]
                resumen.append({
                    'Optimizador': opt,
                    'E_final (media)': f"{np.mean(E_finals):.4f}",
                    'E_final (mín)': f"{np.min(E_finals):.4f}",
                    'Tiempo medio (s)': f"{np.mean(tiempos):.2f}",
                    'Iters (media)': f"{np.mean([r['n_iter'] for r in resultados_optim[opt]]):.0f}",
                })

            df_res = pd.DataFrame(resumen)
            axes[1].axis('off')
            table = axes[1].table(
                cellText=df_res.values, colLabels=df_res.columns,
                cellLoc='center', loc='center'
            )
            table.auto_set_font_size(False)
            table.set_fontsize(9)
            axes[1].set_title('Resumen comparativo', pad=20)

            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
            st.dataframe(df_res, use_container_width=True)
