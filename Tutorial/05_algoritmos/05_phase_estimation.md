# Phase Estimation

## 1. Por que es importante

La estimacion de fase es una de las rutinas mas influyentes de la computacion cuantica. Su valor no reside solo en si misma, sino en que conecta ideas fundamentales:

- autovalores y autovectores;
- transformada cuantica de Fourier;
- informacion de fase codificada en registros auxiliares;
- subrutinas usadas en algoritmos mas avanzados.

## 2. Idea basica

Queremos estimar una fase $\\phi$ asociada a un operador unitario cuando

$$
U|u\\rangle = e^{2\\pi i \\phi}|u\\rangle.
$$

El algoritmo prepara qubits auxiliares, aplica potencias controladas de $U$ y luego usa la transformada cuantica de Fourier inversa para extraer informacion sobre $\\phi$ en forma binaria aproximada.

## 3. Valor pedagogico

Phase estimation es especialmente interesante porque obliga a integrar varias piezas del tutorial:

- control de operaciones;
- fases;
- QFT;
- medicion de registros auxiliares;
- interpretacion de resultados como aproximaciones binarias.

## 4. Rol en el curso

Aunque no sea un algoritmo para introducir en la primera clase, si debe aparecer relativamente pronto en un proyecto que aspire a ser serio. Actua como puente entre algoritmos elementales y herramientas cuanticas de mayor profundidad.

## 5. Ideas clave

- La informacion de fase puede convertirse en informacion legible en un registro clasico.
- La QFT juega un papel estructural, no decorativo.
- Phase estimation es una de las grandes piezas organizadoras del paisaje algoritmico cuantico.

## Navegacion

- Anterior: [Transformada cuantica de Fourier](04_transformada_cuantica_de_fourier.md)
