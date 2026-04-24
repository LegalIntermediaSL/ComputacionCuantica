# Changelog

Todos los cambios relevantes de este proyecto se documentan en este archivo.

El formato sigue una adaptacion simple de Keep a Changelog y usa versionado semantico solo como referencia organizativa mientras el repositorio madura.

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
