# app/analysis/cache.py
import asyncio

cache = {}

async def initialize_cache():
    from app.analysis.analysis_functions import (
        analyze_loan_amount_distribution,
        grade_vs_defaults,
        state_wise_defaults,
        risk_factors_analysis,
        temporal_default_trends,
    )

    global cache

    try:
        # Precompute and cache results
        cache["loan_distribution"] = await analyze_loan_amount_distribution()
        cache["grade_defaults"] = await grade_vs_defaults()
        cache["state_defaults"] = await state_wise_defaults()
        cache["risk_factors"] = await risk_factors_analysis()
        cache["temporal_trends"] = await temporal_default_trends()
    except Exception as e:
        print(f"Error during cache initialization: {e}")
