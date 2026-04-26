# QKD y Criptografía Cuántica

**Módulo 32 · Artículo 3 · Nivel muy avanzado**

---

## El problema de la distribución de claves

En criptografía clásica, la seguridad del intercambio de claves (Diffie-Hellman,
RSA) depende de la dificultad computacional de factorizar números grandes.
El algoritmo de Shor rompe RSA en tiempo polinomial → **amenaza existencial** a la
criptografía actual con llegada de QC fault-tolerant.

Hay dos respuestas complementarias:
1. **Post-Quantum Cryptography (PQC):** algoritmos clásicos resistentes a QC.
2. **Quantum Key Distribution (QKD):** seguridad garantizada por las leyes de la física.

---

## BB84: el protocolo fundacional

Propuesto por Bennett y Brassard en 1984, BB84 permite establecer una clave
secreta con seguridad incondicional (demostrable por la mecánica cuántica).

### Protocolo

```
Alice (emisora)               Bob (receptor)
  ┌────────────────────────────────────────┐
  │ 1. Prepara qubits en bases aleatorias  │
  │    Bases: Z={|0⟩,|1⟩} o X={|+⟩,|−⟩} │
  │ 2. Envía los qubits a Bob              │─── canal cuántico ───►
  │                                        │
  │ 3. Bob mide en bases aleatorias        │◄── canal clásico ────
  │ 4. Reconciliación de bases públicas    │
  │ 5. Estimación del QBER                 │
  │ 6. Amplificación de privacidad         │
  └────────────────────────────────────────┘
```

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

