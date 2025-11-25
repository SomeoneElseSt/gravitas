/**
 * API client for communicating with the backend.
 */

import { API_BASE_URL } from "@/lib/constants";
import type {
  CitiesResponse,
  ErrorResponse,
  ProcessImageryRequest,
  ProcessImageryResponse,
} from "@/lib/types/api";

/**
 * Fetch wrapper that handles errors explicitly.
 */
async function apiRequest<T>(
  endpoint: string,
  options?: RequestInit
): Promise<{ data: T | null; error: ErrorResponse | null }> {
  const url = `${API_BASE_URL}${endpoint}`;

  console.log(`[API] Fetching: ${url}`);

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    });

    if (!response.ok) {
      const errorData = (await response.json()) as ErrorResponse;
      console.error(`[API] Error response:`, errorData);
      return { data: null, error: errorData };
    }

    const data = (await response.json()) as T;
    console.log(`[API] Success:`, data);
    return { data, error: null };
  } catch (err) {
    console.error(`[API] Network error:`, err);
    const error: ErrorResponse = {
      error: "Network Error",
      detail: err instanceof Error ? err.message : "Failed to connect to API",
    };
    return { data: null, error };
  }
}

/**
 * Get available cities.
 */
export async function getCities(): Promise<{
  data: CitiesResponse | null;
  error: ErrorResponse | null;
}> {
  return apiRequest<CitiesResponse>("/api/cities");
}

/**
 * Process imagery for a city and date range.
 */
export async function processImagery(
  request: ProcessImageryRequest
): Promise<{
  data: ProcessImageryResponse | null;
  error: ErrorResponse | null;
}> {
  return apiRequest<ProcessImageryResponse>("/api/process-imagery", {
    method: "POST",
    body: JSON.stringify(request),
  });
}

/**
 * Health check.
 */
export async function healthCheck(): Promise<{
  data: { status: string } | null;
  error: ErrorResponse | null;
}> {
  return apiRequest<{ status: string }>("/health");
}
