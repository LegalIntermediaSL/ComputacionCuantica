# Química cuántica: FeMoco y la simulación de sistemas de correlación fuerte

**Módulo 30 · Artículo 1 · Nivel avanzado**

---

## El problema del nitrógeno y FeMoco

La fijación de nitrógeno (N₂ → 2NH₃) es uno de los procesos biológicos más importantes
del planeta. La enzima nitrogenasa lo lleva a cabo a temperatura ambiente gracias a su
cofactor de hierro-molibdeno, conocido como **FeMoco** (Fe₇MoS₉C).

El proceso industrial Haber-Bosch requiere 400–500 °C, 200 atm y consume el
**1–2 % de la energía global**. Si se pudiera diseñar un catalizador bioinspirido
mejorando la comprensión computacional de FeMoco, el ahorro energético sería enorme.

El problema: FeMoco tiene 54 electrones en orbitales de correlación fuerte.
Los métodos clásicos de DFT (Density Functional Theory) fallan cualitativamente.
CCSD(T), el estándar de oro clásico, escala como O(N^7) y es computacionalmente
intractable para este sistema.

---

## ¿Cuántos qubits lógicos se necesitan?

La simulación exacta de FeMoco requiere representar el espacio de Hilbert del
sistema electrónico activo. Con la representación de segunda cuantización:

$$N_{\text{qubits}} = 2 \times N_{\text{orbitales}}$$

Para FeMoco con espacio activo (54e, 54 orbitales):

| Representación | Qubits | Viable en |
|---|---|---|
| Full CI (exacto) | ~108 | Nunca (clásico o cuántico) |
| CAS(54,54) activo | 108 | Hardware FT con ~10⁶ qubits |
| CAS reducido (20,20) | 40 | Hardware FT con ~10⁵ qubits |
| Embedding + FT | ~200 lógicos | Estimado ~2030-2035 |

---

## Algoritmo: QPE sobre el hamiltoniano de segunda cuantización

El algoritmo de referencia para química cuántica es la **Quantum Phase Estimation (QPE)**
combinada con preparación de estado de referencia (Hartree-Fock) y evolución unitaria
por trotalización del hamiltoniano de Fermi-Hubbard en segunda cuantización.

### Hamiltoniano electrónico

$$H = \sum_{pq\sigma} h_{pq} a^\dagger_{p\sigma} a_{q\sigma}
    + \frac{1}{2}\sum_{pqrs\sigma\tau} h_{pqrs} a^\dagger_{p\sigma} a^\dagger_{r\tau} a_{s\tau} a_{q\sigma}$$

Tras la transformación de Jordan-Wigner o Bravyi-Kitaev, se convierte en una suma de
operadores de Pauli. Para FeMoco activo:

- ~10⁶ términos de Pauli.
- Cada término se implementa como un phase gadget.
- Necesidad de Trotterización con paso δt ~ 0,01 Ha⁻¹.

### Recursos estimados (2020 — artículo Google/Babbush)

```
Qubits lógicos:    ~200
Puertas T:         ~10^10
Tiempo de ejecución (d=27, t_sindrome=1μs): ~10 días
```

Estos números asumen hardware fault-tolerant con error físico ε = 10⁻³.

---

## Comparativa con métodos clásicos

| Método clásico | Escala | Aplicable a FeMoco |
|---|---|---|
| DFT | O(N³) | Sí, pero inexacto |
| CCSD(T) | O(N⁷) | No (N > 50 e⁻) |
| DMRG (1D) | O(N³ × D³) | Parcialmente |
| Monte Carlo cuántico (QMC) | O(N³) | Sí, pero tiene signo problemático |
| CASSCF (CAS reducido) | Exponencial en activo | Solo CAS pequeños |

El **problema del signo** de QMC (sign problem) hace que los métodos Monte Carlo
diverjan exponencialmente para sistemas fermiónicos con frustración. Los computadores
cuánticos no padecen este problema.

---

## ¿Cuándo hay ventaja cuántica en química?

La ventaja cuántica se alcanza cuando:

$$T_{\text{cuántico}} < T_{\text{clásico}} \times C_{\text{relativo}}$$

Para FeMoco con QPE vs. mejor QMC clásico:

- **T_cuántico:** ~10 días en hardware FT (estimado 2030+)
- **T_clásico (QMC):** indefinido por sign problem (no converge)

Para moléculas sin sign problem (H₂, LiH, BeH₂):

- Los mejores ordenadores clásicos resuelven hasta ~20 orbitales exactamente.
- Ventaja cuántica esperada con ~40-50 qubits lógicos (alcanzable ~2028-2030).

---

## Código de ejemplo: VQE para H₂ como caso reducido

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import EfficientSU2
from qiskit.primitives import StatevectorEstimator
from scipy.optimize import minimize
import numpy as np

# Hamiltoniano H2 mínimo (STO-3G, 2 qubits)
H_h2 = SparsePauliOp.from_list([
    ("II", -1.0523),
    ("ZI",  0.3979),
    ("IZ", -0.3979),
    ("ZZ", -0.0112),
    ("XX",  0.1809),
])

ansatz = EfficientSU2(2, reps=2, entanglement="linear")
estimator = StatevectorEstimator()

historia = []
def coste(params):
    bound = ansatz.assign_parameters(params)
    resultado = estimator.run([(bound, H_h2)]).result()
    e = float(resultado[0].data.evs)
    historia.append(e)
    return e

np.random.seed(42)
x0 = np.random.uniform(-np.pi, np.pi, ansatz.num_parameters)
res = minimize(coste, x0, method="COBYLA", options={"maxiter": 300})

print(f"VQE H₂: E = {res.fun:.6f} Ha  (FCI: -1.8572 Ha)")
print(f"Error vs FCI: {abs(res.fun - (-1.8572))*1000:.2f} mHa")
# Criterio de precisión química: error < 1.6 mHa (~1 kcal/mol)
```

---

## Horizonte temporal realista

| Año | Hardware disponible | Resultado posible |
|---|---|---|
| 2025-2027 | ~1000 qubits físicos, NISQ | VQE para moléculas pequeñas (<10 e⁻ activos) |
| 2028-2030 | FT con ~10⁴ qubits físicos | QPE exacta para H₂O, N₂ (calidad química) |
| 2030-2035 | FT con ~10⁶ qubits físicos | FeMoco completo, catálisis heterogénea |
| 2035+ | FT a gran escala | Diseño de catalizadores de nova generación |

---

## Conclusión

La simulación cuántica de FeMoco es el **caso de uso de química con mayor impacto potencial**.
Sin embargo, requiere recursos fault-tolerant que no estarán disponibles antes de 2030-2035.

En el corto plazo (2025-2028), los casos de uso más accesibles son moléculas pequeñas
con sign problem (frustrated magnets) donde incluso 50-100 qubits lógicos pueden dar
resultados científicamente útiles no alcanzables clásicamente.

**Lectura recomendada:** Babbush et al., *npj Quantum Information* (2018); Lee et al., *PRX Quantum* (2021).
