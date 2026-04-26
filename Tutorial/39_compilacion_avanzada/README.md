# Módulo 39 — Compilación Cuántica Avanzada

**Nivel:** muy avanzado · **Prerrequisitos:** módulos 04, 26, 29

La compilación cuántica traduce circuitos lógicos al conjunto de instrucciones
nativo del hardware (ISA), optimizando profundidad, conteo de puertas y errores
de conectividad. Este módulo cubre las técnicas de vanguardia.

## Artículos

1. [01_transpiler_passes_qiskit.md](01_transpiler_passes_qiskit.md)
   — Arquitectura PassManager, passes custom, ruteo de qubits (SABRE),
   síntesis de unitarias, cross-resonance, benchmark transpiler
2. [02_compilacion_basada_en_zx.md](02_compilacion_basada_en_zx.md)
   — T-count optimizado con PyZX, síntesis Clifford+T, phase gadgets,
   reducción de CNOT, comparativa con transpiler nativo de Qiskit

## Contexto

El compilador es el cuello de botella entre el circuito abstracto y el
hardware ruidoso. Una reducción del 30% en profundidad puede significar
el doble de fidelidad en un dispositivo con T₂ limitado.
