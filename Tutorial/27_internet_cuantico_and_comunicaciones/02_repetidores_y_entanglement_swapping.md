# Repetidores cuánticos y entanglement swapping

## 1. El problema de extender el entrelazamiento

En el capítulo anterior vimos que la atenuación en fibra óptica limita la distribución directa de entrelazamiento a distancias de ~100-200 km. Para conectar ciudades o países necesitamos una cadena de nodos intermedios que extiendan el entrelazamiento sin violar el teorema de no-clonación.

La técnica central es el **entanglement swapping** (intercambio de entrelazamiento): combinar dos pares de Bell cortos para crear un par de Bell largo, sin que los extremos de la cadena hayan interactuado físicamente.

## 2. Entanglement swapping: el mecanismo

### 2.1 El protocolo básico

Supongamos tres nodos: Alice (A), Repetidor (R) y Bob (B).

1. La fuente izquierda genera un par entrelazado entre A y R: $|\Phi^+\rangle_{AR_1}$.
2. La fuente derecha genera un par entrelazado entre R y B: $|\Phi^+\rangle_{R_2 B}$.
3. El estado total es:
   $$
   |\Phi^+\rangle_{AR_1} \otimes |\Phi^+\rangle_{R_2 B}
   $$
4. El Repetidor realiza una **medición de Bell** sobre sus dos qubits $(R_1, R_2)$.
5. Después de la medición, los qubits de A y B quedan entrelazados $|\Phi_{\pm}\rangle_{AB}$ (con una corrección de Pauli dependiente del resultado de la medición, comunicada clásicamente).

### 2.2 ¿Por qué funciona?

El estado de cuatro qubits antes de la medición de Bell es:

$$
|\Phi^+\rangle_{AR_1} \otimes |\Phi^+\rangle_{R_2 B} = \frac{1}{4}\sum_{i\in\{0,1,2,3\}} |\Phi_i\rangle_{R_1 R_2} \otimes |\Phi_i\rangle_{AB}
$$

donde $|\Phi_0\rangle = |\Phi^+\rangle$, $|\Phi_1\rangle = |\Phi^-\rangle$, $|\Phi_2\rangle = |\Psi^+\rangle$, $|\Phi_3\rangle = |\Psi^-\rangle$.

Cuando el Repetidor mide y obtiene el resultado $i$, los qubits A y B colapsan al estado $|\Phi_i\rangle_{AB}$ correspondiente. Alice aplica la corrección de Pauli adecuada (comunicada clásicamente por el Repetidor) y obtiene $|\Phi^+\rangle_{AB}$.

El resultado: A y B están entrelazados aunque nunca hayan interactuado.

### 2.3 Implementación en Qiskit

```python
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.primitives import StatevectorSampler
import numpy as np

def entanglement_swapping_circuit() -> QuantumCircuit:
    """
    Circuito de entanglement swapping:
    A (q0) entrelazado con R1 (q1), R2 (q2) entrelazado con B (q3).
    El repetidor mide (q1, q2) en la base de Bell y corrige A o B.
    """
    # 4 qubits: A=q0, R1=q1, R2=q2, B=q3
    # 2 bits clásicos para el resultado de la medición de Bell
    qr = QuantumRegister(4, 'q')
    cr = ClassicalRegister(2, 'c')
    qc = QuantumCircuit(qr, cr)

    # Paso 1: Crear par entrelazado A-R1
    qc.h(0)       # Hadamard en A
    qc.cx(0, 1)   # CNOT A→R1 → par |Φ+>_{A,R1}

    # Paso 2: Crear par entrelazado R2-B
    qc.h(2)       # Hadamard en R2
    qc.cx(2, 3)   # CNOT R2→B → par |Φ+>_{R2,B}

    qc.barrier()

    # Paso 3: Medición de Bell en el Repetidor (R1=q1, R2=q2)
    qc.cx(1, 2)   # CNOT R1→R2 (Bell basis change)
    qc.h(1)       # Hadamard en R1
    qc.measure(1, 0)  # Medir R1 → c[0]
    qc.measure(2, 1)  # Medir R2 → c[1]

    # Paso 4: Correcciones de Pauli en B según resultado de la medición
    # Si c[0]=1: aplicar Z en B; si c[1]=1: aplicar X en B
    with qc.if_test((cr[0], 1)):
        qc.z(3)  # Corrección Z
    with qc.if_test((cr[1], 1)):
        qc.x(3)  # Corrección X

    return qc

qc = entanglement_swapping_circuit()
print("Circuito de Entanglement Swapping:")
print(qc.draw())

# Verificar: A (q0) y B (q3) deben estar entrelazados tras el swapping
# Medir en la base de Bell para verificar correlaciones
verification_qc = qc.copy()
verification_qc.cx(0, 3)
verification_qc.h(0)
verification_qc.measure_all()

sampler = StatevectorSampler()
result = sampler.run([verification_qc], shots=1024).result()
counts = result[0].data.meas.get_counts()
print(f"\nResultados de verificación (deben ser 00xx o 11xx):")
for state, count in sorted(counts.items()):
    print(f"  |{state}⟩: {count}")
```

