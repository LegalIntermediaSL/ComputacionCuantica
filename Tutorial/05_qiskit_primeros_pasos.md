# Qiskit: primeros pasos y flujo de trabajo practico

## 1. Por que Qiskit

Qiskit es uno de los entornos mas utilizados para trabajar con computacion cuantica desde Python. Permite:

- construir circuitos cuanticos;
- visualizarlos;
- simular su ejecucion;
- analizar resultados de medicion;
- transpilar circuitos para arquitecturas concretas;
- ejecutar experimentos en hardware cuantico cuando hay acceso disponible.

Para un tutorial, Qiskit tiene una ventaja decisiva: traduce ideas abstractas en circuitos concretos y resultados observables. La teoria deja de ser solo una secuencia de definiciones y pasa a convertirse en algo manipulable paso a paso.

## 2. Qiskit como puente entre teoria y practica

La utilidad didactica de Qiskit no consiste solo en que "permite programar un circuito". Su valor real es que obliga a explicitar cada una de las capas del problema:

- que qubits y bits clasicos intervienen;
- que estado inicial estamos preparando;
- que puertas aplicamos y en que orden;
- en que base medimos;
- con cuantas repeticiones queremos estimar la distribucion de salida;
- en que backend queremos ejecutar el circuito.

Esta explicitud es pedagogicamente muy valiosa, porque en computacion cuantica muchos malentendidos nacen precisamente de no distinguir estas capas.

## 3. Estructura minima de un circuito

En Qiskit, un flujo elemental suele incluir:

1. crear un `QuantumCircuit`;
2. aplicar puertas;
3. medir qubits;
4. ejecutar el circuito en un simulador;
5. inspeccionar cuentas o distribuciones de resultados.

Esta estructura obliga a pensar con claridad que estado inicial tenemos, que transformaciones realizamos y que magnitud observable queremos estudiar.

Un circuito de un qubit con una puerta Hadamard y medicion puede escribirse como:

```python
from qiskit import QuantumCircuit

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)
```

Este circuito prepara el estado $|+\rangle$ y luego lo mide en la base computacional, produciendo aproximadamente un 50 por ciento de `0` y un 50 por ciento de `1` en muchas repeticiones.

## 4. Anatomia de `QuantumCircuit`

El objeto `QuantumCircuit` es el centro operativo de Qiskit. En el ejemplo anterior, `QuantumCircuit(1, 1)` significa:

- un qubit cuantico para la parte unitaria de la computacion;
- un bit clasico para almacenar el resultado de la medicion.

Esta distincion entre registro cuantico y registro clasico es importante. El circuito no "guarda" automaticamente el resultado de una medicion si no se ha previsto un destino clasico para ella.

## 5. Visualizacion del circuito

Una ventaja practica de Qiskit es que el circuito puede dibujarse de forma legible. Eso ayuda a comprobar si la estructura implementada coincide con la idea teorica. Por ejemplo:

```python
qc.draw("text")
```

La visualizacion no es un detalle menor. En proyectos reales, detectar errores de orden, qubit objetivo o medicion mal ubicada es mucho mas facil cuando el diagrama esta a la vista.

## 6. Simuladores y backends

En la practica, Qiskit distingue entre:

- la definicion abstracta del circuito;
- el backend sobre el que se ejecuta;
- el tipo de resultado que queremos recuperar.

Al principio conviene trabajar con simuladores ideales porque permiten concentrarse en la logica del circuito sin introducir de inmediato ruido, errores de lectura o restricciones fisicas del hardware.

En una primera etapa del aprendizaje, hay tres preguntas utiles:

1. queremos estudiar el estado final ideal?
2. queremos estudiar cuentas de medicion?
3. queremos estudiar como cambia el circuito al adaptarlo a hardware?

Cada una de estas preguntas sugiere herramientas ligeramente distintas dentro de Qiskit.

## 7. Cuentas, shots y estadistica

Una ejecucion de un circuito cuantico no suele bastar para entender su comportamiento. Normalmente se repite muchas veces y se recopilan cuentas de salida. Esta repeticion se expresa con el numero de `shots`.

La razon es profunda: la teoria cuantica predice distribuciones de probabilidad, no una respuesta determinista utilizable en una sola corrida en todos los casos. Por eso Qiskit trabaja muy bien con histogramas y diccionarios de cuentas.

En un circuito con Hadamard ideal sobre un qubit, una salida tipica con muchos `shots` deberia acercarse a

- `0` alrededor del 50 por ciento;
- `1` alrededor del 50 por ciento.

La fluctuacion restante no es un error conceptual, sino una consecuencia estadistica natural del muestreo finito.

## 8. Ejecucion ideal frente a estado cuantico

Hay dos tipos de aprendizaje que conviene no mezclar:

- aprender a leer resultados de medicion;
- aprender a inspeccionar el estado cuantico antes de medir.

