# Programación de pulsos con Qiskit Pulse

## 1. La capa de pulsos en Qiskit

Qiskit expone tres niveles de abstracción para programar un procesador cuántico:

1. **Circuitos de puertas** (`QuantumCircuit`): el nivel más alto. El compilador elige los pulsos.
2. **Qiskit Pulse** (`qiskit.pulse`): el nivel de pulsos. El usuario define las formas de onda directamente.
3. **Hardware raw**: señales digitales al DAC (acceso solo para fabricantes).

Qiskit Pulse permite a los investigadores saltarse la compilación estándar y controlar directamente las señales de microondas que se envían al procesador. Es la herramienta para calibración, diseño de nuevas puertas y estudio de la física de errores.

## 2. Conceptos fundamentales

### 2.1 Channels (canales)

Los canales representan líneas de control físicas del procesador:

- `DriveChannel(i)`: canal de drive del qubit $i$ (para puertas de un qubit).
- `ControlChannel(i)`: canal de control cruzado para puertas de dos qubits (Cross-Resonance).
- `MeasureChannel(i)`: canal de lectura del qubit $i$.
- `AcquireChannel(i)`: canal de adquisición de la señal de lectura.

### 2.2 Pulses (envolventes)

Las envolventes disponibles en `qiskit.pulse.library`:

- `Gaussian(duration, amp, sigma)`: envolvente gaussiana.
- `GaussianSquare(duration, amp, sigma, risefall_sigma_ratio)`: gaussiana con plateau central.
- `Drag(duration, amp, sigma, beta)`: pulso DRAG para suprimir fugas.
- `Constant(duration, amp)`: pulso rectangular.

Los parámetros se especifican en **muestras de tiempo** (dt, típicamente 0.222 ns por muestra en procesadores IBM).

### 2.3 Instructions (instrucciones)

- `Play(pulse, channel)`: reproducir una forma de onda en un canal.
- `Delay(duration, channel)`: insertar un tiempo de espera.
- `SetPhase(phase, channel)`: cambiar la fase del generador (implementa $R_z$ virtual).
- `ShiftFrequency(frequency, channel)`: cambiar la frecuencia del drive.
- `Acquire(duration, channel, mem_slot)`: medir y guardar el resultado.

### 2.4 Schedules y ScheduleBlocks

Un `Schedule` o `ScheduleBlock` es el contenedor temporal que organiza las instrucciones en el tiempo. Los bloques permiten alineación automática de instrucciones.

## 3. Experimento de Rabi con Qiskit Pulse

```python
from qiskit import pulse
from qiskit.pulse.library import Gaussian
import numpy as np

# Parámetros del pulso (en muestras, dt ≈ 0.222 ns)
duration = 160    # 160 muestras ≈ 35.5 ns
sigma = 40        # anchura gaussiana

amplitudes = np.linspace(0, 1.0, 50)
schedules = []

for amp in amplitudes:
    x_pulse = Gaussian(duration=duration, amp=amp, sigma=sigma)

    with pulse.build(name=f'rabi_amp_{amp:.3f}') as sched:
        d0 = pulse.drive_channel(0)
        m0 = pulse.measure_channel(0)
        a0 = pulse.acquire_channel(0)

        # Aplicar pulso de drive
        pulse.play(x_pulse, d0)

        # Medir el qubit 0
        pulse.measure(0)

    schedules.append(sched)

print(f"Creados {len(schedules)} schedules para el experimento de Rabi")
print(f"Cada schedule tiene un pulso de {duration} muestras ≈ {duration*0.222:.1f} ns")
```

## 4. Implementar una puerta X calibrada

