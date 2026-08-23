import React from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import type { RadarAreaItem } from '../types/api';
import 'leaflet/dist/leaflet.css';
import { Shield, Radio, MapPin } from 'lucide-react';

interface RadarMapProps {
  areas: RadarAreaItem[];
  isDemoMode?: boolean;
}

export const RadarMap: React.FC<RadarMapProps> = ({ areas, isDemoMode = false }) => {
  // Default map center around Haryana & North India
  const centerLat = areas.length > 0 ? areas[0].map_lat : 30.1;
  const centerLon = areas.length > 0 ? areas[0].map_lon : 76.9;

  const getActivityColor = (level: string) => {
    switch (level) {
      case 'ELEVATED':
        return '#ef4444'; // coral/red
      case 'MODERATE':
        return '#f59e0b'; // amber/orange
      default:
        return '#10b981'; // emerald/teal
    }
  };

  return (
    <div className="space-y-2">
      <div className="relative w-full rounded-3xl overflow-hidden border border-slate-200 shadow-md">
        <MapContainer
          center={[centerLat, centerLon]}
          zoom={8}
          scrollWheelZoom={false}
          className="w-full h-[400px] sm:h-[450px] z-10"
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {areas.map((area, idx) => {
            const color = getActivityColor(area.activity_level);
            const radius = Math.min(18 + area.signal_count * 3, 38);

            return (
              <CircleMarker
                key={`${area.area_name}_${idx}`}
                center={[area.map_lat, area.map_lon]}
                radius={radius}
                pathOptions={{
                  color,
                  fillColor: color,
                  fillOpacity: 0.55,
                  weight: 2,
                }}
              >
                <Popup className="font-outfit">
                  <div className="p-1 space-y-2 max-w-[220px]">
                    <div className="flex items-center justify-between border-b border-slate-200 pb-1.5">
                      <div className="flex items-center gap-1 font-extrabold text-sm text-slate-900">
                        <MapPin className="w-3.5 h-3.5 text-blue-600" />
                        <span>{area.area_name} Area</span>
                      </div>
                      <span
                        className="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold text-white uppercase"
                        style={{ backgroundColor: color }}
                      >
                        {area.activity_level}
                      </span>
                    </div>

                    <div className="text-xs space-y-1 text-slate-700">
                      <div className="font-bold text-slate-900">
                        {area.signal_count} Community Signal{area.signal_count > 1 ? 's' : ''}
                      </div>

                      <div className="space-y-0.5 text-[11px] text-slate-600 font-medium">
                        {area.conditions.map((c, i) => (
                          <div key={i} className="flex justify-between">
                            <span>{c.crop} • {c.condition}:</span>
                            <span className="font-bold font-mono text-slate-900">{c.count}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="text-[9px] text-slate-500 italic border-t border-slate-100 pt-1 leading-tight">
                      * Coarsened position ({area.map_lat}°N, {area.map_lon}°E). Community report.
                    </div>
                  </div>
                </Popup>
              </CircleMarker>
            );
          })}
        </MapContainer>

        {/* Map Legend Overlay */}
        <div className="absolute bottom-3 left-3 z-20 p-2.5 rounded-2xl glass-panel border border-slate-200 shadow-md text-xs font-outfit space-y-1">
          <div className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">
            Activity Level Legend
          </div>
          <div className="flex items-center gap-3 text-[11px] font-semibold text-slate-800">
            <div className="flex items-center gap-1">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
              <span>Low</span>
            </div>
            <div className="flex items-center gap-1">
              <span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
              <span>Moderate</span>
            </div>
            <div className="flex items-center gap-1">
              <span className="w-2.5 h-2.5 rounded-full bg-rose-500"></span>
              <span>Elevated</span>
            </div>
          </div>
        </div>
      </div>

      {/* Mandatory Map Privacy Disclaimer */}
      <div className="p-3 rounded-2xl bg-slate-100 border border-slate-200 text-[11px] text-slate-600 flex items-start gap-2 leading-relaxed">
        <Shield className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
        <span>
          <strong>Farmer Privacy Guarantee:</strong> Map locations are deliberately coarsened to 1 decimal place (~11km area grid) to protect farm location and personal identity. Signals represent community-reported assessments, not laboratory-confirmed cases.
        </span>
      </div>
    </div>
  );
};
