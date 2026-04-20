# ComputacionCuantica

Proyecto de tutorial de computacion cuantica orientado a teoria y practica, con especial foco en el uso de Qiskit como herramienta para construir, simular y estudiar circuitos cuanticos.

Este repositorio tiene como objetivo explicar los fundamentos de la computacion cuantica de forma progresiva y pedagogica. El proyecto aspira a cubrir tanto la intuicion fisica y matematica basica como la implementacion practica de ejemplos, algoritmos y ejercicios en notebooks y materiales de apoyo.

## Alcance del proyecto

El tutorial se plantea como una introduccion estructurada a temas como:

- qubits y estados cuanticos;
- superposicion y entrelazamiento;
- puertas cuanticas y circuitos;
- medicion y probabilidades;
- algebra lineal basica aplicada a computacion cuantica;
- simulacion de circuitos con Qiskit;
- algoritmos cuanticos introductorios;
- nociones iniciales de hardware y arquitecturas cuanticas.

## Enfoque

El enfoque del repositorio combina tres niveles:

1. fundamentos conceptuales de la computacion cuantica;
2. formulacion matematica accesible;
3. practica guiada con Qiskit y cuadernos Jupyter.

La idea es que el proyecto pueda servir tanto como material de aprendizaje secuencial como repositorio de consulta para conceptos, ejemplos y ejercicios.

## Rutas por perfil

- `Principiante total`: empezar por qubits, medicion, puertas, Qiskit basico y ejercicios basicos.
- `Fisico o matematico`: avanzar rapido hacia informacion cuantica, phase estimation, ruido y correccion de errores.
- `Programador Python`: entrar pronto por Qiskit, cuadernos y laboratorios, y despues volver a fundamentos teoricos.
- `Interesado en Qiskit`: recorrer `04_qiskit`, `10_qiskit_avanzado`, laboratorios y FAQ.

## Estado actual

El proyecto esta en fase inicial de estructuracion. La documentacion base ya se esta organizando para construir despues el tutorial, los cuadernos practicos y el material complementario.

## Estructura inicial

- `Tutorial/`: articulos y desarrollo teorico del recorrido formativo.
- `Cuadernos/`: notebooks Jupyter con ejemplos y problemas resueltos.
- `Imagenes/`: material visual del tutorial.
- `Notas/`: material fuente, resúmenes y referencias de trabajo.
- `referencias.md`: vinculos, enlaces y bibliografia recomendada.
- `roadmap.md`: hoja de ruta de crecimiento del proyecto.
- `Resumenes/`: resúmenes breves por módulo.
- `Ejercicios/`: práctica organizada por nivel.
- `Soluciones/`: soluciones seleccionadas para parte de los ejercicios.
- `ruta_de_estudio.md`: recorridos sugeridos según perfil.
- `tabla_cobertura.md`: visión global del estado de cada bloque.
- `bitacora.md`: seguimiento editorial y tecnico del proyecto.
- `changelog.md`: historial de cambios relevantes.
- `glosario.md`: definiciones breves de conceptos clave.
- `lecturas_recomendadas.md`: guia de referencias y rutas externas de estudio.
- `Qiskit_en_este_repositorio.md`: guia para usar la parte practica del proyecto.
- `mapa_visual_del_curso.md`: mapa Mermaid del recorrido formativo.
- `preguntas_frecuentes_avanzadas.md`: respuestas cortas a dudas de nivel intermedio y avanzado.

La primera version del contenido ya cubre qubits, superposicion, medicion, puertas, circuitos, entrelazamiento, algebra lineal minima, primeros pasos con Qiskit y una introduccion a algoritmos cuanticos elementales.

El bloque de Qiskit se esta ampliando como una linea de trabajo propia dentro del proyecto, con articulos y notebooks sobre simuladores, medicion, estado vector, transpilacion, backends, algoritmos y protocolos cuanticos elementales.

El proyecto tambien empieza a abrir bloques de informacion cuantica, correccion de errores y laboratorios guiados para que la progresion no se quede solo en los fundamentos mas elementales.

Tambien se esta abriendo una segunda capa de madurez con algoritmos variacionales, FAQ, ejercicios clasificados, soluciones seleccionadas y un bloque de realismo sobre los limites actuales del campo.

