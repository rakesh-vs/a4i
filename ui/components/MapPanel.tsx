"use client";

import { useCopilotChat } from "@copilotkit/react-core";
import { useState, useEffect } from "react";

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

export function MapPanel() {
  const [markers, setMarkers] = useState<MapMarker[]>([]);
  const [selectedMarker, setSelectedMarker] = useState<MapMarker | null>(null);
  const [mapCenter, setMapCenter] = useState({ lat: 37.7749, lng: -122.4194 }); // San Francisco
  const [zoom, setZoom] = useState(10);
  const { visibleMessages } = useCopilotChat();

  // Parse messages for location data
  useEffect(() => {
    if (!visibleMessages || visibleMessages.length === 0) return;

    // Extract markers from messages (this is a simplified version)
    // In a real implementation, you'd parse structured data from agent responses
    const newMarkers: MapMarker[] = [];

    visibleMessages.forEach((msg: any) => {
      if (msg.role === "assistant" && msg.content) {
        // Look for location mentions in the content
        // This is a basic implementation - you can enhance it with better parsing
        if (msg.content.includes("San Francisco")) {
          if (!newMarkers.find(m => m.title === "San Francisco")) {
            newMarkers.push({
              id: "sf-1",
              type: "disaster",
              lat: 37.7749,
              lng: -122.4194,
              title: "San Francisco",
              description: "Query location",
              icon: "📍",
            });
          }
        }
        if (msg.content.includes("Los Angeles")) {
          if (!newMarkers.find(m => m.title === "Los Angeles")) {
            newMarkers.push({
              id: "la-1",
              type: "disaster",
              lat: 34.0522,
              lng: -118.2437,
              title: "Los Angeles",
              description: "Query location",
              icon: "📍",
            });
          }
        }
      }
    });

    if (newMarkers.length > 0) {
      setMarkers(newMarkers);
    }
  }, [visibleMessages]);

  const handleZoomIn = () => setZoom(Math.min(zoom + 1, 20));
  const handleZoomOut = () => setZoom(Math.max(zoom - 1, 1));

  return (
    <div className="h-full flex flex-col bg-gradient-to-br from-blue-50 to-blue-100">
      {/* Map Header */}
      <div className="px-4 py-3 bg-white border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900">Emergency Map</h2>
        <p className="text-xs text-gray-500 mt-1">Real-time disaster and relief locations</p>
      </div>

      {/* Map Container */}
      <div className="flex-1 relative overflow-hidden bg-gradient-to-br from-blue-100 via-blue-50 to-cyan-50">
        {/* Simplified Map Visualization */}
        <div className="w-full h-full relative">
          {/* Map Background Grid */}
          <div className="absolute inset-0 opacity-10">
            <div className="w-full h-full" style={{
              backgroundImage: `
                linear-gradient(0deg, transparent 24%, rgba(0,0,0,.05) 25%, rgba(0,0,0,.05) 26%, transparent 27%, transparent 74%, rgba(0,0,0,.05) 75%, rgba(0,0,0,.05) 76%, transparent 77%, transparent),
                linear-gradient(90deg, transparent 24%, rgba(0,0,0,.05) 25%, rgba(0,0,0,.05) 26%, transparent 27%, transparent 74%, rgba(0,0,0,.05) 75%, rgba(0,0,0,.05) 76%, transparent 77%, transparent)
              `,
              backgroundSize: '50px 50px'
            }} />
          </div>

          {/* Markers */}
          <div className="absolute inset-0">
            {markers.map((marker) => {
              // Simple projection: convert lat/lng to screen coordinates
              const x = ((marker.lng + 180) / 360) * 100;
              const y = ((90 - marker.lat) / 180) * 100;

              return (
                <div
                  key={marker.id}
                  className="absolute transform -translate-x-1/2 -translate-y-1/2 cursor-pointer group"
                  style={{ left: `${x}%`, top: `${y}%` }}
                  onClick={() => setSelectedMarker(marker)}
                >
                  {/* Marker Pulse */}
                  <div className={`absolute w-8 h-8 rounded-full ${MARKER_COLORS[marker.type]} opacity-30 animate-pulse`}
                    style={{ transform: 'translate(-50%, -50%)' }} />
                  
                  {/* Marker Pin */}
                  <div className={`relative w-8 h-8 rounded-full ${MARKER_COLORS[marker.type]} border-2 border-white shadow-lg flex items-center justify-center text-white text-sm font-bold`}
                    style={{ transform: 'translate(-50%, -50%)' }}>
                    {MARKER_ICONS[marker.type]}
                  </div>

                  {/* Hover Tooltip */}
                  <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 bg-gray-900 text-white text-xs rounded whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
                    {marker.title}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Center Crosshair */}
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 pointer-events-none">
            <div className="w-6 h-6 border-2 border-blue-400 rounded-full opacity-50" />
            <div className="w-1 h-1 bg-blue-400 rounded-full absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />
          </div>
        </div>
      </div>

      {/* Map Controls */}
      <div className="px-4 py-3 bg-white border-t border-gray-200 space-y-3">
        {/* Zoom Controls */}
        <div className="flex items-center gap-2">
          <button
            onClick={handleZoomOut}
            className="flex-1 px-3 py-2 bg-gray-100 hover:bg-gray-200 rounded text-sm font-medium text-gray-700 transition"
          >
            −
          </button>
          <span className="text-xs text-gray-600 font-medium">Zoom: {zoom}</span>
          <button
            onClick={handleZoomIn}
            className="flex-1 px-3 py-2 bg-gray-100 hover:bg-gray-200 rounded text-sm font-medium text-gray-700 transition"
          >
            +
          </button>
        </div>

        {/* Legend */}
        <div className="space-y-2 pt-2 border-t border-gray-200">
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

