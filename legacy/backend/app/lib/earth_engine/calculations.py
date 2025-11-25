"""Earth Engine calculations for thermal indices."""

import ee

from app.config.constants import (
    EM_MULTIPLIER,
    EM_OFFSET,
    FV_POWER,
    KELVIN_TO_CELSIUS,
    LST_CONSTANT,
    LST_WAVELENGTH,
    MAX_PIXELS,
    SCALE,
)


def calculate_ndvi(image: ee.Image) -> ee.Image:
    """
    Calculate Normalized Difference Vegetation Index (NDVI).

    NDVI = (NIR - Red) / (NIR + Red)

    Args:
        image: Landsat 8 image with SR_B5 (NIR) and SR_B4 (Red) bands

    Returns:
        Image with NDVI band
    """
    ndvi = image.normalizedDifference(["SR_B5", "SR_B4"]).rename("NDVI")
    return ndvi


def calculate_ndvi_stats(
    ndvi: ee.Image, aoi: ee.Geometry
) -> tuple[tuple[float, float] | None, dict[str, str] | None]:
    """
    Calculate NDVI min and max for the area.

    Args:
        ndvi: NDVI image
        aoi: Area of interest

    Returns:
        Tuple of ((ndvi_min, ndvi_max), error_dict)
    """
    try:
        ndvi_min_result = ndvi.reduceRegion(
            reducer=ee.Reducer.min(), geometry=aoi, scale=SCALE, maxPixels=MAX_PIXELS
        )
        ndvi_min = ndvi_min_result.values().get(0).getInfo()

        ndvi_max_result = ndvi.reduceRegion(
            reducer=ee.Reducer.max(), geometry=aoi, scale=SCALE, maxPixels=MAX_PIXELS
        )
        ndvi_max = ndvi_max_result.values().get(0).getInfo()

        return (ndvi_min, ndvi_max), None

    except Exception as e:
        return None, {"error": "Failed to calculate NDVI statistics", "detail": str(e)}


def calculate_fractional_vegetation(
    ndvi: ee.Image, ndvi_min: float, ndvi_max: float
) -> ee.Image:
    """
    Calculate Fractional Vegetation (FV) from NDVI.

    FV = ((NDVI - NDVI_min) / (NDVI_max - NDVI_min))^2

    Args:
        ndvi: NDVI image
        ndvi_min: Minimum NDVI value
        ndvi_max: Maximum NDVI value

    Returns:
        Image with FV band
    """
    fv = (
        ndvi.subtract(ndvi_min)
        .divide(ee.Number(ndvi_max).subtract(ndvi_min))
        .pow(ee.Number(FV_POWER))
        .rename("FV")
    )
    return fv


def calculate_emissivity(fv: ee.Image) -> ee.Image:
    """
    Calculate land surface emissivity (EM) from fractional vegetation.

    EM = FV * 0.004 + 0.986

    Args:
        fv: Fractional vegetation image

    Returns:
        Image with EM band
    """
    em = fv.multiply(ee.Number(EM_MULTIPLIER)).add(ee.Number(EM_OFFSET)).rename("EM")
    return em


def calculate_lst(image: ee.Image, em: ee.Image) -> ee.Image:
    """
    Calculate Land Surface Temperature (LST) in Celsius.

    LST = (TB / (1 + (λ * TB / c2) * ln(EM))) - 273.15

    Where:
    - TB = brightness temperature (thermal band ST_B10)
    - λ = wavelength (11.5 μm)
    - c2 = constant (14380)
    - EM = emissivity

    Args:
        image: Landsat 8 image with thermal band
        em: Emissivity image

    Returns:
        Image with LST band in degrees Celsius
    """
    thermal = image.select("ST_B10").rename("thermal")

    lst = thermal.expression(
        "(tb / (1 + ((11.5 * (tb / 14380)) * log(em)))) - 273.15",
        {"tb": thermal.select("thermal"), "em": em},
    ).rename("LST")

    return lst


