# Qiskit Runtime y primitives

## 1. Por que esta capa importa

Cuando el aprendizaje avanza mas alla de los circuitos elementales, ya no basta con pensar solo en puertas y mediciones. Tambien importa como se envian trabajos, como se organizan ejecuciones repetidas y que interfaz de alto nivel usamos para solicitar resultados.

En el ecosistema moderno de Qiskit, las `primitives` y `Qiskit Runtime` ocupan precisamente esa capa.

## 2. Idea general de las primitives

Las primitives ofrecen una interfaz mas estructurada para ejecutar tareas cuanticas frecuentes. En lugar de pensar solo en “mandar un circuito”, permiten expresar de forma mas directa ciertos tipos de consulta y organizar ejecuciones con menos friccion conceptual.

Desde el punto de vista didactico, esto es importante porque ayuda a separar:

- la construccion del circuito;
- el tipo de experimento que queremos pedir;
- la forma en que el backend procesa esa peticion.

## 3. Runtime como capa de ejecucion

Qiskit Runtime introduce una forma mas integrada de trabajar con recursos cuanticos, especialmente cuando interesa:

- agrupar ejecuciones;
- aprovechar mejor la plataforma;
- reducir sobrecarga de orquestacion;
- acercarse a flujos mas realistas que los de un simple cuaderno local.

## 4. Valor pedagogico

Para este proyecto, no hace falta entrar inmediatamente en todos los detalles de plataforma. Pero si conviene introducir esta capa porque muestra que la computacion cuantica aplicada no termina en dibujar circuitos, sino que incluye infraestructura de ejecucion y abstracciones mas ricas.

## 5. Ideas clave

- `Qiskit Runtime` y las `primitives` representan una capa de trabajo mas alta que la simple construccion de circuitos.
- Son especialmente relevantes cuando el proyecto crece hacia ejecucion mas realista y workflows repetibles.
- Introducirlas pronto ayuda a que el tutorial no quede anclado en una vision demasiado escolar de Qiskit.

## Navegacion

- Anterior: [Qiskit: transpilacion, ruido y paso hacia hardware](../09_qiskit_transpilacion_ruido_y_hardware.md)
- Siguiente: [Deutsch-Jozsa](../05_algoritmos/01_deutsch_jozsa.md)
