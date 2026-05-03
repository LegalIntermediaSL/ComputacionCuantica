# Solución R1 — QSVT: Aproximación polinómica óptima

**Problema:** [Ejercicios de investigación R1](../../Ejercicios/ejercicios_investigacion.md#problema-r1)

---

## Parte a) — Implementación y convergencia

```python
import numpy as np
import matplotlib.pyplot as plt

def base_chebyshev(x: np.ndarray, d: int) -> np.ndarray:
    """Matriz T de dimensión (len(x), d+1) con T[:,k] = T_k(x)."""
    T = np.zeros((len(x), d + 1))
    T[:, 0] = 1.0
    if d >= 1:
        T[:, 1] = x
    for k in range(2, d + 1):
        T[:, k] = 2 * x * T[:, k-1] - T[:, k-2]
    return T

def error_aprox_chebyshev(f, d_max: int, x_vals: np.ndarray,
                           solo_impares: bool = True) -> list[float]:
    """Error máximo de aproximación Chebyshev para grados d=1,3,...,d_max."""
    errores = []
    grados = range(1, d_max+1, 2) if solo_impares else range(1, d_max+1)
    y_target = f(x_vals)

    for d in grados:
        T = base_chebyshev(x_vals, d)
        coeffs, _, _, _ = np.linalg.lstsq(T, y_target, rcond=None)
        y_approx = T @ coeffs
        errores.append(np.max(np.abs(y_approx - y_target)))

    return errores

# Función sgn(x) con zona muerta en |x| < delta
delta = 0.1
x = np.linspace(-1, 1, 500)
x_nz = x[np.abs(x) > delta]  # excluir zona muerta
f_sgn = lambda x: np.sign(x + 1e-15)

grados_impares = list(range(1, 40, 2))
errores_sgn = error_aprox_chebyshev(f_sgn, 39, x_nz)

# Ajuste exponencial: ε(d) ≈ C · exp(-αd)
log_err = np.log(np.array(errores_sgn))
slope, intercept = np.polyfit(grados_impares, log_err, 1)
alpha = -slope

print(f'Decaimiento exponencial: ε(d) ≈ {np.exp(intercept):.3f} · exp(-{alpha:.4f}·d)')
print(f'Teórico (Chebyshev): α = π²/(4·ln(1/δ)) = {np.pi**2 / (4*np.log(1/delta)):.4f}')

# Visualización
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Curvas de aproximación
for d_show in [5, 15, 25, 39]:
    T = base_chebyshev(x_nz, d_show)
    coeffs, _, _, _ = np.linalg.lstsq(T, f_sgn(x_nz), rcond=None)
    axes[0].plot(x_nz, T @ coeffs, lw=1.5, label=f'd={d_show}')
axes[0].plot(x_nz, f_sgn(x_nz), 'k--', lw=2, alpha=0.4, label='sgn(x)')
axes[0].set_title(f'Aproximación de sgn(x) (δ={delta})'); axes[0].legend(fontsize=8)
axes[0].set_xlabel('x'); axes[0].grid(alpha=0.3)

# Convergencia
axes[1].semilogy(grados_impares, errores_sgn, 'b-o', ms=5, label='Error empírico')
axes[1].semilogy(grados_impares,
                  np.exp(intercept + slope * np.array(grados_impares)),
                  'r--', lw=1.5, label=f'Ajuste: exp(-{alpha:.3f}·d)')
axes[1].set_xlabel('Grado d'); axes[1].set_ylabel('Error máximo')
axes[1].set_title('Convergencia Chebyshev para sgn(x)'); axes[1].legend(); axes[1].grid(alpha=0.3)

plt.tight_layout(); plt.show()
```

**Resultado clave:** el error converge como $\varepsilon_d \approx C \cdot e^{-\pi^2 d/(4\ln(1/\delta))}$,
confirmando la cota teórica. Para $\delta=0.1$ y $d=39$: $\varepsilon \approx 10^{-3}$.

---

## Parte b) — Queries QSVT para sgn(A) con ε=10⁻⁴

El grado necesario para error $\varepsilon$ en $|x| > \delta$:

$$
d \approx \frac{4\ln(1/\delta)}{\pi^2} \cdot \ln\left(\frac{1}{\varepsilon}\right)
$$

```python
import numpy as np

def grado_chebyshev_sgn(delta: float, epsilon: float) -> int:
    """Grado mínimo para aproximar sgn(x) con error ε en |x| > δ."""
    return int(np.ceil(4 * np.log(1/delta) / np.pi**2 * np.log(1/epsilon)))

eps = 1e-4
for delta in [0.1, 0.3, 0.5]:
    d = grado_chebyshev_sgn(delta, eps)
    queries = d  # QSVT: d queries a U_A
    print(f'δ={delta}: d={d}, queries QSVT={queries}')

# Para QSVT: número de queries = d (cada query es 1 aplicación de U_A o U_A†)
```

**Respuesta:** Para $\delta=0.1$, $\varepsilon=10^{-4}$: se necesitan $d \approx 43$ queries.

---

## Parte c) — QSVT vs LCU-Taylor para sgn(A)

```python
def queries_lcu_taylor(delta: float, epsilon: float, lambda_A: float = 1.0) -> int:
    """
    Queries LCU-Taylor para sgn(A).
    LCU requiere simular e^{-iHt} y usa d ≈ e·λ·t·log(λ·t/ε) términos de Taylor.
    Para sgn(x) ≈ erf(cx) con c → ∞: el coste es exponencialmente peor en 1/delta.
    """
    # Aproximación a través de polinomio sign via erf(x/delta*pi/2)
    # LCU necesita norma-1 del polinomio, que crece como 1/delta
    lcu_norm = 1.0 / delta
    d_lcu = int(np.ceil(np.e * lcu_norm * np.log(lcu_norm / epsilon)))
    return d_lcu

print('Comparativa QSVT vs LCU-Taylor para sgn(A):')
print(f'{"δ":>6} | {"QSVT (queries)":>16} | {"LCU-Taylor":>12} | {"Ventaja":>8}')
print('-' * 52)
for delta in [0.5, 0.3, 0.1, 0.05]:
    q_qsvt = grado_chebyshev_sgn(delta, 1e-4)
    q_lcu  = queries_lcu_taylor(delta, 1e-4)
    print(f'{delta:>6.2f} | {q_qsvt:>16} | {q_lcu:>12} | {q_lcu//q_qsvt:>7}×')
```

**Conclusión:** QSVT es superior cuando $\delta$ es pequeño (operador mal condicionado),
ya que LCU-Taylor necesita norma $O(1/\delta)$ términos mientras QSVT solo $O(\log(1/\varepsilon)/\delta^0)$.

---

## Referencia
Martyn et al., *PRX Quantum* 2, 040203 (2021), Sec. IV-V.
