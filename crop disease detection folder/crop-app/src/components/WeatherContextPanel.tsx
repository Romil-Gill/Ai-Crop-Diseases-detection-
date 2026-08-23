import React, { useState, useEffect } from 'react';
import type { LocationSearchResult, WeatherContextResponse } from '../types/api';
import { getWeatherContext } from '../services/api';
import { LocationSelector, DEFAULT_DEMO_LOCATION } from './LocationSelector';
import { WeatherMetric } from './WeatherMetric';
import { FavorabilityCard } from './FavorabilityCard';
import { ForecastStrip } from './ForecastStrip';
import { CloudSun, Loader2, Info, ChevronDown, ChevronUp } from 'lucide-react';

interface WeatherContextPanelProps {
  className: string;
  crop: string;
  condition: string;
  isHealthy: boolean;
}

export const WeatherContextPanel: React.FC<WeatherContextPanelProps> = ({
  className,
  crop,
  condition,
  isHealthy,
}) => {
  const [selectedLocation, setSelectedLocation] = useState<LocationSearchResult>(DEFAULT_DEMO_LOCATION);
  const [weatherData, setWeatherData] = useState<WeatherContextResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [showMethodology, setShowMethodology] = useState<boolean>(false);

  useEffect(() => {
    let isMounted = true;
    setLoading(true);

    getWeatherContext(
      selectedLocation.latitude,
      selectedLocation.longitude,
      className,
      selectedLocation.name
    )
      .then((res) => {
        if (!isMounted) return;
        setWeatherData(res);
      })
      .catch(() => {
        if (!isMounted) return;
        setWeatherData(null);
      })
      .finally(() => {
        if (isMounted) setLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, [selectedLocation, className]);

  return (
    <div className="w-full bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-100">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-100/90 text-indigo-900 text-xs font-bold mb-2 border border-indigo-300/80 font-mono">
            <CloudSun className="w-3.5 h-3.5 text-indigo-700" />
            <span>Environmental Micro-Climate Context</span>
          </div>
          <h3 className="text-xl sm:text-2xl font-extrabold font-outfit text-slate-900">
            Weather Risk Context
          </h3>
          <p className="text-sm text-slate-600 mt-0.5 font-medium">
            Evaluate whether local weather conditions favor {isHealthy ? 'crop health maintenance' : `${condition.toLowerCase()} development`} on {crop}.
          </p>
        </div>
      </div>

      {/* Location Selector */}
      <LocationSelector
        selectedLocation={selectedLocation}
        onSelectLocation={setSelectedLocation}
      />

      {loading && (
        <div className="py-8 text-center space-y-2">
          <Loader2 className="w-6 h-6 text-blue-600 animate-spin mx-auto" />
          <p className="text-xs text-slate-500 font-medium">Retrieving Open-Meteo weather context for {selectedLocation.name}...</p>
        </div>
      )}

      {!loading && weatherData && weatherData.weather_available && weatherData.current && (
        <div className="space-y-5">
          {/* Current Weather Metrics Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <WeatherMetric
              type="temp"
              label="Temperature"
              value={weatherData.current.temperature_c}
              unit="°C"
            />
            <WeatherMetric
              type="humidity"
              label="Humidity"
              value={weatherData.current.humidity_percent}
              unit="%"
            />
            <WeatherMetric
              type="precip"
              label="Precipitation"
              value={weatherData.current.precipitation_mm}
              unit="mm"
            />
            <WeatherMetric
              type="wind"
              label="Wind Speed"
              value={weatherData.current.wind_kmh}
              unit="km/h"
            />
          </div>

          {/* 24h Forecast Outlook */}
          {weatherData.forecast_summary && (
            <ForecastStrip forecast={weatherData.forecast_summary} />
          )}

          {/* Disease Favorability Card */}
          <FavorabilityCard diseaseContext={weatherData.disease_context} />

          {/* Weather Methodology Transparency Toggle */}
          <div className="border-t border-slate-100 pt-3">
            <button
              type="button"
              onClick={() => setShowMethodology(!showMethodology)}
              className="flex items-center justify-between w-full text-left text-xs font-bold text-slate-700 hover:text-slate-900 transition-colors font-outfit"
            >
              <div className="flex items-center gap-1.5">
                <Info className="w-3.5 h-3.5 text-blue-600" />
                <span>Weather Methodology & Transparency</span>
              </div>
              {showMethodology ? (
                <ChevronUp className="w-4 h-4 text-slate-400" />
              ) : (
                <ChevronDown className="w-4 h-4 text-slate-400" />
              )}
            </button>

            {showMethodology && (
              <div className="mt-3 p-4 rounded-2xl bg-slate-50 border border-slate-200 text-xs text-slate-600 space-y-2 font-sans leading-relaxed">
                <p>
                  <strong>Weather Provider:</strong> Open-Meteo Global Meteorological API.
                </p>
                <p>
                  <strong>Agricultural Context:</strong> Evaluated against verified ICAR (Indian Council of Agricultural Research) and agricultural extension environmental thresholds.
                </p>
                <p>
                  <strong>Notice:</strong> Weather context indicates environmental compatibility for disease development. FasalRakshak does not use weather as proof that disease is present.
                </p>
                <p className="text-[11px] text-slate-500 italic pt-1 border-t border-slate-200/80">
                  * Note: Future India-focused production deployments may integrate IMD (India Meteorological Department) Gramin Krishi Mausam Sewa & KALP agromet advisories.
                </p>
              </div>
            )}
          </div>
        </div>
      )}

      {!loading && weatherData && !weatherData.weather_available && (
        <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 text-xs text-slate-600 space-y-1">
          <p className="font-bold text-slate-800">Weather Context Temporarily Unavailable</p>
          <p>{weatherData.message || 'Weather service is offline. Crop diagnosis and advisory remain fully functional.'}</p>
        </div>
      )}
    </div>
  );
};
