# Mitigación de Errores y Fidelidad

## 1. Mitigar vs Corregir
Mientras esperamos la llegada de la **Corrección de Errores Cuántica (QEC)** —que requiere miles de qubits físicos para proteger uno solo lógico—, utilizamos técnicas de **Mitigación de Errores**. 

- **QEC:** Detecta y corrige errores en tiempo real durante la ejecución (basado en síndromes).
- **Mitigación:** Es una estrategia de post-procesamiento clásico. Ejecutamos el circuito varias veces bajo diferentes condiciones y usamos estadística para "limpiar" el ruido de los resultados finales.

## 2. Técnicas Vanguardistas
Existen varios métodos integrados en herramientas como Qiskit Runtime:

- **Zero Noise Extrapolation (ZNE):** Se ejecuta el circuito con niveles de ruido artificialmente incrementados. Luego, se realiza una extrapolación matemática hacia el punto de "ruido cero".
- **Probabilistic Error Cancellation (PEC):** Modela el ruido del hardware como un canal inverso y aplica operaciones probabilísticas para cancelar sus efectos, a costa de un mayor número de muestras (*shots*).
- **Readout Mitigation (M3):** Calibra los errores sistemáticos del medidor para corregir las probabilidades de observar '0' o '1'.

## 3. Midiendo el Éxito: Fidelidad ($\mathcal{F}$)
Para evaluar cuánto se parece nuestro estado ruidoso $\rho$ al ideal $|\psi\rangle$, usamos la **Fidelidad**:
$$
\mathcal{F}(\rho, |\psi\rangle) = \langle \psi | \rho | \psi \rangle
$$
Una fidelidad de 1.0 indica perfección; valores cercanos a 0.5 sugieren que la señal se ha perdido en el ruido o la despolarización total. En la era NISQ, el objetivo es maximizar esta fidelidad mediante el diseño de pulsos y la optimización de la transpilación.

## Navegacion

- Anterior: [Decoherencia y ruido](01_decoherencia_y_ruido.md)
- Siguiente: [Matrices de densidad y estados mixtos](../08_informacion_cuantica/01_matrices_de_densidad_y_estados_mixtos.md)
