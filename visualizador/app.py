import streamlit as st

st.set_page_config(
    page_title="Laboratorio Cuántico Interactivo",
    page_icon="⚛️",
    layout="wide",
)

st.title("⚛️ Laboratorio Cuántico Interactivo")
st.markdown(
    """
    Bienvenido al laboratorio visual del curso **ComputacionCuantica**.
    Usa el menú lateral para navegar entre los módulos interactivos.
    """
)

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        ### Módulos disponibles

        | Módulo | Artículos relacionados |
        |---|---|
        | **Esfera de Bloch y Ruido** | 01_fundamentos, 16_canales |
        | **Algoritmos Paso a Paso** | 05_algoritmos (Grover, QPE) |
        | **Canales y Ruido** | 16_canales, 21_open_quantum |
        | **Hardware Dashboard** | 23_hardware, 24_control_pulsos |
        | **VQE / QAOA** | 11_algoritmos_variacionales |
        """
    )

with col2:
    st.markdown(
        """
        ### Cómo usar este laboratorio

        1. Selecciona un módulo en la barra lateral izquierda.
        2. Ajusta los parámetros con los controles interactivos.
        3. Los resultados se actualizan en tiempo real.
        4. Cada módulo conecta con los artículos del tutorial.

        **Requisitos:**
        ```
        qiskit >= 2.0
        qiskit-aer >= 0.15
        streamlit >= 1.35
        matplotlib numpy scipy
        ```
        """
    )

st.divider()
st.info(
    "Para lanzar localmente: `streamlit run visualizador/app.py` "
    "desde la raíz del repositorio."
)
st.caption("Parte del repositorio ComputacionCuantica · 2026")
