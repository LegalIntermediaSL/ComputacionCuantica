# Magic State Distillation y Universalidad Tolerante a Fallos

## 1. El conjunto de puertas tolerante a fallos

El código de superficie protege la información cuántica durante el almacenamiento y las operaciones de síndrome. Pero ¿qué puertas lógicas puede ejecutar de forma **tolerante a fallos** (es decir, sin propagar errores de forma catastrófica)?

La respuesta depende del **grupo de Clifford**: el conjunto de puertas que mapean el grupo de Pauli en sí mismo bajo conjugación.

### 1.1 El grupo de Clifford

Generadores del grupo de Clifford:
- Puerta Hadamard: $H = \frac{1}{\sqrt{2}}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$
- Puerta de fase: $S = \begin{pmatrix}1&0\\0&i\end{pmatrix}$
- Puerta CNOT

**Propiedades:**
- Los circuitos de Clifford se pueden simular eficientemente en clásico (teorema de Gottesman-Knill).
- NO son computacionalmente universales: no pueden ejecutar algoritmos como Shor o Grover.
- Se pueden implementar de forma tolerante a fallos mediante **transversalidad** en el código de superficie.

### 1.2 Transversalidad

Una puerta lógica es **transversal** en un código si puede implementarse aplicando puertas físicas de forma independiente en cada qubit, sin propagar errores entre ellos.

Para el código de superficie de distancia $d$:
- **Transversales:** $\bar{H}$, $\bar{S}$, $\overline{\text{CNOT}}$ (grupo de Clifford)
- **No transversal:** $\bar{T} = \begin{pmatrix}1&0\\0&e^{i\pi/4}\end{pmatrix}$ — necesaria para universalidad

### 1.3 ¿Por qué T no es transversal?

El teorema de Eastin-Knill (2009) demuestra que **ningún código de corrección de errores puede tener un conjunto de puertas transversales universal**. Siempre falta al menos una puerta.

Para el código de superficie, la puerta $T$ lógica no puede implementarse transversalmente. Esto crea el problema central de la computación tolerante a fallos: ¿cómo ejecutar $T$ de forma confiable?

---

## 2. Magic State Distillation (Bravyi-Kitaev, 2005)

### 2.1 El estado mágico

La solución es preparar un **estado mágico** $|T\rangle$:
$$
|T\rangle = T|+\rangle = \cos\frac{\pi}{8}|0\rangle + e^{i\pi/4}\sin\frac{\pi}{8}|1\rangle
$$

Una vez disponible $|T\rangle$, se puede usar **inyección de estado** para aplicar la puerta $T$ lógica usando solo puertas de Clifford y medición:

```
|ψ⟩ ─────●─────── X^m ──── T|ψ⟩
          │
|T⟩ ──── H ── Medir → m ∈ {0,1}
```

Si $m=0$: aplicar $I$. Si $m=1$: aplicar $X$ (corrección de Clifford). El resultado es siempre $T|\psi\rangle$.

### 2.2 El problema: los estados mágicos ruidosos

En hardware real, el estado $|T\rangle$ se prepara con ruido. Un estado mágico con fidelidad $f < 1$ introduce errores en la puerta $T$. La fidelidad necesaria para algoritmos útiles es $f > 1 - 10^{-10}$, inalcanzable directamente.

### 2.3 Protocolo de destilación

La **destilación de estados mágicos** (MSD) toma $k$ copias ruidosas de $|T\rangle$ con fidelidad $f$ y produce $m < k$ copias con mayor fidelidad $f'$:

**Protocolo 15-to-1 (Bravyi-Kitaev):**
- Entrada: 15 copias de $|T\rangle$ con error $\varepsilon$ cada una.
- Salida: 1 copia con error $\sim 35\varepsilon^3$.
- Overhead: ratio 15:1 en número de estados mágicos.

```python
import numpy as np

def distill_15_to_1(eps_in: float) -> float:
    """
    Aproximación del error de salida del protocolo 15-to-1 de BK.
    eps_in: error por estado mágico de entrada
    """
    return 35 * eps_in**3

# Cascada de destilaciones
eps0 = 1e-3  # error inicial del hardware (0.1%)
print(f"Error inicial:          {eps0:.2e}")
eps = eps0
for ronda in range(1, 6):
    eps = distill_15_to_1(eps)
    print(f"Tras ronda {ronda} (15→1):   {eps:.2e}")
```

### 2.4 Overhead de recursos para T tolerante a fallos

Cada puerta $T$ lógica requiere un estado mágico destilado. El coste de recursos domina el coste total de algoritmos como Shor.

**Ejemplo: Shor para RSA-2048**

