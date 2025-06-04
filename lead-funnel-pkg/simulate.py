import yaml
import math
from pathlib import Path
from core import run_funnel
from loader import load_journey

CONFIG = yaml.safe_load(open(Path(__file__).parent / "config" / "defaults.yml"))

def alpha_rule(N: int) -> float:
    """Implements the rule in YAML (could eval for flexibility)."""
    return min(3.0, 1 + N / 10)

def get_length_bucket(N: int) -> str:
    return "short" if N <= 6 else "medium" if N <= 12 else "long"

def simulate(csv_path: str, cohort: int, traffic_src: str,
             E: float, N_importance: float) -> float:
    journey = load_journey(csv_path)
    L = get_length_bucket(len(journey))
    lb = CONFIG["length_buckets"][L]

    params = (
        lb["k"], lb["gamma_exit"], lb["gamma_boost"],
        lb["eps"], alpha_rule(len(journey)), lb["beta"]
    )
    weights = (
        CONFIG["weights"]["w_c"],
        CONFIG["weights"]["w_cb"],
        CONFIG["weights"]["w_f"]
    )
    tables = {
        "input_type_scores": CONFIG["input_type_scores"],
        "traffic_source_multipliers": CONFIG["traffic_source_multipliers"],
        "w_E": CONFIG["weights"]["w_E"],
        "w_N": CONFIG["weights"]["w_N"],
    }

    return run_funnel(journey, cohort, traffic_src,
                      E, N_importance, weights, params, tables)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Simulate funnel CVR")
    parser.add_argument("csv", help="Path to journey CSV")
    parser.add_argument("--cohort", type=int, default=1000)
    parser.add_argument("--source", default="paid_search")
    parser.add_argument("--E", type=float, default=4.0)
    parser.add_argument("--N_imp", type=float, default=4.0)
    args = parser.parse_args()

    cvr = simulate(args.csv, args.cohort, args.source, args.E, args.N_imp)
    print(f"Predicted end-to-end CVR: {cvr:.4f}")