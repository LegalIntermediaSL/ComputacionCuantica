# Computación Cuántica: Teoría y Práctica (v5.2)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://computacioncuantica-legalintermedia.streamlit.app/)
[![Tests](https://github.com/LegalIntermediaSL/ComputacionCuantica/actions/workflows/pytest_numerical.yml/badge.svg)](https://github.com/LegalIntermediaSL/ComputacionCuantica/actions)

Este repositorio es un proyecto educativo de alto nivel diseñado para acompañar al estudiante desde los fundamentos más básicos del qubit hasta las fronteras de la investigación actual en hardware, algoritmos de industria y comunicaciones cuánticas.

## Puntos Destacados

- **90+ Artículos Técnicos:** Una secuencia pedagógica completa con rigor matemático (LaTeX), módulos 1-43 (incluye Topological QC, Tensor Networks, AdS/CFT y gravedad cuántica).
- **47 Laboratorios Jupyter:** Práctica real con Qiskit 2.0 (Primitives V2), desde Grover hasta QSVT, DQC, QML, iDMRG, MPS/TEBD, Código Tórico y Finance cuántica.
- **55+ Ejercicios progresivos:** Básicos, intermedios, avanzados e **investigación** (8 problemas de frontera con soluciones completas R1-R8) + examen de certificación (50 preguntas).
- **Visualizador Interactivo:** Aplicación Streamlit de **16 páginas** — [ver online](https://computacioncuantica-legalintermedia.streamlit.app/).
- **129 Tests pytest:** Suite con regresión numérica + property-based tests (Hypothesis) + iDMRG/MPS/tórico, baseline JSON y marcadores `@pytest.mark.slow`.
- **Multi-provider:** Guía completa para IonQ (Braket/directo), Quantinuum (Azure), Pasqal — ZNE multi-provider incluido.
- **API REST FastAPI:** Endpoints `/run-circuit`, `/run-vqe`, `/run-grover` — Docker incluido.
- **PDF descargable:** Generación automática vía GitHub Actions en cada release.
- **Algoritmos Fault-Tolerant:** QSVT, HHL, QAE, Shor completo, distilación de magic states, **código tórico** con umbral ~10.9%.
- **Aplicaciones industriales:** Quantum Finance (QAOA portfolio), QML (kernel cuántico), Advantage cuántica (RCS, Boson Sampling).

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

## Mapa del Curso e Índices

- [**Indice Maestro del Tutorial**](Tutorial/README.md): Ruta lineal de los 70+ artículos.
- [**Mapa Visual del Curso**](Tutorial/indice_general.md): Diagrama del flujo de aprendizaje por familias temáticas.
- [**Ruta de Estudio por Perfil**](ruta_de_estudio.md): Guía personalizada para programadores, físicos o curiosos.

## Estructura del Repositorio

- `Tutorial/`: El núcleo teórico (29 bloques temáticos, ~70 artículos).
- `Cuadernos/`: Laboratorios guiados y ejemplos de código.
- `visualizador/`: Aplicación interactiva Streamlit (14 páginas).
- `Soluciones/`: Biblioteca de problemas resueltos por bloques temáticos.
- `Ejercicios/`: Práctica clasificada por niveles de dificultad.
- `Resumenes/`: Material de repaso rápido para cada sección.

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
make test          # todos los tests (76)
make test-fast     # tests rápidos (excluye @slow)

# Visualizador
make streamlit
```

[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/LegalIntermediaSL/ComputacionCuantica)

---
*Mantenido como recurso abierto para la comunidad hispana de computación cuántica.*
