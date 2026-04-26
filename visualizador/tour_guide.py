"""
Tour guiado y exportación PNG reutilizables para todas las páginas del visualizador.

Uso en cada página:
    from tour_guide import show_tour, export_figure_button

    show_tour("nombre_pagina", STEPS)
    export_figure_button(fig, "nombre_archivo", params_dict)
"""

import io
import json
import datetime
import streamlit as st


def show_tour(page_id: str, steps: list[dict]) -> None:
    """
    Muestra un botón "▶ Tour interactivo" y, cuando está activo,
    navega entre los pasos con botones Anterior/Siguiente.

    Parámetros:
        page_id:  identificador único de la página (evita colisiones de state).
        steps:    lista de dicts con claves "title" y "body" (admite Markdown).
    """
    if not steps:
        return

    state_key = f"_tour_active_{page_id}"
    step_key  = f"_tour_step_{page_id}"

    if state_key not in st.session_state:
        st.session_state[state_key] = False
    if step_key not in st.session_state:
        st.session_state[step_key] = 0

    # ── Botón de activación ──────────────────────────────────────────────────
    col_btn, col_spacer = st.columns([1, 5])
    with col_btn:
        label = "⏹ Salir del tour" if st.session_state[state_key] else "▶ Tour interactivo"
        if st.button(label, key=f"_tour_toggle_{page_id}"):
            st.session_state[state_key] = not st.session_state[state_key]
            st.session_state[step_key] = 0

    # ── Panel de tour ────────────────────────────────────────────────────────
    if st.session_state[state_key]:
        step_idx = st.session_state[step_key]
        total    = len(steps)
        step     = steps[step_idx]

        with st.container(border=True):
            progress_pct = int((step_idx + 1) / total * 100)
            st.progress(progress_pct,
                        text=f"Paso {step_idx + 1} de {total}: **{step['title']}**")
            st.info(step["body"])

            col_prev, col_next, col_close = st.columns([1, 1, 4])
            with col_prev:
                if st.button("◀ Anterior",
                             key=f"_tour_prev_{page_id}",
                             disabled=(step_idx == 0)):
                    st.session_state[step_key] -= 1
                    st.rerun()
            with col_next:
                if step_idx < total - 1:
                    if st.button("Siguiente ▶", key=f"_tour_next_{page_id}"):
                        st.session_state[step_key] += 1
                        st.rerun()
                else:
                    if st.button("✓ Finalizar tour", key=f"_tour_finish_{page_id}"):
                        st.session_state[state_key] = False
                        st.session_state[step_key] = 0
                        st.rerun()


def export_figure_button(
    fig,
    filename_base: str,
    params: dict | None = None,
    dpi: int = 150,
    key: str | None = None,
) -> None:
    """
    Muestra un botón de descarga para exportar una figura Matplotlib como PNG.
    Incrusta los parámetros actuales en los metadatos PNG (campo Description).

    Parámetros:
        fig:           figura Matplotlib a exportar.
        filename_base: nombre base sin extensión (se añade fecha y hora).
        params:        dict de parámetros del estado actual (se serializa en los metadatos).
        dpi:           resolución de la imagen (default 150).
        key:           clave única de Streamlit (autogenerada si None).
    """
    import matplotlib
    from matplotlib.backends.backend_agg import FigureCanvasAgg

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_base}_{ts}.png"

    # Serializar parámetros como texto para incrustar en los metadatos PNG
    metadata = {}
    if params:
        metadata["Description"] = json.dumps(params, ensure_ascii=False, default=str)
        metadata["Software"] = "ComputacionCuantica Visualizador"
        metadata["CreationTime"] = ts

    buf = io.BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.print_figure(buf, format="png", dpi=dpi, metadata=metadata)
    buf.seek(0)

    btn_key = key or f"_export_png_{filename_base}"
    st.download_button(
        label="📥 Exportar PNG",
        data=buf,
        file_name=filename,
        mime="image/png",
        key=btn_key,
        help=f"Descarga la figura actual como {filename} con los parámetros en los metadatos.",
    )
