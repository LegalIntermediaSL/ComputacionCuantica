# Problemas abiertos en Computación Cuántica (2025)

> Esta sección invita a contribuidores con formación investigadora a trabajar
> en preguntas no resueltas. Cada problema incluye el estado del arte, por qué
> es difícil y referencias recientes.

---

## 1. Compilación óptima de circuitos para arquitecturas específicas

**Enunciado:** Dado un circuito cuántico abstracto y una arquitectura de
conectividad (p.ej., heavy-hex de IBM o retícula 2D de Google), ¿cuál es el
mínimo número de SWAPs necesario para compilar el circuito?

**Por qué es difícil:** La asignación de qubits (*qubit mapping*) es
NP-completo en general. Los compiladores actuales (Qiskit Transpiler,
tket, BQSKit) usan heurísticas que no garantizan el óptimo.

**Estado del arte (2025):** Compiladores basados en SMT solvers dan soluciones
óptimas para n ≤ 10 qubits en minutos. Para n > 20 solo hay cotas inferiores.

**Referencias:**
- Zulehner et al., *ICCAD* 2018 (A* mapping)
- Cowtan et al., *QPL* 2019 (tket)
- BQSKit: Younis et al., *SC* 2021

---

## 2. Umbral de corrección de errores para códigos qLDPC

**Enunciado:** ¿Cuál es el umbral exacto de error físico del código
bivariate bicycle (BB) y del código hypergraph product (HGP) bajo ruido
de circuito realista (no solo ruido de Pauli independiente)?

**Por qué es difícil:** Los decodificadores para qLDPC en presencia de
correlaciones temporales (error de readout + error de puerta en el mismo
ciclo) aún no están completamente caracterizados. Los umbrales actuales
son cotas superiores.

**Estado del arte (2025):** IBM y Google reportan umbrales del 0,7-1% para
BB codes con MWPM modificado. Con decodificadores neuronales los umbrales
suben ~20%, pero la latencia supera el ciclo de síndrome (1 μs).

**Referencias:**
- Bravyi et al., *Nature* 627, 778 (2024) — códigos BB
- Panteleev & Kalachev, *IEEE Trans. Inf. Theory* 2022 — HGP
- Leverrier et al., *STOC* 2022 — good LDPC codes

---

## 3. Clásico vs. cuántico en aprendizaje automático (ventaja demostrable)

**Enunciado:** ¿Existe un problema de aprendizaje automático donde un
algoritmo cuántico sea asintóticamente más eficiente que cualquier algoritmo
clásico, incluso con acceso a hardware ruidoso?

**Por qué es difícil:** Los *dequantization* results (Tang 2019) muestran que
muchos algoritmos QML tienen análogos clásicos igualmente rápidos con acceso
a muestreo aleatorio. Los kernels cuánticos tampoco muestran ventaja clara.

**Estado del arte (2025):** Huang et al. (*Nature Comm.* 2021) muestra
ventaja para *learning from quantum data* (datos generados por un proceso
cuántico). Para datos clásicos, la ventaja no está demostrada.

**Referencias:**
- Tang, *STOC* 2019 — dequantization de HHL
- Huang et al., *Nature Comm.* 12, 2631 (2021)
- Cerezo et al., *Nature Comp. Sci.* 2022 — barren plateaus

---

## 4. Simulación clásica eficiente de circuitos de profundidad logarítmica

**Enunciado:** ¿Pueden simularse clásicamente todos los circuitos cuánticos
de profundidad O(log n) en tiempo polinomial? ¿O hay circuitos logarítmicos
con salidas difíciles de muestrear?

**Por qué es difícil:** Los circuitos de profundidad O(log n) tienen
entrelazamiento acotado en las regiones del circuito, pero los métodos MPS
no escalan bien cuando la anchura del corte crece. Bosonsampling en
profundidad logarítmica podría ser difícil.

**Estado del arte (2025):** En profundidad constante, Bravyi et al. muestran
que ciertos circuitos Clifford+T de profundidad 3 no pueden simularse en
AC⁰. La frontera con profundidad logarítmica sigue abierta.

**Referencias:**
- Bravyi et al., *Science* 362, 308 (2018) — quantum advantage depth-3
- Gao & Duan, *Nature Comm.* 8, 662 (2017)

---

## 5. Decodificación en tiempo real con garantías de latencia

**Enunciado:** ¿Existe un decodificador de corrección de errores que sea
a la vez óptimo (minimiza error lógico) y opere en < 1 μs por ciclo de
síndrome para d = 25 con hardware clásico?

**Por qué es difícil:** MWPM es óptimo pero tarda O(n³) → ~100 μs para d=25.
Union-Find es O(n·α(n)) pero pierde ~10-20% de fidelidad. Los decodificadores
neuronales son rápidos con GPU pero no cumplen la latencia sin hardware dedicado.

**Estado del arte (2025):** Caune et al. presentan Chromobius (2024), un
decodificador de células que alcanza < 1 μs para d=7 en FPGA. Para d=25 aún
no se conoce solución con latencia garantizada.

**Referencias:**
- Higgott & Gidney, *Quantum* 7, 1012 (2023) — Sparse Blossom
- Caune et al., arxiv 2412.xxxxx (2024) — Chromobius
- Delfosse & Nickerson, *Quantum* 5, 595 (2021) — Almost-linear decoder

---

## 6. Ventaja cuántica en química: recursos exactos para FeMoco

