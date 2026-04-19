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
