# Iones atrapados y otras arquitecturas cuánticas

## 1. El paisaje del hardware cuántico

Aunque los transmones superconductores son la tecnología más extendida en la industria, existen varias plataformas físicas con ventajas competitivas distintas. Cada arquitectura hace una elección de compromiso diferente entre velocidad de operación, tiempos de coherencia, conectividad y escalabilidad. Ninguna domina todas las métricas simultáneamente.

## 2. Iones atrapados

### 2.1 Principio de operación

Los qubits de iones atrapados almacenan información en los **estados electrónicos internos** de iones enfriados a temperaturas ultrabajas y confinados en el vacío mediante campos electromagnéticos (**trampa de Paul** o trampa de superficie). Sistemas comunes:

- $^{171}\text{Yb}^+$: qubit hiperfino (transición entre estados atómicos del estado fundamental), frecuencia ~12.6 GHz.
- $^{40}\text{Ca}^+$: qubit óptico (transición de reloj entre estado fundamental y metaestable), frecuencia ~729 nm.
- $^{133}\text{Ba}^+$: qubit de transición óptica con emisión de fotón en fibra estándar (útil para redes cuánticas).

Las puertas de un qubit se implementan con pulsos láser o de microondas resonantes con la transición.

### 2.2 Puertas de dos qubits: modos de vibración

La clave del entrelazamiento entre iones es el uso de los **modos normales de vibración colectiva** (fonones) del cristal iónico como bus de entrelazamiento. Las puertas $M\phi lmer$-$S\phi rensen$ (MS) o Cirac-Zoller explotan esta mediación:

1. Aplicar un pulso que acopla el estado electrónico del ion $i$ con el modo de vibración.
2. Aplicar un pulso similar al ion $j$.
3. El modo de vibración actúa como intermediario: después de la secuencia, los dos iones quedan entrelazados y el modo regresa a su estado inicial.

La fidelidad de estas puertas supera el 99.9% para 2 qubits y sigue siendo >99% para 10+ qubits.

### 2.3 Conectividad total

A diferencia de los superconductores (donde un qubit habla solo con sus vecinos físicos), en una trampa de iones **todos los qubits pueden entrelazarse entre sí** mediante los modos de vibración. Esto significa conectividad all-to-all, eliminando la necesidad de puertas SWAP para el ruteo.

### 2.4 Tiempos de coherencia superiores

El aislamiento del vacío y la criogenia iónica permiten tiempos $T_2$ de **segundos a minutos**, órdenes de magnitud superiores a los transmones:

| Parámetro | Iones atrapados | Transmones |
|---|---|---|
| $T_1$ | >1000 s | 100-500 μs |
| $T_2$ | 1-100 s | 50-400 μs |
| Fidelidad puerta 1-qubit | >99.99% | >99.9% |
| Fidelidad puerta 2-qubits | >99.9% | 99-99.9% |
| Tiempo de puerta 2-qubits | 0.1-10 ms | 100-500 ns |
| Número de qubits (2024) | 32-56 | 127-1121 |

El principal inconveniente es la **velocidad**: las puertas de dos qubits de iones tardan $10^4$-$10^5$ veces más que las de los transmones.

### 2.5 Empresas y sistemas actuales

- **IonQ (Aria, Forte):** hasta 35 qubits "algorítmicos" con fidelidades >99.5% en puertas de dos qubits.
- **Quantinuum (H2):** 56 qubits con fidelidad CNOT >99.8%, conectividad all-to-all.
- **Oxford Ionics:** integración de iones con chips de control CMOS para escalabilidad.

## 3. Átomos neutros de Rydberg

### 3.1 Principio

Los **átomos neutros en trampas ópticas** (tweezer arrays) son otra plataforma emergente. Los qubits se codifican en estados hiperfinos del átomo ($^{87}\text{Rb}$, $^{133}\text{Cs}$, $^{170}\text{Yb}$). Las puertas se implementan excitando los átomos a **estados de Rydberg** (niveles con número cuántico principal muy alto, $n \sim 50$-$100$).

Los estados de Rydberg tienen interacciones dipolo-dipolo o van der Waals de largo alcance:

$$
V_{ij} \approx \frac{C_6}{r_{ij}^6}
$$

que pueden ser tan fuertes que bloquean la excitación simultánea de dos átomos vecinos (**bloqueo de Rydberg**). Esta interacción implementa naturalmente puertas de dos qubits controladas.

### 3.2 Ventajas

- **Escalabilidad:** los arrays ópticos 2D pueden controlar $10^3$ átomos con láseres (QuEra lleva >1000 átomos, Pasqal >1000).
- **Reconfigurabilidad:** los átomos pueden moverse durante el cálculo, cambiando la conectividad en tiempo real.
- **Simulación analógica nativa:** ideal para modelos de Ising, Hubbard y otros Hamiltonianos de muchos cuerpos.

### 3.3 Desafíos

