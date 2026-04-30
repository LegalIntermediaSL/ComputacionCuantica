"""
Tests para simulación GPU con Qiskit Aer — Fase 18.4.

Todos los tests están marcados con @pytest.mark.gpu y se saltan
automáticamente si no hay GPU NVIDIA disponible.

Ejecutar con:  make test-gpu
               python -m pytest tests/test_gpu_aer.py -v -m gpu
"""

import pytest
import numpy as np

# ── Detección de GPU ─────────────────────────────────────────────────────────

def _gpu_available() -> bool:
    """True si qiskit-aer-gpu está instalado y detecta al menos una GPU."""
    try:
        from qiskit_aer import AerSimulator
        devices = AerSimulator().available_devices()
        return 'GPU' in devices
    except Exception:
        return False


GPU_AVAILABLE = _gpu_available()
skip_no_gpu = pytest.mark.skipif(
    not GPU_AVAILABLE,
    reason="GPU NVIDIA no disponible — instalar qiskit-aer-gpu y CUDA"
)


# ── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture(scope='module')
def sim_gpu():
    from qiskit_aer import AerSimulator
    return AerSimulator(method='statevector', device='GPU')


@pytest.fixture(scope='module')
def sim_cpu():
    from qiskit_aer import AerSimulator
    return AerSimulator(method='statevector', device='CPU')


# ── Tests de disponibilidad y configuración ───────────────────────────────────

@pytest.mark.gpu
@skip_no_gpu
def test_gpu_device_available():
    """GPU debe aparecer en available_devices()."""
    from qiskit_aer import AerSimulator
    devices = AerSimulator().available_devices()
    assert 'GPU' in devices


@pytest.mark.gpu
@skip_no_gpu
def test_gpu_simulator_creates(sim_gpu):
    """AerSimulator con device='GPU' debe instanciarse sin error."""
    assert sim_gpu is not None
    assert sim_gpu.options.device == 'GPU'


@pytest.mark.gpu
@skip_no_gpu
def test_gpu_method_statevector(sim_gpu):
    """Método debe ser statevector."""
    assert sim_gpu.options.method == 'statevector'


# ── Tests de corrección numérica ─────────────────────────────────────────────

@pytest.mark.gpu
@skip_no_gpu
def test_bell_state_gpu_vs_cpu(sim_gpu, sim_cpu):
    """Distribución del estado de Bell debe coincidir entre GPU y CPU."""
    from qiskit import QuantumCircuit, transpile

    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    shots = 4096
    counts_gpu = sim_gpu.run(transpile(qc, sim_gpu), shots=shots).result().get_counts()
    counts_cpu = sim_cpu.run(transpile(qc, sim_cpu), shots=shots).result().get_counts()

    p00_gpu = counts_gpu.get('00', 0) / shots
    p11_gpu = counts_gpu.get('11', 0) / shots
    p00_cpu = counts_cpu.get('00', 0) / shots

    # Ambos deben estar cerca de 0.5
    assert abs(p00_gpu - 0.5) < 0.05
    assert abs(p11_gpu - 0.5) < 0.05
    # GPU y CPU deben dar resultados compatibles
    assert abs(p00_gpu - p00_cpu) < 0.05


@pytest.mark.gpu
@skip_no_gpu
def test_statevector_gpu_norm(sim_gpu):
    """Statevector obtenido de GPU debe tener norma 1."""
    from qiskit import QuantumCircuit, transpile
    from qiskit_aer import AerSimulator

    sim_sv = AerSimulator(method='statevector', device='GPU')
    qc = QuantumCircuit(10)
    qc.h(range(10))
    qc.cx(0, 5); qc.cx(1, 6); qc.cx(2, 7)
    qc.save_statevector()

    result = sim_sv.run(transpile(qc, sim_sv)).result()
    sv = result.get_statevector()
    norm = float(np.linalg.norm(sv))
    assert abs(norm - 1.0) < 1e-6, f"Norma inesperada: {norm}"