En muchos ejemplos introductorios interesa primero la medicion, porque es la forma experimentalmente relevante de conectar con resultados clasicos. Pero en otras situaciones es pedagogicamente muy util mirar el vector de estado ideal para entender que amplitudes se han preparado.

Qiskit permite ambas aproximaciones. La clave didactica es usar cada una en el momento adecuado.

## 9. Estados de Bell en Qiskit

Tambien podemos construir un estado de Bell con pocas lineas:

```python
from qiskit import QuantumCircuit

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])
```

Al simular este circuito, deberiamos observar principalmente los resultados `00` y `11`.

Este ejemplo es importante porque muestra como un circuito muy corto ya es capaz de:

- preparar superposicion;
- propagar control de un qubit a otro;
- generar entrelazamiento;
- producir correlaciones no clasicas en la salida medida.

## 10. Preparacion, evolucion y medicion

Qiskit ayuda a separar tres momentos conceptuales:

### Preparacion

Consiste en definir el estado de partida. A veces es simplemente $|0 \dots 0\rangle$, pero otras veces hay que preparar superposiciones o estados auxiliares concretos.

### Evolucion

Es la aplicacion de puertas cuanticas, es decir, de operadores unitarios. Aqui es donde vive la logica del algoritmo.

### Medicion

Convierte el proceso cuantico en datos clasicos analizables. Sin una estrategia de medicion adecuada, un circuito puede ser matematicamente correcto pero experimentalmente poco informativo.

## 11. Transpilacion

A medida que el tutorial avance, aparecera una idea nueva: el circuito que diseñamos de forma abstracta no siempre coincide con el circuito que un dispositivo real puede ejecutar directamente.

La transpilacion es el proceso por el que Qiskit:

- reescribe el circuito;
- lo adapta al conjunto de puertas soportadas;
- respeta restricciones de conectividad entre qubits;
- intenta optimizar profundidad y coste.

Aunque al principio podemos trabajar sin entrar a fondo en este tema, es importante mencionarlo cuanto antes porque muestra que la computacion cuantica real tiene una capa arquitectonica adicional que no aparece en el pizarron.

## 12. Simulacion ideal frente a hardware real

Es esencial distinguir estos dos niveles:

### Simulacion ideal

- no hay ruido;
- las puertas se aplican exactamente;
- la medicion sigue la distribucion teorica ideal.

### Hardware real

- hay decoherencia;
- las puertas tienen fidelidad finita;
- la lectura puede introducir errores;
- la arquitectura impone restricciones concretas.

Uno de los grandes errores pedagogicos seria presentar ambos escenarios como si fueran lo mismo. Qiskit es especialmente valioso porque permite aprender primero en un entorno ideal y, mas adelante, introducir realismo de forma gradual.

## 13. Buenas practicas para trabajar con Qiskit en este proyecto

- mantener notebooks pequenos y enfocados;
- enlazar cada cuaderno con un articulo teorico correspondiente;
- explicar siempre que concepto fisico representa cada instruccion;
- distinguir entre simulacion ideal y hardware real;
- aclarar cuando un ejemplo es pedagogico y cuando pretende ser tecnicamente representativo;
- no usar demasiada abstraccion de libreria si eso oculta la idea que se quiere enseñar;
- enseñar primero circuitos pequeños que puedan leerse visualmente de un vistazo.

## 14. Errores comunes al empezar

Algunos tropiezos frecuentes son:

- olvidar que la medicion destruye la coherencia util del estado;
- interpretar una sola corrida como si revelara el estado completo;
- confundir vector de estado ideal con cuentas de salida;
- creer que una puerta de fase "no hace nada" porque no cambia una medicion inmediata en cierta base;
- perder de vista que el orden de las puertas importa.

Reconocer pronto estos errores ahorra mucha confusion posterior.

## 15. Relacion entre teoria y practica

Qiskit no reemplaza la teoria. Lo que hace es volverla manipulable:

- las amplitudes se convierten en estados simulados;
- las puertas se convierten en operaciones concretas;
- la medicion se convierte en estadisticas de resultados;
- la arquitectura del backend obliga a pensar en restricciones fisicas reales.

Por eso este tutorial debe usar Qiskit no como decoracion, sino como instrumento de comprension.

## 16. Hacia donde debe crecer esta seccion

Una seccion madura de Qiskit deberia ir incorporando progresivamente:

- simuladores y `Statevector`;
- histogramas de cuentas;
- transpilation basica;
- circuitos parametrizados;
- primeros algoritmos completos;
- comparacion entre circuito ideal y circuito adaptado a backend;
- introduccion al ruido y a la mitigacion elemental.

## 17. Ideas clave

- Qiskit permite construir y estudiar circuitos cuanticos desde Python.
- Su valor didactico esta en hacer explicitas las capas del problema.
- La ejecucion practica exige pensar en backends, `shots`, estadistica y transpilacion.
- No debe confundirse simulacion ideal con ejecucion real en hardware.
- Un buen uso de Qiskit refuerza la teoria en lugar de taparla.
