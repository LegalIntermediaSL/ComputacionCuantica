# Soluciones — Módulo 29: Fault-Tolerant Computing

Problemas de práctica para los artículos `01_threshold_theorem.md`, `02_magic_state_distillation.md` y `03_hoja_de_ruta_fault_tolerant.md`.

---

## Problema 1 — Error lógico del código de superficie

**Enunciado:** Un código de superficie de distancia d = 5 opera con tasa de error física ε = 0,3 % (por debajo del umbral ε_th ≈ 1 %). Calcula el error lógico estimado.

**Solución:**

El error lógico del código de superficie se modela como:

$$p_L \approx A \left(\frac{\varepsilon}{\varepsilon_{th}}\right)^{\lceil d/2 \rceil}$$

Con A ≈ 0.1 (constante empírica), ε = 0,003, ε_th = 0,01, d = 5:

```python
import numpy as np

epsilon = 0.003        # error fisico
epsilon_th = 0.01      # umbral
d = 5                  # distancia del codigo
A = 0.1               # constante empirica

exponent = np.ceil(d / 2)   # = 3 para d=5
p_L = A * (epsilon / epsilon_th) ** exponent

print(f"Exponente: {exponent:.0f}")
print(f"ε/ε_th = {epsilon/epsilon_th:.3f}")
print(f"Error lógico p_L ≈ {p_L:.2e}")  # ≈ 2.7e-4
```

**Resultado:** p_L ≈ 2,7 × 10⁻⁴ para d = 5.

Para d = 7 con los mismos parámetros:

```python
for d in [3, 5, 7, 9, 11]:
    pL = A * (epsilon / epsilon_th) ** int(np.ceil(d/2))
    print(f"d={d}: p_L ≈ {pL:.2e}")
```

| d | ⌈d/2⌉ | p_L |
|---|---|---|
| 3 | 2 | 9.0 × 10⁻³ |
| 5 | 3 | 2.7 × 10⁻⁴ |
| 7 | 4 | 8.1 × 10⁻⁶ |
| 9 | 5 | 2.4 × 10⁻⁷ |
| 11 | 6 | 7.3 × 10⁻⁹ |

**Conclusión:** Cada incremento en distancia suprime el error en un factor (ε/ε_th) ≈ 0,3 adicional.

---

## Problema 2 — Overhead de recursos para Shor RSA-2048

**Enunciado:** El algoritmo de Shor para RSA-2048 requiere aproximadamente 4096 qubits lógicos y 10⁸ puertas lógicas. Si el error lógico objetivo por puerta es 10⁻¹⁰ y el error físico es ε = 10⁻³, calcula:
a) La distancia d necesaria para el código de superficie.
b) El número total de qubits físicos.
c) El tiempo de ejecución si cada operación de síndrome tarda 1 μs.

**Solución:**

**a) Distancia del código:**

Necesitamos p_L < 10⁻¹⁰. Usando la fórmula:

```python
import numpy as np

p_L_target = 1e-10
epsilon = 1e-3
epsilon_th = 1e-2
A = 0.1

# Resolver: A * (ε/ε_th)^ceil(d/2) < p_L_target
# log(p_L_target/A) = ceil(d/2) * log(ε/ε_th)
ratio = np.log(p_L_target / A) / np.log(epsilon / epsilon_th)
d_min = int(np.ceil(2 * ratio))
if d_min % 2 == 0:
    d_min += 1   # d debe ser impar para codigos de superficie

print(f"Distancia mínima necesaria: d = {d_min}")  # d ≈ 27
```

**Resultado:** d ≈ 27 (distancia impar; en la práctica se usa d = 27 o d = 29).

**b) Qubits físicos:**

El código de superficie de distancia d requiere d² qubits de datos + ≈ d²-1 ancilla ≈ 2d² qubits físicos por qubit lógico.

