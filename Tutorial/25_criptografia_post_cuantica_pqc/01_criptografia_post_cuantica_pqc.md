# Criptografía Post-Cuántica (PQC)

Sabemos que el algoritmo de Shor puede factorizar números grandes de forma eficiente, lo que rompería RSA y Eliptic Curve Criptography. Pero, ¿significa esto el fin de la seguridad en internet? No.

## El Escenario "Harvest Now, Decrypt Later"

Muchos actores están recolectando datos cifrados hoy con la esperanza de descifrarlos cuando existan computadoras cuánticas potentes. Por eso, la migración a **PQC** es una urgencia de seguridad nacional.

## La Matemática de la Resistencia Cuántica

A diferencia de la factorización, existen problemas matemáticos que se cree que son difíciles incluso para una computadora cuántica. El más prominente es el **Lattice-based Cryptography** (Criptografía basada en retículos).
- El problema de la **Búsqueda del Vector más Corto (SVP)** en un retículo de alta dimensión no tiene un algoritmo cuántico eficiente conocido.
- Otros métodos incluyen criptografía basada en **códigos correctores de errores**, **isogenias de curvas elípticas** y **polinomios multivariados**.

## Estándares del NIST

Recientemente, el NIST ha seleccionado algoritmos estándar para la era post-cuántica:
1. **CRYSTALS-Kyber:** Para el establecimiento de claves.
2. **CRYSTALS-Dilithium:** Para firmas digitales.

## Criptografía Cuántica vs Post-Cuántica
- **Criptografía Cuántica (QKD):** Usa hardware cuántico para generar claves privadas seguras por las leyes de la física.
- **Criptografía Post-Cuántica (PQC):** Usa software clásico (algoritmos matemáticos) resistentes a ataques de hardware cuántico.

## Navegación
- Anterior: [Programación de pulsos con Qiskit Pulse](../24_control_de_pulsos_y_qiskit_pulse/02_programacion_de_pulsos_con_qiskit_pulse.md)
- Siguiente: [Qué puede y que no puede hacer la computación cuántica hoy](../../13_limites_actuales_y_realismo/01_que_puede_y_que_no_puede_hacer_la_computacion_cuantica_hoy.md)
