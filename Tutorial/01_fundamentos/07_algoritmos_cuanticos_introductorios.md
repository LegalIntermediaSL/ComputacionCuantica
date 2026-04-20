# Algoritmos Cuánticos: La Intuición del Paralelismo de Fase

## 1. ¿Qué es un Algoritmo Cuántico?
No es simplemente "hacer muchas cosas a la vez". Un algoritmo cuántico es una coreografía de **interferencias destructivas y constructivas**. El objetivo es que las amplitudes de probabilidad de los resultados incorrectos se anulen entre sí, mientras que la del resultado correcto se refuerce antes de la medición.

## 2. La Estructura de "Sándwich"
Casi todos los algoritmos cuánticos siguen un patrón similar:
1. **Inicialización:** Todos los qubits a $|0\rangle$.
2. **Superposición Uniforme:** Una capa de puertas Hadamard ($H$) para explorar todas las posibilidades.
3. **Oráculo / Transformación:** Una operación controlada que marca o modifica los estados de interés basándose en el problema.
4. **Interferencia / Amplificación:** Una subrutina (como la Difusión en Grover o la QFT) para concentrar la probabilidad.
5. **Medición:** Colapso del sistema para extraer la respuesta clásica.

## 3. Ventaja Exponencial vs Cuadrática
- **Algoritmos Estructurales (Shor, Phase Estimation):** Explotan la estructura matemática periódica del problema para obtener una ventaja exponencial.
- **Algoritmos de Búsqueda (Grover):** No requieren estructura previa y ofrecen una ventaja cuadrática universal.

Entender esta distinción es clave para evaluar qué problemas pueden beneficiarse realmente de la computación cuántica y cuáles seguirán siendo dominio de los superordenadores clásicos.

## Navegacion

- Anterior: [Algebra lineal minima para computacion cuantica](06_algebra_lineal_minima_para_computacion_cuantica.md)
- Siguiente: [Qiskit: simuladores, estado cuantico y resultados](../02_qiskit_basico/08_qiskit_simuladores_estado_y_resultados.md)
