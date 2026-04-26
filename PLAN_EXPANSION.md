# Plan de Expansión — Computación Cuántica: Teoría y Práctica

**Estado general:** v3.0 · 2026-04-27  
**Repositorio:** [LegalIntermediaSL/ComputacionCuantica](https://github.com/LegalIntermediaSL/ComputacionCuantica)

---

## Resumen ejecutivo

| Recurso | v1.0 | v2.0 | v2.5 | v3.0 | Objetivo |
|---|---|---|---|---|---|
| Artículos tutoriales | 30 | 55 | 70 | 80+ | 90 |
| Laboratorios Jupyter | 10 | 20 | 31 | 34 | 40 |
| Páginas visualizador | 3 | 7 | 10 | 12 | 14 |
| Ejercicios | 20 | 35 | 37 | 45+ | 55 |
| Tests pytest | 0 | 15 | 31 | 48 | 65 |
| Soluciones | 5 | 12 | 18 | 18 | 26 |

---

## Fases completadas

### Fase 1-4 — Fundamentos (v1.0)
- Módulos 01-10: qubits, puertas, entrelazamiento, Qiskit básico
- 10 laboratorios iniciales
- Tests básicos

### Fase 5-6 — Algoritmos y Hardware (v1.5)
- Módulos 11-20: algoritmos variacionales, VQE, QAOA, hardware, ruido
- Visualizador Streamlit (3 páginas)
- Laboratorios 11-20

### Fase 7 — Infraestructura educativa (v2.0)
- MkDocs + GitHub Pages
- CONTRIBUTING, CODE_OF_CONDUCT
- Autoevaluación interactiva, evaluador de ejercicios
- CI/CD con GitHub Actions (pytest, code snippets)
- Tour interactivo en el visualizador

### Fase 8 — Hardware avanzado y QML (v2.2)
- Módulos 21-27: sistemas abiertos, recursos cuánticos, hardware físico,
  pulsos, PQC, ZX-Calculus, internet cuántico
- Laboratorios 21-28 (Pennylane, GPU, UCCSD, QML)
- Simulador Ruidoso (página 9 del visualizador)

### Fase 9 — Fronteras modernas (v2.5)
- Módulos 28-37: advantage casos reales, QEC hardware real, DQC, algoritmos FT,
  sistemas abiertos, adiabatica, PQC profundidad, nuevos qubits
- Notebook 31: Qiskit Patterns
- Visualizador páginas 8-10 (Tomografía, Simulador Ruidoso, Algoritmos Completos)
- Tests: 31 casos

### Fase 10 — QSVT, sensing y compilación (v3.0) ← COMPLETADA 2026-04-27
- **Módulos 38-40**: Quantum Sensing y Metrología, Compilación Avanzada, QSVT
- **Laboratorios 32-34**: Química avanzada UCCSD, compilación t\|ket⟩, Quantum Walks
- **Visualizador páginas 11-12**: Estimador de Recursos FT, Landscape VQE/QAOA
- **Ejercicios investigación**: 8 problemas de frontera (R1-R8)
- **Tests**: 31 → 48 (módulos 38-40, QFI, KAK, DTQW, CTQW, Chebyshev)
- **Infraestructura**: `environment.yml`, `Makefile`, `pyproject.toml`, `.devcontainer/`
- **Fix**: Simulador Ruidoso (ccx noise model), tour_guide tuples→dicts

---

## Fase 11 — Soluciones, notebooks 35-37, baseline CI (v3.1) ← EN PROGRESO

### 11.1 — Soluciones de ejercicios de investigación
- **R1**: Aproximación Chebyshev para QSVT (sgn, 1/x, exp) con cotas de convergencia
- **R2**: Block-encoding explícita de matriz 4×4
- **R3**: Verificación experimental de barren plateaus + estrategia de mitigación
- **R4**: ZNE manual con Richardson extrapolation, comparativa vs sin mitigación
- Archivos en `Soluciones/investigacion/`

### 11.2 — Notebook 35: Computación Adiabática y QAOA avanzado
- Teorema adiabático: tiempo mínimo $T \sim \Delta^{-2}$
- Implementación adiabática en Qiskit (Trotter + scheduling)
- Comparativa QAOA p=1,2,3 en MAX-CUT
- Landscape de energía adiabático vs variacional

### 11.3 — Notebook 36: Nuevos Qubits (Fluxonium, Majorana, Spin-Si)
- Hamiltoniano Fluxonium vs Transmon: comparativa de anharmonicidad
- Error rates proyectados para 2025-2028 (Microsoft Majorana 1)
- Implementación de qubits de espín en Si (IBM, Intel)
- Tabla comparativa de plataformas de hardware 2024-2028

### 11.4 — Notebook 37: Redes Cuánticas y QKD avanzado
- BB84 con canal ruidoso: QBER vs Eve's information
- E91 y prueba CHSH completa
- Protocolo MDI-QKD (measurement-device-independent)
- Simulación de repetidor cuántico básico

### 11.5 — Tests baseline JSON y pytest markers
- Serializar valores de referencia en `tests/baseline.json`
- Añadir markers `@pytest.mark.slow` para tests con simulación pesada
- `make test-fast` excluye slow, CI usa fast + nightly usa all
- Target: 65 tests

### 11.6 — Visualizador página 13: Quantum Walk interactivo
- DTQW en línea: controles de moneda, pasos, estado inicial
- Comparativa balístico vs clásico en tiempo real
- Exportar animación GIF

### 11.7 — Actualización MkDocs y deployment
- Añadir laboratorios 32-34 y módulos 38-40 al índice
- Página "Ejercicios de investigación" con soluciones colapsables
- Deploy automático via GitHub Actions

---

## Fase 12 — Aplicaciones industriales extendidas (v3.5) ← PLANIFICADA

### 12.1 — Quantum Finance avanzado
- Quantum Risk Analysis con Monte Carlo cuántico (QAE)
- Optimización de portafolios con QAOA en grafos reales (IBEX-35)
- Quantum credit scoring

### 12.2 — Quantum Chemistry con hardware real
- Integración con IBM Quantum: jobs reales en ibm_brisbane
- Comparativa simulador vs hardware para VQE H₂
- Error mitigation (ZNE, PEC) aplicado a química

### 12.3 — QML con datos reales
- Clasificación de imágenes médicas (MNIST cuántico)
- QNN con Pennylane y PyTorch backend
- Benchmark kernel cuántico vs RBF en datasets reales

### 12.4 — Laboratorio de advantage cuántica
- Random Circuit Sampling (Google Sycamore-style)
- Boson sampling simplificado
- Comparativa clásica (MPS simulator) vs cuántico

---

## Fase 13 — Ecosistema completo (v4.0) ← VISIÓN

- **Curso certificado**: examen autoevaluado con 50 preguntas y badge digital
- **API pública**: endpoints REST para ejecutar circuitos de demostración
- **Comunidad**: foro de preguntas, sistema de PRs educativos revisados
- **Versión hardware**: guía para ejecutar cada notebook en IBM Quantum Free Plan
- **Traducciones**: inglés, portugués

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

- [ ] Traducción inglés del README y módulos 01-10
- [ ] Integración con IBM Quantum Network (credenciales por usuario)
- [ ] Soporte para IonQ y Quantinuum via cloud providers
- [ ] Versión LaTeX del tutorial (PDF descargable)
- [ ] Módulo 41: Computación cuántica distribuida (DQC) avanzada
- [ ] Módulo 42: Quantum Machine Learning teórico (PAC learning cuántico)
- [ ] Benchmark CLOPS/QV actualizado 2025

---

*Actualizado automáticamente — 2026-04-27*
