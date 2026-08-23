import React, { useState, useEffect, useRef } from 'react';
import { Header } from './components/Header';
import { Footer } from './components/Footer';
import { CropSelector } from './components/CropSelector';
import { ImageUploader } from './components/ImageUploader';
import { ScanPreview } from './components/ScanPreview';
import { AnalysisLoader } from './components/AnalysisLoader';
import { DiagnosisCard } from './components/DiagnosisCard';
import { GradCamVisualizer } from './components/GradCamVisualizer';
import { TopPredictions } from './components/TopPredictions';
import { UncertainState } from './components/UncertainState';
import { ErrorState } from './components/ErrorState';

import type { SupportedCrop, PredictResponse } from './types/api';
import { checkHealth, explainDisease } from './services/api';
import { Sparkles, ArrowRight, RefreshCcw } from 'lucide-react';

export const App: React.FC = () => {
  // Application States
  const [selectedCrop, setSelectedCrop] = useState<SupportedCrop | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [imagePreviewUrl, setImagePreviewUrl] = useState<string | null>(null);
  
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);
  const [analysisResult, setAnalysisResult] = useState<PredictResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [serverOnline, setServerOnline] = useState<boolean | null>(null);

  const scannerRef = useRef<HTMLDivElement>(null);

  // Check Backend Server Health on Mount
  useEffect(() => {
    const verifyBackend = async () => {
      try {
        const health = await checkHealth();
        setServerOnline(health.model_loaded);
      } catch {
        setServerOnline(false);
      }
    };
    verifyBackend();
  }, []);

  // Handle Image File Selection
  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
    const previewUrl = URL.createObjectURL(file);
    setImagePreviewUrl(previewUrl);
    setAnalysisResult(null);
    setErrorMessage(null);
  };

  // Handle Image Reset
  const handleResetUpload = () => {
    setSelectedFile(null);
    if (imagePreviewUrl) {
      URL.revokeObjectURL(imagePreviewUrl);
    }
    setImagePreviewUrl(null);
    setAnalysisResult(null);
    setErrorMessage(null);
  };

  // Handle Full Workflow Reset
  const handleResetAll = () => {
    handleResetUpload();
    setSelectedCrop(null);
  };

  // Scroll to Scan Area
  const scrollToScan = () => {
    scannerRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Handle AI Analysis & Grad-CAM Explanation Call to Flask Backend
  const handleAnalyze = async () => {
    if (!selectedFile || !selectedCrop) return;

    setIsAnalyzing(true);
    setErrorMessage(null);
    setAnalysisResult(null);

    try {
      const response = await explainDisease(selectedFile, selectedCrop);
      setAnalysisResult(response);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setErrorMessage(err.message);
      } else {
        setErrorMessage('An unexpected error occurred during prediction analysis.');
      }
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#f8faf7] text-slate-800 antialiased selection:bg-emerald-200 selection:text-emerald-900">
      
      {/* Header Bar */}
      <Header 
        serverOnline={serverOnline}
        selectedCrop={selectedCrop}
        onReset={handleResetAll}
      />

      <main className="flex-1 max-w-6xl w-full mx-auto px-4 sm:px-6 py-8 space-y-10">
        
        {/* HERO SECTION */}
        <section className="text-center max-w-3xl mx-auto space-y-4 pt-4 sm:pt-6">
          <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-emerald-100/90 text-emerald-800 border border-emerald-300 text-xs font-bold shadow-2xs">
            <Sparkles className="w-3.5 h-3.5 text-emerald-600" />
            <span>MobileNetV2 AI Engine • 27 Crop Classes</span>
          </div>

          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-emerald-950 font-outfit tracking-tight leading-[1.1]">
            Fasal<span className="text-emerald-600">Rakshak</span> AI
          </h1>

          <p className="text-base sm:text-lg text-slate-600 font-medium max-w-2xl mx-auto leading-relaxed">
            Know what your crop needs before the damage spreads. Upload a leaf photo for fast, explainable AI diagnosis.
          </p>

          <div className="pt-2 flex items-center justify-center gap-3">
            <button
              onClick={scrollToScan}
              className="px-6 py-3.5 rounded-2xl bg-gradient-to-r from-emerald-800 to-green-700 hover:from-emerald-900 hover:to-green-800 text-white font-bold text-sm shadow-md shadow-emerald-800/20 active:scale-95 transition-all flex items-center gap-2"
            >
              <span>Scan Crop Leaf</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>

          {/* Quick Stats Grid */}
          <div className="pt-6 grid grid-cols-3 gap-3 max-w-lg mx-auto">
            <div className="bg-white/80 border border-slate-200/80 rounded-2xl p-3 shadow-2xs">
              <span className="text-xl sm:text-2xl font-black text-emerald-800 font-outfit block">4</span>
              <span className="text-[11px] font-semibold text-slate-500">Supported Crops</span>
            </div>
            <div className="bg-white/80 border border-slate-200/80 rounded-2xl p-3 shadow-2xs">
              <span className="text-xl sm:text-2xl font-black text-emerald-800 font-outfit block">27</span>
              <span className="text-[11px] font-semibold text-slate-500">Disease & Healthy</span>
            </div>
            <div className="bg-white/80 border border-slate-200/80 rounded-2xl p-3 shadow-2xs">
              <span className="text-xl sm:text-2xl font-black text-emerald-800 font-outfit block">Real</span>
              <span className="text-[11px] font-semibold text-slate-500">TensorFlow AI</span>
            </div>
          </div>
        </section>

        {/* STEP 1: CROP SELECTOR */}
        <section ref={scannerRef} className="pt-4 scroll-mt-20">
          <CropSelector
            selectedCrop={selectedCrop}
            onSelectCrop={(crop) => {
              setSelectedCrop(crop);
              setAnalysisResult(null);
              setErrorMessage(null);
            }}
          />
        </section>

        {/* STEP 2: UPLOAD & ANALYSIS WORKFLOW */}
        <section className="space-y-6">
          
          {/* State 1: No file uploaded yet */}
          {!selectedFile && !isAnalyzing && !analysisResult && !errorMessage && (
            <ImageUploader
              selectedCrop={selectedCrop}
              onFileSelect={handleFileSelect}
            />
          )}

          {/* State 2: Image uploaded & Preview ready */}
          {selectedFile && imagePreviewUrl && !isAnalyzing && !analysisResult && !errorMessage && (
            <ScanPreview
              imageSrc={imagePreviewUrl}
              selectedCrop={selectedCrop!}
              onAnalyze={handleAnalyze}
              onReplace={handleResetUpload}
              onRemove={handleResetUpload}
              isLoading={isAnalyzing}
            />
          )}

          {/* State 3: Analysis in Progress */}
          {isAnalyzing && imagePreviewUrl && (
            <AnalysisLoader
              imageSrc={imagePreviewUrl}
              selectedCrop={selectedCrop!}
            />
          )}

          {/* State 4: Error State */}
          {errorMessage && (
            <ErrorState
              errorMessage={errorMessage}
              onRetry={() => {
                setErrorMessage(null);
                if (selectedFile) handleAnalyze();
              }}
            />
          )}

          {/* State 5: Successful / Reliable Diagnosis */}
          {analysisResult && analysisResult.diagnosis_reliable && (
            <div className="space-y-6">
              <DiagnosisCard result={analysisResult} />
              
              {/* Grad-CAM Explainable AI Overlay (Only for reliable diagnoses) */}
              {analysisResult.explanation && imagePreviewUrl && (
                <GradCamVisualizer
                  explanation={analysisResult.explanation}
                  originalImageUrl={imagePreviewUrl}
                />
              )}

              <TopPredictions predictions={analysisResult.top_predictions} />

              {/* Action Button to Scan Another Leaf */}
              <div className="text-center pt-2">
                <button
                  onClick={handleResetUpload}
                  className="px-6 py-3 rounded-2xl bg-white border border-slate-300 hover:bg-slate-50 text-slate-800 text-xs font-bold transition-all shadow-2xs inline-flex items-center gap-2"
                >
                  <RefreshCcw className="w-4 h-4 text-emerald-600" />
                  Scan Another Leaf
                </button>
              </div>
            </div>
          )}

          {/* State 6: Uncertain Diagnosis (Safe Diagnosis Gate Alert) */}
          {analysisResult && !analysisResult.diagnosis_reliable && (
            <UncertainState
              result={analysisResult}
              selectedCrop={selectedCrop}
              onResetUpload={handleResetUpload}
              onChangeCrop={() => setSelectedCrop(null)}
            />
          )}

        </section>
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
};

export default App;
