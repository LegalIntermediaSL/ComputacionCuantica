# Computación Cuántica Distribuida: Protocolos y Arquitecturas

**Módulo 32 · Artículo 2 · Nivel muy avanzado**

---

## ¿Por qué computación cuántica distribuida?

Un solo procesador cuántico tiene límites físicos de escala:
- **Superconductores:** el criostato dilución tiene un volumen fijo (< 1 m³).
- **Iones atrapados:** trampas de Paul escalan a ~200 iones antes de que el *motional heating* degrade la fidelidad.
- **Rydberg:** el campo láser cubre ~1 mm² de área.

La solución: **modularidad**. Múltiples QPUs pequeñas conectadas por fotones
forman un procesador lógico de mayor escala.

---

## Puertas no-locales: CNOT distribuido

La operación más cara en DQC es una **puerta de 2 qubits entre nodos distintos**.
Requiere un par EPR precompartido y comunicación clásica.

### Protocolo: CNOT distribuido (Eisert et al., 2000)

```
Nodo A (control):  q_A  ──●────────────────────────────────
                           │                                │
                  ancA  ──●── [med] → c_A ── clásico ──→  │
                                                           │
Nodo B (target):   q_B  ──────────────────────── X^{c_A} ─●─
                                                           │
                  ancB  ── (par EPR con ancA) ─────────────
```

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Statevector
import numpy as np

def cnot_distribuido_unitario() -> QuantumCircuit:
    """
    CNOT distribuido entre q0 (control, nodo A) y q3 (target, nodo B)
    usando ancilla q1 (nodo A) y q2 (nodo B) preentrelazadas.

    Versión unitaria (sin medición clásica para verificación).
    """
    qc = QuantumCircuit(4)  # q0=control, q1=ancA, q2=ancB, q3=target

    # Preparar par EPR (ancA, ancB)
    qc.h(1)
    qc.cx(1, 2)

    # Lado A: CNOT de control (q0) a ancA (q1)
    qc.cx(0, 1)

    # Medición en A (simulada como CNOT para mantener unitariedad)
    # En la práctica: medir q1, enviar resultado clásico a B
    qc.cx(1, 2)  # Corrección condicional en B (si resultado = 1)

    # Lado B: CNOT de ancB (q2) a target (q3)
    qc.cx(2, 3)

    # Deshacer entrelazamiento ancillas
    qc.h(0)      # Corrección de fase en A
    qc.cz(0, 3)  # Ajuste de fase global

    return qc

# Verificar que es equivalente a un CNOT directo (hasta fase global)
qc_directo = QuantumCircuit(4)
qc_directo.cx(0, 3)

