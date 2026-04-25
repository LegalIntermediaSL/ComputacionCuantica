# Hoja de Ruta hacia la Computación Cuántica Tolerante a Fallos

## 1. El estado del arte en 2024-2025

La computación cuántica tolerante a fallos (FTQC, Fault-Tolerant Quantum Computing) es el objetivo final de la industria cuántica. En 2024 se cruzaron dos hitos históricos:

1. **Google Willow** (diciembre 2024): primera demostración experimental de escalado subcrítico de errores con el código de superficie.
2. **IBM Heron** (2024): primera arquitectura modular con conexiones cuánticas entre chips y tasa de error 2Q < 0.3%, bajo el umbral del código de superficie.

El camino desde el hardware actual hasta FTQC a escala es largo pero trazado. Este artículo mapea las rutas de los principales actores y los hitos cuantitativos esperados.

---

## 2. IBM: cómputo centrado en cuántica

### 2.1 Filosofía arquitectural

IBM apuesta por la integración de procesadores cuánticos como **aceleradores especializados** en sistemas de cómputo clásico de alta potencia (quantum-centric supercomputing). La idea no es un ordenador cuántico monolítico sino una red de módulos cuánticos interconectados con canales clásicos de alta velocidad.

### 2.2 Hoja de ruta técnica

```
2019: Q System One (27q, QV=32)
  └── Primer sistema cuántico comercial en armario

2021: Eagle (127q)
  └── Primera arquitectura de plano único >100q

2022: Osprey (433q)
  └── Primer chip >400q

2023: Condor (1121q) + Heron (133q)
  └── Condor: mayor chip por número de qubits
  └── Heron: nueva arquitectura, error 2Q < 0.3%, modular

2024: Heron r2 + Flamingo
  └── Comunicación cuántica entre módulos mediante interconexiones de microondas
  └── Primeros "circuitos entre chips"

2025: Kookaburra (1386q efectivos por módulo)
  └── Red de 3 módulos Heron interconectados

2028: ~10.000 qubits físicos
  └── Primeros qubits lógicos útiles (d=7, ~100 lógicos)

2033: >100.000 qubits físicos
  └── FTQC a escala: miles de qubits lógicos
  └── Primera aplicación con ventaja práctica demostrable
```

### 2.3 Desafíos técnicos de IBM

- **Interconexión cuántica:** transmitir el estado cuántico entre chips con alta fidelidad.
- **Control clásico en tiempo real:** latencia de decodificación de síndrome < 1 μs para ciclos de corrección de 1 μs.
- **Compilación cruzada:** optimizar circuitos para topologías de múltiples módulos heterogéneos.

```python
# Estimación de qubits lógicos disponibles con la hoja de ruta IBM
import numpy as np

roadmap_ibm = {
    2024: {"phys": 133, "p_2q": 0.003, "T2_us": 300},
    2025: {"phys": 1386, "p_2q": 0.002, "T2_us": 500},
    2028: {"phys": 10000, "p_2q": 0.001, "T2_us": 1000},
    2033: {"phys": 100000, "p_2q": 0.0005, "T2_us": 2000},
}

p_th = 0.01
print(f"{'Año':>6} {'Qubits físicos':>16} {'Distancia d':>12} {'Qubits lógicos':>16}")
for year, data in roadmap_ibm.items():
    p = data["p_2q"]
    if p < p_th:
        # Distancia mínima para p_L < 10^-6
        d = max(3, int(np.ceil(np.log(1e-6 / 0.1) / np.log(p / p_th))) * 2 + 1)
        d = min(d, 27)
        n_logical = data["phys"] // (2 * d**2)
        print(f"{year:>6} {data['phys']:>16,} {d:>12} {n_logical:>16}")
    else:
        print(f"{year:>6} {data['phys']:>16,} {'sobre umbral':>12} {'—':>16}")
```

---

## 3. Google: escalado experimental

### 3.1 Estrategia

Google sigue una estrategia de **demostraciones experimentales incrementales**, publicando hitos en *Nature* que validan la teoría antes de escalar:

```
2019: Sycamore (53q)
  └── Supremacía cuántica: RCS en 200 segundos vs. 10.000 años (clásico, entonces)

2023: Experimento de corrección de errores en Sycamore
  └── Primer escalado del código de superficie d=3→5 en hardware
  └── Error lógico NO decrecía — aún sobre el umbral

2024: Willow (105q)
  └── Primera demostración de escalado subcrítico: d=3,5,7 con error decreciente
  └── RCS: ventaja vs. supercomputadores clásicos por factor astronómico
  └── p_phys < p_th confirmado experimentalmente

2029 (objetivo): Primer cálculo útil tolerante a fallos
  └── Simulación de molécula FeMoco con ventaja demostrada sobre clásico

2033+ (objetivo): FTQC a escala con miles de qubits lógicos
```

