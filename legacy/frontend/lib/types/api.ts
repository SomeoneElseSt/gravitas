/**
 * API types that match the backend Pydantic schemas.
 * Keep in sync with backend/app/models/schemas.py
 */

export interface ProcessImageryRequest {
  city: string;
  start_date: string; // ISO date string (YYYY-MM-DD)
  end_date: string; // ISO date string (YYYY-MM-DD)
}

export interface VisualizationParams {
  min: number;
  max: number;
  palette: string[];
}

export interface LayerData {
  tile_url: string;
  visualization: VisualizationParams;
  name: string;
  description: string;
}

export type LayerType = "uhi" | "ndvi" | "lst" | "utfvi";

export interface Statistics {
  lst_mean: number;
  lst_std: number;
  ndvi_min: number;
  ndvi_max: number;
}

export interface ProcessImageryResponse {
  city: string;
  start_date: string;
  end_date: string;
  layers: Record<LayerType, LayerData>;
  statistics: Statistics;
  aoi_bounds: number[][];
}

export interface CityInfo {
  name: string;
  center: [number, number]; // [longitude, latitude]
  bbox: [number, number][]; // Array of [lon, lat] coordinates
}

export interface CitiesResponse {
  cities: Record<string, CityInfo>;
}

export interface ErrorResponse {
  error: string;
  detail?: string;
}
