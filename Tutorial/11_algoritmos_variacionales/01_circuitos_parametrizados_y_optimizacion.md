# Circuitos parametrizados y optimizacion

## 1. Idea general

Un circuito parametrizado no fija desde el principio todos los angulos o transformaciones, sino que deja algunos parametros libres para que puedan ajustarse despues.

## 2. Por que esto importa

Esta idea es la base de los algoritmos variacionales. En lugar de construir un circuito completamente cerrado desde el principio, se define una familia de estados y se deja que un procedimiento de optimizacion busque buenos parametros.

## 3. Bucle hibrido

La logica general es:

1. elegir parametros iniciales;
2. ejecutar o simular el circuito;
3. evaluar una cantidad objetivo;
4. actualizar parametros desde un optimizador clasico;
5. repetir.

## 4. Valor pedagogico

Este esquema obliga a pensar la computacion cuantica no solo como una caja cerrada, sino como parte de un flujo hibrido mas amplio.

## Navegacion

- Siguiente: [VQE: intuicion](02_vqe_intuicion.md)
