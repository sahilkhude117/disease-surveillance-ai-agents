'use client';

import React, { useState, useEffect, useMemo } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { Icon } from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-defaulticon-compatibility';
import 'leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css';
import { Card } from './ui/card';
import { Badge } from './ui/badge';

// Mock data for surveillance locations
const mockLocations = [
  { id: 1, name: 'Mumbai Central', lat: 19.0760, lng: 72.8777, severity: 'critical', cases: 245, disease: 'Dengue' },
  { id: 2, name: 'Thane', lat: 19.2183, lng: 72.9781, severity: 'high', cases: 156, disease: 'Malaria' },
  { id: 3, name: 'Kalyan', lat: 19.2403, lng: 73.1305, severity: 'medium', cases: 87, disease: 'Typhoid' },
  { id: 4, name: 'Karjat', lat: 18.9107, lng: 73.3206, severity: 'low', cases: 34, disease: 'Viral Fever' },
  { id: 5, name: 'Airoli', lat: 19.1592, lng: 72.9988, severity: 'medium', cases: 92, disease: 'Dengue' },
  { id: 6, name: 'Kalwa', lat: 19.2056, lng: 73.0008, severity: 'high', cases: 134, disease: 'Leptospirosis' },
  { id: 7, name: 'Goregaon', lat: 19.1653, lng: 72.8526, severity: 'critical', cases: 198, disease: 'Dengue' },
  { id: 8, name: 'Delhi', lat: 28.7041, lng: 77.1025, severity: 'high', cases: 189, disease: 'COVID-19' },
  { id: 9, name: 'New York', lat: 40.7128, lng: -74.0060, severity: 'medium', cases: 87, disease: 'Influenza' },
  { id: 10, name: 'London', lat: 51.5074, lng: -0.1278, severity: 'low', cases: 34, disease: 'Common Cold' },
  { id: 11, name: 'Tokyo', lat: 35.6762, lng: 139.6503, severity: 'medium', cases: 92, disease: 'Flu' },
  { id: 12, name: 'São Paulo', lat: -23.5505, lng: -46.6333, severity: 'high', cases: 156, disease: 'Zika' },
  { id: 13, name: 'Sydney', lat: -33.8688, lng: 151.2093, severity: 'low', cases: 28, disease: 'RSV' },
  { id: 14, name: 'Cairo', lat: 30.0444, lng: 31.2357, severity: 'medium', cases: 73, disease: 'Cholera' },
  { id: 15, name: 'Mexico City', lat: 19.4326, lng: -99.1332, severity: 'high', cases: 167, disease: 'Dengue' },
  { id: 16, name: 'Singapore', lat: 1.3521, lng: 103.8198, severity: 'critical', cases: 203, disease: 'Dengue' },
];

const severityColors = {
  critical: '#ef4444',
  high: '#f97316',
  medium: '#eab308',
  low: '#22c55e',
};

// Create custom marker icons with severity colors
const createCustomIcon = (severity: string) => {
  const color = severityColors[severity as keyof typeof severityColors] || '#6b7280';
  
  const svgIcon = `
    <svg width="32" height="42" viewBox="0 0 32 42" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <filter id="shadow-${severity}" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur in="SourceAlpha" stdDeviation="2"/>
          <feOffset dx="0" dy="2" result="offsetblur"/>
          <feComponentTransfer>
            <feFuncA type="linear" slope="0.3"/>
          </feComponentTransfer>
          <feMerge>
            <feMergeNode/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
      </defs>
      <path d="M16 0C7.163 0 0 7.163 0 16c0 12 16 26 16 26s16-14 16-26c0-8.837-7.163-16-16-16z" 
            fill="${color}" filter="url(#shadow-${severity})"/>
      <circle cx="16" cy="16" r="6" fill="white"/>
      ${severity === 'critical' ? '<circle cx="16" cy="16" r="4" fill="' + color + '"/>' : ''}
    </svg>
  `;
  
  return new Icon({
    iconUrl: 'data:image/svg+xml;base64,' + btoa(svgIcon),
    iconSize: [32, 42],
    iconAnchor: [16, 42],
    popupAnchor: [0, -42],
  });
};

const SurveillanceMap = () => {
  const [isMounted, setIsMounted] = useState(false);
  // Generate a unique key only once when component mounts
  const mapKey = useMemo(() => `map-${Math.random().toString(36).substr(2, 9)}`, []);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  const severityCounts = mockLocations.reduce((acc, loc) => {
    acc[loc.severity] = (acc[loc.severity] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  if (!isMounted) {
    return (
      <div className="space-y-4">
        <Card className="glass p-6 border-white/10">
          <div className="h-[500px] flex items-center justify-center">
            <p className="text-white/60">Loading map...</p>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div>
      <Card className="glass border-white/10">
        <div className="h-[500px] rounded-lg overflow-hidden">
          <style>
            {`
              .leaflet-popup-content-wrapper, .leaflet-popup-tip {
                background-color: rgba(28, 25, 23, 0.95);
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
              }
              .leaflet-popup-content {
                color: white;
                font-family: 'Poppins', sans-serif;
              }
              .leaflet-popup-close-button {
                color: white !important;
              }
            `}
          </style>
          <MapContainer
            key={mapKey}
            center={[20, 0]}
            zoom={2}
            style={{ height: '100%', width: '100%', background: '#000' }}
            className="rounded-lg"
            scrollWheelZoom={true}
            zoomControl={true}
          >
            <TileLayer
              url="https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png?api_key=89476961-3991-4c69-b35b-4badb757ae5d"
              attribution='&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
              maxZoom={20}
            />
            {mockLocations.map((location) => (
              <Marker
                key={location.id}
                position={[location.lat, location.lng]}
                icon={createCustomIcon(location.severity)}
              >
                <Popup>
                  <div className="text-white space-y-2">
                    <h4 className="font-semibold text-base">{location.name}</h4>
                    <div className="space-y-1 text-sm">
                      <div className="flex justify-between gap-4">
                        <span className="text-white/60">Disease:</span>
                        <span className="font-medium">{location.disease}</span>
                      </div>
                      <div className="flex justify-between gap-4">
                        <span className="text-white/60">Cases:</span>
                        <span className="font-medium">{location.cases}</span>
                      </div>
                      <div className="flex justify-between gap-4 items-center">
                        <span className="text-white/60">Severity:</span>
                        <Badge
                          className="capitalize text-xs"
                          style={{
                            backgroundColor: severityColors[location.severity as keyof typeof severityColors],
                          }}
                        >
                          {location.severity}
                        </Badge>
                      </div>
                    </div>
                  </div>
                </Popup>
              </Marker>
            ))}
          </MapContainer>
        </div>
      </Card>

      {/* Stats summary */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {Object.entries(severityColors).map(([severity, color]) => (
          <Card key={severity} className="glass p-4 border-white/10">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full flex items-center justify-center" style={{ backgroundColor: `${color}20` }}>
                <div className="w-4 h-4 rounded-full" style={{ backgroundColor: color }} />
              </div>
              <div>
                <p className="text-2xl font-bold text-white">{severityCounts[severity] || 0}</p>
                <p className="text-xs text-white/60 capitalize">{severity}</p>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default SurveillanceMap;
