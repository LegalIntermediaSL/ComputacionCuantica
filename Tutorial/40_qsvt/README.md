# Módulo 40 — QSVT y Algoritmos de Bloque-Codificación

**Nivel:** muy avanzado · **Prerrequisitos:** módulos 15, 29, 33

La Quantum Singular Value Transformation (QSVT) es el marco unificador
de casi todos los algoritmos cuánticos con ventaja superpolinomial: Shor,
HHL, QPE, Grover, simulación hamiltoniana y estimación de amplitud son
casos especiales de QSVT.

## Artículos

1. [01_block_encoding_y_lcu.md](01_block_encoding_y_lcu.md)
   — Block encoding de matrices hermitianas y generales, LCU (Linear
   Combination of Unitaries), qubitización, walk operators
2. [02_qsvt_aplicaciones.md](02_qsvt_aplicaciones.md)
   — Transformación polinomial de valores singulares, simulación hamiltoniana
   O(log 1/ε), inversión de matrices, QMC cuántico, implementación en Qiskit

## Contexto

QSVT (Gilyen et al., STOC 2019) demostró que todos los algoritmos cuánticos
con ventaja exponencial son instancias de transformación polinomial de
valores singulares de una matriz block-encoded. Es el resultado teórico
más importante de la última década en algoritmos cuánticos.
