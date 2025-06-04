# Lead-Gen Funnel Predictor

A lightweight, configurable engine that predicts step-by-step drop‑off and end‑to‑end conversion for lead‑generation funnels.

## Layout

```
lead_funnel_pkg/
├── config/
│   └── defaults.yml     # All tunable constants
├── core.py              # Pure predictive engine
├── loader.py            # CSV → Journey objects
├── simulate.py          # CLI / glue layer
└── README.md
```

## Quick start

```bash
python simulate.py example_journey.csv \
       --cohort 5000 \
       --source paid_search \
       --E 4 --N_imp 5
```

The script prints the predicted conversion rate.

### CSV format

| column        | type   | notes                                          |
|---------------|--------|------------------------------------------------|
| **step**      | int    | 1‑based step ID                                |
| **input_type**| str    | see keys in `config/defaults.yml`              |
| **invasiveness**| float| 1‑5 scale                                      |
| **difficulty**| float | 1‑5 scale                                      |
| **boosts**    | float | optional, default `0`                           |

## Extending

* Edit `config/defaults.yml` to tune parameters.
* Swap a different `alpha_rule` or bucket logic in `simulate.py`.
* `run_funnel()` in `core.py` is pure and fast—ideal for unit tests or integration into a Streamlit / React dashboard.