# Módulo 37 — Física de Nuevos Qubits

**Nivel:** muy avanzado · **Prerrequisitos:** módulos 23, 29, 34

Más allá del transmon: las plataformas emergentes que podrían llevar la
computación cuántica al régimen fault-tolerant sin la sobrecarga de corrección
de errores que sufre el transmon.

## Artículos

1. [01_fluxonium_y_0pi.md](01_fluxonium_y_0pi.md)
   — Fluxonium y el qubit 0-π: anarmonicidad extrema, protección topológica por diseño
2. [02_majorana_2025.md](02_majorana_2025.md)
   — Qubits de Majorana: estado del arte 2025, Microsoft Topological Core, debate experimental
3. [03_spin_en_silicio.md](03_spin_en_silicio.md)
   — Spin en silicio: qubits de electrón/hueco, CMOS cuántico, roadmap Intel/IMEC

## Motivación

El transmon estándar requiere ~1000 qubits físicos por qubit lógico en surface code.
Las plataformas de este módulo apuntan a reducir ese overhead drásticamente:

| Plataforma    | Overhead estimado | Ventaja clave                        |
|---------------|------------------|--------------------------------------|
| Transmon      | ~1000:1           | Madurez tecnológica                  |
| Fluxonium     | ~100:1 (proyect.) | Tiempos T₁ > 1 ms, alta anarmon.    |
| 0-π qubit     | ~10:1 (teórico)   | Protección exponencial dual          |
| Majorana      | ~10:1 (teórico)   | No-abelian anyons, qubit topológico  |
| Spin-Si       | ~100:1 (proyect.) | CMOS compatible, alta densidad       |
