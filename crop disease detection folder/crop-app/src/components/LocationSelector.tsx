import React, { useState, useEffect, useRef } from 'react';
import type { LocationSearchResult } from '../types/api';
import { searchLocations } from '../services/api';
import { Search, MapPin, Navigation, Loader2 } from 'lucide-react';

interface LocationSelectorProps {
  selectedLocation: LocationSearchResult | null;
  onSelectLocation: (loc: LocationSearchResult) => void;
}

// Default fallback location for quick demo (Ambala, Haryana)
export const DEFAULT_DEMO_LOCATION: LocationSearchResult = {
  name: 'Ambala',
  admin1: 'Haryana',
  country: 'India',
  latitude: 30.3782,
  longitude: 76.7767,
  timezone: 'Asia/Kolkata',
};

export const LocationSelector: React.FC<LocationSelectorProps> = ({
  selectedLocation,
  onSelectLocation,
}) => {
  const [query, setQuery] = useState<string>('');
  const [results, setResults] = useState<LocationSearchResult[]>([]);
  const [isSearching, setIsSearching] = useState<boolean>(false);
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [geoLocating, setGeoLocating] = useState<boolean>(false);
  const [geoError, setGeoError] = useState<string | null>(null);

  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!query || query.trim().length < 2) {
      setResults([]);
      return;
    }

    const timer = setTimeout(() => {
      setIsSearching(true);
      searchLocations(query)
        .then((res) => {
          setResults(res.results || []);
          setIsOpen(true);
        })
        .finally(() => setIsSearching(false));
    }, 300);

    return () => clearTimeout(timer);
  }, [query]);

  // Click outside listener to close search dropdown
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleUseBrowserGeolocation = () => {
    if (!navigator.geolocation) {
      setGeoError('Geolocation is not supported by your browser.');
      return;
    }

    setGeoLocating(true);
    setGeoError(null);

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const userLoc: LocationSearchResult = {
          name: 'Current Location',
          admin1: 'Local Region',
          country: 'India',
          latitude: roundNum(position.coords.latitude),
          longitude: roundNum(position.coords.longitude),
          timezone: 'Asia/Kolkata',
        };
        onSelectLocation(userLoc);
        setGeoLocating(false);
        setIsOpen(false);
      },
      (err) => {
        setGeoLocating(false);
        if (err.code === err.PERMISSION_DENIED) {
          setGeoError('Location permission denied. Please search for your city/district manually.');
        } else {
          setGeoError('Could not retrieve your position. Please enter city manually.');
        }
      },
      { timeout: 8000 }
    );
  };

  const roundNum = (n: number) => Math.round(n * 10000) / 10000;

  return (
    <div className="space-y-3" ref={containerRef}>
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <label className="text-xs font-bold text-slate-800 uppercase tracking-wider font-outfit flex items-center gap-1.5">
          <MapPin className="w-3.5 h-3.5 text-blue-600" />
          <span>Select Field Location (City / District)</span>
        </label>
        <button
          type="button"
          onClick={handleUseBrowserGeolocation}
          disabled={geoLocating}
          className="inline-flex items-center gap-1.5 text-xs text-blue-700 font-bold hover:text-blue-900 transition-colors self-start sm:self-auto"
        >
          {geoLocating ? (
            <Loader2 className="w-3.5 h-3.5 animate-spin" />
          ) : (
            <Navigation className="w-3.5 h-3.5" />
          )}
          <span>Use my location</span>
        </button>
      </div>

      {geoError && (
        <p className="text-[11px] text-amber-700 font-medium bg-amber-50 p-2 rounded-xl border border-amber-200">
          {geoError}
        </p>
      )}

      {/* Search Input Box */}
      <div className="relative">
        <div className="relative flex items-center">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 pointer-events-none" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onFocus={() => setIsOpen(results.length > 0)}
            placeholder="Search city (e.g. Ambala, Karnal, Nashik)..."
            className="w-full pl-10 pr-10 py-2.5 bg-slate-50 border border-slate-200 rounded-2xl text-xs font-medium text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all"
          />
          {isSearching && (
            <Loader2 className="w-4 h-4 text-slate-400 animate-spin absolute right-3.5" />
          )}
        </div>

        {/* Dropdown Results */}
        {isOpen && results.length > 0 && (
          <div className="absolute z-30 top-full left-0 right-0 mt-1.5 bg-white border border-slate-200 rounded-2xl shadow-xl overflow-hidden max-h-56 overflow-y-auto">
            {results.map((loc, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => {
                  onSelectLocation(loc);
                  setQuery('');
                  setIsOpen(false);
                }}
                className="w-full px-4 py-2.5 text-left text-xs hover:bg-blue-50 border-b border-slate-100 last:border-0 transition-colors flex items-center justify-between"
              >
                <div>
                  <span className="font-bold text-slate-900 font-outfit">{loc.name}</span>
                  {loc.admin1 && <span className="text-slate-500 ml-1">, {loc.admin1}</span>}
                  <span className="text-slate-400 ml-1">({loc.country})</span>
                </div>
                <span className="text-[10px] text-slate-400 font-mono">
                  {loc.latitude}°N, {loc.longitude}°E
                </span>
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Selected Location Pill */}
      {selectedLocation && (
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-blue-50 border border-blue-200 text-xs font-medium text-blue-900">
          <MapPin className="w-3.5 h-3.5 text-blue-600 shrink-0" />
          <span>
            Active Location: <strong>{selectedLocation.name}</strong>
            {selectedLocation.admin1 && `, ${selectedLocation.admin1}`} ({selectedLocation.latitude.toFixed(2)}°N, {selectedLocation.longitude.toFixed(2)}°E)
          </span>
        </div>
      )}
    </div>
  );
};
