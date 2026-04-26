# Módulo 33 — Algoritmos de Era Fault-Tolerant

**Nivel:** muy avanzado · **Prerrequisitos:** módulos 07, 09, 11, 14, 29

Este módulo analiza los algoritmos que justifican la construcción de ordenadores
cuánticos tolerantes a fallos: sus recursos reales, sus limitaciones honestas
y el estado del arte de la implementación.

## Artículos

1. [01_shor_circuito_completo.md](01_shor_circuito_completo.md)
   — Circuito de Shor para N=15: exponenciación modular, QFT inversa, estimación de período
2. [02_hhl_sistemas_lineales.md](02_hhl_sistemas_lineales.md)
   — HHL para Ax=b: QPE, rotación controlada, cuándo hay ventaja real vs. clásico
3. [03_amplitude_estimation_qae.md](03_amplitude_estimation_qae.md)
   — QAE sin QPE (MLQAE, IQAE): Monte Carlo cuántico, valoración de opciones, QUBO

## Contexto

Estos tres algoritmos representan el núcleo del valor económico y científico
esperado de la computación cuántica fault-tolerant. Su implementación real
requiere decenas a millones de qubits lógicos — entender sus recursos es
esencial para evaluar el roadmap cuántico con honestidad.
