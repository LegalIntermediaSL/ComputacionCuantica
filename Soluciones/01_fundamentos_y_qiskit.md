# Problemas Resueltos: Fundamentos y Qiskit

## P1: Normalización de un estado de Bell
**Pregunta:** ¿Está el estado $|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$ normalizado?
**Solución:**
Calculamos la norma al cuadrado sumando los módulos de las amplitudes al cuadrado:
$$\langle \Phi^+ | \Phi^+ \rangle = \left| \frac{1}{\sqrt{2}} \right|^2 + \left| \frac{1}{\sqrt{2}} \right|^2 = \frac{1}{2} + \frac{1}{2} = 1$$
El estado está correctamente normalizado.

## P2: Acción de la Puerta Hadamard
**Pregunta:** ¿Cuál es el resultado de aplicar $H$ al estado $|+\rangle$?
**Solución:**
Como $H$ es su propia inversa ($H^2 = I$) y $|+\rangle = H|0\rangle$, entonces $H|+\rangle = H(H|0\rangle) = |0\rangle$. 
Geométricamente, la primera Hadamard lleva el vector del polo norte al ecuador, y la segunda lo devuelve al polo norte.
