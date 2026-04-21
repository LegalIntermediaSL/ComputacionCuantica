# Bitacora del Proyecto ComputacionCuantica

## Proposito

Esta bitacora registra el estado del proyecto, las decisiones editoriales, los avances de contenido y los siguientes pasos recomendados. Su objetivo es dar continuidad al trabajo y evitar que el repositorio crezca sin estructura.

## Estado general

El proyecto se encuentra en fase inicial. La prioridad actual es construir una base documental clara para desarrollar un repositorio serio sobre computacion cuantica, combinando teoria, fundamentos matematicos, algoritmos, hardware y practica.

## Entrada inicial

### Fecha

2026-04-19

### Situacion encontrada

- El repositorio solo contenia un `README.md` muy breve.
- No existia registro editorial ni historial de cambios.
- No habia todavia estructura de carpetas para contenido tecnico.

### Trabajo realizado

- Se creo `bitacora.md` para registrar el avance del proyecto.
- Se creo `changelog.md` para documentar cambios relevantes.

### Decision editorial principal

Se adopta una estrategia de crecimiento progresivo por capas:

1. Documentacion base del proyecto.
2. Estructura general del temario.
3. Desarrollo de fundamentos de computacion cuantica.
4. Cuadernos, ejemplos y problemas resueltos.
5. Material avanzado sobre algoritmos, correccion de errores y hardware.

## Criterios de calidad

- El contenido debe avanzar desde intuicion a formalismo.
- Las explicaciones deben equilibrar rigor y claridad pedagogica.
- La notacion matematica debe mantenerse estable entre documentos.
- Los modulos deben poder leerse en secuencia, pero tambien consultarse por separado.
- La documentacion del proyecto debe actualizarse junto con el contenido tecnico.

## Riesgos identificados

- Mezclar demasiados niveles de dificultad desde el principio puede romper la progresion didactica.
- Separar mal teoria, algoritmos y hardware puede volver confuso el recorrido.
- No fijar una estructura inicial puede producir duplicidades y retrabajo.
- No registrar decisiones editoriales puede dificultar futuras ampliaciones.

## Proximos pasos recomendados

### Prioridad alta

- Ampliar `README.md` con vision, alcance y hoja de ruta.
- Diseñar la arquitectura inicial del tutorial o manual.
- Definir modulos base sobre qubits, puertas, medicion y circuitos.

### Prioridad media

- Crear una carpeta `Tutorial/`.
- Crear una carpeta `Cuadernos/` para notebooks Jupyter.
- Preparar una bibliografia inicial comentada.

### Prioridad baja

- Añadir figuras, diagramas y esquemas visuales.
- Incorporar ejercicios graduados.
- Preparar materiales sobre plataformas concretas como Qiskit, Cirq o PennyLane.

## Nota de seguimiento

Cuando se empiece a desarrollar contenido tecnico, esta bitacora deberia reflejar:

- que modulo se abrio;
- que objetivos cubre;
- que decisiones de estilo se tomaron;
- que temas quedaron pendientes;
- que relacion existe entre teoria, cuadernos y material practico.

## Cierre de esta entrada

El proyecto ya cuenta con una base minima de seguimiento. El siguiente hito importante es transformar el repositorio en una estructura concreta de contenidos sobre computacion cuantica.

## Entrada de apertura de contenido tecnico

### Fecha

2026-04-19

### Objetivo

Empezar el desarrollo real del proyecto con una primera ruta de estudio sobre fundamentos de computacion cuantica y una capa practica en notebooks.

### Trabajo realizado

- Se creo la carpeta `Tutorial/`.
- Se creo la carpeta `Cuadernos/` con subcarpetas `ejemplos/` y `problemas_resueltos/`.
- Se añadieron cinco articulos iniciales sobre qubits, superposicion, medicion, puertas, circuitos, entrelazamiento y primeros pasos con Qiskit.
- Se añadieron notebooks introductorios para trabajar estados, puertas y estados de Bell.
- Se actualizo `README.md` para reflejar la nueva estructura del repositorio.

### Resultado

