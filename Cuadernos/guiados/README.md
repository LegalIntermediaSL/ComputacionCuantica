# Cuadernos Guiados — Computación Cuántica

Esta carpeta contiene **15 notebooks de introducción guiada** que cubren los conceptos fundamentales de la computación cuántica con un enfoque paso a paso y altamente pedagógico.

## Diferencia con `laboratorios/`

| Criterio | `guiados/` | `laboratorios/` |
|---|---|---|
| Extensión | 8-10 celdas | 10-20 celdas |
| Enfoque | Conceptual, paso a paso | Implementación completa |
| Prerrequisitos | Mínimos (numpy/scipy) | Qiskit 2.x completo |
| Uso recomendado | Primera lectura | Práctica y profundización |
| Ejercicios | Incluidos en el notebook | Labs independientes |

## Índice de notebooks

| # | Archivo | Tema | Prerrequisitos |
|---|---|---|---|
| 01 | `01_primer_qubit.ipynb` | Estado cuántico, esfera de Bloch, medición | numpy |
| 02 | `02_puertas_y_circuitos.ipynb` | Puertas X/Y/Z/H/CNOT, estado de Bell | numpy, Qiskit |
| 03 | `03_algoritmo_grover.ipynb` | Oráculo, difusor, amplificación de amplitudes | Qiskit, AerSimulator |
| 04 | `04_teleportacion_cuantica.ipynb` | Protocolo completo, fidelidad, canal ruidoso | Qiskit |
| 05 | `05_transformada_de_fourier.ipynb` | QFT manual vs Qiskit, unitariedad | numpy, Qiskit |
| 06 | `06_estimacion_de_fase.ipynb` | QPE, IQFT, precisión vs ancillas | Qiskit, AerSimulator |
| 07 | `07_entrelazamiento.ipynb` | Entropía, CHSH, GHZ vs W | Qiskit |
| 08 | `08_vqe_paso_a_paso.ipynb` | Principio variacional, ansatz, COBYLA | numpy, scipy, Qiskit |
| 09 | `09_qaoa_paso_a_paso.ipynb` | MAX-CUT, landscape γ/β, optimización | numpy, scipy, Qiskit |
| 10 | `10_ruido_y_decoherencia.ipynb` | Kraus, bit-flip, depolarizante, T1/T2 | numpy |
| 11 | `11_correccion_de_errores.ipynb` | Código repetición, síndrome, tasa lógica | numpy, Qiskit |
| 12 | `12_algoritmo_shor.ipynb` | Período, QPE, factorización N=15 | numpy, Qiskit |
| 13 | `13_machine_learning_cuantico.ipynb` | Feature map, kernel cuántico, SVM, KTA | numpy, sklearn, Qiskit |
| 14 | `14_computacion_adiabatica.ipynb` | QUBO, MAX-CUT, simulated annealing, Ising | numpy |
| 15 | `15_fault_tolerant.ipynb` | Umbral, overhead surface code, magic states | numpy |

## Ruta de estudio recomendada

**Básico** (sin hardware): 01 → 02 → 10 → 11  
**Algoritmos** (con Qiskit): 03 → 04 → 05 → 06 → 07 → 12  
**Optimización**: 08 → 09 → 14  
**Avanzado**: 13 → 15

## Después de estos notebooks

Una vez completados, continúa con:
- `Cuadernos/laboratorios/` — implementaciones completas con más detalle
- `Tutorial/` — teoría matemática rigurosa
- `visualizador/` — exploración interactiva en Streamlit
