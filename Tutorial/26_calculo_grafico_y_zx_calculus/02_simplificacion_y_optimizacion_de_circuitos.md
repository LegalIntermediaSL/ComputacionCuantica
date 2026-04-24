# Simplificación y optimización gráfica de circuitos

## 1. El problema de la optimización de circuitos

Un compilador cuántico debe transformar un circuito lógico (escrito en puertas universales abstractas) en un circuito equivalente que maximice la fidelidad en el hardware real. Los objetivos principales son:

- **Minimizar profundidad:** reducir el tiempo total de ejecución, limitando el daño de la decoherencia.
- **Minimizar CNOTs (puertas de 2 qubits):** son la operación más ruidosa (error $\sim 1\%$ frente a $\sim 0.1\%$ de las puertas de un qubit).
- **Respetar la conectividad:** asegurar que solo se aplican operaciones entre qubits que son físicamente vecinos.

El ZX-Calculus ofrece un conjunto de herramientas para los dos primeros objetivos.

## 2. El flujo de trabajo de optimización con ZX

```
Circuito Qiskit (puertas estándar)
        ↓  to_graph()
Grafo ZX (arañas + cables)
        ↓  full_reduce() / simp()
Grafo ZX simplificado
        ↓  extract_circuit()
Circuito optimizado (puertas estándar)
```

Cada paso es reversible o verificable: la extracción garantiza que el circuito final es unitariamente equivalente al original (up to global phase).

## 3. Regla de fusión masiva: cómo reduce CNOTs

Considera una secuencia de dos puertas CZ consecutivas sobre el mismo par de qubits:

$$
\text{CZ} \cdot \text{CZ} = I \otimes I
$$

En matrices, esto es la multiplicación de dos matrices $4 \times 4$. En ZX:
1. $\text{CZ}$ = araña Z + araña Z conectadas.
2. Dos $\text{CZ}$ consecutivos = dos pares de arañas Z conectadas.
3. Fusión: las dos arañas Z del qubit 1 se fusionan (fase $\pi + \pi = 2\pi = 0$) → se eliminan (identidad).
4. Igual para las arañas Z del qubit 2.
5. Resultado: circuito vacío.

Este razonamiento funciona para cadenas arbitrarias de puertas ZZ, incluso cuando están intercaladas con otras operaciones que el compilador clásico no conectaría.

## 4. Phase gadgets y QAOA

En el algoritmo QAOA, el operador de costo genera el termino:

$$
e^{-i\gamma Z_i Z_j} = e^{-i\gamma ZZ/2}
$$

En circuito estándar: CNOT + $R_z(2\gamma)$ + CNOT. Pero en ZX, un phase gadget ZZ es simplemente una araña Z con dos cables y fase $\gamma$.

**Fusión de phase gadgets:** si dos phase gadgets ZZ sobre el mismo par de qubits aparecen en distintas capas del circuito, el ZX-Calculus los detecta y fusiona, reduciendo el número de CNOTs a la mitad.

**Regla de conmutación:** dos phase gadgets que no comparten qubits son conmutables en ZX. El compilador puede reordenarlos para crear oportunidades de fusión que no eran evidentes en el orden original.

## 5. Simplificación de estabilizadores: el algoritmo de reducción

PyZX implementa `full_reduce()`, que combina varias reglas:

### 5.1 Eliminación de vértices de interior (local complementation)

Si una araña Z con fase $\pi/2$ (puerta $S$) tiene solo vecinos del mismo tipo, se puede eliminar aplicando una transformación local que modifica las fases de sus vecinos. Esta operación es reversible y nunca aumenta el conteo de vértices.

### 5.2 Eliminación por pivote

Si dos arañas de colores opuestos están conectadas y cada una tiene fase $0$ o $\pi$, se puede aplicar la regla de pivote para eliminar una de ellas.

### 5.3 Reducción de puertas T

Las puertas T (con fase $\pi/4$) no pueden eliminarse mediante reglas estabilizadoras. Son las puertas no-Clifford y el "recurso de magia" del circuito. PyZX cuenta el **T-count** (número de puertas T) y lo minimiza:

- El T-count determina el coste en magia cuántica del circuito.
- Reducir el T-count es equivalente a reducir el número de estados mágicos necesarios para la destilación en computación tolerante a fallos.

## 6. Ejemplo cuantitativo: VQE ansatz