```python
from qiskit import pulse
from qiskit.pulse.library import Drag

def calibrated_x_gate(qubit: int, amp: float, sigma: int = 40,
                       beta: float = 0.0, duration: int = 160) -> pulse.ScheduleBlock:
    """
    Puerta X calibrada usando DRAG para suprimir fugas al nivel |2>.
    
    Args:
        qubit: índice del qubit objetivo
        amp: amplitud del pulso (determinada por el experimento de Rabi)
        sigma: anchura gaussiana en muestras
        beta: parámetro DRAG (0.0 = gaussiana pura, sin supresión de fugas)
        duration: duración total del pulso en muestras
    """
    drag_pulse = Drag(duration=duration, amp=amp, sigma=sigma, beta=beta)

    with pulse.build(name=f'x_q{qubit}') as x_sched:
        pulse.play(drag_pulse, pulse.drive_channel(qubit))

    return x_sched

# Puerta X sin DRAG
x_no_drag = calibrated_x_gate(0, amp=0.5, beta=0.0)

# Puerta X con DRAG (beta ajustado experimentalmente)
x_with_drag = calibrated_x_gate(0, amp=0.5, beta=-0.5)

print("Schedule X sin DRAG:", x_no_drag)
print("Schedule X con DRAG:", x_with_drag)
```

## 5. Implementar $R_z$ virtual (frame change)

Las puertas $R_z$ no requieren pulso físico. Se implementan cambiando la fase del generador de microondas, lo que equivale a rotar el marco de referencia:

```python
from qiskit import pulse

def virtual_rz(qubit: int, angle: float) -> pulse.ScheduleBlock:
    """
    Puerta Rz(angle) como cambio de fase virtual del generador.
    No consume tiempo de coherencia.
    
    Args:
        qubit: índice del qubit
        angle: ángulo de rotación en radianes
    """
    with pulse.build(name=f'rz_{angle:.3f}_q{qubit}') as rz_sched:
        # ShiftPhase en el canal de drive acumula la fase para pulsos futuros
        pulse.shift_phase(-angle, pulse.drive_channel(qubit))

    return rz_sched

# Puerta Z = Rz(π)
z_gate = virtual_rz(0, np.pi)
# Puerta S = Rz(π/2)
s_gate = virtual_rz(0, np.pi/2)
# Puerta T = Rz(π/4)
t_gate = virtual_rz(0, np.pi/4)

print("Puerta Z (fase -π):", z_gate)
print("Puerta T (fase -π/4):", t_gate)
```

## 6. Cross-Resonance: puerta CNOT nativa

La puerta Cross-Resonance (CR) es el mecanismo nativo para CNOT en procesadores IBM. Consiste en aplicar un drive al qubit control a la frecuencia del qubit objetivo:

```python
from qiskit import pulse
from qiskit.pulse.library import GaussianSquare

def cr_gate(control: int, target: int, amp: float,
            duration: int = 1312) -> pulse.ScheduleBlock:
    """
    Pulso Cross-Resonance básico para implementar CNOT(control, target).
    En hardware real, se combina con puertas locales para el CNOT completo.
    
    Args:
        control: qubit de control
        target: qubit objetivo
        amp: amplitud del pulso CR (calibrada experimentalmente)
        duration: duración en muestras (~290 ns)
    """
    cr_pulse = GaussianSquare(
        duration=duration,
        amp=amp,
        sigma=64,
        risefall_sigma_ratio=2
    )

    with pulse.build(name=f'cr_{control}_{target}') as cr_sched:
        # El canal ControlChannel conecta el qubit control con el target
        pulse.play(cr_pulse, pulse.control_channels(control, target)[0])

    return cr_sched

cr = cr_gate(0, 1, amp=0.3)
print(f"Pulso CR creado, duración: {cr.duration} muestras ≈ {cr.duration*0.222:.0f} ns")
```

## 7. Experimento de Ramsey para medir $T_2^*$

