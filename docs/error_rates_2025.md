# Tasas de Error de Hardware Cuántico — 2025

Tabla de referencia de métricas actualizadas para los principales procesadores cuánticos disponibles a mitad de 2025.

## IBM Quantum (Heron r2, Eagle r3)

| Backend | Qubits | Arquitectura | T1 (μs) | T2 (μs) | Error 1Q | Error 2Q (ECR) | Readout |
|---------|--------|--------------|---------|---------|----------|----------------|---------|
| ibm_brisbane | 127 | Eagle r3, Heavy-Hex | ~150–200 | ~100–150 | ~2×10⁻⁴ | ~5×10⁻³ | ~2% |
| ibm_kyiv | 127 | Eagle r3, Heavy-Hex | ~150 | ~120 | ~2×10⁻⁴ | ~5×10⁻³ | ~1.5% |
| ibm_sherbrooke | 127 | Eagle r3, Heavy-Hex | ~180 | ~130 | ~1.5×10⁻⁴ | ~4×10⁻³ | ~1.5% |
| ibm_torino | 133 | Heron r2, 100% CZ | ~250–400 | ~150–250 | ~5×10⁻⁵ | ~5×10⁻⁴ | ~1% |
| ibm_fez | 156 | Heron r2 | ~300 | ~200 | ~5×10⁻⁵ | ~5×10⁻⁴ | ~0.8% |

**Nota Heron r2:** La nueva arquitectura utiliza puertas CZ en lugar de CNOT/ECR. La fidelidad de puerta de 2 qubits es ~10x mejor que Eagle.

## Google Quantum AI (Willow, 2024)

| Chip | Qubits | T1 (μs) | T2 (μs) | Error 1Q | Error 2Q (CZ) | Readout |
|------|--------|---------|---------|----------|----------------|---------|
| Willow (2024) | 105 | ~60–100 | ~50–80 | ~1×10⁻⁴ | ~2×10⁻³ | ~1% |
| Sycamore (ref.) | 53 | ~15–30 | ~10–20 | ~3×10⁻⁴ | ~6×10⁻³ | ~3% |

**Hito Willow:** Corrección de errores por debajo del umbral — al aumentar la distancia del código de superficie, la tasa de error lógico *decrece*. Primera demostración experimental de este comportamiento subumbral.

## IonQ (Aria, Forte)

| Sistema | Qubits | T1 (s) | T2 (s) | Error 1Q | Error 2Q | Readout |
|---------|--------|--------|--------|----------|----------|---------|
| IonQ Aria | 25 | ~1000 | ~10–100 | ~4×10⁻⁴ | ~3×10⁻³ | ~0.5% |
| IonQ Forte | 35 | ~1000 | ~50 | ~3×10⁻⁴ | ~2×10⁻³ | ~0.4% |

**Ventaja iones:** T1 y T2 son órdenes de magnitud mayores que qubits superconductores. La interconectividad all-to-all elimina el overhead de SWAP.

**Desventaja:** Las puertas de 2 qubits son ~1000x más lentas (ms vs ns) — el throughput total (CLOPS) es menor.

## Quantinuum (H2)

| Sistema | Qubits | T2 | Error 1Q | Error 2Q | Readout | CLOPS |
|---------|--------|----|----------|----------|---------|-------|
| H2-1 (2024) | 56 | ~1s | ~3×10⁻⁵ | ~1×10⁻³ | <0.1% | ~100 |

**Cuantinuum H2** tiene la mayor fidelidad de puerta de 2 qubits de cualquier sistema disponible comercialmente. Usado para demostrar corrección de errores fault-tolerant con código [[7,1,3]].

## Neutral Atoms (QuEra, Pasqal)

| Sistema | Qubits | T2 | Error 2Q | Conectividad |
|---------|--------|----|----------|--------------|
| QuEra Aquila | 256 | ~1–5s | ~3×10⁻³ | Reconfigurable |
| Pasqal Fresnel | 100 | ~2s | ~5×10⁻³ | 2D array |

**Ventaja:** Conectividad dinámica (mover átomos), escala a 1000+ qubits en camino.

## Comparativa de Quantum Volume (QV) y CLOPS

| Plataforma | Backend | QV | CLOPS |
|------------|---------|-----|-------|
| IBM (Eagle) | ibm_brisbane | 128–256 | ~1,500 |
| IBM (Heron) | ibm_torino | >1024 | ~15,000 |
| IonQ | Aria | 8192 | ~200 |
| Quantinuum | H2-1 | >524,288 | ~100 |
| Google | Willow | N/A (XEB) | ~5,000 |

**Quantum Volume** mide la complejidad del circuito cuadrado más grande ejecutable con fidelidad >2/3.

**CLOPS** mide el throughput: cuántas capas de circuitos de ancho 100 QV se ejecutan por segundo.

## Línea de Tiempo de Mejora de Error

```
Año  | IBM 2Q error | Google 2Q error | IonQ 2Q error
-----|-------------|-----------------|---------------
2019 | ~1×10⁻²     | ~6×10⁻³         | ~5×10⁻³
2021 | ~7×10⁻³     | ~5×10⁻³         | ~3×10⁻³
2023 | ~5×10⁻³     | ~3×10⁻³         | ~2×10⁻³
2025 | ~5×10⁻⁴ (Heron) | ~2×10⁻³    | ~1×10⁻³
```

## Umbral para Fault-Tolerant Computing

| Código | Umbral de error de puerta | Estado actual | Barrera |
|--------|--------------------------|---------------|---------|
| Código de repetición | ~50% | ✅ Superado | — |
| Surface code | ~1% | ✅ Superado (Heron, Willow) | Overhead qubits |
| Color code | ~0.6% | ⚠️ En el límite | — |
| Concatenated Steane | ~0.1% | ❌ No alcanzado | Requiere ~10⁻⁴ 2Q |

## Fuentes y Actualizaciones

- [IBM Quantum System Two specs](https://quantum.ibm.com/services/resources)
- [Google Willow paper](https://research.google/blog/making-quantum-error-correction-work/) (Nature, Dic 2024)
- [IonQ benchmarks](https://ionq.com/quantum-systems)
- [Quantinuum H2 benchmarks](https://www.quantinuum.com/hardware)

*Última actualización: Abril 2025. Los valores de hardware cuántico cambian frecuentemente — verificar fuentes primarias para datos actualizados.*
