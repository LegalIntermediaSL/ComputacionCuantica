# Tutorial de Computacion Cuantica

Este directorio contiene el cuerpo principal del curso. El objetivo es ofrecer una ruta progresiva que combine fundamentos conceptuales, practica con Qiskit, algoritmos, ruido, informacion cuantica, correccion de errores y una mirada realista al estado actual del campo.

## Mapa maestro

- [Indice general](indice_general.md)
- [Ruta de estudio](../ruta_de_estudio.md)
- [Tabla de cobertura](../tabla_cobertura.md)

## Recorrido principal recomendado

### 1. Fundamentos

1. [Qubits y estados cuanticos](01_fundamentos/01_qubits_y_estados.md)
2. [Superposicion, medicion y esfera de Bloch](01_fundamentos/02_superposicion_medicion_y_esfera_de_bloch.md)
3. [Puertas cuanticas y circuitos](01_fundamentos/03_puertas_cuanticas_y_circuitos.md)
4. [Entrelazamiento y estados de Bell](01_fundamentos/04_entrelazamiento_y_estados_de_bell.md)
5. [Qiskit: primeros pasos y flujo de trabajo practico](02_qiskit_basico/05_qiskit_primeros_pasos.md)
6. [Algebra lineal minima para computacion cuantica](01_fundamentos/06_algebra_lineal_minima_para_computacion_cuantica.md)
7. [Algoritmos cuanticos introductorios](01_fundamentos/07_algoritmos_cuanticos_introductorios.md)

### 2. Qiskit y flujo de ejecucion

8. [Qiskit: simuladores, estado cuantico y resultados](02_qiskit_basico/08_qiskit_simuladores_estado_y_resultados.md)
9. [Qiskit: transpilacion, ruido y paso hacia hardware](02_qiskit_basico/09_qiskit_transpilacion_ruido_y_hardware.md)
10. [Qiskit Runtime y primitives](04_qiskit/01_qiskit_runtime_y_primitives.md)

### 3. Algoritmos

11. [Deutsch-Jozsa](05_algoritmos/01_deutsch_jozsa.md)
12. [Bernstein-Vazirani](05_algoritmos/02_bernstein_vazirani.md)
13. [Grover](05_algoritmos/03_grover.md)
14. [Transformada cuantica de Fourier](05_algoritmos/04_transformada_cuantica_de_fourier.md)
15. [Phase Estimation](05_algoritmos/05_phase_estimation.md)

### 4. Ruido, informacion y correccion

16. [Decoherencia y ruido](06_ruido_y_hardware/01_decoherencia_y_ruido.md)
17. [Mitigacion de errores y fidelidad](06_ruido_y_hardware/02_mitigacion_errores_y_fidelidad.md)
18. [Matrices de densidad y estados mixtos](08_informacion_cuantica/01_matrices_de_densidad_y_estados_mixtos.md)
19. [Traza parcial y entropia](08_informacion_cuantica/02_traza_parcial_y_entropia.md)
20. [Qubit logico y codigo de repeticion](09_correccion_errores/01_qubit_logico_y_codigo_de_repeticion.md)
21. [Codigo de Shor: intuicion](09_correccion_errores/02_codigo_de_shor_intuicion.md)
22. [Surface codes: intuicion](14_surface_codes_y_horizonte_fault_tolerant/01_surface_codes_intuicion.md)
23. [Fault tolerance como horizonte](14_surface_codes_y_horizonte_fault_tolerant/02_fault_tolerance_como_horizonte.md)

### 5. Qiskit avanzado y algoritmos variacionales

24. [Sampler, Estimator y primitives](10_qiskit_avanzado/01_sampler_estimator_y_primitives.md)
25. [Operators, Pauli y representaciones utiles](10_qiskit_avanzado/02_operator_y_paulis.md)
26. [Noise models y simulacion realista](10_qiskit_avanzado/03_noise_models_y_simulacion_realista.md)
27. [Circuitos parametrizados y optimizacion](11_algoritmos_variacionales/01_circuitos_parametrizados_y_optimizacion.md)
28. [VQE: intuicion](11_algoritmos_variacionales/02_vqe_intuicion.md)
29. [QAOA: intuicion](11_algoritmos_variacionales/03_qaoa_intuicion.md)

