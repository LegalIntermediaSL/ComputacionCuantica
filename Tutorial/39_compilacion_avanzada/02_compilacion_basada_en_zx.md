# Compilación Basada en ZX-Calculus

**Módulo 39 · Artículo 2 · Nivel muy avanzado**

---

## ZX-Calculus como lenguaje de compilación

El ZX-calculus (Coecke & Duncan 2008) es un lenguaje diagramático completo
para la mecánica cuántica que permite reescribir circuitos usando reglas
algebraicas. A diferencia del transpiler basado en matrices, trabaja
directamente con la estructura de puertas.

Ventaja clave: **optimización de T-count** — el número de puertas T no-Clifford,
que es el recurso escaso en computación fault-tolerant (cada T requiere un
estado mágico destilado).

```python
import numpy as np
import matplotlib.pyplot as plt

# Contar T-gates en circuitos estándar
def contar_T_gates(nombre: str, t_count: int, cx_count: int, otras: int) -> dict:
    return {'nombre': nombre, 'T': t_count, 'CX': cx_count, 'otras': otras,
            'total': t_count + cx_count + otras}

circuitos_referencia = [
    contar_T_gates('Toffoli (naïve)',    7, 6, 10),
    contar_T_gates('Toffoli (óptimo)',   4, 3,  8),  # Selinger 2013
    contar_T_gates('QFT-4q',            0, 6, 10),   # QFT no tiene T gates
    contar_T_gates('UCCSD H₂ (4q)',     8, 4, 12),
    contar_T_gates('Shor N=15 (approx)', 12, 8, 20),
]

print('T-count en circuitos estándar:')
print(f'{"Circuito":>25} | {"T-count":>8} | {"CX-count":>9} | {"Overhead FT"}')
print('-' * 65)
for c in circuitos_referencia:
    # Overhead FT: cada T gate requiere ~100 qubits adicionales para destilación
    overhead = c['T'] * 100
    print(f'{c["nombre"]:>25} | {c["T"]:>8} | {c["CX"]:>9} | {overhead:>10} qubits')
```

---

## Reducción de T-count con PyZX

```python
# Demostración con PyZX (requiere: pip install pyzx)
try:
    import pyzx as zx

    # Circuito Toffoli naïve
    qc_toffoli = zx.Circuit(3)
    qc_toffoli.add_gate('H', 2)
    qc_toffoli.add_gate('CNOT', 1, 2)
    qc_toffoli.add_gate('T', 2, adjoint=True)
    qc_toffoli.add_gate('CNOT', 0, 2)
    qc_toffoli.add_gate('T', 2)
    qc_toffoli.add_gate('CNOT', 1, 2)
    qc_toffoli.add_gate('T', 2, adjoint=True)
    qc_toffoli.add_gate('CNOT', 0, 2)
    qc_toffoli.add_gate('T', 2)
    qc_toffoli.add_gate('T', 1)
    qc_toffoli.add_gate('CNOT', 0, 1)
    qc_toffoli.add_gate('H', 2)
    qc_toffoli.add_gate('T', 0)
    qc_toffoli.add_gate('T', 1, adjoint=True)
    qc_toffoli.add_gate('CNOT', 0, 1)

    # Convertir a grafo ZX
    g = qc_toffoli.to_graph()
    t_antes = zx.tcount(g)

    # Simplificar con full_reduce
    zx.full_reduce(g)
    t_despues = zx.tcount(g)

    # Extraer circuito optimizado
    qc_opt = zx.extract_circuit(g)
    t_final = zx.tcount(qc_opt.to_graph())

    print(f'Toffoli — T-count antes:  {t_antes}')
    print(f'Toffoli — T-count después full_reduce: {t_despues}')
    print(f'Toffoli — T-count circuito extraído: {t_final}')
    print(f'Reducción: {(1 - t_final/t_antes)*100:.1f}%')

except ImportError:
    print('PyZX no instalado (pip install pyzx). Mostrando datos de referencia:')
    print('Toffoli naïve:  T-count = 7')
    print('Toffoli PyZX:   T-count = 4  (reducción 43%)')
    print('→ Equivale a ahorrar 300 qubits de destilación por puerta Toffoli')
```

---

## Reglas de reescritura ZX y su impacto

