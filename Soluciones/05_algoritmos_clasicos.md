# Problemas Resueltos: Algoritmos Clásicos

## P1: Oráculo de Deutsch-Jozsa Constante
**Pregunta:** Si tenemos una función constante $f(x) = 1$ para todo $x$, ¿qué mediremos al final del algoritmo?
**Solución:**
El registro de entrada antes de la Hadamard final será:
$$
\frac{1}{\sqrt{2^n}} \sum_x (-1)^{f(x)} |x\rangle = - \frac{1}{\sqrt{2^n}} \sum_x |x\rangle = - |+\rangle^{\otimes n}
$$
Al aplicar $H^{\otimes n}$ sobre $- |+\rangle^{\otimes n}$, obtenemos el estado $-|00\dots0\rangle$. La medición devolverá siempre la cadena de ceros (indicando que es constante).

## P2: Inversión sobre la media en Grover
**Pregunta:** Explica el efecto del operador de difusión $D = 2|s\rangle\langle s| - I$.
**Solución:**
Este operador refleja las amplitudes respecto a su valor promedio. Si una amplitud es mayor que la media (el estado marcado tras el oráculo tiene amplitud negativa, por lo que está muy por debajo de la media), la inversión la "empuja" muy por encima de la media, amplificando la probabilidad de éxito.
