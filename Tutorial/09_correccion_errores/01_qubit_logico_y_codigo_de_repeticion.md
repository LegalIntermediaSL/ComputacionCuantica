# Qubit logico y codigo de repeticion

## 1. Por que hace falta correccion

Los qubits fisicos actuales son fragiles. Si queremos computacion cuantica escalable, no basta con tener puertas elegantes en el papel: necesitamos maneras sistematicas de proteger la informacion cuantica frente a errores.

## 2. Qubit fisico frente a qubit logico

Un qubit fisico es el sistema elemental implementado en hardware. Un qubit logico, en cambio, es una entidad codificada en varios qubits fisicos para ganar robustez frente a errores.

## 3. Codigo de repeticion

El codigo de repeticion es la puerta de entrada conceptual mas simple. Su version cuantica no resuelve por si sola toda la complejidad del problema, pero ayuda a entender:

- por que la redundancia importa;
- por que no basta con copiar ingenuamente un estado cuantico;
- por que hacen falta mediciones de sindrome y no una lectura destructiva directa del estado.

## 4. Leccion central

La correccion de errores cuanticos no es solo una extension obvia de la clasica. El teorema de no-clonacion impide copiar estados arbitrarios de forma directa, de modo que la proteccion cuantica tiene que formularse con mucha mas sutileza.

## 5. Ideas clave

- El qubit logico se codifica en varios qubits fisicos.
- La redundancia cuantica no puede entenderse como una copia clasica trivial.
- La correccion de errores es una condicion de posibilidad para la escalabilidad real.
