# Qiskit Runtime y Primitives: La Capa de Ejecución Moderna

## 1. Evolución del Modelo de Ejecución
En los inicios de Qiskit, el flujo de trabajo era simple: diseñar un circuito y enviarlo a un backend mediante `execute(circuit, backend)`. Sin embargo, a medida que los algoritmos se volvieron más complejos (especialmente los variacionales como VQE), la latencia entre el ordenador clásico y el chip cuántico se convirtió en un cuello de botella. 

**Qiskit Runtime** resuelve esto permitiendo que programas completos se ejecuten "cerca" del hardware, optimizando las iteraciones y gestionando los recursos de forma asíncrona.

## 2. Las Primitivas: Sampler y Estimator
Las primitivas son interfaces de alto nivel que abstraen la complejidad del hardware ruidoso y proporcionan resultados procesados. Existen dos tipos fundamentales (actualmente en su versión **V2**):

- **Sampler:** Diseñado para algoritmos que generan distribuciones de probabilidad (como Grover o búsqueda de cadenas). Devuelve cuasiprobabilidades de las cadenas de bits resultantes tras la medición. Su salida es una estimación de la distribución de estados finales.
- **Estimator:** Optimizado para calcular valores esperados de observables. En lugar de devolver bits individuales, calcula $\langle \psi | H | \psi \rangle$ para un Hamiltoniano $H$. Es la herramienta esencial para química cuántica y algoritmos variacionales, ya que incorpora técnicas internas de mitigación de errores.

## 3. Ventajas de las Primitives V2
La arquitectura V2 introducida recientemente permite un control mucho más granular sobre la ejecución:
- **Precision (Exactitud):** Puedes definir el nivel de precisión deseado, y la primitiva ajustará automáticamente el número de *shots* y las técnicas de mitigación necesarias.
- **Pubs (Primitive Unified Blocs):** Permite enviar múltiples combinaciones de circuitos, observables y parámetros en un solo "trabajo" (*job*), reduciendo drásticamente los tiempos de espera y comunicación.

## 4. Por qué usarlas hoy
Utilizar primitivas no es solo una cuestión de "comodidad". Es el estándar de la industria para trabajar con computadoras cuánticas reales. Al usar un `Estimator`, Qiskit Runtime aplica automáticamente correcciones de post-procesamiento que un `execute()` básico ignoraría, permitiendo que tus resultados sean mucho más precisos frente al ruido ambiental.

## Navegacion

- Anterior: [Qiskit: transpilacion, ruido y paso hacia hardware](../02_qiskit_basico/09_qiskit_transpilacion_ruido_y_hardware.md)
- Siguiente: [Deutsch-Jozsa](../05_algoritmos/01_deutsch_jozsa.md)
