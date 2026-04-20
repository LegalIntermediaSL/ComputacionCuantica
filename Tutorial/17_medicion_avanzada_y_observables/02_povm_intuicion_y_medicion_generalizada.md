# Medidas POVM (Positive Operator-Valued Measure)

## 1. Cuando $0$ y $1$ no son suficientes
Las medidas proyectivas elementales de hardware convencionales colapsan forzando ortogonalmente a un número de resultados exactamente igual al tamaño de base (2 resultados de colapso binario por cada qubit medido).
En experimentos ultra sofisticados (Criptografía QKD de BB84 o State Discrimination sin fallos), a menudo un analista cuántico desea formularle a la superposición preguntas sutiles "suaves", evitando destruir irremediablemente toda la información colapsando fuertemente el estado subyacente puramente a los polos opuestos.

**Las POVMs** son la teoría cuántica de medición generalizada absolutista. En lugar de estar confinados a Proyectores de Base aislados rígidos, POVM inyecta y expande el universo mediante la utilización matemática de tensores Operadores Positivos Genéricos $E_i$ tales que $\sum E_i = I$.

## 2. Abriendo dimensiones
Gracias a POVM, es perfectamente posible diseñar experimentos de medición para 1 sólo Qubit, y generar estadísticamente **3 o 4 posibles resultados crudos distintos de salida matemática**, a pesar de que el estado Qubit en sí posea meramente 2 bases de almacenamiento $|0\rangle$ y $|1\rangle$.
¿El truco algorítmico detrás de POVM? Entrelazar subrepticiamente tu Qubit experimental temporalmente contra un Ancillar o "Medidor Físico externo acoplado", y arrojar mediciones sobre el entorno completo de forma difusa o "Weak Measurement", abstrayendo de asfixiar bruscamente al estado objetivo original. Es la máxima exquisitez final del tratamiento informático analógico cuántico para criptógrafos y radares cuánticos.

## Navegacion

- Anterior: [Proyectores, valores esperados y varianza](01_proyectores_valores_esperados_y_varianza.md)
- Siguiente: [BQP, oraculos y speedup](../18_complejidad_cuantica/01_bqp_oraculos_y_speedup.md)
