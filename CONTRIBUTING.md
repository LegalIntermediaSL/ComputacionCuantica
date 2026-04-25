# Guía de Contribución

Gracias por tu interés en mejorar este proyecto. Esta guía explica cómo añadir artículos,
notebooks y ejercicios manteniendo la coherencia del curso.

---

## Principios generales

- Priorizar claridad pedagógica antes que densidad innecesaria.
- Mantener la notación consistente entre módulos.
- Enlazar siempre la teoría con el notebook asociado.
- Evitar duplicar contenido si puede integrarse en un módulo existente.
- Todo el código debe usar **Qiskit 2.0** (primitivas V2).

---

## Convenciones de nomenclatura

### Artículos del tutorial

```
Tutorial/NN_nombre_del_modulo/MM_titulo_del_articulo.md
```

- `NN` = número de módulo con cero delante (01, 28, 30…)
- `MM` = número de artículo dentro del módulo (01, 02…)
- Nombres en minúsculas, palabras separadas por guión bajo, sin acentos.

### Notebooks

```
Cuadernos/laboratorios/NN_titulo_breve.ipynb
Cuadernos/ejemplos/NN_titulo_breve.ipynb
Cuadernos/problemas_resueltos/NN_titulo_breve.ipynb
```

### Páginas del visualizador

```
visualizador/pages/N_Titulo_Con_Mayusculas.py
```

---

## Plantilla de artículo

Cada artículo debe seguir esta estructura:

```markdown
# Título del artículo

**Módulo NN · Artículo MM · Nivel [básico | intermedio | avanzado]**

---

## Introducción / motivación

## Formalismo matemático  (LaTeX)

## Implementación en Qiskit 2.0  (código ejecutable)

## Ejercicio propuesto

## Referencias y lectura adicional
```

---

## Estándares de código Qiskit 2.0

| ❌ Deprecated | ✅ Qiskit 2.0 |
|---|---|
| `execute(qc, backend, shots=...)` | `AerSimulator().run(qc, shots=...)` |
| `QuantumInstance` | `StatevectorEstimator` / `StatevectorSampler` |
| `expectation_value("Z")` | `expectation_value(SparsePauliOp("Z"))` |
| `qc.draw("mpl")` sin try/except | Envolver en try/except con fallback a `"text"` |
| `Estimator()` (V1 primitiva) | `StatevectorEstimator()` o `EstimatorV2` |

Los imports de bibliotecas opcionales (PyZX, pylatexenc) deben ir dentro de un
`try/except ImportError` con un mensaje claro de instalación.

---

## Checklist de Pull Request

Antes de abrir un PR, verifica:

- [ ] Sintaxis correcta: `python -m py_compile ruta/archivo.py`
- [ ] Código Qiskit 2.0 (sin `execute()`, sin `QuantumInstance`)
- [ ] Glosario actualizado si se introducen términos nuevos
- [ ] Índices actualizados (`Tutorial/indice_general.md`, `README.md`)
- [ ] Notebook ejecuta sin errores: `jupyter nbconvert --execute notebook.ipynb`
- [ ] Imports opcionales con try/except y fallback
- [ ] Sin secretos, tokens ni credenciales en el código

---

## Estructura de directorios

```
ComputacionCuantica/
├── Tutorial/               # Artículos teóricos (Markdown + LaTeX)
│   ├── 01_fundamentos/
│   ├── ...
│   └── 30_quantum_advantage_casos_reales/
├── Cuadernos/
│   ├── laboratorios/       # Notebooks ejecutables en CI
│   ├── ejemplos/           # Snippets cortos ilustrativos
│   └── problemas_resueltos/
├── visualizador/           # Aplicación Streamlit (8 páginas)
│   ├── app.py
│   └── pages/
├── Ejercicios/             # Ejercicios por nivel + evaluador automático
├── Soluciones/             # Soluciones por módulo temático
├── Resumenes/              # Fichas de repaso rápido
├── glosario.md             # 80+ términos con definiciones
└── requirements.txt        # Dependencias con versiones pinadas
```

---

## Cómo ejecutar el visualizador localmente

```bash
pip install -r requirements.txt
streamlit run visualizador/app.py
```

## Cómo usar el evaluador de ejercicios

```python
from Ejercicios.evaluador import evaluar, listar_ejercicios

listar_ejercicios()   # ver todos los ejercicios disponibles

def mi_solucion():
    from qiskit import QuantumCircuit
    qc = QuantumCircuit(1)
    qc.h(0)
    return qc

score, feedback = evaluar("basicos", 1, mi_solucion)
```

---

*Este proyecto es un recurso abierto para la comunidad hispana de computación cuántica.*
