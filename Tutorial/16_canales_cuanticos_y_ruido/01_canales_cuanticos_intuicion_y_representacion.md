# Canales Cuánticos y Matrices Densidad Impuras

## 1. Perdiendo pureza

Hasta llegar al conocimiento avanzado, la mayoría de libros enseñan la física de qubits aislados asumiendo inocentemente transformaciones rígidamente Unitarias Puras $\rho_{new} = U \rho U^{\dagger}$. 
Aquí entra el balde de agua helada y sucia para el físico aplicado: El estado nunca fluye de forma cerrada aisladamente, siempre sufre injerencias asimétricas abstractamente entrópicas irreversibles perdiendo memoria de amplitud hacia el mundo externo clásico ruidoso.

Para lidiar formalmente con transformaciones imperfectas no unitarias puras, interponemos los denominados **Canales Cuánticos Abstractos $\mathcal{E}$**.  
Una manera intuitiva unificada y profunda de estudiar matemática y estadísticamente el Canal General que asfixia al qubit es valerse puramente matricialmente bajo el formalismo sumatorio C.P.T.P. "Mapas completamente positivos trazivos"  o lo que hoy denominas simplemente usando **Los operadores asimétricos discretos subyacentes de Kraus**.

## 2. Despliegue de Ruido vía Operadores Formadores Kraus
Un canal de ruido $\mathcal{E}(\rho)$ se compila matemáticamente separando cada error posible discreto subyacente asignándole matrices independientes $\{K_i\}$, forzando y garantizando que la probabilidad absoluta de sumatorias combinatorias sean 1 ($\sum K_i^\dagger K_i = I$).

El estado sufre la evolución ruidosa asimétricamente sumando combinando todas las ramas:
$$ \mathcal{E}(\rho) = K_0 \rho K_0^{\dagger} + K_1 \rho K_1^{\dagger} + \dots $$
Donde $K_0$ podría significar "que no ocurriera accidente termodinámico", y $K_1$ el salto indeseado "Bit-Flip cruzado de rayos cósmicos". 

## Navegacion

- Anterior: [Evolucion unitaria y Trotterizacion](../15_hamiltonianos_y_evolucion_temporal/02_evolucion_unitaria_y_trotterizacion.md)
- Siguiente: [Operadores de Kraus, decoherencia y modelos efectivos](02_kraus_decoherencia_y_modelos_efectivos.md)
