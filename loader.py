from dataclasses import dataclass, field
from typing import List
import pandas as pd

@dataclass
class Question:
    type: str
    invasiveness: float
    difficulty: float

@dataclass
class Step:
    questions: List[Question]
    boosts: float = 0.0
    pred: dict = field(default_factory=dict)

def load_journey(csv_path: str) -> List[Step]:
    """Convert a CSV into a list[Step].

    Expected columns:
        step (int), input_type (str), invasiveness (float),
        difficulty (float), boosts (float, optional)
    """
    df = pd.read_csv(csv_path)
    if "boosts" not in df.columns:
        df["boosts"] = 0.0

    steps = []
    for step_id, g in df.groupby("step", sort=True):
        qs = [Question(row.input_type, row.invasiveness, row.difficulty) for row in g.itertuples()]
        boost_val = g.boosts.iloc[0]
        steps.append(Step(qs, boosts=boost_val))
    return steps