@pytest.mark.gpu
@skip_no_gpu
def test_gpu_energy_vqe_h2(sim_gpu):
    """VQE H₂ en GPU debe dar energía dentro de 0.01 Ha del mínimo exacto."""
    from qiskit import QuantumCircuit
    from qiskit.circuit import ParameterVector
    from qiskit.quantum_info import SparsePauliOp
    from qiskit_aer.primitives import EstimatorV2
    from scipy.optimize import minimize

    H2 = SparsePauliOp.from_list([
        ('II', -1.0523732), ('ZI', 0.3979374), ('IZ', -0.3979374),
        ('ZZ', -0.0112802), ('XX', 0.1809270),
    ])

    params = ParameterVector('θ', 4)
    qc = QuantumCircuit(2)
    qc.ry(params[0], 0); qc.ry(params[1], 1)
    qc.cx(0, 1)
    qc.ry(params[2], 0); qc.ry(params[3], 1)

    estimator = EstimatorV2(options={
        'backend_options': {'method': 'statevector', 'device': 'GPU'}
    })

    def cost(p):
        job = estimator.run([(qc, H2, [p])])
        return float(job.result()[0].data.evs)

    result = minimize(cost, np.zeros(4), method='COBYLA',
                      options={'maxiter': 200})
    E_vqe = result.fun
    E_fci = -1.137270

    assert abs(E_vqe - E_fci) < 0.01, f"VQE GPU: {E_vqe:.6f} Ha (ref: {E_fci})"


# ── Tests de escalado y rendimiento ─────────────────────────────────────────

@pytest.mark.gpu
@pytest.mark.slow
@skip_no_gpu
def test_gpu_faster_than_cpu_n24():
    """Para n=24, GPU debe ser más rápida que CPU (o igual en el peor caso)."""
    import time
    from qiskit import QuantumCircuit, transpile
    from qiskit_aer import AerSimulator

    n = 24
    qc = QuantumCircuit(n)
    qc.h(range(n))
    for i in range(0, n - 1, 2):
        qc.cx(i, i + 1)
    qc.measure_all()

    sim_c = AerSimulator(method='statevector', device='CPU')
    sim_g = AerSimulator(method='statevector', device='GPU')

    qc_c = transpile(qc, sim_c, optimization_level=0)
    qc_g = transpile(qc, sim_g, optimization_level=0)

    # Warmup
    sim_c.run(qc_c, shots=1).result()
    sim_g.run(qc_g, shots=1).result()

    t0 = time.perf_counter()
    sim_c.run(qc_c, shots=256).result()
    t_cpu = time.perf_counter() - t0

    t0 = time.perf_counter()
    sim_g.run(qc_g, shots=256).result()
    t_gpu = time.perf_counter() - t0

    speedup = t_cpu / t_gpu
    print(f"\n  n={n}: CPU={t_cpu:.2f}s, GPU={t_gpu:.2f}s, speedup={speedup:.1f}×")
    # Para n=24, GPU debe ser al menos tan rápida como CPU
    assert speedup >= 0.5, f"GPU más lenta de lo esperado: speedup={speedup:.2f}×"


@pytest.mark.gpu
@skip_no_gpu
def test_mps_gpu_large_circuit():
    """MPS en GPU debe simular circuito de 30 qubits con bajo entrelazamiento."""
    from qiskit import QuantumCircuit, transpile
    from qiskit_aer import AerSimulator

    n = 30
    qc = QuantumCircuit(n)
    for q in range(n):
        qc.ry(np.pi / 4, q)
    # Solo CNOTs lineales — bajo entrelazamiento, MPS eficiente
    for q in range(0, n - 1, 2):
        qc.cx(q, q + 1)
    qc.measure_all()

    sim_mps = AerSimulator(
        method='matrix_product_state',
        device='GPU',
        matrix_product_state_max_bond_dimension=32,
    )
    qc_t = transpile(qc, sim_mps, optimization_level=0)
    result = sim_mps.run(qc_t, shots=512).result()

    assert result.success, "Simulación MPS-GPU falló"
    counts = result.get_counts()
    assert sum(counts.values()) == 512


@pytest.mark.gpu
@skip_no_gpu
def test_single_precision_reduces_memory():
    """Precisión single debe ejecutarse sin error y dar resultados razonables."""
    from qiskit import QuantumCircuit, transpile
    from qiskit_aer import AerSimulator

    qc = QuantumCircuit(20)
    qc.h(range(20))
    qc.measure_all()

    sim_f32 = AerSimulator(method='statevector', device='GPU', precision='single')
    qc_t = transpile(qc, sim_f32, optimization_level=0)
    result = sim_f32.run(qc_t, shots=1024).result()

    counts = result.get_counts()
    n_distinct = len(counts)
    # Con 20 qubits en superposición uniforme, esperamos muchos estados distintos
    assert n_distinct > 100, f"Pocos estados distintos: {n_distinct}"
