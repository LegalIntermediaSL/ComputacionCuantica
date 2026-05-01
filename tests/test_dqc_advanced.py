"""
Tests para DQC avanzado — Fase 18.

Verifica purificación BBPSSW, tasa de Bell pairs vs distancia,
decay de fidelidad por memoria cuántica y QBER en MDI-QKD.

Cobertura: Módulo 44, Lab 42 (DQC avanzada).
"""

import numpy as np
import pytest


# ── Estado de Werner ──────────────────────────────────────────────────────────

def werner_state(F: float) -> np.ndarray:
    """
    Estado Werner ρ_W(F) = F|Φ+><Φ+| + (1-F)/3 · (I - |Φ+><Φ+|).
    Traza = 1, PSD para F ∈ [0,1], maximamente mezclado para F=1/4.
    """
    phi_plus = np.array([1.0, 0.0, 0.0, 1.0]) / np.sqrt(2)
    rho_bell = np.outer(phi_plus, phi_plus)
    return F * rho_bell + (1.0 - F) / 3.0 * (np.eye(4) - rho_bell)


def fidelity_werner(rho: np.ndarray) -> float:
    """Calcula F = <Φ+|ρ|Φ+>."""
    phi_plus = np.array([1.0, 0.0, 0.0, 1.0]) / np.sqrt(2)
    return float(phi_plus @ rho @ phi_plus)


# ── Purificación BBPSSW ───────────────────────────────────────────────────────

def bbpssw_round(F: float) -> tuple[float, float]:
    """
    Un paso de purificación BBPSSW (Bennett et al. 1996).
    Retorna (F_nueva, P_éxito).
    """
    F2 = F * F + ((1 - F) / 3) ** 2
    P = F2 + 2 * F * (1 - F) / 3 + 2 * ((1 - F) / 3) ** 2
    # Fórmula correcta BBPSSW:
    # F' = (F² + ((1-F)/3)²) / P_éxito
    # P_éxito = F² + 2F(1-F)/3 + 5((1-F)/3)²
    num = F ** 2 + ((1 - F) / 3) ** 2
    denom = F ** 2 + (2 * F * (1 - F) / 3) + (5 * ((1 - F) / 3) ** 2)
    F_new = num / denom
    return F_new, denom


def bbpssw_iterate(F0: float, rounds: int) -> list[float]:
    """Aplica BBPSSW iterativamente, retorna historial de fidelidades."""
    history = [F0]
    F = F0
    for _ in range(rounds):
        if F >= 1.0:
            break
        F, _ = bbpssw_round(F)
        history.append(F)
    return history


# ── Tasa Bell pairs vs distancia ──────────────────────────────────────────────

def bell_pair_rate(distance_km: float, attenuation_db_per_km: float = 0.2) -> float:
    """Tasa de generación de Bell pairs via fibra óptica: η = 10^(-α·L/10)."""
    return 10 ** (-attenuation_db_per_km * distance_km / 10)


# ── Fidelidad con decay de memoria cuántica ───────────────────────────────────

def memory_fidelity(F0: float, t: float, T_mem: float) -> float:
    """
    Fidelidad de un Bell pair almacenado durante tiempo t.
    Modelo simple: F(t) = F0 · exp(-t/T_mem) + (1/4)(1 - exp(-t/T_mem)).
    """
    decay = np.exp(-t / T_mem)
    return F0 * decay + (1 / 4) * (1 - decay)


# ── BB84 / MDI-QKD ───────────────────────────────────────────────────────────

def simulate_bb84_qber(n_bits: int, eve_present: bool = False, seed: int = 0) -> float:
    """Simula BB84 y devuelve la tasa de error de bits cuánticos (QBER)."""
    rng = np.random.default_rng(seed)
    alice_bits  = rng.integers(0, 2, n_bits)
    alice_bases = rng.integers(0, 2, n_bits)
    bob_bases   = rng.integers(0, 2, n_bits)

    if eve_present:
        eve_bases = rng.integers(0, 2, n_bits)
        # Eve mide en base aleatoria y reenvía
        eve_bits = np.where(eve_bases == alice_bases, alice_bits,
                            rng.integers(0, 2, n_bits))
        source_bits = eve_bits
        source_bases = eve_bases
    else:
        source_bits  = alice_bits
        source_bases = alice_bases

    # Bob obtiene el bit correcto cuando su base coincide con la fuente
    same_basis = bob_bases == alice_bases
    bob_bits   = np.where(
        bob_bases == source_bases,
        source_bits,
        rng.integers(0, 2, n_bits),
    )

    sifted_alice = alice_bits[same_basis]
    sifted_bob   = bob_bits[same_basis]

    if len(sifted_alice) == 0:
        return 0.0

    return float(np.mean(sifted_alice != sifted_bob))


# ══════════════════════════════════════════════════════════════════════════════
# Tests
# ══════════════════════════════════════════════════════════════════════════════

