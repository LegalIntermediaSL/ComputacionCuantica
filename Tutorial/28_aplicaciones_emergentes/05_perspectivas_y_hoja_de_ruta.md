# Perspectivas y Hoja de Ruta: de NISQ a la Computación Cuántica Tolerante a Fallos

## 1. El horizonte actual: era NISQ

El término **NISQ** (Noisy Intermediate-Scale Quantum), acuñado por John Preskill en 2018, describe los procesadores actuales: decenas a miles de qubits físicos, sin corrección de errores completa, con circuitos limitados por la decoherencia. La era NISQ no es una etapa menor: es el laboratorio donde se desarrollan las técnicas algorítmicas, de mitigación y de caracterización que harán posible la siguiente generación.

### 1.1 Limitaciones estructurales de NISQ

- **Profundidad de circuito:** limitada por $T_2$ y la fidelidad de puertas. Para circuitos más profundos que ~100-300 puertas CNOT, el error acumulado supera la señal útil.
- **Overhead de mitigación:** ZNE y PEC mejoran la precisión pero multiplican los shots requeridos por factores $10$-$100\times$, encareciendo el cómputo.
- **Barren plateaus:** el gradiente de los circuitos variacionales decae exponencialmente con el número de qubits en ansätze genéricos, dificultando el entrenamiento.
- **Verificación:** confirmar que un circuito cuántico de $>50$ qubits funcionó correctamente es en sí mismo un problema computacionalmente difícil.

---

## 2. El camino hacia la tolerancia a fallos

### 2.1 Tres eras del cómputo cuántico

```
Era 1 (actual): NISQ
  └── 10³ - 10⁴ qubits físicos
  └── Sin QEC, mitigación de errores
  └── Circuitos superficiales (<300 puertas 2Q)
  └── Aplicaciones: investigación, benchmarking, QML exploratorio

Era 2 (próxima): Early Fault-Tolerant (EFT, ~2028-2032)
  └── 10⁴ - 10⁶ qubits físicos
  └── QEC parcial: unos pocos qubits lógicos de alta calidad
  └── Algoritmos híbridos con qubits lógicos
  └── Aplicaciones: química cuántica, optimización (ventaja estrecha)

Era 3 (objetivo): Full Fault-Tolerant (FT, >2033)
  └── >10⁶ qubits físicos
  └── Miles de qubits lógicos con error < 10⁻¹⁵
  └── Algoritmos de Shor, Grover a escala
  └── Aplicaciones: criptoanálisis, simulación de materiales, optimización
```

### 2.2 El umbral de corrección de errores

El **teorema del umbral** garantiza que si la tasa de error físico por puerta $p < p_{th}$, es posible reducir el error lógico arbitrariamente aumentando el tamaño del código.

Para el código de superficie:
- $p_{th} \approx 1\%$ (con ruido independiente por puerta)
- IBM Heron (2024): $p_{2Q} \approx 0.3\%$ (ya bajo el umbral)
- Google Willow (2024): escalado subcrítico demostrado experimentalmente

```python
import numpy as np
import matplotlib.pyplot as plt

def logical_error_surface_code(p_phys, distance):
    """
    Estimación del error lógico del código de superficie
    de distancia d bajo el umbral (p_phys << p_th).
    """
    p_th = 0.01
    A = 0.1  # prefactor empírico
    return A * (p_phys / p_th) ** ((distance + 1) / 2)

p_vals = np.linspace(0.001, 0.015, 100)
for d in [3, 5, 7, 11]:
    p_L = [logical_error_surface_code(p, d) for p in p_vals]
    plt.semilogy(p_vals * 100, p_L, label=f"d={d}")

plt.axvline(x=1.0, color="red", linestyle="--", label="Umbral ~1%")
plt.xlabel("Error físico por puerta (%)")
plt.ylabel("Error lógico $p_L$")
plt.title("Error lógico del código de superficie vs. error físico")
plt.legend(); plt.grid(alpha=0.3); plt.show()
```

---

## 3. Hojas de ruta de los principales actores (2024-2033)

### 3.1 IBM Quantum

IBM publicó su hoja de ruta "IBM Quantum Development Roadmap":

| Año | Hito | Detalle |
|---|---|---|
| 2023 | Heron (133q) | Error 2Q < 0.3%, nueva arquitectura modular |
| 2024 | Flamingo | Interconexión de chips mediante enlaces cuánticos |
| 2025 | Kookaburra | 1386 qubits, comunicación entre módulos |
| 2028 | ~10.000 qubits | Primeros qubits lógicos útiles |
| 2033 | >100.000 qubits | Cómputo tolerante a fallos a escala |

El concepto clave es **quantum-centric supercomputing**: integrar procesadores cuánticos como aceleradores en sistemas de cómputo clásico de alta potencia, con comunicación cuántica entre módulos.

### 3.2 Google Quantum AI

Google sigue una estrategia de demostraciones experimentales incrementales:

- **2019:** Supremacía cuántica (Sycamore, 53q)
- **2023:** Below-threshold error correction (experimento en Sycamore)
- **2024:** Willow (105q) — primer escalado subcrítico demostrado
- **2029 (objetivo):** Primer cálculo útil tolerante a fallos (química cuántica)

### 3.3 Microsoft: qubits topológicos

Microsoft apuesta por una arquitectura radicalmente diferente: **qubits topológicos** basados en fermiones de Majorana. Su premisa es que los errores son topológicamente protegidos, eliminando el overhead masivo de QEC.

- 2023: Primeras señales de estados de Majorana en dispositivos semiconductores.
- 2025 (objetivo): Qubit topológico funcional de demostración.
- Ventaja potencial: factor $10\times$-$100\times$ menos qubits físicos por qubit lógico.

