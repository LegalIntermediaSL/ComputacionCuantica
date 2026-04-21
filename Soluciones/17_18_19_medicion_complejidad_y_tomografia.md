# Problemas Resueltos: Complejidad y Tomografía

## P1: Parámetros de Tomografía
**Pregunta:** ¿Cuántas mediciones proyectivas independientes necesitamos para reconstruir un estado de 2 qubits?
**Solución:**
La matriz de densidad de 2 qubits es de $4 \times 4$, con 15 parámetros independientes reales (debido a la hermiticidad y traza unidad). Necesitamos al menos 15 mediciones de valores esperados independientes (combinaciones de $XI, IX, XX, XY \dots$) para resolver el sistema de ecuaciones.

## P2: BQP vs NP
**Pregunta:** ¿Es Shor un algoritmo que resuelve un problema NP-completo?
**Solución:**
No. La factorización de enteros está en **NP**, pero no se ha demostrado que sea **NP-Completo**. El éxito de Shor en BQP no implica que la computación cuántica pueda romper la jerarquía de las clases NP-Duras clásicas generales.
