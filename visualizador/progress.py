"""
Módulo de progreso del estudiante — almacenamiento local con st.session_state.
"""
import streamlit as st
from datetime import datetime

_PROGRESS_KEY = "qc_progress"
_TOTAL_MODULES = 49

MODULES = {
    "01": "Qubits y estados",
    "02": "Qiskit básico",
    "04": "Qiskit Runtime",
    "05": "Algoritmos clásicos",
    "06": "Ruido y hardware",
    "09": "Corrección de errores",
    "11": "Variacionales (VQE/QAOA)",
    "12": "Aplicaciones industria",
    "14": "Surface codes",
    "15": "Evolución Trotter",
    "16": "Canales cuánticos",
    "17": "POVM y medidas",
    "19": "Tomografía",
    "22": "Recursos cuánticos",
    "26": "ZX-Calculus",
    "28": "Aplicaciones emergentes",
    "29": "Fault-Tolerant",
    "30": "Quantum Advantage",
    "38": "Quantum Sensing",
    "39": "Compilación avanzada",
    "40": "QSVT",
    "41": "Topological QC",
    "42": "Tensor Networks",
    "43": "Quantum Gravity",
    "44": "DQC avanzado",
    "45": "Computación Fotónica",
    "46": "Átomos Neutros y Rydberg",
    "47": "qLDPC y Decodificadores",
    "48": "QNLP",
    "49": "D-Wave y Annealing",
}


def _get_progress() -> dict:
    if _PROGRESS_KEY not in st.session_state:
        st.session_state[_PROGRESS_KEY] = {}
    return st.session_state[_PROGRESS_KEY]


def save_progress(module_id: str, score: float, notes: str = "") -> None:
    """Guarda el progreso de un módulo (score 0-100)."""
    progress = _get_progress()
    progress[module_id] = {
        "score": max(0, min(100, score)),
        "completed": score >= 60,
        "date": datetime.now().isoformat(),
        "notes": notes,
    }
    st.session_state[_PROGRESS_KEY] = progress


def load_progress() -> dict:
    """Devuelve el diccionario de progreso completo."""
    return _get_progress()


def get_completion_pct() -> float:
    """Porcentaje de módulos completados (score >= 60)."""
    progress = _get_progress()
    if not MODULES:
        return 0.0
    completed = sum(1 for mid in MODULES if progress.get(mid, {}).get("completed", False))
    return completed / len(MODULES) * 100


def get_next_module() -> str | None:
    """Devuelve el ID del siguiente módulo no completado."""
    progress = _get_progress()
    for mid in sorted(MODULES.keys()):
        if not progress.get(mid, {}).get("completed", False):
            return mid
    return None


def show_progress_widget(compact: bool = False) -> None:
    """Muestra widget de progreso. Llamar desde cualquier página."""
    pct = get_completion_pct()
    next_mod = get_next_module()

    if compact:
        st.progress(pct / 100, text=f"Progreso: {pct:.0f}%")
        if next_mod:
            st.caption(f"Siguiente: Módulo {next_mod} — {MODULES.get(next_mod, '')}")
        return

    st.markdown("### 📊 Tu Progreso")
    st.progress(pct / 100, text=f"{pct:.0f}% completado")

    progress = _get_progress()
    cols = st.columns(5)
    for i, (mid, mname) in enumerate(MODULES.items()):
        entry = progress.get(mid, {})
        score = entry.get("score", 0)
        done = entry.get("completed", False)
        with cols[i % 5]:
            color = "🟢" if done else ("🟡" if score > 0 else "⚪")
            st.markdown(f"{color} **{mid}**  \n{mname[:15]}")

    if next_mod:
        st.info(f"**Siguiente módulo recomendado:** {next_mod} — {MODULES[next_mod]}")
    else:
        st.success("🎉 ¡Has completado todos los módulos!")


def reset_progress() -> None:
    """Reinicia todo el progreso."""
    st.session_state[_PROGRESS_KEY] = {}
