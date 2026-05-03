# Módulo 49 — D-Wave, Annealing Cuántico y QUBO

El **annealing cuántico** es el paradigma de computación cuántica más maduro en términos de escala de hardware: D-Wave Advantage tiene más de 5000 qubits físicos y lleva resolviéndose problemas combinatorios desde 2011. Sin embargo, es fundamentalmente distinto al modelo de circuito de puertas: no ejecuta algoritmos universales, sino que implementa una búsqueda de energía mínima directamente en hardware analógico.

La idea es simple y poderosa: cualquier problema de optimización combinatoria que se pueda formular como minimización de una función cuadrática en variables binarias (QUBO) se puede mapear al Hamiltoniano de Ising de D-Wave y dejar que el sistema encuentre el estado de menor energía mediante túnel cuántico a través de barreras energéticas que el annealing clásico (simulated annealing) no traversaría eficientemente.

---

## Índice

1. [Annealing cuántico — principios físicos](#1-annealing)
2. [QUBO — formulación matemática](#2-qubo)
3. [Mapeo de problemas combinatorios a QUBO](#3-mapeo)
4. [D-Wave Advantage — arquitectura Pegasus](#4-dwave)
5. [dimod — librería D-Wave para Python](#5-dimod)
6. [Comparativa D-Wave vs QAOA](#6-comparativa)
7. [Otras plataformas de annealing 2025](#7-plataformas)
8. [Ejercicios](#8-ejercicios)
9. [Referencias](#9-referencias)

---

## 1. Annealing Cuántico — Principios Físicos {#1-annealing}

### 1.1 El Hamiltoniano transverso-Ising

El Hamiltoniano de un sistema de annealing cuántico con $N$ espines tiene la forma:

$$
H(s) = -A(s)\sum_{i=1}^{N} \hat{\sigma}_i^x - B(s) H_P
$$

donde:
- $s \in [0, 1]$ es el parámetro de annealing que varía en el tiempo ($s = t/T_{\text{anneal}}$)
- $A(s)$ es la amplitud del campo transverso (términos cuánticos de tunneling)
- $B(s)$ es la amplitud del Hamiltoniano de problema $H_P$
- $\hat{\sigma}_i^x$ es el operador de Pauli X en el espín $i$ (genera superposición y tunneling)
- $H_P = -\sum_i h_i \hat{\sigma}_i^z - \sum_{i<j} J_{ij} \hat{\sigma}_i^z \hat{\sigma}_j^z$ es el Hamiltoniano de Ising del problema

### 1.2 Schedule A(s) y B(s)

El schedule define cómo evoluciona el sistema:

| Inicio ($s=0$) | Fin ($s=1$) |
|----------------|-------------|
| $A(0) \gg B(0)$ | $A(1) \approx 0$ |
| Campo transverso dominante | Hamiltoniano de problema dominante |
| Estado inicial: superposición de todos los estados | Estado final: solución del problema |
| $H \approx -A_0 \sum_i \sigma_i^x$ | $H \approx -B_1 H_P$ |

El estado inicial es el estado fundamental del campo transverso, que es la superposición uniforme:

$$
|\psi(0)\rangle = \frac{1}{2^{N/2}} \sum_{z \in \{0,1\}^N} |z\rangle = |+\rangle^{\otimes N}
$$

### 1.3 Teorema adiabático

El **teorema adiabático de la mecánica cuántica** (Born-Fock, 1928) garantiza que si el Hamiltoniano varía suficientemente despacio, el sistema permanece en el estado fundamental a lo largo de toda la evolución. La condición es:

$$
T_{\text{anneal}} \gg \frac{\max_{s} |\langle 1(s)| \dot{H}(s) |0(s)\rangle|}{g_{\min}^2}
$$

donde $g_{\min}$ es el **gap espectral mínimo** (diferencia de energía entre el estado fundamental y el primer estado excitado a lo largo del schedule), y $|0(s)\rangle$, $|1(s)\rangle$ son el estado fundamental e inmediatamente superior.

El problema práctico: para instancias difíciles del problema (fases vítreas de espín, instancias de 3-SAT aleatorias), $g_{\min}$ puede ser exponencialmente pequeño en $N$, requiriendo $T_{\text{anneal}}$ exponencialmente largo. Esto es la manifestación del problema NP-hard en el lenguaje cuántico.

### 1.4 Diferencia con el modelo de circuito de puertas

| Aspecto | Annealing cuántico (D-Wave) | Modelo de circuito (IBM, Quantinuum) |
|---------|----------------------------|--------------------------------------|
| Evolución | Continua, analógica | Discreta, digital |
| Universalidad | No universal (solo optimización) | Universal |
| Número de qubits | 5000+ (físicos, baja fidelidad) | 100–1000 (alta fidelidad) |
| Coherencia | Muy corta (~ns), pero schedule largo | $T_2 \sim$ µs–ms |
| Programación | Especificar $h_i$, $J_{ij}$ | Secuencia de puertas |
| Tipo de problema | Minimización energía (QUBO/Ising) | Cualquier algoritmo cuántico |
| Estado actual | Comercial, ~15 años de experiencia | Investigación/early commercial |

D-Wave no compite directamente con IBM o Quantinuum — resuelve una clase diferente de problemas de forma diferente.

---

## 2. QUBO — Formulación Matemática {#2-qubo}

### 2.1 Definición

Un problema **QUBO** (Quadratic Unconstrained Binary Optimization) consiste en minimizar:

$$
E(\mathbf{x}) = \mathbf{x}^T Q \mathbf{x} = \sum_{i} Q_{ii} x_i + \sum_{i<j} Q_{ij} x_i x_j
$$

donde:
- $\mathbf{x} \in \{0, 1\}^n$ es el vector de variables binarias de decisión
- $Q \in \mathbb{R}^{n \times n}$ es la **matriz QUBO** (simétrica o triangular superior)
- $Q_{ii}$ son los términos lineales (energías locales de cada variable)
- $Q_{ij}$ ($i \neq j$) son los términos de interacción cuadrática entre pares de variables

### 2.2 Equivalencia con el modelo de Ising

QUBO y el modelo de Ising son equivalentes mediante la sustitución $x_i = (1 - s_i)/2$ donde $s_i \in \{-1, +1\}$:

$$
E_{\text{Ising}}(\mathbf{s}) = -\sum_{i<j} J_{ij} s_i s_j - \sum_i h_i s_i
$$

Los coeficientes se relacionan como:

$$
J_{ij} = -\frac{Q_{ij}}{4}, \qquad h_i = \frac{Q_{ii}}{2} + \frac{1}{4}\sum_{j \neq i} Q_{ij}
$$

### 2.3 El estado fundamental como solución óptima

El **estado fundamental** (energía mínima) del Hamiltoniano de Ising es precisamente la solución óptima del problema QUBO. Esto justifica el enfoque de annealing: si el proceso de annealing termina en el estado de menor energía, hemos resuelto el problema de optimización.

### 2.4 Complejidad: por qué es NP-hard en general

Encontrar el estado fundamental de un Hamiltoniano de Ising en un grafo general es un problema NP-hard (Barahona, 1982). Esto implica que no se conoce algoritmo clásico o cuántico eficiente (en tiempo polinomial) para todos los casos. Sin embargo:

- Para grafos planares, es polinomial clásicamente
- Para instancias industriales específicas, los heurísticos (incluyendo D-Wave) dan buenas soluciones en tiempo razonable
- D-Wave puede encontrar buenas soluciones (no necesariamente globalmente óptimas) en microsegundos para instancias de miles de variables

---

## 3. Mapeo de Problemas Combinatorios a QUBO {#3-mapeo}

### 3.1 MAX-CUT → QUBO

El problema MAX-CUT: dado un grafo $G = (V, E)$ con pesos $w_{ij}$, particionarlo en dos conjuntos $S$ y $\bar{S}$ maximizando el peso de las aristas que cruzan el corte.

La variable binaria $x_i \in \{0, 1\}$ indica en qué partición está el nodo $i$. El número de aristas cortadas entre nodos $i$ y $j$ es $x_i(1-x_j) + x_j(1-x_i) = x_i + x_j - 2x_ix_j$.

Maximizar el peso del corte equivale a **minimizar** (cambiando signo):

$$
E_{\text{MAX-CUT}}(\mathbf{x}) = -\sum_{(i,j)\in E} w_{ij}(x_i + x_j - 2x_ix_j)
$$

La matriz QUBO tiene:
- Diagonal: $Q_{ii} = -\sum_{j:(i,j)\in E} w_{ij}$ (sumando sobre los vecinos de $i$)
- Fuera de diagonal: $Q_{ij} = 2w_{ij}$ para aristas $(i,j) \in E$, 0 en otro caso

### 3.2 TSP → QUBO

El Problema del Viajante (TSP): dado un grafo completo con $n$ ciudades y distancias $d_{ij}$, encontrar el ciclo hamiltoniano de menor coste.

Se necesitan variables binarias $x_{i,t} \in \{0, 1\}$ donde $x_{i,t} = 1$ significa "el viajante visita la ciudad $i$ en el tiempo $t$".

El QUBO del TSP combina el objetivo con las restricciones de permutación como penalizaciones:

$$
E_{\text{TSP}} = A \cdot C_1 + A \cdot C_2 + B \cdot C_3
$$

donde:
- $C_1 = \sum_{t}\left(1 - \sum_i x_{i,t}\right)^2$ — cada tiempo tiene exactamente una ciudad
- $C_2 = \sum_{i}\left(1 - \sum_t x_{i,t}\right)^2$ — cada ciudad se visita exactamente una vez
- $C_3 = \sum_{t}\sum_{i \neq j} d_{ij} x_{i,t} x_{j,t+1}$ — minimizar distancia total del tour

Los coeficientes $A$ (penalización) y $B$ (peso objetivo) deben satisfacer $A \gg B \cdot d_{\max}$ para garantizar que las soluciones factibles sean más baratas que las infactibles.

El TSP con $n$ ciudades requiere $n^2$ variables binarias, haciendo el QUBO de tamaño $n^2 \times n^2$.

### 3.3 Coloración de grafos → QUBO

Para colorear un grafo $G = (V, E)$ con $k$ colores sin que dos nodos adyacentes tengan el mismo color:

Variables $x_{i,c} = 1$ si el nodo $i$ tiene color $c$. El QUBO es:

$$
E_{\text{color}} = A\sum_i \left(1 - \sum_c x_{i,c}\right)^2 + A\sum_{(i,j)\in E}\sum_c x_{i,c} x_{j,c}
$$

- Primer término: cada nodo tiene exactamente un color
- Segundo término: nodos adyacentes no tienen el mismo color

### 3.4 Portfolio Markowitz → QUBO

El modelo de Markowitz selecciona activos para maximizar retorno y minimizar riesgo. Con variables binarias $x_i \in \{0,1\}$ indicando si el activo $i$ está en el portfolio:

$$
E_{\text{portfolio}} = q \mathbf{x}^T \Sigma \mathbf{x} - (1-q) \boldsymbol{\mu}^T \mathbf{x} + \lambda \left(\sum_i x_i - B\right)^2
$$

donde:
- $\Sigma$ es la matriz de covarianza de retornos (riesgo)
- $\boldsymbol{\mu}$ es el vector de retornos esperados
- $q \in [0,1]$ controla el balance riesgo-retorno
- $B$ es el presupuesto (número de activos a seleccionar)
- $\lambda$ es el multiplicador de penalización de restricción de presupuesto

La matriz QUBO resultante es $Q = q\Sigma + \lambda \mathbf{1}\mathbf{1}^T$ con ajuste diagonal, y el vector lineal absorbe $-(1-q)\boldsymbol{\mu}$ y $-2\lambda B \mathbf{1}$.

---

## 4. D-Wave Advantage — Arquitectura Pegasus {#4-dwave}

### 4.1 Topología Pegasus

**Pegasus** es la topología de conectividad del procesador D-Wave Advantage (lanzado en 2020). Sus características principales:

- **5000+ qubits físicos** (Advantage 4.1: 5627 qubits)
- **Conectividad $k=15$**: cada qubit está conectado a hasta 15 vecinos
- Organización en una estructura tridimensional de células hexagonales
- Coupler density: ~40000 couplers activos

Comparado con la arquitectura Chimera anterior (D-Wave 2000Q):
| Característica | Chimera | Pegasus |
|----------------|---------|---------|
| Qubits | 2048 | 5627 |
| Conectividad | k=6 | k=15 |
| Couplers | ~5600 | ~40000 |
| Ratio qubits lógicos/físicos | 1:6 | 1:3 (aprox.) |

### 4.2 Embedding de grafos arbitrarios en Pegasus

El problema fundamental del annealing con hardware: el grafo del problema QUBO puede no ser un subgrafo de Pegasus. Cuando dos variables necesitan interactuar pero sus qubits físicos no son vecinos, se usa **minor embedding**: se representa una variable lógica mediante una **cadena** de qubits físicos fuertemente acoplados.

```
Variable lógica A ──── Variable lógica B
Qubit físico A₁─A₂─A₃      B₁─B₂
            (cadena A)   (cadena B)
            coupler fuerte A₃-B₁
```

El embedding se resuelve con el algoritmo `minorminer` de D-Wave. Una cadena de $k$ qubits físicos representa una variable lógica, con couplers de cadena muy negativos (fortenemnte ferromagnéticos) para forzar que todos los qubits de la cadena tengan el mismo valor.

El coste del embedding: problemas completamente conectados ($K_n$) en Pegasus requieren $O(n^{1.5})$ qubits físicos para representar $n$ variables lógicas.

### 4.3 D-Wave Leap Cloud

**D-Wave Leap** (leap.dwavesys.com) ofrece acceso cloud a los procesadores D-Wave:

- **Plan gratuito**: 1 minuto/mes de tiempo en QPU (suficiente para cientos de problemas pequeños)
- **Plan comercial**: acceso ilimitado con pago por uso
- **Hybrid solvers**: para problemas grandes, D-Wave ofrece solvers híbridos clásico-cuántico (Kerberos, Leap Hybrid CQM/BQM) que escalan a millones de variables

### 4.4 Hybrid Solvers: CQM y BQM

D-Wave ofrece dos tipos de hybrid solvers que combinan QPU con heurísticas clásicas:

- **BQM Solver** (Binary Quadratic Model): para problemas QUBO directos, hasta $10^6$ variables
- **CQM Solver** (Constrained Quadratic Model): acepta restricciones explícitas (igualdad, desigualdad), las descompone internamente en QUBO con penalizaciones automáticas

```python
from dwave.system import LeapHybridCQMSampler
import dimod

# Problema con restricciones explícitas
cqm = dimod.ConstrainedQuadraticModel()
# Añadir variables, objetivo y restricciones
# ...
sampler = LeapHybridCQMSampler()
result = sampler.sample_cqm(cqm, time_limit=5)
```

---

## 5. dimod — Librería D-Wave para Python {#5-dimod}

### 5.1 Instalación

```bash
pip install dimod dwave-ocean-sdk
```

La librería `dimod` es la base del ecosistema D-Wave: permite definir modelos QUBO/BQM y ejecutarlos en simuladores locales o en hardware real.

### 5.2 BinaryQuadraticModel

```python
import dimod

# Crear un BQM para el problema MAX-CUT
# Grafo: 0-1-2-3 en ciclo
bqm = dimod.BinaryQuadraticModel(vartype='BINARY')

# Variables binarias implícitas al añadir interacciones
# Añadir interacciones (aristas del grafo con peso 1)
edges = [(0,1,1.0), (1,2,1.0), (2,3,1.0), (3,0,1.0)]
for u, v, w in edges:
    # Para MAX-CUT: Q_ii = -w (vecinos), Q_ij = 2*w
    bqm.add_quadratic(u, v, 2*w)   # Q_ij = 2*w

# Añadir términos lineales
for node in [0, 1, 2, 3]:
    degree = 2  # cada nodo tiene grado 2 en el ciclo
    bqm.add_linear(node, -degree * 1.0)  # Q_ii = -suma de pesos vecinos

print(f"Variables: {list(bqm.variables)}")
print(f"Número de variables: {len(bqm.variables)}")
print(f"Número de interacciones: {len(bqm.quadratic)}")
```

### 5.3 ExactSolver — simulador exacto para problemas pequeños

```python
from dimod import ExactSolver

sampler = ExactSolver()
response = sampler.sample(bqm)

# Mostrar las mejores soluciones
print("Top 5 soluciones:")
for sample, energy, *_ in response.data(['sample', 'energy']):
    print(f"  {sample} → energía = {energy:.2f}")
```

El `ExactSolver` evalúa los $2^n$ estados posibles, por lo que solo es viable para $n \leq 20$ variables aproximadamente.

### 5.4 SteepestDescentSolver — heurístico local

```python
from dwave.samplers import SteepestDescentSolver

sampler_sd = SteepestDescentSolver()
response_sd = sampler_sd.sample(bqm, num_reads=100)

best_sample = response_sd.first.sample
best_energy = response_sd.first.energy
print(f"Mejor solución encontrada: {best_sample}")
print(f"Energía: {best_energy:.2f}")
```

### 5.5 Ejecutar en hardware D-Wave real

```python
from dwave.system import DWaveSampler, EmbeddingComposite

# DWaveSampler requiere token de Leap en variable de entorno
# export DWAVE_API_TOKEN=tu_token

sampler_hw = EmbeddingComposite(DWaveSampler())
response_hw = sampler_hw.sample(bqm,
                                num_reads=1000,
                                annealing_time=20)  # microsegundos

print(f"Mejor energía en QPU: {response_hw.first.energy:.2f}")
print(f"Solución: {response_hw.first.sample}")

# Información sobre el embedding
print(f"Cadenas físicas usadas: {response_hw.info}")
```

### 5.6 Comparativa de solvers

| Solver | Tipo | n_vars máx. | Tiempo | Optimal garantizado |
|--------|------|-------------|--------|---------------------|
| `ExactSolver` | Clásico, exacto | ~20 | Exponencial | Sí |
| `SteepestDescentSolver` | Clásico, heurístico | 10^5 | Rápido | No |
| `SimulatedAnnealingSampler` | Clásico, SA | 10^5 | Medio | No |
| `DWaveSampler` | QPU real | ~5000 lógicos | µs (+ latencia cloud) | No |
| `LeapHybridBQMSampler` | Híbrido | 10^6 | Segundos | No |

---

## 6. Comparativa D-Wave vs QAOA {#6-comparativa}

### 6.1 Mismo problema, distintos enfoques

Para el problema MAX-CUT en un grafo de 4 nodos como ejemplo comparativo:

**Con D-Wave (annealing)**:
```python
import dimod
from dwave.samplers import SimulatedAnnealingSampler

bqm = dimod.BinaryQuadraticModel(vartype='BINARY')
# Grafo 4 nodos: 0-1, 1-2, 2-3, 3-0, 0-2 (grafo K4 completo)
edges = [(0,1,1),(1,2,1),(2,3,1),(3,0,1),(0,2,1),(1,3,1)]
for u, v, w in edges:
    bqm.add_quadratic(u, v, 2*w)
for node in range(4):
    bqm.add_linear(node, -3.0)  # grado 3

sampler = SimulatedAnnealingSampler()
result = sampler.sample(bqm, num_reads=100)
print(result.first.sample, result.first.energy)
```

**Con QAOA (gate model)**:
```python
from qiskit_aer import AerSimulator
from qiskit.circuit.library import QAOAAnsatz
from qiskit.quantum_info import SparsePauliOp

# Operador de coste para MAX-CUT
# C = sum_{(i,j) en E} (1 - Z_i Z_j) / 2
cost_op = SparsePauliOp.from_list([
    ("ZZII", -0.5), ("IZZI", -0.5), ("IIZZ", -0.5),
    ("ZIZI", -0.5), ("ZIIZ", -0.5), ("IZIZ", -0.5)
])

ansatz = QAOAAnsatz(cost_op, reps=2)
# Optimizar con VQE/QAOA...
```

### 6.2 Cuándo usar cada uno

| Criterio | D-Wave | QAOA |
|---------|--------|------|
| Tamaño del problema | Grande (miles de vars) | Pequeño-mediano (decenas) |
| Densidad del grafo | Alta conectividad | Moderada |
| Tipo de problema | Solo QUBO/Ising | Cualquier problema cuántico |
| Hardware disponible | D-Wave Leap (gratuito parcial) | IBM Quantum, simuladores |
| Tiempo de respuesta | µs (+ ~50ms latencia cloud) | Segundos-minutos |
| Calidad de solución | Buena heurística | Depende de profundidad |

En general, para instancias de optimización grandes y densas, D-Wave supera a QAOA en la práctica actual. QAOA es más interesante como algoritmo universal con perspectivas de ventaja en hardware tolerante a fallos.

### 6.3 Benchmark en MAX-CUT

Experimentos comparativos (2022–2024) en grafos aleatorios de $n=50$–$200$ nodos muestran:

- **D-Wave Advantage**: soluciones dentro del 1–3% del óptimo en <1 ms de QPU
- **QAOA p=3** (3 capas): soluciones dentro del 5–10% del óptimo, decenas de segundos
- **Simulated Annealing clásico**: comparable a D-Wave para $n<100$, inferior para $n>500$
- **Gurobi (solver exacto clásico)**: óptimo garantizado para $n<1000$ en minutos

---

## 7. Otras Plataformas de Annealing 2025 {#7-plataformas}

### 7.1 Panorama actual

Además de D-Wave, varias empresas han desarrollado **digital annealers** y otros aceleradores para QUBO:

| Plataforma | Empresa | Tipo | Qubits/bits | Conectividad | Acceso |
|-----------|---------|------|-------------|--------------|--------|
| D-Wave Advantage 4.1 | D-Wave | Annealing cuántico | 5627 qubits | Pegasus (~k=15) | Cloud (Leap) |
| Fujitsu DAU 3.0 | Fujitsu | Digital annealer (CMOS) | 100,000+ bits | All-to-all | Cloud enterprise |
| Toshiba SQBM+ | Toshiba | Simulated bifurcation | 100,000+ bits | All-to-all | Cloud enterprise |
| Hitachi CMOS Annealer | Hitachi | CMOS annealer | 102,400 bits | 4-body | Cloud/on-premise |
| D-Wave Advantage2 | D-Wave | Annealing cuántico | ~7000 qubits | Zephyr (k=20) | En desarrollo (2025) |

### 7.2 Fujitsu Digital Annealer (DAU)

El **DAU 3.0** de Fujitsu no usa qubits cuánticos sino transistores CMOS especializados. Sin embargo, implementa un algoritmo de Monte Carlo paralelo masivo con fluctuaciones análogas al annealing cuántico:

- Conectividad all-to-all hasta 100.000 bits: ventaja clave sobre D-Wave (sin problema de embedding)
- Temperatura efectiva programable y schedule de annealing configurable
- Disponible en Fujitsu Cloud (Japón, Europa, América)
- API compatible con dimod a través de adaptadores

### 7.3 Toshiba Simulated Quantum Bifurcation Machine (SQBM+)

SQBM+ implementa el algoritmo de **bifurcación cuántica simulada** (Goto et al., 2019): simulación clásica en GPU de un oscilador no-lineal que exhibe comportamiento análogo al tunneling cuántico. Características:

- Escalado favorable: $O(n^2)$ operaciones por step, paralelizable en GPU
- Hasta 100.000 variables con conectividad full
- Benchmark competitivo con D-Wave en problemas densos de gran escala

### 7.4 Hitachi CMOS Annealer

Desarrollado en Hitachi Cambridge Laboratory, usa circuitos CMOS a baja temperatura que implementan un modelo de Ising estocástico. Disponible como hardware on-premise para aplicaciones industriales en manufactura y logística.

### 7.5 Cuándo elegir qué plataforma

- **D-Wave**: mejor opción para investigación y acceso rápido (Leap gratuito), conectividad cuántica real
- **Fujitsu DAU**: all-to-all sin embedding, mejor para problemas completamente conectados (portfolio, diseño industrial)
- **Toshiba SQBM+**: muy rápido en GPU para problemas grandes y densos, buena API Python
- **Annealing clásico (simulated annealing)**: gratuito, escalable, punto de referencia imprescindible

---

## 8. Ejercicios {#8-ejercicios}

### Ejercicio 1: MAX-CUT de 4 nodos manualmente

Dado el grafo con 4 nodos y aristas $E = \{(0,1), (1,2), (2,3), (3,0)\}$ (ciclo de 4 nodos) con todos los pesos $w_{ij} = 1$:

1. Construye la matriz QUBO $Q$ de $4\times 4$ a mano
2. Enumera los 16 estados posibles $\mathbf{x} \in \{0,1\}^4$ y calcula $E(\mathbf{x}) = \mathbf{x}^T Q \mathbf{x}$ para cada uno
3. Identifica las dos soluciones óptimas (el ciclo tiene simetría)
4. Verifica con `ExactSolver` de dimod que obtienes el mismo resultado

```python
import dimod
import numpy as np

# Tu código aquí
# Construir Q manualmente y con dimod
Q_manual = np.array([...])  # 4x4
bqm = dimod.BinaryQuadraticModel(vartype='BINARY')
# ...
sampler = dimod.ExactSolver()
result = sampler.sample(bqm)
```

**Pregunta**: ¿Cuántas aristas tiene el corte óptimo? ¿Es el máximo posible para este grafo?

### Ejercicio 2: TSP de 3 ciudades con QUBO

Construye y resuelve el TSP con 3 ciudades y las siguientes distancias:
- $d(A,B) = 2$, $d(B,C) = 3$, $d(A,C) = 4$

1. Define las 9 variables binarias $x_{i,t}$ (ciudad $i \in \{A,B,C\}$, tiempo $t \in \{0,1,2\}$)
2. Escribe la matriz QUBO incluyendo las penalizaciones $C_1$, $C_2$ y el objetivo $C_3$ con $A=10$, $B=1$
3. Identifica la solución óptima a mano (hay 2 tours distintos: $A→B→C→A$ y $A→C→B→A$)
4. Resuelve con `SimulatedAnnealingSampler` con 1000 lecturas y comprueba si encuentra el óptimo

```python
from dwave.samplers import SimulatedAnnealingSampler
import dimod

# Las ciudades son 0=A, 1=B, 2=C
# Las variables son x_{ciudad}_{tiempo}
# Nombrar como: '0_0', '0_1', ... '2_2'

bqm = dimod.BinaryQuadraticModel(vartype='BINARY')
# Tu código aquí
```

### Ejercicio 3: Portfolio de 5 activos

Tienes 5 activos con retornos esperados anualizados y la siguiente matriz de covarianza simplificada:

```python
import numpy as np

retornos = np.array([0.12, 0.18, 0.08, 0.15, 0.10])  # 12%, 18%, 8%, 15%, 10%
covarianza = np.array([
    [0.04, 0.01, 0.00, 0.02, 0.01],
    [0.01, 0.09, 0.01, 0.02, 0.00],
    [0.00, 0.01, 0.02, 0.00, 0.01],
    [0.02, 0.02, 0.00, 0.06, 0.01],
    [0.01, 0.00, 0.01, 0.01, 0.03]
])
presupuesto = 2  # seleccionar exactamente 2 activos
q_risk = 0.5    # balance riesgo-retorno
penalizacion = 5.0  # lambda
```

1. Construye el QUBO del portfolio de Markowitz
2. Encuentra la solución óptima con `ExactSolver` (solo hay $\binom{5}{2}=10$ soluciones factibles)
3. Calcula el retorno esperado y la varianza del portfolio óptimo
4. Repite con $q=0$ (solo maximizar retorno) y $q=1$ (solo minimizar riesgo). ¿Cuáles son los portfolios resultantes?

### Ejercicio 4: Comparativa de solvers

Para el problema MAX-CUT en un grafo aleatorio de Erdős–Rényi con $n=20$ nodos y probabilidad de arista $p=0.5$:

1. Genera el grafo y construye el BQM correspondiente
2. Resuelve con `ExactSolver` para obtener el óptimo exacto
3. Resuelve con `SimulatedAnnealingSampler` con 100, 1000 y 10000 lecturas
4. Mide el tiempo de ejecución de cada solver
5. Crea una tabla comparativa: energía obtenida, gap relativo respecto al óptimo, tiempo

```python
import networkx as nx
import dimod
from dwave.samplers import SimulatedAnnealingSampler
import time

# Generar grafo aleatorio
G = nx.erdos_renyi_graph(20, 0.5, seed=42)

# Construir BQM para MAX-CUT
bqm = dimod.BinaryQuadraticModel(vartype='BINARY')
for u, v in G.edges():
    w = 1.0
    bqm.add_quadratic(u, v, 2*w)
for node in G.nodes():
    bqm.add_linear(node, -G.degree(node) * 1.0)

# Tu código de comparativa aquí
```

---

## 9. Referencias {#9-referencias}

1. **Farhi, E., Goldstone, J., Gutmann, S., Sipser, M.** (2000). *Quantum Computation by Adiabatic Evolution*. arXiv:quant-ph/0001106. — Fundamento teórico del quantum annealing adiabático.

2. **D-Wave Systems Documentation** (2024). *D-Wave System Documentation*. https://docs.dwavesys.com/ — Documentación oficial de D-Wave Advantage, Pegasus, y Ocean SDK.

3. **Glover, F., Kochenberger, G., Du, Y.** (2018). *Quantum Bridge Analytics I: A Tutorial on Formulating and Using QUBO Models*. 4OR-Q J Oper Res, 17:335-371. — Tutorial exhaustivo sobre formulación de problemas como QUBO.

4. **Hauke, P., Katzgraber, H.G., Lechner, W., Nishimori, H., Oliver, W.D.** (2020). *Perspectives of Quantum Annealing: Methods and Implementations*. Reports on Progress in Physics, 83(5):054401. — Revisión comprehensiva del estado del arte del annealing cuántico.

5. **Barahona, F.** (1982). *On the Computational Complexity of Ising Spin Glass Models*. J. Phys. A: Math. Gen., 15:3241-3253. — Prueba de NP-hardness del modelo de Ising.

6. **Goto, H., Tatsumura, K., Dixon, A.R.** (2019). *Combinatorial Optimization by Simulating Adiabatic Bifurcations in Nonlinear Hamiltonian Systems*. Science Advances, 5(4):eaav2372. — Base del algoritmo SQBM+ de Toshiba.

7. **Lucas, A.** (2014). *Ising Formulations of Many NP Problems*. Frontiers in Physics, 2:5. — Referencia esencial para mapear problemas clásicos a Ising/QUBO.

8. **Yarkoni, S., Raponi, E., Bäck, T., Schmitt, S.** (2022). *Quantum Annealing for Industry Applications: Introduction and Review*. Reports on Progress in Physics, 85:104001. — Revisión de aplicaciones industriales de D-Wave.

---

*Módulo 49 | ComputacionCuantica | Nivel: Avanzado | Prerrequisitos: Módulos 11 (algoritmos variacionales), 35 (computación adiabática), optimización combinatoria básica*
