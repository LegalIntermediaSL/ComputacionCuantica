# Bernstein-Vazirani

## 1. Motivacion

El algoritmo de Bernstein-Vazirani muestra como recuperar una cadena binaria oculta con una sola consulta cuantica al oraculo, en un problema donde la estrategia clasica elemental requeriria varias consultas.

## 2. Idea central

La estructura del circuito es parecida a Deutsch-Jozsa, pero ahora la fase acumulada en la superposicion codifica directamente la cadena buscada. Tras una capa final de Hadamards, el registro de salida revela la informacion de forma muy limpia.

## 3. Leccion pedagogica

Este algoritmo es muy valioso porque:

- muestra un ejemplo donde el circuito devuelve directamente un string estructurado;
- refuerza el papel de la fase;
- ayuda a entender por que los oraculos en computacion cuantica no deben pensarse como cajas negras clasicas corrientes.
