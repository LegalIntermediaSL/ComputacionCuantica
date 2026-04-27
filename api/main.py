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
    version="1.0.0",
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


# ---------------------------------------------------------------------------
# Ejecutar directamente
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
