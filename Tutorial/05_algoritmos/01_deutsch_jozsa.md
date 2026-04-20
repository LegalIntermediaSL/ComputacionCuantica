# Algoritmo de Deutsch-Jozsa

## 1. El Problema de la Caja Negra (Oráculo)
El algoritmo de Deutsch-Jozsa es históricamente significativo por ser el primer ejemplo de un algoritmo cuántico que supera exponencialmente al mejor algoritmo clásico determinista. El problema plantea lo siguiente: dada una función booleana $f: \{0,1\}^n \to \{0,1\}$ implementada en una caja negra (oráculo), debemos determinar si $f$ es **constante** (devuelve siempre 0 o siempre 1) o **balanceada** (devuelve 0 para la mitad de las entradas y 1 para la otra mitad).

Clásicamente, en el peor de los casos, necesitaríamos consultar el oráculo $2^{n-1} + 1$ veces para estar seguros. Cuánticamente, bastará con **una única consulta**.

## 2. El Mecanismo de Interferencia
La magia de Deutsch-Jozsa reside en el uso de la superposición y el *Phase Kickback*. Preparamos un registro de entrada de $n$ qubits en el estado $|+\rangle^{\otimes n}$ y un qubit auxiliar en el estado $|-\rangle$. Al aplicar el oráculo $U_f$, la información sobre $f(x)$ se "patea" hacia la fase del registro de entrada:

$$ U_f |x\rangle |-\rangle = (-1)^{f(x)} |x\rangle |-\rangle $$

Tras aplicar una capa final de puertas Hadamard, el estado final del registro de entrada es:
$$ |\psi_{final}\rangle = \sum_{y \in \{0,1\}^n} \left( \frac{1}{2^n} \sum_{x \in \{0,1\}^n} (-1)^{f(x) + x \cdot y} \right) |y\rangle $$

## 3. Interpretación del Resultado
Si medimos el registro de entrada:
- Si $f$ es **constante**, todas las contribuciones para estados distintos de $|0\rangle^{\otimes n}$ se cancelan destructivamente, y mediremos $|00\dots0\rangle$ con probabilidad 1.
- Si $f$ es **balanceada**, la contribución para el estado $|0\rangle^{\otimes n}$ se cancela exactamente ($\sum (-1)^{f(x)} = 0$), y mediremos cualquier otro estado distinto de cero.

Este es un ejemplo puro de **interferencia constructiva/destructiva** utilizada para extraer una propiedad global (la paridad de la función) sin evaluar los puntos individuales.

## Navegacion

- Anterior: [Qiskit Runtime y primitives](../04_qiskit/01_qiskit_runtime_y_primitives.md)
- Siguiente: [Bernstein-Vazirani](02_bernstein_vazirani.md)
