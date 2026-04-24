# El lenguaje de las arañas: introducción al ZX-Calculus

## 1. Motivación: más allá de las matrices

El formalismo de circuitos cuánticos con matrices es poderoso pero tiene limitaciones prácticas:
- Para $n$ qubits, las matrices son de $2^n \times 2^n$: impracticable para $n > 20$ en papel.
- Dos circuitos pueden ser idénticos pero verse completamente distintos como matrices.
- El compilador clásico no tiene herramientas para "ver" redundancias estructurales profundas.

El **ZX-Calculus** (Coecke & Duncan, 2008) ofrece un lenguaje gráfico alternativo: los estados y operaciones se representan como grafos, y la equivalencia entre circuitos se demuestra aplicando **reglas de reescritura gráfica** sin multiplicar matrices. Es completo: cualquier igualdad de matrices puede demostrarse solo con las reglas gráficas.

## 2. Los objetos básicos: arañas

El vocabulario del ZX-Calculus tiene dos tipos de nodos:

### 2.1 Araña Z (verde)

Una araña Z con $m$ entradas, $n$ salidas y fase $\alpha$ representa el tensor:

$$
Z_\alpha^{(m,n)} = |0\rangle^{\otimes n}\langle 0|^{\otimes m} + e^{i\alpha}|1\rangle^{\otimes n}\langle 1|^{\otimes m}
$$

Casos especiales:
- $Z_0^{(1,1)}$ = identidad $I$ (sin fase, un cable).
- $Z_\pi^{(1,1)}$ = puerta $Z$.
- $Z_\alpha^{(1,1)}$ = rotación $R_z(\alpha) = \begin{pmatrix}1&0\\0&e^{i\alpha}\end{pmatrix}$.
- $Z_0^{(2,1)}$ = operación que copia la base computacional (CNOT sin normalización).

### 2.2 Araña X (roja)

La araña X es la versión en la base de Hadamard:

$$
X_\alpha^{(m,n)} = |+\rangle^{\otimes n}\langle +|^{\otimes m} + e^{i\alpha}|-\rangle^{\otimes n}\langle -|^{\otimes m}
$$

Casos especiales:
- $X_\alpha^{(1,1)}$ = rotación $R_x(\alpha)$.
- $X_\pi^{(1,1)}$ = puerta $X$ (NOT).

### 2.3 La puerta Hadamard como caja amarilla

La puerta Hadamard $H$ convierte arañas Z en arañas X y viceversa. Se dibuja como una caja amarilla en los cables.

### 2.4 Escalar

El escalar (sin entradas ni salidas) representa la norma de la amplitud global del circuito. En muchos cálculos se ignora (se trabaja "up to scalar").

## 3. Reglas de reescritura

Las reglas del ZX-Calculus son las transformaciones que preservan la igualdad entre grafos. Las fundamentales son:

### Regla 1: Spider Fusion (fusión de arañas)

Dos arañas del **mismo color** conectadas por al menos un cable pueden fusionarse en una sola sumando sus fases:

$$
Z_\alpha \cdot Z_\beta = Z_{\alpha+\beta}
$$

Esto generaliza la identidad $R_z(\alpha)R_z(\beta) = R_z(\alpha+\beta)$.

### Regla 2: Identity removal (eliminación de identidad)

Una araña con fase 0 y exactamente dos cables conectados es simplemente un cable directo:

$$
Z_0^{(1,1)} = \text{cable}
$$

### Regla 3: Copy (copiado)

Una araña X con fase 0 puede "copiar" la fase de una araña Z hacia sus cables:

$$
Z_\alpha \text{ conectada a } X_0 \to \text{se distribuye la fase } \alpha
$$

### Regla 4: Bialgebra

La relación entre arañas Z y X sigue la regla de bialgebra, que permite intercambiar el orden de algunas operaciones:

$$
Z - X \sim X - Z \text{ con reordenamiento de cables}
$$

### Regla 5: Hopf

Si dos arañas del mismo color están conectadas por dos cables paralelos, pueden simplificarse eliminando ambos cables.

### Regla 6: Euler (descomposición de H)

La puerta Hadamard se puede escribir como una secuencia de rotaciones:

$$
H = R_z(\pi/2) \cdot R_x(\pi/2) \cdot R_z(\pi/2) \text{ (up to global phase)}
$$

O en términos de arañas:

$$
\text{Caja amarilla} = Z_{\pi/2} \cdot X_{\pi/2} \cdot Z_{\pi/2}
$$

## 4. Traducción de puertas estándar a ZX

