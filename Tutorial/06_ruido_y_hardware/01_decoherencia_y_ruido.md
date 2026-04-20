# Decoherencia y Ruido: Los Enemigos del Qubit

## 1. El Entorno como Observador
Un sistema cuántico ideal es una abstracción matemática. En la realidad, un qubit está en contacto constante con su entorno (campos magnéticos, fluctuaciones térmicas, radiación). Este contacto actúa como una "medición no deseada" que extrae información del sistema, provocando el colapso de la superposición. A este proceso lo llamamos **Decoherencia**.

## 2. Tipos Fundamentales de Error
En el hardware actual (NISQ), nos enfrentamos principalmente a tres tipos de degradación:

- **Relajación Térmica ($T_1$):** Es la pérdida de energía del qubit, que tiende a decaer de $|1\rangle$ a $|0\rangle$. Es un error asimétrico y longitudinal. Limita el tiempo máximo que podemos mantener la información antes de que se "enfríe".
- **Desfase ($T_2$):** Es la pérdida de la relación de fase entre $|0\rangle$ y $|1\rangle$. No hay pérdida de energía, pero la información sobre la superposición (el ángulo en el ecuador de la esfera de Bloch) se distorsiona. Suele ser mucho más rápido que $T_1$.
- **Errores de Puerta y Lectura:** Las operaciones físicas (pulsos de microondas) no son perfectas. Una puerta X puede rotar $179.9^\circ$ en lugar de $180^\circ$, acumulando errores sistemáticos conocidos como "gate fidelity" insuficiente.

## 3. Impacto en la Computación
El ruido limita la **profundidad** de los circuitos. Si un algoritmo requiere 1000 puertas pero el ruido corrompe el estado tras 50, el resultado final será indistinguible del azar. Entender y modelar este ruido es el primer paso para poder combatirlo mediante la corrección de errores topológica.

## Navegacion

- Anterior: [Phase Estimation](../05_algoritmos/05_phase_estimation.md)
- Siguiente: [Mitigacion de errores y fidelidad](02_mitigacion_errores_y_fidelidad.md)
