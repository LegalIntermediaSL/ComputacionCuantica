"""
Página 0 — Inicio: Selector de perfil y rutas de aprendizaje personalizadas.
"""
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

st.set_page_config(page_title="Inicio — Computación Cuántica", layout="wide", page_icon="⚛️")

st.title("⚛️ Computación Cuántica — Teoría y Práctica")
st.markdown(
    "**50+ módulos · 53 laboratorios · 20 páginas interactivas · >200 tests · En español**"
)
st.divider()

# ── Selector de perfil ────────────────────────────────────────────────────────
st.subheader("¿Cuál es tu perfil?")

perfil = st.radio(
    "Selecciona el que mejor te describe:",
    ["🎓 Estudiante — aprendiendo los fundamentos",
     "🔬 Investigador — profundizando en teoría avanzada",
     "🛠️ Ingeniero — aplicando QC en industria",
     "📢 Divulgador — enseñando y comunicando QC"],
    horizontal=True
)

st.divider()

# ── Rutas de aprendizaje por perfil ──────────────────────────────────────────
RUTAS = {
    "🎓 Estudiante — aprendiendo los fundamentos": {
        "descripcion": "Comienza desde los fundamentos matemáticos y avanza gradualmente hasta los algoritmos cuánticos más importantes.",
        "modulos": [
            ("Módulo 01", "Qubits y estados", "📐"),
            ("Módulo 02", "Qiskit básico", "💻"),
            ("Módulo 04", "Qiskit Runtime", "🔌"),
            ("Módulo 05", "Algoritmos clásicos", "🔢"),
            ("Módulo 06", "Ruido y hardware", "📡"),
            ("Módulo 09", "Corrección errores", "🛡️"),
            ("Módulo 11", "VQE/QAOA", "🧮"),
        ],
        "labs": ["Lab 01-10", "Lab 11", "Lab 12"],
        "tiempo": "~60 horas",
        "siguiente": "Ruta Investigador tras completar los módulos base",
    },
    "🔬 Investigador — profundizando en teoría avanzada": {
        "descripcion": "Diseñado para quien ya conoce los fundamentos y quiere explorar fronteras del campo: topológica, redes tensoriales, qLDPC, QSVT.",
        "modulos": [
            ("Módulo 16", "Canales cuánticos", "📊"),
            ("Módulo 22", "Recursos cuánticos", "⚗️"),
            ("Módulo 26", "ZX-Calculus", "📐"),
            ("Módulo 38", "Quantum Sensing", "🔭"),
            ("Módulo 40", "QSVT", "📈"),
            ("Módulo 41", "Topological QC", "🔮"),
            ("Módulo 47", "qLDPC", "🛡️"),
        ],
        "labs": ["Lab 45-51", "R1-R12"],
        "tiempo": "~120 horas",
        "siguiente": "Contribuir al repositorio con nuevos módulos",
    },
    "🛠️ Ingeniero — aplicando QC en industria": {
        "descripcion": "Enfocado en herramientas prácticas: hardware real IBM, optimización con D-Wave, QML, química cuántica, benchmark.",
        "modulos": [
            ("Módulo 04", "Qiskit Runtime", "🔌"),
            ("Módulo 12", "Aplicaciones industria", "🏭"),
            ("Módulo 29", "Fault-Tolerant", "⚙️"),
            ("Módulo 30", "Quantum Advantage", "🏆"),
            ("Módulo 39", "Compilación avanzada", "🔧"),
            ("Módulo 49", "D-Wave/QUBO", "🎯"),
            ("Página 20", "Compilador interactivo", "💡"),
        ],
        "labs": ["Lab 12", "Lab 33", "Lab 39", "Lab 53"],
        "tiempo": "~80 horas",
        "siguiente": "Benchmark en IBM Quantum (Hardware real)",
    },
    "📢 Divulgador — enseñando y comunicando QC": {
        "descripcion": "Recursos para explicar la computación cuántica a audiencias no técnicas: visualizaciones, analogías, historia y perspectivas.",
        "modulos": [
            ("Módulo 01", "Qubits y estados", "📐"),
            ("Módulo 30", "Quantum Advantage", "🏆"),
            ("Módulo 28", "Aplicaciones emergentes", "🌐"),
            ("Módulo 45", "Computación Fotónica", "🔬"),
            ("Módulo 46", "Átomos Neutros", "⚛️"),
            ("Página 17", "Fotónica interactiva", "🎨"),
            ("Página 18", "Rydberg interactivo", "🎯"),
        ],
        "labs": ["Resúmenes 1-20", "Glosario"],
        "tiempo": "~40 horas",
        "siguiente": "Contribuir con traducciones o nuevas visualizaciones",
    },
}

perfil_key = perfil
ruta = RUTAS[perfil_key]

