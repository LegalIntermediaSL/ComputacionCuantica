# Redes Neuronales Cuánticas (QNN)

Las QNN son la contraparte cuántica de las redes neuronales profundas. Se basan en **Circuitos Cuánticos Variacionales (PQC)**.

## 1. Estructura de una QNN
1. **Capa de Entrada:** Carga de datos clásicos (Feature Map).
2. **Capa Variacional:** Puertas paramétricas $U(\theta)$ que se entrenan.
3. **Medición:** Extracción del resultado (etiqueta o valor de regresión).

## 2. Desafíos del Entrenamiento
- **Barren Plateaus:** El fenómeno donde los gradientes de la función de coste desaparecen exponencialmente con el número de qubits, haciendo imposible el entrenamiento.
- **Retropropagación:** Actualmente usamos gradientes clásicos (Parameter Shift Rule), lo que requiere muchas ejecuciones en la QPU.

## Navegacion
- Anterior: [Kernels cuanticos y espacios de caracteristicas](07_kernels_cuanticos_y_espacios_de_caracteristicas.md)
- Siguiente: [Simulacion de materiales y estructuras complejas](09_simulacion_de_materiales_y_estructuras_complejas.md)
