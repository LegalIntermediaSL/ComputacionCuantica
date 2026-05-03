# Ruta de estudio

Este documento propone varias formas de recorrer el proyecto segun el perfil y el objetivo del lector.

## Ruta rapida

1. `Tutorial/01_qubits_y_estados.md`
2. `Tutorial/02_superposicion_medicion_y_esfera_de_bloch.md`
3. `Tutorial/03_puertas_cuanticas_y_circuitos.md`
4. `Tutorial/04_entrelazamiento_y_estados_de_bell.md`
5. `Tutorial/05_qiskit_primeros_pasos.md`
6. `Cuadernos/ejemplos/02_puertas_basicas_en_qiskit.ipynb`
7. `Cuadernos/problemas_resueltos/02_estados_de_bell.ipynb`

## Ruta teorica

1. fundamentos iniciales;
2. algebra lineal minima;
3. algoritmos introductorios;
4. informacion cuantica;
5. correccion de errores;
6. limites actuales y realismo.

## Ruta Qiskit

1. `Tutorial/05_qiskit_primeros_pasos.md`
2. `Tutorial/08_qiskit_simuladores_estado_y_resultados.md`
3. `Tutorial/09_qiskit_transpilacion_ruido_y_hardware.md`
4. `Tutorial/10_qiskit_avanzado/README.md`
5. laboratorios de Qiskit en `Cuadernos/laboratorios/`

## Ruta avanzada

1. algoritmos;
2. phase estimation;
3. informacion cuantica;
4. algoritmos variacionales;
5. correccion de errores;
6. surface codes y fault tolerance.

---

## Ruta Fotónica

Para quienes quieren explorar la computación cuántica con luz (Xanadu, PsiQuantum, QuiX).

**Prerrequisito:** completar Ruta rápida o conocer la esfera de Bloch.

1. `Tutorial/45_computacion_fotonica/README.md` — modos ópticos, estados gaussianos, GBS, Jiuzhang 2020
2. `Cuadernos/guiados/01_primer_qubit.ipynb` — analogía qubit ↔ qumode
3. `Cuadernos/laboratorios/49_fotonica_cuantica.ipynb` — circuito GBS, squeezing, hafnian
4. `visualizador/pages/17_Fotonica_Cuantica.py` — interferómetro interactivo, función de Wigner
5. `docs/guia_strawberry_fields.md` — instalación, backends, API key opcional
6. `Resumenes/13_fotonico_y_rydberg.md` — repaso rápido

**Salida:** entender GBS, estados squeezed, ventaja muestral (Jiuzhang), arquitectura PsiQuantum.

---

## Ruta Annealing y Optimización

Para quienes trabajan en optimización combinatoria (logística, finanzas, scheduling).

**Prerrequisito:** familiaridad con grafos y problemas NP.

1. `Tutorial/49_dwave_annealing/README.md` — QUBO, Hamiltoniano transverso-Ising, D-Wave Pegasus
2. `Cuadernos/guiados/14_computacion_adiabatica.ipynb` — QUBO desde cero, simulated annealing
3. `Cuadernos/laboratorios/53_qubo_dwave.ipynb` — MAX-CUT, TSP, portfolio con QUBO
4. `Cuadernos/guiados/09_qaoa_paso_a_paso.ipynb` — mismo QUBO resuelto con QAOA cuántico
5. `Cuadernos/laboratorios/21_optimizacion_carteras_vqe.ipynb` — finance con VQE
6. `Resumenes/15_qnlp_y_annealing.md` — repaso rápido

**Salida:** formular problemas como QUBO, comparar annealing vs QAOA vs clásico, usar D-Wave Leap.

---

## Ruta QEC Avanzado

Para quienes quieren entender la tolerancia a fallos a nivel técnico profundo.

**Prerrequisito:** Ruta avanzada completada (especialmente surface codes).

1. `Tutorial/09_correccion_errores/README.md` — QEC fundamentos, código de Shor
2. `Tutorial/14_surface_codes_y_horizonte_fault_tolerant/README.md` — surface code, umbral ~1%
3. `Cuadernos/guiados/11_correccion_de_errores.ipynb` — código repetición guiado
4. `Cuadernos/guiados/15_fault_tolerant.ipynb` — overhead, magic states, hoja de ruta 2030
5. `Tutorial/47_qldpc_decodificadores/README.md` — códigos qLDPC, bivariate bicycle [[144,12,12]]
6. `Cuadernos/laboratorios/51_qldpc_decoder.ipynb` — MWPM, decodificador neuronal MLP
7. `visualizador/pages/19_Decodificador_QEC.py` — surface code interactivo, curvas umbral
8. `Soluciones/investigacion/R9_qldpc_threshold.md` — umbral bajo ruido de circuito
9. `Soluciones/investigacion/R11_decodificacion_realtime.md` — latencia < 1 μs, FPGA vs GPU
10. `Soluciones/investigacion/R12_magic_state_subcuadratico.md` — destilación sub-cuadrática
11. `Resumenes/14_qldpc_y_decodificadores.md` — repaso rápido

**Salida:** entender la ruta completa hacia fault-tolerant práctico: surface code → qLDPC → overhead → decodificadores en tiempo real.
