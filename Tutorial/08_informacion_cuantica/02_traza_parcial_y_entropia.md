# Traza parcial y entropía

## 1. Subsistemas y Entorno

En el artículo anterior hemos visto cómo la matriz de densidad nos permite lidiar cómodamente con la incertidumbre estadística y el "abandono" de los estados matemáticamente puros para enfrentarnos a un conocimiento incompleto del universo. 

Sin embargo, una de las realidades más apabullantes de la cuántica aparece precisamente cuando evaluamos sistemas que, inicialmente puros, sufren de interacciones complejas. Cuando un sistema cuántico compuesto tiene múltiples partes y grados de libertad —por ejemplo un qubit de un sistema de comunicación entrelazado interactuando con fotones errantes o simplemente evaluando uno solo de dos qubits entrelazados de manera compartida— y **no nos interesa observar todo el entorno sino solo nuestro subsistema**, necesitamos una forma matemática efectiva de eliminar esa información. Dicha operación se llama **traza parcial**.

## 2. La máquina de "ignorar": Traza Parcial

Si disponemos de un sistema compuesto por dos partes, $A$ y $B$, descrito conjuntamente por un estado y su respectiva matriz de densidad de universo global $\rho_{AB}$, el estado reducido que un observador local en $A$ visualizaría en su laboratorio, ignorando lo que le suceda a $B$, viene dado por:

$$
\rho_A = \text{Tr}_B(\rho_{AB})
$$

La operación $\text{Tr}_B$ "promedia" lineal e irremediablemente todos los grados de libertad matemáticos que habitaban sobre la base del espacio de Hilbert de $B$.

**Matemáticamente**, si los autoestados bases ortogonales de $B$ son $\{|b_i\rangle\}$, entonces la matriz resultante en $A$ puede calcularse explícitamente rastreando sobre dicha base:
$$
\text{Tr}_B(\rho_{AB}) = \sum_i (I_A \otimes \langle b_i|) \, \rho_{AB} \, (I_A \otimes |b_i\rangle)
$$

## 3. Ejemplo paradigmático: El Estado de Bell

Este punto es donde la matriz de densidad paga sus verdaderas facturas pedagógicas. Analicemos uno de los cuatro estados de base de Bell (puramente entrelazado en un sistema bi-partito), el estado $|\Phi^+\rangle$:

$$
|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}
$$
Se trata de un estado $100\%$ puro que engloba un profundo entrelazamiento correlacionado entre $A$ y $B$.
La matriz combinada global será de la forma de producto exterior puro:
$$
\rho_{AB} = |\Phi^+\rangle\langle\Phi^+| = \frac{1}{2} (|00\rangle\langle 00| + |00\rangle\langle 11| + |11\rangle\langle 00| + |11\rangle\langle 11|)
$$
Pura ($\text{Tr}(\rho_{AB}^2) = 1$) bajo observabilidad global.

¿Qué observará Alice, que está manejando **solo el subsistema $A$**, y no tiene acceso a medir el entorno / qubit de Bob (el subsistema $B$)? Al ejecutar la traza parcial sacando las bases de B:
$$
\rho_A = \text{Tr}_B \left( \frac{1}{2} (|0A, 0B\rangle\langle 0A, 0B| + \dots) \right)
$$
Los términos cruzados $|0\rangle\langle 1|$ del sistema $B$ caen a 0 a través de la contracción, revelándonos únicamente:
$$
\rho_A = \frac{1}{2} |0\rangle\langle 0| + \frac{1}{2} |1\rangle\langle 1| = \frac{I}{2}
$$

**¡El estado ha transicionado mágicamente!** Alice observa un objeto totalmente deshecho (una mezcla pura, de incertidumbre máxima) porque la "información de fase estructural" no habita en $A$ ni en $B$ aislados. La información reside en el **vínculo global entrelazado**. 
Al "ignorar" a Bob, el sistema $A$ para Alice aparece ineludiblemente bajo entropía máxima y un ruido clásico.

## 4. Entropía de von Neumann

Para no tener que hablar de pureza usando adjetivos, la Física optó por asentar la analogía con la termodinámica para codificar este "nivel de ignorancia".
La **entropía de von Neumann**, extendiendo directamente ideas de entropía clásica de Shannon para matrices probabilísticas generalizadas de mecánica cuántica, se define como:

$$
S(\rho) = - \text{Tr}(\rho \log_2 \rho)
$$

Sus propiedades revelan una capa cuantitativa de información subyacente increíble:

- **Si el sistema global es un estado puro:** $S(\rho) = 0$. Conocemos absolutamente todo.
- **Si el estado es una mezcla máxima en $d$ dimensiones:** La entropía es gigantesca y satura $S(\rho) = \log_2(d)$. No poseemos la más mínima idea predictiva de qué vamos a extraer en futuras observaciones.
- En caso de **Entropía de entrelazamiento:** En un sistema de bipartición $AB$ puro general, la forma definitiva de calcular cuantificablemente qué tan "estrechamente vinculados e interdependientes" estaban un sistema y otro (gracias y a causa del entrelazamiento), y cómo reaccionarán al corte de Decoherencia ambiental, recae directamente al evaluar $S(\rho_A)$ derivada de ejecutar una Traza Parcial.

## 5. Valor en el proyecto

La introducción a esta máquina fundamental de "rastreo parcial" es fundamental hoy porque:
- Permite construir las bases y el pánico motivacional hacia tratar de enjaular estados robustos con técnicas de **Corrección de Errores** ante su inevitable propagación destructiva.
- Establece la definición matemática oficial y rigurosa en Qiskit mediante los objetos programables `DensityMatrix` en vez del antiguo `Statevector`.

## 6. Ideas Clave

- La **traza parcial** es la herramienta analítica fundamental matemática para ignorar explícitamente ciertas partes o entornos en un problema interfasado.
- Reducir el universo de visión en un sistema verdaderamente entrelazado puro resulta matemáticamente en observar sistemas ruidosamente caóticos locales. El entrelazamiento puro es global y la parcialización inyecta ruido.
- La **entropía de von Neumann** provee el sistema métrico absoluto que permite inter-relacionar y jerarquizar computabilidad informacional, termodinámica de radiación y ruido subyacente de la computadora.

## Navegacion

- Anterior: [Matrices de densidad y estados mixtos](01_matrices_de_densidad_y_estados_mixtos.md)
- Siguiente: [Qubit logico y codigo de repeticion](../09_correccion_errores/01_qubit_logico_y_codigo_de_repeticion.md)
