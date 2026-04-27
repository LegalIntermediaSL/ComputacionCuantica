# Autoevaluación Modular — Computación Cuántica v3.5

Checklist de competencias por módulo. Marca cada ítem cuando puedas completarlo **sin consultar notas**.

---

## Módulo 01 — Qubits y estados cuánticos

- [ ] Escribo un qubit genérico |ψ⟩ = α|0⟩ + β|1⟩ con la restricción de normalización
- [ ] Represento un qubit en la esfera de Bloch (ángulos θ, φ)
- [ ] Distingo estado puro de estado mixto (matriz densidad ρ, Tr(ρ²))
- [ ] Calculo el valor esperado ⟨ψ|O|ψ⟩ para un observable dado
- [ ] Identifico qubits ortogonales: |0⟩/|1⟩, |+⟩/|−⟩, |i⟩/|−i⟩

**Nivel recomendado para continuar:** completar 4/5

---

## Módulo 02 — Qiskit básico

- [ ] Creo un `QuantumCircuit` con n qubits y m bits clásicos
- [ ] Aplico puertas H, X, Y, Z, S, T, CX, CCX con la API Qiskit 2.x
- [ ] Ejecuto un circuito con `StatevectorSimulator` y obtengo el vector de estado
- [ ] Mido y obtengo una distribución de probabilidades con `StatevectorSampler`
- [ ] Visualizo el circuito con `circuit.draw('mpl')`

**Nivel recomendado para continuar:** completar 4/5

---

## Módulo 03 — Entrelazamiento

- [ ] Preparo los 4 estados de Bell con Qiskit
- [ ] Calculo la entropía de entrelazamiento S(ρ_A) = -Tr(ρ_A log ρ_A)
- [ ] Explico por qué Bell viola las desigualdades de Bell-CHSH
- [ ] Implemento el protocolo de teletransportación cuántica (3 qubits, 2 bits clásicos)
- [ ] Identifico estados separables vs entrelazados para estados de 2 qubits

**Nivel recomendado para continuar:** completar 4/5

---

## Módulo 04 — Qiskit Runtime y Primitivas V2

- [ ] Uso `StatevectorEstimator.run()` con `PauliSumOp` / `SparsePauliOp`
- [ ] Uso `StatevectorSampler.run()` y proceso `PrimitiveResult`
- [ ] Configuro `options.resilience_level` en el Estimator
- [ ] Empaqueto trabajos en `batch` de Primitivas
- [ ] Distingo `Estimator` (expectation values) de `Sampler` (bitstrings)

**Nivel recomendado para continuar:** completar 4/5

---

## Módulo 05 — Algoritmos cuánticos clásicos

- [ ] Implemento Deutsch-Jozsa e identifico función balanceada vs constante en 1 consulta
- [ ] Implemento Bernstein-Vazirani y recupero la cadena secreta s
- [ ] Construyo el oráculo de Grover para N elementos y k soluciones
- [ ] Aplico el operador de difusión de Grover (reflexión alrededor de |s⟩)
- [ ] Calculo el número óptimo de iteraciones: ⌊π√(N/k)/4⌋
- [ ] Implemento QFT sobre n qubits (O(n²) puertas)
- [ ] Explico QPE: precisión 2^(-t) con t qubits de control

**Nivel recomendado para continuar:** completar 5/7

---

## Módulo 06 — Ruido y hardware

- [ ] Defino T1 (relajación) y T2 (decoherencia de fase) y su relación T2 ≤ 2T1
- [ ] Modelizo canal de amortiguamiento de amplitud con parámetro γ
- [ ] Modelizo canal depolarizante con parámetro p
- [ ] Aplico `AerSimulator` con `NoiseModel` de Qiskit Aer
- [ ] Explico la diferencia entre error de puerta, error de medida y error de readout

**Nivel recomendado para continuar:** completar 4/5

---

## Módulo 07 — Mitigación de errores

