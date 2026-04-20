# Qiskit: simuladores, estado cuantico y resultados

## 1. Por que no basta con “ejecutar un circuito”

Cuando alguien empieza con Qiskit suele pensar que el objetivo es simplemente construir un circuito y ejecutarlo. Pero muy pronto aparece una distincion importante: no siempre queremos observar lo mismo del circuito.

En algunos casos queremos saber:

- cual es el estado cuantico ideal antes de medir;
- que cuentas de salida aparecen al repetir muchas mediciones;
- como se comporta el circuito bajo diferentes modelos de simulacion.

Estas preguntas no son equivalentes. De hecho, aprender a distinguirlas es una de las claves para usar Qiskit con madurez.

## 2. Simular el estado frente a simular mediciones

La descripcion de un estado puro ideal es extremadamente informativa desde el punto de vista teorico. Permite ver directamente amplitudes y fases. Sin embargo, no corresponde a lo que devuelve un detector clasico al final de un experimento.

En cambio, una simulacion de mediciones con muchos `shots` devuelve distribuciones de resultados, que si se parecen mas al tipo de dato que obtendriamos experimentalmente.

Por eso conviene pensar en dos niveles de trabajo:

### Nivel estructural

Se pregunta por el estado cuantico generado por el circuito.

### Nivel experimental

Se pregunta por la estadistica observable al medir.

Ambos niveles son correctos, pero responden a necesidades distintas.

## 3. El papel de `Statevector`

Una herramienta especialmente valiosa en Qiskit para aprendizaje es `Statevector`. Permite obtener el estado ideal asociado a un circuito sin medicion final. Esto hace visibles objetos que de otro modo quedarían ocultos tras el colapso de la medicion.

Por ejemplo, si un circuito prepara

$$
|+\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle),
$$

el uso de `Statevector` deja clara la igualdad de amplitudes. Si solo miráramos cuentas de salida, veríamos una distribucion aproximadamente uniforme, pero no veríamos directamente la fase relativa ni el detalle algebraico del estado.

## 4. El papel de las cuentas

Las cuentas, en cambio, son el lenguaje natural de la observacion repetida. Si un circuito se ejecuta muchas veces, Qiskit permite registrar cuantas veces aparece cada string de bits clasicos. En un qubit con Hadamard, por ejemplo, esperamos algo cercano a:

- `0`: aproximadamente 50 por ciento;
- `1`: aproximadamente 50 por ciento.

La diferencia entre decir “el estado es $|+\\rangle$” y decir “las cuentas se reparten aproximadamente mitad y mitad” es profunda:

- la primera afirmacion es estructural;
- la segunda es estadistica.

## 5. Shots y precision estadistica

El numero de `shots` determina cuantas veces repetimos el experimento. Con pocos `shots`, las fluctuaciones son grandes. Con muchos `shots`, la distribucion observada se aproxima mejor a la prediccion teorica.

Eso convierte a Qiskit en una herramienta excelente para enseñar algo importante: incluso en un modelo ideal, los resultados observables no son “exactamente iguales” a las probabilidades teoricas, sino estimaciones muestreadas de ellas.

## 6. Histograma mental de resultados

Aunque un notebook pueda despues dibujar histogramas, conviene desarrollar primero una intuicion cualitativa:

- si un estado esta muy concentrado en un resultado, el histograma deberia reflejarlo claramente;
- si dos resultados comparten amplitud similar, el histograma mostrara competencia estadistica;
- si una interferencia cancela amplitudes, el resultado correspondiente deberia desaparecer o reducirse drásticamente.

Esto hace que interpretar cuentas sea mucho mas que leer un diccionario: significa entender que geometria de amplitudes hay detras.

## 7. Simulacion ideal frente a simulacion mas realista

No toda simulacion significa lo mismo. Una simulacion ideal ignora ruido, decoherencia y errores de lectura. Otras simulaciones pueden incorporar modelos mas cercanos al comportamiento experimental.

Por eso es sano mantener siempre esta pregunta en mente:

> Que exactamente estoy simulando?

Sin esa pregunta, es facil sacar conclusiones equivocadas sobre la robustez o fragilidad de un circuito.

## 8. Buenas practicas para leer resultados

- no interpretar una sola corrida como si describiera el estado completo;
- comparar cuentas con la prediccion teorica del circuito;
- distinguir entre estados equivalentes en una base y no equivalentes en otra;
- recordar que una fase puede no verse directamente en una medicion inmediata;
- usar estado ideal y cuentas como herramientas complementarias, no rivales.

## 9. Ideas clave

- Qiskit permite estudiar tanto el estado ideal como la estadistica de medicion.
- `Statevector` y las cuentas responden a preguntas distintas.
- Los `shots` introducen una capa de muestreo estadistico que no debe ignorarse.
- Interpretar correctamente los resultados exige distinguir estructura cuantica y salida clasica observable.

## Navegacion

- Anterior: [Algoritmos cuanticos introductorios](../01_fundamentos/07_algoritmos_cuanticos_introductorios.md)
- Siguiente: [Qiskit: transpilacion, ruido y paso hacia hardware](09_qiskit_transpilacion_ruido_y_hardware.md)
