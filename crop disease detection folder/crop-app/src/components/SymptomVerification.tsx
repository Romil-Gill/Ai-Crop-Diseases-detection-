import React, { useState, useEffect } from 'react';
import type { SymptomQuestion, FieldSpreadOption, SymptomVerifyResponse } from '../types/api';
import { getSymptomQuestions, verifySymptoms } from '../services/api';
import { VerificationQuestion } from './VerificationQuestion';
import { FieldSpreadSelector } from './FieldSpreadSelector';
import { EvidenceSummary } from './EvidenceSummary';
import { ClipboardCheck, Loader2, Sparkles, CheckCircle2, AlertTriangle } from 'lucide-react';

interface SymptomVerificationProps {
  className: string;
  confidence: number;
  isHealthy: boolean;
  crop: string;
  condition: string;
  onScanAnotherLeaf?: () => void;
}

export const SymptomVerification: React.FC<SymptomVerificationProps> = ({
  className,
  confidence,
  isHealthy,
  crop,
  condition,
  onScanAnotherLeaf,
}) => {
  const [questions, setQuestions] = useState<SymptomQuestion[]>([]);
  const [fieldSpreadOptions, setFieldSpreadOptions] = useState<FieldSpreadOption[]>([]);
  const [answers, setAnswers] = useState<Record<string, 'yes' | 'no' | 'unsure'>>({});
  const [selectedSpread, setSelectedSpread] = useState<string>('only_this_leaf');
  const [loadingQuestions, setLoadingQuestions] = useState<boolean>(false);
  const [evaluating, setEvaluating] = useState<boolean>(false);
  const [verificationResult, setVerificationResult] = useState<SymptomVerifyResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Healthy plant symptom check state
  const [healthyOtherSymptoms, setHealthyOtherSymptoms] = useState<'yes' | 'no' | 'unsure' | ''>('');

  useEffect(() => {
    if (isHealthy) return;

    let isMounted = true;
    setLoadingQuestions(true);
    setError(null);

    getSymptomQuestions(className)
      .then((res) => {
        if (!isMounted) return;
        setQuestions(res.questions || []);
        setFieldSpreadOptions(res.field_spread_options || []);
        // Initialize default answers as empty or unsure
        const initial: Record<string, 'yes' | 'no' | 'unsure'> = {};
        (res.questions || []).forEach((q) => {
          initial[q.id] = 'yes'; // Default to Yes for fast verification UX
        });
        setAnswers(initial);
      })
      .catch((err) => {
        if (!isMounted) return;
        setError(err.message || 'Failed to load symptom verification questions.');
      })
      .finally(() => {
        if (isMounted) setLoadingQuestions(false);
      });

    return () => {
      isMounted = false;
    };
  }, [className, isHealthy]);

  const handleAnswerChange = (qId: string, val: 'yes' | 'no' | 'unsure') => {
    setAnswers((prev) => ({ ...prev, [qId]: val }));
  };

  const handleEvaluate = async () => {
    setEvaluating(true);
    setError(null);
    try {
      const res = await verifySymptoms(className, answers, selectedSpread);
      setVerificationResult(res);
    } catch (err: any) {
      setError(err.message || 'Failed to evaluate field concern.');
    } finally {
      setEvaluating(false);
    }
  };

  // ---------------------------------------------------------------------------
  // HEALTHY LEAF RENDER
  // ---------------------------------------------------------------------------
  if (isHealthy) {
    return (
      <div className="w-full bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-4">
        <div className="flex items-center gap-2 font-bold font-outfit text-slate-900 text-base">
          <CheckCircle2 className="w-5 h-5 text-emerald-600" />
          <span>Foliage Check Summary</span>
        </div>
        <p className="text-xs text-slate-600 leading-relaxed font-sans">
          This leaf sample appears healthy with no visible signs of {condition.toLowerCase()}.
        </p>

        <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-3">
          <label className="block text-xs font-bold text-slate-800 font-outfit">
            Are you seeing symptoms (yellowing, spots, or wilting) elsewhere on this plant?
          </label>
          <div className="flex items-center gap-2">
            {(['yes', 'no', 'unsure'] as const).map((val) => (
              <button
                key={val}
                type="button"
                onClick={() => setHealthyOtherSymptoms(val)}
                className={`py-1.5 px-3 rounded-xl text-xs font-bold capitalize transition-all ${
                  healthyOtherSymptoms === val
                    ? 'bg-slate-900 text-white shadow-xs'
                    : 'bg-white text-slate-700 border border-slate-200 hover:bg-slate-100'
                }`}
              >
                {val === 'unsure' ? 'Not sure' : val}
              </button>
            ))}
          </div>
        </div>

        {healthyOtherSymptoms === 'yes' && (
          <div className="p-4 rounded-2xl bg-amber-50 border border-amber-200 text-amber-950 text-xs space-y-2 font-sans">
            <div className="flex items-center gap-1.5 font-bold font-outfit text-amber-900">
              <AlertTriangle className="w-4 h-4 text-amber-700 shrink-0" />
              <span>Inspect Other Leaves</span>
            </div>
            <p>
              This leaf appears healthy, but symptoms elsewhere on the vine or stalk should be scanned separately.
            </p>
            {onScanAnotherLeaf && (
              <button
                type="button"
                onClick={onScanAnotherLeaf}
                className="px-3.5 py-1.5 rounded-xl bg-amber-700 text-white font-bold text-xs hover:bg-amber-800 transition-colors shadow-2xs mt-1"
              >
                Scan another leaf image
              </button>
            )}
          </div>
        )}
      </div>
    );
  }

  // ---------------------------------------------------------------------------
  // DISEASE LEAF RENDER
  // ---------------------------------------------------------------------------
  return (
    <div className="w-full bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-100">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-100/90 text-blue-900 text-xs font-bold mb-2 border border-blue-300/80 font-mono">
            <ClipboardCheck className="w-3.5 h-3.5 text-blue-700" />
            <span>Symptom Verification & Field Triage</span>
          </div>
          <h3 className="text-xl sm:text-2xl font-extrabold font-outfit text-slate-900">
            Help verify this assessment
          </h3>
          <p className="text-sm text-slate-600 mt-0.5 font-medium">
            Answer a few quick questions about what you can see on the {crop} plant.
          </p>
        </div>
      </div>

      {loadingQuestions && (
        <div className="py-8 text-center space-y-2">
          <Loader2 className="w-6 h-6 text-emerald-600 animate-spin mx-auto" />
          <p className="text-xs text-slate-500 font-medium">Loading symptom questions...</p>
        </div>
      )}

      {error && (
        <div className="p-4 rounded-2xl bg-rose-50 border border-rose-200 text-xs text-rose-800 font-medium">
          {error}
        </div>
      )}

      {!loadingQuestions && questions.length > 0 && (
        <div className="space-y-6">
          {/* Question List */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 font-outfit">
              Observed Symptoms (Select Yes / No / Not Sure)
            </h4>
            {questions.map((q) => (
              <VerificationQuestion
                key={q.id}
                question={q}
                currentAnswer={answers[q.id] || ''}
                onAnswer={handleAnswerChange}
              />
            ))}
          </div>

          {/* Field Spread Question */}
          {fieldSpreadOptions.length > 0 && (
            <FieldSpreadSelector
              options={fieldSpreadOptions}
              selectedOption={selectedSpread}
              onSelect={setSelectedSpread}
            />
          )}

          {/* Evaluate Action Button */}
          <div>
            <button
              type="button"
              onClick={handleEvaluate}
              disabled={evaluating}
              className="w-full py-3.5 px-6 rounded-2xl bg-emerald-600 hover:bg-emerald-700 active:scale-[0.99] text-white font-bold text-xs sm:text-sm transition-all shadow-md shadow-emerald-600/20 flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {evaluating ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Evaluating Field Concern...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4 text-emerald-200" />
                  <span>Evaluate Field Concern Level</span>
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {/* Render Combined Evidence Summary once evaluated */}
      {verificationResult && (
        <EvidenceSummary
          confidence={confidence}
          verificationResult={verificationResult}
        />
      )}
    </div>
  );
};
