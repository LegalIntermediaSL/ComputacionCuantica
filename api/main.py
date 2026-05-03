"""API REST de Computación Cuántica — FastAPI.

Endpoints:
    POST /run-circuit  — Ejecuta un circuito Qiskit desde QASM3
    POST /run-vqe      — Ejecuta VQE para H₂ con parámetros dados
    POST /run-grover   — Ejecuta Grover para N elementos y k marcados

Instalación:
    pip install fastapi uvicorn qiskit qiskit-aer

Ejecutar:
    uvicorn api.main:app --reload --port 8000

Docker:
    docker-compose up
"""

from __future__ import annotations

import time
from typing import Any

import numpy as np

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel, Field
except ImportError as e:
    raise ImportError("Instala FastAPI: pip install fastapi uvicorn") from e

try:
    from qiskit import QuantumCircuit
    from qiskit.circuit import ParameterVector
    from qiskit.quantum_info import SparsePauliOp, Statevector
    from qiskit.primitives import StatevectorEstimator, StatevectorSampler
    from qiskit_aer import AerSimulator
    from qiskit_aer.noise import NoiseModel, depolarizing_error
    from scipy.optimize import minimize
except ImportError as e:
    raise ImportError("Instala Qiskit y Aer: pip install qiskit qiskit-aer scipy") from e


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(
    title="ComputacionCuantica API",
    description="API para ejecutar circuitos y algoritmos cuánticos educativos",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Modelos de request/response
# ---------------------------------------------------------------------------
class CircuitRequest(BaseModel):
    qasm: str = Field(..., description="Código QASM 2.0 del circuito")
    shots: int = Field(1024, ge=1, le=100_000, description="Número de shots")
    noise_p: float = Field(0.0, ge=0.0, le=0.5, description="Error depolarizante por puerta (0=ideal)")


class CircuitResponse(BaseModel):
    counts: dict[str, int]
    shots: int
    elapsed_ms: float
    depth: int
    n_qubits: int


class VQERequest(BaseModel):
    distance_angstrom: float = Field(0.735, ge=0.3, le=3.0, description="Distancia H-H en Ångström")
    max_iter: int = Field(300, ge=10, le=2000, description="Iteraciones máximas del optimizador")
    shots: int = Field(4096, ge=100, le=100_000)


class VQEResponse(BaseModel):
    energy_hartree: float
    energy_ev: float
    iterations: int
    converged: bool
    elapsed_ms: float


class GroverRequest(BaseModel):
    n_qubits: int = Field(3, ge=2, le=10, description="Qubits del espacio de búsqueda")
    marked_states: list[int] = Field([5], description="Estados marcados (enteros)")
    shots: int = Field(2048, ge=100, le=100_000)


class GroverResponse(BaseModel):
    counts: dict[str, int]
    marked_states: list[int]
    optimal_iterations: int
    n_elements: int
    shots: int
    elapsed_ms: float


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": "ComputacionCuantica API",
        "version": "1.0.0",
        "docs": "/docs",
        "github": "https://github.com/LegalIntermediaSL/ComputacionCuantica",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/status")
def status() -> dict[str, Any]:
    """Estado del servicio: versión, métricas del curso y disponibilidad."""
    return {
        "version": "2.0.0",
        "status": "ok",
        "curso": {
            "modulos": 49,
            "laboratorios": 53,
            "guiados": 15,
            "paginas_visualizador": 21,
            "tests": 257,
            "resumenes": 20,
            "soluciones_investigacion": 12,
        },
        "endpoints": ["/run-circuit", "/run-vqe", "/run-grover", "/run-qnlp", "/run-qubo", "/status"],
        "github": "https://github.com/LegalIntermediaSL/ComputacionCuantica",
        "streamlit": "https://computacioncuantica-legalintermedia.streamlit.app",
    }


@app.post("/run-circuit", response_model=CircuitResponse)
def run_circuit(req: CircuitRequest) -> CircuitResponse:
    """Ejecuta un circuito desde QASM 2.0 y devuelve el histograma de resultados."""
    t0 = time.perf_counter()

    try:
        qc = QuantumCircuit.from_qasm_str(req.qasm)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"QASM inválido: {e}")

    if qc.num_qubits > 20:
        raise HTTPException(status_code=422, detail="Máximo 20 qubits")

    if qc.num_clbits == 0:
        raise HTTPException(status_code=422, detail="El circuito no tiene mediciones — añade measure")

    # Construir simulador con ruido opcional
    if req.noise_p > 0:
        noise_model = NoiseModel()
        err_1q = depolarizing_error(req.noise_p, 1)
        err_2q = depolarizing_error(req.noise_p * 10, 2)
        noise_model.add_all_qubit_quantum_error(err_1q, ["h", "x", "y", "z", "s", "t", "ry", "rz"])
        noise_model.add_all_qubit_quantum_error(err_2q, ["cx", "cz"])
        sim = AerSimulator(noise_model=noise_model)
    else:
        sim = AerSimulator()

    job = sim.run(qc, shots=req.shots)
    counts = job.result().get_counts()

    elapsed = (time.perf_counter() - t0) * 1000
    return CircuitResponse(
        counts=counts,
        shots=req.shots,
        elapsed_ms=round(elapsed, 2),
        depth=qc.depth(),
        n_qubits=qc.num_qubits,
    )


