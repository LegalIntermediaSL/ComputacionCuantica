# Guía Práctica: Strawberry Fields y Computación Fotónica

> **Nota:** Esta guía es el complemento práctico del Módulo 45 (`Tutorial/45_computacion_fotonica/README.md`) y del laboratorio `Cuadernos/laboratorios/49_fotonica_cuantica.ipynb`. La teoría (modos gaussianos, squeezed states, GBS) se cubre allí; aquí el foco es instalación, API y ejecución local.

---

## Instalación

```bash
pip install strawberryfields
```

Dependencias recomendadas para funcionalidad completa:

```bash
# Hafnian (cálculo de permanentes, requerido para GBS con backend Fock)
pip install thewalrus

# Plugin PennyLane para circuitos híbridos
pip install pennylane-sf
```

Versión mínima recomendada: `strawberryfields >= 0.23`.

---

## Verificar la instalación

Ejecutar el siguiente circuito mínimo de 2 modos confirma que la instalación funciona correctamente:

```python
import strawberryfields as sf
from strawberryfields.ops import Sgate, BSgate, MeasureHomodyne

prog = sf.Program(2)
with prog.context as q:
    Sgate(0.8) | q[0]          # squeezing modo 0
    Sgate(0.8) | q[1]          # squeezing modo 1
    BSgate(0.5, 0.0) | (q[0], q[1])   # beamsplitter 50/50
    MeasureHomodyne(0) | q[0]  # medición homodina en x
    MeasureHomodyne(0) | q[1]

eng = sf.Engine("gaussian")
result = eng.run(prog)
print(result.samples)          # array con las cuadraturas medidas
```

Si imprime un array numérico sin errores, la instalación es correcta.

---

## API key de Xanadu Cloud

Para ejecutar en hardware real (actualmente suspendido) o usar la API remota se necesita una clave:

1. Crear cuenta en [platform.xanadu.ai](https://platform.xanadu.ai)
2. Ir a **Account → API Keys → Generate**
3. Configurar la variable de entorno:

```bash
export SF_API_KEY="tu_clave_aqui"
```

O desde Python antes de invocar el engine remoto:

```python
import os
os.environ["SF_API_KEY"] = "tu_clave_aqui"
```

> **Nota:** Para simulación local la API key no es necesaria. Solo se requiere si se usa `sf.RemoteEngine`.

---

## Backends disponibles

| Backend | Tipo | Estado | Uso recomendado |
|---|---|---|---|
| `gaussian` | Simulador local | Activo | Circuitos gaussianos, GBS eficiente |
| `bosonic` | Simulador local | Activo | Estados no gaussianos, gatos de Schrödinger |
| `fock` | Simulador local | Activo | Espacio de Fock truncado (costoso) |
| `Borealis` | Hardware fotónico | Suspendido (2023) | No disponible |
| `X8` | Hardware fotónico | Discontinuado | No disponible |

**Recomendación:** usar el backend `gaussian` para la mayoría de experimentos del curso. Es el más rápido y no tiene límite de tiempo de uso.

---

## Ejecución básica

```python
import strawberryfields as sf
from strawberryfields.ops import Sgate, Dgate, MeasureX

prog = sf.Program(1)
with prog.context as q:
    Sgate(1.0, 0.0) | q[0]    # squeezing r=1.0
    Dgate(0.5)      | q[0]    # desplazamiento alfa=0.5
    MeasureX        | q[0]

eng = sf.Engine("gaussian")
result = eng.run(prog, shots=100)
print(result.samples.shape)   # (100, 1)
```

---

## GBS básico: ejemplo completo de 4 modos

Gaussian Boson Sampling (GBS) es el algoritmo central del módulo 45. El siguiente ejemplo muestra un circuito completo con squeezing e interferómetro:

```python
import strawberryfields as sf
from strawberryfields.ops import Sgate, BSgate, MeasureFock
import numpy as np

N_MODOS = 4
prog = sf.Program(N_MODOS)

with prog.context as q:
    # Squeezing en todos los modos
    for i in range(N_MODOS):
        Sgate(1.0) | q[i]

    # Interferómetro: beamsplitters en pares adyacentes (capa 1)
    BSgate(np.pi/4, 0) | (q[0], q[1])
    BSgate(np.pi/4, 0) | (q[2], q[3])

    # Interferómetro: capa 2
    BSgate(np.pi/4, 0) | (q[1], q[2])

    # Medición en base de Fock (conteo de fotones)
    for i in range(N_MODOS):
        MeasureFock() | q[i]

eng = sf.Engine("gaussian")
result = eng.run(prog, shots=10)
print("Muestras de fotones:", result.samples)
# Ejemplo: [[0 1 1 0], [2 0 0 1], ...]
```

> **Nota:** `MeasureFock()` sobre un estado gaussiano requiere cálculo del hafniano internamente. Para muchos shots o muchos modos, instalar `thewalrus` mejora significativamente el rendimiento.

---

## Límites del plan gratuito y estado del hardware

El procesador fotónico **Borealis fue suspendido en octubre de 2023** tras los experimentos de ventaja cuántica. El dispositivo **X8 fue discontinuado** previamente. A mayo de 2026, Xanadu no ofrece acceso a hardware fotónico en la nube para usuarios externos.

Para los laboratorios de este curso esto no representa ninguna limitación: todos los ejercicios usan simuladores locales (`gaussian`, `fock`, `bosonic`) que no tienen cuota de uso ni requieren conexión a internet.

---

## Relación con PennyLane

Strawberry Fields se integra con PennyLane a través del plugin `pennylane-sf`, lo que permite usar circuitos fotónicos dentro de flujos de diferenciación automática y optimización variacional:

```python
import pennylane as qml

dev = qml.device("strawberryfields.gaussian", wires=2, shots=100)

@qml.qnode(dev)
def circuito(r):
    qml.Squeezing(r, 0, wires=0)
    qml.Beamsplitter(0.5, 0, wires=[0, 1])
    return qml.expval(qml.X(0))

grad = qml.grad(circuito)(0.8)
print("Gradiente:", grad)
```

SF también puede combinarse con backends de Qiskit a través de PennyLane como intermediario, aunque no existe integración directa SF–Qiskit.

---

## Laboratorio relacionado

El laboratorio práctico asociado a esta guía es:

```
Cuadernos/laboratorios/49_fotonica_cuantica.ipynb
```

Cubre GBS completo, cálculo de permanentes y comparación de backends. Se recomienda completar el Módulo 45 antes de ejecutarlo.
