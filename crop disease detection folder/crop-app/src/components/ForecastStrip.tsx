import React from 'react';
import type { ForecastSummary } from '../types/api';
import { Calendar, Thermometer, CloudRain } from 'lucide-react';

interface ForecastStripProps {
  forecast: ForecastSummary;
}

export const ForecastStrip: React.FC<ForecastStripProps> = ({ forecast }) => {
  const { temp_max_c, temp_min_c, total_precip_mm } = forecast.next_24h;

  return (
    <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-2">
      <div className="flex items-center gap-1.5 text-xs font-bold text-slate-800 font-outfit uppercase tracking-wider">
        <Calendar className="w-3.5 h-3.5 text-blue-600" />
        <span>Next 24-Hour Weather Outlook</span>
      </div>

      <div className="grid grid-cols-2 gap-3 text-xs">
        <div className="flex items-center gap-2 font-medium text-slate-700">
          <Thermometer className="w-4 h-4 text-amber-500 shrink-0" />
          <span>
            Temp Range: <strong>{temp_min_c}°C</strong> to <strong>{temp_max_c}°C</strong>
          </span>
        </div>

        <div className="flex items-center gap-2 font-medium text-slate-700">
          <CloudRain className="w-4 h-4 text-indigo-500 shrink-0" />
          <span>
            Rain Forecast: <strong>{total_precip_mm} mm</strong>
          </span>
        </div>
      </div>
    </div>
  );
};
