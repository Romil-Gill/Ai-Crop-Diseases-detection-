import axios from 'axios';
import type { HealthResponse, ClassesResponse, PredictResponse, AdvisoryResponse, SymptomQuestionsResponse, SymptomVerifyResponse, LocationSearchResponse, WeatherContextResponse, ScanRecord, SaveScanResponse, ScansListResponse, CommunitySignalResponse, CommunitySignalsListResponse, CommunitySummaryResponse, CommunityRadarResponse, SupportedCrop } from '../types/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Accept': 'application/json',
  },
});

export const checkHealth = async (): Promise<HealthResponse> => {
  try {
    const response = await apiClient.get<HealthResponse>('/api/health');
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (!error.response) {
        throw new Error('Flask server is unreachable. Please verify backend is running at ' + API_BASE_URL);
      }
      throw new Error(error.response.data?.error || 'Failed to reach health endpoint.');
    }
    throw new Error('An unexpected network error occurred.');
  }
};

export const getClasses = async (): Promise<ClassesResponse> => {
  try {
    const response = await apiClient.get<ClassesResponse>('/api/classes');
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (!error.response) {
        throw new Error('Flask server is unreachable. Please start Flask backend.');
      }
      throw new Error(error.response.data?.error || 'Failed to fetch class metadata.');
    }
    throw new Error('An unexpected network error occurred.');
  }
};

export const predictDisease = async (
  imageFile: File,
  selectedCrop?: SupportedCrop | string
): Promise<PredictResponse> => {
  const formData = new FormData();
  formData.append('file', imageFile);
  if (selectedCrop) {
    formData.append('selected_crop', selectedCrop);
  }

  try {
    const response = await apiClient.post<PredictResponse>('/api/predict', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (!error.response) {
        throw new Error('Flask ML backend server is currently offline or unreachable at ' + API_BASE_URL);
      }
      const serverErr = error.response.data?.error || `Server error (${error.response.status})`;
      throw new Error(serverErr);
    }
    throw new Error('Network timeout or connection error during image analysis.');
  }
};

export const explainDisease = async (
  imageFile: File,
  selectedCrop?: SupportedCrop | string
): Promise<PredictResponse> => {
  const formData = new FormData();
  formData.append('file', imageFile);
  if (selectedCrop) {
    formData.append('selected_crop', selectedCrop);
  }

  try {
    const response = await apiClient.post<PredictResponse>('/api/explain', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (!error.response) {
        throw new Error('Flask ML backend server is currently offline or unreachable at ' + API_BASE_URL);
      }
      const serverErr = error.response.data?.error || `Server error (${error.response.status})`;
      throw new Error(serverErr);
    }
    throw new Error('Network timeout or connection error during Grad-CAM explanation generation.');
  }
};

