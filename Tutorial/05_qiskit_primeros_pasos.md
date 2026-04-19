# Qiskit: primeros pasos

## 1. Por que Qiskit

Qiskit es uno de los entornos mas utilizados para trabajar con computacion cuantica desde Python. Permite:

- construir circuitos cuanticos;
- visualizarlos;
- simular su ejecucion;
- ejecutar experimentos en hardware cuantico cuando hay acceso disponible.

Para un tutorial, Qiskit tiene una ventaja decisiva: traduce ideas abstractas en circuitos concretos y resultados observables.

## 2. Estructura minima de un circuito

En Qiskit, un flujo elemental suele incluir:

1. crear un `QuantumCircuit`;
2. aplicar puertas;
3. medir qubits;
4. ejecutar el circuito en un simulador;
5. inspeccionar cuentas o distribuciones de resultados.

Esta estructura obliga a pensar con claridad que estado inicial tenemos, que transformaciones realizamos y que magnitud observable queremos estudiar.

## 3. Ejemplo basico

Un circuito de un qubit con una puerta Hadamard y medicion puede escribirse esquematicamente como:

```python
from qiskit import QuantumCircuit

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)
```

Este circuito prepara el estado $|+\rangle$ y luego lo mide en la base computacional, produciendo aproximadamente un 50 por ciento de `0` y un 50 por ciento de `1` en muchas repeticiones.

## 4. Estados de Bell en Qiskit

Tambien podemos construir un estado de Bell con pocas lineas:

```python
from qiskit import QuantumCircuit

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])
```

Al simular este circuito, deberiamos observar principalmente los resultados `00` y `11`.

## 5. Simuladores y backends

En la practica, Qiskit distingue entre:

- la definicion abstracta del circuito;
- el backend sobre el que se ejecuta;
- el tipo de resultado que queremos recuperar.

Al principio conviene trabajar con simuladores ideales porque permiten concentrarse en la logica del circuito sin introducir de inmediato ruido, errores de lectura o restricciones fisicas del hardware.

## 6. Medicion repetida y estadistica

Una ejecucion de un circuito cuantico no suele bastar para entender su comportamiento. Normalmente se repite muchas veces y se recopilan cuentas de salida. Esta repeticion es esencial porque la teoria predice distribuciones de probabilidad, no solo resultados individuales.

Por eso el trabajo con Qiskit encaja muy bien con el lenguaje probabilistico de la computacion cuantica: las amplitudes no se ven directamente, pero sus efectos se reconstruyen estadisticamente.

## 7. Relacion entre teoria y practica

Qiskit no reemplaza la teoria. Lo que hace es volverla manipulable:

- las amplitudes se convierten en estados simulados;
- las puertas se convierten en operaciones concretas;
- la medicion se convierte en estadisticas de resultados.

Por eso este tutorial debe usar Qiskit no como decoracion, sino como instrumento de comprension.

## 8. Buenas practicas para el proyecto

- mantener notebooks pequenos y enfocados;
- enlazar cada cuaderno con un articulo teorico correspondiente;
- explicar siempre que concepto fisico representa cada instruccion;
- distinguir entre simulacion ideal y hardware real;
- aclarar cuando un ejemplo es pedagogico y cuando pretende ser tecnicamente representativo.

## 9. Ideas clave

- Qiskit permite construir y estudiar circuitos cuanticos desde Python.
- Es una herramienta excelente para reforzar fundamentos.
- Su valor didactico crece cuando cada instruccion se conecta con una idea teorica clara.
- La ejecucion practica exige pensar en backends, repeticiones y estadistica de resultados.
