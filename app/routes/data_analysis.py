# app/routes/data_analysis.py
from fastapi import APIRouter
from app.analysis.analysis_functions import (
    analyze_loan_amount_distribution,
    grade_vs_defaults,
    state_wise_defaults,
    risk_factors_analysis,
    temporal_default_trends,
)

router = APIRouter()

@router.get("/loan-distribution")
async def loan_distribution():
    return await analyze_loan_amount_distribution()

@router.get("/grade-defaults")
async def grade_defaults():
    return await grade_vs_defaults()

@router.get("/state-defaults")
async def state_defaults():
    return await state_wise_defaults()

@router.get("/risk-factors")
async def risk_factors():
    return await risk_factors_analysis()

@router.get("/temporal-trends")
async def temporal_trends():
    return await temporal_default_trends()
