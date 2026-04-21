# Iones Atrapados y Otras Arquitecturas

Aunque los superconductores son la tecnología más mediática, existen otras plataformas con ventajas competitivas en fidelidad y conectividad.

## Iones Atrapados (Trapped Ions)

Utilizada por empresas como IonQ y Quantinuum. El qubit se almacena en los estados electrónicos internos de un ion (como el $^{171}Yb^+$) atrapado en el vacío mediante campos electromagnéticos (**Trampa de Paul**).

### Ventajas Técnicas:
- **Conectividad:** A diferencia de los superconductores (donde un qubit solo habla con sus vecinos físicos), en una trampa de iones todos los qubits pueden entrelazarse entre sí mediante modos de vibración colectiva (fonones).
- **Tiempos de Coherencia:** El aislamiento del vacío permite tiempos $T_2$ de segundos o incluso minutos, frente a los microsegundos de los transmones.

## Centros NV en Diamante (Nitrogen-Vacancy Centers)

Consisten en un defecto cristalino donde un átomo de nitrógeno sustituye a uno de carbono junto a una vacante. 
- **Computación a temperatura ambiente:** A diferencia de los otros sistemas que requieren criostatos de dilución (mK), los centros NV pueden operar a temperaturas mucho más altas.
- **Aplicación:** Son ideales para sensores cuánticos y repetidores en Internet Cuántico.

## Fotónica sobre Silicio

Utilizada por Xanadu y PsiQuantum. Los qubits son fotones que viajan por guías de onda en un chip.
- **Ventaja:** No sufren casi de decoherencia ambiental y pueden integrarse fácilmente con fibra óptica.
- **Reto:** Las puertas de dos fotones son probabilísticas (no deterministas), lo que requiere técnicas de **Computación Cuántica Basada en la Medición (MBQC)**.

## Tabla Comparativa

| Arquitectura | Qubit Físico | Ventaje | Reto |
|---|---|---|---|
| Superconductores | Corriente Cooper | Rapidez de puerta | Decoherencia / Criogenia |
| Iones Atrapados | Estado Atómico | Conectividad / Fidelidad | Lentitud de puerta |
| Fotónica | Fotón | Telecom / Escalabilidad | Operaciones Probabilísticas |

## Navegación
- Anterior: [Transmones y circuitos superconductores](01_transmones_y_circuitos_superconductores.md)
- Siguiente: [Introducción al control por microondas](../24_control_de_pulsos_y_qiskit_pulse/01_introduccion_al_control_por_microondas.md)
