# Circuitos parametrizados y optimización

## 1. Idea general
Hasta ahora, nuestros algoritmos cuánticos solían consistir en secuencias estáticas de puertas lógicas: sabíamos de antemano el circuito $H \to CNOT \to ...$. Un **circuito parametrizado** rompe este esquema. Ya no define todas sus transformaciones desde el principio, sino que deja ciertos ángulos rotacionales libres representados como variables continuas (generalmente llamadas $\theta$).

Un circuito parametrizado matemático se denota rutinariamente como $U(\vec{\theta})$. Su ejecución no genera un único estado final, sino una familia continua de estados según se ajusten los parámetros. El circuito funciona a modo de plantilla (ansatz).

## 2. Por qué esta capa importa en la revolución cuántica actual

La invención de los circuitos parametrizados ha marcado el inicio de la era que llamamos **NISQ (Noisy Intermediate-Scale Quantum)**.
Las máquinas modernas son ruidosas y sus tiempos de coherencia impiden ejecutar algoritmos determinísticos inmensamente largos como Shor. Los circuitos parametrizados resuelven esto al ser cortos ("shallow") pero flexibles. 

En vez de programar una super-secuencia lógica inmutable, se levanta una estructura "moldeable" corta, y se le delega el trabajo pesado a una CPU clásica iterativa.

## 3. El Bucle Híbrido Cuántico-Clásico

Dado un circuito parametrizado, la manera de sacarle partido sigue casi invariablemente este bucle híbrido:

1. **Elegir parámetros (Clásico):** Un optimizador en tu CPU inicializa el vector $\vec{\theta}$ libremente.
2. **Preparar y Evaluar (Cuántica):** Qiskit inyecta el vector en el hardware, corre el circuito formando el estado abstracto $|\psi(\vec{\theta})\rangle$, y extrae un Valor Esperado (`Estimator`) sobre una ecuación Costo/Métrica (el Observable).
3. **Optimizar (Clásico):** El ordenador clásico lee la Métrica que arrojó la QPU. Como si de Machine Learning se tratara, actualiza el vector a $\vec{\theta}_{new}$ avanzando un poco en la pendiente usando gradiente descendiente (ej. SPSA o COBYLA).
4. **Repetir:** Refinamiento progresivo hasta que la métrica (la energía) alcance su mínimo teórico.

Este mecanismo distribuye brillantemente el esfuerzo: la máquina clásica hace la matemática estadística de optimización, y la cuántica solo hace lo que la clásica no puede simular: evaluar estados que podrían esconder un entrelazamiento monstruosamente complejo.

## Navegacion

- Anterior: [Noise models y simulacion realista](../10_qiskit_avanzado/03_noise_models_y_simulacion_realista.md)
- Siguiente: [VQE: intuicion](02_vqe_intuicion.md)
