"""Earth Engine imagery collection and processing."""

import ee

from app.config.constants import (
    CLOUD_SHADOW_BIT_MASK,
    CLOUDS_BIT_MASK,
    LANDSAT_COLLECTION,
    OPTICAL_BANDS_MULTIPLIER,
    OPTICAL_BANDS_OFFSET,
    THERMAL_BANDS_MULTIPLIER,
    THERMAL_BANDS_OFFSET,
)


def apply_scale_factors(image: ee.Image) -> ee.Image:
    """
    Apply scale factors to Landsat 8 optical and thermal bands.

    Args:
        image: Landsat 8 image

    Returns:
        Image with corrected scale factors
    """
    optical_bands = (
        image.select("SR_B.*").multiply(OPTICAL_BANDS_MULTIPLIER).add(OPTICAL_BANDS_OFFSET)
    )
    thermal_bands = (
        image.select("ST_B.*").multiply(THERMAL_BANDS_MULTIPLIER).add(THERMAL_BANDS_OFFSET)
    )

    return image.addBands(optical_bands, None, True).addBands(thermal_bands, None, True)


def mask_clouds(image: ee.Image) -> ee.Image:
    """
    Mask clouds and cloud shadows from Landsat 8 imagery.

    Uses QA_PIXEL band bits 3 and 5 for cloud shadow and clouds.

    Args:
        image: Landsat 8 image

    Returns:
        Masked image
    """
    qa = image.select("QA_PIXEL")

    # Both flags should be set to zero, indicating clear conditions
    mask = qa.bitwiseAnd(CLOUD_SHADOW_BIT_MASK).eq(0).And(qa.bitwiseAnd(CLOUDS_BIT_MASK).eq(0))

    return image.updateMask(mask)


def get_median_composite(
    aoi: ee.Geometry, start_date: str, end_date: str
) -> tuple[ee.Image | None, dict[str, str] | None]:
    """
    Get median composite of Landsat 8 imagery for an area and date range.

    Args:
        aoi: Area of interest geometry
        start_date: Start date in ISO format (YYYY-MM-DD)
        end_date: End date in ISO format (YYYY-MM-DD)

    Returns:
        Tuple of (median_image, error_dict)
    """
    try:
        # Filter and process image collection
        collection = (
            ee.ImageCollection(LANDSAT_COLLECTION)
            .filterDate(start_date, end_date)
            .filterBounds(aoi)
            .map(apply_scale_factors)
            .map(mask_clouds)
        )

        # Check if collection has images
        count = collection.size().getInfo()
        if count == 0:
            return None, {
                "error": "No imagery found",
                "detail": f"No Landsat 8 images found for the specified date range and location",
            }

        # Create median composite
        median_image = collection.median()

        return median_image, None

    except Exception as e:
        return None, {"error": "Failed to process imagery", "detail": str(e)}
