# Soluciones: Hardware Real, PQC y ZX-Calculus (Módulos 23-26)

---

## Módulo 23: Hardware Físico

### Ejercicio 1: Anharmonicidad del transmón

**Enunciado:** Calcular $\alpha$ para $E_C/h = 300\,\text{MHz}$ y $E_J/E_C = 50$.

**Solución:**

En el régimen de transmón ($E_J \gg E_C$), la anharmonicidad es aproximadamente:
$$
\alpha \approx -E_C/\hbar \approx -E_C/h \text{ (en unidades de frecuencia)}
$$

```python
E_C_MHz = 300  # MHz
E_J_over_E_C = 50
E_J_MHz = E_C_MHz * E_J_over_E_C  # 15000 MHz

# Anharmonicidad
alpha_MHz = -E_C_MHz
print(f"E_C/h = {E_C_MHz} MHz")
print(f"E_J/h = {E_J_MHz} MHz")
print(f"E_J/E_C = {E_J_over_E_C}")
print(f"α ≈ -E_C/h = {alpha_MHz} MHz")
print(f"Frecuencia de transición ω_q ≈ √(8 E_J E_C)/h - E_C/h")

import numpy as np
omega_q = np.sqrt(8 * E_J_MHz * E_C_MHz) - E_C_MHz
print(f"ω_q ≈ {omega_q:.1f} MHz = {omega_q/1000:.3f} GHz")
```

**Resultado:** $\alpha \approx -300\,\text{MHz}$ (la anharmonicidad es igual a $-E_C/h$). La frecuencia de transición es $\omega_q \approx \sqrt{8 \times 15000 \times 300} - 300 \approx 5969\,\text{MHz} \approx 5.97\,\text{GHz}$.

---

### Ejercicio 2: Desplazamiento dispersivo

**Enunciado:** Calcular $\chi$ para $g = 100\,\text{MHz}$ y $\Delta = 1\,\text{GHz}$.

**Solución:**

En el régimen dispersivo ($\Delta \gg g$):
$$
\chi = \frac{g^2}{\Delta}
$$

```python
g = 100e6     # 100 MHz en Hz
Delta = 1e9   # 1 GHz en Hz

chi = g**2 / Delta
print(f"g = {g/1e6:.0f} MHz")
print(f"Δ = {Delta/1e9:.1f} GHz")
print(f"χ = g²/Δ = {chi/1e6:.1f} MHz")
print(f"Diferencia de frecuencia de cavidad: 2χ = {2*chi/1e6:.1f} MHz")
```

**Resultado:** $\chi = (100\,\text{MHz})^2 / (1000\,\text{MHz}) = 10\,\text{MHz}$. La diferencia de frecuencia de la cavidad entre $|0\rangle$ y $|1\rangle$ es $2\chi = 20\,\text{MHz}$, suficientemente grande para discriminar los estados.

---

### Ejercicio 3: CNOTs en la ventana de coherencia

**Enunciado:** Comparar la duración de un CNOT por Cross-Resonance ($t \approx 300\,\text{ns}$) con $T_2 = 200\,\mu\text{s}$.

**Solución:**

```python
T2 = 200e-6    # s
t_CR = 300e-9  # s

n_max = T2 / t_CR
print(f"T2 = {T2*1e6:.0f} μs")
print(f"t_CNOT (CR) = {t_CR*1e9:.0f} ns")
print(f"Número máximo de CNOTs: {n_max:.0f}")
print(f"Profundidad efectiva de algoritmo: ~{n_max/3:.0f} (estimando 3 CNOTs por capa)")
```

**Resultado:** Se pueden ejecutar hasta 667 CNOTs dentro de una ventana de coherencia de $200\,\mu s$, equivalente a ~222 capas de circuito (asumiendo 3 CNOTs por capa en promedio).

---

## Módulo 24: Control de Pulsos

### Ejercicio 4: Anchura espectral vs anharmonicidad DRAG

**Enunciado:** Para $\sigma = 10\,\text{ns}$, calcular $\Delta\omega$ y comparar con $|\alpha|/2\pi = 250\,\text{MHz}$.

**Solución:**

Un pulso gaussiano con $\sigma$ tiene anchura espectral $\Delta\omega \approx 1/\sigma$ (en rad/s).

```python
import numpy as np
sigma = 10e-9   # s
alpha_Hz = 250e6  # 250 MHz

Delta_omega = 1 / sigma  # rad/s
Delta_f = Delta_omega / (2 * np.pi)  # Hz

print(f"σ = {sigma*1e9:.0f} ns")
print(f"Δω = 1/σ = {Delta_omega/1e9:.3f} Grad/s")
print(f"Δf = Δω/2π = {Delta_f/1e6:.1f} MHz")
print(f"|α|/2π = {alpha_Hz/1e6:.0f} MHz")

if Delta_f > alpha_Hz:
    print("ALERTA: Δf > |α| — el pulso excitará el nivel |2⟩")
    print("Solución: aumentar σ o usar DRAG")
else:
    print("OK: Δf < |α| — la fuga al nivel |2⟩ es suprimida")
```