- [ ] Explico Zero-Noise Extrapolation (ZNE) y la curva de extrapolación
- [ ] Implemento circuit folding: U → U(U†U)^k para escalar ruido
- [ ] Aplico Richardson extrapolation con λ = 1, 3, 5
- [ ] Explico Probabilistic Error Cancellation (PEC) y su overhead O(γ²)
- [ ] Comparo ZNE vs PEC: cuándo usar cada uno

**Nivel recomendado para continuar:** completar 3/5

---

## Módulo 08 — Pulse-level y compilación

- [ ] Explico qué es un pulso Gaussian y su relación con Rabi oscillations
- [ ] Construyo un `Schedule` en Qiskit Pulse con `DriveChannel`
- [ ] Compilo un circuito con `transpile()` para un backend específico
- [ ] Explico el conjunto de puertas nativas ECR/CX/RZ para IBM
- [ ] Entiendo la diferencia entre 1Q y 2Q gate fidelity

**Nivel recomendado para continuar:** completar 3/5

---

## Módulo 09 — Corrección de errores

- [ ] Implemento el código de repetición clásico de 3 bits
- [ ] Implemento el código de repetición cuántico de 3 qubits (protege contra bit-flips)
- [ ] Explico los 9 qubits del código de Shor (protege contra todos los errores de 1 qubit)
- [ ] Calculo la tasa de error lógico con el código de repetición: p_L ≈ 3p²
- [ ] Explico qué es un síndrome y un operador de estabilizador

**Nivel recomendado para continuar:** completar 4/5

---

## Módulo 10 — Hardware cuántico moderno

- [ ] Explico la arquitectura transmon: energía EJ, EC, frecuencia de transición
- [ ] Distingo transmon, fluxonium y qubit de spin en silicio
- [ ] Explico por qué Majorana qubits son inherentemente protegidos contra errores
- [ ] Interpreto una curva de Rabi y extraigo la frecuencia de Rabi Ω
- [ ] Comparo las métricas de 5 plataformas: T1, T2, fidelidad 2Q, escala

**Nivel recomendado para continuar:** completar 3/5

---

## Módulo 11 — Algoritmos variacionales (VQE/QAOA)

- [ ] Explico el principio variacional: ⟨ψ(θ)|H|ψ(θ)⟩ ≥ E_0
- [ ] Implemento un ansatz Hardware Efficient (HEA) con Qiskit
- [ ] Optimizo VQE con COBYLA/SPSA y analizo convergencia
- [ ] Formulo MAX-CUT como problema QAOA con Hamiltoniano Ising
- [ ] Explico el parámetro p de QAOA y la mejora con p → ∞
- [ ] Identifico barren plateaus: Var[∂C/∂θ_k] ∝ 4^(-n)

**Nivel recomendado para continuar:** completar 4/6

---

## Módulo 12 — Aplicaciones industriales

- [ ] Formulo un portfolio QUBO: min xᵀQx con restricción Σx_i = k
- [ ] Convierto QUBO a Hamiltoniano Ising con SparsePauliOp
- [ ] Implemento quantum kernel K(x,x') = |⟨ϕ(x')|ϕ(x)⟩|² con ZZFeatureMap
- [ ] Calculo Kernel Target Alignment (KTA)
- [ ] Explico por qué QML no garantiza ventaja cuántica (data encoding bottleneck)
- [ ] Implemento QAE para Monte Carlo: ventaja cuadrática O(1/ε) vs O(1/ε²)

**Nivel recomendado para continuar:** completar 4/6

---

## Módulo 14 — Surface codes y horizonte fault-tolerant

- [ ] Explico la arquitectura del surface code en lattice 2D
- [ ] Identifico estabilizadores X y Z del surface code
- [ ] Calculo el umbral del código de repetición: p_th = 50%
- [ ] Calculo el umbral del surface code: p_th ≈ 1%
- [ ] Estimo overhead de qubits físicos para n lógicos: ~O(d²) con distancia d
- [ ] Explico la destilación de magic states: 15→1, p_out ≈ 35p³

**Nivel recomendado para continuar:** completar 4/6

---

