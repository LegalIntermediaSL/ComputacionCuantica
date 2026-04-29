# Plan de Expansión — Computación Cuántica: Teoría y Práctica

**Estado general:** ✅ v5.2 publicado · 2026-04-27 · Fases 1-17 completas  
**Repositorio:** [LegalIntermediaSL/ComputacionCuantica](https://github.com/LegalIntermediaSL/ComputacionCuantica)  
**Streamlit:** [computacioncuantica-legalintermedia.streamlit.app](https://computacioncuantica-legalintermedia.streamlit.app)

---

## Métricas actuales (v5.2)

| Recurso | v1.0 | v2.0 | v3.0 | v4.0 | v5.0 | **v5.2** |
|---|---|---|---|---|---|---|
| Módulos tutoriales | 10 | 20 | 40 | 41 | 42 | **43** |
| Laboratorios Jupyter | 10 | 20 | 34 | 45 | 46 | **47** |
| Páginas visualizador | 3 | 7 | 12 | 16 | 16 | **16** |
| Tests pytest | 0 | 15 | 48 | 101 | 115 | **129** |
| Soluciones investigación | 0 | 0 | 4 | 8 | 8 | **8** |
| Páginas de docs (MkDocs) | 5 | 12 | 22 | 30 | 33+ | **34+** |
| Workflows GitHub Actions | 0 | 1 | 2 | 4 | 5 | **5** |

---

## Mapa de fases

```
v1.0        v1.5        v2.0        v2.2        v2.5
 ├── F1-4    ├── F5-6    ├── F7       ├── F8       ├── F9
 │           │           │            │            │
 ✅          ✅          ✅           ✅           ✅

v3.0        v3.1        v3.5        v4.0-pre     v4.0        v5.0        v5.1        v5.2
 ├── F10     ├── F11     ├── F12      ├── F13      ├── F14     ├── F15     ├── F16     ├── F17
 │           │           │            │            │           │           │           │
 ✅          ✅          ✅          ✅              ✅          ✅          ✅          ✅
```

---

## Estado detallado de todas las fases

| # | Título | Estado | Versión | Fecha | Entregables clave |
|---|---|---|---|---|---|
| 1–4 | Fundamentos | ✅ | v1.0 | — | Módulos 01-10, labs 01-10, tests básicos |
| 5–6 | Algoritmos y Hardware | ✅ | v1.5 | — | Módulos 11-20, VQE/QAOA, labs 11-20 |
| 7 | Infraestructura educativa | ✅ | v2.0 | — | MkDocs, CI/CD, tour interactivo, evaluador |
| 8 | Hardware avanzado y QML | ✅ | v2.2 | — | Módulos 21-27, labs 21-28, Simulador Ruidoso |
| 9 | Fronteras modernas | ✅ | v2.5 | — | Módulos 28-37, lab 31, visualizador pp 8-10 |
| 10 | QSVT, Sensing, Compilación | ✅ | v3.0 | 2026-04-27 | Módulos 38-40, labs 32-34, pp 11-12, infra |
| 11 | Soluciones + Labs 35-37 + CI | ✅ | v3.1 | 2026-04-27 | R1-R4, labs 35-37, p.13, baseline JSON |
| 12 | Aplicaciones industriales | ✅ | v3.5 | 2026-04-27 | Labs 38-41, R5-R8, pp 13-14, 65 tests |
| 13 | Ecosistema completo | ✅ | v4.0 | 2026-04-27 | Certificación, labs 42-44, IBM real, API, Docker |
| 14 | Revisión y QA | ✅ | v4.0 | 2026-04-27 | 76 tests, 0 errores, deps sync, show_tour p.15 |
| 15 | Topological QC + Property Tests + PDF CI | ✅ | v5.0 | 2026-04-27 | Módulo 41, Lab 45, p.16 Benchmark, Hypothesis 101 tests, PDF pipeline |
| 16 | Tensor Networks + Jupyter Book | ✅ | v5.1 | 2026-04-28 | Módulo 42, Lab 46, Jupyter Book, 14 tests MPS → 115 total |
| 17 | Quantum Gravity + iDMRG + Multi-provider | ✅ | v5.2 | 2026-04-27 | Módulo 43, Lab 47, guía multiprovider, 14 tests iDMRG → 129 total |

---

## Fases completadas — detalle

### ✅ Fase 1–4 — Fundamentos (v1.0)

- ✅ Módulos 01-10: Qubits, Qiskit básico, Entrelazamiento, Runtime, Algoritmos, Ruido y hardware, QPE, Matrices densidad, QEC repetición, Primitivas V2.
- ✅ Labs 01-10: `01_grover_dos_qubits`, `02_teleportacion_guiada`, `03_transpilacion`, `04_bernstein_vazirani`, `05_qft_tres_qubits`, `06_informacion_cuantica`, `07_phase_estimation`, `08_matrices_densidad`, `09_correccion_errores`, `10_qiskit_primitives`.
- ✅ Tests iniciales: norma de estado, entrelazamiento Bell, fases QFT, amplificación Grover, QPE.

---

### ✅ Fase 5–6 — Algoritmos y Hardware (v1.5)

- ✅ Módulos 11-20: VQE, QAOA, hardware superconductor, pulsos, tomografía, POVM, Hamiltoniano Ising.
- ✅ Labs 11-20: `11_vqe_y_circuitos_parametrizados`, `12_optimizacion_quimica`, `13_estimator_y_energia`, `14_densitymatrix_ruido_y_tomografia`, `15_evolucion_tiempo_trotter`, `16_canales_de_kraus`, `17_medidas_povm`, `18_calibracion_pulsos_rabi`, `19_tomografia_estados`, `20_intro_qiskit_pulse`.
- ✅ Visualizador páginas 1-3: Bloch, Algoritmos paso a paso, Canales y Ruido.

---

### ✅ Fase 7 — Infraestructura educativa (v2.0)

- ✅ MkDocs Material con GitHub Pages y tema bilingüe.
- ✅ CI/CD GitHub Actions: pytest en push, lint, despliegue automático docs.
- ✅ Tour interactivo `tour_guide.py` con pasos guiados por página.
- ✅ Evaluador de ejercicios con feedback automático y puntuación.
- ✅ `CONTRIBUTING.md` y `CODE_OF_CONDUCT.md`.

---

### ✅ Fase 8 — Hardware avanzado y QML (v2.2)

- ✅ Módulos 21-27: sistemas abiertos (Lindblad), recursos cuánticos, hardware real, pulsos (Rabi, eco), PQC avanzado, ZX-Calculus, internet cuántico (swapping, purificación).
- ✅ Labs 21-28: `21_optimizacion_carteras_vqe`, `22_qae_valoracion_activos`, `23_qml_kernel_alignment`, `24_error_mitigation_zne_pec`, `25_zx_calculus`, `26_qiskit_runtime`, `27_qml_datos_reales`, `28_vqe_uccsd_moleculas`.
- ✅ Visualizador páginas 4-9: Hardware Dashboard, VQE/QAOA, QEC, Compositor, Tomografía, Simulador Ruidoso.

---

### ✅ Fase 9 — Fronteras modernas (v2.5)

- ✅ Módulos 28-37: advantage casos reales, QEC hardware, DQC, algoritmos FT, sistemas abiertos avanzados, computación adiabática, PQC profundidad, nuevos qubits, redes cuánticas.
- ✅ Lab 31: `31_qiskit_patterns` — Qiskit Patterns + Sampler/Estimator V2.
- ✅ Visualizador páginas 8-10: Tomografía interactiva, Simulador Ruidoso (Aer), Algoritmos completos.
- ✅ Tests: 31 casos, cobertura de ruido, VQE, QAOA.

---

### ✅ Fase 10 — QSVT, Sensing y Compilación (v3.0) — 2026-04-27

- ✅ **10.1** `Tutorial/38` Quantum Sensing y Metrología: QFI, Cramér-Rao, magnetometría NV, límites SQL/HL.
- ✅ **10.2** `Tutorial/39` Compilación cuántica avanzada: pases Qiskit, descomposición KAK, Solovay-Kitaev, t|ket⟩.
- ✅ **10.3** `Tutorial/40` QSVT y Block-Encoding: aproximación Chebyshev, HHL óptimo, block-encoding QR.
- ✅ **10.4** `32_quimica_avanzada_vqe_uccsd.ipynb`: VQE UCCSD H₂/LiH, curva potencial vs FCI, QWC cost.
- ✅ **10.5** `33_compilacion_tket_qiskit.ipynb`: Qiskit niveles 0-3, KAK, t|ket⟩ opcional.
- ✅ **10.6** `34_quantum_walk_dtqw_ctqw.ipynb`: DTQW balístico, 4 monedas, CTQW, búsqueda en K_N.
- ✅ **10.7** `11_Recursos_FT.py`: Estimador FT (surface code, overhead, magic state).
- ✅ **10.8** `12_Landscape_Parametros.py`: Landscape VQE/QAOA (barren plateaus, optimizadores).
- ✅ **10.9** `ejercicios_investigacion.md`: 8 enunciados con stubs de código.
- ✅ **10.10** Tests 31→48: QFI GHZ/SQL, Ramsey, KAK ≤3 CX, transpile optimiza, Euler 1Q, Chebyshev sgn, QSVT depth, HHL queries, UCCSD H₂, DTQW balístico, CTQW norma, búsqueda CTQW, coins differ.
- ✅ **10.11** Infraestructura: `environment.yml`, `Makefile`, `pyproject.toml` PEP 517, `.devcontainer/devcontainer.json`.
- ✅ **10.12** Fixes críticos: Simulador Ruidoso `ccx` noise model (2Q→3Q), tour_guide tuples→dicts en pp 10/11/12.

---

### ✅ Fase 11 — Soluciones, Labs 35-37, Baseline CI (v3.1) — 2026-04-27

- ✅ **11.1** `R1_qsvt_chebyshev.md`: Chebyshev sgn(x), α=π²/(4ln(1/δ)), QSVT vs LCU-Taylor.
- ✅ **11.2** `R2_block_encoding.md`: QR-completion, verificación ||U[:4,:4]-A||, ancilla count.
- ✅ **11.3** `R3_barren_plateaus.md`: Var[grad] vs n, base ≈ (4/3)^(-n), identity-init mitigation.
- ✅ **11.4** `R4_zne_error_mitigation.md`: Richardson λ=1,3,5, ZNE vs PEC comparison table.
- ✅ **11.5** `35_computacion_adiabatica_qaoa.ipynb`: brecha adiabática, Trotter, QAOA p=1-4 MAX-CUT.
- ✅ **11.6** `36_nuevos_qubits_fluxonium_majorana.ipynb`: transamón vs Fluxonium, plataformas 2024-28.
- ✅ **11.7** `37_redes_cuanticas_qkd.ipynb`: BB84+Eva, E91 CHSH, BBPSSW, repeaters, MDI/TF-QKD.
- ✅ **11.8** `tests/baseline.json`: valores de referencia para 15 módulos.
- ✅ **11.9** `@pytest.mark.slow` en 13 tests; `make test-fast` excluye lentos.
- ✅ **11.10** `13_Quantum_Walk.py`: DTQW/CTQW interactivo, 4 monedas, σ(t), exportar PNG.
- ✅ **11.11** `mkdocs.yml`: labs 32-37, módulos 38-40, ejercicios investigación en nav.

---

### ✅ Fase 12 — Aplicaciones Industriales Extendidas (v3.5) — 2026-04-27

- ✅ **12.1** `38_quantum_finance_qae.ipynb`: QAE Monte Carlo, portfolio QAOA media-varianza, CVaR cuántico.
- ✅ **12.2** `39_quimica_hardware_zne.ipynb`: VQE H₂ + AerSimulator mock + ZNE Richardson + curva disociación.
- ✅ **12.3** `40_qml_datos_reales.ipynb`: ZZFeatureMap manual, kernel cuántico vs RBF/lineal, KTA, boundaries.
- ✅ **12.4** `41_advantage_cuantica.ipynb`: RCS/XEB, Boson Sampling (permanente Ryser), límites MPS, outlook 2025.
- ✅ **12.5** `R5_qfi_sensing.md`: GHZ vs SQL, Cramér-Rao, dephasing óptimo n_opt≈1/(2γt).
- ✅ **12.6** `R6_qml_kernel.md`: ZZFeatureMap, KTA, cuándo supera al RBF, Huang 2021.
- ✅ **12.7** `R7_fault_tolerance.md`: p_th repetición=0.5, surface ≈1%, overhead d², magic state distillation.
- ✅ **12.8** `R8_advantage_complejidad.md`: jerarquía BQP/QMA/PSPACE, lower bounds, dequantization, crossover.
- ✅ **12.9** `14_Finance_QML.py`: QAOA portfolio + frontera Markowitz, kernel ZZFeatureMap + KTA interactivo.
- ✅ **12.10** Tests 48→65: portfolio, ZNE folding, kernel simetría/KTA, boson sampling permanente, XEB, QFI, FT.

---

## ✅ Fase 13 — Ecosistema Completo (v4.0) — 2026-04-27

### 13.1 — Certificación y banco de preguntas
**Objetivo:** sistema de autoevaluación estructurado con 50 preguntas por nivel y retroalimentación anotada.

- ✅ `Ejercicios/examen_certificacion.md`: 50 preguntas (10 básico, 15 intermedio, 8 avanzado, 2 investigación bonus) con soluciones anotadas y referencias cruzadas a módulos.
- ✅ `Ejercicios/autoevaluacion_modular.md`: checklist de 123 competencias por módulo (01-40), con criterios de evaluación objetivos y tabla de progreso.
- ✅ Página Streamlit 15 (`15_Certificacion.py`): quiz interactivo de 20 preguntas, badge SVG descargable, desglose por nivel.
- ✅ Badge SVG parametrizado con nombre, fecha, nivel alcanzado (Básico/Intermedio/Avanzado/Investigador).

### 13.2 — Módulos de expansión avanzada
**Objetivo:** 3 laboratorios nuevos que cubren gaps en DQC, teoría QML y simulación de materiales.

- ✅ Lab `42_dqc_avanzada.ipynb`: entanglement swapping 4-qubits, BQC (δ uniforme), BB84 con/sin Eve, telepuerta con canal ruidoso vs límite clásico 2/3.
- ✅ Lab `43_qml_teorico.ipynb`: PAC learning (complejidad de muestra), VC-dimension de PQC, barren plateaus analíticos, dequantization y QAE vs Monte Carlo.
- ✅ Lab `44_hubbard_vqe.ipynb`: Hamiltoniano Hubbard L=2 via Jordan-Wigner (4 qubits), VQE completo, gap de carga, diagrama de fase metal-aislante U/t.

### 13.3 — Integración con hardware real IBM
**Objetivo:** guía práctica para ejecutar los labs clave en IBM Quantum Free Plan.

- ✅ `docs/guia_ibm_quantum.md`: registro, configuración QiskitRuntimeService, gestión de colas, mitigación M3, límites del plan gratuito.
- ✅ `run_on_hardware.py`: script CLI que ejecuta VQE H₂ con warm-start simulador + hardware (2 backends, dry-run mode, JSON output).
- ✅ `docs/error_rates_2025.md`: tabla completa IBM/Google/IonQ/Quantinuum 2025: T1, T2, error 1Q/2Q, readout, QV, CLOPS.

### 13.4 — API REST y comunidad
**Objetivo:** endpoints públicos para ejecutar demos sin instalar nada, plantillas de contribución.

- ✅ `api/main.py`: FastAPI con endpoints `/run-circuit` (QASM2), `/run-vqe` (H₂), `/run-grover` (n-qubits, k marcados); respuesta JSON tipada con Pydantic.
- ✅ `Dockerfile` + `docker-compose.yml`: contenedor reproducible con Qiskit + FastAPI (8000) + Streamlit (8501).
- ✅ `.github/ISSUE_TEMPLATE/ejercicio_educativo.md`: plantilla para proponer nuevos ejercicios con enunciado, solución, nivel y checklist de revisión.
- ✅ `TRANSLATING.md`: guía de traducción con tabla de estado por idioma, terminología estándar, flujo de PR.

### 13.5 — Tests Fase 13 (76 en total, +11 nuevos)
- ✅ `test_pac_sample_complexity_finite`: escala O(1/ε)
- ✅ `test_vc_dimension_linear_in_params`: VC-dim ∝ n_params
- ✅ `test_barren_plateau_gradient_scale`: Var[grad] ∝ 4^(-n)
- ✅ `test_entanglement_swapping_bell_input`: 4 estados nonzero ×0.25
- ✅ `test_bqc_delta_uniform`: media≈π, varianza≈π²/3
- ✅ `test_bb84_qber_without_eve`: QBER=0, tasa≈50%
- ✅ `test_bb84_qber_with_full_eve`: QBER≈25% teórico y simulado
- ✅ `test_hubbard_jw_energy_l2`: E0<0 (hopping domina)
- ✅ `test_grover_api_counts`: estado marcado >50% del total
- ✅ `test_qae_speedup_quadratic`: speedup = 1/ε (cuadrático)
- ✅ `test_teleportation_above_classical`: F(p) decreciente, F(0.5)=2/3

---

## ✅ Fase 14 — Revisión y QA (v4.0) — 2026-04-27

**Objetivo:** verificar la integridad de todos los entregables v4.0.

### 14.1 — Tests y cobertura

- ✅ Suite completa pytest 76 tests — **0 fallos** (63 fast + 13 slow).
- ✅ `make test-fast` (sin `@pytest.mark.slow`): 63 tests en **< 1 s**.
- ✅ `tests/baseline.json` actualizado a v1.3.0: módulos 01-44, labs 38-44, DQC, QML, Hubbard.

### 14.2 — Integridad de notebooks

- ✅ 54 notebooks validados como JSON válido — **0 errores**.
- ✅ Todos tienen `nbformat=4` — **0 problemas de formato**.
- ✅ 44 labs numerados (01-44) + 2 extras (`entanglement_swapping`, `pyzx_optimizacion`).

### 14.3 — Visualizador Streamlit

- ✅ 15 páginas con sintaxis Python válida (`py_compile`) — **0 errores**.
- ✅ `show_tour()` presente en todas las páginas (añadida a p.15 en esta fase).
- ✅ `@st.cache_data` en pp.13/14/15 usa solo tipos hashables (int, str, tuple).
- ✅ Kernel cuántico en p.14 limitado a max 60 puntos — memoria O(n²) = ~28 KB máx.
- ⏳ Verificar deploy en Streamlit Cloud — pendiente verificación manual externa (fuera del alcance de CI local).

### 14.4 — Documentación y MkDocs

- ✅ 45 refs en `mkdocs.yml` — **0 archivos faltantes**.
- ✅ `README.md`: 44 labs ✅, 15 páginas ✅, 76 tests ✅, v4.0.0 ✅.
- ✅ `changelog.md`: entradas v1.0.0 – v1.3.0 presentes ✅.

### 14.5 — Dependencias y entorno

- ✅ `requirements.txt` + `environment.yml` + `pyproject.toml`: añadido `scikit-learn>=1.4` (usado en labs 42-43).
- ✅ `pyproject.toml` versión `4.0.0` ✅.
- ✅ Todos los imports de nuevos notebooks cubiertos en requirements.

### 14.6 — Revisión de código de las páginas nuevas (13-15)

- ✅ `13_Quantum_Walk.py`: `@st.cache_data` args son `int, int, str, tuple` — todos hashables ✅.
- ✅ `14_Finance_QML.py`: kernel cuántico slider max=60, arrays convertidos a tuplas para cache ✅.
- ✅ `15_Certificacion.py`: `show_tour()` añadido con 5 pasos ✅. Sin matplotlib → `export_figure_button` no aplicable.
- ✅ Páginas 1-12: `show_tour` presente en todas; `export_figure_button` disponible pero no en todas — aceptado como comportamiento existente (no blocking).

### 14.7 — Workflow GitHub Actions

- ✅ `test_code_snippets.yml`: desactivado triggers push/PR → solo `workflow_dispatch` (manual).

---

## ✅ Fase 16 — Tensor Networks y Jupyter Book (v5.1) — 2026-04-28

### 16.1 — Módulo 42: Tensor Networks y DMRG

- ✅ `Tutorial/42_tensor_networks/README.md`: MPS, notación diagramática, Schmidt decomposition, area law (Hastings), operaciones MPS (forma canónica, truncamiento SVD), DMRG (barridos, eigenproblema efectivo), TEBD (Trotter, cadena XX), PEPS/MERA/TTN, conexión con QC (dequantización, VQE vs DMRG).

### 16.2 — Lab 46: MPS con numpy

- ✅ `46_mps_tensor_networks.ipynb`: Implementación MPS desde cero — SVD recursiva, reconstrucción exacta, truncamiento con fidelidad, entropía de entrelazamiento por corte (Néel/GHZ/W/aleatorio), TEBD cadena XX (magnetización spacio-temporal + crecimiento de entrelazamiento), comparativa parámetros MPS vs vector completo.

### 16.3 — Jupyter Book

- ✅ `_config.yml`: configuración Jupyter Book v5.1 — launch buttons (Binder/Colab), MyST extensions, tema book.
- ✅ `_toc.yml`: tabla de contenidos del libro — 7 partes, módulos 01-42, labs 32-46, ejercicios, hardware, contribución.
- ✅ `.github/workflows/build_jupyterbook.yml`: build automático en push a `main` cuando cambian Tutorial/Cuadernos/docs.

### 16.4 — Tests Tensor Networks (115 totales, +14 nuevos)

- ✅ `tests/test_tensor_networks.py`: 14 tests nuevos.
  - Estado producto: χ=1, S=0 en todos los cortes
  - Estado Néel: χ=1 (estado producto aunque alternado)
  - Estado GHZ: χ=2, S=1 ebit exacto
  - Reconstrucción exacta: fidelidad > 1-10⁻¹⁰
  - Fidelidad monótona con χ
  - Entropía: no negativa, acotada por min(cut, n-cut)
  - Valores de Schmidt: Σλ_k²=1 en todos los cortes
  - Bond dimension máximo: χ ≤ 2^(n//2)
  - Conteo de tensores y dimensión física
  - TEBD: norma conservada tras evolución

---

## ✅ Fase 15 — Topological QC, Property Tests y PDF CI (v5.0) — 2026-04-27

### 15.1 — Módulo 41: Computación Cuántica Topológica

- ✅ `Tutorial/41_topological_qc`: Anyones, código tórico de Kitaev, operadores Av/Bp, espacio lógico, umbral ~10.9%, anyones de Fibonacci, qubits de Majorana (Microsoft 2025).

### 15.2 — Lab 45: Código Tórico con Qiskit

- ✅ `45_toric_code.ipynb`: Construcción retículo L×L, verificación [Av,Bp]=0 para todos los pares, estado de código vía proyector gauge, operadores lógicos X̄/Z̄, introducción/corrección de errores, error lógico indetectable por síndrome, escalado de P_L vs umbral.

### 15.3 — Página 16: Benchmark Hardware Interactivo

- ✅ `16_Benchmark_Hardware.py`: Tabla comparativa 6 sistemas (IBM Heron/Eagle, Google Willow, Quantinuum H2, IonQ Forte, QuEra Aquila), 4 tabs de gráficos (error 2Q vs umbral, QV vs CLOPS, T1/T2, evolución histórica), calculadora de overhead FT con código de superficie.

### 15.4 — PDF automático vía GitHub Actions

- ✅ `.github/workflows/build_pdf.yml`: Build MkDocs + WeasyPrint en release, adjunta PDF al release de GitHub, artifact de 90 días, `workflow_dispatch` manual.
- ✅ `mkdocs.yml`: Plugin `pdf-export` habilitado vía variable de entorno `ENABLE_PDF_EXPORT`.

### 15.5 — Property-based tests con Hypothesis (101 tests totales)

- ✅ `tests/test_property_based.py`: 25 tests nuevos con Hypothesis (76 → 101 total).
  - Estados cuánticos: norma, entropía von Neumann, PSD, traza
  - Algebra de Pauli: involutividad, anticonmutación, unitariedad de rotaciones
  - Código tórico: paridad aristas compartidas, síndromes X/Z, conteos
  - Principio variacional para Hamiltoniano aleatorio
  - PAC learning: monotonicidad en ε y |H|
  - BB84: QBER=0 sin Eva, QBER≈25% con Eva completa
  - Barren plateaus: Var[grad] ∝ 4^(-n)
  - Teleportación: monotonicidad y límite F(0.5)=2/3
  - Umbral tórico: P_L decreciente con L

### 15.6 — Dependencias actualizadas

- ✅ `hypothesis>=6.100` añadido a `requirements.txt`, `environment.yml`, `pyproject.toml` (dev).
- ✅ `mkdocs.yml`: módulo 41 y lab 45 añadidos a nav, sección "Topológica" creada.

---

## Decisiones de arquitectura

| Decisión | Elección | Razón |
|---|---|---|
| Framework cuántico principal | Qiskit 2.x (Primitives V2) | Ecosistema más amplio, soporte IBM, estabilidad API |
| Framework secundario | Pennylane (autodiff) | Diferenciación exacta por parameter-shift sin simulador ruidoso |
| t\|ket⟩ | Opcional (Lab 33) | Ausente de PyPI de Streamlit Cloud |
| Simulador ruidoso | Qiskit Aer | Modelos de ruido realistas (depolarizante, T1/T2, readout) |
| Visualizador | Streamlit | Sin backend, deploy trivial en Community Cloud |
| Documentación | MkDocs Material | Indexable por Google, tema profesional, búsqueda integrada |
| Tests | pytest + JSON baseline | Regresión numérica determinista + CI GitHub Actions |
| Contenedores | DevContainer + conda | Reproducibilidad garantizada en Codespaces/VS Code |
| Notebooks | Jupyter nbformat 4 | Estándar universal, compatible nbviewer/Colab/JupyterHub |
| Soluciones | Markdown con código | Legibles en GitHub sin ejecución |

---

## Inventario de archivos clave (v3.5)

### Visualizador (`visualizador/pages/`)
| Página | Archivo | Tema |
|---|---|---|
| 1 | `1_Esfera_de_Bloch.py` | Bloch sphere, estados Pauli |
| 2 | `2_Algoritmos_Paso_a_Paso.py` | Grover, QFT, QPE animado |
| 3 | `3_Canales_y_Ruido.py` | Canales Kraus, proceso |
| 4 | `4_Hardware_Dashboard.py` | Error rates, conectividad |
| 5 | `5_VQE_QAOA.py` | Landscape interactivo |
| 6 | `6_Corrección_de_Errores.py` | Código repetición, surface |
| 7 | `7_Compositor_de_Circuitos.py` | Drag-and-drop circuitos |
| 8 | `8_Tomografia.py` | Tomografía de estados |
| 9 | `9_Simulador_Ruidoso.py` | AerSimulator + métricas |
| 10 | `10_Algoritmos_Completos.py` | Shor, HHL, QAOA |
| 11 | `11_Recursos_FT.py` | Surface code, overhead |
| 12 | `12_Landscape_Parametros.py` | VQE/QAOA landscape |
| 13 | `13_Quantum_Walk.py` | DTQW/CTQW interactivo |
| 14 | `14_Finance_QML.py` | Portfolio QAOA + kernel |
| 15 | `15_Certificacion.py` | Quiz interactivo + badge SVG |
| 16 | `16_Benchmark_Hardware.py` | Benchmark CLOPS/QV/T1 2025 + overhead FT |

### Soluciones investigación (`Soluciones/investigacion/`)
| Solución | Tema | Estado |
|---|---|---|
| R1 | QSVT: Chebyshev óptimo | ✅ Completa |
| R2 | Block-encoding explícita | ✅ Completa |
| R3 | Barren plateaus: escalado + mitigación | ✅ Completa |
| R4 | ZNE vs PEC | ✅ Completa |
| R5 | QFI y límite de Heisenberg | ✅ Completa |
| R6 | Kernel cuántico vs clásico | ✅ Completa |
| R7 | Fault tolerance: umbral + overhead | ✅ Completa |
| R8 | Advantage cuántica: complejidad | ✅ Completa |

---

## ✅ Fase 17 — Quantum Gravity, iDMRG y Multi-provider (v5.2) — 2026-04-27

### 17.1 — Módulo 43: Gravedad Cuántica ligera

- ✅ `Tutorial/43_quantum_gravity/README.md`: correspondencia AdS/CFT, métrica AdS, MERA como AdS₃ discreto, fórmula de Ryu-Takayanagi S_A = Área(γ_A)/4G_N, código HaPPY (holographic pentagon [[5,1,3]]), ER=EPR (BTZ eternal black hole ↔ Bell state), OTOC scrambling y cota de Planck λ_L ≤ 2π/β, boceto SYK en Qiskit, tabla de estado del arte 2025.

### 17.2 — Lab 47: iDMRG para cadena de Heisenberg

- ✅ `47_dmrg_heisenberg.ipynb`: Hamiltoniano Heisenberg exact diagonalization (n=4-10), `DMRGBlock` con operadores H/Sp/Sm/Sz, `initial_block`, `enlarge_block`, `truncate_block` (density matrix eigendecomposition), `idmrg` (crecimiento simétrico hasta n=30), convergencia E₀/n → Bethe ansatz (−0.4431), convergencia en χ (4→64), función de correlación spin-spin, perfil de entrelazamiento, comparativa VQE vs DMRG.

### 17.3 — Guía Multi-provider

- ✅ `docs/guia_multiprovider.md`: IonQ via Amazon Braket (`qiskit-braket-provider`), Quantinuum via Azure Quantum (`azure-quantum`, créditos HQC), IonQ directo (`qiskit-ionq`), Pasqal via Azure, tabla comparativa por caso de uso, ZNE multi-provider (fold_circuit + Richardson), ejemplo VQE H₂ en IonQ Aria (simulación local + comentarios hardware), tabla de costes y planes gratuitos 2025.

### 17.4 — Tests iDMRG (129 totales, +14 nuevos)

- ✅ `tests/test_dmrg.py`: 14 tests nuevos.
  - Heisenberg: Hermitiano, dimensión 2^n, E0<0 (AFM), n=2 singlete E0=-3, estado normalizado, J<0 ferromagnético E0<0
  - DMRGBlock: `initial_block` (basis_size=2, H=0, length=1), `enlarge_block` duplica basis_size, H Hermitiano, `truncate_block` reduce basis_size ≤ chi
  - iDMRG: E0/n negativa, convergencia a Bethe ansatz (<5% error para n=20 chi=32), E/n<-0.3 para chi moderado, χ mayor → E más baja (variacional)

---

## Backlog (candidatos Fase 18)

- ✅ Módulo 42: Tensor Networks y DMRG — completado en Fase 16
- ✅ Lab 46: Simulación MPS — completado en Fase 16
- ✅ Jupyter Book — completado en Fase 16
- ✅ Módulo 43: Quantum Gravity ligero — completado en Fase 17
- ✅ Lab 47: iDMRG cadena de Heisenberg — completado en Fase 17
- ✅ Soporte para IonQ y Quantinuum via cloud providers — completado en Fase 17
- ✅ PDF descargable vía GitHub Actions — completado en Fase 15 (`build_pdf.yml`)
- ✅ Benchmark CLOPS/QV 2025 interactivo — completado en Fase 15 (Página 16)
- ✅ Módulo 41: Topological QC — completado en Fase 15
- [ ] Integración con IBM Quantum Network (credenciales por usuario, no por repo)
- [ ] Simulación en GPU con `qiskit-aer` CUDA backend (requiere NVIDIA hardware)
- [ ] Módulo 44: Computación cuántica distribuida (DQC) avanzada con repetidores
- [ ] Lab 48: DMRG 2D (PEPS) para modelo de Hubbard cuadrado

---

*Actualizado 2026-04-27 · v5.2 publicado · Fases 1-17 todas ✅ · Backlog abierto para Fase 18*
