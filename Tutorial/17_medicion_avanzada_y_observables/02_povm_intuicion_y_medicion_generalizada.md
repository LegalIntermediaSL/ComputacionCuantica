# POVM: medición generalizada

## 1. Más allá de las medidas proyectivas

Las medidas proyectivas tienen una propiedad restrictiva: los proyectores $\{P_k\}$ son ortogonales entre sí ($P_k P_l = \delta_{kl} P_k$) y están limitados a tener como máximo $d$ resultados (siendo $d$ la dimensión del espacio de Hilbert). Para un qubit, solo dos resultados.

En la práctica experimental, hay situaciones donde se quieren más resultados que la dimensión del sistema, o donde la ortogonalidad es demasiado restrictiva:

- **Discriminación de estados no ortogonales:** dado un estado desconocido de un conjunto $\{|\psi_1\rangle, |\psi_2\rangle\}$ no ortogonal, identificarlo con la menor probabilidad de error posible.
- **Medidas débiles:** obtener información parcial del estado sin colapsarlo completamente.
- **Criptografía cuántica (QKD):** el protocolo BB84 usa cuatro estados en dos bases no ortogonales.

El marco generalizado que cubre todos estos casos son las **medidas POVM** (Positive Operator-Valued Measure).

## 2. Definición matemática

Una POVM es un conjunto de operadores $\{E_i\}$ que satisfacen:

- **Positividad:** $E_i \geq 0$ (semidefinidos positivos) para todo $i$.
- **Completitud:** $\sum_i E_i = I$.

La probabilidad de obtener el resultado $i$ en el estado $\rho$ es:

$$
p_i = \text{Tr}(E_i \rho)
$$

Los operadores $E_i$ no necesitan ser proyectores (no se requiere $E_i^2 = E_i$) ni ortogonales. Un qubit puede tener 3, 4 o más resultados POVM.

Las medidas proyectivas son un caso especial de POVM donde $E_i = P_i$ son proyectores ortogonales.

## 3. Implementación mediante dilatación (teorema de Neumark)

Toda POVM en un espacio de Hilbert de dimensión $d$ puede implementarse como:

1. Ampliar el espacio acoplando un sistema auxiliar (ancilla).
2. Aplicar una evolución unitaria sobre el sistema compuesto.
3. Realizar una medida proyectiva estándar solo sobre la ancilla.

Este resultado (teorema de Neumark o dilatación de Stinespring) muestra que toda medida generalizada es, en principio, realizable en hardware cuántico añadiendo qubits auxiliares.

## 4. Ejemplo: trine POVM de un qubit

Una de las POVM más simétricas para un qubit es la **trine POVM**, con tres elementos correspondientes a vectores igualmente espaciados en el plano ecuatorial de la esfera de Bloch:

$$
|v_k\rangle = \cos\frac{\pi}{3}(k-1)|0\rangle + \sin\frac{\pi}{3}(k-1)|1\rangle, \quad k = 1, 2, 3
$$

Los operadores POVM son:

$$
E_k = \frac{2}{3}|v_k\rangle\langle v_k|
$$

Se puede verificar que $\sum_k E_k = I$ y $E_k \geq 0$. Esta POVM da más información sobre la dirección de un qubit en el plano ecuatorial que cualquier medida proyectiva de dos resultados.

## 5. Discriminación de estados cuánticos

Un problema clásico donde las POVM superan a las medidas proyectivas es la discriminación de dos estados no ortogonales $|\psi_0\rangle$ y $|\psi_1\rangle$ con probabilidades a priori $p_0$ y $p_1$.

**Medida de Helstrom:** la POVM óptima que minimiza la probabilidad de error $P_e$ da:

$$
P_e = \frac{1}{2}\left(1 - \sqrt{1 - 4p_0 p_1 |\langle\psi_0|\psi_1\rangle|^2}\right)
$$

Para el caso de estados igualmente probables ($p_0 = p_1 = 1/2$):

$$
P_e = \frac{1}{2}\left(1 - \sqrt{1 - |\langle\psi_0|\psi_1\rangle|^2}\right)
$$

