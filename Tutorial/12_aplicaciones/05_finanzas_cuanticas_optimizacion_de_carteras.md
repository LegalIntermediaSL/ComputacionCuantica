# Finanzas Cuánticas: Optimización de Carteras (Markowitz)

La optimización de carteras es uno de los problemas más icónicos del sector financiero. El objetivo es seleccionar la proporción de activos que maximice el retorno esperado para un nivel de riesgo dado.

## 1. El Modelo de Markowitz
En su forma clásica, queremos minimizar la varianza de la cartera $\sigma_p^2$ sujeta a un retorno objetivo. En computación cuántica, mapeamos esto a un problema binario donde seleccionamos o no un activo $x_i \in \{0, 1\}$.
La función de coste (Hamiltoniano) se escribe como:
$$ H = - \sum_i \mu_i x_i + q \sum_i \sum_j \sigma_{ij} x_i x_j $$
Donde:
- $\mu_i$: Retorno esperado del activo $i$.
- $\sigma_{ij}$: Covarianza entre los activos $i$ y $j$.
- $q$: Parámetro de aversión al riesgo.

## 2. Implementación Cuántica (QAOA/VQE)
Este Hamiltoniano es un problema **QUBO** (Quadratic Unconstrained Binary Optimization). 
1. Convertimos $x_i \to \frac{1-Z_i}{2}$.
2. Obtenemos un Hamiltoniano de Ising.
3. Usamos **VQE** o **QAOA** para encontrar el estado fundamental, que corresponde a la combinación óptima de activos.

## Navegacion
- Anterior: [Simulacion digital y Hamiltonianos sencillos](04_simulacion_digital_y_hamiltonianos_sencillos.md)
- Siguiente: [Valoracion de activos y Monte Carlo cuantico](06_valoracion_de_activos_y_monte_carlo_cuantico.md)
