"""Imagery processing routes."""

import ee
from fastapi import APIRouter, HTTPException

from app.config.constants import CITIES
from app.lib.earth_engine.calculations import process_all_indices
from app.lib.earth_engine.client import get_ee_instance
from app.lib.earth_engine.imagery import get_median_composite
from app.lib.earth_engine.visualization import create_all_layers
from app.models.schemas import (
    ErrorResponse,
    ProcessImageryRequest,
    ProcessImageryResponse,
    Statistics,
)

router = APIRouter()


@router.post(
    "/process-imagery",
    response_model=ProcessImageryResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
def process_imagery(request: ProcessImageryRequest):
    """
    Process satellite imagery for a city and date range.

    Returns tile URLs and statistics for all four indices:
    - UHI (Urban Heat Index)
    - NDVI (Normalized Difference Vegetation Index)
    - LST (Land Surface Temperature)
    - UTFVI (Urban Thermal Field Variance Index)
    """
    # Validate city exists
    if request.city not in CITIES:
        raise HTTPException(
            status_code=400,
            detail=f"City '{request.city}' not found. Available cities: {list(CITIES.keys())}",
        )

    # Validate date range
    if request.start_date >= request.end_date:
        raise HTTPException(
            status_code=400,
            detail="start_date must be before end_date",
        )

    # Initialize Earth Engine
    ee_module, error = get_ee_instance()
    if error:
        raise HTTPException(status_code=500, detail=error["detail"])

    # Get city data
    city_data = CITIES[request.city]
    aoi = ee.Geometry.Polygon([city_data["bbox"]])

    # Convert dates to strings
    start_date_str = request.start_date.isoformat()
    end_date_str = request.end_date.isoformat()

    # Get median composite
    median_image, error = get_median_composite(aoi, start_date_str, end_date_str)
    if error:
        raise HTTPException(status_code=500, detail=error["detail"])

    # Process all indices
    results, error = process_all_indices(median_image, aoi)
    if error:
        raise HTTPException(status_code=500, detail=error["detail"])

    # Create layer data with tile URLs
    indices = {
        "ndvi": results["ndvi"],
        "lst": results["lst"],
        "uhi": results["uhi"],
        "utfvi": results["utfvi"],
    }
    layers, error = create_all_layers(indices)
    if error:
        raise HTTPException(status_code=500, detail=error["detail"])

    # Create statistics object
    statistics = Statistics(
        lst_mean=results["lst_mean"],
        lst_std=results["lst_std"],
        ndvi_min=results["ndvi_min"],
        ndvi_max=results["ndvi_max"],
    )

    # Return response
    return ProcessImageryResponse(
        city=request.city,
        start_date=start_date_str,
        end_date=end_date_str,
        layers=layers,
        statistics=statistics,
        aoi_bounds=city_data["bbox"],
    )