@app.post("/run-vqe", response_model=VQEResponse)
def run_vqe(req: VQERequest) -> VQEResponse:
    """Ejecuta VQE para la molécula H₂ en la distancia especificada."""
    t0 = time.perf_counter()

    # Hamiltoniano paramétrico según distancia (interpolado en tabla STO-3G)
    # Coeficientes de Peruzzo et al. 2014 para R = 0.735 Å
    # Interpolación lineal simple para otros valores
    scale = req.distance_angstrom / 0.735

    h2_terms = [
        ("II", -1.0523732 / scale),
        ("ZI", +0.3979374 * scale),
        ("IZ", -0.3979374 * scale),
        ("ZZ", -0.0112801),
        ("XX", +0.1809270 / scale),
    ]
    hamiltonian = SparsePauliOp.from_list(h2_terms)

    # Ansatz: 2 qubits, 1 capa
    params = ParameterVector("θ", 8)
    qc = QuantumCircuit(2)
    qc.ry(params[0], 0); qc.ry(params[1], 1)
    qc.rz(params[2], 0); qc.rz(params[3], 1)
    qc.cx(0, 1)
    qc.ry(params[4], 0); qc.ry(params[5], 1)
    qc.rz(params[6], 0); qc.rz(params[7], 1)

    estimator = StatevectorEstimator()
    history: list[float] = []

    def cost(theta):
        job = estimator.run([(qc, hamiltonian, [theta])])
        E = float(job.result()[0].data.evs)
        history.append(E)
        return E

    np.random.seed(42)
    theta0 = np.random.uniform(-np.pi, np.pi, 8)
    result = minimize(cost, theta0, method="COBYLA", options={"maxiter": req.max_iter, "rhobeg": 0.3})

    elapsed = (time.perf_counter() - t0) * 1000
    hartree_to_ev = 27.2114
    return VQEResponse(
        energy_hartree=round(float(result.fun), 8),
        energy_ev=round(float(result.fun) * hartree_to_ev, 6),
        iterations=len(history),
        converged=result.success,
        elapsed_ms=round(elapsed, 2),
    )


