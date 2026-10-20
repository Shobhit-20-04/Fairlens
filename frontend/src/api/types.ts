/**
 * FairLens TypeScript API Types & Data Contracts
 * Mirroring Python Backend Models (Phases 1-4 & REST Server)
 */

export interface GpuTelemetry {
  available: boolean;
  device: string;
  vram_gb: number;
  cuda_version: string | null;
}

export interface HealthResponse {
  status: string;
  service: string;
  version: string;
  environment: string;
  offline_mode: boolean;
  python_version: string;
  gpu: GpuTelemetry;
  timestamp: number;
}

export interface SettingsResponse {
  env: string;
  log_level: string;
  offline_mode: boolean;
  openrouter_model: string;
  openrouter_api_key_configured: boolean;
  openrouter_api_key_masked: string;
  openrouter_timeout_seconds: number;
  openrouter_max_retries: number;
  budget: {
    max_spend_usd: number;
    warn_spend_usd: number;
    input_price_per_m: number;
    output_price_per_m: number;
  };
  providers: {
    huggingface: boolean;
    kaggle: boolean;
    data_gov: boolean;
    zenodo: boolean;
  };
}

export interface ProviderInfo {
  id: string;
  name: string;
  authenticated: boolean;
  public_search: boolean;
  rate_limit_authenticated: string;
  description: string;
}

export interface NormalizedDatasetMetadata {
  name: string;
  dataset_id: string;
  source_provider: string;
  canonical_url: string;
  description: string;
  domain: string;
  task_type: string;
  geography: string[];
  languages: string[];
  documented_demographics: string[];
  available_features: string[];
  target_labels: string[];
  format: string;
  size_bytes?: number | null;
  row_count?: number | null;
  license: string;
  license_verified: boolean;
  publication_date?: string | null;
  last_updated?: string | null;
  verification_status: string;
  metadata_completeness_score: number;
  missing_fields: string[];
  audit_suitability: "high" | "medium" | "low" | "unknown";
  audit_suitability_reasons: string[];
}

export interface DiscoveryResult {
  query: {
    keywords: string;
    domain?: string | null;
    geography?: string | null;
    providers?: string[] | null;
    limit: number;
  };
  total_found: number;
  returned_count: number;
  execution_time_seconds: number;
  provider_counts: Record<string, number>;
  provider_errors: Record<string, string>;
  datasets: NormalizedDatasetMetadata[];
}

export interface AuditDimensionSpec {
  name: string;
  column_name: string;
  dimension_type: "demographic" | "geographic" | "cultural" | "custom";
  expected_distribution?: Record<string, number>;
  expected_categories?: string[];
  min_sample_size?: number;
}

export interface SampleDataset {
  file_name: string;
  file_path: string;
  size_bytes: number;
  title: string;
  description: string;
  recommended_dimensions: AuditDimensionSpec[];
}

export interface ColumnMeta {
  name: string;
  dtype: string;
  null_count: number;
  null_rate: number;
  unique_count: number;
  sample_values: string[];
}

export interface DatasetProfileResponse {
  status: string;
  file_path: string;
  file_name: string;
  total_rows: number;
  total_columns: number;
  duplicate_rows: number;
  duplicate_rate: number;
  memory_usage_bytes?: number;
  columns: ColumnMeta[];
  preview_rows: Record<string, any>[];
}

export interface Scorecard {
  completeness_score: number;
  coverage_score: number | null;
  parity_score: number | null;
  composite_score: number | null;
  active_penalties: string[];
  explainability_notes: string[];
}

export interface AuditWarning {
  code: string;
  severity: "HIGH" | "MEDIUM" | "LOW";
  dimension: string;
  title: string;
  message: string;
  context: Record<string, any>;
  remediation_hint: string;
}

export interface ProportionItem {
  count: number;
  share: number;
  ci_lower: number;
  ci_upper: number;
  sample_size_sparse: boolean;
}

export interface DimensionResult {
  dimension_name: string;
  column_name: string;
  dimension_type: string;
  total_records: number;
  missing_records: number;
  valid_records: number;
  missing_rate: number;
  observed_category_count: number;
  proportions: Record<string, ProportionItem>;
  expected_categories: string[] | null;
  coverage_ratio: number | null;
  zero_observation_categories: string[];
  deviations: Record<string, number> | null;
  max_abs_deviation: number | null;
  mean_abs_deviation: number | null;
  js_divergence: number | null;
  scorecard: Scorecard;
  warnings: AuditWarning[];
}

export interface AuditReport {
  report_id?: string;
  dataset_profile: {
    file_name?: string;
    file_path?: string;
    total_rows: number;
    total_columns: number;
    duplicate_rows: number;
    duplicate_rate: number;
    columns: string[];
  };
  dimensions: Record<string, DimensionResult>;
  intersectional_results: Record<string, {
    pair: [string, string];
    total_valid_intersection: number;
    matrix: Record<string, Record<string, number>>;
    sparse_cell_count: number;
    zero_cells: [string, string][];
  }>;
  total_warnings_count: number;
  high_severity_warnings: number;
  execution_time_seconds: number;
  assumptions_and_limitations: string[];
}

export interface AuditRunResponse {
  status: string;
  report_id: string;
  report: AuditReport;
  summary_text: string;
}

export interface ExportResponse {
  status: string;
  format: string;
  file_path: string;
  file_name: string;
  size_bytes: number;
}

export interface CostEstimate {
  runs: number;
  input_tokens_total: number;
  output_tokens_total: number;
  input_cost_usd: number;
  output_cost_usd: number;
  base_total_usd: number;
  total_cost_usd: number;
  safety_margin: number;
  is_within_budget: boolean;
  budget_limit_usd: number;
}

export interface ResearchStatusResponse {
  layer_b_case_study: {
    target_model: string;
    model_architecture: string;
    openrouter_model_id: string;
    free_tier_variant: string;
    pricing: {
      free_tier: string;
      paid_tier_estimate: string;
      max_spend_ceiling: string;
      warn_threshold: string;
    };
    status: string;
    safety_card_findings: {
      source: string;
      bias_mitigation_claim: string;
      demographic_parities: string;
    };
    methodology: {
      domains: string[];
      evaluation_protocol: string[];
      disclaimer: string;
    };
  };
}
