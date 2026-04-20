# Indice general del tutorial

Este indice resume la arquitectura actual del proyecto y sirve como punto de entrada alternativo a `Tutorial/README.md`.

## Mapa del recorrido

```mermaid
flowchart TD
    A["00 Fundamentos"] --> B["01 Qubits y medicion"]
    B --> C["02 Puertas y circuitos"]
    C --> D["03 Entrelazamiento"]
    D --> E["04 Qiskit"]
    E --> F["05 Algoritmos"]
    F --> G["06 Ruido y hardware"]
    G --> H["07 Apendices"]
```

## Modulos

### Bloque inicial en articulos

- `01_qubits_y_estados.md`
- `02_superposicion_medicion_y_esfera_de_bloch.md`
- `03_puertas_cuanticas_y_circuitos.md`
- `04_entrelazamiento_y_estados_de_bell.md`

Estos cuatro textos cubren el arranque conceptual del curso sin necesidad de carpetas modulares separadas.

### `04_qiskit/`

Simuladores, estado vector, cuentas, transpilacion y flujo de trabajo practico con Qiskit.

### `05_algoritmos/`

Deutsch-Jozsa, Bernstein-Vazirani, Grover y QFT.

### `06_ruido_y_hardware/`

Decoherencia, fidelidad, mitigacion de errores y paso hacia hardware real.

### `07_apendices/`

Bibliografia comentada, referencias y material de apoyo.

## Cuadernos asociados

La carpeta `../Cuadernos/` se organiza ahora en tres niveles:

- `ejemplos/` para ideas concretas;
- `problemas_resueltos/` para desarrollos guiados;
- `laboratorios/` para exploracion mas abierta.