@app.post("/run-grover", response_model=GroverResponse)
def run_grover(req: GroverRequest) -> GroverResponse:
    """Ejecuta el algoritmo de Grover para encontrar estados marcados."""
    t0 = time.perf_counter()

    n = req.n_qubits
    N = 2**n
    k = len(req.marked_states)

    for s in req.marked_states:
        if s < 0 or s >= N:
            raise HTTPException(status_code=422, detail=f"Estado {s} fuera de rango [0, {N-1}]")
    if k == 0:
        raise HTTPException(status_code=422, detail="Debe haber al menos 1 estado marcado")

    # Número óptimo de iteraciones
    optimal_iter = max(1, round(np.pi / 4 * np.sqrt(N / k)))

    def oracle_for_states(marked: list[int]) -> QuantumCircuit:
        """Oráculo que marca los estados dados con fase -1."""
        qc = QuantumCircuit(n)
        for state in marked:
            bits = format(state, f"0{n}b")
            # Aplicar X en qubits donde el bit es 0
            for i, bit in enumerate(reversed(bits)):
                if bit == "0":
                    qc.x(i)
            # Multi-controlled Z
            if n == 1:
                qc.z(0)
            elif n == 2:
                qc.cz(0, 1)
            else:
                qc.h(n - 1)
                qc.mcx(list(range(n - 1)), n - 1)
                qc.h(n - 1)
            # Deshacer X
            for i, bit in enumerate(reversed(bits)):
                if bit == "0":
                    qc.x(i)
        return qc

    def diffuser(n_q: int) -> QuantumCircuit:
        """Operador de difusión de Grover."""
        qc = QuantumCircuit(n_q)
        qc.h(range(n_q))
        qc.x(range(n_q))
        qc.h(n_q - 1)
        qc.mcx(list(range(n_q - 1)), n_q - 1)
        qc.h(n_q - 1)
        qc.x(range(n_q))
        qc.h(range(n_q))
        return qc

    # Construir circuito de Grover
    qc = QuantumCircuit(n, n)
    qc.h(range(n))  # superposición uniforme

    oracle = oracle_for_states(req.marked_states)
    diff = diffuser(n)

    for _ in range(optimal_iter):
        qc.compose(oracle, inplace=True)
        qc.compose(diff, inplace=True)

    qc.measure(range(n), range(n))

    sim = AerSimulator()
    job = sim.run(qc, shots=req.shots)
    counts = dict(job.result().get_counts())

    elapsed = (time.perf_counter() - t0) * 1000
    return GroverResponse(
        counts=counts,
        marked_states=req.marked_states,
        optimal_iterations=optimal_iter,
        n_elements=N,
        shots=req.shots,
        elapsed_ms=round(elapsed, 2),
    )


class QNLPRequest(BaseModel):
    sentence: str = Field(..., description="Frase en inglés (sujeto verbo objeto, max 10 palabras)")
    label: str | None = Field(None, description="Etiqueta esperada para calcular accuracy (opcional)")


class QNLPResponse(BaseModel):
    sentence: str
    prediction: str
    confidence: float
    circuit_params: int
    elapsed_ms: float


class QUBORequest(BaseModel):
    nodes: int = Field(6, ge=2, le=15, description="Número de nodos del grafo")
    edges: list[list[int]] = Field(
        [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [0, 3]],
        description="Aristas del grafo como pares [i, j]",
    )
    method: str = Field("annealing", description="Método: 'annealing' o 'brute_force'")


class QUBOResponse(BaseModel):
    partition: list[int]
    cut_value: int
    max_possible_cut: int
    qubo_energy: float
    method: str
    elapsed_ms: float