### 6. Aplicaciones y Hamiltonianos

30. [Quimica cuantica y simulacion](12_aplicaciones/01_quimica_cuantica_y_simulacion.md)
31. [Optimizacion](12_aplicaciones/02_optimizacion.md)
32. [Machine learning cuantico con perspectiva critica](12_aplicaciones/03_machine_learning_cuantico_con_perspectiva_critica.md)
33. [Simulacion digital y Hamiltonianos sencillos](12_aplicaciones/04_simulacion_digital_y_hamiltonianos_sencillos.md)
34. [Finanzas cuanticas: optimizacion de carteras (Markowitz)](12_aplicaciones/05_finanzas_cuanticas_optimizacion_de_carteras.md)
35. [Valoracion de activos y Monte Carlo cuantico (QAE)](12_aplicaciones/06_valoracion_de_activos_y_monte_carlo_cuantico.md)
36. [Kernels cuanticos y espacios de caracteristicas](12_aplicaciones/07_kernels_cuanticos_y_espacios_de_caracteristicas.md)
37. [Redes neuronales cuanticas (QNN)](12_aplicaciones/08_redes_neuronales_cuanticas_qnn.md)
38. [Simulacion de materiales y estructuras complejas](12_aplicaciones/09_simulacion_de_materiales_y_estructuras_complejas.md)
39. [Observables y Hamiltonianos](15_hamiltonianos_y_evolucion_temporal/01_observables_y_hamiltonianos.md)
40. [Evolucion unitaria y Trotterizacion](15_hamiltonianos_y_evolucion_temporal/02_evolucion_unitaria_y_trotterizacion.md)

### 7. Canales y ruido

41. [Canales cuanticos: intuicion y representacion](16_canales_cuanticos_y_ruido/01_canales_cuanticos_intuicion_y_representacion.md)
42. [Operadores de Kraus, decoherencia y modelos efectivos](16_canales_cuanticos_y_ruido/02_kraus_decoherencia_y_modelos_efectivos.md)

### 8. Medicion avanzada

43. [Proyectores, valores esperados y varianza](17_medicion_avanzada_y_observables/01_proyectores_valores_esperados_y_varianza.md)
44. [POVM: intuicion y medicion generalizada](17_medicion_avanzada_y_observables/02_povm_intuicion_y_medicion_generalizada.md)

### 9. Complejidad y caracterizacion

45. [BQP, oraculos y speedup](18_complejidad_cuantica/01_bqp_oraculos_y_speedup.md)
46. [Limites de la ventaja y comparacion clasica](18_complejidad_cuantica/02_limites_de_la_ventaja_y_comparacion_clasica.md)
47. [Tomografia de estados: intuicion y reconstruccion](19_tomografia_y_caracterizacion/01_tomografia_de_estados_intuicion_y_reconstruccion.md)
48. [Fidelidad y caracterizacion operacional](19_tomografia_y_caracterizacion/02_fidelidad_y_caracterizacion_operacional.md)

### 10. Simulacion cuantica avanzada

49. [Trotter-Suzuki y coste de simulacion](20_simulacion_cuantica_avanzada/01_trotter_suzuki_y_coste_de_simulacion.md)
50. [Simulacion digital frente a analogica](20_simulacion_cuantica_avanzada/02_simulacion_digital_frente_a_analogica.md)

### 11. Open quantum systems

51. [Lindblad y dinamica efectiva](21_open_quantum_systems/01_lindblad_y_dinamica_efectiva.md)
52. [Decoherencia, relajacion y markovianidad](21_open_quantum_systems/02_decoherencia_relajacion_y_markovianidad.md)

### 12. Recursos cuanticos