## Módulos 15–21 — Teoría avanzada (Hamiltonians, canales, sistemas abiertos)

- [ ] Simulo evolución temporal con Trotterización: e^{-iHt} ≈ (e^{-iH_A t/n}e^{-iH_B t/n})^n
- [ ] Escribo la ecuación de Lindblad: dρ/dt = -i[H,ρ] + Σ_k(L_kρL_k† - ½{L_k†L_k,ρ})
- [ ] Calculo la representación de Kraus para canales cuánticos
- [ ] Defino fidelidad de Bures: F(ρ,σ) = (Tr√(√ρ σ √ρ))²
- [ ] Distingo proceso CP, CPTP y unitario

**Nivel recomendado para continuar:** completar 3/5

---

## Módulo 22 — Recursos cuánticos

- [ ] Defino coherencia cuántica como recurso (C_l1, C_rel)
- [ ] Explico el marco de teoría de recursos: operaciones libres, estados libres
- [ ] Distingo entrelazamiento como recurso de coherencia
- [ ] Calculo entropía relativa de entrelazamiento
- [ ] Explico por qué los estados de Bell son máximamente entrelazados

**Nivel recomendado para continuar:** completar 3/5

---

## Módulo 26 — ZX-Calculus y optimización gráfica

- [ ] Identifico spiders Z (verdes) y X (rojos) en un diagrama ZX
- [ ] Aplico la regla de fusión de spiders del mismo color
- [ ] Aplico la regla π-copy (copiar fase π a través de spiders)
- [ ] Uso PyZX para simplificar un circuito Clifford
- [ ] Explico la completud del ZX-Calculus para la computación cuántica universal

**Nivel recomendado para continuar:** completar 3/5

---

## Módulo 27 — Internet cuántico y QKD

- [ ] Explico el protocolo BB84: 4 estados, 2 bases, tasa de error QBER
- [ ] Explico E91 (Ekert): Bell inequality como prueba de seguridad
- [ ] Calculo la tasa de clave segura en función de QBER
- [ ] Explico entanglement swapping y su rol en repetidores cuánticos
- [ ] Distingo QKD (seguridad probada) de criptografía post-cuántica

**Nivel recomendado para continuar:** completar 3/5

---

## Módulo 28 — Aplicaciones emergentes

- [ ] Explico Quantum Volume (QV) y cómo se mide
- [ ] Explico CLOPS (Circuit Layer Operations Per Second)
- [ ] Interpreto mirror circuits para caracterización de error
- [ ] Explico XEB: fidelidad de cross-entropy benchmarking
- [ ] Distingo ventaja cuántica computacional de supremacía cuántica

**Nivel recomendado para continuar:** completar 4/5

---

## Módulo 29 — Fault-Tolerant Computing

- [ ] Explico el teorema de umbral: p < p_th ⟹ escalabilidad fault-tolerant
- [ ] Calculo overhead de concatenación de código de repetición
- [ ] Explico qué es un magic state y por qué no es destilable sin recursos
- [ ] Explico la hoja de ruta de computación fault-tolerant 2025-2035
- [ ] Calculo recursos necesarios para ejecutar Shor en 2048-RSA

**Nivel recomendado para continuar:** completar 3/5

---

## Módulo 30 — Quantum Advantage (casos reales)

- [ ] Explico el experimento RCS de Google Sycamore (2019)
- [ ] Explico Boson Sampling y la conexión con el permanente de matrices
- [ ] Calculo el costo clásico del permanente: O(2^n · n)
- [ ] Explico por qué MPS simula circuitos de bajo entrelazamiento eficientemente
- [ ] Evalúo críticamente las claims de ventaja cuántica actuales

**Nivel recomendado para continuar:** completar 3/5

---

## Módulo 38 — Quantum Sensing

- [ ] Defino QFI: F_Q = 4(⟨H²⟩ - ⟨H⟩²) para estado puro
- [ ] Explico el límite SQL: δφ ≥ 1/√n
- [ ] Explico el límite de Heisenberg: δφ ≥ 1/n con estado GHZ
- [ ] Calculo QFI para estado GHZ de n qubits bajo Jz: F_Q = n²
- [ ] Aplico la cota de Cramér-Rao: δφ ≥ 1/√(νF_Q)

