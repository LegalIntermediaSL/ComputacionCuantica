# Soluciones avanzadas seleccionadas

## 1. Valor esperado y varianza de Z en |+>

Sea

$$
|+\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}},
\qquad
Z =
\begin{pmatrix}
1 & 0 \\
0 & -1
\end{pmatrix}.
$$

Entonces

$$
\langle Z \rangle = \langle + | Z | + \rangle = 0.
$$

Esto refleja que el estado $|+\rangle$ no favorece ni el resultado `0` ni el resultado `1` en la base computacional.

Para la varianza usamos

$$
\mathrm{Var}(Z) = \langle Z^2 \rangle - \langle Z \rangle^2.
$$

Como $Z^2 = I$, se tiene

$$
\langle Z^2 \rangle = 1,
$$

y por tanto

$$
\mathrm{Var}(Z) = 1 - 0^2 = 1.
$$

La lectura conceptual es importante: valor esperado nulo no significa ausencia de fluctuacion. Aqui ocurre justo lo contrario: hay maxima dispersion compatible con ese observable.

## 2. Por que una POVM generaliza la medicion proyectiva

En una medicion proyectiva ortonormal, los operadores de medida son proyectores $P_i$ tales que:

- $P_i^2 = P_i$;
- $P_i P_j = 0$ para $i \neq j$;
- $\sum_i P_i = I$.

Una POVM reemplaza esos proyectores por operadores positivos $E_i$ que solo necesitan satisfacer

$$
\sum_i E_i = I.
$$

Esto permite describir mediciones efectivas donde los resultados no se corresponden necesariamente con una descomposicion ortogonal simple del espacio de Hilbert.

La idea pedagogica clave es esta: toda medicion proyectiva es un caso particular de medicion generalizada, pero no al reves.
