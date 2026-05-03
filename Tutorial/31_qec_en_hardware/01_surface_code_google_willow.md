# Código de superficie en Google Willow: debajo del umbral por primera vez

**Módulo 31 · Artículo 1 · Nivel muy avanzado**

---

## El experimento histórico de Google (2024)

En diciembre de 2024, Google publicó en *Nature* el primer experimento donde
un **código de superficie más grande tiene menos errores que uno más pequeño**,
cruzando el umbral de corrección de errores cuánticos de forma experimental.

Esto es el hito análogo a demostrar que un ordenador clásico con más transistores
funciona mejor que uno con menos —algo que ahora parece obvio pero que requirió
décadas de ingeniería de proceso.

**Resultado clave del paper:**

> "We demonstrate that increasing the code distance from d=3 to d=5 reduces the
> logical error rate per cycle by a factor of ~2, and d=7 reduces it by a factor
> of ~4, consistent with below-threshold operation."

---

## Procesador Willow: arquitectura

El chip Willow tiene **105 qubits superconductores** (transmons) en una rejilla 2D:

| Parámetro | Valor |
|---|---|
| Qubits totales | 105 |
| T1 mediano | ~100 μs |
| T2 mediano | ~150 μs |
| Fidelidad puerta 1Q | ~99,9% |
| Fidelidad puerta 2Q (CZ) | ~99,7% |
| Error de readout | ~0,5% |
| Frecuencia de reloj del ciclo de síndrome | ~1 μs |

Los qubits del experimento de QEC son de dos tipos:
- **Data qubits:** almacenan el qubit lógico.
- **Measure qubits (ancilla):** miden los estabilizadores Z y X.

Para un código de distancia d, se necesitan d² data qubits y (d²-1) measure qubits,
para un total de 2d²-1 qubits físicos.

| Distancia | Qubits físicos |
|---|---|
| d=3 | 17 |
| d=5 | 49 |
| d=7 | 97 |

---

## Protocolo del experimento

El experimento mide el **tasa de error lógica por ciclo de síndrome** usando
el código de superficie de repetición (que protege solo contra errores X o Z, no ambos).

### Ciclo de síndrome

Cada ciclo de síndrome consiste en:

1. **Puertas CZ** entre data qubits y ancilla (en secuencia paralela de 4 CNOTs).
2. **Medición de ancilla** en base Z (para estabilizadores ZZ) o X (para XX).
3. **Reset de ancilla** para el siguiente ciclo.
4. **Decodificación:** el algoritmo MWPM procesa los síndromes.

```
Ciclo de síndrome d=3 (código de repetición bit-flip):

D0 — CZ — D1 — CZ — D2
      |          |
     A01        A12
      |          |
   measure    measure
```

### Decodificación con MWPM

El decodificador MWPM (Minimum Weight Perfect Matching) recibe el **grafo de síndromes**:
- Cada cambio en el síndrome (flip de medición) es un nodo del grafo.
- MWPM encuentra el emparejamiento de mínimo peso (mínimo número de errores que lo explica).
- Si el peso de la corrección es impar, el error lógico ocurre.

```python
# Ejemplo conceptual: decodificación MWPM simple
import numpy as np

def simular_sindrome_bit_flip(p_error: float, n_ciclos: int, d: int) -> list:
    """Simula síndromes de un código de repetición 1D con d qubits."""
    rng = np.random.default_rng(42)
    # Estado inicial: todos en |0⟩
    data = np.zeros(d, dtype=int)
    historial_sindrome = []

    for _ in range(n_ciclos):
        # Errores de bit-flip con probabilidad p_error
        errores = rng.random(d) < p_error
        data ^= errores.astype(int)

        # Síndrome: paridad entre vecinos (d-1 bits de síndrome)
        sindrome = data[:-1] ^ data[1:]
        historial_sindrome.append(sindrome.copy())

    return historial_sindrome, data

# Simular código d=5 con p_error = 0.5% (debajo del umbral)
síndromes, estado_final = simular_sindrome_bit_flip(0.005, 100, 5)
errores_no_corregidos = sum(estado_final)
print(f'Código d=5, p=0.5%: {errores_no_corregidos} errores lógicos en 100 ciclos')
```

---

## Resultados: cruzando el umbral

El paper de Google (Acharya et al., *Nature* 2024) reporta:

| Distancia | Error lógico por ciclo | Factor de mejora |
|---|---|---|
| d=3 | ~3,0 × 10⁻³ | referencia |
| d=5 | ~1,6 × 10⁻³ | ~1,9× |
| d=7 | ~7,5 × 10⁻⁴ | ~4,0× |

Cada incremento de distancia en 2 reduce el error por un factor ~2.
Esto es consistente con la predicción teórica:

$$
p_L(d) \approx A \left(\frac{p_{\text{fís}}}{p_{th}}\right)^{\lceil d/2 \rceil}
$$

Con p_fís ≈ 0,3-0,5% y p_th ≈ 1%, el ratio p_fís/p_th ≈ 0,4 → factor de mejora ≈ 0,4 por nivel.

---

## El problema del tiempo de decodificación

Un desafío práctico del QEC es que el decodificador debe funcionar en tiempo real:

```python
# Restricción de tiempo real para el decodificador
t_ciclo_sindrome = 1e-6     # 1 μs
T2_qubit = 100e-6           # 100 μs

n_ciclos_disponibles = T2_qubit / t_ciclo_sindrome  # = 100 ciclos
print(f'Ciclos antes de decoherencia: {n_ciclos_disponibles:.0f}')

# El decodificador MWPM debe completarse en < 1 μs para no crear backlog
# Los decodificadores actuales de hardware tardan ~10-100 μs en CPU clásica
# Solución: FPGAs dedicadas o decodificadores aproximados más rápidos
print('Requisito de decodificación: < 1 μs por ciclo')
print('Decodificadores actuales: ~10-100 μs → backlog problem')
```

**Backlog problem:** Si el decodificador es más lento que el ciclo de síndrome,
los errores se acumulan más rápido de lo que se procesan. Google resuelve esto
con un decodificador jerárquico ("Union-Find" simplificado para la capa inferior).

---

## Implicaciones para el roadmap fault-tolerant

El experimento de Willow demuestra que los superconductores ya están operando
**por debajo del umbral de corrección de errores cuánticos**. El siguiente paso
es escalar a distancias mayores (d = 25-30) para alcanzar errores lógicos de 10⁻¹⁰
necesarios para algoritmos útiles como Shor o QPE de química.

**Hoja de ruta resultante:**

| Hito | Qubits físicos | Error lógico | Año estimado |
|---|---|---|---|
| d=7 (Willow) | ~100 | ~10⁻⁴ | 2024 (alcanzado) |
| d=15 | ~450 | ~10⁻⁷ | 2027-2028 |
| d=27 | ~1500 | ~10⁻¹⁰ | 2031-2033 |
| RSA-2048 (Shor) | ~60M | ~10⁻¹⁰ | 2035+ |

**Referencia:** Acharya et al., "Quantum error correction below the surface code threshold",
*Nature* 638, 920–926 (2025).