```python
import pyzx as zx
from qiskit import QuantumCircuit
from qiskit.circuit.library import EfficientSU2
from qiskit.qasm2 import dumps

# Crear ansatz VQE de 4 qubits, profundidad 3
n_qubits = 4
depth = 3
ansatz = EfficientSU2(n_qubits, reps=depth, entanglement='linear')
bound_ansatz = ansatz.decompose()

print(f"Circuito original:")
print(f"  Profundidad: {bound_ansatz.depth()}")
print(f"  CNOTs: {bound_ansatz.count_ops().get('cx', 0)}")
print(f"  Total puertas: {sum(bound_ansatz.count_ops().values())}")

# Convertir a PyZX
qasm_str = dumps(bound_ansatz)
pyzx_circ = zx.Circuit.from_qasm(qasm_str)
g = pyzx_circ.to_graph()

print(f"\nGrafo ZX original:")
print(f"  Vértices: {g.num_vertices()}")
print(f"  Aristas: {g.num_edges()}")

# Aplicar simplificación
zx.full_reduce(g)

optimized = zx.extract_circuit(g)
print(f"\nCircuito optimizado con ZX:")
print(f"  Profundidad: {optimized.depth()}")
print(f"  CNOTs: {optimized.count_2q_gates()}")
print(f"  T-count: {optimized.tcount()}")
print(f"  Total puertas: {optimized.num_gates()}")
```

En ansätze variacionales con parámetros fijos (ángulos dados), reducciones típicas:
- CNOTs: 20-40% de reducción.
- Profundidad: 15-30% de reducción.
- T-count: sin cambio (las puertas T son el recurso no-Clifford que no se puede reducir con reglas estabilizadoras).

## 7. Limitaciones del enfoque ZX

El ZX-Calculus no es una solución mágica. Sus limitaciones:

**Extracción no trivial:** simplificar el grafo es fácil; convertirlo de vuelta a un circuito ejecutable (con la topología correcta del hardware) es un problema NP-complejo en general. PyZX usa heurísticas basadas en la descomposición de grafos.

**Parámetros simbólicos:** la fusión de phase gadgets es más difícil cuando las fases son parámetros simbólicos (como en VQE durante el entrenamiento). Las herramientas como `tket` de Quantinuum manejan esto mejor.

**Conectividad del hardware:** el grafo ZX optimizado puede requerir puertas entre qubits no vecinos. La etapa de ruteo (inserción de SWAPs) posterior puede reintroducir la complejidad eliminada.

**No optimiza todo:** la ventaja es mayor en fragmentos Clifford (sin puertas T). Los circuitos con muchas puertas T (como Shor o QPE) son menos beneficiados.

## 8. Herramientas complementarias

Además de PyZX, el ecosistema de compilación cuántica avanzada incluye:

- **`tket` (Quantinuum):** compilador de alta performance con soporte de ZX y otras técnicas. Interfaz Python via `pytket`.
- **BQSKit:** biblioteca de optimización de circuitos del LBNL, más orientada a síntesis de puertas.
- **Quartz:** optimizador basado en egraph (equality saturation) para circuitos cuánticos.
- **Qiskit Transpiler con plugins:** Qiskit 1.x soporta plugins de terceros en el transpilador, incluyendo optimizadores basados en ZX.

```python
# Ejemplo con tket (si disponible)
# from pytket import Circuit
# from pytket.extensions.qiskit import qiskit_to_tk, tk_to_qiskit
# from pytket.passes import FullPeepholeOptimise, CXMappingPass

# tk_circuit = qiskit_to_tk(bound_ansatz)
# FullPeepholeOptimise().apply(tk_circuit)
# optimized_qiskit = tk_to_qiskit(tk_circuit)
# print(f"tket: CNOTs = {optimized_qiskit.count_ops().get('cx', 0)}")
```

## 9. Ideas clave

- El flujo de optimización ZX convierte el circuito en un grafo, aplica reglas de reescritura y extrae el circuito simplificado.
- La fusión de arañas es la regla más poderosa: elimina puertas redundantes en circuitos con muchas operaciones Clifford.
- Los phase gadgets representan compactamente los exponenciales de Pauli de QAOA y VQE, y pueden fusionarse y reordenarse eficientemente.
- El T-count es el indicador del coste en computación tolerante a fallos: reducirlo es el objetivo en compilación post-NISQ.
- La extracción del grafo optimizado a un circuito ejecutable es el cuello de botella y sigue siendo un problema de investigación activo.

## 10. Ejercicios sugeridos

1. Aplicar PyZX a un circuito de Bell ($H$ + CNOT) y verificar que el grafo ZX tiene exactamente 2 vértices tras la simplificación.
2. Comparar el T-count de la puerta Toffoli implementada con puertas estándar (6 puertas T) vs. su implementación óptima conocida (3 puertas T con un ancilla limpio).
3. Implementar el operador $e^{-i\theta Z_0 Z_1 Z_2}$ como phase gadget en ZX y comparar con su implementación como escalera de CNOTs.
4. Estudiar el efecto del ZX-Calculus en un circuito QAOA de 6 qubits para MaxCut: ¿cuántos CNOTs se eliminan para $p=1, 2, 3$ capas?

## Navegación

- Anterior: [El lenguaje de las arañas: introducción al ZX-Calculus](01_el_lenguaje_de_las_aranas.md)
- Siguiente: [Redes y protocolos de entrelazamiento](../27_internet_cuantico_and_comunicaciones/01_redes_y_protocolos_de_entrelazamiento.md)
