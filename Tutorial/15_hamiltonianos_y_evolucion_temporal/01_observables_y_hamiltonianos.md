# Observables y Hamiltonianos

## 1. Observables

Un observable es una cantidad física asociada a un operador hermítico. En computación cuántica, esta capa se vuelve especialmente importante cuando pasamos de medir bits a estimar valores esperados, correlaciones o energías.

En una primera aproximacion, medir un qubit parecia equivalente a preguntar si el resultado era `0` o `1`. Pero esa imagen es demasiado estrecha para casi todo lo que viene despues. Muy pronto necesitamos pensar en operadores como:

$$
X = \begin{pmatrix}
0 & 1 \\
1 & 0
\end{pmatrix},
\qquad
Z = \begin{pmatrix}
1 & 0 \\
0 & -1
\end{pmatrix},
$$

porque son ellos los que representan cantidades fisicas, bases de medida y observables efectivos.

## 2. Hamiltoniano

El Hamiltoniano es el observable que gobierna la dinámica temporal del sistema. Además, en muchos problemas de simulación y algoritmos variacionales, el Hamiltoniano es la cantidad central cuya estructura queremos explotar.

En lenguaje fisico, el Hamiltoniano cumple dos papeles a la vez:

- dice cual es la energia asociada a cada configuracion;
- determina como cambia el estado con el tiempo.

Ese doble papel es una de las razones por las que aparece una y otra vez en computacion cuantica aplicada.

## 3. Valores esperados

Si el sistema esta en un estado $|\psi\rangle$ y el observable es $A$, el valor esperado se escribe como

$$
\langle A \rangle = \langle \psi | A | \psi \rangle.
$$

Esta expresion condensa una intuicion muy importante: no siempre queremos una muestra individual de medicion, sino una cantidad promedio asociada al estado. En VQE, por ejemplo, lo que buscamos minimizar no es un bit suelto, sino una energia esperada

$$
E(\theta) = \langle \psi(\theta) | H | \psi(\theta) \rangle.
$$

Eso ya conecta de forma directa con observables, Hamiltonianos y optimizacion.

## 4. Descomposicion en Paulis

En practica, muchos Hamiltonianos usados en computacion cuantica se escriben como combinaciones lineales de operadores de Pauli:

$$
H = c_0 I + c_1 X + c_2 Y + c_3 Z
$$

para un qubit, o bien como sumas de cadenas de Paulis en varios qubits:

$$
H = \sum_j c_j P_j,
$$

donde cada $P_j$ es un producto tensorial de matrices de Pauli.

Esta forma es muy util porque:

- se adapta bien a la representacion computacional;
- enlaza con `SparsePauliOp`;
- permite estimar observables por bloques;
- hace mas natural la conexion con algoritmos variacionales.

## 5. Relacion con Qiskit

En Qiskit esta capa se conecta muy bien con:

- `SparsePauliOp`;
- `Estimator`;
- VQE;
- simulación de sistemas sencillos.

Una de las ideas mas pedagogicas del ecosistema actual es precisamente esta: un circuito no es solo una secuencia abstracta de puertas; puede ser tambien una herramienta para estimar propiedades de un Hamiltoniano.

## 6. Por que este bloque es importante

Sin observables, el tutorial se quedaria demasiado cerca de la intuicion de “circuitos que producen bits”. Sin Hamiltonianos, se perderia el puente hacia:

- simulacion cuantica;
- quimica cuantica;
- VQE;
- evolucion temporal;
- estimacion de propiedades fisicas.

Por eso este modulo no es un apendice tecnico, sino una capa que reorganiza buena parte del curso.

## 7. Valor dentro del curso

Este tema actúa como puente entre fundamentos, algoritmos y aplicaciones. Sin Hamiltonianos, la conexión con simulación cuántica y química cuántica queda demasiado débil.

## 8. Ejercicios sugeridos

1. Escribe el valor esperado de $Z$ para los estados $|0\rangle$, $|1\rangle$ y $|+\rangle$.
2. Comprueba que una matriz hermitica tiene autovalores reales en los ejemplos sencillos de $X$, $Y$ y $Z$.
3. Considera el Hamiltoniano $H = Z_1 Z_2$. Describe intuitivamente que configuraciones favorece energeticamente.
4. Explica por que minimizar $\langle H \rangle$ tiene sentido en un algoritmo variacional.

## 9. Material asociado

- Cuaderno: [24_observables_y_valores_esperados.ipynb](../../Cuadernos/ejemplos/24_observables_y_valores_esperados.ipynb)
- Cuaderno: [21_qiskit_sparsepauliop_basico.ipynb](../../Cuadernos/ejemplos/21_qiskit_sparsepauliop_basico.ipynb)
- Laboratorio: [08_vqe_intuicion_guiada.ipynb](../../Cuadernos/laboratorios/08_vqe_intuicion_guiada.ipynb)
- Articulo relacionado: [Simulacion digital y Hamiltonianos sencillos](../12_aplicaciones/04_simulacion_digital_y_hamiltonianos_sencillos.md)

## Navegacion

- Anterior: [Simulacion digital y Hamiltonianos sencillos](../12_aplicaciones/04_simulacion_digital_y_hamiltonianos_sencillos.md)
- Siguiente: [Evolucion unitaria y Trotterizacion](02_evolucion_unitaria_y_trotterizacion.md)