def bb84_simulacion(n_bits: int = 100, qber_eavesdrop: float = 0.0,
                    seed: int = 42) -> dict:
    """
    Simula el protocolo BB84.

    qber_eavesdrop: fracción de qubits interceptados por Eve (introduce QBER=0.25*p).
    """
    rng = np.random.default_rng(seed)

    # Alice prepara bits y bases
    bits_alice  = rng.integers(0, 2, n_bits)   # 0 o 1
    bases_alice = rng.integers(0, 2, n_bits)    # 0=Z, 1=X

    # Bob elige bases
    bases_bob = rng.integers(0, 2, n_bits)

    # Simulación de transmisión (con posible escucha de Eve)
    bits_bob_recibidos = []
    for i in range(n_bits):
        qc = QuantumCircuit(1)
        # Alice prepara el qubit
        if bits_alice[i] == 1:
            qc.x(0)
        if bases_alice[i] == 1:  # base X
            qc.h(0)

        # Eve intercepta con probabilidad qber_eavesdrop
        if rng.random() < qber_eavesdrop:
            base_eve = rng.integers(0, 2)
            if base_eve == 1:
                qc.h(0)  # Eve mide en base equivocada, reenvía estado colapsado
            # Eve re-prepara el estado (introduce ruido)
            bit_eve = rng.integers(0, 2)  # resultado aleatorio de Eve
            qc2 = QuantumCircuit(1)
            if bit_eve == 1:
                qc2.x(0)
            if base_eve == 1:
                qc2.h(0)
            # Bob mide el estado re-preparado por Eve
            if bases_bob[i] == 1:
                qc2.h(0)
            qc2.measure_all()
            counts = StatevectorSampler().run([qc2], shots=1).result()[0].data.meas.get_counts()
            bit_medido = int(list(counts.keys())[0])
        else:
            # Sin Eve: Bob mide directamente
            if bases_bob[i] == 1:
                qc.h(0)
            qc.measure_all()
            counts = StatevectorSampler().run([qc], shots=1).result()[0].data.meas.get_counts()
            bit_medido = int(list(counts.keys())[0])

        bits_bob_recibidos.append(bit_medido)

    bits_bob = np.array(bits_bob_recibidos)

    # Reconciliación de bases (público)
    bases_iguales = (bases_alice == bases_bob)
    clave_alice = bits_alice[bases_iguales]
    clave_bob   = bits_bob[bases_iguales]

    # Cálculo del QBER (en una fracción de prueba)
    n_prueba = max(1, len(clave_alice) // 4)
    idx_prueba = rng.choice(len(clave_alice), n_prueba, replace=False)
    errores = np.sum(clave_alice[idx_prueba] != clave_bob[idx_prueba])
    qber = errores / n_prueba

    # Clave final (sin los bits usados en prueba)
    idx_clave = np.setdiff1d(np.arange(len(clave_alice)), idx_prueba)
    clave_final = clave_alice[idx_clave]

    return {
        'n_bits_enviados': n_bits,
        'n_bases_iguales': int(np.sum(bases_iguales)),
        'n_clave_final': len(clave_final),
        'qber': float(qber),
        'seguro': qber < 0.11,  # umbral de seguridad BB84
        'tasa_generacion': len(clave_final) / n_bits,
    }

# Sin Eve
r0 = bb84_simulacion(1000, qber_eavesdrop=0.0)
print(f'Sin Eve: QBER={r0["qber"]:.3f}, clave={r0["n_clave_final"]} bits, '
      f'tasa={r0["tasa_generacion"]:.2f}')

# Con Eve (25% intercepción)
r1 = bb84_simulacion(1000, qber_eavesdrop=0.25)
print(f'Con Eve: QBER={r1["qber"]:.3f}, seguro={r1["seguro"]}, '
      f'clave={r1["n_clave_final"]} bits')
```

### Análisis del QBER

El **Quantum Bit Error Rate (QBER)** es la fracción de bits donde Alice y Bob
obtienen resultados distintos cuando usaron la misma base:

| Escenario | QBER esperado |
|---|---|
| Sin ruido, sin Eve | 0% |
| Solo ruido de canal (fibra típica) | 1-3% |
| Eve intercepta el 50% de los qubits | ~12.5% |
| Eve intercepta el 100% | ~25% |
| Umbral de seguridad BB84 | < 11% |

---

## E91: protocolo basado en entrelazamiento

Propuesto por Artur Ekert en 1991, usa pares EPR. Las correlaciones cuánticas
entre Alice y Bob son mayores que cualquier teoría de variables ocultas (desigualdad de Bell).

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

def e91_correlaciones(n_pares: int = 1000, seed: int = 0) -> dict:
    """
    Simula correlaciones E91 para verificar la violación de Bell.
    Alice y Bob miden en ángulos a₀=0°, a₁=45°, b₀=22.5°, b₁=67.5°.
    """
    rng = np.random.default_rng(seed)
    angulos_alice = [0, np.pi/4]
    angulos_bob   = [np.pi/8, 3*np.pi/8]

    correlaciones = {}
    for a_idx, a in enumerate(angulos_alice):
        for b_idx, b in enumerate(angulos_bob):
            resultados_alice = []
            resultados_bob   = []

            for _ in range(n_pares // 4):
                # Par EPR
                qc = QuantumCircuit(2)
                qc.h(0); qc.cx(0, 1)
                # Alice mide en ángulo a
                qc.ry(-2*a, 0)
                # Bob mide en ángulo b
                qc.ry(-2*b, 1)
                qc.measure_all()

                counts = StatevectorSampler().run([qc], shots=1).result()[0].data.meas.get_counts()
                bits = list(counts.keys())[0]
                # Convertir a ±1
                r_alice = 1 - 2*int(bits[1])  # qubit 0 (bit derecho en Qiskit)
                r_bob   = 1 - 2*int(bits[0])  # qubit 1
                resultados_alice.append(r_alice)
                resultados_bob.append(r_bob)

            E_ab = np.mean(np.array(resultados_alice) * np.array(resultados_bob))
            correlaciones[(a_idx, b_idx)] = E_ab

    # Parámetro S de Bell (CHSH)
    S = (correlaciones[(0,0)] - correlaciones[(0,1)] +
         correlaciones[(1,0)] + correlaciones[(1,1)])

    return {
        'correlaciones': correlaciones,
        'S_chsh': S,
        'viola_bell': abs(S) > 2,
        'S_cuantico_teorico': 2*np.sqrt(2),
    }

r = e91_correlaciones(2000)
print(f'Parámetro CHSH S = {r["S_chsh"]:.3f}  (límite clásico: 2, cuántico: 2√2 ≈ {r["S_cuantico_teorico"]:.3f})')
print(f'¿Viola la desigualdad de Bell? {r["viola_bell"]}')
```

---

## Twin-Field QKD: récord de distancia

El protocolo **Twin-Field QKD** (TF-QKD, 2018) supera el límite lineal de
transmisión de BB84 usando interferencia cuántica en un nodo central.

**Tasa de clave vs. distancia:**

| Protocolo | Distancia máxima | Tasa a 300 km |
|---|---|---|
| BB84 clásico | ~200 km | < 1 bit/s |
| BB84 con decoy | ~500 km | ~10 bit/s |
| TF-QKD | ~830 km (2023) | ~1 kbit/s |
| MDI-QKD | ~400 km | ~100 bit/s |

```python
import numpy as np
import matplotlib.pyplot as plt

# Tasas de clave vs. distancia (modelos simplificados)
distancias = np.linspace(0, 800, 200)
eta_fibra = 10**(-0.2/10)  # 0.2 dB/km en unidades lineales

def tasa_bb84(d):
    eta = eta_fibra**d
    if eta < 1e-10: return 0
    return max(0, eta * (1 - 2 * 0.02))  # 2% QBER de ruido

def tasa_tf_qkd(d):
    # TF-QKD escala como sqrt(eta) en vez de eta
    eta = eta_fibra**d
    if eta < 1e-15: return 0
    return max(0, np.sqrt(eta) * 0.1)

tasas_bb84  = np.array([tasa_bb84(d) for d in distancias])
tasas_tf    = np.array([tasa_tf_qkd(d) for d in distancias])

fig, ax = plt.subplots(figsize=(9, 5))
mask84 = tasas_bb84 > 1e-12
maskTF = tasas_tf   > 1e-12
ax.semilogy(distancias[mask84], tasas_bb84[mask84], 'b-', lw=2, label='BB84 (∝ η)')
ax.semilogy(distancias[maskTF], tasas_tf[maskTF],   'r-', lw=2, label='TF-QKD (∝ √η)')
ax.set_xlabel('Distancia (km)'); ax.set_ylabel('Tasa de clave (arbitraria)')
ax.set_title('Tasa de clave QKD vs. distancia')
ax.legend(); ax.grid(alpha=0.3)
plt.tight_layout(); plt.show()
```

---

## PQC vs. QKD: la comparativa honesta

| Criterio | PQC (CRYSTALS-Kyber) | QKD (BB84) |
|---|---|---|
| Fundamento | Dificultad computacional (retícula) | Leyes de la física |
| Infraestructura | Software (drop-in replacement) | Fibra dedicada / satélites |
| Distancia máxima | Sin límite (internet) | ~1000 km (TF-QKD) |
| Tasa de clave | Gbps | kbps-Mbps (local) |
| Coste | Bajo (solo software) | Alto (hardware especializado) |
| Estandarización | NIST PQC 2024 ✅ | Sin estándar global |
| Amenaza cuántica | Conjetura (no demostrado roto) | Incondicionalmente seguro |

**Conclusión:** PQC es la solución práctica a corto plazo. QKD es complementario
para comunicaciones de alta seguridad donde la infraestructura lo justifica
(financiero, gubernamental, defensa).

---

**Referencias:**
- Bennett & Brassard, *Proc. IEEE Int. Conf. Comp.* 1984 — BB84
- Ekert, *Phys. Rev. Lett.* 67, 661 (1991) — E91
- Lucamarini et al., *Nature* 557, 400 (2018) — TF-QKD
- Liu et al., *Nature* 622, 57 (2023) — TF-QKD 830 km récord
- NIST, *FIPS 203* (2024) — ML-KEM (CRYSTALS-Kyber) estándar PQC
