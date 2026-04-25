# Logística y combinatoria: TSP cuántico, scheduling y comparativa con heurísticas

**Módulo 30 · Artículo 3 · Nivel avanzado**

---

## El problema del viajante (TSP)

El Travelling Salesman Problem es el problema de optimización combinatoria paradigmático:
dado un grafo completo de n ciudades con pesos, encontrar el ciclo hamiltoniano de mínimo coste.

- **Complejidad clásica:** NP-hard. Mejor algoritmo exacto: O(n² · 2ⁿ) (Held-Karp).
- **Mejor heurística clásica:** Lin-Kernighan (LKH), soluciones ~0.5% del óptimo en minutos para n ~ 10.000.

### Formulación QUBO del TSP

Para n ciudades con variables x_{i,t} = 1 si la ciudad i se visita en el paso t:

$$H_{TSP} = A \sum_t \left(1 - \sum_i x_{i,t}\right)^2
           + A \sum_i \left(1 - \sum_t x_{i,t}\right)^2
           + B \sum_{i,j,t} W_{ij} x_{i,t} x_{j,t+1}$$

El primer término asegura que cada paso t tiene una ciudad; el segundo que cada ciudad
se visita exactamente una vez; el tercero minimiza la distancia total.

**Número de qubits:** n² qubits para representar las n² variables binarias.

```python
import numpy as np

def tsp_qubo(distancias: np.ndarray, A: float = 10.0, B: float = 1.0) -> np.ndarray:
    """
    Construye la matriz QUBO para TSP.
    distancias: matriz n×n de distancias entre ciudades.
    """
    n = len(distancias)
    N = n * n   # número total de variables binarias x_{i,t}

    Q = np.zeros((N, N))

    def idx(i, t):
        return i * n + t

    # Restricción 1: exactamente una ciudad por paso
    for t in range(n):
        for i in range(n):
            Q[idx(i,t), idx(i,t)] -= A
            for j in range(i+1, n):
                Q[idx(i,t), idx(j,t)] += 2*A

    # Restricción 2: cada ciudad visitada exactamente una vez
    for i in range(n):
        for t in range(n):
            Q[idx(i,t), idx(i,t)] -= A
            for s in range(t+1, n):
                Q[idx(i,t), idx(i,s)] += 2*A

    # Función de coste: minimizar distancia total
    for i in range(n):
        for j in range(n):
            if i != j:
                for t in range(n):
                    t_next = (t + 1) % n
                    Q[idx(i,t), idx(j,t_next)] += B * distancias[i,j]

    return Q

# Ejemplo pequeño: 4 ciudades en cuadrado
n_ciudades = 4
dist = np.array([
    [0, 1, np.sqrt(2), 1],
    [1, 0, 1, np.sqrt(2)],
    [np.sqrt(2), 1, 0, 1],
    [1, np.sqrt(2), 1, 0],
])

Q_tsp = tsp_qubo(dist)
print(f"QUBO TSP ({n_ciudades} ciudades): {n_ciudades**2} qubits, {n_ciudades**4} términos")
print(f"Solución óptima: ciclo de longitud {4:.3f} (cuadrado unitario)")
```

---

## QUBO a escala: ¿cuántos qubits se necesitan para TSP real?

| Ciudades | Qubits QUBO | Mejores heurísticas clásicas | Ventaja cuántica esperada |
|---|---|---|---|
| 10 | 100 | Óptimo exacto en ms | Ninguna |
| 100 | 10.000 | Heurísticas ~1% óptimo | Ninguna con NISQ |
| 1.000 | 10⁶ | LKH: ~0.5% en minutos | Posible con FT, ~2035 |
| 10.000 | 10⁸ | LKH: escala bien | Sin ventaja conocida |

**Problema fundamental:** Las heurísticas clásicas para TSP son extraordinariamente buenas.
LKH-3 resuelve instancias de 10⁶ ciudades con <0.1% del óptimo. La ventaja cuántica
solo es concebible si hay estructura específica no explotable clásicamente.

---

## Job-Shop Scheduling: caso más prometedor

El Job-Shop Scheduling Problem (JSP) tiene peor performance de heurísticas clásicas
que TSP. Asignar n trabajos a m máquinas minimizando el makespan es NP-hard y
los mejores métodos clásicos solo escalan hasta n,m ~ 100.

### Formulación QUBO para scheduling

```python
def scheduling_qubo_simple(n_jobs: int, n_machines: int,
                           tiempos: np.ndarray) -> np.ndarray:
    """
    QUBO simplificado para asignación de trabajos a máquinas.
    tiempos: matriz n_jobs × n_machines de tiempos de ejecución.
    Minimiza el makespan (tiempo total de la máquina más cargada).
    """
    N = n_jobs * n_machines  # x_{j,m} = 1 si trabajo j va a máquina m
    A = 5.0   # penalización de restricciones
    Q = np.zeros((N, N))

    def idx(j, m):
        return j * n_machines + m

    # Cada trabajo a exactamente una máquina
    for j in range(n_jobs):
        for m in range(n_machines):
            Q[idx(j,m), idx(j,m)] -= A
            for m2 in range(m+1, n_machines):
                Q[idx(j,m), idx(j,m2)] += 2*A

    # Penalizar desequilibrio de carga (proxy del makespan)
    for m in range(n_machines):
        for j1 in range(n_jobs):
            for j2 in range(j1+1, n_jobs):
                Q[idx(j1,m), idx(j2,m)] += tiempos[j1,m] * tiempos[j2,m] * 0.1

    return Q

# Ejemplo: 6 trabajos, 3 máquinas
n_j, n_m = 6, 3
tiempos_ej = np.random.randint(1, 10, (n_j, n_m))
Q_sched = scheduling_qubo_simple(n_j, n_m, tiempos_ej)
print(f"QUBO Scheduling ({n_j} trabajos, {n_m} máquinas): {n_j*n_m} qubits")
```

