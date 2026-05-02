# R11 — Decodificación en Tiempo Real: La Barrera del Microsegundo

> **Problema abierto #5:** ¿Es posible implementar decodificadores QEC con latencia $< 1\,\mu$s suficiente para fault-tolerant computing a escala?

---

## Por qué importa la latencia

En un procesador de superficie de iones trampa o superconductores, el **ciclo de síndrome** dura:
- Preparación ancilla: ~100 ns
- Puertas 2Q para medida: ~300 ns  
- Medida y reset: ~400 ns
- **Total: ~1 μs por ciclo**

Si el decodificador tarda $\tau_\text{dec}$ en procesar el síndrome, y el código tiene $d$ capas temporales, la latencia total de decodificación es $\tau_\text{total} = d \cdot \tau_\text{dec}$.

Para $d=7$ y $\tau_\text{dec} = 10\,\mu$s (software), $\tau_\text{total} = 70\,\mu$s — comparable con $T_2 \sim 100\,\mu$s de muchos procesadores, lo que **anula la corrección**.

**Requisito:** $\tau_\text{dec} \ll 1\,\mu$s por ciclo de síndrome.

---

## Estado del Arte 2025

| Implementación | Latencia | Throughput | Escalabilidad |
|---------------|----------|-----------|---------------|
| Software Python (MWPM) | ~10-100 μs | Limitado | Alta |
| Software C++ (PyMatching) | ~1-5 μs | Medio | Alta |
| GPU paralelo | ~0.5-1 μs | Alto | Moderada |
| FPGA (Xilinx Alveo U250) | ~0.1-0.3 μs | Muy alto | Baja-media |
| ASIC dedicado (prototipo) | <0.05 μs | Máximo | En desarrollo |

**PyMatching v2** (Higgott & Gidney 2023) es el decodificador más rápido en software: implementa MWPM en C++ con estructuras de datos de unión-búsqueda (union-find), alcanzando $\sim 1\,\mu$s para $d=5$ en CPU estándar.

---

## FPGA — Decodificación Sub-Microsegundo

Las **FPGAs** (Field-Programmable Gate Arrays) permiten implementar el decodificador como hardware reconfigurable con latencias deterministas:

### Arquitectura Union-Find FPGA (Das et al. 2022)
1. El síndrome llega como bits en un registro de entrada
2. La estructura Union-Find actualiza el grafo de defectos en paralelo
3. El matching se computa en $O(d^2)$ ciclos de reloj (200 MHz → 5 ns/ciclo)
4. La corrección se emite como máscara de Pauli en salida

**Latencia medida:** 300 ns para $d=5$, escalando aproximadamente como $O(d^2)$.

### Pipeline paralelo para múltiples qubits lógicos
Para $k$ qubits lógicos, el pipeline puede procesarlos en paralelo con $k$ instancias FPGA independientes. La latencia no escala con $k$ si hay suficientes recursos.

---

## Decodificadores Neuronales — Inferencia en Hardware

Los **decodificadores neuronales** (transformer o LSTM) alcanzan alta precisión pero su latencia de inferencia es crítica:

| Arquitectura | Parámetros | Latencia CPU | Latencia GPU | Latencia FPGA |
|-------------|-----------|-------------|-------------|--------------|
| MLP (2 capas, 64 neuronas) | ~8K | ~10 μs | ~1 μs | ~0.1 μs |
| CNN small | ~50K | ~100 μs | ~5 μs | ~0.5 μs |
| Transformer (2 capas) | ~500K | ~500 μs | ~50 μs | Difícil |

Los MLP pequeños son compatibles con el requisito de 1 μs en GPU dedicada.

**Cuantización y pruning:** Reducir a int8 (de float32) acelera la inferencia 4× sin pérdida significativa de accuracy. Redes podadas al 90% pueden alcanzar <100 ns en ASIC.

---

## Brecha Actual y Hoja de Ruta

| Año | Hito | Estado |
|-----|------|--------|
| 2022 | PyMatching v1: ~10 μs software | ✅ |
| 2023 | PyMatching v2: ~1 μs, Union-Find FPGA ~300 ns | ✅ |
| 2024 | Decodificadores neuronales en GPU: ~0.5 μs | ✅ |
| 2025 | ASIC prototipo: <100 ns para d=5 | En progreso |
| 2026-28 | ASIC integrado, d=7-11, <50 ns | Objetivo IBM/Google |

**La brecha principal** no es la latencia punta por síndrome, sino la **escalabilidad**: mantener <1 μs para $d=11$ (needed for 10⁻¹⁵ logical error rate) con miles de qubits lógicos simultáneos requiere chips ASIC dedicados todavía en desarrollo.

---

## Conclusión

El microsegundo ya es alcanzable para $d \leq 7$ en FPGA. La barrera real es:
1. **Escalar a d=11-15** manteniendo la latencia
2. **Integrar** el decodificador junto al control del QPU sin latencia de interconexión
3. **Decodificar en tiempo real** durante la ejecución del circuito lógico (on-the-fly)

El campo avanza rápidamente: la solución probable para procesadores comerciales tolerantes a fallos (2028-2030) son ASICs dedicados co-diseñados con el QPU.