El proyecto deja de ser solo una idea documentada y pasa a tener una base real de contenido tecnico. Ya existe una ruta inicial de aprendizaje que combina teoria y practica.

### Pendientes inmediatos

- Ampliar el modulo con algebra lineal basica y esfera de Bloch.
- Crear mas cuadernos Jupyter con simulaciones y problemas resueltos.
- Abrir un bloque posterior sobre algoritmos cuanticos introductorios.

## Entrada de ampliacion de contenidos

### Fecha

2026-04-19

### Objetivo

Dar mas densidad al tutorial para que no quede reducido a notas introductorias muy cortas y reforzar la conexion con cuadernos practicos.

### Trabajo realizado

- Se ampliaron los cinco articulos iniciales con mas contexto, explicaciones y secciones internas.
- Se añadieron nuevos articulos sobre algebra lineal minima y algoritmos cuanticos introductorios.
- Se desarrollaron mas notebooks en `Cuadernos/ejemplos/` y `Cuadernos/problemas_resueltos/`.
- Se reforzo la documentacion principal para reflejar la nueva cobertura tematica.

### Resultado

El proyecto ya no es solo una introduccion minima. Empieza a funcionar como una ruta de aprendizaje mas solida, con continuidad entre fundamentos, formalismo y primeras herramientas practicas en Qiskit.

### Pendientes inmediatos

- Abrir un modulo sobre Grover, Deutsch-Jozsa y otros algoritmos con mas detalle.
- Añadir cuadernos que ejecuten simuladores de Qiskit con resultados y cuentas.
- Crear una capa visual con diagramas y figuras para el tutorial.

## Entrada de ampliacion de la seccion Qiskit

### Fecha

2026-04-19

### Objetivo

Evitar que Qiskit quede reducido a una nota corta de herramienta y convertirlo en una parte pedagogicamente fuerte del proyecto.

### Trabajo realizado

- Se reescribio y amplió de forma importante `Tutorial/05_qiskit_primeros_pasos.md`.
- Se añadieron notebooks nuevos sobre estado vector, medicion, `shots`, backends y correlaciones de Bell en Qiskit.
- Se reforzo la documentacion de `Cuadernos/` para reflejar mejor la cobertura practica de la herramienta.

### Resultado

La seccion de Qiskit pasa de ser una introduccion breve a funcionar como una guia de trabajo mas seria, conectando teoria, simulacion, estadistica y arquitectura de ejecucion.

## Entrada de expansion fuerte de cuadernos Qiskit

### Fecha

2026-04-19

### Objetivo

Convertir la carpeta de notebooks de Qiskit en una coleccion amplia de ejemplos y problemas que sirva de apoyo real al tutorial.

### Trabajo realizado

- Se añadieron cuadernos sobre medicion en distintas bases.
- Se añadieron cuadernos sobre puertas de fase e interferencia.
- Se añadieron cuadernos sobre circuitos parametrizados y transpilacion.
- Se añadieron ejemplos iniciales de Grover y teleportacion en Qiskit.
- Se reforzo la cobertura de problemas resueltos para Qiskit.

### Resultado

La parte practica asociada a Qiskit deja de ser un bloque corto de iniciacion y pasa a parecer una biblioteca creciente de trabajo, mas util para estudiar, experimentar y extender el proyecto en futuras iteraciones.

## Entrada de profundizacion de Qiskit como modulo propio

### Fecha

2026-04-19

### Objetivo

Consolidar Qiskit no solo como herramienta auxiliar, sino como una linea formativa completa dentro del proyecto.

### Trabajo realizado

- Se añadieron dos articulos nuevos sobre simuladores, resultados, transpilacion, ruido y hardware.
- Se extendio el `Tutorial/README.md` para integrar mejor la ruta practica de Qiskit.
- Se reforzaron las convenciones de `Cuadernos/README.md` para distinguir entre estado ideal, cuentas y adaptacion a backend.
- Se actualizo la portada principal del proyecto para reflejar este crecimiento.

### Resultado

El proyecto empieza a tener dos ejes bien conectados: fundamentos conceptuales de computacion cuantica y formacion practica seria en Qiskit.

