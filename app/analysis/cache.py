from app.analysis.analysis_functions import (
    analyze_loan_amount_distribution,
    grade_vs_defaults,
    state_wise_defaults,
    risk_factors_analysis,
    temporal_default_trends,  
    generate_final_report,
)

cache = {}

async def initialize_cache():
    """
    Precompute and cache results for analyses and the final report.
    """
    global cache

    try:
        # Precompute individual analyses and store them in the cache
        cache["loan_distribution"] = await analyze_loan_amount_distribution()
        cache["grade_defaults"] = await grade_vs_defaults()
        cache["state_defaults"] = await state_wise_defaults()
        cache["risk_factors"] = await risk_factors_analysis()
        cache["temporal_trends"] = await temporal_default_trends()

        # Generate and cache the final report using precomputed analyses
        cache["final_report"] = await generate_final_report(
            loan_distribution=cache["loan_distribution"],
            grade_defaults=cache["grade_defaults"],
            state_defaults=cache["state_defaults"],
            risk_factors=cache["risk_factors"],
            temporal_trends=cache["temporal_trends"],
        )

    except Exception as e:
        print(f"Error during cache initialization: {e}")
