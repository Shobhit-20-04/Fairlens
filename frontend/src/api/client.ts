/**
 * FairLens REST API Client
 * Typed HTTP integration calling the Python Flask backend.
 */

import {
  HealthResponse,
  SettingsResponse,
  ProviderInfo,
  DiscoveryResult,
  SampleDataset,
  DatasetProfileResponse,
  AuditRunResponse,
  ExportResponse,
  ResearchStatusResponse,
  CostEstimate,
  AuditDimensionSpec,
} from "./types";

const BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${BASE_URL}${endpoint}`;
  const headers = new Headers(options.headers || {});

  if (!(options.body instanceof FormData) && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let errorMessage = `HTTP Error ${response.status}: ${response.statusText}`;
    try {
      const errorJson = await response.json();
      if (errorJson.error) {
        errorMessage = errorJson.error;
      }
    } catch {
      // ignore
    }
    throw new Error(errorMessage);
  }

  return response.json() as Promise<T>;
}

export const api = {
  getHealth: () => request<HealthResponse>("/health"),

  getSettings: () => request<SettingsResponse>("/settings"),

  getProviders: () => request<{ providers: ProviderInfo[] }>("/discovery/providers"),

  searchDatasets: (params: {
    query: string;
    domain?: string;
    geographic_coverage?: string;
    providers?: string[];
    min_quality_score?: number;
    limit?: number;
    use_mock_offline?: boolean;
  }) =>
    request<DiscoveryResult>("/discovery/search", {
      method: "POST",
      body: JSON.stringify(params),
    }),

  getSampleDatasets: () => request<{ samples: SampleDataset[] }>("/profiler/samples"),

  profileDatasetByPath: (filePath: string) =>
    request<DatasetProfileResponse>("/profiler/profile", {
      method: "POST",
      body: JSON.stringify({ file_path: filePath }),
    }),

  profileDatasetByUpload: (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    return request<DatasetProfileResponse>("/profiler/profile", {
      method: "POST",
      body: formData,
    });
  },

  runAudit: (payload: {
    file_path: string;
    dimensions: AuditDimensionSpec[];
    intersectional_pairs?: [string, string][];
    confidence_level?: number;
  }) =>
    request<AuditRunResponse>("/audit/run", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  exportAudit: (reportId: string, format: "json" | "csv") =>
    request<ExportResponse>("/audit/export", {
      method: "POST",
      body: JSON.stringify({ report_id: reportId, format }),
    }),

  getResearchStatus: () => request<ResearchStatusResponse>("/research/status"),

  estimateCost: (params: { runs: number; input_tokens: number; output_tokens: number; use_free_tier?: boolean }) =>
    request<CostEstimate>("/research/estimate-cost", {
      method: "POST",
      body: JSON.stringify(params),
    }),
};
