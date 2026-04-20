# QAOA: Intuición (Quantum Approximate Optimization Algorithm)

## 1. El hermano gemelo logístico del VQE

El VQE fue conceptualizado fundamentalmente atacando simulaciones de química modelando Hamiltonianos de evolución atómica. 
El **QAOA** utiliza idénticamente el mismo bloque de hardware paramétrico "Híbrido Clásico/Cuántica Variacional", pero utiliza sus potencias como ariete absoluto de ataque frente a problemas NP-Hard de **Teoría de Optimización Combinatoria de Grafo Clasico abstracto** (por ej: Enrutamiento logístico TSP, agrupamiento clustering logístico, asimetrías topológicas financieras).

## 2. Resolviendo con el Modelo Abstracto Ising 
A la computadora cuántica abstracta le es profundamente ignorante conceptualizar un "camión semirremolque" o un "nudo o puente carretero". QAOA resuelve un puzzle combinatorio engrasando y abstrayendo una simple traducción estructural de pesos y penalizaciones: 
El coste abstracto de tu red ciudadana de grafos tiene que mapearse a la fuerza hacia un **Hamiltoniano de Coste Diagonal ($H_C$)** emulando un modelo físico magnético en rotaciones en fase cuánticas (Modelo Spin Glasses Abstracto o un Formalismo tipo QUBO Clásico).

## 3. Bucle QAOA y Evoluciones Alternantes

Mientras que VQE arranca instalando un "Ansatz" `EfficientSU2` genérico (Heurística Desnuda) confiando que el iterador hallará la clave asomándose por la colina paramétrica, el protocolo riguroso estipulado para **QAOA nunca elige su arquitectura cuántica al azar, lo prefiere fuertamente estricto**. Está sólidamente y hermosamente emparentado matemáticamente en emular pulsos en la teoría unificada fundacional de la Computación Adiabática Múltiple, lo cual induce a que su "Ansatz" esté orquestado como una receta de dos salsas purificadas que se inyectan intermitentemente a intervalos intercalados.

QAOA genera un pulso entrelazado combinando recursivamente dos influencias rotacionales sobre niveles angulares genéricos globales $\gamma$ (Gamma) y $\beta$ (Beta) en capas (Capas = P):

1. **Pulso de Penalización Magnética Diagonal $e^{-i \gamma H_C}$:** Aplica las lógicas del Grafo a nivel abstracto y castiga conexiones incorrectas. Es accionado modularmente según dictamine la CPU con los sesgos en rotación libre temporal $\gamma$.
2. **Pulsador Intercesor o Mezclador Inercial $e^{-i \beta H_M}$:** Después se agitan sistemáticamente uniformes todos los nodos y su registro emparejado usando compuertas transversales matemáticas unitarias (usualmente operadores $X$ en cascada) orientándolos $\beta$ grados impidiendo estancamientos locales algorítmicos.

Avanzando iteraciones entre Clásica $\to$ QPU actualizando este set bidimensional de parámetros elípticos abstractos logrará revelar el output combinatorialmente más valioso en el medidor físico, entregándonos una aproximación increíble a los puzles intratables NP-Hard lógicos del mundo ordinario en la época moderna de ruido NISQ actual.

## Navegacion

- Anterior: [VQE: intuicion](02_vqe_intuicion.md)
- Siguiente: [Quimica cuantica y simulacion](../12_aplicaciones/01_quimica_cuantica_y_simulacion.md)
