import React, { useState, useEffect } from 'react';
import type { ScanRecord } from '../types/api';
import { getScans, deleteScan } from '../services/api';
import { HistoryFilters } from './HistoryFilters';
import { ScanHistoryCard } from './ScanHistoryCard';
import { CropTimeline } from './CropTimeline';
import { History, Loader2, ArrowRight } from 'lucide-react';

interface HistoryPageProps {
  onNavigateHome: () => void;
}

export const HistoryPage: React.FC<HistoryPageProps> = ({ onNavigateHome }) => {
  const [scans, setScans] = useState<ScanRecord[]>([]);
  const [activeCrop, setActiveCrop] = useState<string>('All');
  const [loading, setLoading] = useState<boolean>(true);

  const fetchScans = (crop: string) => {
    setLoading(true);
    getScans(crop)
      .then((res) => {
        setScans(res.scans || []);
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchScans(activeCrop);
  }, [activeCrop]);

  const handleDelete = async (id: number) => {
    const ok = await deleteScan(id);
    if (ok) {
      setScans((prev) => prev.filter((s) => s.id !== id));
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto space-y-6 animate-in fade-in duration-300">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-100 text-slate-800 text-xs font-bold mb-2 font-mono">
            <History className="w-3.5 h-3.5 text-slate-700" />
            <span>SQLite Local Scan Repository</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold font-outfit text-slate-900">
            Assessment History
          </h2>
          <p className="text-xs sm:text-sm text-slate-600 font-medium">
            Review your previously saved reliable crop health assessments.
          </p>
        </div>
      </div>

      {/* Filter Tabs */}
      <HistoryFilters activeCrop={activeCrop} onSelectCrop={setActiveCrop} />

      {loading && (
        <div className="py-12 text-center space-y-2">
          <Loader2 className="w-6 h-6 text-emerald-600 animate-spin mx-auto" />
          <p className="text-xs text-slate-500 font-medium">Loading saved scan records...</p>
        </div>
      )}

      {!loading && scans.length > 0 && (
        <div className="space-y-6">
          <CropTimeline scans={scans} />

          <div className="space-y-4">
            {scans.map((scan) => (
              <ScanHistoryCard key={scan.id} scan={scan} onDelete={handleDelete} />
            ))}
          </div>
        </div>
      )}

      {!loading && scans.length === 0 && (
        <div className="py-16 text-center bg-white rounded-3xl border border-slate-200 p-8 space-y-4 shadow-sm">
          <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center mx-auto text-slate-400">
            <History className="w-6 h-6" />
          </div>
          <div className="space-y-1">
            <h4 className="text-lg font-bold font-outfit text-slate-900">
              No saved assessments yet
            </h4>
            <p className="text-xs text-slate-500 max-w-sm mx-auto">
              Scan a crop leaf and save your assessment to track health trends over time.
            </p>
          </div>
          <button
            type="button"
            onClick={onNavigateHome}
            className="px-5 py-2.5 rounded-2xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs font-outfit shadow-sm inline-flex items-center gap-2"
          >
            <span>Scan your first crop</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      )}
    </div>
  );
};
