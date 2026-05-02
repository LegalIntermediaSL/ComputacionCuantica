# Resumen 17 — Comparativa de Hardware Cuántico 2025

## Tabla Principal: Plataformas Cuánticas 2025

| Plataforma | Empresa | Qubits 2025 | Fidelidad 2Q | T₂ | Vel. Compuerta | Temperatura | Característica Clave |
|---|---|---|---|---|---|---|---|
| **Heron r2** | IBM | 156 físicos | $99.9\%$ (CR) | $\sim 300$ μs | $\sim 100$ ns | 15 mK | Arquitectura modular, 0 cross-talk entre módulos |
| **Willow** | Google | 105 físicos | $99.85\%$ | $\sim 100$ μs | $\sim 25$ ns | 10 mK | Below-threshold QEC, ventaja cuántica RCS |
| **Forte** | IonQ | 36 + AQ | $99.9\%$ (MS) | $\sim 10$ s | $\sim 600$ μs | Temperatura amb. | Iones de Er, conectividad all-to-all |
| **H2-1** | Quantinuum | 56 | $99.9\%$ | $\sim 100$ s | $\sim 1$ ms | Temperatura amb. | Mayor fidelidad publicada, trampas de iones |
| **Aquila** | QuEra | $\sim 10{,}000$ | $99.5\%$ (CZ) | $\sim 1$ s | $\sim 200$ ns | 10 μK | Átomos Rydberg, reconf. mid-circuit |
| **Borealis** | Xanadu | 216 modos | $>99\%$ (1-fotón) | Coherente | $\sim 1$ ps | Temperatura amb. | Boson sampling, ventaja cuántica GBS |
| **Advantage2** | D-Wave | 5,000+ | N/A (annealing) | μs (adiabático) | $1\text{--}2000$ μs | 15 mK | Optimización QUBO, topología Pegasus |
| **Alpha** (proyectado) | PsiQuantum | $10^6$ (objetivo) | $>99.9\%$ (target) | $\sim 1$ μs | $\sim 1$ ns | 4 K (SNSPD) | Fotónica en silicio, fab CMOS |

---

## Comparativa por Categoría

### Fidelidad y Calidad Lógica

| Plataforma | Fidelidad 1Q | Fidelidad 2Q | SPAM Error | Métrica AQ |
|---|---|---|---|---|
| Quantinuum H2-1 | $99.998\%$ | $99.9\%$ | $<0.1\%$ | AQ 56 |
| IonQ Forte | $99.97\%$ | $99.9\%$ | $<0.3\%$ | AQ 35 |
| Google Willow | $99.9\%$ | $99.85\%$ | $<0.5\%$ | — |
| IBM Heron r2 | $99.9\%$ | $99.9\%$ | $<0.3\%$ | — |
| QuEra Aquila | $99.5\%$ | $99.5\%$ | $<1\%$ | — |

### Escalado de Qubits (Roadmap Publicado)

| Empresa | 2023 | 2024 | 2025 | 2027 (proyección) |
|---|---|---|---|---|
| IBM | 433 (Osprey) | 1,386 (Condor) | Heron r2 (156 mod.) | Kookaburra modular |
| Google | 72 (Sycamore) | 105 (Willow) | Willow+ | >1,000 |
| QuEra | 256 | 1,000 | 10,000 | >100,000 |
| IonQ | 29 (Aria) | 35 (Forte) | 64 (proyectado) | 1,024 |

---

## Temperatura y Tecnología de Enfriamiento

| Tecnología | Temperatura | Método | Costo (OPEX) |
|---|---|---|---|
| Superconductor (IBM/Google) | 10–15 mK | Dilution refrigerator | Alto |
| Iones en trampa (IonQ/Quantinuum) | Temperatura amb. | Trampa electromagnética | Medio |
| Átomos neutros (QuEra) | $\sim 10$ μK | Pinzas ópticas + MOT | Medio |
| Fotónico (Xanadu/PsiQuantum) | Temperatura amb. / 4 K | SNSPD a 4 K | Bajo–Medio |
| Annealing (D-Wave) | 15 mK | Dilution refrigerator | Alto |

---

## Notas Técnicas

- **AQ (Algorithmic Qubits)**: métrica de IonQ que mide qubits efectivos con $>99\%$ fidelidad en circuito completo
- **Cross-Resonance (CR)**: compuerta nativa de IBM en superconductores, implementa CX/CNOT
- **Mølmer-Sørensen (MS)**: compuerta nativa en iones, implementa XX interaction
- **SNSPD**: Superconducting Nanowire Single-Photon Detector, necesario en fotónica a 4 K
- **Below-threshold QEC (Google Willow)**: primer hardware donde aumentar distancia del surface code reduce el error lógico

---

## Métricas de Comparación Práctica

Para seleccionar plataforma según tarea:

| Caso de Uso | Mejor Opción 2025 | Razón |
|---|---|---|
| Algoritmos con alta fidelidad, pocos qubits | Quantinuum H2-1 | Mayor fidelidad publicada |
| Simulación variacional (VQE, QAOA) | IBM Heron r2 | Rapidez + ecosistema Qiskit |
| Optimización combinatoria masiva | D-Wave Advantage | Nativo QUBO, 5000 qubits |
| Simulación de átomos/moléculas neutras | QuEra Aquila | Nativo Hamiltoniano Rydberg |
| Computación fotónica / boson sampling | Xanadu Borealis | Ventaja cuántica GBS demostrada |
