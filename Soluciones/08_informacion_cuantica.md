# Problemas Resueltos: Información Cuántica

## P1: Estado reducido de un estado de Bell
**Pregunta:** Calcula la matriz de densidad reducida del primer qubit de $|\Psi^-\rangle = \frac{1}{\sqrt{2}}(|01\rangle - |10\rangle)$.
**Solución:**
La matriz global es $\rho = |\Psi^-\rangle\langle \Psi^-|$. Al aplicar la traza parcial sobre el segundo qubit:
$$ \rho_1 = \text{Tr}_2(\rho) = \frac{1}{2}(|0\rangle\langle 0| + |1\rangle\langle 1|) = \frac{1}{2} I $$
El resultado es un estado **máximamente mezclado**. Esto demuestra que en un sistema perfectamente entrelazado, no tenemos información absoluta sobre los subsistemas individuales.
