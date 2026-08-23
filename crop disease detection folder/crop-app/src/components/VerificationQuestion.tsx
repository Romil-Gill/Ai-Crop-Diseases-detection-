import React from 'react';
import type { SymptomQuestion } from '../types/api';
import { Check, X, HelpCircle } from 'lucide-react';

interface VerificationQuestionProps {
  question: SymptomQuestion;
  currentAnswer: string; // 'yes' | 'no' | 'unsure' | ''
  onAnswer: (id: string, value: 'yes' | 'no' | 'unsure') => void;
}

export const VerificationQuestion: React.FC<VerificationQuestionProps> = ({
  question,
  currentAnswer,
  onAnswer,
}) => {
  return (
    <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/90 space-y-3 transition-all hover:border-slate-300">
      <p className="text-xs sm:text-sm font-semibold text-slate-800 font-outfit leading-snug">
        {question.question}
      </p>

      <div className="grid grid-cols-3 gap-2">
        <button
          type="button"
          onClick={() => onAnswer(question.id, 'yes')}
          className={`py-2 px-3 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-1.5 ${
            currentAnswer === 'yes'
              ? 'bg-emerald-600 text-white shadow-sm shadow-emerald-600/20 scale-[1.02]'
              : 'bg-white text-slate-700 border border-slate-200 hover:bg-emerald-50 hover:text-emerald-800'
          }`}
        >
          <Check className="w-3.5 h-3.5" />
          <span>Yes</span>
        </button>

        <button
          type="button"
          onClick={() => onAnswer(question.id, 'no')}
          className={`py-2 px-3 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-1.5 ${
            currentAnswer === 'no'
              ? 'bg-slate-800 text-white shadow-sm scale-[1.02]'
              : 'bg-white text-slate-700 border border-slate-200 hover:bg-slate-100 hover:text-slate-900'
          }`}
        >
          <X className="w-3.5 h-3.5" />
          <span>No</span>
        </button>

        <button
          type="button"
          onClick={() => onAnswer(question.id, 'unsure')}
          className={`py-2 px-3 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-1.5 ${
            currentAnswer === 'unsure'
              ? 'bg-amber-100 text-amber-950 border border-amber-300 shadow-2xs scale-[1.02]'
              : 'bg-white text-slate-700 border border-slate-200 hover:bg-amber-50 hover:text-amber-900'
          }`}
        >
          <HelpCircle className="w-3.5 h-3.5" />
          <span>Not Sure</span>
        </button>
      </div>
    </div>
  );
};
