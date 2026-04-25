"""
Tour guiado reutilizable para todas las páginas del visualizador.

Uso en cada página:
    from tour_guide import show_tour

    STEPS = [
        {"title": "Paso 1", "body": "Descripción del control A."},
        {"title": "Paso 2", "body": "Descripción del fenómeno B."},
    ]
    show_tour("nombre_pagina", STEPS)
"""

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

    state_key   = f"_tour_active_{page_id}"
    step_key    = f"_tour_step_{page_id}"

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
        step_idx  = st.session_state[step_key]
        total     = len(steps)
        step      = steps[step_idx]

        with st.container(border=True):
            progress_pct = int((step_idx + 1) / total * 100)
            st.progress(progress_pct,
                        text=f"Paso {step_idx + 1} de {total}: **{step['title']}**")
            st.info(step["body"])

            col_prev, col_next, col_close = st.columns([1, 1, 4])
            with col_prev:
                prev_disabled = step_idx == 0
                if st.button("◀ Anterior",
                             key=f"_tour_prev_{page_id}",
                             disabled=prev_disabled):
                    st.session_state[step_key] -= 1
                    st.rerun()
            with col_next:
                if step_idx < total - 1:
                    if st.button("Siguiente ▶",
                                 key=f"_tour_next_{page_id}"):
                        st.session_state[step_key] += 1
                        st.rerun()
                else:
                    if st.button("✓ Finalizar tour",
                                 key=f"_tour_finish_{page_id}"):
                        st.session_state[state_key] = False
                        st.session_state[step_key] = 0
                        st.rerun()
