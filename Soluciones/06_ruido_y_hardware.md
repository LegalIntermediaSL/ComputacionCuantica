# Problemas Resueltos: Ruido y Hardware NISQ

## P1: Relación entre T1 y T2
**Pregunta:** ¿Por qué se dice que el desfase ($T_2$) es independiente de la pérdida de energía ($T_1$)?
**Solución:**
El tiempo de coherencia total obedece a $\frac{1}{T_2} = \frac{1}{2T_1} + \frac{1}{T_\phi}$. 
Incluso si no hubiera pérdida de energía ($T_1 \to \infty$), el qubit puede perder su fase debido a fluctuaciones magnéticas externas ($T_\phi$), lo que limita $T_2$ a valores muy cortos en hardware real.

## P2: Zero Noise Extrapolation (ZNE)
**Pregunta:** ¿Cómo estimamos el valor a ruido cero si solo tenemos hardware ruidoso?
**Solución:**
Ejecutamos el experimento con ruido $E$, luego escalamos el ruido a $2E$ y $3E$ (insertando pares de puertas identidad). Ajustamos una curva (lineal o polinómica) a los puntos $(E, \langle O \rangle_E), (2E, \langle O \rangle_{2E}), \dots$ y calculamos el valor de la función en el punto teórico $0$.
