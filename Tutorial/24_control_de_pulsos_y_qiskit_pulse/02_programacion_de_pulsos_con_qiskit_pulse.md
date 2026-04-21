# Programación de Pulsos con Qiskit Pulse

Qiskit Pulse (módulo `qiskit.pulse`) permite a los investigadores saltarse la capa de "puertas digitales" ($X, CNOT$, etc.) y definir las señales de microondas crudas que se enviarán a los procesadores cuánticos actuales.

## Conceptos Clave

1. **Channels:** Representan líneas de control físicas.
    - `DriveChannel`: Para manipular qubits individuales.
    - `MeasureChannel`: Para enviar pulsos de lectura.
    - `ControlChannel`: Para operaciones multiqubit (como Cross-Resonance).
2. **Instructions:** Formas de onda (`Play`), retardos (`Delay`) o alineación (`Barrier`).
3. **Schedule:** El contenedor que organiza las instrucciones en el tiempo.

## Ejemplo Conceptual de un Pulso X

```python
from qiskit import pulse
from qiskit.pulse.library import Gaussian

# Definir la envolvente
amp = 0.5
sigma = 64
duration = 512
x_pulse = Gaussian(duration=duration, amp=amp, sigma=sigma)

# Crear el Schedule
with pulse.build(name='Pulso X experimental') as x_sched:
    # Canal de drive del qubit 0
    d0 = pulse.drive_channel(0)
    pulse.play(x_pulse, d0)

x_sched.draw()
```

## Por qué usar Qiskit Pulse?

- **Calibración:** Para encontrar la amplitud exacta que causa una rotación de $\pi$ (experimento de Rabi).
- **Física de Errores:** Estudiar cómo un pulso defectuoso genera errores de fase o fugas.
- **Eficiencia:** A veces, una operación compleja puede implementarse con un solo pulso personalizado más corto que una secuencia de puertas estándar, reduciendo el impacto de la decoherencia.

## Navegación
- Anterior: [Introducción al control por microondas](01_introduccion_al_control_por_microondas.md)
- Siguiente: [Criptografía post-cuántica (PQC)](../25_criptografia_post_cuantica_pqc/01_criptografia_post_cuantica_pqc.md)