### 3.2 Arquitectura Willow

Willow usa transmones superconductores en una topología de rejilla cuadrada con conectividad a primeros vecinos (idéntica al código de superficie). Los parámetros clave:

| Parámetro | Valor (Willow 2024) |
|---|---|
| Qubits | 105 |
| T1 (promedio) | ~100 μs |
| T2 (promedio) | ~150 μs |
| Fidelidad 1Q | ~99.9% |
| Fidelidad 2Q (CZ) | ~99.7% |
| Tiempo de puerta CZ | ~25 ns |
| Ciclo de síndrome | ~1 μs |

---

## 4. Microsoft: qubits topológicos

### 4.1 La apuesta diferenciada

Microsoft no compite directamente con IBM y Google en la carrera de qubits superconductores. En cambio, apuesta por una arquitectura radicalmente distinta basada en **estados de Majorana**, una forma de materia topológica que codifica información de forma intrínsecamente protegida contra errores locales.

### 4.2 Fermiones de Majorana

Un fermión de Majorana es su propia antipartícula: $\gamma = \gamma^\dagger$. En ciertos sistemas semiconductores (InAs o InSb en contacto con superconductores), pueden aparecer modos de Majorana en los extremos del sistema.

**Ventaja topológica:**
- La información cuántica está codificada en la **paridad no-abeliana** de los modos de Majorana.
- Los errores locales (fluctuaciones de temperatura, ruido electromagnético) no pueden distinguir los estados de paridad sin mover físicamente los modos de Majorana por el sistema completo.
- El umbral de error efectivo es mucho más alto: $p_{th}^{\text{Majorana}} \sim 10-20\%$ vs. $\sim 1\%$ para superconductores convencionales.
- El overhead de corrección de errores puede ser $\sim 10\times$-$100\times$ menor.

### 4.3 Estado experimental (2025)

- 2023: Microsoft publicó en *Nature* evidencia de estados de Majorana en dispositivos InAs-Al.
- 2024: Demostración de manipulación coherente de un qubit topológico.
- 2025 (objetivo): Primer qubit topológico de demostración funcional.
- 2030+ (objetivo): Procesador topológico con overhead de QEC reducido.

**Controversia:** la ruta topológica es más incierta experimentalmente. Reproducir y escalar los estados de Majorana es un desafío de física experimental de primer nivel.

---

## 5. Quantinuum: iones atrapados de alta fidelidad

### 5.1 Ventajas de los iones

Los iones atrapados (Yb⁺ en Quantinuum, Ca⁺ en IonQ) tienen propiedades únicas:

| Propiedad | Superconductores | Iones atrapados |
|---|---|---|
| T2 | ~100-400 μs | 1-100 segundos |
| Fidelidad 2Q | ~99.5-99.8% | ~99.8-99.9% |
| Conectividad | Local (rejilla) | Total (all-to-all) |
| Velocidad de puerta 2Q | ~100-500 ns | ~100-1000 μs |
| Temperatura operación | ~20 mK | ~μK |

La conectividad total es especialmente valiosa: en el código de superficie, la arquitectura de rejilla es natural para superconductores pero artificial para iones.

### 5.2 Hoja de ruta Quantinuum

```
2023: H2 (56q, QV=32768, F_2Q=99.8%)
  └── Mayor Quantum Volume del mercado

2024: H2-1 + corrección de errores
  └── Primeros qubits lógicos funcionales con error lógico < error físico

2025: H3 (~64q con QEC nativa)
  └── Primeros algoritmos ejecutados en qubits lógicos de iones

2028: Procesador de cómputo cuántico universal con decenas de qubits lógicos
```

---

## 6. Códigos cuánticos de próxima generación

Los códigos de superficie tienen overhead $O(d^2)$ en qubits físicos por qubit lógico. Investigación reciente apunta a códigos con mejor relación:

### 6.1 Códigos qLDPC (Quantum Low-Density Parity Check)

Los códigos qLDPC permiten tasas $k/n$ constantes (no decrecientes con $n$), lo que en principio permite overheads $O(1)$ por qubit lógico.

**Código de Gross (2024):** tasa $k/n = 2/15$, distancia $d \propto \sqrt{n}$. IBM lo anunció como candidato para hardware modular.

