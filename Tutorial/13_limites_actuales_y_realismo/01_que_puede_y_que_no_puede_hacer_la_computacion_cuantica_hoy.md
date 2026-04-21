# Qué Puede y Qué No Puede Hacer la Computación Cuántica Hoy

## 1. El Espejismo de la Revolución Universal
Existe un clamor general de que QPU sustituirá a la CPU de tu teléfono y tu tarjeta gráfica. La computación cuántica **no acelera mágicamente todo proceso clásico de software**. Para el 99% de tareas humanas (escribir un documento de Word, navegar, compilar C++ o renderizar Minecraft), el entrelazamiento y las compuertas unitarias son una complicación espantosa y estúpida que sería miles de veces más lenta.
La ventaja reside puramente en problemas donde las configuraciones posibles de respuesta estallan exponencialmente, y donde una interferencia constructiva de ondas puede converger asintóticamente a la respuesta global.

## 2. Límites del Entorno Físico (Las Cadenas de NISQ)
¿Por qué VQE o QAOA no desfalcan servidores hoy mismo con 500 qubits? Hoy vivimos atados al **Hardware Ruidoso de Escala Intermedia Limitada**.
Ese ruido que simulaste en laboratorios pasados (T1, T2, Decoherencia), se traga vivos a los chips de hoy. 
Si envías una cadena matemática larga de 50 compuertas CNOT entrelazantes (como requeriría el algoritmo de Shor), las impurezas de Kraus colapsan el cubo, devolviendo una señal $50/50$ idéntica al ruido blanco (White Noise/Depolarization). Estamos atrapados programando algoritmos poco profundos "Shallow-Depth".

## Navegacion

- Anterior: [Criptografía Post-Cuántica (PQC)](../25_criptografia_post_cuantica_pqc/01_criptografia_post_cuantica_pqc.md)
- Siguiente: [Realismo sobre ventaja cuantica](02_realismo_sobre_ventaja_cuantica.md)
