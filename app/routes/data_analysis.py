# app/routes/data_analysis.py
from fastapi import APIRouter, HTTPException
from app.analysis.cache import cache

router = APIRouter()

@router.get("/loan-distribution")
async def loan_distribution():
    """Fetch precomputed loan distribution analysis from the cache."""
    if "loan_distribution" in cache:
        return cache["loan_distribution"]
    raise HTTPException(status_code=500, detail="Loan distribution data is not available in the cache.")

@router.get("/grade-defaults")
async def grade_defaults():
    """Fetch precomputed grade defaults analysis from the cache."""
    if "grade_defaults" in cache:
        return cache["grade_defaults"]
    raise HTTPException(status_code=500, detail="Grade defaults data is not available in the cache.")

@router.get("/state-defaults")
async def state_defaults():
    """Fetch precomputed state defaults analysis from the cache."""
    if "state_defaults" in cache:
        return cache["state_defaults"]
    raise HTTPException(status_code=500, detail="State defaults data is not available in the cache.")

@router.get("/risk-factors")
async def risk_factors():
    """Fetch precomputed risk factors analysis from the cache."""
    if "risk_factors" in cache:
        return cache["risk_factors"]
    raise HTTPException(status_code=500, detail="Risk factors data is not available in the cache.")

@router.get("/temporal-trends")
async def temporal_trends():
    """Fetch precomputed temporal trends analysis from the cache."""
    if "temporal_trends" in cache:
        return cache["temporal_trends"]
    raise HTTPException(status_code=500, detail="Temporal trends data is not available in the cache.")

@router.get("/report")
async def report():
    """Fetch the precomputed final analysis report from the cache."""
    if "final_report" in cache:
        return cache["final_report"]
    raise HTTPException(status_code=500, detail="Final report is not available in the cache.")
