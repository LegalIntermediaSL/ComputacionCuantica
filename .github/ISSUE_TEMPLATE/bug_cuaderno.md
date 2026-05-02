---
name: "🐛 Bug en Cuaderno (Notebook)"
about: "Reportar un error de ejecución, resultado incorrecto o celda que falla en un laboratorio"
title: "[BUG] Lab XX — Descripción breve del error"
labels: ["bug", "notebooks"]
assignees: []
---

## Laboratorio afectado

- **Archivo:** `Cuadernos/laboratorios/XX_nombre.ipynb`
- **Celda número:** (si aplica)
- **Sección:** (número y título de la sección en el notebook)

## Descripción del error

<!-- Describe claramente qué falla y qué comportamiento esperabas -->

## Error completo (traceback)

```
Pega aquí el mensaje de error completo
```

## Entorno

- Python: `python --version`
- Qiskit: `python -c "import qiskit; print(qiskit.__version__)"`
- NumPy: `python -c "import numpy; print(numpy.__version__)"`
- OS: (Linux / macOS / Windows)
- Cómo ejecutas el notebook: (JupyterLab / VS Code / Colab / otra)

## Pasos para reproducir

1. Abre el notebook `Cuadernos/laboratorios/XX_...ipynb`
2. Ejecuta las celdas en orden hasta la celda N
3. Observa el error

## Posible solución (opcional)

<!-- Si tienes una idea de por qué falla o cómo arreglarlo, compártela -->
