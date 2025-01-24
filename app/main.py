from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import data_analysis, data_processing
from app.analysis.cache import initialize_cache

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan handler to initialize and clean up resources."""
    print("Initializing cache...")
    await initialize_cache()  # Precompute results and store them in cache
    print("Cache initialized.")
    yield  # This allows the application to run
    print("Shutting down resources (if necessary)...")

# Create FastAPI application with lifespan
app = FastAPI(lifespan=lifespan)

# Mount routers
app.include_router(data_processing.router, prefix="/api/data-processing", tags=["Data Processing"])
app.include_router(data_analysis.router, prefix="/api/data_analysis", tags=["Data Analysis"])

@app.get("/")
def read_root():
    return {"message": "Backend is running"}
