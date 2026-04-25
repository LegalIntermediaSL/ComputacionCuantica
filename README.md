# Computación Cuántica: Teoría y Práctica (v1.0)

Este repositorio es un proyecto educativo de alto nivel diseñado para acompañar al estudiante desde los fundamentos más básicos del qubit hasta las fronteras de la investigación actual en hardware, algoritmos de industria y comunicaciones cuánticas.

## Puntos Destacados

- **70+ Artículos Técnicos:** Una secuencia pedagógica completa con rigor matemático (LaTeX).
- **30+ Laboratorios Jupyter:** Práctica real con Qiskit 2.0 (Primitives V2).
- **37 Ejercicios progresivos:** Básicos, intermedios y avanzados con código ejecutable y pistas graduadas.
- **Visualizador Interactivo:** Aplicación Streamlit de 7 páginas para explorar la física cuántica de forma visual.
- **Especialización Industrial:** Módulos dedicados a Finanzas, QML Avanzado y Ciencia de Materiales.
- **Hardware y Control:** Deep-dive en Transmones, Iones Atrapados y Qiskit Pulse.
- **Computación Tolerante a Fallos:** Módulo 29 con teorema del umbral, distilación de magic states y hoja de ruta 2033.

## Visualizador Cuántico Interactivo

El repositorio incluye una herramienta visual dinámica con 7 páginas interactivas. Para lanzarla:
```bash
pip install -r requirements.txt
streamlit run visualizador/app.py
```

Páginas disponibles:
1. **Esfera de Bloch** — estado qubit con canales de ruido y trayectoria 3D
2. **Algoritmos** — Deutsch-Jozsa, Bernstein-Vazirani, Grover paso a paso
3. **Canales y Ruido** — simulación de decoherencia con fidelidad Bures
4. **Hardware Dashboard** — comparativa de 10 procesadores reales (2019-2024)
5. **VQE / QAOA** — optimización variacional con comparativa COBYLA / SPSA / Nelder-Mead
6. **Corrección de Errores** — código de repetición y Shor con curva de protección
7. **Compositor de Circuitos** — 15 puertas, hasta 4 qubits, exporta código Qiskit

## Mapa del Curso e Índices

- [**Indice Maestro del Tutorial**](Tutorial/README.md): Ruta lineal de los 70+ artículos.
- [**Mapa Visual del Curso**](Tutorial/indice_general.md): Diagrama del flujo de aprendizaje por familias temáticas.
- [**Ruta de Estudio por Perfil**](ruta_de_estudio.md): Guía personalizada para programadores, físicos o curiosos.

## Estructura del Repositorio

- `Tutorial/`: El núcleo teórico (29 bloques temáticos, ~70 artículos).
- `Cuadernos/`: Laboratorios guiados y ejemplos de código.
- `visualizador/`: Aplicación interactiva Streamlit (7 páginas).
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

---
*Mantenido como recurso abierto para la comunidad hispana de computación cuántica.*
