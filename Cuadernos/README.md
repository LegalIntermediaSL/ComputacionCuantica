# Cuadernos Jupyter

Este directorio reune notebooks de apoyo para el tutorial de computacion cuantica. Su objetivo es conectar teoria, practica y experimentacion con Qiskit.

## Estructura

- `ejemplos/`: notebooks cortos para ilustrar ideas o herramientas concretas.
- `problemas_resueltos/`: notebooks mas guiados para estudiar ejercicios paso a paso.
- `laboratorios/`: notebooks mas largos para exploracion guiada.

## Cobertura inicial

- qubits y estados;
- superposicion y medicion;
- puertas basicas;
- estados de Bell;
- primeros circuitos en Qiskit;
- estado vector, medicion y estadistica en Qiskit;
- backends, shots y flujo practico de trabajo;
- medicion en distintas bases con Qiskit;
- puertas de fase, interferencia y circuitos parametrizados;
- transpilation basica y adaptacion de circuitos;
- ejemplos iniciales de Grover y teleportacion;
- laboratorios guiados para Grover, Bernstein-Vazirani, teleportacion y QFT;
- phase estimation guiada;
- primeras intuiciones de `Sampler` y `Estimator`;
- laboratorios iniciales de VQE y QAOA;
- `SparsePauliOp` y observables sencillos;
- observables, valores esperados y Hamiltonianos introductorios;
- introduccion a modelos de ruido conceptuales;
- canales cuanticos y operadores de Kraus a nivel introductorio;
- trotterizacion y evolucion guiada;
- medicion avanzada, proyectores y POVM a nivel intuitivo;
- estimator y energia esperada en Hamiltonianos sencillos;
- complejidad cuantica y BQP a nivel introductorio;
- tomografia, reconstruccion y fidelidad a nivel conceptual;
- simulacion hamiltoniana avanzada y trade-offs de precision;
- comparaciones conceptuales entre ruido y fidelidad;
- sistemas abiertos, Lindblad y dinamica efectiva a nivel intuitivo;
- comparaciones entre observables, `Estimator` y estadistica de medicion;
- recursos cuanticos como coherencia, entrelazamiento y no-clonacion;
- matrices de densidad, subsistemas e informacion cuantica;
- esfera de Bloch;
- producto tensorial;
- algoritmos cuanticos introductorios.

## Criterios

- cada cuaderno debe declarar su objetivo al inicio;
- las formulas deben escribirse en LaTeX siempre que ayuden;
- el codigo debe ser pequeno, claro y comentado con mesura;
- cada notebook debe enlazarse mentalmente con uno o varios articulos del directorio `Tutorial/`.
- los cuadernos de Qiskit deben dejar claro si trabajan con estado ideal, cuentas de medicion o adaptacion a backend.