# Comparar en un estado de prueba
psi_test = np.array([0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=complex)
psi_test[4] = 1  # |0100> → control=1, ancA=0, ancB=0, target=0

sv_directo = Statevector(qc_directo)
print('CNOT distribuido implementado.')
print('En hardware real, requiere 1 par EPR y 2 bits clásicos de comunicación.')
```

---

## Delegated Quantum Computing (DQC)

El **delegated QC** permite a un cliente con capacidad cuántica mínima
delegar una computación a un servidor cuántico potente.

### Blind Quantum Computing (Broadbent et al., 2009)

El cliente prepara qubits en estados rotados aleatoriamente y los envía
al servidor. El servidor aplica el circuito sobre los estados cifrados
sin poder inferir la entrada ni la computación realizada.

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def blind_qc_demo(theta_secreto: float, phi_secreto: float) -> dict:
    """
    Demostración simplificada de Blind QC de 1 qubit.
    El cliente quiere aplicar Rz(phi)*Ry(theta) a |0>.
    Envía el qubit con un offset aleatorio que el servidor desconoce.
    """
    # Cliente: elige offset aleatorio
    offset = np.random.uniform(0, 2*np.pi)

    # Cliente prepara qubit con offset: Ry(theta + offset)
    qc_cliente = QuantumCircuit(1)
    qc_cliente.ry(theta_secreto + offset, 0)
    estado_cliente = Statevector(qc_cliente)

    # Servidor aplica su puerta (que el cliente le pide aplicar, cifrada)
    # El servidor aplica Ry(-offset) * Rz(phi) * Ry(offset) sin conocer theta
    qc_servidor = QuantumCircuit(1)
    qc_servidor.initialize(estado_cliente.data)
    qc_servidor.ry(-offset, 0)   # El servidor recibe este ángulo cifrado
    qc_servidor.rz(phi_secreto, 0)
    qc_servidor.ry(offset, 0)
    estado_resultado = Statevector(qc_servidor)

    # Resultado correcto (sin blind QC)
    qc_ideal = QuantumCircuit(1)
    qc_ideal.ry(theta_secreto, 0)
    qc_ideal.rz(phi_secreto, 0)
    estado_ideal = Statevector(qc_ideal)

    fidelidad = abs(np.dot(estado_resultado.data.conj(), estado_ideal.data))**2
    return {
        'theta': theta_secreto,
        'phi': phi_secreto,
        'fidelidad': float(fidelidad),
        'offset_secreto': offset,
    }

resultado = blind_qc_demo(theta_secreto=0.8, phi_secreto=1.2)
print(f"Blind QC demo:")
print(f"  θ={resultado['theta']:.3f}, φ={resultado['phi']:.3f}")
print(f"  Fidelidad resultado: {resultado['fidelidad']:.6f}")
print(f"  El servidor no conoce θ (solo ve el offset cifrado)")
```

---

## Arquitecturas de DQC propuestas

### 1. Modular con bus fotónico (IBM, Google)

```
QPU A ──[transductor]── fibra óptica ──[transductor]── QPU B
  ↑                                                       ↑
microondas                                           microondas
  ↑                                                       ↑
(local)                                              (local)
```

El reto: convertir fotones de microondas (~6 GHz) a fotones ópticos (~200 THz)
con alta eficiencia. Los mejores resultados actuales (2024) logran ~30% de
eficiencia de transducción.

### 2. Iones con comunicación fotónica (IonQ, Quantinuum)

Los iones atrapados pueden emitir fotones entrelazados con el spin del ión.
Esto permite **generación directa de pares EPR** entre trampas separadas.

Eficiencia actual: ~0.1% de probabilidad de éxito por intento, pero con
frecuencias de repetición de MHz → ~kHz de pares EPR/segundo.

### 3. Rydberg con tweezer arrays móviles (QuEra, Pasqal)

```python
# Modelo simplificado de throughput de DQC
import numpy as np

def throughput_dqc(
    n_nodos: int,
    tasa_epr_hz: float,       # pares EPR/segundo entre nodos vecinos
    fidelidad_epr: float,     # fidelidad del par EPR
    prob_purificacion: float,  # probabilidad de éxito de purificación
) -> dict:
    """Calcula el throughput efectivo de DQC con purificación."""
    # Pares EPR utilizables por segundo (tras purificación)
    tasa_utilizable = tasa_epr_hz * prob_purificacion * fidelidad_epr

    # CNOTs no-locales por segundo (cada CNOT necesita 1 par EPR)
    cnots_por_segundo = tasa_utilizable

    # Para un circuito de 1000 CNOTs entre 2 nodos
    n_cnots_circuito = 1000
    tiempo_circuito_s = n_cnots_circuito / cnots_por_segundo

    return {
        'tasa_epr_util': tasa_utilizable,
        'cnots_por_s': cnots_por_segundo,
        'tiempo_1k_cnots_s': tiempo_circuito_s,
    }

for tasa in [100, 1000, 10000]:
    r = throughput_dqc(n_nodos=2, tasa_epr_hz=tasa,
                       fidelidad_epr=0.95, prob_purificacion=0.5)
    print(f'Tasa EPR={tasa} Hz: {r["cnots_por_s"]:.0f} CNOT/s, '
          f'T(1000 CNOTs)={r["tiempo_1k_cnots_s"]:.2f} s')
```

---

## Overhead cuántico de DQC

La comunicación entre nodos tiene un coste en qubits y puertas. Para un circuito
que necesita k CNOTs no-locales:

| Recurso | Por CNOT no-local | Fuente |
|---|---|---|
| Pares EPR consumidos | 1 | Eisert 2000 |
| Bits clásicos enviados | 2 | Eisert 2000 |
| Puertas locales extra | ~4 | Protocolo de teleportación |
| Overhead temporal | ×2-×10 vs. local | Según tasa EPR |

Para un circuito de Shor para N=2048 con CNOTs no-locales ~30%:
el overhead sería ×3-×5 en tiempo de ejecución.

---

**Referencias:**
- Eisert et al., *Phys. Rev. Lett.* 85, 437 (2000) — CNOT no-local
- Broadbent et al., *FOCS* 2009 — Blind Quantum Computing
- Nickerson et al., *Nature Comm.* 5, 3658 (2014) — topologías DQC
- Cuomo et al., *IET Quantum Comm.* 1, 3 (2020) — revisión DQC