Se abre ademas un bloque de aplicaciones y un primer horizonte hacia surface codes y computacion tolerante a fallos.

Se añade ahora tambien una capa mas clara de orientacion al lector con rutas de estudio, tabla de cobertura y un nuevo bloque sobre Hamiltonianos y evolucion temporal.

El proyecto empieza ahora tambien a conectar mejor simulacion, ruido y descripcion efectiva de sistemas abiertos mediante un bloque nuevo sobre canales cuanticos y operadores de Kraus.

Se añade ademas una capa mas fina sobre medicion avanzada, observables y POVM, para que la idea de medir no quede reducida a leer bits al final de un circuito.

El proyecto empieza tambien a incorporar complejidad cuantica, tomografia y caracterizacion, para equilibrar mejor el triangulo entre algoritmos, hardware y evaluacion experimental.

Tambien se abre ahora una capa de simulacion cuantica avanzada para conectar mejor Hamiltonianos, coste de aproximacion, precision y arquitecturas de simulacion.

Se incorpora ademas una guia de uso de Qiskit dentro del repositorio, un mapa visual del curso y un bloque de `open quantum systems` para reforzar la descripcion de dinamica abierta y ruido continuo.

Tambien se empiezan a reforzar las comparaciones practicas entre `DensityMatrix`, `Estimator`, shots y fidelidad para que la parte avanzada sea mas operativa.

Se abre ahora tambien un bloque sobre recursos cuanticos para ordenar mejor la relacion entre coherencia, entrelazamiento, interferencia y limites como la no-clonacion.

## Tabla maestra de modulos

| Modulo | Estado | Teoria | Cuadernos | Laboratorios |
|---|---|---:|---:|---:|
| Fundamentos | base solida | si | si | no |
| Qubits y medicion | base solida | si | si | no |
| Puertas y circuitos | base solida | si | si | no |
| Entrelazamiento | base solida | si | si | no |
| Qiskit | en fuerte desarrollo | si | si | si |
| Algoritmos | en desarrollo | si | si | si |
| Ruido y hardware | borrador solido | si | parcial | si |
| Informacion cuantica | abierto | si | si | si |
| Correccion de errores | abierto | si | parcial | no |
| Qiskit avanzado | abierto | si | parcial | no |
| Algoritmos variacionales | abierto | si | parcial | si |
| Aplicaciones | abierto | si | parcial | no |
| Hamiltonianos y evolucion temporal | abierto | si | parcial | si |
| Canales cuanticos y ruido | abierto | si | parcial | no |
| Medicion avanzada y observables | abierto | si | parcial | no |
| Complejidad cuantica | abierto | si | parcial | no |
| Tomografia y caracterizacion | abierto | si | parcial | si |
| Simulacion cuantica avanzada | abierto | si | parcial | si |
| Open quantum systems | abierto | si | parcial | no |
| Recursos cuanticos | abierto | si | parcial | no |
| Limites actuales y realismo | abierto | si | no | no |
| Surface codes y fault tolerance | abierto | si | no | no |

## Vinculos, enlaces y referencias

El proyecto ya incluye una base inicial de referencias en [referencias.md](/Users/legalintermedia/Documents/GitHub/ComputacionCuantica/referencias.md).

Recursos destacados:

- [Qiskit en IBM Quantum](https://www.ibm.com/quantum/qiskit)
- [Documentacion oficial de IBM Quantum y Qiskit](https://quantum.cloud.ibm.com/docs/en)
- [Learning path: Getting started with Qiskit](https://learning.quantum.ibm.com/learning-path/getting-started-with-qiskit)
- [Repositorio oficial de Qiskit en GitHub](https://github.com/Qiskit/qiskit)
- [Nielsen y Chuang](https://www.cambridge.org/highereducation/books/quantum-computation-and-quantum-information/01E10196D0A682A6AEFFEA52D53BE9AE)
- [Curso de John Preskill en Caltech](https://www.preskill.caltech.edu/ph219/ph219_2018.html)

## Proyectos relacionados

- [QFT en GitHub](https://github.com/LegalIntermediaSL/QFT)
  Proyecto hermano centrado en Teoria Cuantica de Campos, util como base conceptual para conectar computacion cuantica con fundamentos de teoria cuantica.
