# Computación tolerante a fallos: el horizonte

## 1. Qué significa tolerancia a fallos

Un sistema de computación cuántica es **tolerante a fallos** (fault-tolerant) si puede ejecutar circuitos lógicos arbitrariamente largos con tasa de error lógica arbitrariamente pequeña, siempre que la tasa de error física por puerta esté por debajo de un umbral.

La tolerancia a fallos no es simplemente corrección de errores: requiere que cada operación sobre los qubits lógicos se realice de forma que los errores no se amplifiquen durante el proceso de corrección. Un código corrector puede corregir errores, pero si la operación correctora introduce errores adicionales, el sistema puede no mejorar.

La **condición de tolerancia a fallos** (fault-tolerant condition) exige que cada puerta lógica esté diseñada para propagar como máximo $t$ errores físicos a $t$ errores en qubits de datos distintos, donde $t = \lfloor (d-1)/2 \rfloor$ es la capacidad de corrección del código.

## 2. El overhead de la tolerancia a fallos

El coste de la tolerancia a fallos es alto. Para un qubit lógico de distancia $d$ en un surface code:

- **Qubits físicos por qubit lógico:** $\sim 2d^2$ (datos + ancillas).
- **Tiempo por ciclo de corrección:** $\sim d$ ciclos de puerta.
- **Overhead total** para tasa de error lógica $p_L$:

$$
N_\text{físico} \approx 2d^2, \quad d \approx O\left(\log\frac{1}{p_L}\right) \text{ cuando } p \ll p_\text{th}
$$

Para los algoritmos más relevantes:

| Aplicación | Qubits lógicos | Distancia necesaria | Qubits físicos totales |
|---|---|---|---|
| Factor. RSA-2048 (Shor) | ~4000 | ~17 | ~4 millones |
| Simulación FeMoco (Hamiltoniano) | ~1000 | ~13 | ~0.5 millones |
| Grover sobre AES-128 | ~3000 | ~15 | ~2 millones |

Estos números asumen tasas de error físico de $\sim 0.1\%$. Con $p = 0.01\%$ (estado del arte futuro), la distancia necesaria se reduce aproximadamente a la mitad.

## 3. El conjunto de puertas tolerante a fallos: Clifford + T

La teoría de tolerancia a fallos distingue dos tipos de puertas:

**Puertas del grupo de Clifford** ($H, S, CNOT$): se implementan de forma transversal en el surface code, lo que garantiza automáticamente la tolerancia a fallos. Son eficientes pero no suficientes para computación universal.

**Puerta T** ($T = \text{diag}(1, e^{i\pi/4})$): no tiene implementación transversal en el surface code. Requiere **magic state distillation**.

La **destilación de estados mágicos** funciona así:
1. Preparar muchas copias ruidosas del estado $|T\rangle = (|0\rangle + e^{i\pi/4}|1\rangle)/\sqrt{2}$.
2. Aplicar un protocolo de destilación que usa $n$ copias ruidosas para producir $k < n$ copias de alta fidelidad.
3. Usar los estados purificados para implementar la puerta $T$ lógica mediante teleportación de puerta.

El overhead de la destilación de estados mágicos es enorme: para obtener un estado $|T\rangle$ con infidelidad $\epsilon$, se necesitan $O(\log^3(1/\epsilon))$ fábricas de destilación, cada una con $\sim 1000$ qubits físicos.

## 4. El horizonte temporal

Los principales grupos de investigación tienen hojas de ruta explícitas:

**Google:** objetivo de demostrar corrección de errores útil con un qubit lógico de distancia 11+ para 2025-2026. El sistema Willow (2024) mostró corrección de errores por debajo del umbral.

**IBM:** objetivo de 100.000 qubits físicos con corrección de errores para 2033, suficientes para problemas de química relevantes.

**Microsoft:** apuesta por qubits topológicos (basados en anyones de Majorana) con umbrales de error más altos de forma nativa, reduciendo el overhead de corrección.

Los principales cuellos de botella técnicos son:
- **Conectividad 3D de qubits:** las fábricas de destilación requieren interconexiones más densas que las retículas 2D actuales.
- **Velocidad de las operaciones:** el ciclo de corrección debe ser más rápido que $T_1$.
- **Cableado criogénico:** controlar $10^6$ qubits requiere una infraestructura criogénica inédita.

## 5. Computación cuántica tolerante a fallos como problema de ingeniería

La tolerancia a fallos cuántica es hoy un problema fundamentalmente de ingeniería, no de principios. Los ingredientes teóricos están establecidos desde los años 1990 (Shor, Steane, Knill-Laflamme-Zurek). El reto es la realización física:

- Qubits con tasa de error $< 0.1\%$ de forma consistente y a escala.
- Decodificadores clásicos en tiempo real capaces de procesar $10^6$ síndromes por segundo.
- Arquitecturas de interconexión que permitan las puertas lógicas entre qubits arbitrarios.

## 6. Ideas clave

- La tolerancia a fallos requiere que los errores no se amplifiquen durante las operaciones correctoras.
- El surface code necesita $\sim 2d^2$ qubits físicos por qubit lógico; para aplicaciones útiles (Shor sobre RSA-2048) esto implica millones de qubits.
- Las puertas Clifford son tolerantes a fallos de forma nativa; la puerta $T$ requiere destilación de estados mágicos con un overhead enorme.
- La distancia necesaria decrece si la tasa de error física mejora.
- El problema es fundamentalmente de ingeniería: los principios están establecidos, la realización física no.

## 7. Ejercicios sugeridos

1. Calcular el número de qubits físicos necesarios para un qubit lógico $d = 5, 7, 9$ asumiendo $\sim 2d^2$ qubits.
2. Estimar la tasa de error lógica de un surface code $d = 7$ si la tasa física es $p = 0.3\%$ y $p_\text{th} = 1\%$.
3. Explicar por qué la puerta $T$ no tiene implementación transversal en el surface code pero $H$ y $CNOT$ sí.
4. Buscar el artículo de Google sobre el experimento Willow (2024) y resumir el avance demostrado.

## Navegacion

- Anterior: [Surface codes: intuicion](01_surface_codes_intuicion.md)
- Siguiente: [Sampler, Estimator y primitives](../10_qiskit_avanzado/01_sampler_estimator_y_primitives.md)
