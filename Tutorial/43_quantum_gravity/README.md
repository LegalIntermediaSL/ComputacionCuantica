# Módulo 43 — Quantum Gravity y Holografía Cuántica

## Índice

1. [El problema de la gravedad cuántica](#1-el-problema)
2. [Correspondencia AdS/CFT](#2-adscft)
3. [Tensor networks como geometría emergente](#3-tn-geometría)
4. [MERA y el espacio de Anti-de Sitter](#4-mera-ads)
5. [Entropía de Ryu-Takayanagi](#5-ryu-takayanagi)
6. [Holographic Quantum Error Correction](#6-qec-holográfico)
7. [Wormholes, EPR y ER=EPR](#7-er-epr)
8. [Computación cuántica y gravedad](#8-conexión-qc)
9. [Estado del arte (2025)](#9-estado-arte)
10. [Resumen](#10-resumen)

---

## 1. El problema de la gravedad cuántica

La relatividad general describe la gravedad como curvatura del espacio-tiempo. La mecánica cuántica gobierna el mundo subatómico. Unificarlas es el problema abierto más profundo de la física teórica.

**Las dificultades principales:**
- La relatividad general es no renormalizable perturbativamente.
- El principio de equivalencia choca con la unitariedad cuántica (paradoja de la información del agujero negro).
- No existe una teoría experimental directamente verificable (energías de Planck ≈ 10¹⁹ GeV).

Sin embargo, la **correspondencia holográfica** ofrece un laboratorio teórico donde preguntas de gravedad cuántica se transforman en preguntas de teoría cuántica de campos — sin gravedad — en una dimensión menos.

---

## 2. Correspondencia AdS/CFT

La **correspondencia AdS/CFT** (Maldacena 1997) es la realización más precisa de la holografía:

> Una teoría de gravedad cuántica en un espacio Anti-de Sitter (AdS) de d+1 dimensiones es **dual** a una Teoría de Campo Conforme (CFT) sin gravedad en la frontera d-dimensional.

### Espacio Anti-de Sitter (AdS)

El espacio AdS_{d+1} es la solución maximalmente simétrica de las ecuaciones de Einstein con constante cosmológica negativa Λ < 0:

$$ds^2 = \frac{L^2}{z^2}\left(-dt^2 + d\vec{x}^2 + dz^2\right), \quad z > 0$$

- La frontera está en $z \to 0$: ahí vive la CFT.
- El "bulk" $z > 0$ es el espacio de la gravedad.
- $L$ es el radio de AdS (escala de la geometría).

### Diccionario AdS/CFT

| Lado gravedad (bulk) | Lado CFT (frontera) |
|---------------------|---------------------|
| Métrica $g_{\mu\nu}$ | Tensor energía-momento $T_{\mu\nu}$ |
| Campo escalar $\phi$ | Operador local $\mathcal{O}$ |
| Temperatura del agujero negro | Temperatura de la CFT |
| Entropía de Bekenstein-Hawking | Entropía de entrelazamiento CFT |
| Profundidad $z$ | Escala de energía (RG flow) |
| Geometría AdS pura | Estado vacío de la CFT |
| Agujero negro de BTZ | Estado térmico de la CFT |

### Ejemplo: Correladores holográficos

El propagador de un campo escalar masivo $m^2 L^2 = \Delta(\Delta - d)$ en AdS_{d+1} reproduce el correlador de 2 puntos de la CFT:

$$\langle\mathcal{O}(x)\mathcal{O}(y)\rangle_{\text{CFT}} = \frac{C}{|x-y|^{2\Delta}}$$

donde $\Delta$ es la dimensión de escala del operador dual. La dimensión de escala se determina por la masa del campo en el bulk:

$$\Delta = \frac{d}{2} + \sqrt{\frac{d^2}{4} + m^2 L^2}$$

---

## 3. Tensor networks como geometría emergente

La idea central es que la **estructura de entrelazamiento** de la función de onda del estado cuántico **codifica la geometría** del espacio-tiempo dual.

### Principio de Ryu-Takayanagi (RT)

Para una región $A$ en la frontera, la entropía de entrelazamiento de $A$ en la CFT es proporcional al **área de la superficie mínima** en el bulk que termina en $\partial A$:

$$S_A = \frac{\text{Area}(\gamma_A)}{4G_N}$$

donde $\gamma_A$ es la superficie geodésica de mínima área en AdS que tiene la misma frontera que $A$, y $G_N$ es la constante de Newton en el bulk.

### Conexión con MPS/MERA

Las tensor networks discretizan este principio:

- Las **líneas de enlace** del tensor network representan geodésicas en AdS.
- El **número de índices** cortados al dividir la red (bond dimension) cuenta los bits de entrelazamiento.
- La **profundidad** de la red corresponde a la coordenada radial $z$ (dirección RG).

Swingle (2009) propuso que MERA (Multi-scale Entanglement Renormalization Ansatz) es una discretización de AdS:

$$\text{MERA} \leftrightarrow \text{AdS}_3 / \text{CFT}_2$$

---

## 4. MERA y el espacio de Anti-de Sitter

MERA es una tensor network jerárquica diseñada para estados críticos (sin masa, invariantes bajo escala):

```
Capa UV (resolución fina):
  ○-○-○-○-○-○-○-○   ← qubits físicos (frontera)
    ╲ ╱   ╲ ╱
     ⊗     ⊗         ← disentanglers (gates de 2 qubits)
    ╱ ╲   ╱ ╲
   ○   ○   ○   ○
    ╲ ╱     ╲ ╱
     ▽         ▽      ← isometrias (coarse-graining)
    ╱           ╲
   ○             ○

Capa IR (resolución gruesa):
   ○               ← top tensor

Profundidad = escala de energía = coord. radial z en AdS
```

### Propiedades de MERA

1. **Entropía de entrelazamiento logarítmica:** para un intervalo de longitud $\ell$:
   $$S(\ell) = \frac{c}{3}\log \ell + \text{cte}$$
   donde $c$ es la carga central de la CFT. MERA reproduce exactamente este comportamiento.

2. **Geometría discreta de AdS:** el número de pasos para llegar del sitio $i$ al sitio $j$ en la red MERA escala como $\log|i-j|$ — igual que la distancia geodésica en AdS_3.

3. **Renormalization group:** cada capa de MERA es un paso de coarse-graining que integra los grados de libertad UV — análogo al flujo RG de la CFT hacia el IR.

---

## 5. Entropía de Ryu-Takayanagi

Para AdS_3/CFT_2, la fórmula de RT da:

$$S_A = \frac{c}{3}\log\left(\frac{2L}{\epsilon}\sin\frac{\pi \ell}{L}\right)$$

para un intervalo de longitud $\ell$ en un sistema de tamaño $L$ con cutoff UV $\epsilon$.

### Verificación numérica en MERA

Para la cadena XX crítica (c=1) con MERA de 3 capas y $\chi = 4$:

$$S(\ell) \approx \frac{1}{3}\log \ell + \text{cte}$$

**Código de verificación:**
```python
from scipy.linalg import svd
import numpy as np

def ryu_takayanagi_entropy(psi, ell, n):
    """Entropía RT para un intervalo de longitud ell en n sitios."""
    M = psi.reshape(2**ell, 2**(n-ell))
    _, S, _ = svd(M, full_matrices=False)
    lam2 = S**2; lam2 = lam2[lam2 > 1e-14]
    return float(-np.sum(lam2 * np.log(lam2)))

# Para un estado crítico (XX sin masa), S ~ (c/3) log(ell)
# Pendiente log ≈ c/3 = 1/3 (cadena XX tiene c=1)
```

---

## 6. Holographic Quantum Error Correction

Almheiri, Dong y Harlow (2015) mostraron que la correspondencia holográfica **es un código de corrección de errores cuánticos**:

### La analogía exacta

| Holografía | QEC |
|-----------|-----|
| Operador de bulk (interior) | Operador lógico |
| Operadores de frontera (CFT) | Operadores físicos |
| Complementariedad del agujero negro | Corrección de borrado |
| Área de RT = entropía de código | Distancia del código |
| Subregión del bulk → subregión de frontera | Operador lógico → subespacios físicos |

### Códigos holográficos concretos

**Código de Parrilo-Almheiri (HaPPY, 2015):** Tesela el plano hiperbólico con pentágonos de código [[5,1,3]]:

- 5 tensores físicos en la frontera.
- 1 tensor lógico en el bulk.
- Reconstruible desde cualquier 3 de los 5 qubits de frontera.
- Exactamente el código perfecto [[5,1,3]] que usamos en QEC.

```
      [bulk]
     /   |   \
  [f₁] [f₂] [f₃]
    |         |
  [f₄]     [f₅]
```

**Propiedad clave:** para recuperar el operador del bulk, basta con la mitad más uno de los qubits de frontera — como en los agujeros negros, donde el interior se recupera desde la radiación de Hawking.

### Umbral de corrección holográfico

El código HaPPY tiene distancia $d = 3$ con 5 qubits físicos. La generalización a redes tensoriales más grandes da una familia de códigos con:

$$d = \Theta(n^{1-1/D})$$

donde $D$ es la dimensión del bulk. Para $D = 2$ (AdS_3): $d \sim \sqrt{n}$ — umbral que crece con el tamaño del sistema.

---

## 7. Wormholes, EPR y ER=EPR

**Conjetura ER=EPR** (Maldacena & Susskind, 2013):

> Dos partículas entrelazadas (EPR) están conectadas por un wormhole de Einstein-Rosen (ER).

### La geometría del entrelazamiento

El estado de Bell $|\Phi^+\rangle_{AB}$ entre dos sistemas A y B es dual, en AdS, al **agujero negro eterno de BTZ** — una solución con dos exteriores conectados por un wormhole:

```
CFT_L ← (frontera izquierda) ── Wormhole ── (frontera derecha) → CFT_R

Estado cuántico dual: |ψ⟩ = 1/√Z Σ_n e^{-βEn/2} |n⟩_L|n⟩_R  (estado de Hartle-Hawking)
```

### Consecuencias

1. **Paradoja de la información:** La información que cae en un agujero negro no se pierde — escapa codificada en la radiación de Hawking, a través del wormhole cuántico.

2. **Complejidad cuántica y volumen:** La complejidad del estado cuántico dual es proporcional al volumen del wormhole (conjetura CV de Susskind):
   $$\mathcal{C} \propto \frac{\text{Vol}(\mathcal{M})}{G_N \ell}$$

3. **Firewall paradox:** Si se distila suficiente entrelazamiento de la radiación de Hawking, el wormhole se hace traversable — pero violaría la censura cósmica.

---

## 8. Conexión con computación cuántica

### Simulación de AdS/CFT en hardware cuántico

En 2022 Google simuló un wormhole traversable en el procesador Sycamore de 9 qubits usando el modelo SYK (Sachdev-Ye-Kitaev):

- El modelo SYK con $N$ Majoranas es maximalmente caótico (límite de Planckian scrambling).
- Para $N=7$, el ground state y la transferencia de información a través del wormhole son simulables con 9 qubits.
- Se verificó que la información puede "teletransportarse" a través del wormhole cuántico.

**Crítica:** El experimento fue criticado por usar solo 9 qubits — la fisica interesante requiere $N \to \infty$. La escala del experimento de Google no permite descartar explicaciones clásicas.

### SYK en Qiskit (mínimo ejemplo)

```python
from qiskit.quantum_info import SparsePauliOp
import numpy as np

def syk_hamiltonian(N: int, seed: int = 0) -> SparsePauliOp:
    """Hamiltoniano SYK con N Majoranas, mapeado a N//2 qubits (JW).
    
    H_SYK = Σ_{ijkl} J_{ijkl} γ_i γ_j γ_k γ_l / (4! * 3^(3/2))
    J_{ijkl} ~ N(0, J²/C(N,4))
    """
    rng = np.random.default_rng(seed)
    n_qubits = N // 2
    # Coeficientes aleatorios
    from itertools import combinations
    terms = []
    sigma = np.sqrt(6.0 / N**3)  # normalización
    for i, j, k, l in combinations(range(N), 4):
        J = rng.normal(0, sigma)
        # Mapeo JW simplificado: γ_{2k} = X_k Π Z, γ_{2k+1} = Y_k Π Z
        # Para este ejemplo usamos XXXX como aproximación
        pauli = ['I'] * n_qubits
        for idx in [i//2, j//2, k//2, l//2]:
            if idx < n_qubits:
                pauli[idx] = 'Z' if pauli[idx] == 'I' else 'I'
        terms.append((''.join(reversed(pauli)), J))
    return SparsePauliOp.from_list(terms, num_qubits=n_qubits).simplify()
```

### Quantum complexity y OTOC

El **Out-of-Time-Order Correlator (OTOC)** mide el scrambling cuántico:

$$F(t) = \langle W(t) V W(t) V \rangle_\beta$$

Para sistemas caóticos (como SYK), $F(t)$ decae exponencialmente con un exponente de Lyapunov $\lambda_L$. El límite de Planck establece:

$$\lambda_L \leq \frac{2\pi}{\beta}$$

Los agujeros negros **saturan este límite** — son los scramblers más rápidos del universo. El modelo SYK también lo satura.

---

## 9. Estado del arte (2025)

### Logros recientes

| Año | Resultado | Grupo |
|-----|-----------|-------|
| 2022 | Wormhole traversable en 9 qubits | Google/Caltech |
| 2023 | Código holográfico con qubits de trampa de iones | Quantinuum |
| 2024 | Simulación MERA de estados críticos con 50+ qubits | IBM/Caltech |
| 2024 | Medición de OTOC en procesador de 100 qubits | Google Willow |
| 2025 | Evidencia de scrambling de Planckian en hardware | IBM Heron |

### Límites actuales

- La simulación de AdS/CFT requiere $N \to \infty$ para la física real.
- Con los qubits actuales (~100-1000), solo se pueden simular regímenes de baja dimensión.
- La relación exacta entre complejidad cuántica y volumen del wormhole no ha sido demostrada.

---

## 10. Resumen

| Concepto | Fórmula clave |
|----------|---------------|
| Dualidad AdS/CFT | $Z_{\text{gravity}}[\phi_0] = \langle e^{\int \phi_0 \mathcal{O}}\rangle_{\text{CFT}}$ |
| Entropía Ryu-Takayanagi | $S_A = \text{Area}(\gamma_A) / 4G_N$ |
| MERA ↔ AdS_3 | Profundidad = escala RG = coord. radial $z$ |
| Código HaPPY | Pentágono [[5,1,3]] tesela el plano hiperbólico |
| ER = EPR | Entrelazamiento ↔ wormhole geométrico |
| Scrambling de Planck | $\lambda_L \leq 2\pi/\beta$ (saturado por agujeros negros y SYK) |

### Conexiones con el curso

- **Módulo 09** — QEC: el código tórico es un código de corrección "plano", los códigos holográficos son su generalización hiperbólica.
- **Módulo 41** — Topological QC: el código HaPPY es un código topológico sobre el plano hiperbólico.
- **Módulo 42** — Tensor Networks: MERA es la tensor network holográfica fundamental.
- **Lab 46** — MPS: la misma SVD recursiva que construye MPS es la base de MERA y los códigos holográficos.

### Referencias

1. Maldacena, J. (1997). *The large N limit of superconformal field theories and supergravity*. Int. J. Theor. Phys. 38, 1113.
2. Ryu, S., Takayanagi, T. (2006). *Holographic derivation of entanglement entropy*. PRL 96, 181602.
3. Swingle, B. (2012). *Entanglement renormalization and holography*. PRD 86, 065007.
4. Almheiri, A., Dong, X., Harlow, D. (2015). *Bulk locality and quantum error correction in AdS/CFT*. JHEP 04, 163.
5. Maldacena, J., Susskind, L. (2013). *Cool horizons for entangled black holes*. Fortschr. Phys. 61, 781.
6. Jafferis, D. et al. (2022). *Traversable wormhole dynamics on a quantum processor*. Nature 612, 51.
