# Deutsch-Jozsa

## 1. Idea del problema

El problema de Deutsch-Jozsa pregunta, en una version idealizada, si una funcion booleana es constante o balanceada. Su valor pedagogico es grande porque muestra de forma muy limpia como una consulta cuantica puede codificar una propiedad global de la funcion.

## 2. Estructura del algoritmo

El esquema basico es:

1. preparar un registro de entrada en superposicion;
2. preparar un qubit auxiliar adecuado;
3. aplicar el oraculo;
4. aplicar Hadamards finales;
5. medir el registro de entrada.

## 3. Donde aparece la ventaja cuantica

La ventaja conceptual no viene de "evaluar todas las entradas de forma clasica simultanea", sino de usar la fase para hacer interferir las contribuciones de manera que la medicion revele una propiedad global.

## 4. Por que sigue siendo importante

Aunque no sea el algoritmo mas util en aplicaciones reales, es una excelente puerta de entrada a:

- el papel de los oraculos;
- la interferencia como recurso;
- la distincion entre informacion puntual e informacion global.
