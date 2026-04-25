# Teorema del Umbral y Escalado Subcrítico de Errores

## 1. El problema fundamental de la corrección de errores cuánticos

En el módulo 09 vimos que el código de repetición protege contra errores de bit-flip, y en el módulo 14 que el código de superficie protege contra errores arbitrarios de un qubit. Pero queda una pregunta crucial: ¿tiene sentido añadir qubits de corrección si las propias operaciones de corrección introducen errores?

La respuesta la da el **teorema del umbral**: sí, siempre que el error físico por puerta esté por debajo de un valor crítico $p_{th}$.

---

## 2. Enunciado del teorema del umbral

**Teorema (Aharonov-Ben-Or, Knill-Laflamme-Zurek, 1996-1998):**
Existe una constante $p_{th} > 0$ tal que, si la probabilidad de error por operación elemental es $p < p_{th}$, entonces es posible realizar cómputo cuántico arbitrariamente largo con probabilidad de error lógico arbitrariamente pequeña, usando un overhead polilogarítmico en el número de operaciones.

### 2.1 Hipótesis del teorema

- **Errores independientes:** cada qubit falla de forma independiente con probabilidad $p$.
- **Errores locales:** los errores actúan sobre qubits individuales o pares de qubits (no correlacionados a largo alcance).
- **Medición y corrección rápidas:** el ciclo de síndrome ocurre mucho más rápido que $T_1$ y $T_2$.
- **Paralelismo:** múltiples operaciones de corrección se ejecutan simultáneamente.

### 2.2 Idea de la prueba: concatenación

La prueba se basa en **códigos concatenados**: codificar cada qubit lógico de nivel 1 en $k$ qubits físicos, y luego codificar cada uno de esos qubits en otros $k$ qubits físicos, y así sucesivamente.

Para $L$ niveles de concatenación y un código con umbral $p_{th}$:
$$
p_L^{(\text{lógico})} = p_{th} \left(\frac{p}{p_{th}}\right)^{2^L}
$$

Si $p < p_{th}$, entonces $p/p_{th} < 1$ y $p_L^{(\text{lógico})} \to 0$ exponencialmente en $L$.

```python
import numpy as np
import matplotlib.pyplot as plt

p_th = 0.01  # umbral típico del código de superficie

def p_logical_concatenated(p_phys, p_th, levels):
    """Error lógico bajo concatenación de L niveles."""
    return p_th * (p_phys / p_th) ** (2 ** levels)

p_vals = np.linspace(0.001, 0.02, 200)

fig, ax = plt.subplots(figsize=(9, 5))
for L in range(1, 6):
    p_L = [p_logical_concatenated(p, p_th, L) for p in p_vals]
    ax.semilogy(p_vals * 100, p_L, label=f"L={L} niveles")

ax.axvline(x=1.0, color="red", linestyle="--", alpha=0.7, label=f"Umbral $p_{{th}}$={p_th*100:.0f}%")
ax.set_xlabel("Error físico por puerta (%)")
ax.set_ylabel("Error lógico $p_L$")
ax.set_title("Supresión de errores por concatenación")
ax.legend(); ax.grid(alpha=0.3)
plt.tight_layout(); plt.show()
```

---

## 3. El código de superficie a escala

### 3.1 Parámetros del código

El código de superficie de distancia $d$ (módulo 14) tiene:
- $d^2$ qubits de datos + $(d^2-1)$ qubits ancilla = $\approx 2d^2$ qubits físicos por qubit lógico.
- Capacidad de corregir errores en hasta $\lfloor (d-1)/2 \rfloor$ qubits.
- Umbral: $p_{th} \approx 1\%$ para ruido independiente.

### 3.2 Error lógico en función de la distancia

Para $p_{\text{phys}} \ll p_{th}$:
$$
p_L \approx A \left(\frac{p_{\text{phys}}}{p_{th}}\right)^{\lceil d/2 \rceil}
$$

```python
import numpy as np

def p_logical_surface(p_phys, d, p_th=0.01, A=0.1):
    return A * (p_phys / p_th) ** np.ceil(d / 2)

# Tabla de requisitos: ¿qué distancia necesitamos para p_L < 10^-k?
p_phys = 0.001  # error físico 0.1% (IBM Heron 2024)
print(f"Error físico: {p_phys*100:.1f}%\n")
print(f"{'Distancia d':>12} {'Qubits físicos':>16} {'Error lógico p_L':>18}")
for d in [3, 5, 7, 9, 11, 15, 21, 27]:
    p_L = p_logical_surface(p_phys, d)
    n_phys = 2 * d**2
    print(f"{d:>12} {n_phys:>16} {p_L:>18.2e}")
```

### 3.3 Ciclo de síndrome

Un ciclo de corrección en el código de superficie requiere:
1. **Preparación:** inicializar qubits ancilla en $|0\rangle$ o $|+\rangle$.
2. **Medición de síndromes:** 4 puertas CNOT por ancilla (estabilizadores X y Z).
3. **Decodificación:** algoritmo de decodificación (MWPM — Minimum Weight Perfect Matching).
4. **Corrección virtual:** acumular las correcciones en software (Pauli frame).

El ciclo completo tarda $\sim 1\,\mu\text{s}$ en superconductores modernos, lo que permite miles de ciclos dentro de $T_1 \sim 300\,\mu\text{s}$.

