# Valoración de Activos y Monte Carlo Cuántico (QAE)

Calcular el precio de derivados financieros (como las opciones) requiere simular miles de trayectorias posibles de precios. Clásicamente se usa Monte Carlo, cuya convergencia es lenta ($1/\sqrt{N}$).

## 1. De Monte Carlo a QAE
La **Estimación de Amplitud Cuántica (QAE)** proporciona una aceleración cuadrática, logrando una convergencia de $1/N$.
El proceso sigue estos pasos:
1. **Carga de Probabilidad:** Codificamos la distribución de precios en un estado cuántico $|\psi\rangle = \sum \sqrt{p_i} |i\rangle$.
2. **Cálculo del Payoff:** Aplicamos un operador que calcula el valor del derivado $f(i)$ y lo almacena en la amplitud de un qubit ancila.
3. **QAE:** Usamos el algoritmo de estimación de fase para "leer" esa amplitud, que representa el precio justo del activo.

## 2. Aplicaciones en Gestión de Riesgos
- **Value-at-Risk (VaR):** Calcular la pérdida máxima probable en un escenario de mercado.
- **Credit Risk:** Evaluar la probabilidad de impago en carteras de crédito complejas.

## Navegacion
- Anterior: [Finanzas cuanticas optimizacion de carteras](05_finanzas_cuanticas_optimizacion_de_carteras.md)
- Siguiente: [Kernels cuanticos y espacios de caracteristicas](07_kernels_cuanticos_y_espacios_de_caracteristicas.md)
