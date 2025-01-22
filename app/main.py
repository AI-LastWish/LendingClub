from fastapi import FastAPI
from app.routes import data_processing, analysis

app = FastAPI()

# Mount routers
app.include_router(data_processing.router, prefix="/api")
app.include_router(analysis.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Backend is running"}
