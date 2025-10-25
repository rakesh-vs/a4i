"use client";

import { useCopilotChat } from "@copilotkit/react-core";
import { useState, useEffect } from "react";
import dynamic from "next/dynamic";

interface MapMarker {
  id: string;
  type: "disaster" | "shelter" | "hospital" | "supply";
  lat: number;
  lng: number;
  title: string;
  description: string;
  icon: string;
}

const MARKER_COLORS: Record<string, string> = {
  disaster: "bg-red-500",
  shelter: "bg-blue-500",
  hospital: "bg-green-500",
  supply: "bg-yellow-500",
};

const MARKER_ICONS: Record<string, string> = {
  disaster: "🌪️",
  shelter: "🏠",
  hospital: "🏥",
  supply: "📦",
};

// Dynamically import Leaflet map to avoid SSR issues
const LeafletMap = dynamic(() => import("./LeafletMap"), { ssr: false });

export function MapPanel() {
  const [markers, setMarkers] = useState<MapMarker[]>([]);
  const [selectedMarker, setSelectedMarker] = useState<MapMarker | null>(null);
  const [mapCenter, setMapCenter] = useState({ lat: 37.7749, lng: -122.4194 }); // San Francisco
  const [zoom, setZoom] = useState(10);
  const { visibleMessages } = useCopilotChat();

  // Parse agent responses for location data
  useEffect(() => {
    if (!visibleMessages || visibleMessages.length === 0) return;

    const newMarkers: MapMarker[] = [];
    let centerLat = 37.7749;
    let centerLng = -122.4194;

    visibleMessages.forEach((msg: any, idx: number) => {
      if (msg.role === "assistant" && msg.content) {
        const content = msg.content;

        // Parse shelter locations (look for coordinates in format: lat, lng or latitude, longitude)
        const shelterMatches = content.match(/shelter[^.]*?(\d+\.\d+)[,\s]+(-?\d+\.\d+)/gi);
        if (shelterMatches) {
          shelterMatches.forEach((match, i) => {
            const coords = match.match(/(\d+\.\d+)[,\s]+(-?\d+\.\d+)/);
            if (coords) {
              const lat = parseFloat(coords[1]);
              const lng = parseFloat(coords[2]);
              newMarkers.push({
                id: `shelter-${idx}-${i}`,
                type: "shelter",
                lat,
                lng,
                title: "Emergency Shelter",
                description: "Shelter location from agent data",
                icon: "🏠",
              });
              centerLat = lat;
              centerLng = lng;
            }
          });
        }

        // Parse hospital locations
        const hospitalMatches = content.match(/hospital[^.]*?(\d+\.\d+)[,\s]+(-?\d+\.\d+)/gi);
        if (hospitalMatches) {
          hospitalMatches.forEach((match, i) => {
            const coords = match.match(/(\d+\.\d+)[,\s]+(-?\d+\.\d+)/);
            if (coords) {
              const lat = parseFloat(coords[1]);
              const lng = parseFloat(coords[2]);
              newMarkers.push({
                id: `hospital-${idx}-${i}`,
                type: "hospital",
                lat,
                lng,
                title: "Medical Facility",
                description: "Hospital location from agent data",
                icon: "🏥",
              });
              centerLat = lat;
              centerLng = lng;
            }
          });
        }

        // Parse disaster/alert locations
        const disasterMatches = content.match(/disaster|alert|warning[^.]*?(\d+\.\d+)[,\s]+(-?\d+\.\d+)/gi);
        if (disasterMatches) {
          disasterMatches.forEach((match, i) => {
            const coords = match.match(/(\d+\.\d+)[,\s]+(-?\d+\.\d+)/);
            if (coords) {
              const lat = parseFloat(coords[1]);
              const lng = parseFloat(coords[2]);
              newMarkers.push({
                id: `disaster-${idx}-${i}`,
                type: "disaster",
                lat,
                lng,
                title: "Disaster Alert",
                description: "Disaster location from agent data",
                icon: "🌪️",
              });
              centerLat = lat;
              centerLng = lng;
            }
          });
        }

        // Parse supply locations
        const supplyMatches = content.match(/supply|distribution[^.]*?(\d+\.\d+)[,\s]+(-?\d+\.\d+)/gi);
        if (supplyMatches) {
          supplyMatches.forEach((match, i) => {
            const coords = match.match(/(\d+\.\d+)[,\s]+(-?\d+\.\d+)/);
            if (coords) {
              const lat = parseFloat(coords[1]);
              const lng = parseFloat(coords[2]);
              newMarkers.push({
                id: `supply-${idx}-${i}`,
                type: "supply",
                lat,
                lng,
                title: "Supply Center",
                description: "Supply distribution point from agent data",
                icon: "📦",
              });
              centerLat = lat;
              centerLng = lng;
            }
          });
        }
      }
    });

    if (newMarkers.length > 0) {
      setMarkers(newMarkers);
      setMapCenter({ lat: centerLat, lng: centerLng });
    }
  }, [visibleMessages]);

  return (
    <div className="h-full flex flex-col bg-white">
      {/* Map Header */}
      <div className="px-4 py-3 bg-white border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900">Emergency Map</h2>
        <p className="text-xs text-gray-500 mt-1">Real-time disaster and relief locations</p>
      </div>

      {/* Leaflet Map Container */}
      <div className="flex-1 relative overflow-hidden">
        <LeafletMap
          markers={markers}
          center={mapCenter}
          zoom={zoom}
          onMarkerClick={setSelectedMarker}
        />
      </div>

      {/* Map Controls & Legend */}
      <div className="px-4 py-3 bg-white border-t border-gray-200 space-y-3 max-h-48 overflow-y-auto">
        {/* Legend */}
        <div className="space-y-2">
          <p className="text-xs font-semibold text-gray-700">Legend</p>
          <div className="grid grid-cols-2 gap-2 text-xs">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-red-500" />
              <span className="text-gray-600">Disasters</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-blue-500" />
              <span className="text-gray-600">Shelters</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-green-500" />
              <span className="text-gray-600">Hospitals</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-yellow-500" />
              <span className="text-gray-600">Supplies</span>
            </div>
          </div>
        </div>

        {/* Marker Count */}
        <div className="text-xs text-gray-600 pt-2 border-t border-gray-200">
          📍 {markers.length} location{markers.length !== 1 ? 's' : ''} found
        </div>

        {/* Selected Marker Info */}
        {selectedMarker && (
          <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="flex items-start gap-2">
              <span className="text-xl">{MARKER_ICONS[selectedMarker.type]}</span>
              <div className="flex-1 min-w-0">
                <h4 className="font-semibold text-gray-900 text-sm">{selectedMarker.title}</h4>
                <p className="text-xs text-gray-600 mt-1">{selectedMarker.description}</p>
                <p className="text-xs text-gray-500 mt-2">
                  📍 {selectedMarker.lat.toFixed(4)}, {selectedMarker.lng.toFixed(4)}
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

