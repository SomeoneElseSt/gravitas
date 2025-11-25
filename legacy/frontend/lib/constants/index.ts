/**
 * Frontend constants.
 * Keep visualization constants in sync with backend/app/config/constants.py
 */

// Map configuration
export const DEFAULT_ZOOM_LEVEL = 11;

// NDVI visualization
export const NDVI_MIN = -1;
export const NDVI_MAX = 1;
export const NDVI_PALETTE = ["blue", "white", "green"];

// LST visualization (degrees Celsius)
export const LST_MIN = 7;
export const LST_MAX = 50;
export const LST_PALETTE = [
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
];

// UHI visualization
export const UHI_MIN = -4;
export const UHI_MAX = 4;
export const UHI_PALETTE = [
  "313695",
  "74add1",
  "fed976",
  "feb24c",
  "fd8d3c",
  "fc4e2a",
  "e31a1c",
  "b10026",
];

// UTFVI visualization
export const UTFVI_MIN = -1;
export const UTFVI_MAX = 0.3;
export const UTFVI_PALETTE = [
  "313695",
  "74add1",
  "fed976",
  "feb24c",
  "fd8d3c",
  "fc4e2a",
  "e31a1c",
  "b10026",
];

// Legend configurations
export const UHI_LEGEND = {
  "> 3°C Severe": UHI_PALETTE[7],
  "2 - 3°C Strong": UHI_PALETTE[6],
  "1 - 2°C Moderate": UHI_PALETTE[5],
  "0 - 1°C Slight": UHI_PALETTE[4],
  "± 0.5°C Neutral": UHI_PALETTE[3],
  "–1 - 0°C Slight Cool": UHI_PALETTE[2],
  "–2 - –1°C Moderate Cool": UHI_PALETTE[1],
  "< 2°C Strong Cool": UHI_PALETTE[0],
};

export const NDVI_LEGEND = {
  "Built-up Areas/Bare Surfaces": "white",
  "Healthy/Dense Vegetation": "green",
  "Water Bodies": "blue",
};

export const LST_LEGEND = {
  "7°C - 14°C (Very Cool)": LST_PALETTE[2],
  "15°C - 24°C (Cool)": LST_PALETTE[9],
  "25°C - 34°C (Moderate)": LST_PALETTE[14],
  "35°C - 42°C (Warm)": LST_PALETTE[18],
  "43°C - 50°C (Very Hot)": LST_PALETTE[24],
};

export const UTFVI_LEGEND = {
  "High Heat Stress": "b10026",
  "Moderate Heat Stress": "e31a1c",
  "Mild Heat Stress": "fc4e2a",
  Neutral: "fd8d3c",
  "Cooling Effect": "feb24c",
};

// Default date range
export const DEFAULT_START_DATE = "2022-05-01";
export const DEFAULT_END_DATE = "2022-12-31";

// API configuration
export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
