# Comparativa de arquitecturas cuánticas para QEC: 2024

**Módulo 31 · Artículo 3 · Nivel muy avanzado**

---

## ¿Qué necesita una arquitectura para QEC?

Para implementar un código de corrección de errores de forma útil, una plataforma cuántica debe satisfacer:

1. **Error físico por debajo del umbral:** ε < ε_th (típico: 0,1-1% dependiendo del código).
2. **Conectividad suficiente:** el código de superficie requiere vecinos inmediatos en 2D.
3. **Lectura de síndrome sin destruir el estado lógico:** medición de ancilla en ciclos rápidos.
4. **Decodificación en tiempo real:** el decodificador debe operar en < 1 ciclo de síndrome.
5. **Escalabilidad:** fabricar miles de qubits con parámetros homogéneos.

---

## Tabla comparativa de plataformas (2024)

| Plataforma | T1 | T2 | F_2Q | Readout | Ciclo síndrome | Umbral | Escalabilidad | Estado 2024 |
|---|---|---|---|---|---|---|---|---|
| **Superconductores (transmon)** | ~100-400 μs | ~100-200 μs | 99.5-99.9% | ~0.5-2% | ~1 μs | ~1% | Alta (fab. CMOS) | Willow, debajo umbral ✅ |
| **Iones atrapados (Ca⁺, Yb⁺)** | >1 s | >1 s | 99.9-99.99% | ~0.1-1% | ~1-10 ms | ~1-3% | Media (chips MEMS) | Demonstraciones ~50q ✅ |
| **Rydberg (átomos neutros)** | ~1-100 ms | ~1-100 ms | 99-99.9% | ~0.5-5% | ~100 μs | ~1% | Alta (reconfigurable) | 100-1000 qubits ✅ |
| **Qubit topológico (Majorana)** | >ms (teórico) | >ms (teórico) | >99.9% (estimado) | TBD | TBD | ~10% (estimado) | Desconocida | Primer chip 2025 ⚠️ |
| **Fotónico** | ∞ (en tránsito) | ∞ | ~90-99% | Probabilístico | ~ns | Diferente | Media | Boson sampling ⚠️ |

---

## Análisis por plataforma

### Superconductores (transmon) — Líder actual

**Ventajas:**
- Tecnología de fabricación madura (fotolitografía CMOS).
- Tiempos de puerta ultrarrápidos (~10-100 ns), ciclos de síndrome de ~1 μs.
- Conectividad 2D en chip —el código de superficie es directamente implementable.
- Escala probada: 1000+ qubits en chip (IBM Condor, Atom Computing).

**Desventajas:**
- Operación a 20 mK: dilución de helio costosa y voluminosa (~1 ton/sistema).
- T1, T2 limitados a ~100-400 μs → solo ~100-400 ciclos de síndrome antes de decoherencia.
- Dispersión de parámetros (variabilidad entre qubits) → overhead de calibración.

```python
# ¿Cuántos errores lógicos tolera una cadena de Shor con transmons?
import numpy as np

T2 = 200e-6        # 200 μs
t_ciclo = 1e-6     # 1 μs por ciclo
n_ciclos = T2 / t_ciclo   # = 200 ciclos de síndrome

# Con d=7, p_fis=0.3% debajo del umbral:
p_fis = 0.003
p_th = 0.01
p_logico_por_ciclo = 0.1 * (p_fis/p_th)**4  # ceil(7/2)=4

p_logico_total = 1 - (1 - p_logico_por_ciclo)**n_ciclos
print(f'Transmons d=7: {p_logico_total:.2e} de error lógico en {n_ciclos:.0f} ciclos')
```

### Iones atrapados — Mayor fidelidad, menor velocidad

**Ventajas:**
- T1, T2 de segundos a minutos — miles de ciclos de síndrome disponibles.
- Fidelidad de puerta 2Q: 99,9-99,99% (mejor que superconductores).
- Conectividad all-to-all dentro de la trampa (ventaja para algunos códigos).
- Sin necesidad de refrigeración criogénica (~μK en campo magnético).

**Desventajas:**
- Tiempos de puerta lentos: 10-100 μs por puerta 2Q (gates lentas → menos ciclos por unidad de tiempo).
- Escalabilidad limitada: trampas actuales con ~50-200 iones; escalar a 1000+ requiere interconexión entre trampas.
- Error de motional heating limita la cohesión en trampas grandes.

**Status 2024:** Quantinuum H2 (56 qubits, F_2Q = 99,8%) demostró circuitos de corrección con
fidelidades sin precedentes. IonQ Forte con 35 qubits AQ.

