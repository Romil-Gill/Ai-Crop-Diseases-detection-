import React from 'react';
import { Thermometer, Droplets, CloudRain, Wind } from 'lucide-react';

interface WeatherMetricProps {
  type: 'temp' | 'humidity' | 'precip' | 'wind';
  value: string | number;
  unit: string;
  label: string;
}

export const WeatherMetric: React.FC<WeatherMetricProps> = ({ type, value, unit, label }) => {
  const icon = {
    temp: <Thermometer className="w-4 h-4 text-amber-500" />,
    humidity: <Droplets className="w-4 h-4 text-blue-500" />,
    precip: <CloudRain className="w-4 h-4 text-indigo-500" />,
    wind: <Wind className="w-4 h-4 text-slate-500" />,
  }[type];

  return (
    <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200 space-y-1">
      <div className="flex items-center gap-1.5 text-[11px] font-bold text-slate-600 font-outfit uppercase tracking-wider">
        {icon}
        <span>{label}</span>
      </div>
      <div className="text-sm sm:text-base font-extrabold font-outfit text-slate-900">
        {value} <span className="text-xs font-normal text-slate-500">{unit}</span>
      </div>
    </div>
  );
};
