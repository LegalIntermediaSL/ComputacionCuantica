# Módulo 36 — Criptografía Post-Cuántica: Profundidad

**Nivel:** muy avanzado · **Prerrequisitos:** módulos 25, 33

Los estándares NIST PQC 2024 (ML-KEM, ML-DSA, SLH-DSA) son la respuesta
práctica a corto plazo ante la amenaza de los ordenadores cuánticos fault-tolerant.
Este módulo analiza sus fundamentos matemáticos y estrategias de migración.

## Artículos

1. [01_kyber_y_dilithium.md](01_kyber_y_dilithium.md)
   — ML-KEM (Kyber) y ML-DSA (Dilithium): retículas, LWE/MLWE, implementación Python
2. [02_migracion_y_transicion.md](02_migracion_y_transicion.md)
   — TLS híbrido, timeline NIST, harvest-now-decrypt-later, estrategia de migración

## Contexto

En agosto de 2024, NIST publicó los primeros estándares PQC: FIPS 203 (ML-KEM),
FIPS 204 (ML-DSA) y FIPS 205 (SLH-DSA). Su adopción masiva es urgente —
la ventana de "harvest now, decrypt later" ya está activa.
