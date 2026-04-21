# Problemas Resueltos: Algoritmos Variacionales y Aplicaciones

## P1: El papel del Ansatz
**Pregunta:** ¿Qué ocurre si el Ansatz no es "expresivo" suficiente para un Hamiltoniano dado?
**Solución:**
VQE solo encontrará el mínimo dentro del espacio de estados que el Ansatz puede generar. Si el estado fundamental real está fuera de ese espacio, el algoritmo convergerá a una cota superior de la energía real, introduciendo un error sistemático ineludible.

## P2: Mapeo de H2
**Pregunta:** ¿Cómo se traduce el repudio de electrones a operadores de Qiskit?
**Solución:**
Se utiliza la transformación de Jordan-Wigner o Parity Mapping. Estos convierten los operadores de creación/aniquilación de fermiones en cadenas de operadores Pauli ($X, Y, Z, I$). Por ejemplo, la interacción de intercambio se convierte en términos de la forma $X_i X_j + Y_i Y_j$.
