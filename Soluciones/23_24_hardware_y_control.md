# Problemas Resueltos: Hardware y Control

## P1: El problema del oscilador armónico puro
**Pregunta:** ¿Por qué no podemos usar un circuito LC convencional (sin unión de Josephson) como qubit?
**Solución:**
En un oscilador armónico ideal, los niveles de energía están equiespaciados ($\Delta E = \hbar \omega$). Esto significa que la energía necesaria para pasar de $|0\rangle \to |1\rangle$ es la misma que para pasar de $|1\rangle \to |2\rangle$. Un pulso de control no podría "aislar" los dos niveles básicos, provocando fugas masivas hacia estados superiores. La unión de Josephson introduce una no-linealidad que cambia el espaciado, permitiendo el direccionamiento selectivo.

## P2: Calibración de amplitud (Rabi)
**Pregunta:** Si un pulso de amplitud $0.5 V$ y duración $100 ns$ realiza una rotación $\pi$, ¿qué amplitud debemos usar para una puerta $\sqrt{X}$ (pulso $\pi/2$) con la misma duración?
**Solución:**
En el régimen lineal de amplitud, la rotación es proporcional al área del pulso. Si mantenemos la duración constante, la amplitud debe reducirse a la mitad: $0.25 V$.

## P3: CRYSTALS-Kyber y Computación Cuántica
**Pregunta:** ¿Por qué se dice que Kyber es "seguro" frente a computadoras cuánticas si Shor rompe RSA?
**Solución:**
El algoritmo de Shor se basa en encontrar el periodo de una función exponencial en grupos abelianos finitos. Kyber se basa en problemas de retículos (Lattices), como el *Learning With Errors (LWE)*. Hasta hoy, no existe ningún algoritmo cuántico conocido que proporcione una aceleración exponencial para resolver problemas de retículos de alta dimensión, lo que lo hace un candidato sólido para la era PQC.