- Fidelidades de puerta actualmente inferiores (~99-99.5% para dos qubits) comparadas con iones.
- El movimiento de átomos introduce calor y pérdida de átomos.
- La lectura es fluorescente (destruye el estado), con eficiencia ~99%.

## 4. Centros NV en diamante

Los **centros de vacante de nitrógeno** (NV) en diamante son defectos cristalinos donde un átomo de nitrógeno sustituye a un carbono adyacente a una vacante. El espín electrónico del centro NV actúa como qubit:

- **Temperatura de operación:** temperatura ambiente (a diferencia de la criogenia del resto de plataformas).
- **Tiempo de coherencia:** $T_2 \sim 1$-$10\,\text{ms}$ a temperatura ambiente; segundos en diamante isótopicamente purificado a baja temperatura.
- **Lecturas:** fluorescencia óptica con eficiencia cercana al 100% para espines individuales.
- **Escalabilidad:** difícil. El entrelazamiento entre NVs requiere fotones mediadores con probabilidades bajas.

**Aplicaciones principales:** sensores cuánticos de campo magnético (magnetometría de un solo espín, detección de neuronas individuales) y nodos de repetición en redes cuánticas de corto alcance.

## 5. Fotónica cuántica integrada

Las plataformas fotónicas usan **fotones** como qubits, codificando información en polarización, número de fotones (Fock states) o tiempo de llegada.

### 5.1 Ventajas

- Sin decoherencia ambiental significativa (los fotones no interactúan con el entorno fácilmente).
- Velocidad de la luz: transmisión natural por fibra óptica estándar.
- Integración con infraestructura de telecomunicaciones existente.

### 5.2 Desafíos

Los fotones no interactúan entre sí fácilmente, lo que hace que las **puertas de dos fotones sean probabilísticas**. Hay dos enfoques para superar esto:

**KLM (Knill-Laflamme-Milburn):** puertas probabilísticas aumentadas con estados ancilla y teleportación cuántica. Requiere multiplicidad de fotones ancilla.

**MBQC (Measurement-Based QC):** crear un **cluster state** de fotones entrelazados y luego realizar el cómputo aplicando mediciones adaptativas. Xanadu y PsiQuantum usan este enfoque con chips fotónicos integrados en silicio.

### 5.3 Empresas

- **Xanadu (Borealis):** procesador de luz continua (modo gaussiano) en fotónica de silicio.
- **PsiQuantum:** chips en proceso CMOS de silicon photonics, objetivo 1 millón de qubits fotónicos.
- **QuiX Quantum:** procesadores de interferencia de fotones en waveguides de Si₃N₄.

## 6. Tabla comparativa de arquitecturas

| Arquitectura | Qubit físico | $T_2$ | Puerta 2-qubits | Conectividad | Escala actual | T° operación |
|---|---|---|---|---|---|---|
| Superconductores | Corriente Cooper | 50-400 μs | 100-500 ns | Vecinos 2D | ~1000 qubits | 10-20 mK |
| Iones atrapados | Espín hiperfino | 1-100 s | 0.1-10 ms | All-to-all | 20-56 qubits | μK |
| Rydberg | Espín hiperfino | ms | μs | Configurable | 100-1000 átomos | μK |
| NV en diamante | Espín electrónico | ms-s | μs | Par (fotón) | 2-10 qubits | Temperatura ambiente |
| Fotónica | Polarización/Fock | ∞ (en tránsito) | Probabilístico | Todas | 100s fotones | Temperatura ambiente |

## 7. ¿Qué plataforma ganará?

No hay consenso. La respuesta depende de la aplicación:
- **Algoritmos de circuito profundo a corto plazo:** transmones (más rápidos).
- **Algoritmos de circuito largo con alta fidelidad:** iones (más coherentes).
- **Simulación de muchos cuerpos a gran escala:** átomos de Rydberg.
- **Redes cuánticas y comunicaciones:** NV en diamante y fotónica.
- **Fault-tolerant a largo plazo:** aún incierto; IBM, Google, Quantinuum y QuEra compiten activamente.

El campo más probable es la coexistencia de plataformas especializadas, similar a la coexistencia de CPUs, GPUs, FPGAs y ASICs en la computación clásica.

## 8. Ejercicios sugeridos

1. Comparar el número de operaciones alcanzable en 1 segundo en iones atrapados vs transmones dado sus tiempos de puerta y coherencia.
2. Explicar por qué el bloqueo de Rydberg implementa un CNOT y cuál es el estado de dos qubits producido por la puerta CZ basada en Rydberg.
3. Calcular la fidelidad de un circuito de 100 puertas de dos qubits con fidelidad por puerta del 99.9% asumiendo errores independientes.
4. Discutir los requisitos de un repetidor cuántico basado en NV en diamante para conectar dos ciudades separadas 300 km.

## Navegación

- Anterior: [Transmones y circuitos superconductores](01_transmones_y_circuitos_superconductores.md)
- Siguiente: [Introducción al control por microondas](../24_control_de_pulsos_y_qiskit_pulse/01_introduccion_al_control_por_microondas.md)
