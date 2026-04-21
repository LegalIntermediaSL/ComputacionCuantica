# Protocolos de Internet Cuántico

Si una computadora cuántica es potente, una red de computadoras cuánticas entrelazadas es el siguiente salto tecnológico. Esto es lo que llamamos el **Internet Cuántico**.

## Gestión de Claves (QKD)

El primer uso práctico ha sido la **Distribución Cuántica de Claves**.
- **Protocolo BB84:** Utiliza fotones en diferentes bases para detectar espías (gracias al teorema de no-clonación).
- **Protocolo E91:** Utiliza pares de Bell entrelazados. La seguridad se verifica mediante la desigualdad de Bell (CHSH). Si hay un espía, la violación de la desigualdad disminuye.

## El Desafío de la Distancia

A diferencia de los bits clásicos, los qubits no pueden amplificarse (de nuevo, por el teorema de no-clonación). En una fibra óptica, un fotón se pierde tras unos 100 km. Esto limita las comunicaciones cuánticas directas.

## Arquitectura de Capas
Como el modelo OSI clásico, el Internet Cuántico requiere:
1. **Capa Física:** Generación de fotones y fibras.
2. **Capa de Enlace:** Generación de entrelazamiento entre nodos vecinos.
3. **Capa de Red:** Enrutamiento de entrelazamiento a larga distancia.

## Navegación
- Anterior: [Simplificación y optimización de circuitos](../26_calculo_grafico_y_zx_calculus/02_simplificacion_y_optimizacion_de_circuitos.md)
- Siguiente: [Repetidores y redes de entrelazamiento](02_repetidores_y_entanglement_swapping.md)