## Entrada de referencias y enlaces

### Fecha

2026-04-19

### Objetivo

Incorporar una capa de referencias externas fiable para que el proyecto no dependa solo del contenido interno del repositorio.

### Trabajo realizado

- Se creo `referencias.md`.
- Se añadieron enlaces oficiales de Qiskit e IBM Quantum.
- Se añadieron referencias bibliograficas y de curso para estudio mas profundo.
- Se integro una seccion visible de vinculos y referencias en `README.md`.

### Resultado

El repositorio ya tiene una base documental externa clara, util tanto para consulta rapida como para orientar futuras ampliaciones del tutorial.

## Entrada de reorganizacion modular y laboratorios

### Fecha

2026-04-19

### Objetivo

Aplicar una reorganizacion mas curricular del proyecto y abrir zonas de trabajo que preparen crecimiento sostenido.

### Trabajo realizado

- Se crearon modulos numerados dentro de `Tutorial/`.
- Se abrio el bloque `05_algoritmos/` con documentos sobre Deutsch-Jozsa, Bernstein-Vazirani, Grover y QFT.
- Se abrio el bloque `06_ruido_y_hardware/`.
- Se creo el bloque `07_apendices/` con `bibliografia_comentada.md`.
- Se crearon `Imagenes/` y `Notas/` como zonas de apoyo.
- Se añadió `Cuadernos/laboratorios/` con laboratorios sobre Grover, teleportacion y transpilacion.

### Resultado

El proyecto deja de crecer solo como una secuencia lineal de articulos y empieza a adquirir forma de curso modular con teoria, practica, bibliografia y espacios auxiliares claramente diferenciados.

## Entrada de apertura de informacion cuantica y correccion

### Fecha

2026-04-19

### Objetivo

Abrir las siguientes capas naturales del curso: informacion cuantica y correccion de errores, junto con una hoja de ruta mas clara.

### Trabajo realizado

- Se crearon los modulos `08_informacion_cuantica/` y `09_correccion_errores/`.
- Se añadieron documentos introductorios sobre matrices de densidad, traza parcial, qubit logico y codigo de Shor.
- Se añadieron cuadernos y laboratorios asociados.
- Se creo `roadmap.md`.
- Se actualizo la portada del tutorial con una tabla de estado de modulos.

### Resultado

El proyecto ya no solo explica circuitos y algoritmos iniciales, sino que empieza a tender un puente claro hacia informacion cuantica y escalabilidad real.

## Entrada de qiskit avanzado y resúmenes

### Fecha

2026-04-19

### Objetivo

Dar una segunda vuelta de madurez al proyecto añadiendo una capa de Qiskit avanzado y material de repaso compacto.

### Trabajo realizado

- Se creo `10_qiskit_avanzado/`.
- Se añadieron textos sobre `Sampler`, `Estimator`, operadores, Paulis y modelos de ruido.
- Se añadió `05_phase_estimation.md` al bloque de algoritmos.
- Se creó el directorio `Resumenes/`.
- Se incorporaron mapas Mermaid adicionales y una tabla de estado mas informativa.

### Resultado

El proyecto gana una capa de sofisticacion practica y tambien una capa de legibilidad, al incorporar materiales de repaso y una vision mas moderna del ecosistema Qiskit.

## Entrada de ejercicios y sprint phase estimation

### Fecha

2026-04-19

### Objetivo

Reforzar la practica del proyecto con ejercicios organizados y desarrollar la siguiente pieza algoritmica natural: phase estimation.

### Trabajo realizado

- Se creo el directorio `Ejercicios/`.
- Se añadieron ejercicios basicos, intermedios y avanzados.
- Se añadieron cuadernos sobre `Sampler`, `Estimator` y observables.
- Se añadio un laboratorio guiado de `phase estimation`.
- Se incorporo una tabla maestra de modulos en `README.md`.

### Resultado

El proyecto gana una capa de estudio activo y una forma mas clara de presentar su madurez actual modulo por modulo.

