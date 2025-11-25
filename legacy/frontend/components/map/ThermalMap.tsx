"use client";

import { useEffect } from "react";
import { MapContainer, TileLayer, useMap } from "react-leaflet";
import type { LayerData } from "@/lib/types/api";
import "leaflet/dist/leaflet.css";

interface ThermalMapProps {
  layer: LayerData;
  center: [number, number];
  zoom: number;
}

function TileLayerUpdater({ tileUrl }: { tileUrl: string }) {
  const map = useMap();

  useEffect(() => {
    // Force map to refresh when tile URL changes
    map.invalidateSize();
  }, [tileUrl, map]);

  return <TileLayer url={tileUrl} />;
}

export function ThermalMap({ layer, center, zoom }: ThermalMapProps) {
  return (
    <MapContainer
      center={center}
      zoom={zoom}
      style={{ height: "100%", width: "100%" }}
      scrollWheelZoom={true}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <TileLayerUpdater tileUrl={layer.tile_url} />
    </MapContainer>
  );
}