@app.post("/run-qnlp", response_model=QNLPResponse)
def run_qnlp(req: QNLPRequest) -> QNLPResponse:
    """Clasifica una frase simple con un circuito IQP cuántico (DisCoCat simplificado).

    Implementación sin lambeq: circuito IQP manual con 4 qubits para SVO (sujeto-verbo-objeto).
    Clasificación basada en paridad del primer qubit al medir.
    """
    t0 = time.perf_counter()

    words = req.sentence.lower().split()
    if len(words) < 2:
        raise HTTPException(status_code=422, detail="La frase debe tener al menos 2 palabras")
    if len(words) > 10:
        raise HTTPException(status_code=422, detail="Máximo 10 palabras")

    # Codificación: cada palabra contribuye un ángulo derivado de su hash
    def word_angle(word: str) -> float:
        h = sum(ord(c) * (i + 1) for i, c in enumerate(word))
        return (h % 628) / 100.0  # ángulo en [0, 2π)

    n_qubits = min(len(words), 4)
    angles = [word_angle(w) for w in words[:n_qubits]]

    # Circuito IQP: H · Rz(θ) · H en cada qubit, con CZ entre pares
    qc = QuantumCircuit(n_qubits, 1)
    qc.h(range(n_qubits))
    for i, ang in enumerate(angles):
        qc.rz(ang, i)
    for i in range(n_qubits - 1):
        qc.cz(i, i + 1)
    qc.h(range(n_qubits))
    qc.measure(0, 0)  # clasificación: bit 0

    sim = AerSimulator()
    job = sim.run(qc, shots=512)
    counts = job.result().get_counts()

    p1 = counts.get("1", 0) / 512
    prediction = "positivo" if p1 >= 0.5 else "negativo"
    confidence = p1 if p1 >= 0.5 else 1 - p1

    elapsed = (time.perf_counter() - t0) * 1000
    return QNLPResponse(
        sentence=req.sentence,
        prediction=prediction,
        confidence=round(confidence, 4),
        circuit_params=n_qubits,
        elapsed_ms=round(elapsed, 2),
    )


@app.post("/run-qubo", response_model=QUBOResponse)
def run_qubo(req: QUBORequest) -> QUBOResponse:
    """Resuelve MAX-CUT como QUBO por simulated annealing o fuerza bruta."""
    t0 = time.perf_counter()

    n = req.nodes
    edges = [(e[0], e[1]) for e in req.edges if len(e) == 2 and 0 <= e[0] < n and 0 <= e[1] < n]
    if not edges:
        raise HTTPException(status_code=422, detail="No hay aristas válidas")

    # Construir matriz Q para MAX-CUT
    Q = np.zeros((n, n))
    for i, j in edges:
        Q[i, i] += 1.0
        Q[j, j] += 1.0
        Q[i, j] -= 1.0
        Q[j, i] -= 1.0
    Q /= 2.0

    def qubo_energy(x: np.ndarray) -> float:
        return float(x @ Q @ x)

    def cut_value(x: list[int]) -> int:
        return sum(1 for i, j in edges if x[i] != x[j])

    best_x: list[int] = []
    best_cut = 0
    best_energy = np.inf

    if req.method == "brute_force" and n <= 15:
        from itertools import product as iproduct
        for bits in iproduct([0, 1], repeat=n):
            x = np.array(bits, dtype=float)
            e = qubo_energy(x)
            c = cut_value(list(bits))
            if c > best_cut or (c == best_cut and e < best_energy):
                best_cut, best_energy, best_x = c, e, list(bits)
    else:
        # Simulated annealing
        x = np.random.randint(0, 2, n).astype(float)
        E = qubo_energy(x)
        best_x = x.astype(int).tolist()
        best_energy, best_cut = E, cut_value(best_x)
        T_start, T_end, steps = 2.0, 0.01, 5000
        for step in range(steps):
            T = T_start * (T_end / T_start) ** (step / steps)
            idx = np.random.randint(n)
            x_new = x.copy()
            x_new[idx] = 1 - x_new[idx]
            E_new = qubo_energy(x_new)
            dE = E_new - E
            if dE < 0 or np.random.rand() < np.exp(-dE / T):
                x, E = x_new, E_new
            c = cut_value(x.astype(int).tolist())
            if c > best_cut or (c == best_cut and E < best_energy):
                best_cut, best_energy, best_x = c, E, x.astype(int).tolist()

    # Cota superior del corte
    max_possible = len(edges)

    elapsed = (time.perf_counter() - t0) * 1000
    return QUBOResponse(
        partition=best_x,
        cut_value=best_cut,
        max_possible_cut=max_possible,
        qubo_energy=round(best_energy, 6),
        method=req.method,
        elapsed_ms=round(elapsed, 2),
    )


# ---------------------------------------------------------------------------
# Ejecutar directamente
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
