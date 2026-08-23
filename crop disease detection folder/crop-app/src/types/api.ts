export type SupportedCrop = 'Tomato' | 'Rice' | 'Sugarcane' | 'Pumpkin';

export interface ClassInfo {
  class_name: string;
  condition: string;
  is_healthy: boolean;
}

export interface ClassesResponse {
  crops: Record<string, ClassInfo[]>;
  supported_crops: SupportedCrop[];
  total_classes: number;
}

export interface HealthResponse {
  status: string;
  model_loaded: boolean;
  supported_crops: SupportedCrop[];
  total_classes: number;
}

export interface PredictionItem {
  class_name: string;
  crop: string;
  condition: string;
  confidence: number;
}

export interface GradCamExplanation {
  heatmap: string;
  overlay: string;
  method: string;
  target_layer: string;
}

export interface AdvisorySource {
  organization: string;
  title: string;
  url: string;
  source_type?: string;
  verified_url?: boolean;
}

export interface AdvisoryContent {
  overview: string;
  common_symptoms: string[];
  immediate_actions: string[];
  prevention: string[];
  monitoring: string[];
  expert_escalation: string;
  sources: AdvisorySource[];
}

export interface AdvisoryResponse {
  status: string;
  class_name: string;
  crop: string;
  condition: string;
  is_healthy: boolean;
  advisory: AdvisoryContent;
  sources: AdvisorySource[];
}

export interface SymptomQuestion {
  id: string;
  question: string;
  weight: number;
}

export interface FieldSpreadOption {
  id: string;
  label: string;
  description: string;
}

export interface SymptomQuestionsResponse {
  status: string;
  class_name: string;
  questions: SymptomQuestion[];
  field_spread_options: FieldSpreadOption[];
}

export interface SymptomVerificationResult {
  answered: number;
  agreement: 'high' | 'moderate' | 'low';
  agreement_label: string;
  match_score: number;
}

export interface FieldAssessmentResult {
  concern_level: 'LOW' | 'MODERATE' | 'HIGH';
  reason: string;
  field_spread: string;
}

export interface SymptomVerifyResponse {
  status: string;
  class_name: string;
  symptom_verification: SymptomVerificationResult;
  field_assessment: FieldAssessmentResult;
  disclaimer: string;
}

export interface LocationSearchResult {
  name: string;
  admin1: string;
  country: string;
  latitude: number;
  longitude: number;
  timezone: string;
}

export interface LocationSearchResponse {
  status: string;
  query?: string;
  results: LocationSearchResult[];
}

export interface CurrentWeather {
  temperature_c: number;
  humidity_percent: number;
  precipitation_mm: number;
  wind_kmh: number;
  weather_code: number;
}

export interface ForecastSummary {
  next_24h: {
    temp_max_c: number;
    temp_min_c: number;
    total_precip_mm: number;
  };
}

export interface DiseaseWeatherContext {
  available: boolean;
  favorability: 'LOW' | 'MODERATE' | 'HIGH' | 'NEUTRAL' | 'UNAVAILABLE';
  favorability_label: string;
  matched_factors: string[];
  unmatched_factors: string[];
  explanation: string;
  disclaimer: string;
  sources: string[];
}

export interface WeatherSourceInfo {
  provider: string;
  url?: string;
  notes?: string;
}

export interface WeatherContextResponse {
  status: string;
  weather_available: boolean;
  location?: {
    name: string;
    latitude: number;
    longitude: number;
    timezone: string;
  };
  current?: CurrentWeather;
  forecast_summary?: ForecastSummary;
  disease_context: DiseaseWeatherContext;
  weather_source: WeatherSourceInfo;
  message?: string;
}

export interface ScanRecord {
  id: number;
  created_at: string;
  crop: string;
  class_name: string;
  condition: string;
  model_confidence: number;
  is_healthy: boolean;
  symptom_agreement?: string | null;
  symptom_match_score?: number | null;
  field_concern?: string | null;
  weather_favorability?: string | null;
  location_name?: string | null;
  community_shared: boolean;
}

export interface SaveScanResponse {
  status: string;
  message?: string;
  scan: ScanRecord;
}

export interface ScansListResponse {
  status: string;
  total: number;
  scans: ScanRecord[];
}

export interface CommunitySignalRecord {
  id: number;
  created_at: string;
  source_scan_id: number;
  crop: string;
  class_name: string;
  condition: string;
  area_name: string;
  approx_lat?: number;
  approx_lon?: number;
  symptom_agreement?: string | null;
  field_concern?: string | null;
  weather_favorability?: string | null;
  status: string;
}

export interface CommunitySignalResponse {
  status: string;
  message?: string;
  signal: CommunitySignalRecord;
}

export interface CommunitySignalsListResponse {
  status: string;
  total: number;
  signals: CommunitySignalRecord[];
}

export interface AreaBreakdownItem {
  area_name: string;
  condition: string;
  reported_signals: number;
}

export interface CommunitySummaryResponse {
  status: string;
  total_reported_signals: number;
  signals_last_7_days: number;
  most_reported_condition: string;
  area_breakdown: AreaBreakdownItem[];
  disclaimer: string;
}

export interface PredictResponse {
  status: 'success' | 'uncertain';
  selected_crop?: string | null;
  prediction: PredictionItem;
  top_predictions: PredictionItem[];
  diagnosis_reliable: boolean;
  uncertainty_reason?: string | null;
  is_healthy: boolean;
  explanation?: GradCamExplanation | null;
  advisory?: AdvisoryContent | null;
}

export interface ApiError {
  error: string;
}