```python
from qiskit import QuantumCircuit

def surface_code_syndrome_cycle(d: int) -> QuantumCircuit:
    """
    Ciclo de síndrome simplificado para el código de superficie de distancia d.
    Solo ilustra la estructura; un ciclo real requiere mapeo a topología específica.
    """
    n_data = d * d
    n_ancilla = (d * d - 1)
    qc = QuantumCircuit(n_data + n_ancilla, n_ancilla)

    # Inicializar ancillas X (Hadamard)
    for i in range(n_ancilla // 2):
        qc.h(n_data + i)

    qc.barrier()

    # Puertas de medición de estabilizadores (esquematizado)
    # En un código real, cada ancilla conecta a sus 2-4 vecinos de datos
    for i in range(n_ancilla):
        data_neighbors = [min(i, n_data-1), min(i+1, n_data-1)]
        for dn in data_neighbors:
            qc.cx(n_data + i, dn) if i >= n_ancilla//2 else qc.cx(dn, n_data + i)

    qc.barrier()
    # Deshacer Hadamard y medir
    for i in range(n_ancilla // 2):
        qc.h(n_data + i)
    qc.measure(range(n_data, n_data + n_ancilla), range(n_ancilla))

    return qc

qc_synd = surface_code_syndrome_cycle(3)
print(f"Circuito de síndrome d=3: {qc_synd.num_qubits} qubits, profundidad={qc_synd.depth()}")
```

---

## 4. Decodificación: Minimum Weight Perfect Matching (MWPM)

El síndrome de error es el conjunto de ancillas que miden $-1$ (detectan un error). El decodificador MWPM busca la corrección de menor peso que explica el síndrome observado.

**Complejidad:** MWPM tiene complejidad $O(n^3)$ en el número de defectos, pero implementaciones aproximadas como Union-Find logran $O(n\alpha(n))$ (casi lineal), compatible con corrección en tiempo real.

```python
import numpy as np

def simple_mwpm_1d(syndrome: list) -> list:
    """
    MWPM simplificado para código de repetición 1D.
    Empareja defectos adyacentes mínimizando la distancia total.
    """
    defects = [i for i, s in enumerate(syndrome) if s == 1]
    corrections = []
    while len(defects) >= 2:
        # Emparejar los dos defectos más cercanos
        d1, d2 = defects[0], defects[1]
        for q in range(min(d1,d2), max(d1,d2)):
            corrections.append(q)
        defects = defects[2:]
    return corrections

# Ejemplo: código de repetición de 7 bits con 2 errores
# Error en posición 2 y 4 → síndrome en posición 2, 3, 4, 5
syndrome = [0, 0, 1, 1, 1, 1, 0]
corrections = simple_mwpm_1d(syndrome)
print(f"Síndrome:     {syndrome}")
print(f"Correcciones: {corrections}")
```

---

## 5. Experimento Google Willow (2024): primer escalado subcrítico

En diciembre de 2024, Google publicó en *Nature* los resultados del chip Willow de 105 qubits superconductores. El experimento clave:

- Código de superficie con distancias $d = 3, 5, 7$.
- Al aumentar $d$, el error lógico **decreció** exponencialmente.
- Primera demostración en hardware real de escalado subcrítico $p_L \propto (p/p_{th})^{(d+1)/2}$.

Esto confirma experimentalmente que:
1. El error físico de Willow está por debajo de $p_{th}$.
2. El código de superficie funciona como la teoría predice.
3. El camino hacia qubits lógicos útiles está despejado en principio.

```python
# Datos experimentales aproximados de Willow (Nature, dic. 2024)
distancias = [3, 5, 7]
p_logico_willow = [6.3e-3, 2.1e-3, 6.2e-4]  # error lógico por ciclo de síndrome

import numpy as np
import matplotlib.pyplot as plt

d_fit = np.array(distancias)
p_fit = np.array(p_logico_willow)

# Ajuste exponencial: log(p_L) ~ (d+1)/2 * log(p/p_th)
log_p = np.log(p_fit)
slope, intercept = np.polyfit((d_fit + 1) / 2, log_p, 1)
p_th_empirico = np.exp(intercept / (-1)) if slope < 0 else None

print(f"Pendiente del ajuste: {slope:.3f}")
print(f"p_th empírico estimado: ~{np.exp(-intercept):.1%}")

plt.semilogy(distancias, p_logico_willow, "o-", label="Willow (2024)")
plt.xlabel("Distancia d"); plt.ylabel("Error lógico por ciclo")
plt.title("Escalado subcrítico en Google Willow")
plt.grid(alpha=0.3); plt.legend(); plt.show()
```

---

## 6. Overhead de recursos: el precio de la tolerancia a fallos

| Aplicación | Qubits lógicos | Dist. $d$ | Qubits físicos | Tiempo |
|---|---|---|---|---|
| Demo Shor (RSA-512) | ~1000 | 13 | ~340.000 | ~1 hora |
| Shor RSA-2048 | ~4000 | 27 | ~5.800.000 | ~8 horas |
| FeMoco (química) | ~200 | 17 | ~116.000 | ~días |
| Grover SHA-256 | ~300 | 17 | ~174.000 | impráctical |

El factor clave es que el código de superficie requiere $\sim 2d^2$ qubits físicos por qubit lógico, convirtiendo cientos de qubits lógicos en millones de qubits físicos.

---

## 7. Resumen

El teorema del umbral garantiza que la corrección de errores cuánticos es posible en principio. El código de superficie ofrece el camino más prometedor hacia la práctica, con un umbral de ~1% compatible con la tecnología actual. Google Willow (2024) demostró por primera vez en hardware real que al aumentar el código, el error lógico decrece — el hito experimental que valida la ruta hacia la computación cuántica tolerante a fallos.

---

*← [README Módulo 29](README.md) | [02 Magic state distillation →](02_magic_state_distillation.md)*
