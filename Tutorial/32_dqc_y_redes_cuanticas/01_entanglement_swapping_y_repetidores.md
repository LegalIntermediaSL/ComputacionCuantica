# Entanglement Swapping y Repetidores Cuánticos

**Módulo 32 · Artículo 1 · Nivel muy avanzado**

---

## El problema de la distancia en comunicación cuántica

La teletransportación cuántica transfiere un estado sin enviar el qubit físico,
pero requiere un **par EPR precompartido** entre emisor y receptor. A grandes
distancias, generar y mantener este par es el reto central de las redes cuánticas.

**El problema:** los fotones se pierden en fibra óptica a razón de ~0.2 dB/km.
A 1000 km, la probabilidad de transmisión es 10^{-20} — prácticamente cero.

---

## Entanglement Swapping: entrelazar sin interacción directa

El **entanglement swapping** permite crear entrelazamiento entre partículas que
nunca han interactuado, usando una partícula intermediaria.

### Protocolo

Partiendo de dos pares EPR: (A,C) y (C',B), una medición de Bell sobre (C,C')
entrelaza a A y B:

```
A ─── Par 1 ─── C   C' ─── Par 2 ─── B
                │───│
           Medición de Bell
                ↓
A ──────────── entrelazado ──────────── B
```

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, partial_trace, state_fidelity, DensityMatrix

def entanglement_swapping_circuit() -> QuantumCircuit:
    """
    Qubits: 0=A, 1=C, 2=C', 3=B
    Crea pares EPR (A,C) y (C',B), luego hace swapping.
    """
    qc = QuantumCircuit(4, 2)

    # Par 1: entrelazar A (q0) y C (q1)
    qc.h(0)
    qc.cx(0, 1)

    # Par 2: entrelazar C' (q2) y B (q3)
    qc.h(2)
    qc.cx(2, 3)

    # Medición de Bell en C (q1) y C' (q2)
    qc.cx(1, 2)
    qc.h(1)
    qc.measure([1, 2], [0, 1])

    # Correcciones condicionales sobre B (q3) basadas en resultados de C,C'
    with qc.if_else((qc.clbits[0], 1)):
        qc.z(3)
    with qc.if_else((qc.clbits[1], 1)):
        qc.x(3)

    return qc

# Verificación sin correcciones (versión unitaria)
def swap_unitario() -> Statevector:
    qc = QuantumCircuit(4)
    qc.h(0); qc.cx(0, 1)  # Par EPR (A,C)
    qc.h(2); qc.cx(2, 3)  # Par EPR (C',B)
    qc.cx(1, 2); qc.h(1)  # Medición de Bell (sin medir)
    # Proyectar sobre |00> en C,C' para verificar
    # El estado resultante de A,B es |Phi+>
    return Statevector(qc)

sv = swap_unitario()
print('Estado 4 qubits tras entanglement swapping:')
print(np.round(sv.data, 3))
```

### Verificación: fidelidad de A-B tras el swapping

```python
# Tras el swapping correcto, el par A-B debe ser |Phi+>
# Calculamos la traza parcial sobre C,C' (qubits 1,2)

sv = swap_unitario()
rho_total = DensityMatrix(sv)

# Traza sobre qubits 1 y 2 (C y C')
# En Qiskit: partial_trace toma los índices A CONSERVAR
rho_AB = partial_trace(rho_total, [1, 2])  # traza sobre q1, q2

# Estado Bell ideal |Phi+>
phi_plus = np.array([1, 0, 0, 1]) / np.sqrt(2)
rho_phi_plus = DensityMatrix(np.outer(phi_plus, phi_plus.conj()))

# Fidelidad
F = state_fidelity(rho_AB, rho_phi_plus)
print(f'Fidelidad rho_AB con |Phi+>: {F:.4f}')
print('El entanglement swapping funciona correctamente si F=1')
```

---

## Repetidores Cuánticos

Para distancias > 100 km, la pérdida de fotones hace que la probabilidad de
éxito caiga exponencialmente. Los **repetidores cuánticos** dividen el canal en
segmentos cortos y usan entanglement swapping para extender el alcance.

### Arquitectura de un repetidor cuántico

```
Nodo A ──[20 km]── Repetidor 1 ──[20 km]── Repetidor 2 ──[20 km]── Nodo B
          Par EPR 1               Par EPR 2               Par EPR 3
                    ↓ Swapping              ↓ Swapping
                         Par extendido A–B
