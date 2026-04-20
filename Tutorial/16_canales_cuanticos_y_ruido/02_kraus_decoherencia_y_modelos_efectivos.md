# Modelos Efectivos Fundamentales de Ruido Físico

## 1. Analizando a tus enemigos termodinámicos

Desmenuzando la técnica asimétrica explicada (Kraus Operators), los físicos formaron arquitecturas puras de los "peores enemigos" típicos para programar los NoiseModels en simuladores de base (como Qiskit Aer).

- **El canal de Bit-Flip Lógico y Phase-Flip ($T_2$ Decoherence)**: 
  Simula esporádicos castigos booleanos estadísticos aleatorizados empíricamente sobre el Estado de Bloch. (Es lo que castigaba tu "Circuito Entrelazador Parity" resuelto llanamente en las clases de Código Repetidor Tempranas del temario).
- **El canal de Depolarización Termodinámica Pura (White Noise)**:
  La bomba letal experimental absoluta que contrae catastróficamente toda la esfera orbital estática de un Qubit simétricamente de colapso esférico hacia el origen negro neutral (Matrix mezclada máxima $I/2$). Significa que una computadora se asfixiaba olvidando la amnesia física computacional de lo simulado, derivando un tensor de ruleta rusa pura donde no existe señal en el Measurement. 
- **Canal de Amplitude Damping Asimétrica ($T_1$ Relaxation):**
  Un qubit sobre $|1\rangle$ (estado con altísima excitación cuántica energética de carga inestable) gotea calor gravitacional y energético espontáneamente decantando su onda perdiendo excitación hacia $|0\rangle$, de manera probabilística temporal, soltando el remanente en forma de radiaciones u ondas al ambiente térmico externo subyacente.

Con estas herramientas Kraus y simuladores NoiseModel emparejados, desarrollamos el framework híbrido analítico que servirá fundamentalmente de sostén algorítmico al Mitigation y Surface Codes.

## Navegacion

- Anterior: [Canales cuanticos: intuicion y representacion](01_canales_cuanticos_intuicion_y_representacion.md)
- Siguiente: [Proyectores, valores esperados y varianza](../17_medicion_avanzada_y_observables/01_proyectores_valores_esperados_y_varianza.md)
