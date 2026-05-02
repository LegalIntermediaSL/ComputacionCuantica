# Resumen 16 — Infraestructura CI/CD para Proyectos Cuánticos

## 1. GitHub Actions — Workflows para QC

Un pipeline CI/CD típico para proyectos de computación cuántica usa múltiples jobs:

```yaml
# .github/workflows/ci.yml
name: CI Cuántico
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -e ".[dev]"
      - run: pytest tests/ --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v4
  notebooks:
    runs-on: ubuntu-latest
    steps:
      - run: pytest --nbval notebooks/ --nbval-lax
  docs:
    runs-on: ubuntu-latest
    steps:
      - run: mkdocs build --strict
```

**Eventos clave**: `push` a `main`, `pull_request`, `schedule` (cron para regresión semanal).

---

## 2. Jerarquía de Tests con pytest

| Nivel | Directorio | Qué prueba | Velocidad |
|---|---|---|---|
| Unitarios | `tests/unit/` | Funciones aisladas, circuitos pequeños | Rápido (~ms) |
| Integración | `tests/integration/` | Pipelines completos, simulador local | Medio (~s) |
| Notebooks | `notebooks/` + `--nbval` | Ejecución completa de cuadernos | Lento (~min) |
| Hardware | `tests/hardware/` | Marcados `@pytest.mark.hardware` | Muy lento (skip en CI) |

**Configuración en `pyproject.toml`**:

```toml
[tool.pytest.ini_options]
markers = ["hardware: requiere acceso a QPU real"]
addopts = "--tb=short -q"
testpaths = ["tests"]
```

---

## 3. Validación de Notebooks con nbval

**nbval** ejecuta cuadernos Jupyter y compara salidas con las almacenadas en celda:

```bash
pytest --nbval notebooks/Lab01_Introduccion.ipynb
pytest --nbval-lax notebooks/   # ignora diferencias de formato
pytest --nbval-sanitize-with sanitize.cfg notebooks/
```

**Archivo de sanitización** (`sanitize.cfg`):

```ini
[regex1]
regex: \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}
replace: <DATE>

[regex2]
regex: job_id: [a-z0-9]{8}
replace: job_id: <ID>
```

Esto estabiliza salidas con timestamps, IDs de jobs cuánticos, y valores flotantes variables.

---

## 4. Docker y DevContainers

**Dockerfile** para entorno cuántico reproducible:

```dockerfile
FROM python:3.11-slim
WORKDIR /workspace
COPY requirements.txt .
RUN pip install --no-cache-dir qiskit pennylane cirq lambeq
COPY . .
RUN pip install -e ".[dev]"
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser"]
```

**DevContainer** (`.devcontainer/devcontainer.json`):

```json
{
  "name": "Quantum Computing",
  "dockerfilePath": "../Dockerfile",
  "extensions": ["ms-python.python", "ms-toolsai.jupyter"],
  "postCreateCommand": "pip install -e '.[dev]'"
}
```

Permite desarrollo uniforme en VS Code, GitHub Codespaces, y Gitpod.

---

## 5. MkDocs Material y Documentación

**`mkdocs.yml`** con Material y extensiones matemáticas:

```yaml
site_name: Computación Cuántica
theme:
  name: material
  features: [navigation.tabs, content.code.copy]
plugins:
  - search
  - mkdocstrings:
      handlers:
        python: {options: {show_source: true}}
markdown_extensions:
  - pymdownx.arithmatex:
      generic: true
extra_javascript:
  - https://cdn.jsdelivr.net/npm/mathjax@3/...
```

---

## 6. Codecov — Cobertura de Tests

**Configuración** (`.codecov.yml`):

```yaml
coverage:
  status:
    project:
      default:
        target: 80%      # umbral mínimo
        threshold: 2%    # tolerancia a caída
    patch:
      default:
        target: 70%
```

| Métrica | Objetivo típico QC | Nota |
|---|---|---|
| Líneas | $\geq 80\%$ | Código Python |
| Ramas | $\geq 70\%$ | Condicionales |
| Funciones | $\geq 85\%$ | APIs públicas |
| Notebooks | Via nbval | No en Codecov directo |

---

## Resumen del Pipeline

```
git push → GitHub Actions
  ├── pytest (unit + integration) → Codecov
  ├── pytest --nbval (notebooks)
  ├── mkdocs build (documentación)
  └── Docker build (imagen reproducible)
```
