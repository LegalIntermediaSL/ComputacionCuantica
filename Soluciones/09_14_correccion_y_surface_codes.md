# Problemas Resueltos: Corrección de Errores y Surface Codes

## P1: Medición de Síndrome en Código de Repetición
**Pregunta:** Si tenemos 3 qubits de datos y medimos los síndromes $Z_1Z_2 = 1$ (error) y $Z_2Z_3 = -1$ (no error), ¿dónde está el fallo?
**Solución:**
$Z_1Z_2=1$ indica que el qubit 1 y el 2 son diferentes. $Z_2Z_3=-1$ indica que el 2 y el 3 son iguales. Por mayoría de votos, el error reside en el **qubit 1**.

## P2: Placas de Estabilización Z en Surface Codes
**Pregunta:** ¿Por qué usamos CNOTs desde los qubits de datos hacia el ancilla para medir paridad Z?
**Solución:**
Cada CNOT propaga la paridad del bit hacia el ancilla. Una CNOT no altera el valor del bit de control (datos), por lo que podemos extraer la información de si hay un "bit-flip" sin colapsar la fase cuántica del sistema global.
