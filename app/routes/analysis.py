from fastapi import APIRouter
from app.services.analysis import analyze_data

router = APIRouter()

@router.get("/health/analysis")
def check_analysis():
    """Health check for the analysis service."""
    try:
        result = analyze_data()
        return {"status": "ok", "message": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
