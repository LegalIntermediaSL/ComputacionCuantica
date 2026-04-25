# Glosario

## Observable

Operador hermitico asociado a una cantidad fisica medible. Sus autovalores representan resultados posibles y sus autoestados organizan la estructura de la medida.

## Proyector

Operador que selecciona una componente concreta del espacio de estados. En medicion proyectiva aparece de forma natural en las probabilidades de resultado.

## Valor esperado

Promedio teorico del resultado de muchas mediciones de un observable sobre el mismo estado preparado repetidamente.

## Varianza

Medida de dispersion de los resultados de una medicion respecto al valor esperado.

## Hamiltoniano

Observable que organiza la energia del sistema y gobierna su evolucion temporal.

## Canal cuantico

Transformacion fisicamente valida sobre estados cuanticos, expresada de forma natural sobre matrices de densidad.

## Operadores de Kraus

Conjunto de operadores que permiten escribir un canal cuantico como suma de contribuciones elementales.

## POVM

Medicion generalizada descrita por operadores positivos que suman la identidad, mas amplia que la medicion proyectiva ortogonal.

## Fidelidad

Medida de cercania entre estados o procesos cuanticos. La fidelidad de Bures entre rho y sigma es F = (Tr sqrt(sqrt(rho) sigma sqrt(rho)))^2.

## Tomografia

Proceso de reconstruccion de informacion sobre un estado o un proceso a partir de muchas mediciones en distintas configuraciones.

## Qubit logico

Unidad de informacion protegida mediante codificacion sobre varios qubits fisicos.

## Transpilacion

Proceso de transformar un circuito abstracto en otro compatible con un backend concreto y sus restricciones.

## BQP

Clase de problemas resolubles eficientemente por un computador cuantico con error acotado.

## Oraculo

Caja negra formal usada en muchos algoritmos para modelar acceso estructurado a una funcion.

## Speedup

Mejora en coste computacional frente a un enfoque de referencia, idealmente comparada de forma honesta con el mejor algoritmo clasico conocido.

---

## Coherencia cuantica

Capacidad de un sistema cuantico de mantener superposiciones de estados distinguibles durante un tiempo apreciable. Se puede cuantificar con la medida de coherencia l1 (suma de valores absolutos de las coherencias de la matriz densidad) o con la entropía relativa de coherencia C = S(rho_diag) - S(rho).

## Tiempo de decoherencia T2

Escala de tiempo en la que se pierden las coherencias fuera de la diagonal de la matriz de densidad. Incluye contribuciones de T1 (amortiguamiento de amplitud) y de desfase puro T_phi: 1/T2 = 1/(2T1) + 1/T_phi.

## T1 (amortiguamiento de amplitud)

Tiempo de relajacion de un qubit desde el estado excitado |1> al estado base |0>. Limitado por la perdida de energia al entorno.

## Entrelazamiento

Correlacion cuantica entre subsistemas que no puede describirse como producto de estados individuales. Se cuantifica mediante entropia de entrelazamiento, negatividad o concurrencia.

## Monogamia del entrelazamiento

Restriccion fundamental: si dos qubits estan maximamente entrelazados entre si, ninguno puede estar entrelazado con un tercer sistema. La cota CKW (Coffman-Kundu-Wootters) formaliza este intercambio: tau_AB + tau_AC <= tau_A donde tau es la concurrencia al cuadrado.

## Pureza

Cantidad Tr(rho^2) que vale 1 para estados puros y 1/d para el estado de maxima mezcla en dimension d.

## Entropia de von Neumann

S(rho) = -Tr(rho log rho). Medida del grado de mezcla de un estado cuantico, analogo cuantico de la entropia de Shannon.

## Estado de Bell

Uno de los cuatro estados maximamente entrelazados de dos qubits: Phi+, Phi-, Psi+, Psi-. Base de muchos protocolos de informacion cuantica.

## Teleportacion cuantica

Protocolo que transfiere el estado de un qubit usando un par de Bell compartido y dos bits clasicos de comunicacion, sin transferir materia ni informacion mas rapido que la luz.

## Superdense coding

Protocolo dual a la teleportacion: usa un par de Bell para transmitir 2 bits de informacion clasica enviando solo 1 qubit.

---

## Codigo de repeticion

Codigo de correccion de errores mas simple: codifica 1 qubit logico en 3 fisicos (|0_L> = |000>, |1_L> = |111>) y corrige 1 error de bit-flip por mayoria de votos.

## Codigo de Shor

Primer codigo cuantico completo [[9,1,3]]: concatena tres codigos de repeticion de 3 qubits para proteger contra errores de bit-flip y phase-flip arbitrarios en un qubit.

## Codigo de superficie

