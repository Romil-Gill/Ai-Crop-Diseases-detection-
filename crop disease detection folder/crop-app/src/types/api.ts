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

export interface PredictResponse {
  status: 'success' | 'uncertain';
  selected_crop: string | null;
  prediction: PredictionItem;
  top_predictions: PredictionItem[];
  diagnosis_reliable: boolean;
  uncertainty_reason: string | null;
  is_healthy: boolean;
}

export interface ApiError {
  error: string;
}
