from fastapi import APIRouter
from app.services.data_processing import process_data

router = APIRouter()

@router.get("/health/data-processing")
def check_data_processing():
    """Health check for the data processing service."""
    try:
        result = process_data()
        return {"status": "ok", "message": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
