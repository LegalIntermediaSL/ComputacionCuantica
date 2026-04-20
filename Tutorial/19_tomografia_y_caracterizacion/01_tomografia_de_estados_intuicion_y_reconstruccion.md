# Tomografia de estados: intuicion y reconstruccion

## Prerequisitos

- Esfera de Bloch.
- Medicion en distintas bases.
- Matrices de densidad.

## Objetivos

- entender por que la reconstruccion exige muchas mediciones;
- conectar tomografia con descripcion por matrices de densidad;
- situar la caracterizacion experimental dentro del curso.

## 1. El problema de partida

No podemos “abrir” un estado cuantico y leer directamente toda su informacion interna en una sola medicion. Por eso, si queremos caracterizar un estado preparado en el laboratorio, debemos repetir el experimento muchas veces y medir en distintas bases.

Esa es la idea basica de la tomografia de estados.

## 2. Intuicion operativa

La tomografia no recupera amplitudes magicamente de una sola ejecucion. Lo que hace es combinar estadisticas de medicion obtenidas desde varias perspectivas para reconstruir una descripcion compatible del estado.

En un qubit, esto se relaciona muy bien con la esfera de Bloch: estimar componentes asociadas a $X$, $Y$ y $Z$ ya nos acerca a reconstruir el estado.

## 3. Relacion con matrices de densidad

La formulacion natural de la tomografia usa matrices de densidad. Esto es importante porque permite tratar:

- estados puros;
- estados mixtos;
- ruido experimental;
- e informacion parcial.

## 4. Por que este bloque es valioso

La tomografia ayuda a que el tutorial no solo enseñe a preparar circuitos, sino tambien a pensar como se verifica y se caracteriza lo que un dispositivo realmente produce.

## 5. Errores comunes

- creer que una sola base de medida basta para reconstruir un estado general;
- confundir estadistica de medicion con acceso directo al vector de estado;
- olvidar el papel natural de las matrices de densidad.

## 6. Ejercicios sugeridos

1. Explica por que una sola base de medida no basta para reconstruir un estado general de un qubit.
2. Relaciona tomografia de estados con la esfera de Bloch.
3. Indica por que la formulacion con matrices de densidad es natural en este contexto.

## 7. Material asociado

- Cuaderno: [29_tomografia_estado_intuicion.ipynb](../../Cuadernos/ejemplos/29_tomografia_estado_intuicion.ipynb)
- Laboratorio: [14_densitymatrix_ruido_y_tomografia_guiada.ipynb](../../Cuadernos/laboratorios/14_densitymatrix_ruido_y_tomografia_guiada.ipynb)
- Resumen: [08_complejidad_y_tomografia.md](../../Resumenes/08_complejidad_y_tomografia.md)

## Navegacion

- Anterior: [Limites de la ventaja y comparacion clasica](../18_complejidad_cuantica/02_limites_de_la_ventaja_y_comparacion_clasica.md)
- Siguiente: [Fidelidad y caracterizacion operacional](02_fidelidad_y_caracterizacion_operacional.md)