```python
import numpy as np

# Estimaciones (Gidney & Ekerå 2021)
rsa_bits = 2048
T_gates_shor = 4e9         # ~4×10^9 puertas T
distillation_ratio = 15    # protocolo 15→1

# Qubits físicos en la fábrica de estados mágicos
qubits_magic_factory = 1000  # aprox. por fábrica
T_rate_per_factory = 1e6     # T/segundo por fábrica (estimado)
factories_needed = T_gates_shor / (T_rate_per_factory * 3600 * 8)  # en 8 horas

print(f"Puertas T necesarias:      {T_gates_shor:.2e}")
print(f"Fábricas de estados mágicos: {factories_needed:.0f}")
print(f"Tiempo total (1 fábrica):  {T_gates_shor/T_rate_per_factory/3600:.1f} horas")
```

---

## 3. Alternativas a la destilación

### 3.1 Código Reed-Muller: transversalidad de T

El código de Reed-Muller $[[15, 1, 3]]$ permite implementar $T$ de forma transversal pero no implementa $H$ transversalmente. Se puede usar en combinación con el código de superficie.

### 3.2 Code switching

Alternar entre dos códigos complementarios: el código de superficie (transversal en Clifford) y el código Reed-Muller (transversal en T). El cambio de código requiere mediciones adicionales.

### 3.3 Gauge fixing (color codes)

Los códigos de color (Bombin, 2006) permiten implementar el grupo de Clifford transversalmente en 2D y la puerta $T$ transversalmente en 3D, eliminando la necesidad de destilación para algunos circuitos.

---

## 4. Universalidad tolerante a fallos: el cuadro completo

Con estas herramientas, el conjunto de puertas lógicas tolerante a fallos es:

| Puerta | Implementación | Overhead |
|---|---|---|
| $\bar{H}$, $\bar{S}$, $\overline{\text{CNOT}}$ | Transversal (código de superficie) | $O(1)$ |
| $\bar{T}$ | Inyección de estado mágico + MSD | $O(15^L)$ para $L$ rondas |
| Preparación $\bar{|0\rangle}$, $\bar{|+\rangle}$ | Teleportación lógica | $O(d)$ ciclos |
| Medición $\bar{Z}$, $\bar{X}$ | Medición transversal | $O(1)$ |

El conjunto $\{H, S, T, \text{CNOT}\}$ es **universal**: cualquier unitaria puede aproximarse con error $\varepsilon$ usando $O(\log^c(1/\varepsilon))$ puertas (teorema de Solovay-Kitaev, $c \approx 3.97$).

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
import numpy as np

# Verificar que {H, S, T, CNOT} genera todas las unitarias
# Aproximación de Rz(θ) con puertas T y H (secuencia de Solovay-Kitaev)
def rz_approx_clifford_T(theta: float, depth: int = 10) -> QuantumCircuit:
    """Aproximación de Rz(θ) usando puertas {H, S, T, Tdg}."""
    qc = QuantumCircuit(1)
    # Secuencia simple: alternar T y HTH para diferentes fases
    for i in range(depth):
        if (i * theta / np.pi) % 1 < 0.5:
            qc.t(0)
        else:
            qc.h(0); qc.t(0); qc.h(0)
    return qc

# Comparar con Rz exacto
theta = np.pi / 7
qc_exact = QuantumCircuit(1); qc_exact.rz(theta, 0)
qc_approx = rz_approx_clifford_T(theta, depth=20)

U_exact = Operator(qc_exact).data
U_approx = Operator(qc_approx).data
fidelity = abs(np.trace(U_exact.conj().T @ U_approx)) / 2
print(f"Fidelidad de la aproximación: {fidelity:.4f}")
print("(1.0 = perfecto, esta es una demo simplificada)")
```

---

## 5. El coste real: fábricas de estados mágicos

Las **magic state factories** son bloques de hardware dedicados a producir estados $|T\rangle$ destilados de alta fidelidad. Son el componente más costoso de un procesador cuántico tolerante a fallos.

Estimaciones para Shor en RSA-2048:
- **Destilación:** $\sim 10^9$ puertas $T$ → requiere fábricas ejecutando $\sim 10^6$ T/segundo.
- **Tamaño físico:** cada fábrica ocupa $\sim 10^4$ qubits físicos.
- **Fracción del chip:** $\sim 50-80\%$ del chip es fábrica de estados mágicos.

Esto motiva la búsqueda de algoritmos con menos puertas $T$, como las variantes optimizadas de Shor (Gidney & Ekerå 2021) que reducen el conteo de $T$ en $5\times$ respecto a implementaciones naïve.

---

## 6. Resumen

La universalidad tolerante a fallos no es gratuita: el teorema de Eastin-Knill prohíbe un conjunto transversal universal, forzando el uso de estados mágicos y destilación para implementar la puerta $T$. Este overhead, aunque cuantificable y decreciente con mejores hardware, es la principal razón por la que los procesadores cuánticos tolerantes a fallos a escala requieren millones de qubits físicos. La investigación en códigos alternativos (Reed-Muller, color codes, qLDPC) busca reducir este overhead manteniendo las garantías de corrección.

---

*← [01 Teorema del umbral](01_threshold_theorem.md) | [03 Hoja de ruta →](03_hoja_de_ruta_fault_tolerant.md)*