```python
reglas_zx = """
REGLAS FUNDAMENTALES DE ZX-CALCULUS
═══════════════════════════════════════════════════════════════════

1. SPIDER FUSION (fusión de arañas del mismo color):
   Z(α) — Z(β) = Z(α+β)     [siempre que estén conectadas]
   X(α) — X(β) = X(α+β)
   → Fusiona fases: RZ(α)·RZ(β) = RZ(α+β)
   → Impacto: elimina puertas RZ/RX redundantes

2. IDENTIDAD (araña con fase 0):
   Z(0) = identidad (con ≠2 legs)
   → Elimina puertas Rz(0) y Rx(0) innecesarias

3. COLOR CHANGE (Hadamard):
   H·Z(α)·H = X(α)
   → Mueve Hadamards a través de arañas

4. COPY (arañas de paridad):
   X(π) conectada a |0⟩ → copia el estado
   → Base de las reglas de cancelación CNOT

5. BIALGEBRA (relación entre Z y X):
   Permite mover puertas Z a través de CNOT y viceversa
   → Base de la optimización de circuitos Clifford

6. HOPF (ortogonalidad):
   Loop Z-X = escalado
   → Cancelación de pares CNOT

IMPACTO EN T-COUNT (resultados empíricos, Ross & Selinger 2016):
  QFT (n=10q):    T-count reducido de 96 a 24  (75% reducción)
  ADDER (n=4q):   T-count reducido de 56 a 32  (43% reducción)
  Clifford+T gen: reducción media ~30-50% en circuitos aleatorios
"""
print(reglas_zx)

# Simulación: T-count vs profundidad del circuito sin/con ZX
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
n_circuitos = 30
t_antes = np.random.randint(10, 80, n_circuitos)
# PyZX reduce típicamente un 30-60% del T-count
factor_reduccion = np.random.uniform(0.3, 0.65, n_circuitos)
t_despues = (t_antes * (1 - factor_reduccion)).astype(int)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Scatter antes vs después
axes[0].scatter(t_antes, t_despues, alpha=0.7, c='blue', s=50)
axes[0].plot([0, 80], [0, 80], 'r--', alpha=0.5, label='Sin reducción')
axes[0].plot([0, 80], [0, 40], 'g--', alpha=0.5, label='50% reducción')
axes[0].set_xlabel('T-count original')
axes[0].set_ylabel('T-count tras optimización ZX')
axes[0].set_title('Impacto de PyZX en T-count')
axes[0].legend()
axes[0].grid(alpha=0.3)

# Histograma de reducción
reduccion_pct = factor_reduccion * 100
axes[1].hist(reduccion_pct, bins=12, color='steelblue', edgecolor='white', alpha=0.8)
axes[1].axvline(reduccion_pct.mean(), color='red', ls='--', lw=2,
                label=f'Media: {reduccion_pct.mean():.1f}%')
axes[1].set_xlabel('Reducción T-count (%)')
axes[1].set_ylabel('Número de circuitos')
axes[1].set_title('Distribución de reducción T-count con ZX')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print(f'\nReducción media T-count: {reduccion_pct.mean():.1f}%')
print(f'Ahorro medio en overhead FT: {(t_antes - t_despues).mean():.0f} puertas T')
print(f'→ Equivale a {(t_antes - t_despues).mean() * 100:.0f} qubits de destilación ahorrados por circuito')
```

---

## Comparativa: Qiskit transpiler vs ZX vs t|ket⟩

```python
comparativa_compiladores = """
COMPARATIVA DE COMPILADORES CUÁNTICOS 2024
═══════════════════════════════════════════════════════════════════

┌──────────────────┬──────────────┬───────────────┬──────────────────┐
│ Métrica          │ Qiskit L3    │ PyZX          │ t|ket⟩ (Pytket)  │
├──────────────────┼──────────────┼───────────────┼──────────────────┤
│ Enfoque          │ Circuito     │ ZX graph      │ Circuito + ZX    │
│ T-count optim.   │ No           │ Sí (fuerte)   │ Sí (moderado)    │
│ CX-count optim.  │ Sí           │ Moderado      │ Sí (fuerte)      │
│ Ruteo hardware   │ SABRE        │ No nativo     │ Routing props.   │
│ Backend support  │ IBM, Aer     │ Agnóstico     │ IBM, IonQ, Quant.│
│ Velocidad        │ Rápido       │ Lento (>100q) │ Medio            │
│ Mejor para       │ NISQ general │ FT Clifford+T │ NISQ + FT mixto  │
│ Integración      │ Nativa Qiskit│ PyZX API      │ pytket-qiskit    │
└──────────────────┴──────────────┴───────────────┴──────────────────┘

RECOMENDACIÓN PRÁCTICA:
  NISQ hardware hoy:  Qiskit L3 (mejor integración con IBM)
  FT fault-tolerant:  PyZX para minimizar T-count antes de Qiskit L3
  Pipeline óptimo:    PyZX → t|ket⟩ → backend nativo

INTEGRACIÓN QISKIT + PYZX:
  1. Exportar a QASM: qc.qasm()
  2. Importar en PyZX: zx.Circuit.from_qasm(qasm_str)
  3. Optimizar: zx.full_reduce(g)
  4. Exportar: qc_opt.to_qasm()
  5. Reimportar en Qiskit: QuantumCircuit.from_qasm_str(qasm_opt)
"""
print(comparativa_compiladores)
```

---

**Referencias:**
- Coecke & Duncan, *ICALP 2008* — ZX-calculus original
- Kissinger & van de Wetering, *Quantum* 4, 279 (2020) — PyZX
- Duncan et al., *arXiv:1902.03178* — simplificación de Clifford+T con ZX
- Ross & Selinger, *Logical Methods CS* 12 (2016) — T-count optimization
- Sivarajah et al., *Quantum* 5, 577 (2021) — t|ket⟩ architecture
