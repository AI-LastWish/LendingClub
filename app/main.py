from fastapi import FastAPI
from app.routes import data_processing, analysis

app = FastAPI()

# Mount routers
app.include_router(data_processing.router, prefix="/api/data-processing", tags=["Data Processing"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["Analysis"])

@app.get("/")
def read_root():
    return {"message": "Backend is running"}