## Entrada de practica avanzada y resúmenes ampliados

### Fecha

2026-04-19

### Objetivo

Pasar de sugerencias generales a una capa más tangible de práctica avanzada y consolidación pedagógica.

### Trabajo realizado

- Se añadieron cuadernos conceptuales sobre `Sampler`, `Estimator` y ruido.
- Se añadieron laboratorios guiados sobre `phase estimation`, `VQE` y `QAOA`.
- Se amplió el bloque de surface codes con fault tolerance como horizonte.
- Se añadieron nuevos resúmenes sobre algoritmos e información cuántica.

### Resultado

El proyecto gana una continuidad mucho más clara entre teoría avanzada, práctica en Qiskit y repaso estructurado por bloques.

## Entrada de consolidacion variacional y aplicaciones

### Fecha

2026-04-20

### Objetivo

Evitar que los bloques de algoritmos variacionales y aplicaciones queden solo como introducciones teóricas sin apoyo práctico mínimo.

### Trabajo realizado

- Se añadieron laboratorios nuevos para VQE y QAOA.
- Se añadió un ejemplo básico con `SparsePauliOp`.
- Se amplió el bloque de aplicaciones con simulación digital y Hamiltonianos sencillos.
- Se completó la tabla maestra del `README.md` con más módulos.

### Resultado

El proyecto queda más equilibrado entre teoría, práctica y orientación temática, especialmente en las zonas que estaban empezando a abrirse.

## Entrada de orientacion del lector y Hamiltonianos

### Fecha

2026-04-20

### Objetivo

Mejorar la navegabilidad global del repositorio y abrir un bloque tematico muy natural: Hamiltonianos y evolucion temporal.

### Trabajo realizado

- Se creo `ruta_de_estudio.md`.
- Se creo `tabla_cobertura.md`.
- Se abrio `15_hamiltonianos_y_evolucion_temporal/`.
- Se añadieron ejemplos sobre counts, histogramas conceptuales y comparacion ideal vs ruidoso.
- Se añadió un resumen adicional sobre correccion y fault tolerance.

### Resultado

El proyecto mejora tanto en orientacion para distintos lectores como en continuidad tematica hacia simulacion y Hamiltonianos.

## Entrada de Hamiltonianos ampliados y canales cuanticos

### Fecha

2026-04-20

### Objetivo

Profundizar el paso desde circuitos y algoritmos hacia dinamica, observables y descripcion efectiva del ruido, para que el tutorial no se quede en una vision demasiado idealizada.

### Trabajo realizado

- Se amplió `15_hamiltonianos_y_evolucion_temporal/` con mas desarrollo conceptual y matematico.
- Se añadió `16_canales_cuanticos_y_ruido/`.
- Se incorporaron ejercicios sugeridos y material asociado en los articulos nuevos.
- Se crearon cuadernos sobre observables, valores esperados, canales de ruido y trotterizacion.
- Se actualizó la ruta principal del tutorial para integrar este nuevo bloque.

### Resultado

El proyecto conecta mejor informacion cuantica, hardware, ruido, simulacion y algoritmos variacionales. El lector dispone ahora de un puente mucho mas natural entre teoria ideal, evolucion temporal y modelos efectivos de ruido.

## Entrada de medicion avanzada y estimator

### Fecha

2026-04-20

### Objetivo

Dar una capa mas madura a la nocion de medicion y reforzar el puente entre observables formales, valores esperados y herramientas practicas como `Estimator`.

### Trabajo realizado

- Se abrio `17_medicion_avanzada_y_observables/`.
- Se añadieron cuadernos sobre `Estimator`, Hamiltonianos sencillos y medicion generalizada.
- Se creo un laboratorio guiado adicional sobre energia esperada.
- Se añadieron un nuevo resumen y soluciones avanzadas seleccionadas.
- Se recoloco la navegacion del tutorial para integrar el bloque antes del cierre sobre limites del campo.

### Resultado

La idea de medicion queda menos simplificada, la relacion entre teoria y Qiskit se refuerza y los modulos avanzados ganan continuidad pedagogica.

