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

## 3. Arquitectura del circuito

Una forma pedagogica de leer phase estimation es dividirla en tres bloques:

1. un registro auxiliar preparado en superposicion;
2. un registro objetivo en un autovector de la unitaria;
3. una capa de operaciones controladas seguida de una QFT inversa.

Esta separacion es importante porque hace visible que el algoritmo no "mide la fase directamente", sino que la va trasladando a un registro que luego puede leerse en forma binaria.

## 4. Potencias controladas

Las potencias controladas de $U$ son un ingrediente esencial. No se aplican por capricho, sino porque permiten codificar distintas escalas de la fase en qubits auxiliares distintos. De ese modo, cada qubit del registro auxiliar acumula informacion complementaria sobre $\\phi$.

En un tratamiento mas detallado, esta estructura explica por que la salida puede interpretarse como una aproximacion binaria de la fase.

## 5. Papel de la QFT inversa

La QFT inversa no es un añadido ornamental. Actua como una transformacion que reorganiza la informacion de fase acumulada en el registro auxiliar para volverla legible tras la medicion. Sin ella, el algoritmo no entregaria el mismo tipo de informacion util.

Por eso phase estimation es un gran ejemplo pedagógico del papel no trivial de la transformada cuantica de Fourier.

## 6. Valor pedagogico

Phase estimation es especialmente interesante porque obliga a integrar varias piezas del tutorial:

- control de operaciones;
- fases;
- QFT;
- medicion de registros auxiliares;
- interpretacion de resultados como aproximaciones binarias.

## 7. Relacion con otros algoritmos

Phase estimation no solo es interesante por si misma. Tambien actua como pieza estructural en algoritmos mas avanzados relacionados con:

- periodicidad;
- estimacion espectral;
- simulacion cuantica;
- ciertos enfoques de quimica cuantica y Hamiltonianos.

## 8. Rol en el curso

Aunque no sea un algoritmo para introducir en la primera clase, si debe aparecer relativamente pronto en un proyecto que aspire a ser serio. Actua como puente entre algoritmos elementales y herramientas cuanticas de mayor profundidad.

## 9. Ideas clave

- La informacion de fase puede convertirse en informacion legible en un registro clasico.
- La QFT juega un papel estructural, no decorativo.
- Phase estimation es una de las grandes piezas organizadoras del paisaje algoritmico cuantico.
- El registro auxiliar no es accesorio: es donde la fase se traduce a informacion medible.
- Las potencias controladas de la unitaria son parte central de la arquitectura.

## Navegacion

- Anterior: [Transformada cuantica de Fourier](04_transformada_cuantica_de_fourier.md)
