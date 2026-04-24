# Redes y protocolos de entrelazamiento cuántico

## 1. El Internet Cuántico: qué es y qué no es

El **Internet Cuántico** no es un reemplazo del internet clásico: es una infraestructura complementaria que permite la distribución de entrelazamiento cuántico entre nodos remotos. Sus aplicaciones no son "computar más rápido" en general, sino habilitar capacidades imposibles clásicamente:

- **Distribución cuántica de claves (QKD):** criptografía con seguridad incondicional.
- **Computación cuántica distribuida:** varios procesadores cuánticos entrelazados resuelven un problema que ninguno puede resolver solo.
- **Sincronización cuántica de relojes:** precisión de temporización superior al límite cuántico estándar.
- **Telescopía de base muy larga (VLBI) cuántica:** imágenes astronómicas con resolución superior.
- **Blind Quantum Computing:** cliente envía cálculos a un servidor sin revelar el algoritmo ni los datos.

## 2. Distribución cuántica de claves: QKD

### 2.1 Protocolo BB84 (Bennett & Brassard, 1984)

BB84 usa la no-clonación cuántica para detectar espías:

**Protocolo:**
1. Alice genera bits aleatorios $b_i$ y bases aleatorias $\theta_i \in \{+, \times\}$.
2. Prepara fotones: si $\theta_i = +$, usa $\{|0\rangle, |1\rangle\}$; si $\theta_i = \times$, usa $\{|+\rangle, |-\rangle\}$.
3. Bob elige bases aleatorias $\theta'_i$ para medir.
4. Alice y Bob comparan públicamente sus bases (no los bits).
5. Conservan solo los bits donde $\theta_i = \theta'_i$ (~50% de los bits): la **clave crudagra**.
6. Verifican una fracción de la clave crudagra para detectar errores (QBER: Quantum Bit Error Rate).
7. Aplican reconciliación de errores y amplificación de privacidad para obtener la clave final.

**Seguridad:** si Eva intercepta y mide un fotón, perturba su estado (por el teorema de no-clonación). Esto aumenta el QBER. Un QBER > 11% indica un espía con seguridad demostrable.

**Tasa de clave segura:** para QBER = $e$ y usando el protocolo de reconciliación Cascade:
$$
R_\text{clave} \approx 1 - h(e) - h(e) = 1 - 2h(e)
$$
donde $h(e) = -e\log_2 e - (1-e)\log_2(1-e)$ es la entropía binaria.

### 2.2 Protocolo E91 (Ekert, 1991)

E91 usa pares de Bell en lugar de fotones individuales:

1. Una fuente genera pares de fotones entrelazados en $|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$.
2. Alice recibe un fotón y Bob el otro.
3. Cada uno elige aleatoriamente entre tres bases de medición.
4. Los resultados correlacionan según la mecánica cuántica.
5. La seguridad se verifica comprobando la violación de la **desigualdad de Bell (CHSH)**:
   $$
   S = |E(a,b) - E(a,b') + E(a',b) + E(a',b')| \leq 2 \text{ (clásico)}
   $$
   La mecánica cuántica predice $S = 2\sqrt{2} \approx 2.83$. Si se mide $S$ cercano al máximo, no hay espía.

**Ventaja sobre BB84:** la seguridad se certifica por la física (violación de Bell), no por suposiciones sobre la implementación.

## 3. El desafío de la distancia

### 3.1 La atenuación en fibra

Un fotón en fibra óptica tiene una longitud de atenuación de ~20 km a 1550 nm (ventana de telecomunicaciones). Esto significa que la probabilidad de transmisión decae exponencialmente:

$$
P_\text{transmisión} = 10^{-\alpha L / 10}
$$

donde $\alpha \approx 0.2\,\text{dB/km}$ y $L$ es la distancia. Para 100 km: $P = 10^{-2} = 1\%$. Para 500 km: $P = 10^{-10} \approx 10^{-8}\%$: impracticable.

**En el internet clásico**, la solución son los amplificadores: copiar y regenerar la señal. En el internet cuántico esto está **prohibido por el teorema de no-clonación**. Los fotones no pueden amplificarse sin destruir el estado cuántico.

### 3.2 Solución: repetidores cuánticos

Los **repetidores cuánticos** extienden el alcance sin copiar el estado. La clave es el **entanglement swapping** (intercambio de entrelazamiento), que se trata en el siguiente capítulo.

La tasa de generación de entrelazamiento a distancia $L$ con $n$ nodos intermedios escala como:

- Sin repetidores (directo): $R \propto e^{-\alpha L}$ (exponencial).
- Con repetidores cuánticos ideales: $R \propto L^{-\beta}$ (polinomial).

## 4. Arquitectura por capas del Internet Cuántico

Igual que el modelo OSI clásico, el internet cuántico se organiza en capas:

