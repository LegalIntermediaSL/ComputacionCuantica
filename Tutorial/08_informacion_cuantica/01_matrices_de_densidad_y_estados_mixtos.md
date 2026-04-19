# Matrices de densidad y estados mixtos

## 1. Por que no basta con estados puros

En una primera etapa del aprendizaje solemos describir todo con vectores de estado puros. Ese lenguaje es suficiente para muchos circuitos ideales, pero se queda corto cuando:

- no conocemos exactamente el estado del sistema;
- solo observamos una parte de un sistema compuesto;
- queremos describir ruido o mezcla estadistica;
- analizamos resultados efectivos tras ignorar grados de libertad.

En todos esos casos aparece de forma natural la matriz de densidad.

## 2. Definicion

Si el sistema esta en un estado puro $|\\psi\\rangle$, la matriz de densidad asociada es

$$
\\rho = |\\psi\\rangle\\langle\\psi|.
$$

Este objeto contiene la misma informacion fisica que el estado puro, pero se generaliza de forma natural a estados mixtos.

## 3. Estados mixtos

Un estado mixto representa una mezcla estadistica de varios estados posibles. Si el sistema esta en $|\\psi_i\\rangle$ con probabilidad $p_i$, entonces

$$
\\rho = \\sum_i p_i |\\psi_i\\rangle\\langle\\psi_i|.
$$

La diferencia entre superposicion y mezcla es fundamental:

- una superposicion conserva coherencia entre amplitudes;
- una mezcla representa incertidumbre clasica o perdida de acceso a parte de la informacion.

## 4. Propiedades basicas

Una matriz de densidad fisica debe satisfacer:

- hermiticidad;
- traza igual a uno;
- positividad.

Estas condiciones garantizan que el objeto representa un estado cuantico fisicamente admisible.

## 5. Valor pedagogico

Introducir matrices de densidad cambia el tono del tutorial: ya no describimos solo la mecanica cuantica idealizada de estados puros, sino una capa mas cercana a informacion cuantica realista, ruido y subsistemas.

## 6. Ideas clave

- Las matrices de densidad generalizan la descripcion por vectores de estado.
- Los estados mixtos no son lo mismo que las superposiciones.
- Esta herramienta es indispensable para ruido, subsistemas y entropia.
