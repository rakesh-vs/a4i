"use client";

import { useEffect, useRef, useState } from 'react';
import { GoogleMap, LoadScript, Marker, InfoWindow } from '@react-google-maps/api';

interface LocationMarker {
  name: string;
  address: string;
  lat: number;
  lng: number;
  place_id: string;
  place_type: string;
  rating?: number | string;
  is_open?: boolean | null;
}

interface MapProps {
  locations: LocationMarker[];
  center: { lat: number; lng: number };
}

const containerStyle = {
  width: '100%',
  height: '100%'
};

export function Map({ locations, center }: MapProps) {
  const [selectedMarker, setSelectedMarker] = useState<LocationMarker | null>(null);
  const mapRef = useRef<google.maps.Map | null>(null);

  const getMarkerIcon = (placeType: string) => {
    const iconMap: Record<string, string> = {
      hospital: 'https://maps.google.com/mapfiles/ms/icons/red-dot.png',
      shelter: 'https://maps.google.com/mapfiles/ms/icons/blue-dot.png',
      emergency: 'https://maps.google.com/mapfiles/ms/icons/red-dot.png',
      pharmacy: 'https://maps.google.com/mapfiles/ms/icons/green-dot.png',
      police: 'https://maps.google.com/mapfiles/ms/icons/blue-dot.png',
      'fire station': 'https://maps.google.com/mapfiles/ms/icons/red-dot.png',
      disaster: 'https://maps.google.com/mapfiles/ms/icons/red-dot.png',
      supply: 'https://maps.google.com/mapfiles/ms/icons/orange-dot.png',
    };
    return iconMap[placeType.toLowerCase()] || 'https://maps.google.com/mapfiles/ms/icons/orange-dot.png';
  };

  useEffect(() => {
    if (mapRef.current && locations.length > 0) {
      const bounds = new google.maps.LatLngBounds();
      locations.forEach(location => {
        bounds.extend({ lat: location.lat, lng: location.lng });
      });
      mapRef.current.fitBounds(bounds);
    }
  }, [locations]);

  return (
    <LoadScript googleMapsApiKey={process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY || ''}>
      <GoogleMap
        mapContainerStyle={containerStyle}
        center={center}
        zoom={12}
        onLoad={(map) => {
          mapRef.current = map;
        }}
        options={{
          streetViewControl: false,
          mapTypeControl: false,
          fullscreenControl: true,
        }}
      >
        {locations.map((location, index) => (
          <Marker
            key={`${location.place_id}-${index}`}
            position={{ lat: location.lat, lng: location.lng }}
            onClick={() => setSelectedMarker(location)}
            icon={{
              url: getMarkerIcon(location.place_type),
              scaledSize: new google.maps.Size(32, 32),
            }}
          />
        ))}

        {selectedMarker && (
          <InfoWindow
            position={{ lat: selectedMarker.lat, lng: selectedMarker.lng }}
            onCloseClick={() => setSelectedMarker(null)}
          >
            <div style={{ maxWidth: '250px' }}>
              <h3 style={{ margin: '0 0 8px 0', fontWeight: 'bold', fontSize: '14px' }}>
                {selectedMarker.name}
              </h3>
              <p style={{ margin: '4px 0', fontSize: '12px', color: '#666' }}>
                {selectedMarker.address}
              </p>
              {selectedMarker.rating && selectedMarker.rating !== 'N/A' && (
                <p style={{ margin: '4px 0', fontSize: '12px' }}>
                  ⭐ Rating: {selectedMarker.rating}
                </p>
              )}
              {selectedMarker.is_open !== null && (
                <p style={{ margin: '4px 0', fontSize: '12px', fontWeight: 'bold' }}>
                  {selectedMarker.is_open ? '🟢 Open Now' : '🔴 Closed'}
                </p>
              )}
              <p style={{ margin: '8px 0 4px 0', fontSize: '11px', color: '#999' }}>
                Type: {selectedMarker.place_type}
              </p>
            </div>
          </InfoWindow>
        )}
      </GoogleMap>
    </LoadScript>
  );
}

