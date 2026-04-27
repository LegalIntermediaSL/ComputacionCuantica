"""Página 15: Quiz de Certificación interactivo con badge SVG."""

import streamlit as st
import math
import random
import xml.etree.ElementTree as ET
from datetime import date

st.set_page_config(page_title="Certificación Cuántica", page_icon="🏆", layout="wide")

st.title("🏆 Certificación en Computación Cuántica")
st.markdown(
    "Quiz adaptativo de 20 preguntas. Responde sin consultar notas para obtener una evaluación honesta."
)

# ---------------------------------------------------------------------------
# Banco de preguntas (subset del examen completo — 20 preguntas representativas)
# ---------------------------------------------------------------------------
QUESTIONS = [
    {
        "id": "B1",
        "module": "01",
        "level": "Básico",
        "text": "Un qubit en superposición |+⟩ = (|0⟩ + |1⟩)/√2 se mide en la base computacional. ¿Cuál es la probabilidad de obtener |1⟩?",
        "options": ["0%", "25%", "50%", "100%"],
        "answer": 2,
        "explanation": "|⟨1|+⟩|² = |1/√2|² = 1/2 = 50%",
    },
    {
        "id": "B2",
        "module": "02",
        "level": "Básico",
        "text": "¿Cuántos qubits tiene el estado de Bell |Φ⁺⟩ = (|00⟩ + |11⟩)/√2?",
        "options": ["1", "2", "3", "4"],
        "answer": 1,
        "explanation": "|Φ⁺⟩ vive en ℂ² ⊗ ℂ² → es un estado de 2 qubits.",
    },
    {
        "id": "B3",
        "module": "02",
        "level": "Básico",
        "text": "La puerta Hadamard actúa como H|0⟩ = ?",
        "options": ["|1⟩", "|+⟩ = (|0⟩+|1⟩)/√2", "|−⟩ = (|0⟩−|1⟩)/√2", "i|1⟩"],
        "answer": 1,
        "explanation": "H = (X + Z)/√2, por lo que H|0⟩ = (|0⟩ + |1⟩)/√2 = |+⟩.",
    },
    {
        "id": "B4",
        "module": "03",
        "level": "Básico",
        "text": "¿Qué puerta convierte |00⟩ en el estado de Bell |Φ⁺⟩?",
        "options": ["X ⊗ X", "H ⊗ I, luego CNOT", "CNOT, luego H ⊗ I", "CZ"],
        "answer": 1,
        "explanation": "H crea superposición en el control, CNOT entrelaza: H|0⟩|0⟩ → |+⟩|0⟩ → (|00⟩+|11⟩)/√2.",
    },
    {
        "id": "B5",
        "module": "05",
        "level": "Básico",
        "text": "El algoritmo de Grover para N elementos requiere aprox. ¿cuántas consultas al oráculo?",
        "options": ["O(N)", "O(√N)", "O(log N)", "O(N²)"],
        "answer": 1,
        "explanation": "Grover usa π√N/4 iteraciones → complejidad O(√N), cuadráticamente mejor que O(N) clásico.",
    },
    {
        "id": "B6",
        "module": "06",
        "level": "Básico",
        "text": "T1 en un qubit superconductor mide:",
        "options": [
            "Tiempo de decoherencia de fase",
            "Tiempo de relajación de energía (|1⟩ → |0⟩)",
            "Tiempo de puerta de dos qubits",
            "Frecuencia de Rabi",
        ],
        "answer": 1,
        "explanation": "T1 es el tiempo de relajación longitudinal: el tiempo medio en que |1⟩ decae a |0⟩.",
    },
    {
        "id": "I1",
        "module": "05",
        "level": "Intermedio",
        "text": "La QFT sobre n qubits requiere un número de puertas de:",
        "options": ["O(n)", "O(n log n)", "O(n²)", "O(2ⁿ)"],
        "answer": 2,
        "explanation": "La QFT usa n niveles de Hadamard + rotaciones controladas: total n(n+1)/2 = O(n²) puertas.",
    },
    {
        "id": "I2",
        "module": "05",
        "level": "Intermedio",
        "text": "En la Estimación de Fase Cuántica (QPE) con t qubits de fase, la precisión es:",
        "options": ["1/t", "1/2ᵗ", "1/√t", "t/2π"],
        "answer": 1,
        "explanation": "QPE resuelve la fase con t bits de precisión → error máximo 2^(-t).",
    },
    {
        "id": "I3",
        "module": "11",
        "level": "Intermedio",
        "text": "El principio variacional de VQE garantiza que:",
        "options": [
            "⟨ψ(θ)|H|ψ(θ)⟩ ≤ E_0",
            "⟨ψ(θ)|H|ψ(θ)⟩ ≥ E_0",
            "⟨ψ(θ)|H|ψ(θ)⟩ = E_0 para cualquier θ",
            "VQE siempre converge al estado fundamental",
        ],
        "answer": 1,
        "explanation": "Por el principio variacional: E[ψ] = ⟨ψ|H|ψ⟩/⟨ψ|ψ⟩ ≥ E_0 para cualquier estado |ψ⟩.",
    },
    {
        "id": "I4",
        "module": "09",
        "level": "Intermedio",
        "text": "El código de Shor de 9 qubits corrige:",
        "options": [
            "Solo errores de bit-flip (X)",
            "Solo errores de fase (Z)",
            "Cualquier error de un qubit",
            "Errores de dos qubits simultáneos",
        ],
        "answer": 2,
        "explanation": "El código de Shor combina código de repetición de 3 qubits (bit-flip) y código de fase de 3 qubits → corrige X, Z y Y en cualquier qubit.",
    },
    {
        "id": "I5",
        "module": "14",
        "level": "Intermedio",
        "text": "El umbral del surface code es aproximadamente:",
        "options": ["0.1%", "1%", "10%", "50%"],
        "answer": 1,
        "explanation": "El surface code tiene p_th ≈ 1% bajo depolarizing noise. Para p < p_th, la tasa de error lógico decrece con la distancia d.",
    },
    {
        "id": "I6",
        "module": "38",
        "level": "Intermedio",
        "text": "Un estado GHZ de n qubits como sonda de fase alcanza QFI =",
        "options": ["n", "n²", "2n", "√n"],
        "answer": 1,
        "explanation": "Para estado GHZ y generador colectivo Jz: F_Q = n², alcanzando el límite de Heisenberg δφ ≥ 1/n.",
    },
    {
        "id": "I7",
        "module": "07",
        "level": "Intermedio",
        "text": "En ZNE con circuit folding, el factor de escala de ruido λ para k folds es:",
        "options": ["λ = k", "λ = 2k - 1", "λ = 2k + 1", "λ = k²"],
        "answer": 2,
        "explanation": "U → U(U†U)^k implica k folds extra de ida y vuelta. Número total de capas: 1 + 2k, por tanto λ = 2k + 1.",
    },
    {
        "id": "A1",
        "module": "40",
        "level": "Avanzado",
        "text": "QSVT aplica un polinomio de grado d a los valores singulares de A mediante block-encoding. ¿Cuántas consultas a la block-encoding requiere?",
        "options": ["O(1)", "O(d)", "O(d²)", "O(2^d)"],
        "answer": 1,
        "explanation": "QSVT usa exactamente d consultas a la block-encoding (y su conjugado) para implementar un polinomio de grado d de los valores singulares.",
    },
    {
        "id": "A2",
        "module": "11",
        "level": "Avanzado",
        "text": "En un circuito variacional de n qubits con capas Lc, el gradiente satisface aproximadamente:",
        "options": [
            "Var[∂C/∂θ] ∝ 1/n",
            "Var[∂C/∂θ] ∝ 1/√n",
            "Var[∂C/∂θ] ∝ 4^(-n)",
            "Var[∂C/∂θ] ∝ e^(-n)",
        ],
        "answer": 2,
        "explanation": "Los barren plateaus implican que la varianza del gradiente decrece exponencialmente: Var ∝ 4^(-n) para ansätze aleatorios globales.",
    },
    {
        "id": "A3",
        "module": "39",
        "level": "Avanzado",
        "text": "La descomposición KAK garantiza que cualquier unitario de 2 qubits puede implementarse con a lo sumo:",
        "options": ["1 CNOT", "2 CNOT", "3 CNOT", "4 CNOT"],
        "answer": 2,
        "explanation": "El teorema KAK (Cartan decomposition): U(4) = (SU(2)⊗SU(2)) · exp(i∑_k h_k σ_k⊗σ_k) · (SU(2)⊗SU(2)). Siempre ≤3 CNOT.",
    },
    {
        "id": "A4",
        "module": "29",
        "level": "Avanzado",
        "text": "En la destilación de magic states 15→1, la tasa de error de salida es aproximadamente:",
        "options": ["p_out ≈ 15p²", "p_out ≈ 35p³", "p_out ≈ p/15", "p_out ≈ p²"],
        "answer": 1,
        "explanation": "El protocolo 15→1 de Bravyi-Kitaev da p_out ≈ 35p³ para p ≪ 1 (corrección de distancia 3 sobre 15 estados de entrada).",
    },
    {
        "id": "A5",
        "module": "12",
        "level": "Avanzado",
        "text": "Kernel Target Alignment (KTA) para un kernel perfecto (K = yy^T) vale:",
        "options": ["0", "0.5", "1", "n"],
        "answer": 2,
        "explanation": "KTA(K, y) = ⟨K, yy^T⟩_F / (||K||_F · n). Para K = yy^T, numerador = ||yy^T||²_F = n², denominador = n · n = n², luego KTA = 1.",
    },
    {
        "id": "A6",
        "module": "30",
        "level": "Avanzado",
        "text": "El costo clásico de calcular el permanente de una matriz n×n es:",
        "options": ["O(n!)", "O(2ⁿ · n)", "O(n³)", "O(n² log n)"],
        "answer": 1,
        "explanation": "El algoritmo de Ryser calcula el permanente en O(2ⁿ · n) — exponencial en n pero mejor que n! de la definición.",
    },
    {
        "id": "A7",
        "module": "28",
        "level": "Avanzado",
        "text": "XEB (Cross-Entropy Benchmarking) mide la fidelidad como:",
        "options": [
            "F_XEB = ⟨log p_ideal⟩ - ⟨log p_unif⟩",
            "F_XEB = 2ⁿ⟨p_ideal(x)⟩_exp - 1",
            "F_XEB = 1 - TVD(p_ideal, p_exp)",
            "F_XEB = |⟨ψ_ideal|ψ_exp⟩|²",
        ],
        "answer": 1,
        "explanation": "F_XEB = 2ⁿ · E_x[p_ideal(x)] - 1. Para circuito ideal = 1; para ruido total (distribución uniforme) = 0.",
    },
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def badge_svg(name: str, level: str, score: int, total: int, exam_date: str) -> str:
    """Genera un badge SVG parametrizado con nombre, nivel y puntuación."""
    colors = {
        "Investigador": "#6A0DAD",
        "Avanzado": "#1565C0",
        "Intermedio": "#2E7D32",
        "Básico": "#E65100",
    }
    color = colors.get(level, "#555")
    pct = int(100 * score / total)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="340" height="110">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{color};stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#111827;stop-opacity:1"/>
    </linearGradient>
  </defs>
  <rect width="340" height="110" rx="12" fill="url(#grad)"/>
  <text x="20" y="32" font-family="monospace" font-size="22" font-weight="bold" fill="white">⚛ Computación Cuántica</text>
  <text x="20" y="58" font-family="monospace" font-size="16" fill="#E0E0E0">{name}</text>
  <text x="20" y="80" font-family="monospace" font-size="13" fill="#BDBDBD">Nivel: {level}  |  Score: {score}/{total} ({pct}%)</text>
  <text x="20" y="100" font-family="monospace" font-size="11" fill="#9E9E9E">{exam_date}  —  LegalIntermediaSL/ComputacionCuantica</text>
</svg>"""
    return svg


def classify(pct: float) -> tuple[str, str]:
    if pct >= 92:
        return "Investigador", "🏆"
    elif pct >= 75:
        return "Avanzado", "🥇"
    elif pct >= 55:
        return "Intermedio", "🥈"
    else:
        return "Básico", "🥉"


# ---------------------------------------------------------------------------
# Session state init
# ---------------------------------------------------------------------------
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "questions" not in st.session_state:
    st.session_state.questions = []

# ---------------------------------------------------------------------------
# Sidebar — configuración
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configuración")
    user_name = st.text_input("Tu nombre (para el badge)", value="Estudiante")
    n_questions = st.slider("Número de preguntas", 5, len(QUESTIONS), 10)
    level_filter = st.multiselect(
        "Niveles a incluir",
        ["Básico", "Intermedio", "Avanzado"],
        default=["Básico", "Intermedio", "Avanzado"],
    )
    shuffle = st.checkbox("Orden aleatorio", value=True)
    st.markdown("---")
    st.markdown("📖 [Ver banco completo](../Ejercicios/examen_certificacion.md)")
    st.markdown("📋 [Autoevaluación modular](../Ejercicios/autoevaluacion_modular.md)")

# ---------------------------------------------------------------------------
# Start quiz
# ---------------------------------------------------------------------------
if not st.session_state.quiz_started:
    st.markdown("## ¿Listo para certificarte?")
    col1, col2, col3 = st.columns(3)
    col1.metric("Preguntas seleccionadas", n_questions)
    col2.metric("Niveles", ", ".join(level_filter) if level_filter else "Todos")
    col3.metric("Total disponible", len(QUESTIONS))

    if st.button("🚀 Iniciar Quiz", type="primary"):
        pool = [q for q in QUESTIONS if q["level"] in level_filter]
        selected = random.sample(pool, min(n_questions, len(pool)))
        if shuffle:
            random.shuffle(selected)
        st.session_state.questions = selected
        st.session_state.answers = {}
        st.session_state.submitted = False
        st.session_state.quiz_started = True
        st.rerun()

elif not st.session_state.submitted:
    # ---------------------------------------------------------------------------
    # Quiz in progress
    # ---------------------------------------------------------------------------
    questions = st.session_state.questions
    progress = len(st.session_state.answers) / len(questions)
    st.progress(progress, text=f"Respondidas: {len(st.session_state.answers)}/{len(questions)}")

    for i, q in enumerate(questions):
        with st.expander(f"Q{i+1} [{q['level']} | Módulo {q['module']}]  {q['text']}", expanded=True):
            prev = st.session_state.answers.get(q["id"], None)
            prev_idx = prev if prev is not None else None
            choice = st.radio(
                "Selecciona tu respuesta:",
                options=range(len(q["options"])),
                format_func=lambda x, opts=q["options"]: opts[x],
                index=prev_idx,
                key=f"radio_{q['id']}",
            )
            if choice is not None:
                st.session_state.answers[q["id"]] = choice

    st.markdown("---")
    col_submit, col_reset = st.columns([2, 1])
    with col_submit:
        if st.button("✅ Enviar respuestas", type="primary", disabled=len(st.session_state.answers) < len(questions)):
            st.session_state.submitted = True
            st.rerun()
    with col_reset:
        if st.button("🔄 Reiniciar"):
            st.session_state.quiz_started = False
            st.session_state.answers = {}
            st.session_state.submitted = False
            st.rerun()

else:
    # ---------------------------------------------------------------------------
    # Results
    # ---------------------------------------------------------------------------
    questions = st.session_state.questions
    answers = st.session_state.answers

    correct = sum(1 for q in questions if answers.get(q["id"]) == q["answer"])
    total_q = len(questions)
    pct = 100 * correct / total_q
    level, emoji = classify(pct)

    st.markdown(f"## {emoji} Resultado: **{level}**")
    col1, col2, col3 = st.columns(3)
    col1.metric("Correctas", f"{correct}/{total_q}")
    col2.metric("Porcentaje", f"{pct:.1f}%")
    col3.metric("Nivel", level)

    # Desglose por nivel
    st.markdown("### Desglose por nivel")
    for lvl in ["Básico", "Intermedio", "Avanzado"]:
        lvl_qs = [q for q in questions if q["level"] == lvl]
        if lvl_qs:
            lvl_correct = sum(1 for q in lvl_qs if answers.get(q["id"]) == q["answer"])
            st.write(f"**{lvl}:** {lvl_correct}/{len(lvl_qs)}")

    # Revisión detallada
    st.markdown("### Revisión de respuestas")
    for i, q in enumerate(questions):
        user_ans = answers.get(q["id"])
        is_correct = user_ans == q["answer"]
        icon = "✅" if is_correct else "❌"
        with st.expander(f"{icon} Q{i+1} — {q['text'][:60]}..."):
            for j, opt in enumerate(q["options"]):
                if j == q["answer"] and j == user_ans:
                    st.markdown(f"**✅ {opt}** ← Tu respuesta (correcta)")
                elif j == q["answer"]:
                    st.markdown(f"**✅ {opt}** ← Respuesta correcta")
                elif j == user_ans:
                    st.markdown(f"~~❌ {opt}~~ ← Tu respuesta")
                else:
                    st.markdown(f"◻ {opt}")
            st.info(f"**Explicación:** {q['explanation']}")
            st.caption(f"Módulo {q['module']} | {q['level']}")

    # Badge SVG
    st.markdown("### 🏅 Tu Badge de Certificación")
    today = date.today().isoformat()
    svg = badge_svg(user_name, level, correct, total_q, today)
    st.markdown(svg, unsafe_allow_html=True)

    # Download badge
    st.download_button(
        label="⬇️ Descargar Badge (SVG)",
        data=svg.encode("utf-8"),
        file_name=f"badge_cuantica_{user_name.replace(' ', '_')}_{today}.svg",
        mime="image/svg+xml",
    )

    st.markdown("---")
    col_retry, col_home = st.columns(2)
    with col_retry:
        if st.button("🔄 Repetir quiz"):
            st.session_state.quiz_started = False
            st.session_state.submitted = False
            st.session_state.answers = {}
            st.rerun()
    with col_home:
        st.link_button("📚 Volver al tutorial", "https://github.com/LegalIntermediaSL/ComputacionCuantica")
