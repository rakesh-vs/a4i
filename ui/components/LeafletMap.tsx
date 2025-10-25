"use client";

import { useEffect, useRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

interface MapMarker {
  id: string;
  type: "disaster" | "shelter" | "hospital" | "supply";
  lat: number;
  lng: number;
  title: string;
  description: string;
  icon: string;
}

interface LeafletMapProps {
  markers: MapMarker[];
  center: { lat: number; lng: number };
  zoom: number;
  onMarkerClick: (marker: MapMarker) => void;
}

const MARKER_COLORS: Record<string, string> = {
  disaster: "#ef4444",
  shelter: "#3b82f6",
  hospital: "#22c55e",
  supply: "#eab308",
};

const MARKER_ICONS: Record<string, string> = {
  disaster: "🌪️",
  shelter: "🏠",
  hospital: "🏥",
  supply: "📦",
};

export default function LeafletMap({
  markers,
  center,
  zoom,
  onMarkerClick,
}: LeafletMapProps) {
  const mapRef = useRef<L.Map | null>(null);
  const markersRef = useRef<Map<string, L.Marker>>(new Map());

  // Initialize map
  useEffect(() => {
    if (!mapRef.current) {
      mapRef.current = L.map("map-container").setView(
        [center.lat, center.lng],
        zoom
      );

      // Add OpenStreetMap tiles
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19,
      }).addTo(mapRef.current);
    }

    return () => {
      // Cleanup is handled by Next.js
    };
  }, []);

  // Update map center and zoom
  useEffect(() => {
    if (mapRef.current) {
      mapRef.current.setView([center.lat, center.lng], zoom);
    }
  }, [center, zoom]);

  // Update markers
  useEffect(() => {
    if (!mapRef.current) return;

    // Remove old markers
    markersRef.current.forEach((marker) => {
      mapRef.current?.removeLayer(marker);
    });
    markersRef.current.clear();

    // Add new markers
    markers.forEach((markerData) => {
      const color = MARKER_COLORS[markerData.type];
      const icon = MARKER_ICONS[markerData.type];

      // Create custom HTML icon
      const html = `
        <div style="
          background-color: ${color};
          color: white;
          border-radius: 50%;
          width: 40px;
          height: 40px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 20px;
          border: 3px solid white;
          box-shadow: 0 2px 8px rgba(0,0,0,0.3);
          cursor: pointer;
        ">
          ${icon}
        </div>
      `;

      const customIcon = L.divIcon({
        html,
        iconSize: [40, 40],
        iconAnchor: [20, 20],
        popupAnchor: [0, -20],
      });

      const marker = L.marker([markerData.lat, markerData.lng], {
        icon: customIcon,
      })
        .bindPopup(
          `<div style="font-size: 12px;">
            <strong>${markerData.title}</strong><br/>
            ${markerData.description}<br/>
            <small>${markerData.lat.toFixed(4)}, ${markerData.lng.toFixed(4)}</small>
          </div>`
        )
        .on("click", () => {
          onMarkerClick(markerData);
        })
        .addTo(mapRef.current!);

      markersRef.current.set(markerData.id, marker);
    });

    // Fit bounds if markers exist
    if (markers.length > 0) {
      const group = new L.FeatureGroup(Array.from(markersRef.current.values()));
      mapRef.current.fitBounds(group.getBounds().pad(0.1));
    }
  }, [markers, onMarkerClick]);

  return (
    <div
      id="map-container"
      style={{
        width: "100%",
        height: "100%",
        position: "relative",
      }}
    />
  );
}

