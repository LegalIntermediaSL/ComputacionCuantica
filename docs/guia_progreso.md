# Guía del Sistema de Progreso del Estudiante

## Introducción

El sistema de progreso permite al estudiante registrar su avance a lo largo de los módulos del curso de Computación Cuántica. Cada módulo recibe una puntuación de 0 a 100; los módulos con puntuación igual o superior a 60 se consideran completados. El sistema es completamente local: no requiere cuenta, no envía datos a ningún servidor y funciona desde el primer momento sin configuración adicional.

---

## Cómo funciona

El progreso se almacena en `st.session_state` de Streamlit bajo la clave interna `qc_progress`. Cada entrada tiene la siguiente estructura:

```python
{
    "score": 85.0,        # float, rango 0-100
    "completed": True,    # bool: True si score >= 60
    "date": "2026-05-02T10:30:00.000000",  # ISO 8601
    "notes": ""           # str, opcional
}
```

El estado completo es un diccionario `{ module_id: entry }`, por ejemplo:

```json
{
    "01": {"score": 90, "completed": true, "date": "2026-05-02T09:00:00", "notes": ""},
    "02": {"score": 55, "completed": false, "date": "2026-05-02T09:45:00", "notes": ""}
}
```

---

## Cómo usar desde el visualizador

El módulo `visualizador/progress.py` expone las siguientes funciones públicas:

| Función | Descripción |
|---|---|
| `save_progress(module_id, score, notes="")` | Registra la puntuación de un módulo |
| `load_progress()` | Devuelve el diccionario completo de progreso |
| `get_completion_pct()` | Porcentaje de módulos completados (score >= 60) |
| `get_next_module()` | ID del siguiente módulo no completado |
| `show_progress_widget(compact=False)` | Renderiza el widget visual en la página actual |
| `reset_progress()` | Reinicia todo el progreso a cero |

La página que integra el sistema de forma más completa es **`pages/15_Certificacion.py`**, que muestra el widget completo y calcula el porcentaje global. Otras páginas pueden insertar el widget compacto con `show_progress_widget(compact=True)`.

---

## Cómo llamar desde un notebook

Desde cualquier notebook del proyecto se puede importar y usar el módulo directamente. Requiere que Streamlit esté activo (la función escribe en `st.session_state`); para uso fuera del contexto Streamlit, acceder a `MODULES` y gestionar el dict manualmente.

```python
import sys
sys.path.insert(0, "../visualizador")

from progress import save_progress, load_progress, get_completion_pct, get_next_module

# Registrar puntuación del módulo 01
save_progress("01", score=88.0, notes="Completado tras ejercicios 1-3")

# Consultar progreso global
data = load_progress()
print(data["01"])
# {'score': 88.0, 'completed': True, 'date': '2026-05-02T...', 'notes': '...'}

# Porcentaje completado
print(f"Completado: {get_completion_pct():.1f}%")

# Siguiente módulo recomendado
next_id = get_next_module()
print(f"Siguiente: {next_id}")
```

---

## Privacidad

Los datos de progreso residen **únicamente en la memoria de la sesión del navegador** (`st.session_state`). No se almacenan en disco, no se envían a ningún servidor y no son accesibles por terceros. Xanadu, IBM ni ningún otro proveedor recibe información sobre el avance del estudiante.

---

## Limitaciones

- **No persiste entre sesiones:** al cerrar o recargar el navegador el progreso se pierde.
- **No es multi-dispositivo:** cada sesión es independiente; no hay sincronización entre navegadores o equipos.
- **Sin autenticación:** no hay sistema de usuarios; el progreso no está asociado a ninguna identidad.

---

## Alternativa de persistencia (opcional avanzado)

Para persistir el progreso entre sesiones se puede usar el paquete `streamlit-local-storage`, que escribe en el `localStorage` del navegador:

```bash
pip install streamlit-local-storage
```

```python
from streamlit_local_storage import LocalStorage

ls = LocalStorage()
ls.setItem("qc_progress", load_progress())   # guardar
saved = ls.getItem("qc_progress")            # recuperar al inicio
```

Esta solución mantiene los datos en el navegador local (persisten al cerrar la pestaña) pero sigue sin ser multi-dispositivo.

---

## Módulos registrables

El sistema reconoce los siguientes 29 módulos. Cualquier `module_id` fuera de esta lista se puede registrar igualmente pero no aparecerá en el widget visual ni en el cálculo de porcentaje.

| ID | Nombre | ID | Nombre |
|---|---|---|---|
| 01 | Qubits y estados | 29 | Fault-Tolerant |
| 02 | Qiskit básico | 30 | Quantum Advantage |
| 04 | Qiskit Runtime | 38 | Quantum Sensing |
| 05 | Algoritmos clásicos | 39 | Compilación avanzada |
| 06 | Ruido y hardware | 40 | QSVT |
| 09 | Corrección de errores | 41 | Topological QC |
| 11 | Variacionales (VQE/QAOA) | 42 | Tensor Networks |
| 12 | Aplicaciones industria | 43 | Quantum Gravity |
| 14 | Surface codes | 44 | DQC avanzado |
| 15 | Evolución Trotter | 45 | Computación Fotónica |
| 16 | Canales cuánticos | 46 | Átomos Neutros y Rydberg |
| 17 | POVM y medidas | 47 | qLDPC y Decodificadores |
| 19 | Tomografía | 48 | QNLP |
| 22 | Recursos cuánticos | 49 | D-Wave y Annealing |
| 26 | ZX-Calculus | 28 | Aplicaciones emergentes |