53. [Coherencia, entrelazamiento y utilidad](22_recursos_cuanticos/01_coherencia_entrelazamiento_y_utilidad.md)
54. [No-clonacion y limites operacionales](22_recursos_cuanticos/02_no_clonacion_y_limites_operacionales.md)

### 13. Implementacion de Hardware

55. [Transmones y circuitos superconductores](23_hardware_fisico_y_arquitecturas/01_transmones_y_circuitos_superconductores.md)
56. [Iones atrapados y otras arquitecturas](23_hardware_fisico_y_arquitecturas/02_iones_atrapados_y_otras_arquitecturas.md)

### 14. Control de calibracion y Pulsos (Qiskit Pulse)

57. [Introduccion al control por microondas](24_control_de_pulsos_y_qiskit_pulse/01_introduccion_al_control_por_microondas.md)
58. [Programacion de pulsos con Qiskit Pulse](24_control_de_pulsos_y_qiskit_pulse/02_programacion_de_pulsos_con_qiskit_pulse.md)

### 15. Criptografia Post-Cuantica

59. [Criptografia Post-Cuantica (PQC)](25_criptografia_post_cuantica_pqc/01_criptografia_post_cuantica_pqc.md)

### 16. Cierre y perspectiva

60. [Que puede y que no puede hacer la computacion cuantica hoy](13_limites_actuales_y_realismo/01_que_puede_y_que_no_puede_hacer_la_computacion_cuantica_hoy.md)
61. [Realismo sobre ventaja cuantica](13_limites_actuales_y_realismo/02_realismo_sobre_ventaja_cuantica.md)
62. [Bibliografia comentada](07_apendices/bibliografia_comentada.md)

## Modulos especializados

- [04_qiskit](04_qiskit/README.md)
- [05_algoritmos](05_algoritmos/README.md)
- [06_ruido_y_hardware](06_ruido_y_hardware/README.md)
- [07_apendices](07_apendices/README.md)
- [08_informacion_cuantica](08_informacion_cuantica/README.md)
- [09_correccion_errores](09_correccion_errores/README.md)
- [10_qiskit_avanzado](10_qiskit_avanzado/README.md)
- [11_algoritmos_variacionales](11_algoritmos_variacionales/README.md)
- [12_aplicaciones](12_aplicaciones/README.md)
- [13_limites_actuales_y_realismo](13_limites_actuales_y_realismo/README.md)
- [14_surface_codes_y_horizonte_fault_tolerant](14_surface_codes_y_horizonte_fault_tolerant/README.md)
- [15_hamiltonianos_y_evolucion_temporal](15_hamiltonianos_y_evolucion_temporal/README.md)
- [16_canales_cuanticos_y_ruido](16_canales_cuanticos_y_ruido/README.md)
- [17_medicion_avanzada_y_observables](17_medicion_avanzada_y_observables/README.md)
- [18_complejidad_cuantica](18_complejidad_cuantica/README.md)
- [19_tomografia_y_caracterizacion](19_tomografia_y_caracterizacion/README.md)
- [20_simulacion_cuantica_avanzada](20_simulacion_cuantica_avanzada/README.md)
- [21_open_quantum_systems](21_open_quantum_systems/README.md)
- [22_recursos_cuanticos](22_recursos_cuanticos/README.md)
- [23_hardware_fisico_y_arquitecturas](23_hardware_fisico_y_arquitecturas/README.md)
- [24_control_de_pulsos_y_qiskit_pulse](24_control_de_pulsos_y_qiskit_pulse/README.md)
- [25_criptografia_post_cuantica_pqc](25_criptografia_post_cuantica_pqc/README.md)

## Filosofia del material

- empezar por intuicion y lenguaje;
- consolidar una base matematica minima sin volver el arranque demasiado abstracto;
- conectar pronto teoria y practica con Qiskit;
- separar con claridad fundamentos, herramientas, algoritmos, ruido y aplicaciones;
- dejar enlaces de navegacion entre articulos para que la lectura sea continua;
- reforzar teoria con cuadernos Jupyter, ejercicios, resumentes y laboratorios.
