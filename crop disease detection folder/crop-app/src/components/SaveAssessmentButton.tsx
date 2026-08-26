import React, { useState } from 'react';
import type { ScanRecord } from '../types/api';
import { saveScan } from '../services/api';
import { Bookmark, Check, Loader2 } from 'lucide-react';

interface SaveAssessmentButtonProps {
  crop: string;
  className: string;
  condition: string;
  confidence: number;
  isHealthy: boolean;
  locationName?: string;
  symptomAgreement?: string;
  symptomScore?: number;
  fieldConcern?: string;
  weatherFavorability?: string;
  onSaved?: (record: ScanRecord) => void;
}

export const SaveAssessmentButton: React.FC<SaveAssessmentButtonProps> = ({
  crop,
  className,
  condition,
  confidence,
  isHealthy,
  locationName = 'Local Field',
  symptomAgreement,
  symptomScore,
  fieldConcern,
  weatherFavorability,
  onSaved,
}) => {
  const [saving, setSaving] = useState<boolean>(false);
  const [savedRecord, setSavedRecord] = useState<ScanRecord | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSave = async () => {
    if (savedRecord) return;
    setSaving(true);
    setError(null);

    try {
      const payload: Partial<ScanRecord> = {
        crop,
        class_name: className,
        condition,
        model_confidence: confidence,
        is_healthy: isHealthy,
        location_name: locationName,
        symptom_agreement: symptomAgreement || null,
        symptom_match_score: symptomScore ?? null,
        field_concern: fieldConcern || null,
        weather_favorability: weatherFavorability || null,
      };

      const res = await saveScan(payload);
      setSavedRecord(res.scan);
      if (onSaved) onSaved(res.scan);
    } catch (err: any) {
      setError(err.message || 'Assessment could not be saved.');
    } finally {
      setSaving(false);
    }
  };

  if (savedRecord) {
    return (
      <div className="inline-flex items-center gap-2 px-4 py-2 rounded-2xl bg-emerald-100 text-emerald-950 text-xs font-bold border border-emerald-300 font-outfit shadow-2xs">
        <Check className="w-4 h-4 text-emerald-700" />
        <span>Assessment Saved</span>
      </div>
    );
  }

  return (
    <div className="space-y-1.5">
      <button
        type="button"
        onClick={handleSave}
        disabled={saving}
        className="px-5 py-2.5 rounded-2xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs sm:text-sm transition-all shadow-sm flex items-center justify-center gap-2 disabled:opacity-50 font-outfit"
      >
        {saving ? (
          <>
            <Loader2 className="w-4 h-4 animate-spin text-slate-300" />
            <span>Saving Assessment...</span>
          </>
        ) : (
          <>
            <Bookmark className="w-4 h-4 text-emerald-400" />
            <span>Save Assessment</span>
          </>
        )}
      </button>

      {error && (
        <p className="text-[11px] text-rose-600 font-medium">
          {error}
        </p>
      )}
    </div>
  );
};