```

### Tres generaciones de repetidores

| Generación | Mecanismo | Fidelidad | Estado |
|---|---|---|---|
| 1ª gen. | Purificación + swapping (sin QEC) | ~90% | Demostrado en lab |
| 2ª gen. | QEC en nodos intermedios | ~99% | Prototipo 2024 |
| 3ª gen. | All-optical con QEC integrado | >99.9% | Investigación |

```python
import numpy as np

def tiempo_entrelazamiento_repetidor(
    n_segmentos: int,
    L_total_km: float,
    eta_fibra: float = 0.97,   # transmisividad por km (0.2 dB/km -> 0.955/km)
    t_procesamiento_us: float = 10.0,
) -> float:
    """
    Estima el tiempo medio para establecer entrelazamiento extremo a extremo.

    La tasa de éxito por segmento es η^(L/n).
    El tiempo esperado para conectar k segmentos escala como O(n * (1/η)^(L/n)).
    """
    L_seg = L_total_km / n_segmentos
    eta_seg = eta_fibra ** L_seg
    t_luz_us = (L_seg * 1e3 / 3e8) * 1e6  # tiempo de propagación del fotón

    # Tiempo esperado para un par EPR en un segmento
    t_par_us = t_luz_us / eta_seg

    # Tiempo para conectar todos los segmentos (peor caso: secuencial)
    t_total_us = t_par_us * n_segmentos + t_procesamiento_us * (n_segmentos - 1)
    return t_total_us

print('Tiempo para establecer entrelazamiento A-B (1000 km):')
print(f'{"Segmentos":>10} | {"T_est (s)":>12} | {"Tasa (Hz)":>10}')
print('-' * 38)
for n in [1, 2, 5, 10, 20, 50]:
    t_us = tiempo_entrelazamiento_repetidor(n, 1000)
    t_s  = t_us * 1e-6
    rate = 1 / t_s
    print(f'{n:>10} | {t_s:>12.3f} | {rate:>10.2f}')
```

---

## Purificación de entrelazamiento

Los pares EPR generados en la práctica no son perfectos. La **purificación**
consume múltiples pares imperfectos para producir uno con mayor fidelidad.

El protocolo BBPSSW convierte dos pares con fidelidad F en un par con:

$$F' = \frac{F^2 + \frac{(1-F)^2}{9}}{F^2 + \frac{2F(1-F)}{3} + \frac{5(1-F)^2}{9}}$$

```python
def purificacion_bbpssw(F: float) -> float:
    """Una ronda del protocolo de purificación BBPSSW."""
    numerador   = F**2 + (1-F)**2 / 9
    denominador = F**2 + 2*F*(1-F)/3 + 5*(1-F)**2 / 9
    return numerador / denominador

F_inicial = 0.80
F = F_inicial
rondas = 0
print(f'Purificación BBPSSW desde F={F_inicial:.2f}:')
while F < 0.99 and rondas < 10:
    F_nueva = purificacion_bbpssw(F)
    rondas += 1
    print(f'  Ronda {rondas}: F = {F:.4f} → {F_nueva:.4f}')
    F = F_nueva
print(f'\nAlcanzado F > 0.99 en {rondas} rondas (consumiendo 2^{rondas} pares)')
```

---

## Estado experimental 2024-2025

| Hito | Grupo | Año | Distancia |
|---|---|---|---|
| Primer entanglement swapping | Zeilinger et al. | 1998 | ~1 m |
| Swapping sobre fibra | Briegel et al. | 2003 | 10 km |
| Swapping vía satélite (Micius) | Pan et al. (China) | 2017 | 1200 km |
| Primer repetidor de 2ª gen. | Delft (QuTech) | 2022 | 10 km |
| Red cuántica de 3 nodos | QuTech | 2023 | ~50 km |
| Entrelazamiento vía satélite GEO | China | 2025 | >36000 km |

---

**Referencias:**
- Briegel et al., *Phys. Rev. Lett.* 81, 5932 (1998) — propuesta de repetidores
- Yin et al., *Science* 356, 1140 (2017) — Micius satellite entanglement
- Pompili et al., *Science* 372, 259 (2021) — red de 3 nodos (QuTech)
- Azuma et al., *Rev. Mod. Phys.* 95, 045006 (2023) — revisión repetidores
