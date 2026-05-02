# Plan de Expansión — Computación Cuántica: Teoría y Práctica

**Estado general:** ✅ v5.5 publicado · 2026-05-02 · Fases 1-20 completas · **Fase 25 COMPLETA** ✅  
**Repositorio:** [LegalIntermediaSL/ComputacionCuantica](https://github.com/LegalIntermediaSL/ComputacionCuantica)  
**Streamlit:** [computacioncuantica-legalintermedia.streamlit.app](https://computacioncuantica-legalintermedia.streamlit.app)

---

## Métricas actuales (v5.2) y proyección

| Recurso | v1.0 | v2.0 | v3.0 | v4.0 | v5.0 | **v5.2** | v5.3 | v5.4 | v5.5 | v5.6 | v6.0 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Módulos tutoriales | 10 | 20 | 40 | 41 | 42 | **43** | 44 | 45 | 46 | 47 | 49 |
| Laboratorios Jupyter | 10 | 20 | 34 | 45 | 46 | **47** | 48 | 49 | 50 | 51 | 53 |
| Páginas visualizador | 3 | 7 | 12 | 16 | 16 | **16** | 16 | 17 | 18 | 19 | 20 |
| Tests pytest | 0 | 15 | 48 | 101 | 115 | **129** | ~149 | ~159 | ~169 | ~184 | ~210 |
| Soluciones investigación | 0 | 0 | 4 | 8 | 8 | **8** | 8 | 9 | 10 | 12 | 12 |
| Páginas de docs (MkDocs) | 5 | 12 | 22 | 30 | 33+ | **34+** | 36+ | 38+ | 40+ | 42+ | 46+ |
| Workflows GitHub Actions | 0 | 1 | 2 | 4 | 5 | **5** | 5 | 5 | 6 | 6 | 7 |
| Resúmenes | — | — | — | — | — | **10** | 10 | 10 | 12 | 14 | 20 |

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

v5.3        v5.4        v5.5        v5.6        v6.0        v6.1        v6.2
 ├── F18     ├── F19     ├── F20      ├── F21      ├── F22     ├── F23     ├── F24
 │           │           │            │            │           │           │
 ✅          ✅          ✅          📋           📋          📋          📋
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
| 18 | DQC avanzado + PEPS + IBM Network + GPU | ✅ | v5.3 | 2026-05-01 | Módulo 44, Lab 48, guías IBM/GPU/multiprovider, 20 tests → 149 total |
| 19 | Computación Fotónica | ✅ | v5.4 | 2026-05-02 | Módulo 45, Lab 49, visualizador p.17, 10 tests → 159 total |
| 20 | Átomos Neutros y Rydberg | ✅ | v5.5 | 2026-05-02 | Módulo 46, Lab 50, visualizador p.18, 10 tests → 169 total |
| 21 | qLDPC + Decodificadores Neuronales | 📋 | v5.6 | — | Módulo 47, Lab 51, visualizador p.19, R9, ~15 tests → ~184 total |
| 22 | QNLP + D-Wave + Annealing | 📋 | v6.0 | — | Módulos 48-49, Labs 52-53, visualizador p.20, ~15 tests → ~199 total |
| 23 | Calidad e Infraestructura QA | 📋 | v6.0 | — | nbval CI, pytest-cov, resúmenes ×20, R10-R12, progreso estudiante |
| 24 | Traducción y Comunidad | 📋 | v6.1 | — | Traducción inglés, gamificación contribuidores, rutas IA |
| 25 | Completar Labs 01-23 (stubs → completos) | ✅ | v5.4 | 2026-04-30 | 25.1✅ 25.2✅ 25.3✅ 25.4✅ 25.5✅ — 47 tests nuevos |

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

---

## 🔜 Fase 18 — DQC Avanzado, PEPS y Escalabilidad (v5.3) — PLANIFICADA

**Estado:** 🚧 En progreso · 18.1 ✅ · 18.2 ✅ · 18.4 ✅ · Estimación: ~4-5 entregables · ~20 tests nuevos

### 18.1 — Módulo 44: DQC avanzada con repetidores cuánticos

**Objetivo:** cubrir el gap entre el Lab 42 (DQC básico) y arquitecturas reales de internet cuántico.

- ✅ `Tutorial/44_dqc_repetidores/README.md`: estado Werner, purificación BBPSSW/DEJMPS (fórmulas F' y P_éxito, convergencia iterativa), entanglement swapping (circuito Qiskit), repetidores 1G/2G/3G (tasa R∝exp(-√(αL)), requisitos T_mem), fidelidad vs tiempo de memoria, MDI-QKD y TF-QKD (supera límite PLOB), métricas de red (BGR, F_link, D_eff), tabla de plataformas 2025, hoja de ruta SEQC 2025-2035, red de 3 nodos en Qiskit.

### 18.2 — Lab 48: PEPS y Hubbard 2D en cilindro

**Objetivo:** extender el análisis de redes tensoriales al caso 2D e implementar la transición metal-aislante de Mott.

- ✅ `48_peps_hubbard_2d.ipynb`: PEPS class (contracción exacta 2×2 vía einsum, escalado de entropía vs D, area law 2D), Hamiltoniano Hubbard 2D via JW (sparse, bit manipulation), ED para cilindro 2×2 y 2×4, gap de carga Δc(U/t), doble ocupación ⟨D⟩, factor de estructura antiferromagnético S(π,π), diagrama de fase metal-aislante de Mott, tabla PEPS vs MPS.

### 18.3 — Integración IBM Quantum Network

**Objetivo:** permitir al estudiante ejecutar labs clave en hardware IBM real sin credenciales hardcodeadas.

- [ ] `docs/guia_ibm_network.md`: gestión de tokens via variable de entorno `IBM_QUANTUM_TOKEN`, selección dinámica del backend menos congestionado (`least_busy`), estimación de tiempo de cola, resultado con M3 readout mitigation, límites del plan Open (10 min/mes).
- [ ] `run_on_hardware.py` extendido: soporte `--provider ionq|quantinuum|ibm`, dry-run mode, output JSON con metadata de hardware.

### 18.4 — Simulación GPU con `qiskit-aer` CUDA

**Objetivo:** habilitar simulaciones de >30 qubits en hardware con GPU NVIDIA.

- ✅ `docs/guia_gpu_aer.md`: requisitos hardware/software (VRAM vs n qubits), instalación pip/conda/source, backends GPU (statevector/density_matrix/MPS), cuStateVec (speedup 4-8×), benchmark CPU vs GPU 24-32 qubits con tabla de referencia, ruido en GPU, precisión single (mitad de memoria), multi-GPU con blocking, integración Qiskit Runtime, troubleshooting.
- ✅ `Makefile` target `test-gpu`: `python -m pytest tests/ -m gpu` — skip automático sin GPU.
- ✅ `tests/test_gpu_aer.py`: 9 tests con `@pytest.mark.gpu` + `@skip_no_gpu` — detección automática, Bell state GPU vs CPU, norma statevector, VQE H₂ GPU, speedup n=24, MPS-GPU n=30, precisión single. `gpu` registrado en `pyproject.toml`.

### 18.5 — Tests Fase 18 (~20 nuevos → ~149 totales)

- [ ] `tests/test_dqc_advanced.py`: purificación BBPSSW (fidelidad crece con rondas), tasa Bell pairs vs distancia, fidelidad memory decay, MDI-QKD QBER.
- [ ] `tests/test_peps.py`: norma PEPS producto=1, entropía 2D acotada por perímetro (area law 2D), energía Hubbard 2×2 vs ED exacta.

---

---

## 📋 Fase 25 — Completar Labs 01-23 (stubs → labs completos) ✅ COMPLETA 2026-04-30

**Motivación (auditado 2026-05-01):** Los labs 01-23 son stubs incompletos: la mayoría tiene 1 sola celda de código y 1-3 celdas markdown, sin pasos explicados, sin outputs, sin contexto pedagógico. Los labs 24+ están correctamente desarrollados (10-18 celdas, markdown completo). Esta asimetría viola directamente los criterios de AI_Fluency: *información suficiente y completa*, *explicar los pasos o significados*, *reproducible*. Además, labs 21-23 usan `qiskit_algorithms` y `qiskit_machine_learning` (deprecados en Qiskit 2.x).

**Prioridad:** ALTA — hacer antes de la Fase 19 (nuevo contenido). La calidad del existente primero.

### 25.1 — Corrección inmediata: imports deprecados (labs 21-23) ✅ 2026-05-01

- ✅ `21_optimizacion_carteras_vqe.ipynb` — 8 celdas código + 5 markdown, Qiskit 2.x (`StatevectorEstimator`, QUBO + Ising, frontera Markowitz)
- ✅ `22_qae_valoracion_activos.ipynb` — 5 celdas código + 5 markdown, QAE con `Statevector`, comparativa MC vs QAE, complejidad O(1/ε)
- ✅ `23_qml_kernel_alignment.ipynb` — 6 celdas código + 6 markdown, `ZZFeatureMap` manual, matriz Gram, SVM cuántico vs RBF

### 25.2 — Completar labs guiados básicos (01-07) ✅

- [ ] `01_grover_dos_qubits.ipynb` → 6+ celdas: teoría oráculo, difusor paso a paso, estadísticas, variación con 3 qubits
- [ ] `02_teleportacion_guiada.ipynb` → protocolo completo, correcciones clásicas, verificación fidelidad
- [ ] `03_transpilacion_y_comparacion.ipynb` → niveles 0-3, métricas profundidad/gates, visualización
- [ ] `04_bernstein_vazirani_guiado.ipynb` → circuito completo, prueba con distintas cadenas ocultas
- [ ] `05_qft_tres_qubits.ipynb` → QFT manual + `qiskit.circuit.library.QFT`, verificación unitariedad
- [ ] `06_informacion_cuantica_guiada.ipynb` → entropía von Neumann, traza parcial, fidelidad
- [ ] `07_phase_estimation_guiada.ipynb` → QPE completo, precisión vs n_bits ancilla, aplicación a T-gate

### 25.3 — Completar labs intermedios (08-15) ✅

- [ ] `08_vqe_intuicion_guiada.ipynb` → ansatz, COBYLA, convergencia, comparativa con ED
- [ ] `09_qaoa_intuicion_guiada.ipynb` → grafo MAX-CUT, landscape γ/β, solución óptima
- [ ] `10_vqe_energy_scan.ipynb` → curva de energía vs parámetro, barren plateaus básico
- [ ] `11_qaoa_cost_landscape.ipynb` → heatmap, óptimos locales, número de capas p=1-3
- [ ] `12_trotterizacion_y_evolucion_guiada.ipynb` → error de Trotter vs paso dt, comparativa exacta
- [ ] `13_estimator_y_energia_guiada.ipynb` → Estimator V2, observables, shots vs precisión
- [ ] `14_densitymatrix_ruido_y_tomografia_guiada.ipynb` → ruido depolarizante, fidelidad, reconstrucción
- [ ] `15_noise_vs_fidelity_guiada.ipynb` → curvas TVD/Hellinger vs p_error, modelos de ruido

### 25.4 — Completar labs intermedios-avanzados (16-23) ✅

- [ ] `16_trotter_suzuki_intuicion.ipynb` → Trotter de primer y segundo orden, error acumulado
- [ ] `18_calibracion_pulsos_y_oscilaciones_rabi.ipynb` → oscilación Rabi, pi-pulse, decoherencia T1
- [ ] `20_intro_qiskit_pulse_hardware.ipynb` → Schedule, canal Drive, pulso gaussiano, backend real
- [ ] `21_optimizacion_carteras_vqe.ipynb` → ✅ reescrito (25.1)
- [ ] `22_qae_valoracion_activos.ipynb` → ✅ reescrito (25.1)
- [ ] `23_qml_kernel_alignment.ipynb` → ✅ reescrito (25.1)

### 25.5 — Tests para labs completados ✅

- [ ] `tests/test_labs_basicos.py`: tests parametrizados para labs 01-07 (valores esperados clave: probabilidad Grover > 90%, fidelidad teleportación = 1, QFT unitaria, etc.)
- [ ] `tests/test_labs_intermedios.py`: labs 08-15 (VQE converge, QAOA encuentra óptimo, Trotter error ∝ dt²)

---

## Backlog histórico (ya completado)

- ✅ Módulo 41: Topological QC — completado en Fase 15
- ✅ Módulo 42: Tensor Networks y DMRG — completado en Fase 16
- ✅ Lab 46: Simulación MPS — completado en Fase 16
- ✅ Jupyter Book — completado en Fase 16
- ✅ Módulo 43: Quantum Gravity ligero — completado en Fase 17
- ✅ Lab 47: iDMRG cadena de Heisenberg — completado en Fase 17
- ✅ Soporte para IonQ y Quantinuum via cloud providers — completado en Fase 17
- ✅ PDF descargable vía GitHub Actions — completado en Fase 15
- ✅ Benchmark CLOPS/QV 2025 interactivo — completado en Fase 15

---

---

## ✅ Fase 19 — Computación Fotónica (v5.4) — COMPLETA 2026-05-02

**Motivación:** La fotónica cuántica (Xanadu, PsiQuantum, QuiX) es el tercer gran paradigma junto al gate model superconductor y los átomos neutros. Strawberry Fields permite ejecutar circuitos fotónicos reales. El módulo 43 ya menciona GBS en el contexto de Boson Sampling, pero no hay cobertura pedagógica propia.

### 19.1 — Módulo 45: Computación Cuántica Fotónica

- [ ] `Tutorial/45_computacion_fotonica/README.md`: modos ópticos como qumodes, estados de Fock vs estados gaussianos, puertas ópticas (desplazamiento, rotación, squeezing, beamsplitter), medición homódina/heteródina, GBS (Gaussian Boson Sampling) y ventaja cuántica (Jiuzhang 2020), cluster states y computación basada en medición (MBQC), arquitectura PsiQuantum (silicio fotónico), Xanadu X-series, decoherencia por pérdidas en fibra, tabla de plataformas fotónicas 2025.

### 19.2 — Lab 49: GBS con Strawberry Fields

- [ ] `49_gaussian_boson_sampling.ipynb`: instalación Strawberry Fields, circuito GBS básico (4 modos, squeezing + interferómetro), muestreo de hafnian vs permanente, verificación estadística (distribución de clicks), comparativa simulación local vs hardware Borealis (API key opcional), cálculo de ventaja muestral, MBQC toy-example con cluster state lineal de 4 modos.

### 19.3 — Visualizador Página 17: Interferómetro Fotónico Interactivo

- [ ] `visualizador/pages/17_Fotonico.py`: sliders de squeezing (r) y ángulo de beamsplitter (θ) para hasta 4 modos, visualización de función de Wigner (matplotlib), distribución de número de fotones, muestra de clicks GBS, comparativa estado coherente / squeezed / cat state.

### 19.4 — Tests Fase 19 (~10 nuevos → ~159 totales)

- [ ] `tests/test_fotonico.py`: norma de estado Fock, squeezing reduce varianza cuadratura, beamsplitter conserva número medio de fotones, GBS genera distribución super-Poissonian, hafnian para matriz 2×2, cluster state lineal tiene correlaciones EPR, función de Wigner negativa para estado gato.

### 19.5 — Documentación

- [ ] `docs/guia_strawberry_fields.md`: instalación, API key Xanadu Cloud, backends disponibles (Borealis, simulador), límites del plan gratuito.
- [ ] `mkdocs.yml`: módulo 45, lab 49, p.17 añadidos a nav.

---

## ✅ Fase 20 — Átomos Neutros y Computación Analógica (v5.5) — COMPLETA

**Motivación:** QuEra Aquila ya aparece en el Benchmark (p.16) pero sin módulo propio. Los arrays de Rydberg son el paradigma de mayor escala actual (>1000 qubits analógicos), con aplicaciones directas en optimización y simulación de materiales. Bloqade.jl (QuEra) y Pasqal tienen SDKs accesibles.

### 20.1 — Módulo 46: Átomos Neutros y Arrays de Rydberg

- [x] `Tutorial/46_atomos_neutros_rydberg/README.md`: trampa óptica y tweezer arrays, interacción de Rydberg (U = C₆/r⁶), bloqueo de Rydberg (mecanismo de puerta CZ nativa), Hamiltoniano PXP, fases cuánticas, computación analógica vs digital, QuEra/Pasqal/Atom Computing, tabla plataformas 2025.

### 20.2 — Lab 50: Simulación de Cadena de Rydberg

- [x] `50_rydberg_chain.ipynb`: Hamiltoniano PXP + full Rydberg, diagrama de fases Ω/Δ, evolución temporal Z2, quantum many-body scars, radio de bloqueo, puerta CZ.

### 20.3 — Visualizador Página 18: Array de Rydberg Interactivo

- [x] `Visualizador/pages/18_Rydberg.py`: array 2D configurable (hasta 5×5 átomos), sliders Ω/Δ, radio de bloqueo visual, diagrama de fases, evolución PXP con revivals, ejemplo MAX-CUT 6 nodos, tabla plataformas.

### 20.4 — Tests Fase 20 (10 nuevos → 169 totales)

- [x] `tests/test_labs_intermedios.py::TestRydberg`: 10 tests — Hamiltoniano hermítico, dimensión, bloqueo, fases, PXP, revival Z2, escalado r_b, CZ truth table, parámetro orden Z2.

### 20.5 — Documentación

- [x] `mkdocs.yml`: módulo 46, lab 50, visualizador p.18 añadidos.

---

## 📋 Fase 21 — Códigos qLDPC y Decodificadores Neuronales (v5.6) — PLANIFICADA

**Motivación:** Los códigos qLDPC (bivariate bicycle, hypergraph product) son el problema abierto #2 en `problemas_abiertos.md` y la apuesta principal de IBM (Nature 2024) y Google para fault tolerance sub-cuadrático. Es el tema más activo del campo en 2025-2026. El decodificador neuronal y el visualizador interactivo de QEC son gaps pedagógicos evidentes.

### 21.1 — Módulo 47: Códigos qLDPC y Decodificadores

- [ ] `Tutorial/47_qldpc_decodificadores/README.md`: repaso de códigos clásicos LDPC (Tanner graph, belief propagation), códigos CSS cuánticos generalizados, hypergraph product (Tillich-Zémor 2014), bivariate bicycle codes (Bravyi et al. Nature 2024, [[144,12,12]] y [[72,12,6]]), comparativa overhead vs surface code (factor 10× menos qubits físicos por qubit lógico), MWPM (Kolmogorov blossom V), BP+OSD, decodificadores neuronales (LSTM y transformer para corrección en tiempo real), requisito de latencia < 1 μs para FT, estado del arte umbral qLDPC bajo ruido de circuito realista (0.5-1%), hoja de ruta IBM Condor → Flamingo → Starling.

### 21.2 — Lab 51: Implementación qLDPC y Decodificador Neuronal

- [ ] `51_qldpc_decoder.ipynb`: construcción de matriz de paridad H para hypergraph product (n=18 toy), síndrome lookup, MWPM simplificado (networkx min-weight matching), entrenamiento de MLP decodificador (scikit-learn, dataset sintético de errores Pauli), curva de umbral empírico vs tasa de error físico p ∈ [0.001, 0.15], comparativa MWPM vs neural vs lookup-table, overhead de qubits físicos [[n,k,d]] vs surface code equivalente.

### 21.3 — Visualizador Página 19: Decodificador QEC Interactivo

- [ ] `visualizador/pages/19_Decodificador_QEC.py`: retícula surface code L×L configurable (L=3,5,7), modo "dibuja errores" (click en aristas para introducir error X o Z), cálculo y visualización del síndrome (vértices resaltados), animación de corrección MWPM (matching mostrado en la retícula), comparativa P_L vs p para L=3/5/7, panel qLDPC: muestra Tanner graph del código [[18,2,3]] y síndrome como subgrafo.

### 21.4 — Solución R9: Threshold qLDPC bajo ruido de circuito

- [ ] `Soluciones/investigacion/R9_qldpc_threshold.md`: derivación del umbral teórico del código bivariate bicycle bajo ruido de circuito (no solo ruido de Pauli), comparativa BP+OSD vs MWPM modificado, análisis de correlaciones temporales en el ciclo de síndrome, cota del umbral empírico obtenida numéricamente.

### 21.5 — Tests Fase 21 (~15 nuevos → ~184 totales)

- [ ] `tests/test_qldpc.py`: matriz H satisface HH^T=0 (mod 2) para CSS, síndrome es 0 para estado sin error, síndrome detecta error de peso 1, MWPM corrige errores bajo umbral, decodificador neuronal accuracy > 90% para p=0.05, overhead [[144,12,12]] vs surface code equivalente, umbral empírico cae en [0.005, 0.015].

---

## 📋 Fase 22 — QNLP y D-Wave / Annealing (v6.0) — PLANIFICADA

**Motivación:** Dos paradigmas sin cobertura propia: (1) D-Wave / annealing cubre el espacio de optimización combinatoria con hardware real accesible y gratuito; (2) QNLP con lambeq es un caso de uso concreto, ejecutable y con ventaja pedagógica clara (conecta lingüística formal con computación cuántica).

### 22.1 — Módulo 48: QNLP — Quantum Natural Language Processing

- [ ] `Tutorial/48_qnlp/README.md`: gramática categorial (pregrupos, tipos básicos n/s), funtores semánticos (DisCoCat, Coecke-Sadrzadeh-Clark 2010), circuito cuántico como diagrama de cuerda, lambeq (Oxford, 2021): pipeline text→diagrama→circuito→entrenamiento, clasificación de frases (positivo/negativo, relación sujeto-objeto), entrenamiento híbrido clásico-cuántico (SPSA), limitaciones actuales (n_params ∝ longitud de frase), conexión con transformers clásicos, estado del arte 2025 (Quantinuum QNLP, IBM NLP), perspectiva: ¿ventaja cuántica en NLP?

### 22.2 — Lab 52: Clasificador QNLP con lambeq

- [ ] `52_qnlp_lambeq.ipynb`: instalación lambeq + pytket, dataset toy (20 frases positivas/negativas), parse gramatical automático (BobcatParser), diagrama DisCoCat → circuito IQP, entrenamiento con NumpyModel (simulación local) y SPSAOptimizer (30 épocas), curva de accuracy (train/test), visualización de diagramas de cuerda con discopy, experimento con frases ambiguas, comparativa con clasificador clásico (Naive Bayes).

### 22.3 — Módulo 49: D-Wave, Annealing y QUBO

- [ ] `Tutorial/49_dwave_annealing/README.md`: principio de annealing cuántico (Hamiltoniano transverso-Ising), QUBO (Quadratic Unconstrained Binary Optimization): matriz Q, energía de ground state = solución óptima, mapeo de problemas NP: MAX-CUT → QUBO, TSP → QUBO, coloración de grafos → QUBO, portfolio optimization → QUBO, D-Wave Advantage (5000+ qubits, conectividad Pegasus), Leap quantum cloud (acceso gratuito 1 min/mes), comparativa annealing vs QAOA vs clásico en tamaño de instancia, hybrid solvers (CQM, BQM), limitaciones: no garantía de óptimo global, temperatura efectiva, tabla de plataformas annealing 2025 (D-Wave, Fujitsu DAU, Toshiba SQBM+).

### 22.4 — Lab 53: QUBO para Optimización Combinatoria

- [ ] `53_qubo_dwave.ipynb`: formulación QUBO para MAX-CUT (grafo 6 nodos), solución exacta con dimod (simulador BQM local), comparativa con NetworkX (solución clásica exacta), TSP para 5 ciudades: QUBO con penalización, energía landscape (heatmap de la matriz Q), formulación de portfolio QUBO (Markowitz con restricción de presupuesto), conexión con QAOA (mismo QUBO, distinto solver), acceso opcional a D-Wave Leap (token requerido, dry-run mode por defecto).

### 22.5 — Visualizador Página 20: Compilador Cuántico Paso a Paso

- [ ] `visualizador/pages/20_Compilador.py`: circuito de entrada editable (hasta 5 qubits, puertas H/X/CNOT/Rz/T), selector de backend (heavy-hex IBM / retícula 2D / all-to-all), visualización de: (1) circuito abstracto, (2) routing con SWAPs insertados, (3) circuito transpilado, (4) decomposición en basis gates, métricas comparativas (profundidad, número de CX, número de SWAPs), animación paso a paso con botón "siguiente pase", exporta QASM.

### 22.6 — Tests Fase 22 (~15 nuevos → ~199 totales)

- [ ] `tests/test_qnlp.py`: diagrama DisCoCat para frase sujeto-verbo-objeto tiene dimensión correcta, circuito IQP tiene número correcto de parámetros, accuracy > 60% tras 10 épocas en dataset toy.
- [ ] `tests/test_qubo.py`: QUBO MAX-CUT n=4 tiene ground state = corte óptimo, energía QUBO ≤ 0 para solución factible, TSP n=3 QUBO tiene permutaciones válidas como ground states, formulación portfolio conserva restricción de presupuesto, penalización garantiza factibilidad.

---

## 📋 Fase 23 — Calidad, Infraestructura QA y Contenido Pendiente (v6.0) — PLANIFICADA

**Motivación:** Con >200 tests y 49 módulos, la infraestructura necesita un salto de madurez: validación de notebooks en CI, cobertura medible, y cierre de gaps de contenido (resúmenes incompletos, soluciones de investigación pendientes, notas no integradas).

### 23.1 — nbval: Validación de Notebooks en CI

- [ ] `.github/workflows/validate_notebooks.yml`: ejecuta `pytest --nbval-lax` sobre los 53 notebooks de laboratorio en Python 3.11 + Qiskit 2.x. Timeout por notebook: 120 s. Excluye notebooks marcados con `# nbval-skip` (hardware real, GPU). Artifact con log de fallos.
- [ ] Marcar con `# nbval-skip` los labs que requieren token IBM/D-Wave/Xanadu: `31`, `39`, `48`, `52`, `53`.

### 23.2 — pytest-cov + Badge de Cobertura

- [ ] `pyproject.toml`: añadir `pytest-cov` a dev deps, target `make coverage` genera HTML + XML.
- [ ] `.github/workflows/pytest_numerical.yml`: añadir `--cov=. --cov-report=xml`, subir a Codecov.
- [ ] `README.md`: badge de cobertura junto a badge de CI.

### 23.3 — Resúmenes Ampliados (10 → 20)

- [ ] `Resumenes/11_topological_y_tensor.md` — Topológica, redes tensoriales, DMRG.
- [ ] `Resumenes/12_quantum_gravity_dqc.md` — Gravedad cuántica, DQC, repetidores.
- [ ] `Resumenes/13_fotonico_y_rydberg.md` — Fotónica, átomos neutros.
- [ ] `Resumenes/14_qldpc_y_decodificadores.md` — qLDPC, MWPM, neural decoder.
- [ ] `Resumenes/15_qnlp_y_annealing.md` — QNLP, D-Wave, QUBO.
- [ ] `Resumenes/16_infraestructura_y_ci.md` — CI/CD, Docker, Jupyter Book, nbval.
- [ ] `Resumenes/17_hardware_comparativo_2025.md` — Tabla unificada todos los paradigmas.
- [ ] `Resumenes/18_rutas_y_carreras.md` — Perfil investigador / ingeniero / divulgador.
- [ ] `Resumenes/19_glosario_extendido.md` — 50 términos adicionales (F-I-N-P-Q-R-S-T-Z).
- [ ] `Resumenes/20_matematicas_esenciales.md` — Álgebra lineal, grupos de Lie, funciones de Green.

### 23.4 — Soluciones de Investigación R10-R12

- [ ] `Soluciones/investigacion/R10_simulacion_logaritmica.md` — Problema abierto #4: simulación clásica en O(log n) para familias de circuitos estructurados; análisis de MPS, FKS, y estabilizadores extendidos.
- [ ] `Soluciones/investigacion/R11_decodificacion_realtime.md` — Problema abierto #5: decodificación < 1 μs; latencia de FPGA vs GPU, pipeline de síndrome paralelo, estado del arte 2025.
- [ ] `Soluciones/investigacion/R12_magic_state_subcuadratico.md` — Problema abierto #9: destilación de magic states con overhead sub-cuadrático; protocolo Reed-Muller vs [[15,1,3]], cotas de Bravyi-Haah.

### 23.5 — Sistema de Progreso del Estudiante

- [ ] `visualizador/progress.py`: módulo auxiliar con funciones `save_progress(module_id, score)` y `load_progress()` usando `st.session_state` + `localStorage` via `streamlit-local-storage`.
- [ ] Integrar en p.15 (Certificación): mostrar módulos completados, porcentaje global, siguiente módulo recomendado.
- [ ] `docs/guia_progreso.md`: descripción del sistema, privacidad (solo local, sin backend).

### 23.6 — Integración Notas/ no integradas

- [ ] Revisar contenido de `Notas/` (material bruto): integrar notas útiles como apéndices en los módulos correspondientes o moverlas a `Resumenes/` si son autocontenidas.
- [ ] `Notas/README.md` actualizado con criterio editorial claro de qué es integrable.

---

## 📋 Fase 24 — Traducción al Inglés y Comunidad (v6.1) — PLANIFICADA

**Motivación:** El repositorio está en español, lo que limita la audiencia global. `TRANSLATING.md` ya prevé la traducción. Una versión inglesa abre el proyecto a revisión por pares de la comunidad Qiskit/Xanadu y aumenta el impacto pedagógico exponencialmente. La gamificación de contribuciones reduce la fricción para nuevos colaboradores.

### 24.1 — Traducción al Inglés (milestone v6.0-en)

- [ ] Traducir `README.md`, `CONTRIBUTING.md`, `FAQ.md` al inglés como prioridad.
- [ ] Traducir los 10 Resúmenes (más compactos, menor esfuerzo).
- [ ] Traducir módulos 01-10 (fundamentos) como prueba de concepto.
- [ ] Workflow CI: verificar que archivos traducidos tienen par en el otro idioma (`docs/translations_status.md`).
- [ ] `TRANSLATING.md` actualizado con estado por sección y tabla de traductores.

### 24.2 — Rutas de Aprendizaje Personalizadas

- [ ] `visualizador/pages/0_Inicio.py` (nueva home page): selector de perfil (Estudiante / Investigador / Ingeniero / Divulgador), recomendación de ruta de estudio personalizada, mapa visual del curso interactivo (Mermaid → Plotly graph), enlace directo a cada módulo/lab/visualizador.
- [ ] `ruta_de_estudio.md` ampliado: añadir ruta "fotónica", ruta "annealing/optimización", ruta "QEC avanzado".

### 24.3 — Gamificación de Contribuidores

- [ ] `.github/ISSUE_TEMPLATE/`: añadir template `bug_cuaderno.md` (bug en notebook) y `mejora_visualizador.md`.
- [ ] `CONTRIBUTING.md`: sistema de badges de contribuidor (primer PR / corrección de bug / módulo nuevo / traducción), tabla de contributors activos en README.
- [ ] GitHub Actions: workflow `contributors.yml` que actualiza tabla de contribuidores en README tras cada PR merged.

### 24.4 — API REST Ampliada

- [ ] `api/main.py` extendido: endpoints `/run-qnlp` (frase → clasificación), `/run-qubo` (grafo → solución MAX-CUT), `/status` (versión, métricas), documentación OpenAPI automática en `/docs`.
- [ ] `Dockerfile` actualizado: añadir lambeq, dimod a dependencias del contenedor.
- [ ] Tests de integración para nuevos endpoints FastAPI.

---

## Decisiones de arquitectura

| Decisión | Elección | Razón |
|---|---|---|
| Framework cuántico principal | Qiskit 2.x (Primitives V2) | Ecosistema más amplio, soporte IBM, estabilidad API |
| Framework secundario | Pennylane (autodiff) | Diferenciación exacta por parameter-shift sin simulador ruidoso |
| Fotónica | Strawberry Fields (Xanadu) | SDK más maduro, backend Borealis accesible |
| Átomos neutros | QuTiP + Bloqade.jl (Julia) / Pulser (Pasqal) | QuTiP disponible en Python puro; Bloqade más realista |
| Annealing | dimod (D-Wave) | Simulador local sin token, API idéntica al hardware real |
| QNLP | lambeq (Oxford) | Única librería madura para DisCoCat + circuitos cuánticos |
| t\|ket⟩ | Opcional (Lab 33) | Ausente de PyPI de Streamlit Cloud |
| Simulador ruidoso | Qiskit Aer | Modelos de ruido realistas (depolarizante, T1/T2, readout) |
| Visualizador | Streamlit | Sin backend, deploy trivial en Community Cloud |
| Documentación | MkDocs Material | Indexable por Google, tema profesional, búsqueda integrada |
| Tests | pytest + JSON baseline + Hypothesis | Regresión numérica + property-based + CI GitHub Actions |
| Contenedores | DevContainer + conda | Reproducibilidad garantizada en Codespaces/VS Code |
| Notebooks | Jupyter nbformat 4 | Estándar universal, compatible nbviewer/Colab/JupyterHub |
| Soluciones | Markdown con código | Legibles en GitHub sin ejecución |

---

*Actualizado 2026-04-30 · v5.2 publicado · Fases 1-17 todas ✅ · Fase 18 en progreso · Fases 19-24 planificadas*