| Capa | Función | Analogía clásica |
|---|---|---|
| Capa 1: Física | Transmisión de fotones por fibra o espacio libre | Fibra óptica, radio |
| Capa 2: Enlace | Generación de entrelazamiento entre nodos vecinos | Ethernet, Wi-Fi |
| Capa 3: Red | Routing de entrelazamiento a larga distancia | IP |
| Capa 4: Transporte | Calidad de entrelazamiento (fidelidad mínima) | TCP |
| Capa 5-7: Aplicación | QKD, teletransportación, computación ciega | HTTPS, SSH |

## 5. QKD en satélites: el experimento Micius

El satélite chino **Micius** (lanzado en 2016) demostró QKD por enlace satélite-tierra en 2017-2020:
- Distribución de entrelazamiento entre dos estaciones terrestres separadas 1120 km.
- QKD entre China y Austria (7600 km) a través del satélite.
- QBER medido: ~5%, suficientemente bajo para generar clave segura.

El enlace satélite evita la atenuación de la fibra (solo hay atenuación en los últimos ~500 km de atmósfera), permitiendo distancias interoceánicas.

## 6. Implementación: simulación de QKD clásica

```python
import numpy as np
from typing import Tuple

def bb84_simulation(n_bits: int, eve_intercept_prob: float = 0.0
                    ) -> Tuple[float, float]:
    """
    Simulación del protocolo BB84.
    
    Args:
        n_bits: número de bits transmitidos
        eve_intercept_prob: probabilidad de que Eva intercepte cada bit
    
    Returns:
        (key_rate, qber): fracción de bits en la clave y tasa de error
    """
    rng = np.random.default_rng(42)

    # Alice prepara bits y bases aleatorias
    alice_bits = rng.integers(0, 2, n_bits)
    alice_bases = rng.integers(0, 2, n_bits)  # 0=+, 1=×

    # Bob elige bases aleatorias
    bob_bases = rng.integers(0, 2, n_bits)

    # Eva intercepta con probabilidad eve_intercept_prob
    bob_received_bits = alice_bits.copy()
    eva_mask = rng.random(n_bits) < eve_intercept_prob
    eve_bases = rng.integers(0, 2, n_bits)

    # Eva mide en su base (puede introducir errores)
    for i in range(n_bits):
        if eva_mask[i]:
            if eve_bases[i] != alice_bases[i]:
                # Eva mide en la base incorrecta: introduce error aleatorio
                bob_received_bits[i] = rng.integers(0, 2)

    # Bob mide en su base
    bob_bits = np.where(bob_bases == alice_bases, bob_received_bits,
                        rng.integers(0, 2, n_bits))

    # Sifting: conservar solo los bits donde las bases coinciden
    matching = alice_bases == bob_bases
    alice_key = alice_bits[matching]
    bob_key = bob_bits[matching]

    # Calcular QBER
    qber = np.mean(alice_key != bob_key)
    key_rate = np.sum(matching) / n_bits

    return float(key_rate), float(qber)

# Sin espía
rate, qber = bb84_simulation(10000, eve_intercept_prob=0.0)
print(f"Sin espía: tasa de clave = {rate:.3f}, QBER = {qber:.4f}")

# Con espía al 100%
rate, qber = bb84_simulation(10000, eve_intercept_prob=1.0)
print(f"Con espía: tasa de clave = {rate:.3f}, QBER = {qber:.4f}")
# QBER esperado ≈ 0.25 (1/4 de los bits interceptados se equivocan)
```

## 7. Ideas clave

- El Internet Cuántico distribuye entrelazamiento, no información más rápida: habilita capacidades imposibles clásicamente (QKD, computación ciega, sensores distribuidos).
- BB84 usa fotones individuales y el teorema de no-clonación para garantizar la seguridad; E91 usa pares de Bell y la violación de la desigualdad de Bell.
- La atenuación en fibra limita la QKD directa a ~100-200 km; los satélites (Micius) superan esta limitación para distancias intercontinentales.
- La arquitectura del internet cuántico sigue un modelo de capas análogo al modelo OSI clásico.
- La detección de espías en BB84 es cuantitativa: un QBER > 11% certifica la presencia de Eva con seguridad demostrabe.

## 8. Ejercicios sugeridos

1. Calcular la tasa de clave segura de BB84 para QBER = 5%, 10% y 15% usando la fórmula $R = 1 - 2h(e)$.
2. Verificar que la desigualdad CHSH se viola para el estado $|\Phi^+\rangle$ con los ángulos óptimos $a=0, a'=\pi/4, b=\pi/8, b'=3\pi/8$, obteniendo $S = 2\sqrt{2}$.
3. Extender la simulación BB84 para incluir reconciliación de errores (por ejemplo, con el código de paridad XOR) y amplificación de privacidad (hash universal).
4. Calcular la atenuación en dB para una fibra de 200 km y estimar la tasa de fotones detectable si Alice envía $10^8$ fotones por segundo.

## Navegación

- Anterior: [Simplificación y optimización de circuitos](../26_calculo_grafico_y_zx_calculus/02_simplificacion_y_optimizacion_de_circuitos.md)
- Siguiente: [Repetidores y entanglement swapping](02_repetidores_y_entanglement_swapping.md)