---

## Quantum Annealing vs. Gate-Based Quantum Computing

Para problemas combinatorios QUBO, existen dos paradigmas cuánticos:

### D-Wave (Quantum Annealing)

- **Ventaja:** procesadores con 5000+ qubits, directamente aplicables a QUBO.
- **Limitación:** qubits con conectividad limitada requieren embedding de grafos
  densos con overhead de 5-15× en número de qubits físicos.
- **Performance real:** comparable a SA (Simulated Annealing) clásico para la mayoría de instancias.

### QAOA Gate-Based

- **Ventaja teórica:** garantías de aproximación con hardware universal.
- **Limitación actual:** profundidad de circuito demasiado alta para hardware NISQ.

### Comparativa empírica (2024)

```python
# Resultado de benchmarks publicados (McGeoch & Wang 2023, Shaydulin 2023)
resultados_benchmark = {
    "Simulated Annealing (clásico)": {"calidad": 99.8, "tiempo_ms": 100},
    "D-Wave Advantage (QA)": {"calidad": 99.5, "tiempo_ms": 0.5},
    "QAOA p=3 (IBM 127q, NISQ)": {"calidad": 85.0, "tiempo_ms": 50},
    "Gurobi (clásico exacto)": {"calidad": 100.0, "tiempo_ms": 10000},
}

print("Comparativa en instancias QUBO de n=50 variables:")
print(f"{'Método':<40} {'Calidad (%)':>12} {'Tiempo (ms)':>12}")
print("-" * 66)
for metodo, datos in resultados_benchmark.items():
    print(f"{metodo:<40} {datos['calidad']:>12.1f} {datos['tiempo_ms']:>12.1f}")
```

---

## Casos de uso con mayor potencial real

### 1. Optimización de rutas de entrega (VRP)

El Vehicle Routing Problem (VRP) con múltiples restricciones (ventanas temporales,
capacidad) es más duro que TSP. Para flotas de 50-100 vehículos y 1000-5000 puntos:

- Heurísticas clásicas (Google OR-Tools): buenas pero no óptimas.
- Ventaja cuántica: posible con ~500 qubits lógicos (horizonte ~2030).

### 2. Scheduling de logística de semiconductores

La fabricación de chips requiere planificar ~1000 trabajos en ~200 máquinas con
restricciones de secuencia complejas. Es uno de los casos donde las heurísticas
clásicas tienen peor performance relativa:

```python
# Estimación de recursos cuánticos para JSP en semiconductores
n_jobs_fab = 500
n_machines_fab = 100
n_qubits_qubo = n_jobs_fab * n_machines_fab  # 50.000 qubits lógicos

# Con código de superficie d=20, ε=1e-3:
qubits_fisicos = n_qubits_qubo * 2 * 20**2  # ~4×10^8 qubits físicos
print(f"Qubits QUBO: {n_qubits_qubo:,}")
print(f"Qubits físicos estimados (d=20): {qubits_fisicos:,.0e}")
print("Horizonte: 2040+")
```

---

## Honestidad sobre la ventaja cuántica en logística

A fecha de 2024-2025, la situación honesta es:

| Afirmación | Realidad |
|---|---|
| "QAOA resuelve TSP mejor que clásico" | Falso para hardware actual. Las heurísticas clásicas son mucho mejores |
| "D-Wave ya tiene ventaja cuántica en logistics" | No demostrado. SA clásico es comparable o mejor |
| "En 2030 habrá ventaja cuántica en rutas" | Posible pero requiere FT con ~10⁵ qubits |
| "La ventaja es cuadrática (√N mejora)" | Solo en simulación Monte Carlo, no en combinatoria |

**Recomendación práctica:** Invertir en preparación (formación, datos, APIs), no en
hardware cuántico específico. Los beneficios serán accesibles vía cloud cuando lleguen.

---

## Conclusión del módulo 30

La ventaja cuántica práctica en problemas reales de química, finanzas y logística
comparte un patrón común:

1. **Problemas NP-hard** donde las heurísticas clásicas son imperfectas → mayor oportunidad.
2. **Horizonte realista:** 2028-2035 dependiendo del caso, condicionado al hardware FT.
3. **Corto plazo (2025-2027):** el mayor valor práctico es la **aceleración Monte Carlo**
   (Quantum Amplitude Estimation) para simulación de riesgo y pricing, con circuitos
   más superficiales que las alternativas QAOA.

El campo evoluciona rápidamente. Mantenerse actualizado con los benchmarks publicados
es más valioso que confiar en afirmaciones especulativas de proveedores.
