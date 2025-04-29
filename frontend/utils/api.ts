import axios, { AxiosError } from 'axios';
import axiosRetry from 'axios-retry';

const baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 second timeout
});

// Configure retry behavior
axiosRetry(api, {
  retries: 3,
  retryDelay: (retryCount) => {
    return retryCount * 1000; // exponential backoff
  },
  retryCondition: (error) => {
    // Retry on network errors or 5xx server errors
    return axiosRetry.isNetworkOrIdempotentRequestError(error) || 
           (error.response?.status && error.response?.status >= 500);
  }
});

// Error handler
const handleError = (error: unknown) => {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError;
    if (axiosError.response) {
      throw new Error(axiosError.response.data?.detail || 'Server error occurred');
    } else if (axiosError.request) {
      throw new Error('No response received from server');
    }
  }
  throw new Error('An unexpected error occurred');
};

export interface ChatSession {
  id: string;
  title: string;
  timestamp: string;
  message_count: number;
}

export const getChatSessions = async (): Promise<ChatSession[]> => {
  try {
    const response = await api.get('/chat/sessions');
    return response.data;
  } catch (error) {
    handleError(error);
    return [];
  }
};

export const sendMessage = async (message: string, sessionId: string = 'default') => {
  try {
    const response = await api.post('/chat/send', { 
      message, 
      session_id: sessionId
    });
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

export const getChatHistory = async (sessionId: string = 'default') => {
  try {
    const response = await api.get(`/chat/history?session_id=${sessionId}`);
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

export const uploadFile = async (file: File) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/files/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / (progressEvent.total || progressEvent.loaded));
        // You can use this for progress indication if needed
        console.log(`Upload Progress: ${percentCompleted}%`);
      },
    });
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

export const getFilesList = async () => {
  try {
    const response = await api.get('/files/list');
    return response.data;
  } catch (error) {
    handleError(error);
  }
};