### 3.4 Quantinuum: iones atrapados de alta fidelidad

Quantinuum (fusión de Honeywell y Cambridge Quantum) opera con iones de iterbio en trampas de iones. Sus ventajas son la altísima fidelidad de puertas (99.9% en 2Q) y la conectividad total (todos los qubits se pueden conectar).

- H2 (2024): 56 qubits, QV = 32768, fidelidad 2Q = 99.8%.
- Estrategia: pocos qubits de muy alta calidad para aplicaciones de precisión.

---

## 4. Aplicaciones con horizonte realista

### 4.1 Corto plazo (2025-2028, NISQ avanzado)

**Química cuántica de molécula pequeña:** VQE con mitigación de errores para moléculas de 10-20 electrones correlacionados, competitivo con CCSD(T) clásico pero sin ventaja de escala.

**Optimización combinatoria (estrecha):** QAOA con $p > 5$ capas podría superar heurísticas clásicas en instancias de grafos de geometría especial (Max-Cut en grafos locales).

**QML para datos cuánticos:** clasificación de estados cuánticos provenientes de experimentos físicos reales (óptica cuántica, física de partículas). Aquí los datos son cuánticos de origen, eliminando el cuello de botella de la codificación.

### 4.2 Medio plazo (2028-2033, EFT)

**Simulación de FeMoco:** el cofactor metálico de la nitrogenasa es clave para la síntesis de amoniaco. Estimaciones sugieren que ~200 qubits lógicos serían suficientes para superizar la simulación clásica más precisa. Impacto potencial: 1-2% del consumo energético mundial (fijación de nitrógeno industrial).

**Factorización de RSA-512:** con ~1000 qubits lógicos y $10^9$ operaciones tolerantes a fallos. No amenaza RSA-2048, pero demostraría Shor a escala relevante.

**Optimización logística y financiera:** QUBO a escala de $10^3$ variables con garantías de aproximación.

### 4.3 Largo plazo (>2033, FT completo)

**RSA-2048 con Shor:** requiere ~4000 qubits lógicos y $10^{12}$ operaciones tolerantes a fallos. Con overhead de surface code ($d \approx 27$), esto implica ~$4 \times 10^6$ qubits físicos. Probable ~2035-2040.

**Simulación de superconductores de alta temperatura:** para diseño de materiales y baterías de próxima generación.

**Descubrimiento de fármacos cuántico:** simulación de proteínas completas con precisión química.

---

## 5. Qué falta para RSA y Grover prácticos

```python
import numpy as np

# Requisitos para Shor en RSA-2048 (Gidney & Ekerå, 2021)
rsa_bits = 2048
logical_qubits_shor = 4 * rsa_bits + 2  # ~8200 qubits lógicos
toffoli_gates = 3 * rsa_bits**3          # ~25×10^9 puertas Toffoli
surface_code_distance = 27               # para p_L < 10^-12
physical_per_logical = 2 * surface_code_distance**2  # ~1458
total_physical = logical_qubits_shor * physical_per_logical

print(f"=== Shor para RSA-{rsa_bits} ===")
print(f"Qubits lógicos:         {logical_qubits_shor:,}")
print(f"Qubits físicos:         {total_physical:,}")
print(f"Puertas Toffoli:        {toffoli_gates:.2e}")
print(f"Tiempo estimado:        ~8 horas (con Heron 2024)")
print()

# Requisitos para Grover: búsqueda en 2^256 (SHA-256)
n_grover = 256
iterations = int(np.pi / 4 * np.sqrt(2**n_grover))
print(f"=== Grover sobre SHA-{n_grover} ===")
print(f"Iteraciones necesarias: 2^{n_grover//2} = {2**(n_grover//2):.2e}")
print(f"Esto NO es cuadráticamente 'fácil': sigue siendo 2^128 operaciones")
print(f"Seguridad AES-128 con Grover: equivalente a AES-64 clásico")
```

---

## 6. El horizonte del software cuántico

El progreso en hardware debe acompañarse de avances en:

- **Compiladores:** transpilación óptima de algoritmos a circuitos hardware-específicos.
- **Optimizadores variacionales:** resistentes a barren plateaus (SPSA, gradiente natural cuántico).
- **Lenguajes de alto nivel:** OpenQASM 3.0, Qiskit 2.x, Cirq permiten expresar algoritmos FT con feed-forward clásico en tiempo real.
- **Simuladores clásicos:** tensor network methods (MPS, PEPS) para verificar circuitos de hasta ~100 qubits de profundidad limitada.

---

## 7. Conclusión del tutorial

Este módulo 28 cierra el recorrido desde los fundamentos del qubit (módulo 01) hasta las fronteras de la investigación actual. El panorama en 2024 muestra un campo en transición acelerada: los primeros procesadores por debajo del umbral de corrección de errores (Willow, Heron) marcan el inicio del camino hacia la computación cuántica tolerante a fallos.

La pregunta ya no es **si** habrá computadoras cuánticas útiles, sino **cuándo** y **para qué aplicaciones primero**. Las apuestas más fundadas apuntan a la simulación cuántica de materiales y química como primera aplicación de ventaja práctica demostrable, seguida de optimización a escala y, a más largo plazo, criptoanálisis.

El siguiente paso para quien ha completado este tutorial es explorar el módulo 29 (fault-tolerant computing) y las bibliografías especializadas en la carpeta `referencias.md`.

---

*← [04 Benchmarking NISQ](04_benchmarking_nisq_y_quantum_volume.md) | [Módulo 13: Límites y realismo →](../13_limites_actuales_y_realismo/README.md)*
