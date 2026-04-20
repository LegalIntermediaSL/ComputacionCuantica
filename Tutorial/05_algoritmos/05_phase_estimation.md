# Quantum Phase Estimation (QPE)

## 1. El Problema del Autovalor
Muchos problemas en física y matemáticas se reducen a encontrar el autovalor de una matriz unitaria $U$. Si tenemos un autovector $|u\rangle$ tal que:
$$ U|u\rangle = e^{2\pi i \phi} |u\rangle $$
el objetivo de QPE es estimar la fase $\phi \in [0, 1)$. 

## 2. El Protocolo Algorítmico
QPE utiliza dos registros de qubits:
1. **Registro de Conteo ($n$ qubits):** Determina la precisión de la estimación. Tras el algoritmo, contendrá la representación binaria de $\phi$.
2. **Registro del Estado ($m$ qubits):** Almacena el autovector $|u\rangle$.

El proceso sigue tres fases críticas:
- **Hadamards y Evolución Controlada:** Se aplican puertas $U^{2^k}$ controladas por los qubits del registro de conteo. Esto codifica la fase de forma iterativa y binaria en las amplitudes del primer registro.
- **QFT Inversa:** Traslada la información de las fases a la base computacional para que sea medible.
- **Medición:** Obtenemos una cadena de bits que representa la mejor aproximación de $n$ bits de $\phi$.

## 3. Importancia y Precisión
La precisión del algoritmo depende linealmente del número de qubits en el registro de conteo. Con $n$ qubits, podemos estimar $\phi$ con un error menor a $1/2^n$ con alta probabilidad. QPE es la subrutina central de:
- **Algoritmo de Shor:** Para encontrar el periodo de una función.
- **Química Cuántica:** Para encontrar la energía del estado fundamental (Hamiltonianos).
- **HHL:** Para resolver sistemas de ecuaciones lineales.

## Navegacion

- Anterior: [Transformada cuantica de Fourier](04_transformada_cuantica_de_fourier.md)
- Siguiente: [Decoherencia y ruido](../06_ruido_y_hardware/01_decoherencia_y_ruido.md)