## 3. Purificación de entrelazamiento

### 3.1 El problema del ruido

En la práctica, los pares de Bell generados por la fuente no son perfectos: la decoherencia durante la transmisión y el almacenamiento los degrada. Un par ruidoso se describe por una matriz de densidad:

$$
\rho = F|\Phi^+\rangle\langle\Phi^+| + (1-F)\frac{I}{4}
$$

donde $F$ es la **fidelidad** del par y $(1-F)/4$ es la mezcla con el estado máximamente mixto. Para un par utlizable en protocolos cuánticos, se necesita $F > 0.5$.

### 3.2 Protocolo de purificación (DEJMPS)

El protocolo de Deutsch-Ekert-Jozsa-Macchiavello-Plenio-Sanpera (DEJMPS) toma **dos pares de baja fidelidad** y produce **un par de alta fidelidad** con alguna probabilidad:

1. Alice y Bob comparten dos pares de Bell ruidosos: $\rho_1 \otimes \rho_2$.
2. Alice aplica un CNOT entre sus dos qubits (primero del par 1 como control, primero del par 2 como target).
3. Bob hace lo mismo con sus qubits.
4. Alice y Bob miden el par 2 y comparan sus resultados clásicamente.
5. Si los resultados coinciden, el par 1 ha aumentado su fidelidad:
   $$
   F' = \frac{F^2 + \left(\frac{1-F}{3}\right)^2}{F^2 + \frac{2F(1-F)}{3} + 5\left(\frac{1-F}{3}\right)^2}
   $$
6. Si no coinciden, descartan el par 1 (probabilidad de éxito $\sim F^2 + (1-F)^2/9$).

Aplicando la purificación repetidamente (destilación de entrelazamiento), se puede obtener pares con $F \to 1$ a costa de consumir más pares iniciales.

### 3.3 Coste de la purificación

Para llegar de $F_0 = 0.7$ a $F = 0.99$ se necesitan aproximadamente $n \sim 100$ pares iniciales por cada par puro obtenido. Esto es un overhead significativo pero manejable comparado con la imposibilidad de la transmisión directa.

## 4. Repetidores cuánticos: la cadena completa

Una cadena de repetidores cuánticos para distancia $L$ con $n$ nodos intermedios funciona así:

1. Dividir la distancia $L$ en $n+1$ segmentos de longitud $\ell = L/(n+1)$.
2. **Generación:** establecer pares de Bell entre cada par de nodos vecinos.
3. **Purificación:** refinar la fidelidad de cada par hasta $F_\text{target}$.
4. **Swapping:** encadenar los pares usando entanglement swapping para crear un par extremo-a-extremo.

La tasa de generación de pares escala con el número de nodos:

$$
R \sim \frac{c}{L} \cdot p_\text{succ}^{\log_2(n+1)}
$$

donde $p_\text{succ}$ es la probabilidad de éxito por operación. La dependencia es **polinomial** en $L$ (frente a exponencial sin repetidores).

## 5. Memorias cuánticas: el eslabón crítico

Los repetidores cuánticos requieren **memorias cuánticas**: dispositivos que almacenan un estado cuántico el tiempo suficiente para que llegue el resultado de las operaciones de los otros nodos (comunicado clásicamente a la velocidad de la luz).

El tiempo de espera máximo para un segmento de $\ell$ km es $\ell/c \approx 3.3\,\mu\text{s/km}$. Para 100 km entre nodos: $t_\text{espera} \sim 330\,\mu\text{s}$.