Codigo LDPC topologico en rejilla 2D que codifica 1 qubit logico en d^2 fisicos (distancia d). Umbral de error ~1% bajo ruido independiente; preferido para implementaciones hardware por requerir solo acoplamientos locales.

## Sindrome de error

Resultado de medir operadores de estabilizadores que identifica el tipo y ubicacion de un error sin colapsar el estado logico codificado.

## Umbral de corrección (threshold)

Tasa de error fisico por debajo de la cual la concatenacion de codigos reduce el error logico arbitrariamente. Para el codigo de superficie, epsilon_th ~ 1%. Por encima del umbral, anadir mas qubits empeora la situacion.

## MWPM (Minimum Weight Perfect Matching)

Algoritmo de decodificacion para codigos de superficie que empareja sindromes de error con minimo coste, ejecutandose en tiempo O(n^3) clasico o O(n) con algoritmos aproximados.

## Estabilizador

Operador de Pauli que conmuta con todos los elementos del grupo estabilizador y deja invariante el espacio del codigo. La medicion de estabilizadores extrae sindromes sin perturbar el estado logico.

## Magic state distillation

Proceso de purificacion de estados magicos impuros (como |T> = (|0>+e^{i pi/4}|1>)/sqrt(2)) mediante circuitos Clifford para obtener estados de alta fidelidad utilizables en puertas no-Clifford. El protocolo 15->1 distila 15 copias de baja fidelidad en 1 copia de alta fidelidad, a costa de gran overhead de recursos.

## Clifford + T

Conjunto universal de puertas: las puertas de Clifford (H, CNOT, S) son eficientes de simular clasicamente (teorema de Gottesman-Knill), mientras que T = diag(1, e^{i pi/4}) eleva el circuito a universalidad cuantica. Toda puerta unitaria se descompone en Clifford+T.

## Qubit topologico

Qubit cuyo estado logico esta codificado en propiedades topologicas globales del sistema fisico, haciendolo intrinsecamente robusto frente a perturbaciones locales. Propuesto por Kitaev mediante cadenas de Majorana.

## Fermiion de Majorana

Particula que es su propio antiparticula. En materia condensada, cuasiparticulas de Majorana en nanohilos semiconductores pueden formar qubits topologicos con proteccion intrinseca. Microsoft Majorana 1 (2025) demostro su creacion.

## qLDPC (Quantum Low-Density Parity-Check)

Familia de codigos cuanticos cuyos operadores de control involucran un numero constante de qubits, con overhead de recursos asintoticamente mejor que la concatenacion de codigos. Prometedores para implementaciones a gran escala.

---

## VQE (Variational Quantum Eigensolver)

Algoritmo hibrido cuantico-clasico que minimiza el valor esperado de un hamiltoniano variando los parametros de un ansatz. Candidato para simulacion quimica en hardware NISQ.

## QAOA (Quantum Approximate Optimization Algorithm)

Algoritmo variacional para problemas de optimizacion combinatoria. Alterna capas de evolucion bajo el hamiltoniano de coste y el hamiltoniano mixer, con profundidad p ajustable.

## Ansatz

Forma parametrizada de un estado cuantico o circuito cuyo optimo se busca durante la optimizacion variacional.

## Barren plateau

Region plana en el paisaje de optimizacion de circuitos variacionales donde los gradientes son exponencialmente pequenos, dificultando el entrenamiento.

## ZNE (Zero-Noise Extrapolation)

Tecnica de mitigacion de errores que ejecuta el circuito a ruido amplificado (scale factors 1, 2, 3...) y extrapola el resultado a ruido cero. No requiere qubits ancilla adicionales.

## PEC (Probabilistic Error Cancellation)

Metodo de mitigacion de errores que representa el canal ideal como combinacion cuasi-probabilistica de canales ruidosos y promedia con pesos con signo. Tiene overhead exponencial en el numero de puertas.

## Mitigacion de errores cuanticos

Tecnicas que reducen el efecto del ruido en los resultados sin corregirlo a nivel de hardware. Incluye ZNE, PEC, readout correction y symmetry verification.

---

## Quantum Volume (QV)

Benchmark que mide la calidad de un procesador cuantico como la mayor profundidad de circuito cuadrado (n qubits x n capas) ejecutable con exito. QV = 2^n si el circuito aleatorio supera el 2/3 de exito.

## CLOPS (Circuit Layer Operations Per Second)

Metrica de rendimiento que mide cuantas capas de circuito puede ejecutar un procesador por segundo, incluyendo latencia clasica del bucle de control.

## EPLG (Error Per Layered Gate)

Medida del error promedio por puerta de dos qubits en un circuito de capas, mas representativa que la fidelidad individual de puerta.

## Algorithmic Qubit

