# Simulación digital frente a simulación analógica

## 1. Dos paradigmas de simulación cuántica

La idea de Feynman de usar un sistema cuántico para simular otro admite dos realizaciones fundamentalmente diferentes:

**Simulación digital:** el sistema target se codifica en qubits y su evolución se implementa como un circuito de puertas cuánticas discretas (trotterización, LCU, etc.). Es programable, universal, y comparte la arquitectura de la computación cuántica de propósito general.

**Simulación analógica:** se toma un sistema físico cuyo Hamiltoniano nativo se parece al Hamiltoniano que se quiere estudiar, y se manipulan directamente los parámetros de ese Hamiltoniano. No se compilan puertas; se "programa la física" directamente.

## 2. Simuladores analógicos: ventajas y limitaciones

Los simuladores analógicos más prominentes son:

**Átomos fríos en redes ópticas:** átomos neutros atrapados en potenciales periódicos creados por interferencia láser. Cada sitio de la red es un qubit o un sistema de múltiples niveles. La interacción túnel entre sitios implementa acoplamientos tipo Hubbard. Son los simuladores con más qubits efectivos (hasta $10^3$-$10^4$ átomos) y los más limpios en términos de coherencia.

**Iones atrapados en modo analógico:** en lugar de aplicar puertas discretas, se varían los parámetros de los láseres de forma continua para implementar Hamiltonianos de Ising o XY de largo alcance con conectividad todas a todas.

**Qubits superconductores en modo analógico:** ajustando dinámicamente los parámetros de los circuitos (frecuencias, acoplamientos), se implementan Hamiltonianos de Ising transverso o modelos de bosones de Bose-Hubbard.

**Ventajas:**
- Sin overhead de compilación.
- Naturalmente adecuados para su Hamiltoniano nativo.
- Posibles a escalas mucho mayores que los procesadores digitales.

**Limitaciones:**
- No universales: solo simulan Hamiltonianos con la misma estructura que su Hamiltoniano nativo.
- Difíciles de verificar: no hay acceso a estados intermedios.
- Menos controlables: los errores sistemáticos son difíciles de caracterizar.

## 3. Comparación cuantitativa

| Aspecto | Digital | Analógico |
|---|---|---|
| Universalidad | Universal (cualquier Hamiltoniano) | Específico (Hamiltoniano nativo) |
| Escala actual | ~1000 qubits físicos | ~$10^4$ átomos/iones |
| Verificabilidad | Tomografía de proceso | Limitada |
| Overhead de compilación | Alto (trotterización) | Ninguno |
| Temperatura | mK (superconductores), $\mu$K (iones) | nK (átomos fríos) |
| Fidelidad por operación | ~99% | No aplica (continuo) |

## 4. Simuladores analógicos de interés actual

**Modelo de Fermi-Hubbard:** describe la transición metal-aislante de Mott y el mecanismo de superconductividad de alta $T_c$. El Hamiltoniano es:

$$
H = -t\sum_{\langle i,j\rangle, \sigma} c_{i\sigma}^\dagger c_{j\sigma} + U\sum_i n_{i\uparrow} n_{i\downarrow}
$$

Con átomos fríos fermiones en redes ópticas 2D, se puede simular este modelo con $\sim 100 \times 100$ sitios, inaccesible para cualquier simulador clásico o digital actual.

**Modelo de Ising transverso con campo longitudinal:** relacionado con computación adiabática, detección de fases cuánticas de materia. Implementable directamente en procesadores de Rydberg (QuEra) o superconductores (IBM) en modo analógico.

## 5. Hybrid digital-analog: el camino actual

El enfoque más prometedora en el corto plazo es la **simulación híbrida digital-analógica**: usar la dinámica analógica nativa del hardware para las partes del Hamiltoniano que coinciden con la física del dispositivo, y complementarla con puertas digitales para los términos restantes.

Por ejemplo, en procesadores superconductores, el acoplamiento ZZ entre qubits vecinos es nativo. Se puede explotar este acoplamiento directamente (sin compilar CNOTs) para simular Hamiltonianos de Ising, reduciendo el número de operaciones digitales en un factor $\sim 10\times$.

## 6. Simulación de materiales: el objetivo a largo plazo

El objetivo más ambicioso de la simulación cuántica es calcular propiedades de materiales de interés tecnológico:

- **Superconductores de alta $T_c$:** descubrir el mecanismo microsocópico y diseñar materiales con $T_c$ mayor que la temperatura ambiente.
- **Catalizadores moleculares:** el cofactor FeMoco de la nitrogenasa convierte $N_2$ a $NH_3$ sin presión ni temperatura elevadas. Su simulación cuántica exacta podría revolucionar la producción de fertilizantes (proceso Haber-Bosch usa el 1% de la energía mundial).
- **Materiales para baterías y fotovoltaicos.**

Estimaciones indican que simular FeMoco exactamente requiere $\sim 1000$ qubits lógicos tolerantes a fallos, lo que está fuera de alcance del hardware actual pero es un objetivo plausible para 2035-2040.

## 7. Ideas clave

- La simulación digital usa puertas cuánticas para implementar cualquier Hamiltoniano; la analógica usa la física nativa del sistema.
- Los simuladores analógicos (átomos fríos, iones) operan a escalas mayores pero no son universales.
- Los procesadores digitales son más versátiles pero más lentos y más susceptibles al ruido.
- La simulación híbrida digital-analógica combina ventajas de ambos paradigmas.
- El objetivo a largo plazo (post-NISQ) es simular sistemas de interés industrial como FeMoco o materiales superconductores.

## 8. Ejercicios sugeridos

1. Describir cómo se implementaría el modelo de Ising 1D ($H = J\sum_i Z_i Z_{i+1} + h\sum_i X_i$) en un simulador analógico de átomos fríos.
2. Estimar el número de qubits lógicos (con corrección de errores) necesarios para simular FeMoco con error de energía $< 1$ kcal/mol.
3. Comparar el número de operaciones necesarias para simular el modelo de Heisenberg de 10 qubits durante $t=5$ usando Trotter orden 2 vs. LCU.
4. Investigar el experimento de Google con el procesador Sycamore en modo analógico para el modelo de Ising transverso y resumir los resultados.

## Navegacion

- Anterior: [Trotter-Suzuki y coste de simulacion](01_trotter_suzuki_y_coste_de_simulacion.md)
- Siguiente: [Lindblad y dinamica efectiva](../21_open_quantum_systems/01_lindblad_y_dinamica_efectiva.md)