Tecnologías candidatas:
- **Centros NV en diamante:** $T_2 \sim 1\,\text{ms}$ (a temperatura ambiente), $\sim 1\,\text{s}$ (a baja temperatura).
- **Iones atrapados:** $T_2 \sim 1\,\text{min}$. Posibles, pero difíciles de acoplar a fotones.
- **Ensembles de átomos fríos** (AFC, Atomic Frequency Comb): $T_2 \sim 10\,\text{ms}$ en fibra.

## 6. Blind Quantum Computing

Una de las aplicaciones más interesantes del internet cuántico es la **computación cuántica ciega** (Blind Quantum Computing, BQC): un cliente cuántico débil (sin capacidades de cómputo cuántico completo) puede delegar cálculos a un servidor cuántico potente de forma que el servidor no sepa qué está calculando.

El protocolo de Broadbent-Fitzsimons-Kashefi (BFK, 2009):

1. El cliente prepara qubits en estados $|+\theta\rangle = \frac{1}{\sqrt{2}}(|0\rangle + e^{i\theta}|1\rangle)$ con ángulos $\theta$ aleatorios y los envía al servidor.
2. El servidor genera un **cluster state** con los qubits del cliente.
3. El cliente envía instrucciones de medición al servidor, modificadas con sus ángulos secretos $\theta$.
4. El servidor mide y devuelve los resultados clásicos.
5. El cliente corrige los resultados usando sus ángulos secretos.

Resultado: el servidor ve solo estados aleatorios y resultados de mediciones sin correlación aparente. No puede inferir el algoritmo ni los datos. La seguridad es incondicional bajo la mecánica cuántica.

## 7. Estado actual del Internet Cuántico (2024-2026)

| Proyecto | País | Alcance | Estado |
|---|---|---|---|
| QuTech Delft | Países Bajos | Red de 3 nodos (200 km) | Operativo (NV en diamante) |
| SECOQC / OpenQKD | Europa | Red pan-europea QKD | Demostración |
| Quantum Internet Alliance | Europa | Hoja de ruta 2030 | Planificación |
| Micius | China | Satélite → 7600 km | Operativo |
| EPB Quantum Network | EEUU | Chattanooga, Tennessee | Operativo (fibra local) |
| Q-NEXT / EQnet | EEUU | Red de laboratorios DOE | En desarrollo |

La red de Delft (QuTech, 2022) fue la primera en demostrar repetidores cuánticos genuinos: tres nodos conectados con memorias de NV en diamante y entanglement swapping verificado con $F > 0.8$.

## 8. Ideas clave

- El entanglement swapping extiende el entrelazamiento a distancias arbitrarias sin violar el teorema de no-clonación: el Repetidor mide en la base de Bell y comunica el resultado clásicamente.
- La purificación de entrelazamiento destila pares de alta fidelidad a partir de múltiples pares ruidosos.
- Las memorias cuánticas (NV en diamante, iones, ensembles atómicos) son el componente limitante de los repetidores cuánticos actuales.
- El Blind Quantum Computing permite computación privada verificable: el servidor no puede conocer el algoritmo ni los datos del cliente.
- La red de Delft (2022) es el primer repetidor cuántico genuino operativo; la red pan-europea QKD está en fase de demostración.

## 9. Ejercicios sugeridos

1. Simular el protocolo de purificación DEJMPS en Qiskit para $F_0 = 0.75$ y calcular la fidelidad $F'$ del par purificado.
2. Estimar la tasa de generación de pares de Bell a 1000 km con $n=10$ repetidores, segmentos de 100 km y $p_\text{succ} = 0.9$ por nodo.
3. Verificar con la simulación de Qiskit que el entanglement swapping produce $|\Phi^+\rangle_{AB}$ a partir de $|\Phi^+\rangle_{AR} \otimes |\Phi^+\rangle_{RB}$.
4. Describir el protocolo de BQC en términos del modelo de computación MBQC (Measurement-Based Quantum Computing) y explicar por qué el servidor no puede inferir el algoritmo del cliente.

## Navegación

- Anterior: [Redes y protocolos de entrelazamiento](01_redes_y_protocolos_de_entrelazamiento.md)
- Siguiente: [Qué puede y que no puede hacer la computación cuántica hoy](../../13_limites_actuales_y_realismo/01_que_puede_y_que_no_puede_hacer_la_computacion_cuantica_hoy.md)
