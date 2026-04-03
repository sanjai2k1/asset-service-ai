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
}export async function streamRequest<T = any>({
  url,
  method = 'POST',
  data,
  onMessage,
  onError,
}: {
  url: string;
  method?: 'POST' | 'GET';
  data?: any;
  onMessage?: (chunk: any) => void;
  onError?: (err: any) => void;
}): Promise<ApiResult<T>> {
  try {
    const response = await fetch(getBaseURL() + url, {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
      body: method === 'POST' ? JSON.stringify(data) : undefined,
    });

    if (!response.body) {
      throw new Error('Streaming not supported in this browser');
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    let buffer = '';
    let finalData: T | null = null;

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });

      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed) continue;

        try {
          const parsed = JSON.parse(trimmed);

          // ✅ emit ALL events immediately
          onMessage?.(parsed);

          // ✅ store final separately
          if (parsed.type === 'final') {
            finalData = parsed as T;
          }

        } catch (err) {
          console.warn('Failed to parse stream chunk:', trimmed);
        }
      }
    }

    if (finalData) {
      return {
        success: true,
        data: finalData,
        status: 200,
      };
    }

    throw new Error('No final response received');

  } catch (err: any) {
    console.error('Streaming error:', err);

    onError?.(err);

    return {
      success: false,
      error: err.message || 'Streaming failed',
      status: 500,
    };
  }
}

export default api;