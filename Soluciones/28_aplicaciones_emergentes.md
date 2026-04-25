# Soluciones — Módulo 28: Aplicaciones Emergentes

Problemas de práctica para los artículos `04_benchmarking_nisq_y_quantum_volume.md` y `05_perspectivas_y_hoja_de_ruta.md`.

---

## Problema 1 — Cálculo manual de Quantum Volume

**Enunciado:** Un procesador tiene 5 qubits con fidelidad de puerta CNOT del 99,2 % y conectividad lineal. Estime su Quantum Volume.

**Solución:**

El Quantum Volume se define como QV = 2^n donde n es el mayor entero tal que un circuito cuadrado aleatorio de n×n capas supera el umbral del 66,7 % de éxito.

Para n = 5:
- Número de CNOTs en el circuito: cada capa tiene ≈ n/2 = 2 CNOTs → total ≈ n × (n/2) = 12 CNOTs.
- Fidelidad acumulada: F ≈ F_CNOT^{n_CNOT} = 0.992^12 ≈ 0.908.
- Umbral: 0.908 > 0.667 → el circuito pasa con n = 5.

Para n = 6:
- CNOTs: 6 × 3 = 18 → F ≈ 0.992^18 ≈ 0.865 > 0.667 → también pasa.

El límite real depende de la conectividad: con conectividad lineal, hay overhead de SWAP (≈ 3 CNOTs por SWAP). Con n = 5 y conectividad lineal, el overhead reduce la fidelidad efectiva, siendo el QV típicamente menor que en all-to-all.

**Conclusión:** Con conectividad lineal y F_2Q = 99,2 %, el QV estimado es **QV = 32** (n = 5) en condiciones óptimas, pero puede ser menor en práctica debido al overhead de routing.

```python
import numpy as np

F_cnot = 0.992
for n in range(2, 10):
    n_cnots = n * (n // 2)  # approx CNOTs per square circuit
    F_eff = F_cnot ** n_cnots
    qv = 2**n if F_eff > 2/3 else None
    print(f"n={n}: F_eff={F_eff:.4f}, QV={2**n if F_eff > 2/3 else 'no'}")
```

---

## Problema 2 — Zero-Noise Extrapolation manual

**Enunciado:** Se ejecuta un circuito de estimación de energía y se obtienen los resultados siguientes bajo ruido amplificado:

| Factor de escala λ | ⟨H⟩ medido |
|---|---|
| 1 | -1.2145 |
| 2 | -1.1203 |
| 3 | -1.0261 |

Estima el valor ideal (λ → 0) usando extrapolación lineal y Richardson de orden 2.

**Solución:**

**Extrapolación lineal:**

Ajuste lineal E(λ) = a + b·λ:

```python
import numpy as np

lambdas = np.array([1, 2, 3])
E = np.array([-1.2145, -1.1203, -1.0261])

# Regresión lineal
coeffs = np.polyfit(lambdas, E, 1)
E0_lineal = np.polyval(coeffs, 0)
print(f"E0 (lineal): {E0_lineal:.4f}")  # ≈ -1.3087
```

**Extrapolación Richardson de orden 2:**

Usando los puntos λ = 1 y λ = 2:

E0 = (4·E(1) - E(2)) / 3 = (4·(-1.2145) - (-1.1203)) / 3 = (-4.858 + 1.1203) / 3 ≈ **-1.2459**

Usando los tres puntos (orden 2 completo):

```python
# Richardson con 3 puntos: E0 = (9*E1 - 4*E2 + E3) / 6  [aprox.]
E1, E2, E3 = -1.2145, -1.1203, -1.0261
E0_rich = (9*E1 - 4*E2 + E3) / 6   # no exacto; el coef. depende del modelo
# Forma exacta: resolución del sistema lineal
A = np.vstack([np.ones(3), lambdas, lambdas**2]).T
coeffs2 = np.linalg.solve(A[:3,:3], E[:3])
E0_poly = coeffs2[0]
print(f"E0 (Richardson 2º orden): {E0_poly:.4f}")
```

**Interpretación:** La extrapolación lineal da un límite superior; Richardson de orden mayor es más precisa pero requiere más puntos y mayor varianza en cada estimación.

---

## Problema 3 — Benchmark de ventaja cuántica

**Enunciado:** Google afirma que Willow resuelve en 5 minutos un sampling problem que un supercomputador clásico tardaría 10^25 años. ¿Qué caveats metodológicos debes considerar al evaluar esta afirmación?

**Solución:**

1. **Instancia elegida a dedo:** El circuito de Random Circuit Sampling (RCS) fue diseñado para ser difícil clásicamente, no para resolver un problema práctico. No hay garantía de que sea el mejor problema posible para el adversario clásico.

2. **Algoritmo clásico de referencia:** Las estimaciones clásicas usan simuladores basados en contracción de redes tensoriales. El mejor algoritmo clásico conocido mejora continuamente; la ventaja puede reducirse.

3. **Verificación del resultado:** Con circuitos de n > 50 qubits, no se puede verificar exactamente el resultado cuántico (el espacio de Hilbert es demasiado grande). Se usa el test de cross-entropy benchmarking (XEB), que mide correlación con predicciones de circuitos pequeños.

4. **Sin utilidad práctica:** RCS no resuelve ningún problema de optimización, simulación o criptografía. La ventaja es en computabilidad, no en aplicaciones.

5. **Escala de ruido:** El experimento solo es válido para la profundidad de circuito donde el procesador Willow mantiene coherencia. Para circuitos más profundos, el ruido domina y la "computación" es ruido aleatorio.

**Conclusión:** La afirmación es técnicamente válida pero altamente específica al problema elegido. La ventaja cuántica general para problemas de interés práctico sigue sin demostrarse a fecha de 2024.

---

## Problema 4 — Cálculo de CLOPS

**Enunciado:** Un procesador ejecuta 1000 capas de circuito en 2,5 segundos, incluyendo 100 ms de latencia clásica por capa. Calcula el CLOPS.

**Solución:**

```python
n_capas = 1000
t_total = 2.5  # segundos
t_latencia_clasica = 0.1  # s por capa
t_total_efectivo = t_latencia_clasica * n_capas  # tiempo que domina el bucle

CLOPS = n_capas / t_total
print(f"CLOPS observado: {CLOPS:.0f}")  # 400 CLOPS

# Para comparar: IBM Eagle reporta ~2100 CLOPS con primitivas V2
# La diferencia se debe a latencia clásica de control
```

**Discusión:** La latencia clásica (compilación, comunicación con el QPU) domina el tiempo total en muchos sistemas NISQ actuales. Reducirla es clave para algoritmos variacionales iterativos.
