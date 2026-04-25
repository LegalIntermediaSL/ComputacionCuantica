# Código de repetición en IBM 127 qubits: mejora del error lógico con la distancia

**Módulo 31 · Artículo 2 · Nivel muy avanzado**

---

## El experimento de IBM (2023)

IBM realizó en 2023 un experimento de QEC en el procesador **ibm_sherbrooke** de 127 qubits
(arquitectura Eagle r3), demostrando la escalabilidad del código de repetición bit-flip
desde d=3 hasta d=29 en una sola cadena de qubits.

El experimento fue publicado como parte del roadmap de IBM hacia computación tolerante a fallos,
acompañando la demostración de "utility-scale" computation con 127 qubits.

---

## Arquitectura Eagle r3: conectividad relevante

El procesador ibm_sherbrooke tiene topología de acoplamiento **pesada hexagonal**
(*heavy-hex lattice*), donde cada qubit de datos tiene 2-3 vecinos y las puertas
de 2 qubits se implementan con Cross-Resonance (CR).

```
Topología heavy-hex (sección):

D0 — A01 — D1 — A12 — D2 — A23 — D3
             |              |
            A13            A24
             |              |
            D4 — A45 — D5 — A56 — D6
```

Esta topología es **subóptima para el código de superficie** (que necesita rejilla 2D cuadrada),
pero el código de repetición 1D encaja perfectamente en una cadena lineal.

---

## Código de repetición bit-flip en 127 qubits

El experimento implementa un código de repetición de distancia d en una cadena
de d data qubits y d-1 ancilla qubits intercalados:

```
D0 — A01 — D1 — A12 — D2 — ... — D_{d-1}
```

Para el procesador de 127 qubits, la cadena más larga posible tiene ~85 qubits,
permitiendo d hasta 29 (con 29 data + 28 ancilla = 57 qubits, usando la cadena principal).

### Parámetros del procesador ibm_sherbrooke (2023)

| Parámetro | Mediana | Mejor |
|---|---|---|
| T1 | ~200 μs | ~400 μs |
| T2 | ~150 μs | ~300 μs |
| Error puerta 1Q (Rz) | 0.02% | 0.01% |
| Error puerta 2Q (CNOT/ECR) | 0.3-0.7% | 0.15% |
| Error de readout | 1-2% | 0.5% |

---

## Resultados: mejora del error lógico con d

```python
import numpy as np
import matplotlib.pyplot as plt

# Datos del experimento IBM (aproximados del paper)
# Error lógico por ciclo de síndrome vs. distancia
distancias = [3, 5, 7, 9, 11, 15, 19, 25, 29]
# Experimento (con decodificador MWPM, 5 ciclos)
p_logico_exp = [1.8e-2, 9.5e-3, 5.8e-3, 4.1e-3, 3.2e-3, 2.2e-3, 1.8e-3, 1.5e-3, 1.4e-3]
# Predicción teórica (modelo simple con p_fís ≈ 0.5%)
p_fis = 0.005
p_th = 0.10  # umbral alto por topología 1D
p_logico_teorico = [0.15 * (p_fis / p_th)**((d+1)//2) for d in distancias]

fig, ax = plt.subplots(figsize=(9, 5))
ax.semilogy(distancias, p_logico_exp, 'o-', color='#3498db', lw=2, ms=8, label='Experimento IBM 2023')
ax.semilogy(distancias, p_logico_teorico, '--', color='#e74c3c', lw=1.5, label='Modelo teórico (p=0.5%)')
ax.set_xlabel('Distancia d del código de repetición')
ax.set_ylabel('Error lógico por ciclo de síndrome')
ax.set_title('Código de repetición en IBM Eagle 127q — error lógico vs. distancia')
ax.legend()
ax.grid(alpha=0.3, which='both')
plt.tight_layout()
plt.show()

print('Observación: el error logico sí disminuye con d, pero la mejora es menos')
print('pronunciada que en Google Willow, porque IBM Eagle tiene más error físico')
print('y la topología 1D tiene umbral menor que el código de superficie 2D.')
```

