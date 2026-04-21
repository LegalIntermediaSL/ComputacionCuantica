# Repetidores y Entanglement Swapping

Para conectar dos ciudades que están a 1000 km, necesitamos **Repetidores Cuánticos**. Como no podemos copiar el qubit, debemos "teleportarlo" por tramos.

## Entanglement Swapping (Intercambio de Entrelazamiento)

Es la técnica clave. Supongamos que Alice tiene un par entrelazado con un Repetidor (A-R), y el Repetidor tiene otro par con Bob (R-B).
1. El Repetidor realiza una **medición de base de Bell** sobre sus dos qubits (el que comparte con Alice y el que comparte con Bob).
2. Automáticamente, los qubits de Alice y Bob quedan entrelazados, ¡aunque nunca hayan estado en contacto físico!.

Esto permite extender el entrelazamiento a distancias arbitrarias uniendo tramos cortos.

## Purificación de Entrelazamiento (Distillation)

Debido al ruido en las fibras, el entrelazamiento se degrada. La **purificación** permite tomar varios pares de Bell "de baja calidad" (ruidosos) y procesarlos para obtener un solo par de "alta calidad" (casi puro).

## El Futuro: Computación Cuántica en la Nube Ciega

Una red cuántica permitiría el **Blind Quantum Computing**: un cliente envía cálculos cifrados a un servidor cuántico potente, y el servidor los ejecuta sin saber qué está calculando ni cuáles son los resultados. Privacidad física absoluta.

## Navegación
- Anterior: [Protocolos de Internet Cuántico](01_redes_y_protocolos_de_entrelazamiento.md)
- Siguiente: [Qué puede y que no puede hacer la computación cuántica hoy](../../13_limites_actuales_y_realismo/01_que_puede_y_que_no_puede_hacer_la_computacion_cuantica_hoy.md)
