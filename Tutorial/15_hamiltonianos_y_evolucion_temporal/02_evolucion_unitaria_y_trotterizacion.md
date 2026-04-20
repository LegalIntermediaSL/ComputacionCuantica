# Evolucion unitaria y Trotterizacion

## 1. Evolucion temporal

La evolución temporal de un sistema cuántico gobernado por un Hamiltoniano $H$ se expresa mediante un operador unitario. Esta es una de las razones profundas por las que la dinámica cuántica y la computación cuántica están tan conectadas.

Si el Hamiltoniano no depende explícitamente del tiempo, la expresión formal es

$$
U(t) = e^{- i H t}.
$$

Aquí aparece una idea decisiva: simular un sistema cuántico equivale, en gran medida, a aproximar esa evolución por un circuito de puertas que podamos implementar.

## 2. Dificultad práctica

Cuando el Hamiltoniano es simple, la evolución puede escribirse de forma manejable. Cuando está formado por varias partes no conmutativas, la implementación directa se vuelve más compleja.

Si escribimos

$$
H = A + B,
$$

el problema es que, en general,

$$
e^{-i(A+B)t} \neq e^{-iAt} e^{-iBt}.
$$

La igualdad solo se cumple de forma directa cuando $A$ y $B$ conmutan. Esa es una de las puertas de entrada naturales a la trotterizacion.

## 3. Idea de Trotterizacion

La trotterización consiste, de forma muy esquemática, en aproximar la evolución total por una composición de evoluciones más simples. Esa idea es una puerta de entrada muy natural a la simulación digital.

En su forma más básica,

$$
e^{-i(A+B)t} \approx \left(e^{-iA t/n} e^{-iB t/n}\right)^n.
$$

Cuando $n$ crece, la aproximación mejora. Pedagógicamente esto es muy valioso porque convierte una evolución complicada en una sucesión de bloques más sencillos.

## 4. Interpretacion computacional

Desde el punto de vista de circuitos, la trotterizacion nos enseña algo muy importante: algunos circuitos no se diseñan “a mano” pensando en una tarea algorítmica abstracta, sino como aproximaciones controladas a un fenómeno físico.

Esta es la lógica que conecta:

- Hamiltonianos;
- simulación digital;
- química cuántica;
- phase estimation;
- algoritmos variacionales;
- y, en general, la idea de usar un computador cuántico para estudiar otro sistema cuántico.

## 5. Coste y precision

La trotterizacion no es gratis. Mejorar la precisión exige normalmente:

- más pasos;
- más puertas;
- más profundidad de circuito;
- y, por tanto, más sensibilidad al ruido.

Eso hace que este tema también conecte con limitaciones prácticas del hardware. No basta con saber que una aproximación existe: hay que preguntarse si es ejecutable con los recursos de un dispositivo realista.

## 6. Valor pedagógico

Este tema ayuda a entender que no todos los circuitos cuánticos nacen como algoritmos “de libro”. Muchos aparecen como aproximaciones controladas a evoluciones físicas.

## 7. Ejercicios sugeridos

1. Explica con tus palabras por qué la no conmutatividad complica la evolución exacta.
2. Considera un Hamiltoniano de la forma $H = Z + X$. Describe por qué la trotterizacion resulta razonable como estrategia.
3. Discute qué trade-off aparece entre precisión y profundidad del circuito.
4. Relaciona esta idea con la promesa de simulación cuántica.

## 8. Material asociado

- Cuaderno: [25_canales_de_ruido_y_kraus.ipynb](../../Cuadernos/ejemplos/25_canales_de_ruido_y_kraus.ipynb)
- Laboratorio: [12_trotterizacion_y_evolucion_guiada.ipynb](../../Cuadernos/laboratorios/12_trotterizacion_y_evolucion_guiada.ipynb)
- Articulo relacionado: [Phase Estimation](../05_algoritmos/05_phase_estimation.md)
- Articulo relacionado: [Simulacion digital y Hamiltonianos sencillos](../12_aplicaciones/04_simulacion_digital_y_hamiltonianos_sencillos.md)

## Navegacion

- Anterior: [Observables y Hamiltonianos](01_observables_y_hamiltonianos.md)
- Siguiente: [Canales cuanticos: intuicion y representacion](../16_canales_cuanticos_y_ruido/01_canales_cuanticos_intuicion_y_representacion.md)
