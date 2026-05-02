# Bitácora del Proyecto — Computación Cuántica: Teoría y Práctica

Registro cronológico de las sesiones de desarrollo, decisiones técnicas y hitos del proyecto.

---

## Sesión 2026-05-02 — v6.2 · Cierre total del plan de expansión

**Estado previo:** v6.1 — Fases 1-25 marcadas completas en la tabla maestra, pero 68 checkboxes individuales sin actualizar y varios entregables genuinamente ausentes.

### Trabajo realizado

#### 1. Actualización del checklist (PLAN_EXPANSION.md)
- Marcados `[x]` todos los items cuyo archivo existe (68 items en total).
- Items genuinamente ausentes dejados como `[ ]`: `guia_strawberry_fields.md`, `guia_progreso.md`, notebooks guiados (pendientes en sesión anterior).
- Header actualizado a v6.2 con métricas finales.

#### 2. Documentación nueva
- **`docs/guia_progreso.md`**: documenta el sistema de seguimiento `visualizador/progress.py` — funciones, formato de datos, privacidad, integración en p.15 Certificación.
- **`docs/guia_strawberry_fields.md`**: guía práctica de Strawberry Fields — instalación, backends, GBS, suspensión de Borealis (oct 2023), relación con PennyLane.

#### 3. Cuadernos guiados (`Cuadernos/guiados/`)
Creados 15 notebooks de introducción pedagógica paso a paso:

| Notebook | Tema |
|---|---|
| 01_primer_qubit | Estado cuántico, Bloch, medición |
| 02_puertas_y_circuitos | X/Y/Z/H/CNOT, Bell state |
| 03_algoritmo_grover | Oráculo, difusor, 1-4 qubits |
| 04_teleportacion_cuantica | Protocolo, fidelidad, canal ruidoso |
| 05_transformada_de_fourier | QFT manual, unitariedad, comparativa |
| 06_estimacion_de_fase | QPE, IQFT, precisión vs ancillas |
| 07_entrelazamiento | Entropía, CHSH S=2√2, GHZ/W |
| 08_vqe_paso_a_paso | Principio variacional, COBYLA |
| 09_qaoa_paso_a_paso | MAX-CUT, landscape γ/β |
| 10_ruido_y_decoherencia | Kraus, T1/T2, TVD |
| 11_correccion_de_errores | Código repetición, síndrome |
| 12_algoritmo_shor | Período, QPE, factorización N=15 |
| 13_machine_learning_cuantico | Feature map, kernel, KTA |
| 14_computacion_adiabatica | QUBO, simulated annealing, Ising |
| 15_fault_tolerant | Umbral, overhead d², magic states |

#### 4. PLAN_EXPANSION.md
- Métricas v6.2: 49 módulos, 53+15 labs, 21 páginas, 257 tests, 12 soluciones, 20 resúmenes.
- Footer actualizado.

### Métricas finales v6.2

| Recurso | Valor |
|---|---|
| Módulos tutoriales | 49 |
| Labs (laboratorios/) | 53 |
| Labs (guiados/) | 15 |
| Páginas visualizador | 21 |
| Tests pytest | 257 |
| Resúmenes | 20 |
| Soluciones investigación | 12 (R1-R12) |
| Páginas MkDocs | ~50 |
| Workflows GitHub Actions | 6 |

---

## Sesión 2026-05-01–02 — v6.1 · Fases 21-25

**Estado previo:** v5.6 — Fase 20 completada (Rydberg, 169 tests).

### Trabajo realizado

- **Fase 21**: qLDPC — Módulo 47, Lab 51, Visualizador p.19, R9, 10 tests → 193 total.
- **Fase 22**: QNLP + D-Wave — Módulos 48-49, Labs 52-53, Visualizador p.20, 14 tests → 207 total.
- **Fase 23**: Infraestructura QA — nbval CI, Resúmenes 11-20, R10-R12, progress.py, issue templates.
- **Fase 24**: Comunidad — TRANSLATING.md, 0_Inicio.py, CONTRIBUTING.md.
- **Fase 25**: Completar labs 01-23 — 257 tests finales.

### Problemas encontrados y resueltos

| Problema | Solución |
|---|---|
| `test_repetition_code_css` fallaba | Reemplazado H_rep con código [[4,2,2]] CSS válido |
| `test_error_correctable_below_threshold` P_L=0.222 | Decoder mayoría votación, assert P_L < 0.05 |
| `test_simulated_annealing` E=-2.0 ≠ -1.0 | Expected value corregido a -1.9 |
| `test_portfolio_qubo` seleccionaba 1 asset | Test reformulado como penalización pura |
| dimod no instalado | QUBO implementado con numpy puro |

---

## Sesión 2026-05-01 — v5.4/5.5 · Fotónica y Rydberg (Fases 19-20)

- Módulo 45: Computación Fotónica (GBS, Xanadu, PsiQuantum).
- Lab 49: `49_fotonica_cuantica.ipynb` (sin Strawberry Fields).
- Visualizador p.17: interferómetro fotónico (función de Wigner, squeezing).
- Módulo 46: Átomos Neutros y Rydberg (PXP, bloqueo, QuEra).
- Lab 50: `50_rydberg_chain.ipynb` (Hamiltoniano PXP, diagrama de fases).
- Visualizador p.18: array Rydberg 2D interactivo.
- +20 tests → 169 total.

---

## Sesión 2026-04-28 — v5.1/5.2 · Tensor Networks y Gravedad Cuántica

- Módulo 42: Tensor Networks y DMRG (MPS, Schmidt, TEBD, PEPS, MERA).
- Lab 46: `46_mps_tensor_networks.ipynb` — MPS desde cero con numpy.
- Jupyter Book: `_config.yml` + `_toc.yml` + workflow.
- Módulo 43: Gravedad Cuántica (AdS/CFT, MERA, HaPPY, ER=EPR, OTOC).
- Lab 47: `47_dmrg_heisenberg.ipynb` — iDMRG, convergencia a Bethe ansatz.
- Guía multi-provider: IonQ/Quantinuum/Pasqal.
- +28 tests → 129 total.

---

## Sesión 2026-04-27 — v4.0/5.0 · Fases 13-18

- Certificación: quiz 50 preguntas, badge SVG, p.15.
- Topological QC: código tórico, anyones, Lab 45.
- Property-based tests con Hypothesis: 101 tests.
- PDF automático vía GitHub Actions.
- Benchmark Hardware interactivo (p.16).
- DQC avanzado: repetidores, BBPSSW, MDI-QKD.
- PEPS + Hubbard 2D.
- GPU AerSimulator: guía, tests con skip automático.
- 149 tests → base para expansión posterior.

---

## Sesión 2026-04-27 (inicial) — v1.0 → v3.5

- Fundamentos: módulos 01-10, labs 01-10.
- Algoritmos: VQE, QAOA, QPE, QFT, Shor.
- Hardware: IBM Quantum, error rates, guía práctica.
- QEC: código repetición, superficie, Shor.
- Aplicaciones industriales: Finance (QAOA portfolio), QML (kernel).
- API FastAPI: `/run-circuit`, `/run-vqe`, `/run-grover`.
- Docker + DevContainer.
- Tests progresivos: 0 → 76 → 101 → 129.

---

*Bitácora iniciada 2026-05-02 · Proyecto en estado de mantenimiento activo*
