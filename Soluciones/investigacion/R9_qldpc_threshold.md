# Solución R9 — Umbral qLDPC bajo ruido de circuito

**Problema:** [Tutorial 47 — qLDPC y decodificadores neuronales](../../Tutorial/47_qldpc_decodificadores/README.md#ejercicio-5-investigacion)

---

## Parte 1 — Modelo de ruido de circuito

El análisis de umbrales de corrección de errores depende críticamente del **modelo de ruido** utilizado. Los dos modelos principales son:

### Ruido de Pauli independiente

En el modelo más simple, cada qubit sufre un error de Pauli $X$, $Z$ o $Y$ con probabilidad $p$ independientemente en cada paso de tiempo. El síndrome se mide perfectamente. Este modelo es útil para cotas teóricas pero no refleja la física del hardware.

Bajo este modelo, el umbral del surface code es $p_{\text{th}} \approx 10.3\%$ con decodificación óptima, o $p_{\text{th}} \approx 1\%$ con MWPM (el factor 10 refleja la suboptimalidad del decodificador).

### Ruido de circuito

El modelo de **ruido de circuito** es más realista: los errores ocurren en los componentes del ciclo de síndrome, no solo en los datos. Un ciclo completo de síndrome consta de:

1. **Preparación de ancilla:** el qubit ancilla se prepara en $|0\rangle$ o $|+\rangle$ con probabilidad de error $p_{\text{prep}}$.
2. **Puertas CNOT:** cada CNOT entre ancilla y qubit de datos falla con probabilidad $p_{\text{gate}}$. Un error en un CNOT puede propagarse a dos qubits.
3. **Medición:** la medición del ancilla produce el bit de síndrome equivocado con probabilidad $p_{\text{meas}}$.

En el modelo estándar de ruido de circuito se asume $p_{\text{prep}} = p_{\text{gate}} = p_{\text{meas}} = p$, y el síndrome tiene errores correlacionados espacial y temporalmente.

La ecuación de propagación de errores a través de una puerta CNOT (control $c$, target $t$) es:

$$
\text{CNOT}_{ct}: X_c \to X_c X_t, \quad X_t \to X_t, \quad Z_c \to Z_c, \quad Z_t \to Z_c Z_t
$$

Esto significa que un error $Z$ en el control se propaga como $Z_cZ_t$ después del CNOT, correlacionando los qubits.

### Correlaciones temporales

Las mediciones de síndrome son **ruidosas**: una ancilla puede reportar $-1$ no por un error en el dato, sino por un error en su propia medición. Esto obliga a acumular $d$ rondas de síndrome antes de decodificar, tratando el problema como 3D (2 dimensiones espaciales + 1 temporal):

$$
\text{Síndrome efectivo:}\quad \Delta s_t = s_t \oplus s_{t-1}
$$

El síndrome diferencial $\Delta s_t$ revela cuándo cambia el síndrome de una ronda a la siguiente, lo que es indicativo de un error real (cambio persistente) frente a un error de medición (cambio transitorio).

---

## Parte 2 — Por qué el umbral cae de ~1% a ~0.5–0.7%

La reducción del umbral del $1\%$ teórico (ruido de Pauli) al $0.5$–$0.7\%$ observable (ruido de circuito) tiene tres causas principales:

### 2.1 Multiplicación de errores por propagación en CNOT

En el ciclo de síndrome de un código qLDPC con peso de estabilizador $w$ (número de qubits de datos por ancilla), se aplican $w$ puertas CNOT por ancilla. Cada CNOT tiene probabilidad $p$ de fallo. La probabilidad de que al menos un CNOT falle es:

$$
p_{\text{ciclo}} \approx w \cdot p + O(p^2)
$$

Para los códigos BB con $w = 6$ (cada ancilla conectada a 6 qubits de datos), el error efectivo por ciclo es $\sim 6p$, reduciendo el umbral efectivo por un factor $\sim 6$.

Sin embargo, no todos estos errores son independientes o igualmente dañinos. El umbral preciso requiere análisis numérico.

### 2.2 Decodificación 3D vs. 2D

Bajo ruido de circuito, el espacio-tiempo de síndromes tiene $d$ capas temporales. El grafo de decodificación tiene $O(d^3)$ nodos en lugar de $O(d^2)$, lo que aumenta la complejidad pero también genera correlaciones adicionales que pueden confundir al decodificador.

La expresión de la tasa de error lógica bajo ruido de circuito es, asintóticamente:

$$
P_L(p) \approx A_{\text{circuit}} \cdot \left(\frac{p}{p_{\text{th,circuit}}}\right)^{\lfloor d/2 \rfloor}
$$

donde $A_{\text{circuit}} > A_{\text{Pauli}}$ porque hay más caminos de error mínimo en 3D.

### 2.3 Estimación numérica del umbral

```python
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Simulacion simplificada de Monte Carlo para estimar el umbral
# (resultados ilustrativos basados en Bravyi et al. 2024)

def simulate_logical_error_rate(p_phys, n_qubits, n_trials=10000):
    """
    Placeholder para simulacion real de Monte Carlo.
    En produccion: usar Stim (Gidney, 2021) para circuitos de estabilizador.
    
    Parametros
    ----------
    p_phys : float
        Tasa de error fisico por puerta.
    n_qubits : int
        Numero de qubits fisicos (determina la distancia del codigo).
    n_trials : int
        Numero de realizaciones Monte Carlo.
    
    Retorna
    -------
    p_logical : float
        Tasa de error logico estimada.
    """
    # Modelo simplificado: P_L ~ A * (p/p_th)^(d/2)
    # Para BB [[n, 12, d]]: d ~ sqrt(n/12)
    d = int(np.sqrt(n_qubits / 12))
    p_th = 0.006  # ~0.6% bajo ruido de circuito
    A = 0.1
    p_logical = A * (p_phys / p_th) ** (d // 2)
    return min(p_logical, 0.5)

# Tasas de error fisico a evaluar
p_values = np.linspace(0.001, 0.012, 50)

# Tamanios de codigo (n = 72, 144, 288 -> distancias 6, 12, 18)
sizes = {
    72:  {'label': '[[72,12,6]]',   'color': 'blue'},
    144: {'label': '[[144,12,12]]', 'color': 'red'},
    288: {'label': '[[288,12,18]]', 'color': 'green'},
}

fig, ax = plt.subplots(figsize=(8, 6))

for n, props in sizes.items():
    p_L = [simulate_logical_error_rate(p, n) for p in p_values]
    ax.semilogy(p_values * 100, p_L, color=props['color'],
                lw=2, label=props['label'])

ax.axvline(0.6, color='k', ls='--', lw=1.5, label='Umbral estimado ~0.6%')
ax.set_xlabel('Tasa de error fisico p (%)')
ax.set_ylabel(r'Tasa de error logico $P_L$')
ax.set_title('Curvas P_L(p) para BB codes bajo ruido de circuito')
ax.legend(); ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()
```

El **crossing point** (punto de cruce) es el valor de $p$ donde las curvas $P_L(p, n)$ para distintos tamaños $n$ se intersectan. Por debajo del cruce, aumentar $n$ reduce $P_L$; por encima, lo aumenta. El crossing point es el estimador numérico del umbral:

$$
p_{\text{th}} = p^* : \quad \frac{\partial P_L}{\partial n}\bigg|_{p=p^*} = 0
$$

---

## Parte 3 — BP+OSD vs. MWPM

### Complejidad computacional

| Decodificador | Complejidad | Ventaja | Limitación |
|---|---|---|---|
| MWPM (Blossom V) | $O(n^3)$ worst case | Óptimo para surface code | No escala; requiere planariedad |
| BP | $O(n \cdot t_{\max})$ | Masivamente paralelizable | Falla en grafos con ciclos |
| BP+OSD | $O(n \log n) + O(n^3/\log n)$ | Balance velocidad/calidad | OSD costoso para códigos grandes |
| Neural (LSTM) | $O(1)$ inferencia | Latencia $< 1\,\mu$s en FPGA | Requiere entrenamiento; no generaliza trivialmente |

La complejidad de BP+OSD se desglosa en:

$$
T_{\text{BP+OSD}} = \underbrace{O(n \cdot t_{\max})}_{\text{fase BP}} + \underbrace{O\!\left(\binom{n}{w_{\text{OSD}}} + n^2\right)}_{\text{fase OSD}}
$$

Para $w_{\text{OSD}} = 2$ (OSD de orden 2), la fase OSD es $O(n^2)$, que domina sobre BP pero es mucho mejor que $O(n^3)$ de MWPM.

### Por qué BP+OSD supera a MWPM en qLDPC

El rendimiento superior de BP+OSD para códigos qLDPC se debe a tres factores estructurales:

1. **Estructura de grafo:** Los códigos BB tienen un grafo de Tanner con distribución de grados regular y alta girona (*girth* $\geq 6$), lo que favorece la convergencia de BP frente a los grafos irregulares donde falla.

2. **No planariedad:** MWPM requiere que el grafo de síndrome sea planar (o casi planar) para encontrar emparejamientos eficientes. Los códigos qLDPC generan grafos de síndrome no planares donde MWPM produce emparejamientos subóptimos.

3. **Correlaciones de alto orden:** Un error en un CNOT crea una correlación de dos qubits. BP modela estas correlaciones mediante la propagación de mensajes de probabilidad conjunta; MWPM las ignora al tratar cada defecto como independiente.

El resultado empírico de Bravyi et al. 2024 es que BP+OSD alcanza una tasa de error lógica $P_L$ aproximadamente $3$–$5\times$ menor que MWPM para los mismos parámetros de código y tasa de error físico.

---

## Parte 4 — Análisis numérico del umbral

### Protocolo Monte Carlo

El procedimiento estándar para estimar $p_{\text{th}}$ numéricamente es:

1. **Generar errores:** para cada qubit $j$, muestrear $e_j \sim \text{Bernoulli}(p)$ independientemente (modelo de Pauli) o simular el circuito completo con Stim (modelo de circuito).

2. **Calcular síndrome:** $s = H_Z e \pmod{2}$ para errores $X$; $s = H_X e \pmod{2}$ para errores $Z$.

3. **Decodificar:** aplicar BP+OSD para obtener una estimación del error $\hat{e}$.

4. **Verificar éxito:** calcular $r = e \oplus \hat{e}$. Si $r \in \text{rowspace}(H_Z)$ (es decir, $r$ es un estabilizador), la decodificación fue exitosa. Si $r$ es un operador lógico no trivial, hay un **error lógico**.

5. **Estimar $P_L$:** promediar sobre $N \geq 10^4$ realizaciones.

### Estimación del crossing point

Para estimar el umbral con precisión, se ajusta el modelo de escalado finito:

$$
P_L(p, d) = f\!\left((p - p_{\text{th}}) \cdot d^{1/\nu}\right)
$$

donde $\nu$ es el exponente crítico. Para el surface code $\nu \approx 1.33$ (clase de universalidad de percolación 2D). Para códigos BB el valor es similar.

El ajuste se realiza minimizando:

$$
\chi^2 = \sum_{i,j} \frac{\left[P_L(p_i, d_j) - f\!\left((p_i - p_{\text{th}}) d_j^{1/\nu}\right)\right]^2}{\sigma_{ij}^2}
$$

sobre los parámetros $p_{\text{th}}$, $\nu$ y los coeficientes del polinomio $f$.

```python
from scipy.optimize import minimize
import numpy as np

def finite_size_scaling_fit(p_values, d_values, P_L_data, p_th_init=0.006, nu_init=1.33):
    """
    Ajuste de escalado de tamanio finito para estimar p_th y nu.
    
    P_L_data[i, j] = P_L medida para p = p_values[i], d = d_values[j]
    """
    def model(params, p_arr, d_arr):
        p_th, nu, a0, a1, a2 = params
        x = (p_arr - p_th) * d_arr**(1.0/nu)
        # Polinomio de segundo orden como funcion de escalado
        return 0.5 + a0*x + a1*x**2 + a2*x**3
    
    def cost(params):
        total = 0
        for i, p in enumerate(p_values):
            for j, d in enumerate(d_values):
                predicted = model(params, p, d)
                observed  = P_L_data[i, j]
                total += (predicted - observed)**2
        return total
    
    result = minimize(cost, x0=[p_th_init, nu_init, 0.1, 0.0, 0.0],
                      method='Nelder-Mead')
    p_th_fit, nu_fit = result.x[0], result.x[1]
    return p_th_fit, nu_fit

# Uso tipico (con datos reales de simulacion):
# p_values = np.linspace(0.003, 0.010, 20)
# d_values = [6, 12, 18]   # distancias de los codigos BB
# P_L_data = np.array(...)  # resultado de N=10^4 simulaciones por punto
# p_th, nu = finite_size_scaling_fit(p_values, d_values, P_L_data)
# print(f"Umbral estimado: p_th = {p_th:.4f} ({p_th*100:.2f}%)")
```

---

## Parte 5 — Conclusión: por qué qLDPC supera a surface codes

La superioridad asintótica de los códigos qLDPC sobre los surface codes descansa en un resultado matemático fundamental: la existencia de **buenos códigos cuánticos LDPC** (Panteleev & Kalachev 2022; Leverrier & Zémor 2022) con:

$$
k = \Theta(n), \quad d = \Theta(n), \quad w = O(1)
$$

donde $w$ es el peso máximo de los estabilizadores. Esto implica una **tasa de código constante** $R = k/n = \Theta(1)$ con distancia lineal, lo cual es imposible para el surface code (que tiene $R = 1/d^2 \to 0$).

En el límite de muchos qubits lógicos $k \gg 1$, la comparación de overhead es:

$$
\frac{n_{\text{surface}}}{n_{\text{qLDPC}}} \sim \frac{k \cdot d^2}{k/R} = R \cdot d^2 \xrightarrow{d \to \infty} \infty
$$

Es decir, para cualquier distancia $d$ fija, el overhead del surface code crece sin límite con $k$, mientras que el overhead del código qLDPC permanece acotado.

Para los códigos BB con parámetros actuales ($n = 144$, $k = 12$, $d = 12$), el ahorro ya es un factor $\sim 12\times$ frente al surface code. Con la hoja de ruta de IBM hacia Starling (2026–2027), este factor se espera que alcance $\sim 10$–$20\times$ a escala de 100–1000 qubits lógicos.

La combinación de tasa finita, buenos umbrales, y decodificadores eficientes como BP+OSD posiciona a los códigos BB y sus sucesores como la base más probable de la computación cuántica tolerante a fallos a gran escala.

---

## Referencias

1. **Bravyi, S. et al.** (2024). "High-threshold and low-overhead fault-tolerant quantum memory." *Nature*, 627, 778–782.
2. **Panteleev, P. & Kalachev, G.** (2022). "Asymptotically good quantum and locally testable classical LDPC codes." *STOC 2022*.
3. **Leverrier, A. & Zémor, G.** (2022). "Quantum Tanner codes." *IEEE FOCS 2022*.
4. **Gidney, C.** (2021). "Stim: a fast stabilizer circuit simulator." *Quantum*, 5, 497.
5. **Roffe, J. et al.** (2020). "Decoding across the quantum low-density parity-check code landscape." *Physical Review Research*, 2, 043423.
