"""Main FastAPI application."""

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import imagery
from app.config.constants import CITIES
from app.models.schemas import CitiesResponse, CityInfo

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI(
    title="Gravitas API",
    description="Urban Heat Analysis API with Earth Engine",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        "https://*.vercel.app",  # Vercel deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(imagery.router, prefix="/api", tags=["imagery"])


@app.get("/")
def read_root():
    """Root endpoint."""
    return {
        "message": "Gravitas API",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/api/cities", response_model=CitiesResponse)
def get_cities():
    """Get available cities for analysis."""
    cities_info = {
        name: CityInfo(name=name, center=data["center"], bbox=data["bbox"])
        for name, data in CITIES.items()
    }
    return CitiesResponse(cities=cities_info)


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