def calculate_lst_stats(
    lst: ee.Image, aoi: ee.Geometry
) -> tuple[tuple[float, float] | None, dict[str, str] | None]:
    """
    Calculate LST mean and standard deviation for the area.

    Args:
        lst: LST image
        aoi: Area of interest

    Returns:
        Tuple of ((lst_mean, lst_std), error_dict)
    """
    try:
        lst_mean_result = lst.reduceRegion(
            reducer=ee.Reducer.mean(), geometry=aoi, scale=SCALE, maxPixels=MAX_PIXELS
        )
        lst_mean = lst_mean_result.values().get(0).getInfo()

        lst_std_result = lst.reduceRegion(
            reducer=ee.Reducer.stdDev(), geometry=aoi, scale=SCALE, maxPixels=MAX_PIXELS
        )
        lst_std = lst_std_result.values().get(0).getInfo()

        return (lst_mean, lst_std), None

    except Exception as e:
        return None, {"error": "Failed to calculate LST statistics", "detail": str(e)}


def calculate_uhi(lst: ee.Image, lst_mean: float, lst_std: float) -> ee.Image:
    """
    Calculate Urban Heat Index (UHI).

    UHI = (LST - LST_mean) / LST_std

    Args:
        lst: LST image
        lst_mean: Mean LST for the area
        lst_std: Standard deviation of LST

    Returns:
        Image with UHI band
    """
    uhi = lst.subtract(lst_mean).divide(lst_std).rename("UHI")
    return uhi


def calculate_utfvi(lst: ee.Image, lst_mean: float) -> ee.Image:
    """
    Calculate Urban Thermal Field Variance Index (UTFVI).

    UTFVI = (LST - LST_mean) / LST

    Args:
        lst: LST image
        lst_mean: Mean LST for the area

    Returns:
        Image with UTFVI band
    """
    utfvi = lst.subtract(lst_mean).divide(lst).rename("UTFVI")
    return utfvi


def process_all_indices(
    image: ee.Image, aoi: ee.Geometry
) -> tuple[dict[str, ee.Image | float] | None, dict[str, str] | None]:
    """
    Process all thermal indices for an image and area.

    Calculates NDVI, LST, UHI, and UTFVI with statistics.

    Args:
        image: Median composite Landsat 8 image
        aoi: Area of interest

    Returns:
        Tuple of (results_dict, error_dict) where results_dict contains:
        - ndvi: NDVI image
        - lst: LST image
        - uhi: UHI image
        - utfvi: UTFVI image
        - lst_mean: Mean LST value
        - lst_std: Standard deviation of LST
        - ndvi_min: Minimum NDVI value
        - ndvi_max: Maximum NDVI value
    """
    # Calculate NDVI
    ndvi = calculate_ndvi(image)

    # Get NDVI statistics
    ndvi_stats, error = calculate_ndvi_stats(ndvi, aoi)
    if error:
        return None, error
    ndvi_min, ndvi_max = ndvi_stats

    # Calculate FV and emissivity
    fv = calculate_fractional_vegetation(ndvi, ndvi_min, ndvi_max)
    em = calculate_emissivity(fv)

    # Calculate LST
    lst = calculate_lst(image, em)

    # Get LST statistics
    lst_stats, error = calculate_lst_stats(lst, aoi)
    if error:
        return None, error
    lst_mean, lst_std = lst_stats

    # Calculate UHI and UTFVI
    uhi = calculate_uhi(lst, lst_mean, lst_std)
    utfvi = calculate_utfvi(lst, lst_mean)

    results = {
        "ndvi": ndvi,
        "lst": lst,
        "uhi": uhi,
        "utfvi": utfvi,
        "lst_mean": lst_mean,
        "lst_std": lst_std,
        "ndvi_min": ndvi_min,
        "ndvi_max": ndvi_max,
    }

    return results, None
