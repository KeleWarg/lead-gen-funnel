# api/predict.py

import yaml
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sys, os

# Tell Python how to find your funnel package:
sys.path.append(os.path.join(os.path.dirname(__file__), "../lead_funnel_pkg"))

from core import run_funnel  # Adjust if your function name is different

app = FastAPI()

class StepInput(BaseModel):
    step: int
    input_type: str
    invasiveness: float
    difficulty: float
    boosts: Optional[float] = 0.0

class FunnelRequest(BaseModel):
    steps: List[StepInput]
    # You can add more fields here if core.run_funnel needs them

@app.post("/predict")
def predict(request: FunnelRequest):
    try:
        # Convert incoming JSON into the format run_funnel expects
        steps_data = []
        for s in request.steps:
            steps_data.append({
                "step": s.step,
                "input_type": s.input_type,
                "invasiveness": s.invasiveness,
                "difficulty": s.difficulty,
                "boosts": s.boosts or 0.0
            })

        # Load your defaults from config/defaults.yml
        config_path = os.path.join(os.path.dirname(__file__), "../lead_funnel_pkg/config/defaults.yml")
        with open(config_path, "r") as yf:
            defaults = yaml.safe_load(yf)

        # Call your core engine
        result = run_funnel(steps_data, defaults)
        return {"success": True, "prediction": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))