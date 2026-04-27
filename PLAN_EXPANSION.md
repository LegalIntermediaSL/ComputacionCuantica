# Plan de Expansión — Computación Cuántica: Teoría y Práctica

**Estado general:** v3.5 · 2026-04-27  
**Repositorio:** [LegalIntermediaSL/ComputacionCuantica](https://github.com/LegalIntermediaSL/ComputacionCuantica)

---

## Resumen ejecutivo

| Recurso | v1.0 | v2.0 | v2.5 | v3.0 | v3.5 | Objetivo v4.0 |
|---|---|---|---|---|---|---|
| Artículos tutoriales | 30 | 55 | 70 | 80+ | 85+ | 90 |
| Laboratorios Jupyter | 10 | 20 | 31 | 34 | 42 | 45 |
| Páginas visualizador | 3 | 7 | 10 | 12 | 14 | 15 |
| Ejercicios | 20 | 35 | 37 | 45+ | 55+ | 65 |
| Tests pytest | 0 | 15 | 31 | 48 | 60+ | 70 |
| Soluciones investigación | 0 | 0 | 0 | 4 | 8 | 8 |

---

## Estado de fases

| Fase | Título | Estado | Versión | Fecha |
|---|---|---|---|---|
| 1–4 | Fundamentos (v1.0) | ✅ Completa | v1.0 | — |
| 5–6 | Algoritmos y Hardware | ✅ Completa | v1.5 | — |
| 7 | Infraestructura educativa | ✅ Completa | v2.0 | — |
| 8 | Hardware avanzado y QML | ✅ Completa | v2.2 | — |
| 9 | Fronteras modernas | ✅ Completa | v2.5 | — |
| 10 | QSVT, Sensing, Compilación | ✅ Completa | v3.0 | 2026-04-27 |
| 11 | Soluciones + Labs 35-37 + CI | ✅ Completa | v3.1 | 2026-04-27 |
| 12 | Aplicaciones industriales extendidas | ✅ Completa | v3.5 | 2026-04-27 |
| 13 | Ecosistema completo | 🔄 En progreso | v4.0 | — |

---

## Fases completadas

### ✅ Fase 1–4 — Fundamentos (v1.0)
- Módulos 01-10: qubits, puertas, entrelazamiento, Qiskit básico
- 10 laboratorios iniciales, tests básicos

### ✅ Fase 5–6 — Algoritmos y Hardware (v1.5)
- Módulos 11-20: VQE, QAOA, hardware, ruido
- Visualizador Streamlit (3 páginas), laboratorios 11-20

### ✅ Fase 7 — Infraestructura educativa (v2.0)
- MkDocs + GitHub Pages, CONTRIBUTING, CODE_OF_CONDUCT
- Autoevaluación interactiva, evaluador de ejercicios
- CI/CD con GitHub Actions, tour interactivo

### ✅ Fase 8 — Hardware avanzado y QML (v2.2)
- Módulos 21-27: sistemas abiertos, recursos, hardware físico, pulsos, PQC, ZX-Calculus
- Laboratorios 21-28 (Pennylane, GPU, UCCSD, QML), Simulador Ruidoso

### ✅ Fase 9 — Fronteras modernas (v2.5)
- Módulos 28-37, Notebook 31 Qiskit Patterns
- Visualizador páginas 8-10, tests 31 casos

### ✅ Fase 10 — QSVT, Sensing y Compilación (v3.0) — 2026-04-27
- [x] Módulos 38-40: Sensing, Compilación Avanzada, QSVT
- [x] Laboratorios 32-34: Química UCCSD, compilación, Quantum Walks
- [x] Visualizador páginas 11-12: Estimador FT, Landscape VQE/QAOA
- [x] Ejercicios investigación R1-R8 (enunciados con stubs)
- [x] Tests: 31 → 48 (QFI, KAK, DTQW, CTQW, Chebyshev)
- [x] Infraestructura: `environment.yml`, `Makefile`, `pyproject.toml`, `.devcontainer/`
- [x] Fix: Simulador Ruidoso (ccx noise model), tour_guide tuples→dicts

### ✅ Fase 11 — Soluciones, Labs 35-37, Baseline CI (v3.1) — 2026-04-27
- [x] **11.1** Soluciones investigación R1-R4 (`Soluciones/investigacion/`)
- [x] **11.2** Notebook 35: Computación Adiabática y QAOA avanzado
- [x] **11.3** Notebook 36: Nuevos Qubits (Fluxonium, Majorana, Spin-Si)
- [x] **11.4** Notebook 37: Redes Cuánticas y QKD avanzado (BB84, E91, repeaters)
- [x] **11.5** Tests baseline JSON + pytest markers `@pytest.mark.slow` (13 tests)
- [x] **11.6** Visualizador página 13: Quantum Walk interactivo (DTQW/CTQW)
- [x] **11.7** MkDocs: labs 32-37, módulos 38-40, ejercicios investigación

### ✅ Fase 12 — Aplicaciones Industriales Extendidas (v3.5) — 2026-04-27
- [x] **12.1** Notebook 38: Quantum Finance — QAE Monte Carlo + portfolio QAOA (`38_quantum_finance_qae.ipynb`)
- [x] **12.2** Notebook 39: Química + Hardware — VQE H₂ con ZNE/PEC en hardware mock (`39_quimica_hardware_zne.ipynb`)
- [x] **12.3** Notebook 40: QML con datos reales — kernel cuántico vs RBF (`40_qml_datos_reales.ipynb`)
- [x] **12.4** Notebook 41: Advantage cuántica — RCS, boson sampling, límites MPS (`41_advantage_cuantica.ipynb`)
- [x] **12.5** Soluciones investigación R5: QFI sensing y límite de Heisenberg (`R5_qfi_sensing.md`)
- [x] **12.6** Soluciones investigación R6: Kernel cuántico vs clásico (`R6_qml_kernel.md`)
- [x] **12.7** Soluciones investigación R7: Umbral fault tolerance + overhead (`R7_fault_tolerance.md`)
- [x] **12.8** Soluciones investigación R8: Complejidad cuántica y lower bounds (`R8_advantage_complejidad.md`)
- [x] **12.9** Visualizador página 14: Dashboard Finance + QML (`14_Finance_QML.py`)
- [ ] **12.10** Tests: 48 → 65+ (notebooks 38-41, finance, kernel, advantage) — *pendiente*

---

## Fase 13 — Ecosistema Completo (v4.0) 🔄 EN PROGRESO

### 13.1 — Certificación y examen
- [ ] Banco de 50 preguntas con soluciones anotadas (`Ejercicios/examen_certificacion.md`)
- [ ] Sistema de autoevaluación con puntuación y retroalimentación por módulo
- [ ] Badge digital generado localmente (SVG parametrizado)

### 13.2 — Módulos de expansión avanzada
- [ ] Módulo 41: DQC avanzada — protocolos entrelazamiento distribuido, quantum repeaters
- [ ] Módulo 42: QML teórico — PAC learning cuántico, VC dimension cuántica
- [ ] Módulo 43: Simulación de materiales — Hamiltoniano Hubbard, Fermi-Hubbard

### 13.3 — Integración con hardware real
- [ ] Guía IBM Quantum Free Plan: credenciales, job submission, queue management
- [ ] Script `run_on_hardware.py`: ejecuta VQE H₂ en ibm_brisbane con transpile + ZNE
- [ ] Comparativa simulador vs hardware real para circuitos cortos

### 13.4 — API pública y comunidad
- [ ] FastAPI endpoints REST para ejecutar circuitos demo (Dockerfile incluido)
- [ ] ISSUE_TEMPLATE para ejercicios educativos
- [ ] Traducción inglés: README y módulos 01-05

---

## Decisiones de arquitectura

| Decisión | Elección | Razón |
|---|---|---|
| Framework cuántico principal | Qiskit 2.x (Primitives V2) | Ecosistema más amplio, soporte IBM |
| Framework secundario | Pennylane (autodiff) | Diferenciación exacta de circuitos |
| t\|ket⟩ | Opcional (Lab 33) | No en PyPI de Streamlit Cloud |
| Simulador ruidoso | Qiskit Aer | Modelos de ruido realistas |
| Visualizador | Streamlit | Sin backend, deploy trivial |
| Docs | MkDocs Material | Indexación por Google, tema profesional |
| Tests | pytest + JSON baseline | Regresión numérica + CI GitHub Actions |
| Contenedores | DevContainer + conda | Reproducibilidad garantizada |

---

## Backlog (no prioritario)

- [ ] Integración con IBM Quantum Network (credenciales por usuario)
- [ ] Soporte para IonQ y Quantinuum via cloud providers
- [ ] Versión LaTeX del tutorial (PDF descargable)
- [ ] Benchmark CLOPS/QV actualizado 2025
- [ ] Módulo 44: Quantum Gravity (AdS/CFT, tensor networks)

---

*Actualizado — 2026-04-27 · v3.5*
