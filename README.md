# Computación Cuántica: Teoría y Práctica (v6.3)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://computacioncuantica-legalintermedia.streamlit.app/)
[![Tests](https://github.com/LegalIntermediaSL/ComputacionCuantica/actions/workflows/pytest_numerical.yml/badge.svg)](https://github.com/LegalIntermediaSL/ComputacionCuantica/actions)
[![codecov](https://codecov.io/gh/LegalIntermediaSL/ComputacionCuantica/branch/main/graph/badge.svg)](https://codecov.io/gh/LegalIntermediaSL/ComputacionCuantica)

Este repositorio es un proyecto educativo de alto nivel diseñado para acompañar al estudiante desde los fundamentos más básicos del qubit hasta las fronteras de la investigación actual en hardware, algoritmos de industria y comunicaciones cuánticas.

## Puntos Destacados

- **49 Módulos Tutoriales:** Teoría completa con LaTeX — desde qubits hasta qLDPC, QNLP, Rydberg, fotónica y tolerancia a fallos.
- **53 Laboratorios + 22 Guiados:** 53 labs completos con Qiskit 2.x + 22 cuadernos paso a paso en `Cuadernos/guiados/`.
- **55+ Ejercicios progresivos:** Básicos, intermedios, avanzados e **investigación** (12 soluciones R1-R12) + examen de certificación.
- **Visualizador Interactivo:** Aplicación Streamlit de **21 páginas** — [ver online](https://computacioncuantica-legalintermedia.streamlit.app/).
- **314 Tests pytest:** Regresión numérica + property-based (Hypothesis) + nbval CI + fotónica, qLDPC, QNLP, QUBO, baseline JSON, `@pytest.mark.slow`.
- **20 Resúmenes:** Material de repaso rápido para cada bloque temático (módulos 01-49).
- **Multi-provider:** IonQ (Braket/directo), Quantinuum (Azure), Pasqal — ZNE multi-provider incluido.
- **API REST FastAPI:** Endpoints `/run-circuit`, `/run-vqe`, `/run-grover` — Docker incluido.
- **PDF descargable:** Generación automática vía GitHub Actions en cada release.
- **Fault-Tolerant:** QSVT, HHL, QAE, Shor, qLDPC (bivariate bicycle [[144,12,12]]), surface code umbral ~1%.

## Visualizador Cuántico Interactivo

🌐 **[Acceso online](https://computacioncuantica-legalintermedia.streamlit.app/)** — sin instalación.

Para lanzarlo localmente:
```bash
pip install -r requirements.txt
streamlit run visualizador/app.py
```

Páginas disponibles:
1. **Esfera de Bloch** — estado qubit con canales de ruido y trayectoria 3D
2. **Algoritmos paso a paso** — Deutsch-Jozsa, Bernstein-Vazirani, Grover
3. **Canales y Ruido** — simulación de decoherencia con fidelidad Bures
4. **Hardware Dashboard** — comparativa de 10 procesadores reales (2019-2024)
5. **VQE / QAOA** — optimización variacional con comparativa COBYLA / SPSA / Nelder-Mead
6. **Corrección de Errores** — código de repetición y Shor con curva de protección
7. **Compositor de Circuitos** — 15 puertas, hasta 4 qubits, exporta código Qiskit
8. **Tomografía** — reconstrucción de estado 1-2q con matriz χ
9. **Simulador Ruidoso** — comparativa ideal vs ruidoso con TVD/Hellinger/XEB
10. **Algoritmos Completos** — simulación paso a paso con amplitudes complejas
11. **Estimador de Recursos FT** — surface code, magic states, viabilidad por algoritmo
12. **Landscape VQE/QAOA** — barren plateaus, comparativa de optimizadores
13. **Quantum Walk** — DTQW/CTQW interactivo, propagación balística vs difusiva, 4 monedas
14. **Finance & QML** — Portfolio QAOA + frontera Markowitz, kernel cuántico vs RBF
15. **Certificación** — Quiz interactivo 20 preguntas, badge SVG descargable
16. **Benchmark Hardware** — Comparativa CLOPS/QV/T1/T2 2025, calculadora overhead FT
17. **Interferómetro Fotónico** — squeezing, beamsplitter, función de Wigner, GBS
18. **Array de Rydberg** — PXP, diagrama de fases, MAX-CUT analógico
19. **Decodificador QEC** — surface code interactivo, MWPM, curvas de umbral
20. **Compilador Cuántico** — transpilación Heavy-Hex, métricas, optimización niveles 0-3
21. **Inicio / Rutas** — selector de perfil, mapa del curso, progreso del estudiante

## Mapa del Curso e Índices

- [**Indice Maestro del Tutorial**](Tutorial/README.md): Ruta lineal de los 70+ artículos.
- [**Mapa Visual del Curso**](Tutorial/indice_general.md): Diagrama del flujo de aprendizaje por familias temáticas.
- [**Ruta de Estudio por Perfil**](ruta_de_estudio.md): Guía personalizada para programadores, físicos o curiosos.

## Estructura del Repositorio

- `Tutorial/`: 49 módulos teóricos con LaTeX y ejemplos Qiskit.
- `Cuadernos/laboratorios/`: 53 labs completos (Qiskit 2.x, 10-20 celdas).
- `Cuadernos/guiados/`: 15 notebooks introductorios paso a paso (sin dependencias pesadas).
- `visualizador/`: Aplicación Streamlit 21 páginas interactivas.
- `Soluciones/`: R1-R12 — soluciones a problemas de frontera.
- `Ejercicios/`: Práctica clasificada por nivel + examen de certificación.
- `Resumenes/`: 20 resúmenes de repaso rápido (módulos 01-49).
- `docs/`: Guías prácticas (IBM Quantum, GPU, multiprovider, progreso, Strawberry Fields).
- `api/`: FastAPI REST endpoints + Docker.
- `BITACORA.md`: Registro cronológico de sesiones de desarrollo.

## Tabla de Cobertura Global

| Bloque | Estado | Contenido | Práctica |
|---|---|---|---|
| **01-04. Fundamentos y Qiskit** | ✅ Completo | Qubits, Puertas, Entrelazamiento | Labs de base |
| **05. Algoritmos Clásicos** | ✅ Completo | Deutsch-Jozsa, Grover, QFT, Shor | Labs avanzados |
| **06-10. Hardware y Ruido** | ✅ Completo | T1/T2, Mitigación, Transmones, Pulse | Labs de hardware |
| **11-12. Aplicaciones e Industria** | ✅ Completo | Finanzas, QML, Química, Materiales | Labs industriales |
| **15-21. Teoría Avanzada** | ✅ Completo | Hamiltonianos, Canales, Sistemas Abiertos | Labs de simulación |
| **26-27. Fronteras Modernas** | ✅ Completo | ZX-Calculus, Internet Cuántico | Teoría de vanguardia |
| **28. Aplicaciones Emergentes** | ✅ Completo | QV, CLOPS, Mirror Circuits, Willow 2024 | Ejercicios avanzados |
| **29. Fault-Tolerant Computing** | ✅ Completo | Umbral, Magic States, Hoja de Ruta 2033 | Soluciones |

## Ejercicios

- [Básicos (15)](Ejercicios/ejercicios_basicos.md) — Puertas, circuitos, medición, entrelazamiento
- [Intermedios (12)](Ejercicios/ejercicios_intermedios.md) — Algoritmos, QFT, estimación de fase, VQE
- [Avanzados (10)](Ejercicios/ejercicios_avanzados.md) — Corrección de errores, QAOA, QML, mitigación
- [Investigación (8)](Ejercicios/ejercicios_investigacion.md) — QSVT, block-encoding, barren plateaus, sensing, QML kernel, fault tolerance, advantage cuántica

## Infraestructura

```bash
# Conda (recomendado)
conda env create -f environment.yml
conda activate qc-edu

# pip
pip install -e ".[dev]"

# Tests
make test          # todos los tests (314)
make test-fast     # tests rápidos (excluye @slow)

# Visualizador
make streamlit
```

[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/LegalIntermediaSL/ComputacionCuantica)

---
*Mantenido como recurso abierto para la comunidad hispana de computación cuántica.*
