# Qiskit: transpilacion, ruido y paso hacia hardware

## 1. Del circuito abstracto al circuito ejecutable

En una primera etapa del aprendizaje es natural pensar que un circuito cuantico es simplemente el diagrama que escribimos en el cuaderno o en el notebook. Sin embargo, cuando queremos acercarnos al hardware real, aparece una capa adicional: el circuito abstracto debe adaptarse a las restricciones fisicas del dispositivo.

Qiskit hace visible esa capa mediante la transpilacion.

## 2. Que es transpilacion

Transpilar un circuito significa reescribirlo en una forma compatible con un backend determinado o con un conjunto concreto de puertas base. Este proceso puede:

- reemplazar unas puertas por otras equivalentes;
- reorganizar parte del circuito;
- insertar operaciones auxiliares necesarias por conectividad;
- optimizar profundidad o conteo de puertas.

El resultado puede verse muy distinto del circuito original, pero seguir representando la misma tarea computacional ideal.

## 3. Por que importa en computacion cuantica real

En computacion clasica solemos abstraernos bastante de la arquitectura al nivel de algoritmos introductorios. En computacion cuantica eso es mucho mas dificil porque:

- no todos los dispositivos implementan las mismas puertas nativamente;
- no todos los qubits pueden interactuar directamente entre si;
- las puertas tienen fidelidades diferentes;
- la profundidad del circuito importa mucho por decoherencia.

Por eso, incluso en una fase temprana del aprendizaje, conviene saber que existe una distancia real entre “el circuito matematico” y “el circuito ejecutable”.

## 4. Conjuntos de puertas base

Un backend puede trabajar de forma preferente con un conjunto reducido de puertas nativas, por ejemplo rotaciones alrededor de ciertos ejes y una puerta de dos qubits concreta. La transpilacion traduce las puertas abstractas de alto nivel a esa gramatica operativa.

Esto es pedagogicamente muy importante porque enseña una leccion general:

> las puertas que usamos para pensar no siempre son las puertas que la maquina usa para ejecutar.

## 5. Conectividad

Otra restriccion crucial es la conectividad entre qubits. En un dispositivo ideal de papel solemos dibujar una `CNOT` entre cualquier par de qubits. En hardware real, eso puede no estar permitido directamente.

En ese caso, la transpilacion puede insertar operaciones adicionales para mover la informacion cuantica de forma compatible con la arquitectura. Esas operaciones extra tienen coste y pueden degradar la fidelidad global.

## 6. Ruido

Cuando pasamos del simulador ideal al hardware real aparece inevitablemente el ruido. Bajo ese nombre se agrupan varios efectos:

- decoherencia;
- imperfeccion en las puertas;
- errores de lectura;
- relajacion energetica;
- desfasaje.

No hace falta dominar todos estos detalles desde el primer dia, pero si conviene entender la intuicion general: los circuitos largos y complejos suelen sufrir mas al ejecutarse en hardware imperfecto.

## 7. Fidelidad y profundidad

Dos conceptos practicos aparecen rapidamente:

### Fidelidad

Mide cuan cerca esta la operacion realizada de la operacion ideal deseada.

### Profundidad

Mide, de forma simplificada, cuantas capas secuenciales de operaciones necesita el circuito.

En hardware ruidoso, aumentar la profundidad suele empeorar el resultado, porque el sistema permanece mas tiempo expuesto a errores.

## 8. Simulador ideal no es hardware real

Esta distincion nunca debe desaparecer del tutorial:

- un circuito perfecto en simulador ideal puede rendir mal en hardware real;
- un circuito transpiled puede ser mas largo que el circuito conceptual original;
- una salida ruidosa no invalida la teoria, sino que refleja limitaciones fisicas de la plataforma.

Qiskit es especialmente util porque permite recorrer gradualmente este camino: desde el circuito ideal de aprendizaje hasta una version mas realista del mismo experimento.

## 9. Estrategia didactica recomendada

Para un proyecto como este, la secuencia mas sana es:

1. entender el circuito ideal;
2. estudiar su estado y sus cuentas esperadas;
3. ver como se transpila;
4. discutir que problemas aparecen al pensar en hardware;
5. introducir de forma gradual el concepto de ruido.

Esta secuencia evita que la complejidad experimental opaque demasiado pronto la idea cuantica que se quiere enseñar.

## 10. Ideas clave

- La transpilacion adapta el circuito abstracto a restricciones concretas.
- El hardware cuantico impone limitaciones de puertas, conectividad y fidelidad.
- El ruido no es un accidente marginal, sino una parte estructural del presente de la computacion cuantica.
- Qiskit es valioso porque permite estudiar el paso desde la idealizacion hasta la implementacion realista.

## Navegacion

- Anterior: [Qiskit: simuladores, estado cuantico y resultados](08_qiskit_simuladores_estado_y_resultados.md)
- Siguiente: [Bibliografia comentada](07_apendices/bibliografia_comentada.md)
