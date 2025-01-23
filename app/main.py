from fastapi import FastAPI
from app.routes import data_analysis, data_processing

app = FastAPI()

# Mount routers
app.include_router(data_processing.router, prefix="/api/data-processing", tags=["Data Processing"])
app.include_router(data_analysis.router, prefix="/api/data_analysis", tags=["Data Analysis"])

@app.get("/")
def read_root():
    return {"message": "Backend is running"}
