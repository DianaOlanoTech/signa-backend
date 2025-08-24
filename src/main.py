import sys
from pathlib import Path

# Configurar el path de Python para resolver imports
current_dir = Path(__file__).resolve().parent
backend_dir = current_dir.parent
sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.endpoints import trademarks

# Create the main FastAPI application instance
# This is the core of our API with metadata for documentation
app = FastAPI(
    title="Trademark CRUD API",
    description="API for trademark record management - SignaIP Technical Test",
    version="1.0.0"
)

# Configure CORS (Cross-Origin Resource Sharing) middleware
# This allows our API to be accessed from different domains/origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the trademark router with all its endpoints
# This connects all routes defined in trademarks.router to our main app
# The prefix adds "/api/v1/trademarks" before all routes in that router
# Tags group the endpoints in the API documentation
app.include_router(trademarks.router, prefix="/api/v1/trademarks", tags=["Trademarks"])

# Root endpoint - simple health check or welcome message
# This will be accessible at GET /
@app.get("/")
def read_root():
    """
    Root endpoint that returns a welcome message.
    Useful for health checks and API status verification.
    """
    return {"message": "Welcome to SignaIP API"}