col_desc, col_modulos = st.columns([1, 2])
with col_desc:
    st.markdown(f"### Ruta recomendada")
    st.info(ruta["descripcion"])
    st.metric("⏱️ Tiempo estimado", ruta["tiempo"])
    st.markdown(f"**Laboratorios clave:** {', '.join(ruta['labs'])}")
    st.markdown(f"**Siguiente paso:** {ruta['siguiente']}")

with col_modulos:
    st.markdown("### Módulos de la ruta")
    cols_m = st.columns(4)
    for i, (mod_id, mod_name, emoji) in enumerate(ruta["modulos"]):
        with cols_m[i % 4]:
            st.markdown(f"""
<div style="background:#f0f4ff;border-radius:8px;padding:8px;margin:4px;text-align:center">
<div style="font-size:1.5em">{emoji}</div>
<div style="font-size:0.8em;font-weight:bold">{mod_id}</div>
<div style="font-size:0.75em">{mod_name}</div>
</div>""", unsafe_allow_html=True)

st.divider()

# ── Mapa visual del curso ─────────────────────────────────────────────────────
st.subheader("🗺️ Mapa del Curso Completo")

col_map1, col_map2 = st.columns([2, 1])
with col_map1:
    fig_map, ax_map = plt.subplots(figsize=(10, 6))
    ax_map.set_xlim(0, 10); ax_map.set_ylim(0, 7); ax_map.axis('off')

    modules_map = [
        (1,6,"Fundamentos\n01-04", "steelblue"),
        (3,6,"Algoritmos\n05, 11-12", "darkorange"),
        (5,6,"Ruido & QEC\n06, 09, 14", "mediumseagreen"),
        (7,6,"Teoría Avanzada\n16, 22, 26", "mediumpurple"),
        (9,6,"Fronteras\n28-30", "crimson"),
        (2,4,"Variacionales\nVQE, QAOA", "steelblue"),
        (4,4,"Hardware Real\nIBM, Qiskit", "darkorange"),
        (6,4,"Surface Codes\n& Trotter", "mediumseagreen"),
        (8,4,"QSVT &\nTensor Nets", "mediumpurple"),
        (1,2,"Topológica\n41", "crimson"),
        (3,2,"Fotónica\n45", "steelblue"),
        (5,2,"Rydberg\n46", "darkorange"),
        (7,2,"qLDPC\n47", "mediumseagreen"),
        (9,2,"QNLP &\nD-Wave 48-49", "mediumpurple"),
    ]

    for x, y, label, color in modules_map:
        box = mpatches.FancyBboxPatch((x-0.7, y-0.45), 1.4, 0.9,
                                      boxstyle="round,pad=0.1", color=color, alpha=0.7)
        ax_map.add_patch(box)
        ax_map.text(x, y, label, ha='center', va='center', fontsize=7,
                   color='white', fontweight='bold')

    arrows = [(1,6,3,6),(3,6,5,6),(5,6,7,6),(7,6,9,6),
              (1,6,2,4),(3,6,4,4),(5,6,6,4),(7,6,8,4),
              (2,4,1,2),(2,4,3,2),(6,4,5,2),(6,4,7,2),(8,4,9,2)]
    for x1,y1,x2,y2 in arrows:
        ax_map.annotate("", xy=(x2,y2), xytext=(x1,y1),
                        arrowprops=dict(arrowstyle="-|>", color='gray', lw=1.5))

    ax_map.set_title("Árbol de módulos del curso", fontsize=13)
    st.pyplot(fig_map); plt.close(fig_map)

with col_map2:
    st.markdown("### 📊 Métricas del curso")
    stats = {
        "📚 Módulos": 49,
        "🔬 Laboratorios": 53,
        "📊 Visualizaciones": 20,
        "✅ Tests pytest": ">200",
        "📄 Páginas docs": ">50",
        "🌍 Idioma": "Español",
    }
    for k, v in stats.items():
        st.metric(k, v)

st.divider()

# ── Links rápidos ─────────────────────────────────────────────────────────────
st.subheader("🔗 Acceso Rápido")
col_l1, col_l2, col_l3, col_l4 = st.columns(4)
with col_l1:
    st.markdown("""
**📐 Fundamentos**
- [Qubits y estados](#)
- [Qiskit básico](#)
- [Algoritmos](#)
""")
with col_l2:
    st.markdown("""
**🛡️ QEC**
- [Surface codes](#)
- [qLDPC (p.19)](#)
- [Trotter](#)
""")
with col_l3:
    st.markdown("""
**🔬 Fronteras**
- [Fotónica (p.17)](#)
- [Rydberg (p.18)](#)
- [Compilador (p.20)](#)
""")
with col_l4:
    st.markdown("""
**🎯 Práctica**
- [Ejercicios básicos](#)
- [Certificación](#)
- [Hardware real](#)
""")

st.caption("⚛️ Computación Cuántica — Teoría y Práctica | github.com/LegalIntermediaSL/ComputacionCuantica")
