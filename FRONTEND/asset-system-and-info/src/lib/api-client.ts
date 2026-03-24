import axios, { AxiosError, AxiosRequestConfig } from 'axios';

// 1. Dynamic Base URL Constructor
const getBaseURL = () => {
  // 1. Vite requires the VITE_ prefix
  const protocol = import.meta.env.VITE_API_PROTOCOL || 'http';
  const host = import.meta.env.VITE_API_HOST || '127.0.0.1';
  const port = import.meta.env.VITE_API_PORT || '8000';

  // 2. Build the string
  const url = `${protocol}://${host}:${port}/`; // Added v1 or your base path
  

  return url;
};

// 2. Axios Instance
const api = axios.create({
  baseURL: getBaseURL(),
  headers: {
    'Content-Type': 'application/json',
  },
});

// 3. Structured Result Type
export type ApiResult<T> = 
  | { success: true; data: T; status: number } 
  | { success: false; error: string; status: number; raw?: any };

/**
 * Common request function to handle API calls with structured errors.
 */
export async function request<T>(config: AxiosRequestConfig): Promise<ApiResult<T>> {
  try {
    const response = await api.request<T>(config);
    
    return {
      success: true,
      data: response.data,
      status: response.status
    };
  } catch (error) {
    const axiosError = error as AxiosError<any>;
    
    // Extract the most descriptive error message from backend
    const backendError = axiosError.response?.data;
    const message = 
      backendError?.message || 
      backendError?.error || 
      backendError?.detail || // Common in Python/FastAPI backends
      axiosError.message || 
      "Unknown Server Error";

    return {
      success: false,
      error: message,
      status: axiosError.response?.status || 500,
      raw: backendError
    };
  }
}

export default api;