### Rydberg (átomos neutros) — El jugador emergente

**Ventajas:**
- Átomos individuales atrapados por pinzas ópticas en geometrías arbitrarias reconfigurables.
- Escalabilidad natural: arrays de 1000+ qubits demostrados (Harvard 2023).
- El acoplamiento Rydberg permite puertas CZ de alta fidelidad.
- Sin conectividad fija → se puede mover átomos para implementar cualquier topología.

**Desventajas:**
- Pérdida de átomos durante operación (~1% por ciclo) → necesidad de recarga.
- Fidelidades de puerta todavía ligeramente por debajo de los mejores superconductores.
- Velocidad limitada por el trap refresh (~100 μs por ciclo de síndrome).

**Status 2024:** Microsoft y QuEra demostraron circuitos transversales con corrección de errores
en arrays de 48-280 qubits. Primer paper de ventaja cuántica con 280 qubits (Harvard, 2023).

### Qubit topológico (Majorana) — La apuesta a largo plazo

**Concepto:** Un qubit topológico codifica información en pares de fermiones de Majorana
no-abelianos en un nanohilo semiconductor. El estado lógico es una propiedad global del par,
intrínsecamente protegido contra perturbaciones locales.

**Ventaja teórica:** La tasa de error intrínseca es exponencialmente suprimida en la longitud
del nanohilo, potencialmente sin necesidad de corrección de errores adicional.

**Microsoft Majorana 1 (2025):** Primer chip con qubits topológicos basados en junciones
superconductoras-semiconductoras. Anunciado en febrero 2025, con demostración de coherencia
topológica. Aún no hay benchmarks de fidelidad de puerta publicados.

```python
# Ventaja teórica del qubit topológico
# Error intrínseco ~ exp(-2*L/xi) donde L = longitud, xi = longitud de coherencia

import numpy as np

xi = 0.5e-6    # longitud de coherencia ~ 500 nm
L_vals = np.linspace(1, 10, 50) * 1e-6  # 1-10 μm

p_error_topologico = np.exp(-2 * L_vals / xi)
p_error_transmon = 0.003  # 0.3% por puerta típico

print('Longitud (μm) | Error topológico | Comparativa transmon')
print('-' * 55)
for L, p in zip(L_vals[::10]*1e6, p_error_topologico[::10]):
    comparativa = 'MEJOR' if p < p_error_transmon else 'peor'
    print(f'{L:>13.1f} | {p:>16.2e} | {comparativa}')
```

---

## ¿Qué plataforma ganará?

No hay consenso en la comunidad. La comparativa honesta a 2024:

| Criterio | Superconductores | Iones | Rydberg | Majorana |
|---|---|---|---|---|
| Error físico ahora | ✅ Bueno | ✅✅ Mejor | ✅ Bueno | ❓ Desconocido |
| Debajo del umbral | ✅ Sí (Google 2024) | ✅ Sí | ✅ Sí | ❓ No demostrado |
| Escala a 10⁶ qubits | ⚠️ Difícil (criostato) | ❌ Difícil (trampas) | ✅ Posible | ❓ Desconocido |
| Velocidad de ciclo | ✅✅ Muy rápido | ❌ Lento | ⚠️ Moderado | ❓ TBD |
| Compatibilidad con QEC | ✅ Alta | ✅ Alta | ✅ Creciente | ✅ Intrínseca (teórico) |
| Inversión industrial | ✅✅ IBM, Google | ✅ IonQ, Quantinuum | ✅ QuEra, Atom | ✅✅ Microsoft |

**Escenario más probable (2025-2035):**

Los **superconductores** seguirán liderando en el corto plazo por su madurez tecnológica
y velocidad de ciclo. Los **iones** dominarán aplicaciones que necesitan altísima fidelidad
con pocos qubits. Los **átomos neutros** emergerán como alternativa escalable cuando las
pérdidas de átomos se resuelvan. Los **Majorana** tienen el mayor potencial a largo plazo
pero necesitan 5-10 años de investigación experimental para validarse.

La computación tolerante a fallos a gran escala probablemente requerirá un **enfoque híbrido**:
módulos de procesamiento cuántico interconectados por fotones (quantum networking),
donde cada nodo usa la plataforma mejor adaptada a su función.

---

**Referencias:**
- Google: Acharya et al., *Nature* 638, 920 (2025)
- IBM: Sundaresan et al., *Nature Communications* 14, 2852 (2023)
- Rydberg: Bluvstein et al., *Nature* 626, 58 (2024)
- Majorana: Aghaee et al. (Microsoft), arxiv 2503.13000 (2025)