**Nivel recomendado para continuar:** completar 4/5

---

## Módulo 39 — Compilación avanzada

- [ ] Explico la descomposición KAK: cualquier 2Q unitario ≤ 3 CNOT
- [ ] Uso `transpile()` con `optimization_level=3` en Qiskit
- [ ] Comparo t|ket⟩ vs Qiskit para circuitos de 10+ qubits
- [ ] Explico Solovay-Kitaev: aproximación con O(log^c(1/ε)) puertas
- [ ] Distingo compilación estática de compilación adaptativa (mid-circuit measurement)

**Nivel recomendado para continuar:** completar 3/5

---

## Módulo 40 — QSVT y algoritmos de bloque-codificación

- [ ] Defino block-encoding: U|0⟩|x⟩ = A/(α||A||)|0⟩|ψ⟩ + ...
- [ ] Explico QSVT: transformación de valores singulares por procesamiento de señal cuántica
- [ ] Calculo número de ancillas para block-encoding de A ∈ ℂ^{2^n}: n ancillas (QR-completion)
- [ ] Explico la ventaja de QSVT sobre HHL para sistemas lineales
- [ ] Implemento una QSP sequence para la función signum

**Nivel recomendado para continuar:** completar 3/5

---

## Resumen de Progreso

| Módulo | Items | Completados | % | Estado |
|--------|-------|-------------|---|--------|
| 01 — Qubits | 5 | ___ | ___% | ⬜ |
| 02 — Qiskit básico | 5 | ___ | ___% | ⬜ |
| 03 — Entrelazamiento | 5 | ___ | ___% | ⬜ |
| 04 — Runtime V2 | 5 | ___ | ___% | ⬜ |
| 05 — Algoritmos | 7 | ___ | ___% | ⬜ |
| 06 — Ruido | 5 | ___ | ___% | ⬜ |
| 07 — Mitigación | 5 | ___ | ___% | ⬜ |
| 08 — Pulse/Compilación | 5 | ___ | ___% | ⬜ |
| 09 — Corrección errores | 5 | ___ | ___% | ⬜ |
| 10 — Hardware | 5 | ___ | ___% | ⬜ |
| 11 — Variacionales | 6 | ___ | ___% | ⬜ |
| 12 — Aplicaciones | 6 | ___ | ___% | ⬜ |
| 14 — Surface codes | 6 | ___ | ___% | ⬜ |
| 15–21 — Teoría avanzada | 5 | ___ | ___% | ⬜ |
| 22 — Recursos | 5 | ___ | ___% | ⬜ |
| 26 — ZX-Calculus | 5 | ___ | ___% | ⬜ |
| 27 — Internet cuántico | 5 | ___ | ___% | ⬜ |
| 28 — Emergentes | 5 | ___ | ___% | ⬜ |
| 29 — Fault-Tolerant | 5 | ___ | ___% | ⬜ |
| 30 — Advantage | 5 | ___ | ___% | ⬜ |
| 38 — Sensing | 5 | ___ | ___% | ⬜ |
| 39 — Compilación avanzada | 5 | ___ | ___% | ⬜ |
| 40 — QSVT | 5 | ___ | ___% | ⬜ |
| **TOTAL** | **123** | ___ | ___% | ⬜ |

### Criterios de certificación

| Puntuación global | Nivel |
|---|---|
| ≥ 90% (≥111/123) | 🏆 Investigador — apto para contribuir a fronteras |
| 75–89% (92–110) | 🥇 Avanzado — domina el stack completo |
| 55–74% (68–91) | 🥈 Intermedio — bases sólidas, profundizar teoría avanzada |
| < 55% (< 68) | 🥉 Básico — revisar módulos 01–09 antes de continuar |

---

*Usa este checklist con el [Examen de Certificación](examen_certificacion.md) para una evaluación completa.*
