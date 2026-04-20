# Sampler, Estimator y primitives

## 1. Qué cambia al pasar a primitives

Durante mucho tiempo, la forma de ejecutar circuitos cuánticos se basó en el paradigma de ensamblaje tradicional: diseñabas un circuito, llamabas a `execute(qc, backend)` y parseabas un diccionario de cuentas o un vector de estado de los resultados.

A medida que los algoritmos avanzaban, el ecosistema maduró. Se hizo doloroso gestionar manualmente recuentos estocásticos para intentar inferir la energía de un hamiltoniano usando VQE, o lidiar con sesiones distribuidas entre computadoras clásicas y cuánticas. Así nacieron las **Primitives** en Qiskit: interfaces unificadas y de alto nivel que **encapsulan la ejecución con un claro propósito orientativo de utilidad**. 

Ya no le pides a una computadora cuántica "corre este circuito 1000 veces". En cambio, le pides: "Dime cuál es la probabilidad de que mi respuesta correcta converja aquí" (**Sampler**) o "Calcula la energía de la molécula que acabo de codificar bajo este circuito" (**Estimator**).

## 2. Sampler (Primitive de Muestreo)

La primitive `Sampler` (actualmente estándarizada en `SamplerV2`) está orientada a **distribuciones de salida**.
Conceptualmente, encaja de maravilla cuando lo que buscamos son probabilidades, cuasi-probabilidades, o histogramas directos tras medir las bases z en registros clásicos.

### Cuándo usar el Sampler:
- Algoritmos de oráculos booleanos (Grover, Deutsch-Jozsa) donde buscamos una "tira de bits correcta" $01100$.
- Criptografía cuántica.
- Cuando la lectura de la distribución cruda de errores importa.

### La estructura de su uso:
El `Sampler` toma exclusivamente circuitos cuánticos que tienen puertas de medición explícitas en su final.

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

# 1. Definir circuito con mediciones
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

# 2. Instanciar Sampler y ejecutar
sampler = StatevectorSampler()
job = sampler.run([qc], shots=1024)

# 3. Leer distribución usando el framework de result V2
result = job.result()
# PubResult provee data orientada al número de registros clásicos
counts = result[0].data.meas.get_counts()
print(counts)  # -> {'00': 511, '11': 513}
```

## 3. Estimator (Primitive de Valor Esperado)

`Estimator` responde a una necesidad matemática y física absolutamente central y abrumadoramente usada hoy en día: **calcular valores esperados de observables**.

En lugar de devolverte un diccionario estocástico con recuentos, `Estimator` exige un Observable algebraico físico (por ejemplo construir un Hamiltoniano usando objetos Pauli como $Z \otimes Z$), y un Circuito Cuántico que prepara un Estado. El Estimator cruza internamente el estado preparado contra el observable devolviéndote directamente la media estadística real del experimento $\langle \psi | H | \psi \rangle$ junto con su varianza.

### Cuándo usar el Estimator:
- **Algoritmos variacionales** como VQE (Búsqueda de energía en moléculas) y QAOA (Problemas de optimización).
- Evaluación de magnitudes físicas (magnetización artificial, etc).

### La estructurada de su uso:
A diferencia del Sampler, el Estimator no quiere que midas por tu cuenta el circuito (no querrás interferir colapsando la base), sino que tú le dejas el circuito puro y el observable explícito. 

```python
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp

# 1. Definir un circuito paramétrico puro (Sin measure_all)
qc = QuantumCircuit(1)
qc.x(0)  # Estado |1>

# 2. Definir un Observable algebraico
# Por ejemplo, el proyector Pauli Z. El Z del estado |1> vale -1.
observable = SparsePauliOp(["Z"])

# 3. Lanzar Estimator
estimator = StatevectorEstimator()
job = estimator.run([(qc, observable)])

# 4. Leer resultados
result = job.result()
ev = result[0].data.evs
print(f"Valor Esperado: {ev}") # -> -1.0
```

## 4. Ventaja conceptual y de Qiskit Runtime

La principal ventaja de estas interfaces no es solo comodidad de programación. Cuando utilizamos hardware real a través de IBM Quantum, podemos usar `Sampler` y `Estimator` dentro del servicio en la nube (Qiskit Runtime). Al hacerlo a través de Primitives:

1. **Sesiones Reales:** Puedes mantener una sesión viva sin colas repetitivas en hardware real y hacer cálculos interactivos de VQE de forma híbrida.
2. **Mitigación Integrada:** Internamente, IBM Qiskit Runtime aplica técnicas avanzadísimas matemáticas para limpiar el ruido (Zero Noise Extrapolation) al vuelo y corregir errores cuando le pides un valor `.evs` al `Estimator`.
3. **Abstracción:** Ordena fundamentalmente la cabeza:
   - `Sampler`: me interesan distribuciones y tirar "dados".
   - `Estimator`: me interesa una constante física subyacente determinística.

## 5. Lugar dentro del proyecto

Es fundamental que asumas estas API modernas no como una peculiaridad del ecosistema, sino como el estandar actual de desarrollo de algoritmos de producción. Todos los desarrollos de capas superiores (Surface Codes, Química Computacional variacional) asumen que el "motor" del software usa Estimator para extraer el resultado de energía de los qubits.

## 6. Ideas clave

- Las `primitives` añaden la capa de abstracción definitiva sobre la ejecución de circuitos para estandarizar flujos modernos de algoritmos útiles.
- `Sampler` organiza resultados tipo distribución o muestreo estocástico orientados a lecturas booleanas.
- `Estimator` organiza cálculos implícitos de valor esperado proyectivo conectando directamente variables del circuito en observables de operadores físicos.
- Entender la diferencia separa el conocimiento del programador novel del nivel avanzado de investigador cuántico.

## Navegacion

- Anterior: [Fault tolerance como horizonte](../14_surface_codes_y_horizonte_fault_tolerant/02_fault_tolerance_como_horizonte.md)
- Siguiente: [Operators, Pauli y representaciones utiles](02_operator_y_paulis.md)