---

## Decodificador: MWPM vs. Union-Find

IBM usa dos decodificadores en el experimento:

| Decodificador | Complejidad | Latencia | Calidad |
|---|---|---|---|
| MWPM (Blossom V) | O(n³) | ~100 μs | Óptimo |
| Union-Find | O(n α(n)) ≈ O(n) | ~1 μs | Sub-óptimo (~10% peor) |

Para tiempo real (ciclos de 1 μs), solo Union-Find es viable. MWPM se usa para
post-procesamiento offline de experimentos científicos.

---

## Comparativa IBM vs. Google

| Aspecto | IBM Eagle 127q (2023) | Google Willow (2024) |
|---|---|---|
| Qubits | 127 | 105 |
| Código | Repetición 1D (bit-flip) | Superficie 2D (completo) |
| Distancia máxima | d=29 (lineal) | d=7 (2D) |
| Error lógico (d=7) | ~5×10⁻³ | ~7,5×10⁻⁴ |
| ¿Debajo del umbral? | Sí (para código 1D) | Sí (para código de superficie) |
| Overhead de SWAP | Bajo (topología 1D) | Alto (topología heavy-hex → superficie 2D) |

**Ventaja de Google:** El código de superficie 2D protege contra TODOS los errores
(X, Y, Z), mientras que el código de repetición de IBM solo protege contra bit-flips.
Para computación fault-tolerant universal se necesita el código de superficie.

**Ventaja de IBM:** Chips con más qubits físicos disponibles (127, 433, 1121 qubits)
y accesibilidad pública vía IBM Quantum Network.

---

## Lección técnica: importancia del error de readout

El mayor contribuyente al error lógico en el experimento IBM es el **readout error** (~1-2%),
no el error de puerta (~0,3-0,7%):

```python
# Análisis de contribución de errores
p_gate_1q = 0.0002    # 0.02%
p_gate_2q = 0.005     # 0.5%
p_readout  = 0.015    # 1.5%
p_idle_T1  = 0.001    # decoherencia durante ciclo

# Para d=7: número de operaciones por ciclo
n_puertas_1q_por_ciclo = 2 * 7     # H en ancilla
n_puertas_2q_por_ciclo = 4 * 6     # 4 CNOTs × 6 ancilla
n_readouts_por_ciclo   = 6         # medición de 6 ancilla

p_total_por_ciclo = (
    n_puertas_1q_por_ciclo * p_gate_1q +
    n_puertas_2q_por_ciclo * p_gate_2q +
    n_readouts_por_ciclo   * p_readout
)
print(f'Contribución estimada por ciclo (d=7):')
print(f'  Puertas 1Q:  {n_puertas_1q_por_ciclo * p_gate_1q:.4f}')
print(f'  Puertas 2Q:  {n_puertas_2q_por_ciclo * p_gate_2q:.4f}')
print(f'  Readout:     {n_readouts_por_ciclo * p_readout:.4f}  ← dominante')
print(f'  Total:       {p_total_por_ciclo:.4f}')
```

**Implicación:** Mejorar el readout de 1,5% a 0,1% tendría más impacto en el error lógico
que reducir el error de puerta a la mitad. Esto motiva el trabajo en integradores dispersivos
de alta fidelidad y amplificadores paramétricos cuánticos (parametric amplifiers, QPA).

---

## Conclusión

El experimento de IBM valida que el código de repetición escala correctamente en hardware real.
Sin embargo, el salto a un código de superficie completo requiere:

1. **Topología 2D de qubits** con conectividad all-to-nearest-neighbour (no heavy-hex).
2. **Reducción del error de readout** a < 0,5%.
3. **Decodificadores en tiempo real** a < 1 μs.

IBM está desarrollando el procesador **Heron** (topología modificada, 2024) y el **Flamingo** (2025)
precisamente para abordar estas limitaciones.

**Referencia:** Sundaresan et al., "Demonstrating multi-round subsystem quantum error correction
using matching and maximum likelihood decoders", *Nature Communications* 14, 2852 (2023).
