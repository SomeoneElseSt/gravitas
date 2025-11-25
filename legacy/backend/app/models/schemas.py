"""API request and response schemas."""

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


class ProcessImageryRequest(BaseModel):
    """Request body for processing imagery."""

    city: str = Field(..., description="Name of the city to analyze")
    start_date: date = Field(..., description="Start date for imagery collection")
    end_date: date = Field(..., description="End date for imagery collection")


class VisualizationParams(BaseModel):
    """Visualization parameters for map layers."""

    min: float
    max: float
    palette: list[str]


class LayerData(BaseModel):
    """Data for a single map layer."""

    tile_url: str = Field(..., description="URL template for map tiles")
    visualization: VisualizationParams
    name: str
    description: str


class Statistics(BaseModel):
    """Statistical data for the analyzed area."""

    lst_mean: float = Field(..., description="Mean Land Surface Temperature in °C")
    lst_std: float = Field(..., description="Standard Deviation of LST in °C")
    ndvi_min: float = Field(..., description="Minimum NDVI value")
    ndvi_max: float = Field(..., description="Maximum NDVI value")


class ProcessImageryResponse(BaseModel):
    """Response body for processed imagery."""

    city: str
    start_date: str
    end_date: str
    layers: dict[Literal["uhi", "ndvi", "lst", "utfvi"], LayerData]
    statistics: Statistics
    aoi_bounds: list[list[float]] = Field(..., description="Area of Interest bounding box")


class CityInfo(BaseModel):
    """Information about a city."""

    name: str
    center: list[float] = Field(..., description="[longitude, latitude]")
    bbox: list[list[float]] = Field(..., description="Bounding box coordinates")


class CitiesResponse(BaseModel):
    """Response body for available cities."""

    cities: dict[str, CityInfo]


class ErrorResponse(BaseModel):
    """Error response."""

    error: str
    detail: str | None = None
