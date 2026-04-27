# Changelog

Todos los cambios relevantes de este proyecto se documentan en este archivo.

El formato sigue una adaptacion simple de Keep a Changelog y usa versionado semantico solo como referencia organizativa mientras el repositorio madura.

## [2.1.0] - 2026-04-28

### Added (Fase 16 — Tensor Networks y Jupyter Book · v5.1)

- **Módulo 42** `Tutorial/42_tensor_networks/README.md`: MPS (representación, parámetros, ejemplos exactos), notación diagramática, descomposición de Schmidt, area law de Hastings (1D gapped), operaciones MPS (forma canónica, truncamiento SVD), DMRG (barridos two-site), TEBD (Trotter + cadena XX), más allá de 1D (PEPS/MERA/TTN), conexión con QC (dequantización, VQE vs DMRG).
- **Lab 46** `46_mps_tensor_networks.ipynb`: implementación MPS desde cero con numpy — SVD recursiva, reconstrucción exacta, truncamiento con fidelidad, entropía de entrelazamiento por corte, TEBD cadena XX con propagación de magnetización y crecimiento de entrelazamiento, comparativa parámetros MPS vs estado completo.
- **Jupyter Book** `_config.yml` + `_toc.yml`: versión offline navegable del curso — 7 secciones, módulos 01-42, labs 32-46, launch buttons para Binder/Colab.
- **Workflow Jupyter Book** `.github/workflows/build_jupyterbook.yml`: build automático en push a main (Tutorial/Cuadernos/docs cambiados), artifact HTML de 30 días.
- **14 tests nuevos** `tests/test_tensor_networks.py`: χ producto=1, GHZ χ=2 S=1ebit, reconstrucción exacta, fidelidad monótona en χ, entropía no negativa y acotada, Σλ²=1, χ_max ≤ 2^(n//2), TEBD norma conservada. **Total: 115 tests**.
- **PLAN_EXPANSION.md**: Fase 16 añadida ✅, métricas v5.1 actualizadas, backlog reorganizado para Fase 17.

### Fixed

- `mps_from_statevector`: truncamiento de valores singulares near-zero con tolerancia relativa para bond dimension exacto en estados producto y GHZ.

## [2.0.0] - 2026-04-28

### Added (Fase 15 — Topological QC, Property Tests y PDF CI · v5.0)

- **Módulo 41** `Tutorial/41_topological_qc`: Computación Cuántica Topológica completa — anyones, código tórico de Kitaev, operadores Av/Bp, espacio lógico (2 qubits por toro), umbral ~10.9%, anyones de Fibonacci, qubits de Majorana (Microsoft 2025).
- **Lab 45** `45_toric_code.ipynb`: Simulación Qiskit del código tórico L×L — verificación [Av,Bp]=0 para todos los pares, estado de código vía proyector gauge, operadores lógicos X̄/Z̄, introducción/detección/corrección de errores X y Z, error lógico indetectable por síndrome, escalado P_L vs L.
- **Página 16** `16_Benchmark_Hardware.py`: Benchmark interactivo CLOPS/QV/T1/T2 de 6 plataformas 2025 (IBM Heron/Eagle, Google Willow, Quantinuum H2, IonQ Forte, QuEra Aquila); 4 tabs de visualización; calculadora de overhead FT para código de superficie.
- **Workflow PDF** `.github/workflows/build_pdf.yml`: generación automática de PDF (MkDocs + WeasyPrint) en cada release de GitHub; adjunta PDF al release y como artifact de 90 días.
- **Property-based tests** `tests/test_property_based.py`: 25 tests con Hypothesis — estados cuánticos, algebra de Pauli, código tórico (paridad de aristas, síndromes), principio variacional, PAC learning, BB84, barren plateaus, teleportación, umbral tórico. Total: **101 tests**.
- **`hypothesis>=6.100`** añadido a `requirements.txt`, `environment.yml`, `pyproject.toml[dev]`.
- **`mkdocs.yml`**: módulo 41, lab 45, sección "Topológica" en nav; plugin `pdf-export` configurado con `ENABLE_PDF_EXPORT`.
- **`pyproject.toml`**: versión `4.0.0` → `5.0.0`.

### Fixed

- Bug en constructor de plaquetas del código tórico: borde derecho era `v_edge(pi, pj-1)` → corregido a `v_edge(pi, pj+1)` (Lab 45 y tests).
- Backlog: ítems de PDF y Benchmark marcados como completados.

## [1.4.0] - 2026-04-27

### Changed (Fase 14 — Revisión y QA v4.0)

- **Workflow desactivado:** `test_code_snippets.yml` movido a `workflow_dispatch` (solo manual) — eliminados triggers automáticos en push/PR.
- **`scikit-learn>=1.4,<2.0`** añadido a `requirements.txt`, `environment.yml` y `pyproject.toml` (usado en labs 42 y 43).
- **Página 15** `15_Certificacion.py`: añadido `show_tour()` con 5 pasos de guía interactiva.
- **`tests/baseline.json`** actualizado a v1.3.0: entradas para labs 42-44 (DQC, QML teórico, Hubbard).
- **PLAN_EXPANSION.md**: Fases 13 y 14 marcadas ✅ con checkmarks detallados.
- **QA verificado:** 76 tests passing, 54 notebooks JSON válidos, 45 refs MkDocs sin rotos, 15 páginas Streamlit con sintaxis válida.

## [1.3.0] - 2026-04-27

### Added (Fase 13 — Ecosistema Completo v4.0)

- **Examen de certificación** `Ejercicios/examen_certificacion.md`: 50 preguntas estructuradas (básico/intermedio/avanzado/investigación) con respuestas anotadas, explicaciones y referencias a módulos.
- **Autoevaluación modular** `Ejercicios/autoevaluacion_modular.md`: 123 competencias distribuidas en 23 módulos (01-40) con tabla de progreso y criterios de certificación.
- **Visualizador página 15** `15_Certificacion.py`: quiz interactivo de 20 preguntas con banco de 20 preguntas representativas, badge SVG descargable parametrizado (nombre, fecha, nivel).
- **Lab 42** `42_dqc_avanzada.ipynb`: entanglement swapping (4 qubits), Blind QC (demostración de uniformidad de δ), BB84 con/sin Eve (curva QBER), teletransportación vs canal ruidoso (F vs p, límite clásico 2/3).
- **Lab 43** `43_qml_teorico.ipynb`: PAC learning (complejidad de muestra finita + VC-dim), VC-dim de PQC, barren plateaus analítico + empírico, dequantization (Tang 2019), QAE vs Monte Carlo (speedup cuadrático).
- **Lab 44** `44_hubbard_vqe.ipynb`: Hamiltoniano de Hubbard via Jordan-Wigner (L=2, 4 qubits), VQE con ansatz HEA, gap de carga, diagrama de fase metal-aislante Mott.
- **Guía IBM Quantum** `docs/guia_ibm_quantum.md`: configuración QiskitRuntimeService, gestión de colas, mitigación M3, límites plan gratuito 2025.
- **Error rates 2025** `docs/error_rates_2025.md`: tabla comparativa IBM/Google/IonQ/Quantinuum con T1/T2/error 1Q/2Q/readout/QV/CLOPS, hito Willow, umbral FT.
- **Script hardware** `run_on_hardware.py`: CLI con warm-start simulador, VQE H₂ en IBM Quantum real, dry-run mode, export JSON.
- **API FastAPI** `api/main.py`: endpoints `/run-circuit` (QASM2+ruido), `/run-vqe` (H₂ por distancia), `/run-grover` (n-qubits, k estados marcados); respuestas tipadas Pydantic.
- **Docker** `Dockerfile` + `docker-compose.yml`: servicios api (8000) + streamlit (8501).
- **GitHub templates** `.github/ISSUE_TEMPLATE/ejercicio_educativo.md`: plantilla para proponer ejercicios con enunciado, solución, nivel y checklist.
- **Guía de traducción** `TRANSLATING.md`: tabla de estado por idioma, terminología ES→EN estándar, flujo de PR para contribuidores.
- **11 tests nuevos** (Fase 13): PAC learning, VC-dim, barren plateau, entanglement swapping, BQC δ uniforme, BB84 sin/con Eve, Hubbard E0<0, Grover API, QAE speedup, teleportación vs límite clásico. Total: 76 tests.
- **PLAN_EXPANSION.md** actualizado: Fase 13 ✅ completa con checkmarks, métricas v4.0 (44 labs, 15 páginas, 76 tests).

## [1.2.0] - 2026-04-27

### Added (Fase 12 — Aplicaciones Industriales Extendidas)

- **Lab 38** `38_quantum_finance_qae.ipynb`: QAE para Monte Carlo cuántico, portfolio QAOA media-varianza, Quantum Risk Analysis con CVaR.
- **Lab 39** `39_quimica_hardware_zne.ipynb`: VQE H₂ con AerSimulator mock + ZNE (circuit folding + Richardson), comparativa ZNE vs PEC, curva de disociación H₂.
- **Lab 40** `40_qml_datos_reales.ipynb`: ZZFeatureMap manual, kernel cuántico vs RBF/lineal en moons/circles/blobs, Kernel Target Alignment (KTA), decision boundaries.
- **Lab 41** `41_advantage_cuantica.ipynb`: RCS y Cross-Entropy Benchmarking, Boson Sampling (permanente de Ryser), límites MPS (bond dimension χ), análisis del advantage cuántico 2025.
- **Soluciones R5-R8** completas con código ejecutable: QFI sensing (GHZ vs SQL, Cramér-Rao, dephasing), kernel cuántico vs clásico, umbral fault-tolerant (repetición + surface code + magic state distillation), complejidad cuántica y lower bounds (Grover óptimo, dequantization, crossover clásico-cuántico).
- **Visualizador página 14** `14_Finance_QML.py`: portafolio QAOA interactivo con frontera de Markowitz, kernel cuántico ZZFeatureMap con heatmap y KTA en tiempo real.
- **MkDocs** actualizado: labs 32-41, módulos 38-40, ejercicios de investigación R1-R8 en el índice de navegación.
- **PLAN_EXPANSION.md** v3.5: Fases 1-12 marcadas como ✅ completas con checkmarks por ítem.

## [1.1.0] - 2026-04-27

### Added (Fase 11 — Soluciones + Labs 35-37 + CI baseline)

- **Lab 35** `35_computacion_adiabatica_qaoa.ipynb`: brecha adiabática, Trotter, fidelidad vs T, QAOA p=1-4 en MAX-CUT.
- **Lab 36** `36_nuevos_qubits_fluxonium_majorana.ipynb`: transamón vs Fluxonium, tabla plataformas 2024-2028, overhead surface code.
- **Lab 37** `37_redes_cuanticas_qkd.ipynb`: BB84 + Eva, E91 CHSH, purificación BBPSSW, repeaters cuánticos, MDI-QKD/TF-QKD.
- **Soluciones R1-R4** con código ejecutable: Chebyshev QSVT, block-encoding, barren plateaus + identity-init, ZNE Richardson + PEC.
- `tests/baseline.json`: valores de referencia numérica para 15 módulos.
- `@pytest.mark.slow` en 13 tests pesados; `make test-fast` excluye lentos.
- **Visualizador página 13** `13_Quantum_Walk.py`: DTQW/CTQW interactivo, moneda seleccionable, σ(t) balístico vs difusivo, exportar PNG.

## [1.0.0] - 2026-04-27

### Added (Fase 10 — QSVT, Sensing, Compilación)

- **Módulos 38-40**: Quantum Sensing y Metrología (QFI, Cramér-Rao, magnetometría NV), Compilación Cuántica Avanzada (Qiskit passes, t|ket⟩, Solovay-Kitaev), QSVT y Block-Encoding (aproximación Chebyshev, HHL, simulación hamiltoniana óptima).
- **Lab 32** `32_quimica_avanzada_vqe_uccsd.ipynb`: VQE-UCCSD H₂ y LiH, curva de energía potencial vs FCI, mapeos JW/BK/Paridad, coste de medición QWC.
- **Lab 33** `33_compilacion_tket_qiskit.ipynb`: Qiskit niveles 0-3, descomposición KAK, síntesis de unitarias, comparativa con t|ket⟩ (opcional).
- **Lab 34** `34_quantum_walk_dtqw_ctqw.ipynb`: DTQW balístico, distintas monedas, CTQW en grafo de línea/hipercubo/Petersen, búsqueda cuántica en K_N con O(√N).
- **Visualizador páginas 11-12**: Estimador de Recursos FT (surface code, distilación T, viabilidad por algoritmo), Landscape VQE/QAOA (barren plateaus, comparativa COBYLA/SLSQP).
- **Ejercicios de investigación** `Ejercicios/ejercicios_investigacion.md`: 8 problemas de frontera (QSVT, block-encoding, barren plateaus, ZNE, sensing, QML kernel, fault tolerance, advantage cuántica).
- **Tests**: 31 → 48 casos (módulos 38-40, QFI/HL, KAK, DTQW/CTQW balístico, Chebyshev).
- **Infraestructura**: `environment.yml` (conda), `Makefile`, `pyproject.toml` (PEP 517 + extras), `.devcontainer/devcontainer.json` (GitHub Codespaces/VS Code).
- **PLAN_EXPANSION.md**: documento vivo con historial de fases (1-10), Fase 11 en progreso y Fases 12-13 planificadas.

### Fixed

- Visualizador página 9 (Simulador Ruidoso): `NoiseModel` aplicaba error de 2 qubits a `ccx` (3 qubits) → `NoiseError` al cargar. Añadido error depolarizante de 3 qubits para `ccx`.
- Páginas 10, 11, 12: `_TOUR_STEPS` en formato de tuplas incompatible con `tour_guide.show_tour` (espera dicts `{"title", "body"}`). Convertido en las tres páginas.

---

## [0.9.0] - 2026-04-24

### Changed (reescritura masiva de artículos)

- **37 artículos reescritos** desde stub (< 30 líneas) a artículos completos (~150-200 líneas) con formalismo matemático, código Qiskit 2.0 y ejercicios sugeridos.
- Módulos afectados: 05, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27.
- Todo el código actualizado a la API moderna de Qiskit 2.0 (`StatevectorSampler`, `StatevectorEstimator`, `SparsePauliOp`).

### Added

- **Módulo 22 (recursos cuánticos):** teoría de coherencia (medidas ℓ₁, entropía relativa), entropía de entrelazamiento, no-clonación (demostración por linealidad), monogamia CKW, principio de Landauer cuántico, cota de Holevo.
- **Módulo 23 (hardware físico):** Hamiltoniano del transmón, circuit QED dispersivo, Cross-Resonance, tablas de parámetros 2024, comparativa completa de 5 arquitecturas (superconductores, iones, Rydberg, NV, fotónica).
- **Módulo 24 (control de pulsos):** marco rotatorio, Hamiltoniano de drive, mezclador IQ, envolventes DRAG, experimento de Rabi/Ramsey, Qiskit Pulse completo.
- **Módulo 25 (PQC):** LWE, estándares NIST 2024 (ML-KEM/Kyber, ML-DSA/Dilithium, SLH-DSA/SPHINCS+), comparativa QKD vs PQC.
- **Módulo 26 (ZX-Calculus):** arañas Z/X, reglas de reescritura, phase gadgets, código PyZX con circuito de demostración.
- **Módulo 27 (internet cuántico):** BB84 con análisis de QBER, E91 con CHSH, entanglement swapping (circuito Qiskit), purificación DEJMPS, memorias cuánticas, Blind Quantum Computing, estado del arte 2024.

### Fixed

- Eliminados todos los stubs con contenido incoherente o ilegible en módulos 22-27.
- Navegación bidireccional verificada en todos los artículos reescritos.

## [0.8.0] - 2026-04-22

### Added
- Nueva herramienta: [visualizador/app.py](visualizador/app.py) (Aplicación Streamlit para visualización interactiva de la Esfera de Bloch y ruido).
- Bloque 17: Cálculo Gráfico y ZX-Calculus (2 artículos sobre la optimización gráfica de circuitos).
- Bloque 18: Comunicaciones e Internet Cuántico (2 artículos sobre repetidores y protocolos de red).
- Ampliación del tutorial hasta alcanzar los 66 artículos finales comprobados.

## [0.7.0] - 2026-04-22

### Added
- Expansión de Verticales Industriales: Finanzas (Markowitz/QAE), QML Avanzado (Kernels/QNN) y Ciencia de Materiales.
- 5 nuevos artículos técnicos de alta profundidad en el bloque 12 de aplicaciones.
- 3 nuevos laboratorios prácticos sobre optimización de carteras, pricing y alineación de kernels.
- Renumeración completa del tutorial hasta alcanzar los 62 artículos temáticos.

## [0.5.0] - 2026-04-21

### Added
- Finalización de los 52 artículos del tutorial con profundidad técnica y matemática.
- Nueva biblioteca de Soluciones Modulares (10 artículos organizados por bloques).
- Verificación de navegación bidireccional en todo el repositorio.
- Corrección de rutas absolutas en archivos de documentación raíz.
- Ampliación de laboratorios prácticos (27 cuadernos Jupyter en total).

### Fixed
- Corrección de rutas locales absolutas en `README.md`, `lecturas_recomendadas.md` y `Qiskit_en_este_repositorio.md`.


## [Unreleased]

### Planned

- Ampliar `README.md` con objetivos, alcance y estructura del proyecto.
- Crear una arquitectura inicial de contenidos para teoria y practica.
- Incorporar modulos introductorios sobre qubits, puertas, medicion y circuitos.
- Añadir cuadernos Jupyter para ejemplos y problemas resueltos.

### Added

- `bitacora.md` para registrar el avance editorial y tecnico del proyecto.
- `changelog.md` para centralizar el historial de cambios relevantes.
- Directorio `Tutorial/` con primeros articulos sobre fundamentos de computacion cuantica.
- Directorio `Cuadernos/` con notebooks Jupyter de ejemplos y problemas resueltos.
- Articulos iniciales sobre qubits, superposicion, medicion, puertas, circuitos, entrelazamiento y Qiskit.
- Cuadernos iniciales para qubits, puertas basicas y estados de Bell.
- Nuevos articulos sobre algebra lineal minima y algoritmos cuanticos introductorios.
- Nuevos notebooks sobre esfera de Bloch, producto tensorial, cambios de base y Deutsch-Jozsa.
- Nuevos articulos sobre simuladores de Qiskit, resultados, transpilacion, ruido y hardware.
- Fuerte ampliacion de la biblioteca de notebooks de Qiskit.
- `referencias.md` con enlaces oficiales, bibliografia base y recursos recomendados.
- Estructura modular en `Tutorial/` con bloques de fundamentos, algoritmos, ruido/hardware y apendices.
- `Imagenes/` y `Notas/` como directorios de apoyo al crecimiento del proyecto.
- `Cuadernos/laboratorios/` con laboratorios guiados para Grover, teleportacion y transpilacion.
- Modulos `08_informacion_cuantica/` y `09_correccion_errores/`.
- `roadmap.md` como hoja de ruta del proyecto.
- `10_qiskit_avanzado/` con primitives, operadores y modelos de ruido.
- `Resumenes/` con materiales breves de repaso.
- `05_phase_estimation.md` dentro del bloque de algoritmos.
- `Ejercicios/` con practica clasificada por nivel.
- Nuevos cuadernos sobre `Sampler`, `Estimator` y `phase estimation`.
- `FAQ.md` y `Soluciones/`.
- `11_algoritmos_variacionales/` y `13_limites_actuales_y_realismo/`.
- `12_aplicaciones/` y `14_surface_codes_y_horizonte_fault_tolerant/`.
- `estructura_del_proyecto.md` y `CONTRIBUTING.md`.
- Nuevos laboratorios guiados para `phase estimation`, `VQE` y `QAOA`.
- Resumenes adicionales sobre algoritmos e informacion cuantica.
- Ampliacion del bloque de surface codes con fault tolerance.
- Nuevos laboratorios y ejemplos para reforzar VQE, QAOA y observables con `SparsePauliOp`.
- Ampliacion del modulo de aplicaciones con simulacion digital y Hamiltonianos sencillos.
- `ruta_de_estudio.md` y `tabla_cobertura.md`.
- Nuevo modulo `15_hamiltonianos_y_evolucion_temporal/`.
- Ejemplos adicionales sobre counts, histogramas y comparacion ideal frente a ruidoso.
- Nuevo modulo `16_canales_cuanticos_y_ruido/`.
- Ampliacion fuerte del bloque `15_hamiltonianos_y_evolucion_temporal/`.
- Nuevos cuadernos sobre observables, valores esperados, canales cuanticos y trotterizacion.
- Secciones de ejercicios sugeridos y material asociado en los articulos nuevos.
- Nuevo modulo `17_medicion_avanzada_y_observables/`.
- Nuevos cuadernos sobre `Estimator`, Hamiltonianos sencillos y POVM.
- Nuevo laboratorio guiado sobre energia esperada.
- Nuevo resumen sobre Hamiltonianos, ruido y medicion avanzada.
- `soluciones_avanzadas_seleccionadas.md`.
- Nuevo modulo `18_complejidad_cuantica/`.
- Nuevo modulo `19_tomografia_y_caracterizacion/`.
- Nuevos cuadernos sobre BQP, complejidad, tomografia y fidelidad conceptual.
- Nuevo laboratorio sobre matrices de densidad, ruido y tomografia.
- Nuevos resumenes sobre variacionales/aplicaciones y complejidad/tomografia.
- `glosario.md` y `lecturas_recomendadas.md`.
- Nuevo modulo `20_simulacion_cuantica_avanzada/`.
- Nuevos cuadernos sobre simulacion hamiltoniana y fidelidad frente a ruido.
- Nuevos laboratorios sobre ruido/fidelidad y Trotter-Suzuki.
- Refuerzo pedagogico en articulos avanzados con prerequisitos, objetivos y errores comunes.
- `Qiskit_en_este_repositorio.md` y `mapa_visual_del_curso.md`.
- Nuevo modulo `21_open_quantum_systems/`.
- Nuevo cuaderno introductorio sobre sistemas abiertos.
- Nuevos cuadernos sobre shots, `DensityMatrix`, sistemas abiertos y observables distintos.
- `preguntas_frecuentes_avanzadas.md`.
- Nuevo modulo `22_recursos_cuanticos/`.
- Nuevos cuadernos sobre coherencia, entrelazamiento y no-clonacion.
- Nuevo resumen sobre recursos cuanticos.

## [0.1.0] - 2026-04-19

### Added

- Base documental inicial del proyecto con `README.md`, `bitacora.md` y `changelog.md`.

### Notes

- Esta version marca el arranque formal del repositorio como proyecto estructurado.
- El contenido tecnico todavia esta pendiente de desarrollo.
