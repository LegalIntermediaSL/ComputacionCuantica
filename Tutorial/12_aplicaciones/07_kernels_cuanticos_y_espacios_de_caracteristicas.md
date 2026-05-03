# Kernels Cuánticos y Espacios de Características

En Machine Learning, el **truco del Kernel** permite proyectar datos a un espacio de dimensiones superiores donde sean linealmente separables. Las computadoras cuánticas pueden hacer esto de forma natural.

## 1. Quantum Feature Maps
Un mapa de características cuántico $\phi(x)$ mapea un dato clásico $x$ a un estado cuántico $|\phi(x)\rangle$. El producto escalar en este espacio es el **Quantum Kernel**:
$$
K(x, y) = |\langle \phi(x) | \phi(y) \rangle|^2
$$

## 2. El Teorema de Representación
Si la estructura de los datos es suficientemente compleja (ej: datos correlacionados con patrones "cuánticos"), una computadora clásica no puede calcular este Kernel de forma eficiente, mientras que una QPU puede estimarlo midiendo la fidelidad entre estados.

## Navegacion
- Anterior: [Valoracion de activos y Monte Carlo cuantico](06_valoracion_de_activos_y_monte_carlo_cuantico.md)
- Siguiente: [Redes neuronales cuanticas qnn](08_redes_neuronales_cuanticas_qnn.md)