Si los estados son ortogonales ($|\langle\psi_0|\psi_1\rangle| = 0$), la discriminación es perfecta ($P_e = 0$). Si son idénticos ($|\langle\psi_0|\psi_1\rangle| = 1$), no hay discriminación posible ($P_e = 1/2$).

## 6. Medidas débiles

Las **medidas débiles** (weak measurements) son un tipo especial de POVM donde los operadores $E_i$ están muy cerca de la identidad: la medición extrae poca información pero perturba poco el estado.

Una secuencia de medidas débiles seguida de una medida fuerte (postselección) permite medir el **valor débil** de un observable, que puede estar fuera del rango de los autovalores ordinarios. Este fenómeno, descubierto por Aharonov, Albert y Vaidman (1988), tiene aplicaciones en metrología de precisión.

## 7. Implementación en Qiskit

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
import numpy as np

def trine_povm_circuit() -> QuantumCircuit:
    """
    Implementa la trine POVM mediante dilatación:
    añade una ancilla de 2 qubits para codificar 3 resultados.
    Implementación simplificada para el resultado k=0.
    """
    # Sistema: qubit 0. Ancilla: qubits 1,2
    qc = QuantumCircuit(3, 2)

    # Preparar el estado bajo test en qubit 0: aquí |+>
    qc.h(0)

    # Evolución unitaria de dilatación (simplificada)
    qc.cx(0, 1)
    qc.h(0)
    qc.t(1)
    qc.cx(1, 2)

    # Medir la ancilla
    qc.measure([1, 2], [0, 1])
    return qc

# Ejemplo simplificado: POVM de 3 resultados en el plano ecuatorial
def sym_informationally_complete_povm(state_vec):
    """
    Calcula las probabilidades de una SIC-POVM de 4 elementos para 1 qubit.
    Los 4 tetrahedro de Bloch.
    """
    # Vectores del tetraedro inscrito en la esfera de Bloch
    tetrahedron = [
        np.array([1, 0]),
        np.array([1/np.sqrt(3), np.sqrt(2/3)]),
        np.array([1/np.sqrt(3), np.sqrt(2/3) * np.exp(2j*np.pi/3)]),
        np.array([1/np.sqrt(3), np.sqrt(2/3) * np.exp(4j*np.pi/3)]),
    ]
    # Operadores SIC-POVM: E_k = |psi_k><psi_k| / 2
    probs = []
    for psi in tetrahedron:
        E = np.outer(psi, psi.conj()) / 2
        p = np.real(np.trace(E @ np.outer(state_vec, state_vec.conj())))
        probs.append(p)
    return probs

# Estado de prueba |+>
plus_state = np.array([1, 1]) / np.sqrt(2)
probs = sym_informationally_complete_povm(plus_state)
print("Probabilidades SIC-POVM para |+>:", [f"{p:.3f}" for p in probs])
print(f"Suma de probabilidades: {sum(probs):.6f}")
```

## 8. Ideas clave

- Las POVM generalizan las medidas proyectivas: permiten más resultados que la dimensión del sistema y no requieren ortogonalidad.
- Una POVM es un conjunto de operadores semidefinidos positivos que suman la identidad: $E_i \geq 0$, $\sum_i E_i = I$.
- Toda POVM puede implementarse como una medida proyectiva sobre un sistema ampliado (teorema de Neumark).
- Las POVM son óptimas para discriminación de estados no ortogonales y medidas de información mínima.
- Las medidas débiles son un caso especial de POVM donde la perturbación del estado es mínima.

## 9. Ejercicios sugeridos

1. Verificar que la trine POVM $E_k = \frac{2}{3}|v_k\rangle\langle v_k|$ satisface $\sum_k E_k = I$.
2. Calcular la probabilidad de error de Helstrom para discriminar $|0\rangle$ y $|+\rangle$.
3. Diseñar una POVM de 3 elementos para un qubit que no sea la trine POVM pero satisfaga las condiciones de positividad y completitud.
4. Explicar por qué no existe ninguna POVM que distinga perfectamente dos estados no ortogonales.

## Navegacion

- Anterior: [Proyectores, valores esperados y varianza](01_proyectores_valores_esperados_y_varianza.md)
- Siguiente: [BQP, oraculos y speedup](../18_complejidad_cuantica/01_bqp_oraculos_y_speedup.md)
