# Notas

Este directorio reune material fuente y notas de trabajo para futuras ampliaciones del proyecto.

## Estructura

- `pdf/` — artículos y papers de referencia descargados
- `notas_utiles/` — apuntes de trabajo y borradores
- `referencias/` — bibliografía y enlaces externos
- `resumenes/` — resúmenes preliminares (versiones antiguas, antes de `Resumenes/`)

## Criterio editorial

Este directorio es el **área de staging** del proyecto: material que aún no ha sido integrado
en `Tutorial/`, `Cuadernos/` o `Resumenes/`.

### ¿Qué se integra y qué no?

| Tipo de contenido | Destino |
|---|---|
| Teoría suficientemente desarrollada (>500 palabras, con LaTeX) | `Tutorial/NN_modulo/README.md` |
| Resumen autónomo de un tema (200-600 palabras) | `Resumenes/NN_tema.md` |
| Código ejecutable con contexto pedagógico | `Cuadernos/laboratorios/` o `guiados/` |
| Referencia bibliográfica | Apéndice del módulo más cercano |
| Borrador incompleto o notas personales | Permanece en `Notas/` |

### Proceso de integración

1. Identifica el módulo tutorial más cercano al tema.
2. Si el módulo existe: añade como sección o apéndice en su `README.md`.
3. Si el tema merece módulo propio: abre una issue con label `content` antes de crear.
4. Si es autónomo y compacto: añade a `Resumenes/` como `NN_tema.md` y enlaza desde `mkdocs.yml`.
5. Tras integrar, mueve el archivo original a `Notas/integrado/` (no borrar — mantener historial).

### Estado actual

El material en `pdf/` y `referencias/` es bibliografía de apoyo, no destinada a integración directa.
El material en `notas_utiles/` puede contener borradores; revisar antes de abrir una fase nueva.
Los `resumenes/` aquí son versiones antiguas — el contenido canónico está en `Resumenes/` (raíz).