| Puerta | Representación ZX |
|---|---|
| $I$ | Araña Z (o X) con $\alpha=0$ y 2 cables |
| $X$ | Araña X con $\alpha=\pi$ |
| $Z$ | Araña Z con $\alpha=\pi$ |
| $H$ | Caja amarilla |
| $R_z(\alpha)$ | Araña Z con fase $\alpha$, un cable de entrada, un cable de salida |
| $R_x(\alpha)$ | Araña X con fase $\alpha$ |
| $S$ | Araña Z con $\alpha=\pi/2$ |
| $T$ | Araña Z con $\alpha=\pi/4$ |
| $\text{CNOT}$ | Araña Z (control) + Araña X (target) + cable de conexión |
| $\text{CZ}$ | Araña Z + Araña Z + cable de conexión |

## 5. Ejemplo: simplificación de $HZH = X$

En matrices: $H \begin{pmatrix}1&0\\0&-1\end{pmatrix} H = \begin{pmatrix}0&1\\1&0\end{pmatrix}$.

En ZX-Calculus:
1. $Z$ = araña Z con $\alpha=\pi$.
2. $H$ cambia araña Z → araña X.
3. $H \cdot Z_\pi \cdot H$ = caja amarilla + $Z_\pi$ + caja amarilla.
4. Aplicando la regla de Euler: las dos cajas amarillas que rodean a $Z_\pi$ lo convierten en $X_\pi$.
5. $X_\pi$ = puerta $X$. $\square$

## 6. Phase gadgets: patrones en QAOA

Un **phase gadget** de $n$ qubits con fase $\theta$ implementa $e^{-i\theta Z^{\otimes n}/2}$. En circuitos estándar, esto requiere una escalera de $n-1$ CNOTs. En ZX-Calculus, es simplemente una araña Z con $n$ cables y fase $\theta$.

Manipular phase gadgets directamente en el grafo ZX permite reordenarlos, fusionarlos y cancelarlos sin expandirlos en CNOTs, descubriendo simplificaciones que un compilador clásico no vería.

## 7. Herramientas: PyZX

```python
import pyzx as zx
from qiskit import QuantumCircuit
from qiskit.qasm2 import dumps

# Crear un circuito de ejemplo
qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.h(0)
qc.h(1)
qc.h(2)
qc.cx(0, 1)
qc.cx(1, 2)
qc.h(0)
print("Circuito original:")
print(qc.draw())
print(f"Profundidad original: {qc.depth()}, CNOTs: {qc.count_ops().get('cx', 0)}")

# Convertir a PyZX y simplificar
qasm_str = dumps(qc)
pyzx_circuit = zx.Circuit.from_qasm(qasm_str)

# Convertir a grafo ZX
g = pyzx_circuit.to_graph()
print(f"\nVértices en el grafo ZX: {g.num_vertices()}")
print(f"Aristas en el grafo ZX: {g.num_edges()}")

# Aplicar simplificación (full_reduce usa las reglas del ZX-Calculus)
zx.full_reduce(g)
print(f"Vértices tras simplificación: {g.num_vertices()}")
print(f"Aristas tras simplificación: {g.num_edges()}")

# Extraer circuito simplificado
optimized_circuit = zx.extract_circuit(g)
print(f"\nProfundidad tras ZX: {optimized_circuit.depth()}")
print(f"CNOTs tras ZX: {optimized_circuit.count_2q_gates()}")
```

## 8. Ideas clave

- El ZX-Calculus es un lenguaje gráfico completo para la mecánica cuántica: cualquier igualdad matricial se puede demostrar solo con reglas gráficas.
- Los dos tipos de nodos (arañas Z y X) se relacionan por la puerta Hadamard (caja amarilla).
- La regla de fusión es la más poderosa: arañas del mismo color conectadas se funden en una.
- Los phase gadgets son representaciones compactas de operaciones multiqubit frecuentes en QAOA y VQE.
- PyZX implementa el ZX-Calculus con reglas de simplificación que pueden reducir el conteo de CNOT en un 20-40% en algoritmos variacionales.

## 9. Ejercicios sugeridos

1. Demostrar con las reglas de ZX-Calculus que $\text{CNOT} \cdot (H \otimes I) \cdot \text{CNOT} = \text{CNOT} \cdot (H \otimes H) \cdot \text{CNOT} \cdot (I \otimes H)$ (equivalencia entre CNOT y CZ).
2. Traducir el circuito de Bell $H_0 \cdot \text{CNOT}_{01}$ a ZX y verificar que genera el estado $|\Phi^+\rangle$.
3. Instalar PyZX y simplificar un circuito aleatorio de 10 qubits y profundidad 20. ¿Cuántos CNOTs se eliminan?
4. Explicar por qué el ZX-Calculus no puede simplificar circuitos con puertas T no múltiplas de $\pi/2$ usando solo las reglas del fragmento estabilizador.

## Navegación

- Anterior: [Criptografía post-cuántica (PQC)](../25_criptografia_post_cuantica_pqc/01_criptografia_post_cuantica_pqc.md)
- Siguiente: [Simplificación y optimización de circuitos](02_simplificacion_y_optimizacion_de_circuitos.md)