## Entrada de complejidad cuantica y tomografia

### Fecha

2026-04-20

### Objetivo

Seguir elevando el nivel del proyecto con dos capas que suelen faltar en tutoriales demasiado elementales: complejidad computacional y caracterizacion experimental de estados.

### Trabajo realizado

- Se abrio `18_complejidad_cuantica/`.
- Se abrio `19_tomografia_y_caracterizacion/`.
- Se añadieron cuadernos sobre BQP, complejidad, tomografia y fidelidad conceptual.
- Se añadio un laboratorio sobre matrices de densidad, ruido y tomografia.
- Se completaron resumenes adicionales para variacionales, aplicaciones, complejidad y tomografia.

### Resultado

El proyecto gana madurez en dos direcciones a la vez: por un lado, mejor criterio para hablar de ventaja cuantica; por otro, mejor comprension de como se valida y caracteriza lo que un dispositivo realmente prepara.

## Entrada de glosario, lecturas y simulacion avanzada

### Fecha

2026-04-20

### Objetivo

Convertir el repositorio en una herramienta de estudio mas completa, no solo como secuencia de articulos, sino tambien como referencia de consulta y puente hacia estudio autonomo.

### Trabajo realizado

- Se crearon `glosario.md` y `lecturas_recomendadas.md`.
- Se abrio `20_simulacion_cuantica_avanzada/`.
- Se añadieron cuadernos y laboratorios sobre fidelidad, ruido y simulacion hamiltoniana.
- Se reforzaron varios articulos avanzados con `Prerequisitos`, `Objetivos` y `Errores comunes`.

### Resultado

El proyecto gana profundidad, autonomia pedagogica y mejores puentes entre fundamentos, aplicaciones fisicas y estudio posterior fuera del propio repositorio.

## Entrada de guia Qiskit, mapa visual y sistemas abiertos

### Fecha

2026-04-20

### Objetivo

Mejorar la usabilidad del repositorio como curso completo y reforzar la capa de fisica de sistemas abiertos, que da mas continuidad a los bloques de ruido y canales cuanticos.

### Trabajo realizado

- Se crearon `Qiskit_en_este_repositorio.md` y `mapa_visual_del_curso.md`.
- Se abrio `21_open_quantum_systems/`.
- Se añadio un cuaderno introductorio sobre sistemas abiertos.
- Se actualizo la ruta principal del tutorial para integrar este nuevo bloque.

### Resultado

El proyecto se vuelve mas facil de recorrer, mas claro en su parte practica con Qiskit y mas solido en la transicion entre ruido discreto, canales y dinamica abierta.

## Entrada de comparativas practicas avanzadas

### Fecha

2026-04-20

### Objetivo

Reforzar la utilidad practica de los bloques avanzados con comparaciones mas concretas sobre estadistica de medicion, observables y descripciones de estados en presencia de ruido.

### Trabajo realizado

- Se añadieron cuadernos sobre shots, `DensityMatrix`, sistemas abiertos y observables distintos.
- Se creo `preguntas_frecuentes_avanzadas.md`.
- Se reforzo el bloque `21_open_quantum_systems/` con material asociado adicional.

### Resultado

La parte avanzada gana mas valor operativo: ya no solo introduce conceptos, sino que los aterriza en comparaciones que ayudan a interpretar mejor simulacion, ruido y estimacion.

## Entrada de recursos cuanticos

### Fecha

2026-04-20

### Objetivo

Dar mas unidad conceptual al curso incorporando una seccion explicita sobre recursos cuanticos, para que la ventaja y los limites del formalismo no aparezcan como ideas aisladas.

### Trabajo realizado

- Se abrio `22_recursos_cuanticos/`.
- Se añadieron cuadernos sobre coherencia, entrelazamiento y no-clonacion.
- Se añadió un resumen adicional sobre recursos cuanticos.
- Se integro el nuevo bloque dentro de la ruta principal del tutorial.

### Resultado

El proyecto gana una capa de interpretacion mas fuerte sobre que estructuras cuanticas importan realmente y por que ciertos limites son tan formativos como los propios algoritmos.

