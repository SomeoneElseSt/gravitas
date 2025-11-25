"use client";

import { useState } from "react";
import dynamic from "next/dynamic";
import { processImagery } from "@/lib/api/client";
import type { ProcessImageryResponse, LayerType } from "@/lib/types/api";
import { DEFAULT_START_DATE, DEFAULT_END_DATE } from "@/lib/constants";

// Dynamically import map to avoid SSR issues with Leaflet
const ThermalMap = dynamic(
  () => import("@/components/map/ThermalMap").then((mod) => mod.ThermalMap),
  { ssr: false }
);

const CITIES = [
  "San Francisco",
  "Belgrade",
  "Zagreb",
  "Sarajevo",
  "Podgorica",
  "Skopje",
  "Tirana",
  "Pristina",
  "Novi Sad",
  "Banja Luka",
];

const LAYER_TYPES: LayerType[] = ["uhi", "ndvi", "lst", "utfvi"];

const LAYER_NAMES: Record<LayerType, string> = {
  uhi: "Urban Heat Index",
  ndvi: "NDVI",
  lst: "Land Surface Temperature",
  utfvi: "Thermal Variance Index",
};

export default function Home() {
  const [city, setCity] = useState("Belgrade");
  const [startDate, setStartDate] = useState(DEFAULT_START_DATE);
  const [endDate, setEndDate] = useState(DEFAULT_END_DATE);
  const [currentLayerIndex, setCurrentLayerIndex] = useState(0);
  const [data, setData] = useState<ProcessImageryResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleProcess = async () => {
    setLoading(true);
    setError(null);

    const result = await processImagery({
      city,
      start_date: startDate,
      end_date: endDate,
    });

    if (result.error) {
      setError(result.error.error);
      setLoading(false);
      return;
    }

    setData(result.data);
    setLoading(false);
  };

  const currentLayerType = LAYER_TYPES[currentLayerIndex];
  const currentLayer = data?.layers[currentLayerType];

  const goToPrevLayer = () => {
    setCurrentLayerIndex((prev) =>
      prev === 0 ? LAYER_TYPES.length - 1 : prev - 1
    );
  };

  const goToNextLayer = () => {
    setCurrentLayerIndex((prev) =>
      prev === LAYER_TYPES.length - 1 ? 0 : prev + 1
    );
  };

  return (
    <div className="flex flex-col h-screen">
      {/* Header */}
      <header className="bg-gray-900 text-white p-4 shadow-lg">
        <h1 className="text-2xl font-bold">
          Urban Heat Analysis
        </h1>
        <p className="text-gray-300 text-sm mt-1">
          Land Surface Temperature and UHI Index Visualization
        </p>
      </header>

      {/* Controls */}
      <div className="bg-gray-100 p-4 shadow-md">
        <div className="max-w-6xl mx-auto flex flex-wrap gap-4 items-end">
          {/* City Selector */}
          <div className="flex-1 min-w-[200px]">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              City
            </label>
            <select
              value={city}
              onChange={(e) => setCity(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {CITIES.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>

          {/* Start Date */}
          <div className="flex-1 min-w-[180px]">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Start Date
            </label>
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* End Date */}
          <div className="flex-1 min-w-[180px]">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              End Date
            </label>
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Process Button */}
          <button
            onClick={handleProcess}
            disabled={loading}
            className="px-6 py-2 bg-blue-600 text-white rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? "Processing..." : "Process Imagery"}
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="max-w-6xl mx-auto mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
            {error}
          </div>
        )}
      </div>

      {/* Map Viewport */}
      <div className="flex-1 relative">
        {data && currentLayer ? (
          <>
            {/* Map */}
            <div className="h-full">
              <ThermalMap
                layer={currentLayer}
                center={[data.aoi_bounds[0][1], data.aoi_bounds[0][0]]}
                zoom={11}
              />
            </div>

            {/* Layer Navigation */}
            <div className="absolute top-4 left-1/2 transform -translate-x-1/2 bg-white rounded-lg shadow-lg p-4 z-[1000]">
              <div className="flex items-center gap-4">
                <button
                  onClick={goToPrevLayer}
                  className="p-2 hover:bg-gray-100 rounded-full"
                  aria-label="Previous layer"
                >
                  <svg
                    className="w-6 h-6"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M15 19l-7-7 7-7"
                    />
                  </svg>
                </button>

                <div className="text-center min-w-[200px]">
                  <h3 className="font-bold text-lg">{currentLayer.name}</h3>
                  <p className="text-sm text-gray-600">
                    {currentLayer.description}
                  </p>
                </div>

                <button
                  onClick={goToNextLayer}
                  className="p-2 hover:bg-gray-100 rounded-full"
                  aria-label="Next layer"
                >
                  <svg
                    className="w-6 h-6"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 5l7 7-7 7"
                    />
                  </svg>
                </button>
              </div>
            </div>

            {/* Statistics */}
            <div className="absolute bottom-4 right-4 bg-white rounded-lg shadow-lg p-4 z-[1000]">
              <h4 className="font-bold mb-2">Statistics</h4>
              <div className="text-sm space-y-1">
                <div>
                  <span className="font-medium">LST Mean:</span>{" "}
                  {data.statistics.lst_mean.toFixed(2)}°C
                </div>
                <div>
                  <span className="font-medium">LST Std Dev:</span>{" "}
                  {data.statistics.lst_std.toFixed(2)}°C
                </div>
                <div>
                  <span className="font-medium">NDVI Range:</span>{" "}
                  {data.statistics.ndvi_min.toFixed(2)} -{" "}
                  {data.statistics.ndvi_max.toFixed(2)}
                </div>
              </div>
            </div>
          </>
        ) : (
          <div className="h-full flex items-center justify-center text-gray-500">
            <div className="text-center">
              <svg
                className="w-16 h-16 mx-auto mb-4 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"
                />
              </svg>
              <p className="text-lg">Select a city and date range, then click Process Imagery</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
