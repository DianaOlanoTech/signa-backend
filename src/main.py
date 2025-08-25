import sys
from pathlib import Path

# Configure the Python path to resolve imports
current_dir = Path(__file__).resolve().parent
backend_dir = current_dir.parent
sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.endpoints import trademarks

# Define the list of allowed origins (domains)
# This explicitly tells the backend which frontend URLs are allowed to make requests.
origins = [
    "https://signa-frontend-chi.vercel.app",  # Your frontend's production URL
    "http://localhost:3000",                  # The URL for your local frontend development
    "http://localhost:8000",                  # Local backend for development
]

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
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
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