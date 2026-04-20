# BQP, oraculos y speedup

## Prerequisitos

- Algoritmos cuanticos introductorios.
- Idea basica de oraculo.
- Diferencia entre coste y numero de pasos.

## Objetivos

- entender por que la ventaja cuantica se formula en terminos de problemas y recursos;
- introducir la intuicion minima de BQP;
- conectar algoritmos vistos con modelos de consulta y speedup.

## 1. Por que hace falta hablar de complejidad

A medida que el tutorial crece, ya no basta con mostrar circuitos elegantes o algoritmos llamativos. Tambien hace falta responder una pregunta mas exigente: cuando decimos que la computacion cuantica puede ofrecer una ventaja, de que tipo de ventaja estamos hablando exactamente?

Esa pregunta pertenece al terreno de la complejidad computacional.

## 2. La idea de BQP

Una de las clases de complejidad mas citadas en computacion cuantica es `BQP`, abreviatura de `Bounded-Error Quantum Polynomial Time`.

La intuicion minima que necesitamos aqui es:

- recoge problemas resolubles eficientemente por un computador cuantico;
- permite una probabilidad de error acotada;
- y sirve como referencia para comparar el modelo cuantico con modelos clasicos.

No hace falta convertir este tutorial en un curso formal de complejidad para captar la idea central: una promesa seria de ventaja debe hablar de familias de problemas, escalado y recursos.

## 3. Oraculos y consultas

En muchos algoritmos introductorios, como Deutsch-Jozsa o Bernstein-Vazirani, aparece la idea de un oraculo. Pedagogicamente, un oraculo puede verse como una caja negra que implementa cierta funcion y a la que preguntamos informacion de forma estructurada.

Eso es importante porque muchos speedups cuanticos se entienden inicialmente en el llamado modelo de consultas:

- cuantas veces debemos acceder al oraculo?;
- que estructura puede explotar el algoritmo?;
- y como se compara ese coste con el mejor enfoque clasico conocido?

## 4. Que significa speedup

La palabra `speedup` suele usarse demasiado rapido. Conviene distinguir:

- mejora constante o leve;
- mejora polinomica;
- mejora exponencial;
- y superioridad solo en modelos muy restringidos.

No todo resultado llamativo equivale a una ventaja cuantica robusta en el sentido mas fuerte.

## 5. Valor dentro del proyecto

Este bloque ayuda a poner en contexto los algoritmos ya vistos. No basta con conocer Grover o la QFT: tambien hay que entender bajo que criterio se consideran interesantes.

## 6. Errores comunes

- llamar ventaja cuantica a cualquier resultado llamativo;
- olvidar que el modelo de comparacion importa;
- pensar que una separacion en modelo de consultas resuelve por si sola la utilidad practica.

## 7. Ejercicios sugeridos

1. Explica con tus palabras por que no basta con que un circuito sea dificil de entender para hablar de ventaja cuantica.
2. Relaciona la idea de oraculo con Deutsch-Jozsa y Bernstein-Vazirani.
3. Distingue entre mejora polinomica y mejora exponencial.

## 8. Material asociado

- Cuaderno: [28_complejidad_y_bqp_intuicion.ipynb](../../Cuadernos/ejemplos/28_complejidad_y_bqp_intuicion.ipynb)
- Resumen: [08_complejidad_y_tomografia.md](../../Resumenes/08_complejidad_y_tomografia.md)
- Articulo relacionado: [Realismo sobre ventaja cuantica](../13_limites_actuales_y_realismo/02_realismo_sobre_ventaja_cuantica.md)

## Navegacion

- Anterior: [POVM: intuicion y medicion generalizada](../17_medicion_avanzada_y_observables/02_povm_intuicion_y_medicion_generalizada.md)
- Siguiente: [Limites de la ventaja y comparacion clasica](02_limites_de_la_ventaja_y_comparacion_clasica.md)