## Entrada de FAQ, soluciones y realismo

### Fecha

2026-04-19

### Objetivo

Dar un paso de madurez editorial: no solo expandir contenido, sino mejorar navegabilidad, práctica guiada y equilibrio conceptual.

### Trabajo realizado

- Se creo `FAQ.md`.
- Se creo `Soluciones/` con soluciones seleccionadas.
- Se abrio `11_algoritmos_variacionales/`.
- Se abrio `13_limites_actuales_y_realismo/`.
- Se reforzo la portada con nuevas rutas y estados.

### Resultado

El proyecto empieza a parecer menos una colección de materiales en crecimiento y más un curso estructurado con capas de aprendizaje, consulta rápida, práctica y realismo crítico.

## Entrada de aplicaciones y horizonte fault-tolerant

### Fecha

2026-04-19

### Objetivo

Seguir ampliando el proyecto hacia una visión más completa del campo, incluyendo aplicaciones y el horizonte de surface codes.

### Trabajo realizado

- Se creó `estructura_del_proyecto.md`.
- Se creó `CONTRIBUTING.md`.
- Se abrió `12_aplicaciones/`.
- Se abrió `14_surface_codes_y_horizonte_fault_tolerant/`.
- Se añadieron rutas de lectura por perfil en el `README.md`.

### Resultado

El proyecto gana valor como repositorio formativo y también como proyecto mantenible, con mejor orientación para lectores distintos y una visión más amplia del ecosistema de computación cuántica.

## Entrada de finalización de la fase maestra

### Fecha

2026-04-21

### Objetivo

Consolidar el repositorio como una enciclopedia completa de 52 artículos, con soluciones modulares y navegación verificada, eliminando rastro de rutas locales.

### Trabajo realizado

- Se completaron los 52 artículos del tutorial (Lote 1-4 completados).
- Se crearon 10 artículos de soluciones modulares por bloque temático.
- Se verificó la navegación bidireccional en el 100% de los documentos.
- Se corrigieron rutas absolutas en la documentación raíz.
- Se actualizaron los índices maestros (`Tutorial/README.md`, `Soluciones/README.md`).

### Resultado

El proyecto ha alcanzado su primera versión mayor estable teórica (v0.5.0), con una de las coberturas más profundas de computación cuántica en español, integrando teoría avanzada y práctica moderna con Qiskit.

## Entrada de expansión: Verticales Industriales y QML

### Fecha

2026-04-22

### Objetivo

Elevar la utilidad práctica del repositorio mediante la inclusión de aplicaciones financieras, aprendizaje automático cuántico (QML) de vanguardia y simulación de materiales complejos.

### Trabajo realizado

- Se añadieron 5 artículos técnicos al módulo de Aplicaciones (Finanzas, QAE, Kernels, QNN, Hubbard).
- Se crearon laboratorios específicos para optimización de carteras y SVM cuánticos.
- Se reajustó la navegación maestra para integrar estos contenidos sin romper la linealidad del curso.
- Sincronización de índices y registros para una publicación estable en GitHub (v0.7.0).

### Resultado

El repositorio deja de ser solo un tutorial de fundamentos para convertirse en una guía de aplicaciones de industria, cubriendo ahora 62 artículos y 30 laboratorios guiados.

## Entrada de expansión: Interactividad y Fronteras Teóricas

### Fecha

2026-04-22

### Objetivo

Dotar al repositorio de una dimensión visual dinámica e integrar los temas más avanzados de la literatura actual (ZX-Calculus e Internet Cuántico).

### Trabajo realizado

- Creación del visualizador interactivo con **Streamlit** (Esfera de Bloch + Simulador de Ruido).
- Redacción de 4 artículos técnicos de vanguardia (Bloques 17 y 18).
- Renumeración y sincronización total de 66 artículos en índices y navegación bidireccional.
- Actualización de `requirements.txt` con bibliotecas de visualización.

### Resultado

El proyecto alcanza un nivel de excelencia pedagógica y tecnológica poco común en repositorios educativos, integrando software interactivo y teoría avanzada.