**Resultado:** $\Delta f = 1/(2\pi \times 10\,\text{ns}) = 15.9\,\text{MHz} < 250\,\text{MHz} = |\alpha|/2\pi$. El pulso de 10 ns es suficientemente selectivo para no excitar el nivel $|2\rangle$. Para pulsos más cortos ($\sigma < 0.6\,\text{ns}$) sería necesario DRAG.

---

## Módulo 25: Criptografía Post-Cuántica

### Ejercicio 5: Tamaños de clave RSA vs PQC

**Enunciado:** Comparar los tamaños de clave pública, clave privada y firma para RSA-2048, ECDSA-256 y Dilithium3.

**Solución:**

| Algoritmo | Clave pública | Clave privada | Firma | Seguridad |
|---|---|---|---|---|
| RSA-2048 | 256 bytes | 1232 bytes | 256 bytes | 112 bits (clasico) |
| ECDSA-256 | 64 bytes | 32 bytes | 64 bytes | 128 bits (clasico) |
| Dilithium2 (FIPS 204) | 1312 bytes | 2528 bytes | 2420 bytes | 128 bits (post-cuántico) |
| Dilithium3 | 1952 bytes | 4000 bytes | 3293 bytes | 192 bits (post-cuántico) |
| SPHINCS+-128s | 32 bytes | 64 bytes | 7856 bytes | 128 bits (post-cuántico) |

```python
algos = {
    "RSA-2048":       {"pk": 256,   "sk": 1232,  "sig": 256,  "sec": "112 (clás.)"},
    "ECDSA-256":      {"pk": 64,    "sk": 32,    "sig": 64,   "sec": "128 (clás.)"},
    "Dilithium2":     {"pk": 1312,  "sk": 2528,  "sig": 2420, "sec": "128 (PQC)"},
    "Dilithium3":     {"pk": 1952,  "sk": 4000,  "sig": 3293, "sec": "192 (PQC)"},
    "SPHINCS+-128s":  {"pk": 32,    "sk": 64,    "sig": 7856, "sec": "128 (PQC)"},
}

print(f"{'Algoritmo':<18} {'PK (bytes)':<12} {'SK (bytes)':<12} {'Firma (bytes)':<15} {'Seguridad'}")
print("-" * 70)
for name, data in algos.items():
    print(f"{name:<18} {data['pk']:<12} {data['sk']:<12} {data['sig']:<15} {data['sec']}")
```

**Observación clave:** Dilithium tiene claves ~20× más grandes que ECDSA, pero la verificación es eficiente. SPHINCS+ tiene claves muy pequeñas pero firmas muy grandes.

---

## Módulo 26: ZX-Calculus

### Ejercicio 6: CNOT $\equiv$ CZ con puertas Hadamard

**Enunciado:** Demostrar que $\text{CNOT}_{01} = (I \otimes H) \cdot \text{CZ}_{01} \cdot (I \otimes H)$.

**Solución algebraica:**

La puerta CZ aplica $|11\rangle \to -|11\rangle$ y deja el resto invariante. Aplicando $H$ al qubit 1 antes y después:

$$
H|0\rangle = |+\rangle, \quad H|1\rangle = |-\rangle
$$

$$
(I \otimes H) \text{CZ} (I \otimes H)|00\rangle = (I \otimes H)\text{CZ}|0+\rangle = (I \otimes H)|0+\rangle = |00\rangle
$$
$$
(I \otimes H) \text{CZ} (I \otimes H)|01\rangle = (I \otimes H)|0-\rangle = |01\rangle
$$
$$
(I \otimes H) \text{CZ} (I \otimes H)|10\rangle = (I \otimes H)\text{CZ}|1+\rangle = (I \otimes H)(-|1-\rangle + ... ) = |11\rangle
$$

Esto coincide con la tabla de verdad de CNOT. Verificación numérica:

```python
import numpy as np

H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
CZ   = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,-1]])
IH   = np.kron(np.eye(2), H)

CNOT_via_CZ = IH @ CZ @ IH
print("CNOT vía CZ:")
print(np.round(CNOT_via_CZ.real))
print("\nCNOT directo:")
print(CNOT)
print(f"\n¿Son iguales? {np.allclose(CNOT_via_CZ, CNOT)}")
```

**En ZX-Calculus:** la araña Z del control + araña X del target (CNOT) equivale a dos arañas Z conectadas (CZ) con una caja amarilla (H) en el cable del target. La regla de cambio de color confirma la equivalencia.