class TestWernerState:
    def test_trace_is_one(self):
        rho = werner_state(0.8)
        assert abs(np.trace(rho) - 1.0) < 1e-10

    def test_hermitian(self):
        rho = werner_state(0.7)
        assert np.allclose(rho, rho.conj().T)

    def test_fidelity_recovery(self):
        for F in [0.5, 0.75, 0.9, 1.0]:
            rho = werner_state(F)
            assert abs(fidelity_werner(rho) - F) < 1e-10

    def test_maximally_mixed_at_quarter(self):
        # F = 1/4 → estado maximamente mezclado
        rho = werner_state(0.25)
        assert np.allclose(rho, np.eye(4) / 4, atol=1e-10)

    def test_positive_semidefinite(self):
        rho = werner_state(0.9)
        evals = np.linalg.eigvalsh(rho)
        assert np.all(evals >= -1e-10)


class TestBBPSSWPurification:
    def test_fidelity_increases_per_round(self):
        F0 = 0.7
        history = bbpssw_iterate(F0, rounds=5)
        for i in range(len(history) - 1):
            assert history[i + 1] > history[i], (
                f"Fidelidad no creció en ronda {i}: {history[i]:.4f} → {history[i+1]:.4f}"
            )

    def test_converges_toward_one(self):
        history = bbpssw_iterate(0.6, rounds=10)
        assert history[-1] > 0.9, f"No convergió: F_final = {history[-1]:.4f}"

    def test_success_probability_positive(self):
        _, P = bbpssw_round(0.8)
        assert 0.0 < P <= 1.0

    def test_no_improvement_below_threshold(self):
        # F < 0.5: BBPSSW no puede purificar (F' < F)
        F_low = 0.4
        F_new, _ = bbpssw_round(F_low)
        assert F_new <= F_low, (
            f"BBPSSW purificó por debajo del umbral: F={F_low:.2f} → {F_new:.4f}"
        )

    def test_identity_at_f_one(self):
        F_new, P = bbpssw_round(1.0)
        assert abs(F_new - 1.0) < 1e-10
        assert abs(P - 1.0) < 1e-10


class TestBellPairRate:
    def test_rate_decreases_with_distance(self):
        rates = [bell_pair_rate(d) for d in [10, 50, 100, 200]]
        for i in range(len(rates) - 1):
            assert rates[i] > rates[i + 1]

    def test_rate_at_zero_distance(self):
        assert abs(bell_pair_rate(0.0) - 1.0) < 1e-10

    def test_rate_at_100km(self):
        # 100 km con 0.2 dB/km → η = 10^(-2) = 1%
        eta = bell_pair_rate(100.0)
        assert abs(eta - 0.01) < 1e-10

    def test_exponential_decay(self):
        # Verificar que log(η) ∝ -L (decaimiento exponencial en escala lineal)
        L1, L2 = 50.0, 100.0
        eta1 = bell_pair_rate(L1)
        eta2 = bell_pair_rate(L2)
        ratio = np.log10(eta2) / np.log10(eta1)
        assert abs(ratio - 2.0) < 1e-6  # log η ∝ L


class TestMemoryFidelityDecay:
    def test_fidelity_decreases_with_time(self):
        F0, T_mem = 0.95, 1.0
        times = [0.1, 0.5, 1.0, 2.0]
        fids = [memory_fidelity(F0, t, T_mem) for t in times]
        for i in range(len(fids) - 1):
            assert fids[i] > fids[i + 1]

    def test_fidelity_at_t0(self):
        assert abs(memory_fidelity(0.9, 0.0, 1.0) - 0.9) < 1e-10

    def test_asymptote_at_quarter(self):
        # t → ∞: F → 1/4 (estado maximamente mezclado)
        F_inf = memory_fidelity(0.99, 1000.0, 1.0)
        assert abs(F_inf - 0.25) < 1e-3

    def test_better_memory_retains_fidelity(self):
        F0, t = 0.9, 0.5
        F_short = memory_fidelity(F0, t, T_mem=0.5)
        F_long  = memory_fidelity(F0, t, T_mem=5.0)
        assert F_long > F_short


class TestMDIQKD:
    def test_qber_zero_without_eve(self):
        qber = simulate_bb84_qber(n_bits=10000, eve_present=False)
        assert qber < 0.02, f"QBER sin Eva demasiado alto: {qber:.3f}"

    def test_qber_nonzero_with_eve(self):
        qber = simulate_bb84_qber(n_bits=10000, eve_present=True)
        assert qber > 0.15, f"QBER con Eva demasiado bajo: {qber:.3f}"

    def test_qber_with_eve_near_25_percent(self):
        # BB84 con Eve completa introduce ~25% QBER teórico
        qber = simulate_bb84_qber(n_bits=50000, eve_present=True, seed=42)
        assert 0.18 < qber < 0.32, f"QBER con Eva fuera de rango: {qber:.3f}"

    def test_qber_is_bounded(self):
        for seed in range(5):
            qber = simulate_bb84_qber(500, eve_present=True, seed=seed)
            assert 0.0 <= qber <= 1.0