**Enunciado:** ¿Cuántos qubits lógicos y qué profundidad de circuito se
necesita exactamente para calcular la energía del estado fundamental de FeMoco
(nitrogenasa) con precisión química (1 kcal/mol)?

**Por qué es difícil:** Las estimaciones actuales (200-4000 qubits lógicos,
10⁹-10¹² puertas) tienen órdenes de magnitud de incertidumbre según la base,
el algoritmo de codificación y las aproximaciones usadas.

**Estado del arte (2025):** Lee et al. (*JCTC* 2021) estiman ~4000 qubits con
first-quantization y QPE. Babbush et al. (*npj QI* 2019) bajan a ~200 con
second-quantization y sparse encoding. La discrepancia no está resuelta.

**Referencias:**
- Reiher et al., *PNAS* 114, 7555 (2017) — estimación original
- Lee et al., *JCTC* 17, 1316 (2021) — first-quantization
- Babbush et al., *npj Quantum Inf.* 5, 92 (2019)

---

## 7. Complejidad exacta de Quantum Phase Estimation con ruido

**Enunciado:** ¿Cuántos repeticiones de QPE se necesitan para estimar una
energía con precisión ε bajo un modelo de ruido realista de tasa p, y cómo
escala esto con el tamaño del sistema?

**Por qué es difícil:** El análisis clásico de QPE asume unitarios perfectos.
Con ruido, la fase acumulada tiene error que crece con el tiempo de evolución,
creando un óptimo no trivial entre precisión y ruido.

**Estado del arte (2025):** Lin & Tong (*PRX Quantum* 2022) dan un algoritmo
de QPE con complejidad cuasi-óptima bajo ruido. El factor de overhead sigue
siendo una función compleja de p y ε.

**Referencias:**
- Lin & Tong, *PRX Quantum* 3, 010318 (2022)
- Dong et al., *SIAM J. Sci. Comput.* 2022

---

## 8. Estabilidad de qubits topológicos de Majorana a temperatura finita

**Enunciado:** ¿Los qubits topológicos basados en fermiones de Majorana
mantienen su ventaja de protección intrínseca a temperaturas experimentalmente
alcanzables (> 100 mK), o las excitaciones térmicas destruyen la protección?

**Por qué es difícil:** La brecha de protección topológica Δ debe ser >> k_B T,
pero los nanohilos experimentales tienen Δ ~ 0.1-0.5 K (solo 4-20× sobre 20 mK).
No hay demostración experimental de coherencia topológica medible.

**Estado del arte (2025):** Microsoft anunció coherencia topológica en Majorana 1
(febrero 2025), pero sin benchmarks de puerta publicados. La comunidad espera
replicación independiente.

**Referencias:**
- Aghaee et al. (Microsoft), arxiv 2503.13000 (2025)
- Sarma et al., *npj Quantum Inf.* 1, 15001 (2015)
- Plugge et al., *New J. Phys.* 19, 012001 (2017)

---

## 9. Protocolos de destilación de estados mágicos con overhead sub-cuadrático

**Enunciado:** ¿Existe un protocolo de destilación de estados mágicos
(para implementar T gates fault-tolerant) con overhead de qubits físicos
sub-cuadrático en la precisión objetivo ε?

**Por qué es difícil:** El protocolo estándar 15→1 necesita O(log³(1/ε))
copias. Los protocolos de nivel k necesitan 15^k copias para ε ~ ε₀^(3^k),
lo que da overhead O(log³(1/ε)/log³(1/ε₀)). Bajar el exponente es abierto.

**Estado del arte (2025):** Haah et al. (*Quantum* 2018) introducen un protocolo
con constante menor, pero el exponente no cambia. Lattice surgery podría dar
mejoras constantes, no asimp.

**Referencias:**
- Bravyi & Kitaev, *Phys. Rev. A* 71, 022316 (2005) — protocolo original
- Haah et al., *Quantum* 2, 56 (2018) — códigos Reed-Muller
- Litinski, *Quantum* 3, 205 (2019) — magic state factory

---

## 10. Hardness de Boson Sampling con pérdidas experimentales

**Enunciado:** ¿Sigue siendo computacionalmente difícil el Boson Sampling
cuando los fotones se pierden con probabilidad η por modo, tal como ocurre
en experimentos reales?

**Por qué es difícil:** Con pérdidas η, el problema degrada hacia un muestreo
de fotones distinguibles (clásicamente fácil). La frontera entre difícil y
fácil en función de η no está caracterizada teóricamente.

**Estado del arte (2025):** Aaronson & Brod (*Phys. Rev. A* 2015) muestran que
con η > 1 - 1/√m pérdidas el problema es clásicamente eficiente. El rango
intermedio sigue sin resolver. Experimentos de Jiuzhang (China 2020-2023)
operan cerca de esta frontera.

**Referencias:**
- Aaronson & Brod, *Phys. Rev. A* 93, 012335 (2016)
- Zhong et al. (Jiuzhang), *Science* 370, 1460 (2020)
- Deshpande et al., *PRX Quantum* 3, 010304 (2022)

---

## Cómo contribuir

Si trabajas en alguno de estos problemas o conoces avances recientes:

1. Abre un issue con la etiqueta `research-problem`.
2. Propón una actualización del estado del arte o una nueva referencia.
3. Si tienes resultados propios, añade un artículo en el módulo correspondiente
   siguiendo la plantilla de [CONTRIBUTING.md](../CONTRIBUTING.md).

Ver también: [lecturas_recomendadas.md](lecturas_recomendadas.md) para
bibliografía avanzada por módulo.
