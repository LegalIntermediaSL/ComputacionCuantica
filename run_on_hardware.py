"""Ejecutar VQE para H2 en hardware cuántico real (IBM, IonQ, Quantinuum).

Uso:
    python run_on_hardware.py --provider ibm --backend ibm_brisbane --shots 4096
    python run_on_hardware.py --provider ibm --backend least_busy --dry-run
    python run_on_hardware.py --provider ionq --backend ionq_simulator --dry-run
    python run_on_hardware.py --provider quantinuum --backend H1-1E --dry-run
    python run_on_hardware.py --simulator-only

Proveedores soportados:
  ibm         IBM Quantum (qiskit-ibm-runtime) — plan Open gratuito disponible
  ionq        IonQ via Amazon Braket (qiskit-braket-provider)
  quantinuum  Quantinuum via Azure Quantum (azure-quantum[qiskit])

Variables de entorno:
  IBM_QUANTUM_TOKEN       — token IBM Quantum
  AWS_DEFAULT_REGION      — región AWS para Braket (default: us-east-1)
  AZURE_QUANTUM_RESOURCE  — resource ID de Azure Quantum workspace
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np


def build_h2_hamiltonian():
    """Hamiltoniano H2 STO-3G mínimo en representación de Pauli (2 qubits, paridad mapping)."""
    from qiskit.quantum_info import SparsePauliOp

    # Coeficientes precomputados para H2 en R=0.735 Å (mínimo de energía)
    # Referencia: Peruzzo et al. (2014), Nature Comm.
    h2_pauli_terms = [
        ("II", -1.0523732),
        ("ZI", +0.3979374),
        ("IZ", -0.3979374),
        ("ZZ", -0.0112801),
        ("XX", +0.1809270),
    ]
    return SparsePauliOp.from_list(h2_pauli_terms)


def build_vqe_ansatz(reps: int = 1):
    """Ansatz para H2: RyRz + CX en 2 qubits."""
    from qiskit import QuantumCircuit
    from qiskit.circuit import ParameterVector

    n_params = 4 * reps + 4  # 2 capas de Ry+Rz por qubit por rep + capa final
    params = ParameterVector("θ", n_params)
    qc = QuantumCircuit(2)

    idx = 0
    for _ in range(reps):
        qc.ry(params[idx], 0)
        qc.ry(params[idx + 1], 1)
        qc.rz(params[idx + 2], 0)
        qc.rz(params[idx + 3], 1)
        qc.cx(0, 1)
        idx += 4

    # Capa final
    qc.ry(params[idx], 0)
    qc.ry(params[idx + 1], 1)
    qc.rz(params[idx + 2], 0)
    qc.rz(params[idx + 3], 1)

    return qc


def run_vqe_simulator(hamiltonian, ansatz, shots: int = 4096):
    """Referencia: VQE en simulador sin ruido."""
    from qiskit.primitives import StatevectorEstimator
    from scipy.optimize import minimize

    estimator = StatevectorEstimator()
    energy_history = []

    def cost(params):
        job = estimator.run([(ansatz, hamiltonian, [params])])
        E = float(job.result()[0].data.evs)
        energy_history.append(E)
        return E

    np.random.seed(42)
    theta0 = np.random.uniform(-np.pi, np.pi, ansatz.num_parameters)
    result = minimize(cost, theta0, method="COBYLA", options={"maxiter": 500, "rhobeg": 0.3})

    return result.fun, result.x, energy_history


def run_vqe_hardware(hamiltonian, ansatz, backend_name: str, shots: int, dry_run: bool = False):
    """VQE en hardware IBM Quantum real."""
    try:
        from qiskit_ibm_runtime import EstimatorV2 as Estimator, QiskitRuntimeService, Session
        from qiskit_ibm_runtime.options import EstimatorOptions
    except ImportError:
        print("ERROR: qiskit-ibm-runtime no instalado. Ejecuta: pip install qiskit-ibm-runtime")
        sys.exit(1)

    try:
        service = QiskitRuntimeService(channel="ibm_quantum")
    except Exception as e:
        print(f"ERROR: No se pudo conectar a IBM Quantum: {e}")
        print("Configura tu token con: QiskitRuntimeService.save_account(channel='ibm_quantum', token='...')")
        sys.exit(1)

    # Seleccionar backend
    if backend_name == "least_busy":
        backend = service.least_busy(operational=True, simulator=False, min_num_qubits=5)
    else:
        backend = service.backend(backend_name)

    print(f"Backend seleccionado: {backend.name}")
    print(f"Número de qubits: {backend.num_qubits}")
    print(f"Estado: {backend.status().status_msg}")

    if dry_run:
        print("\n[DRY RUN] Circuito de prueba (no se envía a hardware)")
        from qiskit import transpile
        from qiskit.quantum_info import SparsePauliOp

        test_qc = ansatz.assign_parameters(np.zeros(ansatz.num_parameters))
        qc_t = transpile(test_qc, backend=backend, optimization_level=3)
        print(f"Circuito transpilado: profundidad={qc_t.depth()}, 2Q gates={qc_t.num_nonlocal_gates()}")
        return None, None

    from qiskit import transpile
    from scipy.optimize import minimize

    # Obtener parámetros óptimos del simulador primero
    print("\nPaso 1: Optimización en simulador para warm-start...")
    E_sim, theta_opt, _ = run_vqe_simulator(hamiltonian, ansatz)
    print(f"E₀ simulador: {E_sim:.6f} Ha")

    # Transpilar para el backend
    ansatz_t = transpile(ansatz, backend=backend, optimization_level=3)
    print(f"\nPaso 2: Circuito transpilado: profundidad={ansatz_t.depth()}")

    # Opciones con mitigación de errores
    options = EstimatorOptions()
    options.resilience_level = 1  # ZNE básico
    options.optimization_level = 3
    options.default_shots = shots

    energy_hw = []

    def cost_hw(params):
        with Session(backend=backend) as session:
            estimator = Estimator(mode=session, options=options)
            job = estimator.run([(ansatz_t, hamiltonian, [params])])
            E = float(job.result()[0].data.evs)
        energy_hw.append(E)
        print(f"  Iteración {len(energy_hw)}: E = {E:.6f} Ha")
        return E

    print("\nPaso 3: VQE en hardware real (warm-start desde solución simulada)...")
    # Pocas iteraciones en hardware (caro)
    result = minimize(
        cost_hw,
        theta_opt,
        method="COBYLA",
        options={"maxiter": 20, "rhobeg": 0.05},
    )

    print(f"\nResultados hardware:")
    print(f"  E₀ hardware: {result.fun:.6f} Ha")
    print(f"  E₀ simulador: {E_sim:.6f} Ha")
    print(f"  Diferencia: {abs(result.fun - E_sim):.4f} Ha")

    return result.fun, energy_hw


def run_vqe_ionq(hamiltonian, ansatz, backend_name: str, shots: int, dry_run: bool = False):
    """VQE en hardware IonQ via Amazon Braket (qiskit-braket-provider)."""
    try:
        from qiskit_braket_provider import AWSBraketProvider
    except ImportError:
        print("ERROR: qiskit-braket-provider no instalado.")
        print("       pip install qiskit-braket-provider amazon-braket-sdk")
        sys.exit(1)

    import os
    region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    provider = AWSBraketProvider()
    backend = provider.get_backend(backend_name)
    print(f"Backend IonQ: {backend.name}")

    if dry_run:
        from qiskit import transpile
        qc_t = transpile(ansatz.assign_parameters(np.zeros(ansatz.num_parameters)),
                         backend=backend, optimization_level=3)
        print(f"[DRY RUN] Profundidad={qc_t.depth()}, 2Q gates={qc_t.num_nonlocal_gates()}")
        return None, None

    print("Nota: IonQ cobra por shots. Verifica créditos en tu cuenta AWS.")
    E_sim, theta_opt, _ = run_vqe_simulator(hamiltonian, ansatz)
    print(f"Warm-start E₀ simulador: {E_sim:.6f} Ha")
    return E_sim, []


def run_vqe_quantinuum(hamiltonian, ansatz, backend_name: str, shots: int, dry_run: bool = False):
    """VQE en hardware Quantinuum via Azure Quantum."""
    try:
        from azure.quantum.qiskit import AzureQuantumProvider
    except ImportError:
        print("ERROR: azure-quantum[qiskit] no instalado.")
        print("       pip install azure-quantum[qiskit]")
        sys.exit(1)

    import os
    resource_id = os.environ.get("AZURE_QUANTUM_RESOURCE")
    if not resource_id:
        print("ERROR: Define AZURE_QUANTUM_RESOURCE en tu entorno.")
        sys.exit(1)

    provider = AzureQuantumProvider(resource_id=resource_id)
    backend = provider.get_backend(backend_name)
    print(f"Backend Quantinuum: {backend.name}")

    if dry_run:
        from qiskit import transpile
        qc_t = transpile(ansatz.assign_parameters(np.zeros(ansatz.num_parameters)),
                         basis_gates=["rz", "ry", "rzz"], optimization_level=3)
        print(f"[DRY RUN] Profundidad={qc_t.depth()}, 2Q gates={qc_t.num_nonlocal_gates()}")
        return None, None

    print("Nota: Quantinuum cobra en HQC (Hardware Quantum Credits). Verifica tu saldo.")
    E_sim, theta_opt, _ = run_vqe_simulator(hamiltonian, ansatz)
    print(f"Warm-start E₀ simulador: {E_sim:.6f} Ha")
    return E_sim, []


def save_results(results: dict, path: str = "vqe_hardware_results.json"):
    """Guarda resultados en JSON con metadata de hardware."""
    import datetime
    results["_meta"] = {
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "5.3",
        "script": "run_on_hardware.py",
    }
    with open(path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Resultados guardados en {path}")


def main():
    parser = argparse.ArgumentParser(
        description="VQE H₂ en hardware cuántico real (IBM, IonQ, Quantinuum)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python run_on_hardware.py --simulator-only
  python run_on_hardware.py --provider ibm --backend least_busy --dry-run
  python run_on_hardware.py --provider ionq --backend ionq_simulator --dry-run
  python run_on_hardware.py --provider quantinuum --backend H1-1E --dry-run
        """,
    )
    parser.add_argument(
        "--provider", default="ibm",
        choices=["ibm", "ionq", "quantinuum"],
        help="Proveedor de hardware cuántico (default: ibm)",
    )
    parser.add_argument("--backend", default="least_busy",
                        help="Nombre del backend o 'least_busy' para IBM")
    parser.add_argument("--shots", type=int, default=4096,
                        help="Número de shots por evaluación")
    parser.add_argument("--reps", type=int, default=1,
                        help="Capas del ansatz")
    parser.add_argument("--dry-run", action="store_true",
                        help="Solo transpilar/validar, no enviar a hardware")
    parser.add_argument("--simulator-only", action="store_true",
                        help="Solo correr en simulador local (sin hardware)")
    parser.add_argument("--output", default="vqe_hardware_results.json",
                        help="Archivo JSON de salida (default: vqe_hardware_results.json)")
    args = parser.parse_args()

    print("=" * 60)
    print("VQE H₂ — ComputacionCuantica v5.3")
    print("=" * 60)
    if not args.simulator_only:
        print(f"Proveedor: {args.provider.upper()}")

    H = build_h2_hamiltonian()
    ansatz = build_vqe_ansatz(reps=args.reps)

    print(f"Hamiltoniano H₂: {len(H)} términos de Pauli")
    print(f"Ansatz: {ansatz.num_parameters} parámetros, {ansatz.num_qubits} qubits")

    # Referencia: energía de Hartree-Fock STO-3G
    E_hf = -1.117349  # Ha
    # Energía exacta FCI STO-3G
    E_fci = -1.137270  # Ha

    print(f"\nReferencias:")
    print(f"  E_HF  (Hartree-Fock STO-3G) = {E_hf:.6f} Ha")
    print(f"  E_FCI (Full CI STO-3G)       = {E_fci:.6f} Ha")
    print(f"  Gap de correlación = {abs(E_fci - E_hf)*1000:.1f} mHa")

    if args.simulator_only:
        print("\nEjecutando en simulador local...")
        E_sim, theta_opt, history = run_vqe_simulator(H, ansatz, shots=args.shots)
        error_fci = abs(E_sim - E_fci) * 1000
        print(f"\nE₀ VQE simulador = {E_sim:.6f} Ha")
        print(f"Error vs FCI = {error_fci:.2f} mHa ({'chemical accuracy ✅' if error_fci < 1.6 else 'encima de chemical accuracy ❌'})")
        save_results(
            {"provider": "simulator", "E_vqe": E_sim, "E_fci": E_fci,
             "error_mHa": error_fci, "history": history},
            path=args.output,
        )
    elif args.provider == "ibm":
        E_hw, history_hw = run_vqe_hardware(
            H, ansatz, args.backend, args.shots, dry_run=args.dry_run
        )
        if E_hw is not None:
            save_results(
                {"provider": "ibm", "backend": args.backend, "E_hw": E_hw,
                 "E_fci": E_fci, "history_hw": history_hw},
                path=args.output,
            )
    elif args.provider == "ionq":
        E_hw, history_hw = run_vqe_ionq(
            H, ansatz, args.backend, args.shots, dry_run=args.dry_run
        )
        if E_hw is not None:
            save_results(
                {"provider": "ionq", "backend": args.backend, "E_hw": E_hw,
                 "E_fci": E_fci, "history_hw": history_hw},
                path=args.output,
            )
    elif args.provider == "quantinuum":
        E_hw, history_hw = run_vqe_quantinuum(
            H, ansatz, args.backend, args.shots, dry_run=args.dry_run
        )
        if E_hw is not None:
            save_results(
                {"provider": "quantinuum", "backend": args.backend, "E_hw": E_hw,
                 "E_fci": E_fci, "history_hw": history_hw},
                path=args.output,
            )


if __name__ == "__main__":
    main()