**Código bivariate bicycle (Bravyi et al., 2024):** $[[144, 12, 12]]$ — 144 qubits físicos para 12 qubits lógicos de distancia 12. Requiere 12 qubits físicos por qubit lógico vs. ~50-100 para el código de superficie equivalente.

```python
# Comparación de overhead: superficie vs. qLDPC
import numpy as np

print(f"{'Código':>25} {'[[n,k,d]]':>15} {'n/k (overhead)':>16}")
print("-" * 60)

codes = [
    ("Superficie d=7",    "[[98, 1, 7]]",    98),
    ("Superficie d=11",   "[[242, 1, 11]]",  242),
    ("Bivariate bicycle", "[[144, 12, 12]]", 12),
    ("Gross code",        "[[360, 12, 12]]", 30),
]

for name, params, overhead in codes:
    print(f"{name:>25} {params:>15} {overhead:>16.0f}")
```

### 6.2 Desafíos de los qLDPC en hardware

- Requieren conectividad no-local (qubits que no son vecinos próximos deben interactuar).
- Difíciles de implementar en topologías 2D de superconductores.
- Compatibles con arquitecturas de iones (conectividad total) y con interconexiones cuánticas entre módulos.

---

## 7. El cuadro completo: timeline consolidado

```
2024 ── Willow: primer escalado subcrítico (Google)
     ── Heron: primer error 2Q < p_th en IBM
     ── Quantinuum H2: QV=32768
     
2025 ── Primeros qubits lógicos persistentes en hardware de iones
     ── IBM Kookaburra: primer sistema modular real
     ── Microsoft: primer qubit topológico (objetivo)
     
2027 ── ~100 qubits lógicos de alta calidad (d=7, superconductores)
     ── Primeras ventajas en química cuántica (moléculas pequeñas)
     
2030 ── ~1000 qubits lógicos
     ── Shor para RSA-512 demostrado
     ── FeMoco simulado con ventaja sobre clásico
     
2033 ── ~10.000 qubits lógicos (IBM objetivo)
     ── Primeras aplicaciones industriales: materiales, optimización
     
2035+ ── RSA-2048 amenazado (requiere ~4000 qubits lógicos, d=27)
      ── FTQC general con millones de qubits físicos
```

---

## 8. Implicaciones para la criptografía

El impacto más mediático de la FTQC es la amenaza a RSA y curvas elípticas (ECDSA). Las respuestas:

**NIST PQC (2024):** estándares post-cuánticos aprobados:
- ML-KEM (Kyber): criptografía de clave pública post-cuántica.
- ML-DSA (Dilithium): firma digital post-cuántica.
- SLH-DSA (SPHINCS+): firma basada en hash.

**Store now, decrypt later:** adversarios con grandes recursos pueden almacenar comunicaciones cifradas hoy para descifrarlas con ordenadores cuánticos futuros. La migración a PQC es urgente para datos con secreto a largo plazo.

```python
# Timeline de riesgo criptográfico
amenazas = {
    "RSA-512 (demo)":    {"año": 2030, "qubits_logicos": 1000},
    "RSA-1024":          {"año": 2032, "qubits_logicos": 2000},
    "RSA-2048":          {"año": 2036, "qubits_logicos": 4000},
    "ECDSA-256":         {"año": 2033, "qubits_logicos": 2500},
    "AES-128 (Grover)":  {"año": "nunca práctico", "qubits_logicos": ">10^6"},
}

print(f"{'Algoritmo':>22} {'Año estimado':>14} {'Qubits lógicos':>16}")
for alg, data in amenazas.items():
    print(f"{alg:>22} {str(data['año']):>14} {str(data['qubits_logicos']):>16}")
```

---

## 9. Resumen del módulo 29

La tolerancia a fallos cuántica ya no es ciencia ficción: el teorema del umbral está probado, el código de superficie funciona por debajo del umbral en hardware real (Willow, Heron), y la hoja de ruta industrial es concreta y financia millones de dólares de investigación. Los desafíos restantes son de ingeniería y escala, no de principio físico.

El camino completo que has recorrido en este tutorial — desde el qubit y la esfera de Bloch hasta los estados mágicos y los qubits topológicos — es el mapa conceptual que necesitas para seguir la investigación activa en este campo durante los próximos años.

---

*← [02 Magic state distillation](02_magic_state_distillation.md) | [Tutorial: Índice general →](../../Tutorial/indice_general.md)*