```python
d = 27
n_logicos = 4096
fisicos_por_logico = 2 * d**2   # ≈ 1458 por qubit logico
# Factor de overhead para magic state distillation: ~10x adicional
overhead_msd = 10
n_fisicos_total = n_logicos * fisicos_por_logico * overhead_msd

print(f"Físicos por qubit lógico (solo código): {fisicos_por_logico}")
print(f"Total con overhead MSD: {n_fisicos_total:,}")  # ~60 millones
```

| Componente | Qubits físicos |
|---|---|
| Datos lógicos (4096 × d²) | ~3M |
| Ancilla de síndrome (≈ igual) | ~3M |
| Magic state factories (overhead ×10) | ~60M |
| **Total estimado** | **~60-100M** |

**c) Tiempo de ejecución:**

```python
n_puertas_logicas = 1e8
d = 27
t_sindrome_us = 1   # microsegundos por ciclo de síndrome

# Cada puerta lógica requiere O(d) ciclos de síndrome
ciclos_por_puerta = d
t_por_puerta_us = ciclos_por_puerta * t_sindrome_us

t_total_us = n_puertas_logicas * t_por_puerta_us
t_total_horas = t_total_us / (3600 * 1e6)

print(f"Tiempo por puerta lógica: {t_por_puerta_us} μs")
print(f"Tiempo total: {t_total_horas:.1f} horas")  # ≈ 0.75 horas
```

**Resultado:** Con síndrome de 1 μs, Shor RSA-2048 tomaría aproximadamente **1 hora** en un procesador fault-tolerant de 60M qubits con d = 27.

---

## Problema 3 — Protocolo de distilación de magic states

**Enunciado:** El protocolo 15→1 distila 15 copias de un estado T con fidelidad F = 0,99 en 1 copia con alta fidelidad. Calcula la fidelidad de salida y el número de copias del estado físico necesarias para obtener 1 magic state con p_L < 10⁻¹².

**Solución:**

**Fidelidad del protocolo 15→1:**

El protocolo 15→1 tiene un error de salida proporcional al cuadrado del error de entrada:

```python
import numpy as np

F_entrada = 0.99
epsilon_entrada = 1 - F_entrada  # error inicial = 0.01

# Protocolo 15->1: epsilon_salida ≈ 35 * epsilon_entrada^3
epsilon_salida_nivel1 = 35 * epsilon_entrada**3
F_salida_nivel1 = 1 - epsilon_salida_nivel1
print(f"Nivel 1: ε_out = {epsilon_salida_nivel1:.2e}, F = {F_salida_nivel1:.8f}")

# Nivel 2: distilacion en cascada
epsilon_salida_nivel2 = 35 * epsilon_salida_nivel1**3
F_salida_nivel2 = 1 - epsilon_salida_nivel2
print(f"Nivel 2: ε_out = {epsilon_salida_nivel2:.2e}")
```

**Resultado:**
- Nivel 1: ε_out ≈ 3,5 × 10⁻⁵ → F ≈ 0,999965
- Nivel 2: ε_out ≈ 1,5 × 10⁻¹³ → ¡Supera p_L < 10⁻¹²!

**Copias necesarias para p_L < 10⁻¹²:**

```python
# Nivel 1: consume 15 copias físicas → 1 copia nivel 1
# Nivel 2: consume 15 copias nivel 1 → cada una costó 15 copias físicas
copias_nivel2 = 15 * 15  # = 225 copias físicas

print(f"Copias físicas por magic state nivel 2: {copias_nivel2}")
```

**Overhead de magic state distillation:** Para obtener 1 magic state de alta calidad (ε < 10⁻¹²) con F_entrada = 0,99, se necesitan **225 copias físicas** del estado T crudo.

**Implicación para Shor RSA-2048:** Con 10⁸ puertas T y 225 copias por magic state, se necesitan ≈ 2,25 × 10¹⁰ estados T físicos. La factory de distilación debe producirlos a tasa suficiente para no ser el cuello de botella. Esto motiva el diseño de fábricas de magic states eficientes en los planes de Google y IBM.