```python
from qiskit import pulse
from qiskit.pulse.library import Gaussian
import numpy as np

def ramsey_schedule(qubit: int, delay_samples: int,
                    amp_pi2: float, sigma: int = 40) -> pulse.ScheduleBlock:
    """
    Secuencia Ramsey: π/2 → espera → π/2 → medición.
    Mide la decoherencia de fase T2*.
    """
    pi2_pulse = Gaussian(duration=160, amp=amp_pi2/2, sigma=sigma)

    with pulse.build(name=f'ramsey_delay_{delay_samples}') as sched:
        d0 = pulse.drive_channel(qubit)

        # Primer pulso π/2
        pulse.play(pi2_pulse, d0)
        # Tiempo libre de evolución
        pulse.delay(delay_samples, d0)
        # Segundo pulso π/2
        pulse.play(pi2_pulse, d0)
        # Medición
        pulse.measure(qubit)

    return sched

# Crear schedules para diferentes tiempos de espera
dt = 0.222e-9  # segundos por muestra
delays_ns = np.linspace(0, 50000, 30)  # 0 a 50 μs
delays_samples = (delays_ns * 1e-9 / dt).astype(int)

schedules = [ramsey_schedule(0, d, amp_pi2=0.5) for d in delays_samples]
print(f"Experimento de Ramsey: {len(schedules)} puntos de tiempo")
print(f"Rango de tiempos: 0 a {delays_ns[-1]/1000:.1f} μs")
```

## 8. Por qué usar Qiskit Pulse

**Calibración:** permite encontrar la amplitud exacta del pulso $\pi$ para cada qubit (el compilador de IBM actualiza esta calibración periódicamente, pero con Pulse se puede recalibrar manualmente).

**Nuevas puertas:** se pueden implementar puertas que no están en el conjunto nativo. Por ejemplo, la puerta $e^{-i\theta ZZ}$ directamente usando el acoplamiento ZZ natural entre qubits vecinos.

**Eficiencia:** un operador complejo puede implementarse con un solo pulso personalizado más corto que la secuencia de puertas estándar compilada. Esto reduce la profundidad del circuito y el impacto de la decoherencia.

**Investigación de errores:** permite estudiar cómo defectos específicos en la forma del pulso (amplitud incorrecta, fuga de fase) se traducen en errores de proceso.

**Nota:** a partir de Qiskit 1.0, el acceso a hardware de IBM vía Qiskit Pulse está siendo restringido a usuarios con acceso Premium (IBM Research). En simuladores con Qiskit Aer y en procesadores de otros fabricantes, Qiskit Pulse sigue siendo accesible.

## 9. Ideas clave

- Qiskit Pulse expone la capa de control de microondas: formas de onda, canales, fases.
- Las puertas de un qubit son pulsos gaussianos o DRAG en `DriveChannel`; las puertas $R_z$ son cambios de fase virtuales (sin coste temporal).
- Las puertas de dos qubits (Cross-Resonance) usan `ControlChannel` con pulsos de mayor duración.
- El experimento de Rabi calibra la amplitud del pulso $\pi$; el experimento de Ramsey mide $T_2^*$.
- Qiskit Pulse es la herramienta para investigación de calibración, diseño de puertas y estudio de física de errores a nivel de señal.

## 10. Ejercicios sugeridos

1. Crear un schedule que implemente la secuencia de Hahn echo (π/2 → delay → π → delay → π/2 → medición) y explicar cómo revierte el desfase estático.
2. Modificar el experimento de Rabi para incluir un detuning de $\delta = 2\pi \times 1\,\text{MHz}$ y observar cómo la frecuencia de oscilación cambia.
3. Comparar la duración de una puerta CNOT nativa (Cross-Resonance) con la duración de la misma puerta compilada como secuencia de puertas de la base nativa.
4. Implementar una puerta $R_x(\theta)$ parametrizada como `ScheduleBlock` con `Parameter` de Qiskit y ejecutarla para $\theta \in [0, 2\pi]$.

## Navegación

- Anterior: [Introducción al control por microondas](01_introduccion_al_control_por_microondas.md)
- Siguiente: [Criptografía post-cuántica (PQC)](../25_criptografia_post_cuantica_pqc/01_criptografia_post_cuantica_pqc.md)