export const getAdvisory = async (className: string): Promise<AdvisoryResponse> => {
  try {
    const response = await apiClient.get<AdvisoryResponse>('/api/advisory', {
      params: { class_name: className },
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (!error.response) {
        throw new Error('Flask ML backend server is currently offline.');
      }
      throw new Error(error.response.data?.error || 'Failed to fetch agricultural advisory.');
    }
    throw new Error('Network error while retrieving advisory information.');
  }
};

export const getSymptomQuestions = async (className: string): Promise<SymptomQuestionsResponse> => {
  try {
    const response = await apiClient.get<SymptomQuestionsResponse>('/api/symptom-questions', {
      params: { class_name: className },
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.error || 'Failed to fetch symptom verification questions.');
    }
    throw new Error('Network error while retrieving symptom questions.');
  }
};

export const verifySymptoms = async (
  className: string,
  answers: Record<string, string>,
  fieldSpread: string
): Promise<SymptomVerifyResponse> => {
  try {
    const response = await apiClient.post<SymptomVerifyResponse>('/api/verify-symptoms', {
      class_name: className,
      answers,
      field_spread: fieldSpread,
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.error || 'Failed to submit symptom verification.');
    }
    throw new Error('Network error during symptom verification submission.');
  }
};

export const searchLocations = async (query: string): Promise<LocationSearchResponse> => {
  try {
    const response = await apiClient.get<LocationSearchResponse>('/api/location-search', {
      params: { q: query },
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      return { status: 'error', results: [] };
    }
    return { status: 'error', results: [] };
  }
};

export const getWeatherContext = async (
  latitude: number,
  longitude: number,
  className: string,
  locationName?: string
): Promise<WeatherContextResponse> => {
  try {
    const response = await apiClient.get<WeatherContextResponse>('/api/weather-context', {
      params: {
        latitude,
        longitude,
        class_name: className,
        location_name: locationName,
      },
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      return {
        status: 'partial_success',
        weather_available: false,
        message: 'Weather service temporarily unreachable.',
        disease_context: {
          available: false,
          favorability: 'UNAVAILABLE',
          favorability_label: 'Weather Service Unavailable',
          matched_factors: [],
          unmatched_factors: [],
          explanation: 'Weather service is offline. Crop diagnosis and advisory remain fully functional.',
          disclaimer: 'Weather favorability is supplementary and does not affect diagnosis reliability.',
          sources: [],
        },
        weather_source: { provider: 'Open-Meteo' },
      };
    }
    throw new Error('Network error while retrieving weather context.');
  }
};

export const saveScan = async (scanData: Partial<ScanRecord>): Promise<SaveScanResponse> => {
  try {
    const response = await apiClient.post<SaveScanResponse>('/api/scans', scanData);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.error || 'Assessment could not be saved.');
    }
    throw new Error('Network error while saving assessment.');
  }
};

export const getScans = async (crop?: string): Promise<ScansListResponse> => {
  try {
    const response = await apiClient.get<ScansListResponse>('/api/scans', {
      params: crop && crop.toLowerCase() !== 'all' ? { crop } : {},
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      return { status: 'error', total: 0, scans: [] };
    }
    return { status: 'error', total: 0, scans: [] };
  }
};

export const deleteScan = async (scanId: number): Promise<boolean> => {
  try {
    const response = await apiClient.delete<{ status: string }>(`/api/scans/${scanId}`);
    return response.data.status === 'success';
  } catch (error) {
    return false;
  }
};

export const shareCommunitySignal = async (
  scanId: number,
  approxLat?: number,
  approxLon?: number
): Promise<CommunitySignalResponse> => {
  try {
    const response = await apiClient.post<CommunitySignalResponse>('/api/community-signals', {
      scan_id: scanId,
      approx_lat: approxLat,
      approx_lon: approxLon,
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.error || 'Failed to share community signal.');
    }
    throw new Error('Network error while sharing community signal.');
  }
};

export const getCommunitySignals = async (): Promise<CommunitySignalsListResponse> => {
  try {
    const response = await apiClient.get<CommunitySignalsListResponse>('/api/community-signals');
    return response.data;
  } catch (error) {
    return { status: 'error', total: 0, signals: [] };
  }
};

export const getCommunitySummary = async (): Promise<CommunitySummaryResponse> => {
  try {
    const response = await apiClient.get<CommunitySummaryResponse>('/api/community-summary');
    return response.data;
  } catch (error) {
    return {
      status: 'error',
      total_reported_signals: 0,
      signals_last_7_days: 0,
      most_reported_condition: 'None',
      area_breakdown: [],
      disclaimer: 'Community signals represent anonymized user reports and are not laboratory-confirmed cases.',
    };
  }
};

export const getCommunityRadar = async (
  mode: 'live' | 'demo' = 'live',
  days: number = 7,
  crop: string = 'All'
): Promise<CommunityRadarResponse> => {
  try {
    const response = await apiClient.get<CommunityRadarResponse>('/api/community-radar', {
      params: {
        mode,
        days,
        crop: crop && crop.toLowerCase() !== 'all' ? crop : 'All',
      },
    });
    return response.data;
  } catch (error) {
    return {
      status: 'error',
      mode,
      filters: { days, crop },
      summary: { total_signals: 0, active_areas: 0, most_reported_crop: 'None', most_reported_condition: 'None' },
      areas: [],
      daily_trend: [],
      crop_breakdown: [],
      recent_signals: [],
      disclaimer: 'Map locations are coarsened for farmer privacy. Signals represent community reports, not laboratory cases.',
    };
  }
};

export { API_BASE_URL };
