"""Constants for the Gravitas API."""

from typing import TypedDict


class CityCoordinates(TypedDict):
    """City coordinates with center and bounding box."""

    center: list[float]  # [longitude, latitude]
    bbox: list[list[float]]  # [[lon, lat], [lon, lat], [lon, lat], [lon, lat]]


# Earth Engine constants
LANDSAT_COLLECTION = "LANDSAT/LC08/C02/T1_L2"
SCALE = 30
MAX_PIXELS = 1_000_000_000

# Bit masks for cloud masking
CLOUD_SHADOW_BIT_MASK = 1 << 3
CLOUDS_BIT_MASK = 1 << 5

# Scale factors for Landsat 8
OPTICAL_BANDS_MULTIPLIER = 0.0000275
OPTICAL_BANDS_OFFSET = -0.2
THERMAL_BANDS_MULTIPLIER = 0.00341802
THERMAL_BANDS_OFFSET = 149.0

# NDVI visualization
NDVI_MIN = -1
NDVI_MAX = 1
NDVI_PALETTE = ["blue", "white", "green"]

# LST visualization (degrees Celsius)
LST_MIN = 7
LST_MAX = 50
LST_PALETTE = [
    "040274",
    "040281",
    "0502a3",
    "0502b8",
    "0502ce",
    "0502e6",
    "0602ff",
    "235cb1",
    "307ef3",
    "269db1",
    "30c8e2",
    "32d3ef",
    "3be285",
    "3ff38f",
    "86e26f",
    "3ae237",
    "b5e22e",
    "d6e21f",
    "fff705",
    "ffd611",
    "ffb613",
    "ff8b13",
    "ff6e08",
    "ff500d",
    "ff0000",
    "de0101",
    "c21301",
    "a71001",
    "911003",
]

# UHI visualization
UHI_MIN = -4
UHI_MAX = 4
UHI_PALETTE = [
    "313695",
    "74add1",
    "fed976",
    "feb24c",
    "fd8d3c",
    "fc4e2a",
    "e31a1c",
    "b10026",
]

# UTFVI visualization
UTFVI_MIN = -1
UTFVI_MAX = 0.3
UTFVI_PALETTE = [
    "313695",
    "74add1",
    "fed976",
    "feb24c",
    "fd8d3c",
    "fc4e2a",
    "e31a1c",
    "b10026",
]

# Emissivity calculation constants
FV_POWER = 2
EM_MULTIPLIER = 0.004
EM_OFFSET = 0.986

# LST calculation constants
LST_WAVELENGTH = 11.5
LST_CONSTANT = 14380
KELVIN_TO_CELSIUS = 273.15

# Default zoom level for maps
DEFAULT_ZOOM_LEVEL = 11

# City coordinates and bounding boxes
CITIES: dict[str, CityCoordinates] = {
    "San Francisco": {
        "center": [-122.4194, 37.7749],
        "bbox": [
            [-122.5194, 37.8749],
            [-122.5194, 37.6749],
            [-122.3194, 37.6749],
            [-122.3194, 37.8749],
        ],
    },
    "Belgrade": {
        "center": [20.4489, 44.7866],
        "bbox": [
            [20.3489, 44.8866],
            [20.3489, 44.6866],
            [20.5489, 44.6866],
            [20.5489, 44.8866],
        ],
    },
    "Zagreb": {
        "center": [15.9819, 45.8150],
        "bbox": [
            [15.8819, 45.9150],
            [15.8819, 45.7150],
            [16.0819, 45.7150],
            [16.0819, 45.9150],
        ],
    },
    "Sarajevo": {
        "center": [18.4131, 43.8563],
        "bbox": [
            [18.2131, 43.9563],
            [18.2131, 43.7563],
            [18.5131, 43.7563],
            [18.5131, 43.9563],
        ],
    },
    "Podgorica": {
        "center": [19.2594, 42.4304],
        "bbox": [
            [19.1594, 42.5304],
            [19.1594, 42.3304],
            [19.3594, 42.3304],
            [19.3594, 42.5304],
        ],
    },
    "Skopje": {
        "center": [21.4254, 41.9981],
        "bbox": [
            [21.3254, 42.0981],
            [21.3254, 41.8981],
            [21.5254, 41.8981],
            [21.5254, 42.0981],
        ],
    },
    "Tirana": {
        "center": [19.8189, 41.3275],
        "bbox": [
            [19.7189, 41.4275],
            [19.7189, 41.2275],
            [19.9189, 41.2275],
            [19.9189, 41.4275],
        ],
    },
    "Pristina": {
        "center": [21.1655, 42.6629],
        "bbox": [
            [21.0655, 42.7629],
            [21.0655, 42.5629],
            [21.2655, 42.5629],
            [21.2655, 42.7629],
        ],
    },
    "Novi Sad": {
        "center": [19.8444, 45.2671],
        "bbox": [
            [19.7444, 45.3671],
            [19.7444, 45.1671],
            [19.9444, 45.1671],
            [19.9444, 45.3671],
        ],
    },
    "Banja Luka": {
        "center": [17.1876, 44.7750],
        "bbox": [
            [17.0876, 44.8750],
            [17.0876, 44.6750],
            [17.2876, 44.6750],
            [17.2876, 44.8750],
        ],
    },
}
