"""Earth Engine visualization and tile generation."""

import ee

from app.config.constants import (
    LST_MAX,
    LST_MIN,
    LST_PALETTE,
    NDVI_MAX,
    NDVI_MIN,
    NDVI_PALETTE,
    UHI_MAX,
    UHI_MIN,
    UHI_PALETTE,
    UTFVI_MAX,
    UTFVI_MIN,
    UTFVI_PALETTE,
)
from app.models.schemas import LayerData, VisualizationParams


def get_visualization_params(layer_type: str) -> dict[str, any]:
    """
    Get visualization parameters for a layer type.

    Args:
        layer_type: One of 'ndvi', 'lst', 'uhi', 'utfvi'

    Returns:
        Visualization parameters dict for Earth Engine
    """
    vis_params = {
        "ndvi": {"min": NDVI_MIN, "max": NDVI_MAX, "palette": NDVI_PALETTE},
        "lst": {"min": LST_MIN, "max": LST_MAX, "palette": LST_PALETTE},
        "uhi": {"min": UHI_MIN, "max": UHI_MAX, "palette": UHI_PALETTE},
        "utfvi": {"min": UTFVI_MIN, "max": UTFVI_MAX, "palette": UTFVI_PALETTE},
    }

    return vis_params.get(layer_type, {})


def get_layer_descriptions() -> dict[str, tuple[str, str]]:
    """
    Get human-readable names and descriptions for each layer.

    Returns:
        Dict mapping layer type to (name, description) tuple
    """
    return {
        "ndvi": (
            "NDVI",
            "Vegetation health and density. Higher values (green) indicate healthier vegetation.",
        ),
        "lst": (
            "Land Surface Temperature",
            "Surface temperature in degrees Celsius. Cooler areas are blue, warmer areas are red.",
        ),
        "uhi": (
            "Urban Heat Index",
            "Relative heat concentration compared to city average. Shows urban heat island effects.",
        ),
        "utfvi": (
            "Urban Thermal Field Variance Index",
            "Temperature comfort level classification for urban areas.",
        ),
    }


def generate_tile_url(image: ee.Image, vis_params: dict[str, any]) -> str | None:
    """
    Generate a tile URL from an Earth Engine image.

    Args:
        image: Earth Engine image
        vis_params: Visualization parameters

    Returns:
        Tile URL string or None if failed
    """
    try:
        map_id = image.getMapId(vis_params)
        tile_url = map_id["tile_fetcher"].url_format
        return tile_url
    except Exception:
        return None


def create_layer_data(
    image: ee.Image, layer_type: str
) -> tuple[LayerData | None, dict[str, str] | None]:
    """
    Create LayerData for a specific index.

    Args:
        image: Earth Engine image for the index
        layer_type: One of 'ndvi', 'lst', 'uhi', 'utfvi'

    Returns:
        Tuple of (LayerData, error_dict)
    """
    vis_params = get_visualization_params(layer_type)
    if not vis_params:
        return None, {"error": "Invalid layer type", "detail": f"Unknown layer: {layer_type}"}

    tile_url = generate_tile_url(image, vis_params)
    if not tile_url:
        return None, {
            "error": "Failed to generate tile URL",
            "detail": f"Could not create tiles for {layer_type}",
        }

    descriptions = get_layer_descriptions()
    name, description = descriptions[layer_type]

    layer_data = LayerData(
        tile_url=tile_url,
        visualization=VisualizationParams(
            min=vis_params["min"], max=vis_params["max"], palette=vis_params["palette"]
        ),
        name=name,
        description=description,
    )

    return layer_data, None


def create_all_layers(
    indices: dict[str, ee.Image]
) -> tuple[dict[str, LayerData] | None, dict[str, str] | None]:
    """
    Create LayerData objects for all indices.

    Args:
        indices: Dict with keys 'ndvi', 'lst', 'uhi', 'utfvi' and ee.Image values

    Returns:
        Tuple of (layers_dict, error_dict)
    """
    layers = {}

    for layer_type in ["ndvi", "lst", "uhi", "utfvi"]:
        if layer_type not in indices:
            return None, {
                "error": "Missing index",
                "detail": f"Index '{layer_type}' not found in results",
            }

        layer_data, error = create_layer_data(indices[layer_type], layer_type)
        if error:
            return None, error

        layers[layer_type] = layer_data

    return layers, None
