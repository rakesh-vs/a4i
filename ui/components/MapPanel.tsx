"use client";

import { useCoAgent } from "@copilotkit/react-core";
import { Map } from "./Map";

interface LocationData {
  name: string;
  address: string;
  lat: number;
  lng: number;
  place_id: string;
  place_type: string;
  rating?: number | string;
  is_open?: boolean | null;
}

type AgentState = {
  locations: LocationData[];
  center: { lat: number; lng: number };
}

export function MapPanel() {
  // Shared State with the agent - updated automatically via callbacks
  const { state } = useCoAgent<AgentState>({
    name: "first_responder_agent",
    initialState: {
      locations: [],
      center: { lat: 37.7749, lng: -122.4194 },
    },
  });



  return (
    <div className="h-full flex flex-col bg-white relative">
      {/* Map Header Overlay */}
      <div className="absolute top-4 left-4 z-10 bg-white/95 backdrop-blur-md p-4 rounded-xl shadow-xl max-w-xs">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 rounded-full bg-blue-300 flex items-center justify-center shadow-md">
            <span className="text-2xl">🗺️</span>
          </div>
          <div>
            <h2 className="text-xl font-bold text-gray-900">Emergency Map</h2>
            <p className="text-sm text-gray-600">Real-time locations</p>
          </div>
        </div>

        {state.locations && state.locations.length > 0 && (
          <div className="mt-4 pt-3 border-t border-gray-200">
            <p className="text-sm font-semibold text-gray-700 mb-2">
              {state.locations.length} location{state.locations.length !== 1 ? 's' : ''} found
            </p>
            <div className="flex gap-2 flex-wrap">
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
                <span className="w-2 h-2 bg-red-500 rounded-full mr-1"></span>
                Hospitals
              </span>
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                <span className="w-2 h-2 bg-blue-500 rounded-full mr-1"></span>
                Shelters
              </span>
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                <span className="w-2 h-2 bg-green-500 rounded-full mr-1"></span>
                Pharmacies
              </span>
            </div>
          </div>
        )}
      </div>

      {/* Map Container */}
      <div className="flex-1 relative">
        <Map
          locations={state.locations || []}
          center={state.center || { lat: 37.7749, lng: -122.4194 }}
        />
      </div>
    </div>
  );
}