Metrica propuesta por IonQ: numero de qubits efectivos usables para algoritmos reales, penalizando la fidelidad de puerta. AQ = n_qubits si F_2Q > (2/3)^(1/n).

## Mirror Circuits

Tecnica de benchmarking que aplica un circuito y su inverso para medir el error acumulado directamente comparando entrada y salida sin acceso al estado ideal.

## Cross-Resonance (CR)

Mecanismo de puerta de dos qubits en qubits superconductores: se impulsa el qubit control a la frecuencia del qubit objetivo, induciendo rotaciones condicionales por acoplamiento dispersivo.

## Hamiltoniano dispersivo

Regimen de interaccion entre un qubit transmon y un resonador donde la frecuencia del resonador cambia segun el estado del qubit, sin intercambio de fotones. Permite leer el estado del qubit sin afectarlo directamente.

## Transmon

Tipo de qubit superconductor basado en una union Josephson con gran capacitancia en paralelo que reduce la sensibilidad a ruido de carga. Es el qubit dominante en procesadores de IBM y Google.

## Puerta rzz / Ising ZZ

Puerta de dos qubits RZZ(theta) = exp(-i theta/2 Z⊗Z), base de QAOA. Implementada directamente con pulsos de cross-resonance en superconductores.

---

## ZX-Calculus

Marco grafico para razonar sobre circuitos cuanticos mediante dos tipos de nudos (spiders): verde Z y rojo X, conectados por alambres. Permite simplificar, optimizar y verificar circuitos usando reescritura de grafos.

## Spider (ZX-Calculus)

Nudo en un diagrama ZX que representa una puerta de fase parametrizada actuando sobre multiples alambres. La fusion de spiders del mismo tipo es una regla fundamental del calculo.

## Phase gadget

Patron de circuito compuesto por un CNOT tree seguido de una rotacion Rz, equivalente a una puerta Pauli exponencial. Central en la optimizacion de circuitos variacionales mediante ZX-Calculus.

---

## QKD (Quantum Key Distribution)

Protocolo de distribucion de clave criptografica cuya seguridad esta garantizada por las leyes de la fisica cuantica. BB84 y E91 son los protocolos mas conocidos.

## PQC (Post-Quantum Cryptography)

Criptografia clasica resistente a ataques cuanticos. NIST estandarizo en 2024 CRYSTALS-Kyber (intercambio de clave) y CRYSTALS-Dilithium (firmas digitales).

## Protocolo BB84

Primer protocolo QKD: Alice envia qubits en dos bases conjugadas, Bob mide en base aleatoria; la discordancia entre bases revela escuchas de Eve.

---

## Simulacion de Trotter

Tecnica para aproximar la evolucion temporal unitaria exp(-iHt) de un hamiltoniano con multiples terminos descomponiendo la exponencial en un producto de exponenciales de cada termino. El error de Trotter es O(t^2 delta_t).

## Evolucion cuantica adiabática

Protocolo que evoluciona lentamente un sistema desde el estado fundamental de un hamiltoniano simple hasta el de un hamiltoniano complejo, aprovechando el teorema adiabático para preparar el estado fundamental deseado.

## Kernel cuantico

Funcion de similitud entre datos clasicos calculada mediante el solapamiento de estados cuanticos en un espacio de caracteristicas de alta dimension. Usado en SVM cuantico.

## Quantum Machine Learning (QML)

Area que explora el uso de circuitos cuanticos para aprender y generalizar de datos, ya sean clasicos o cuanticos. Su ventaja practica sobre ML clasico sigue siendo objeto de debate.

## QPE (Quantum Phase Estimation)

Algoritmo que estima la fase de un autovalor de un operador unitario con precision exponencial en el numero de qubits ancilla. Base del algoritmo de Shor y de la simulacion de hamiltonianos.

## HHL (algoritmo de Harrow-Hassidim-Lloyd)

Algoritmo cuantico para resolver sistemas de ecuaciones lineales Ax=b con coste O(log N * kappa^2) frente a O(N) clasico, bajo condiciones especificas de sparsity y acceso QRAM.

## QRAM (Quantum RAM)

Modelo teorico de acceso a datos clasicos en superposicion cuantica. Su implementacion fisica eficiente sigue sin demostrarse; muchos speedups de QML asumen QRAM.

## Dilema NISQ

Tension entre las limitaciones de hardware actual (ruido, pocos qubits, sin QEC) y la necesidad de circuitos profundos para ventaja cuantica significativa.

## Ventaja cuantica

Resolucion de un problema util por un computador cuantico mas rapido que cualquier computador clasico conocido, demostrada de forma rigurosa. Distinta de supremacia cuantica (solo demostracion de capacidad sin utilidad practica).
