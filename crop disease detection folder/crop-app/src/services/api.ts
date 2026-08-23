import axios from 'axios';
import type { HealthResponse, ClassesResponse, PredictResponse, SupportedCrop } from '../types/api';

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

export { API_BASE_URL };
