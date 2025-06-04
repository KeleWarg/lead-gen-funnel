import math
from typing import List

def run_funnel(journey: List, cohort: int, traffic_src: str,
               E: float, N_importance: float,
               weights: tuple, params: tuple, tables: dict) -> float:
    """Pure predictive engine. No file‑I/O or globals.

    Args:
        journey: list of Step objects (see loader.py)
        cohort:  starting user count
        traffic_src: key into traffic_source_multipliers
        E, N_importance: entry emotion / necessity (1‑5)
        weights: (w_c, w_cb, w_f)
        params:  (k, gamma_exit, gamma_boost, eps, alpha, beta)
        tables:  dict with lookup tables
    Returns:
        CR_total: predicted end‑to‑end conversion rate (0‑1)
    """
    k, gamma_exit, gamma_boost, eps, alpha, beta = params
    w_c, w_cb, w_f = weights
    input_type_scores = tables["input_type_scores"]
    S = tables["traffic_source_multipliers"][traffic_src]

    # Entry motivation
    w_E, w_N = tables["w_E"], tables["w_N"]
    M_prev = min(5, (w_E * E + w_N * N_importance) * S)
    U_prev, streak, CR_total = cohort, 0.0, 1.0

    for s, step in enumerate(journey, start=1):
        # --- question complexity
        Q_scores = [input_type_scores[q.type] for q in step.questions]
        raw_SC = sum(Q_scores) / len(Q_scores)
        SC_s = max(1, min(raw_SC, 5))

        # --- count burden
        CB_s = min(eps * max(0, len(step.questions) - 1), 4)

        # --- fatigue & streak
        progress = s / len(journey) if len(journey) <= 6 else math.sqrt(s / len(journey))
        streak = streak * 0.5 + (1 if SC_s >= 4 else 0)
        F_s = max(1, min(1 + alpha * progress + beta * streak - gamma_boost * step.boosts, 5))

        # --- page score & motivation decay
        PS_s = (w_c * SC_s + w_cb * CB_s + w_f * F_s) / (w_c + w_cb + w_f)
        M_s = max(0, M_prev - k * PS_s)

        delta = PS_s - M_s
        p_exit = 1 / (1 + math.exp(-gamma_exit * delta))
        CR_s = 1 - p_exit

        # propagate
        U_prev *= CR_s
        M_prev = M_s
        CR_total *= CR_s

        # store predictions on the step object (optional)
        step.pred = dict(SC=SC_s, CB=CB_s, F=F_s, CR=CR_s)

    return CR_total