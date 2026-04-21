# Simplificación y Optimización Gráfica

En este capítulo aplicamos las reglas del ZX-Calculus para demostrar cómo circuitos aparentemente distintos son, en realidad, idénticos.

## La Magia de la Fusión

Considera una secuencia de dos puertas $Z$. En un circuito tradicional, son dos bloques. En ZX, son dos arañas verdes conectadas. Por la regla de **Spider Fusion**, se convierten en una sola. Esto parece trivial, pero cuando tienes miles de puertas, la fusión masiva reduce la profundidad del circuito drásticamente.

## El Gadget de Fase (Phase Gadgets)

Un patrón común en algoritmos como **QAOA** es la rotación multiqubit (ej: $e^{-i\theta Z \otimes Z}$). En circuitos estándar, esto requiere una "escalera" de puertas CNOT. En ZX, esto se representa como un **Phase Gadget**: una araña con una fase conectada a otras arañas de control.
Manipular estos "gadgets" permite reordenar el circuito de formas que la intuición clásica del compilador no permitiría.

## De Grafos a Circuitos (Extracción)

El flujo de trabajo de un optimizador basado en ZX es:
1. **Circuito $\to$ Grafo:** Convertir el código Qiskit a arañas.
2. **Simplificación:** Aplicar fusión, reglas de pivote y eliminación de identidades locales.
3. **Extracción:** Volver a convertir el grafo simplificado en un circuito de puertas.

Este proceso puede reducir el número de puertas CNOT (las más ruidosas) hasta en un 30-40% en algoritmos variacionales.

## Navegación
- Anterior: [El lenguaje de las arañas: Introducción al ZX-Calculus](01_el_lenguaje_de_las_aranas.md)
- Siguiente: [Protocolos de Internet Cuántico](../27_internet_cuantico_and_comunicaciones/01_redes_y_protocolos_de_entrelazamiento.md)
