import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  FileSpreadsheet,
  Upload,
  Database,
  ArrowRight,
  AlertTriangle,
  CheckCircle2,
  Table,
  FileCheck,
  RefreshCw,
} from "lucide-react";
import { api } from "../api/client";
import { SampleDataset, DatasetProfileResponse } from "../api/types";

interface ProfilerProps {
  selectedFilePath: string | null;
  onSetSelectedFilePath: (path: string) => void;
}

export const Profiler: React.FC<ProfilerProps> = ({
  selectedFilePath,
  onSetSelectedFilePath,
}) => {
  const navigate = useNavigate();

  const [samples, setSamples] = useState<SampleDataset[]>([]);
  const [activePath, setActivePath] = useState<string>(
    selectedFilePath || "tests/fixtures/auditing/indian_legal_synthetic_audit.csv"
  );
  const [profile, setProfile] = useState<DatasetProfileResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Load pre-loaded sample fixtures
    api
      .getSampleDatasets()
      .then((res) => {
        setSamples(res.samples);
      })
      .catch((err) => console.error("Failed to load sample datasets:", err));

    // Profile initial dataset
    if (activePath) {
      loadProfile(activePath);
    }
  }, []);

  const loadProfile = async (path: string) => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.profileDatasetByPath(path);
      setProfile(res);
      setActivePath(path);
      onSetSelectedFilePath(path);
    } catch (err: any) {
      setError(err.message || "Failed to profile dataset");
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setLoading(true);
    setError(null);
    try {
      const res = await api.profileDatasetByUpload(file);
      setProfile(res);
      setActivePath(res.file_path);
      onSetSelectedFilePath(res.file_path);
    } catch (err: any) {
      setError(err.message || "Failed to upload and profile dataset");
    } finally {
      setLoading(false);
    }
  };

  const handleProceedToAudit = () => {
    if (profile) {
      onSetSelectedFilePath(profile.file_path);
      navigate("/audit");
    }
  };

  return (
    <div className="page-content">
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "var(--space-3)" }}>
        <div>
          <h1 style={{ fontSize: "var(--text-xl)", fontWeight: 700 }}>Tabular Data Profiler & Ingestion</h1>
          <p style={{ color: "var(--text-muted)", fontSize: "var(--text-sm)", marginTop: "2px" }}>
            Safe, read-only inspection of schema, null rates, duplicate rows, and statistical types.
          </p>
        </div>

        {profile && (
          <button className="btn btn-primary" onClick={handleProceedToAudit}>
            <span>Configure & Run Audit</span>
            <ArrowRight size={15} />
          </button>
        )}
      </div>

      {/* Dataset Selection: Pre-loaded Fixtures & Upload */}
      <div className="grid-2">
        {/* Pre-loaded Benchmark Fixtures */}
        <div className="card">
          <div className="card-header">
            <div className="card-title">
              <Database size={16} style={{ color: "var(--color-primary)" }} />
              Pre-loaded Research Benchmark Fixtures
            </div>
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-2)" }}>
            {samples.map((s) => {
              const isSelected = activePath.endsWith(s.file_name);
              return (
                <div
                  key={s.file_name}
                  onClick={() => loadProfile(s.file_path)}
                  style={{
                    padding: "var(--space-2) var(--space-3)",
                    borderRadius: "var(--radius-md)",
                    backgroundColor: isSelected ? "var(--color-primary-subtle)" : "var(--bg-card-subtle)",
                    border: `1px solid ${isSelected ? "rgba(99, 102, 241, 0.4)" : "var(--border-subtle)"}`,
                    cursor: "pointer",
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    transition: "all var(--transition-fast)",
                  }}
                >
                  <div>
                    <div style={{ fontWeight: 600, fontSize: "var(--text-sm)", color: isSelected ? "var(--color-primary)" : "var(--text-primary)" }}>
                      {s.title}
                    </div>
                    <div style={{ fontSize: "var(--text-xs)", color: "var(--text-muted)" }}>
                      {s.description}
                    </div>
                  </div>
                  <span className="badge badge-neutral" style={{ fontSize: "10px" }}>
                    {(s.size_bytes / 1024).toFixed(1)} KB
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        {/* File Drag-and-Drop Upload */}
        <div className="card">
          <div className="card-header">
            <div className="card-title">
              <Upload size={16} style={{ color: "var(--color-primary)" }} />
              Upload Custom Dataset
            </div>
          </div>
          <label
            style={{
              flex: 1,
              border: "2px dashed var(--border-default)",
              borderRadius: "var(--radius-lg)",
              padding: "var(--space-6)",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              gap: "var(--space-2)",
              cursor: "pointer",
              backgroundColor: "var(--bg-card-subtle)",
              textAlign: "center",
            }}
          >
            <Upload size={32} style={{ color: "var(--color-primary)" }} />
            <div style={{ fontWeight: 600, fontSize: "var(--text-sm)" }}>
              Drag & drop CSV, Parquet, TSV, or Excel file
            </div>
            <div style={{ fontSize: "var(--text-xs)", color: "var(--text-muted)" }}>
              Supports .csv, .parquet, .tsv, .xlsx (Evaluated read-only in memory)
            </div>
            <input
              type="file"
              accept=".csv,.parquet,.tsv,.xlsx,.xls"
              onChange={handleFileUpload}
              style={{ display: "none" }}
            />
          </label>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="alert-banner high">
          <AlertTriangle size={18} />
          <span>{error}</span>
        </div>
      )}

      {/* Profiling Telemetry Summary */}
      {loading ? (
        <div className="card" style={{ textAlign: "center", padding: "var(--space-8)" }}>
          <RefreshCw size={24} className="spin" style={{ margin: "0 auto var(--space-2)" }} />
          <div>Profiling tabular dataset...</div>
        </div>
      ) : profile ? (
        <>
          <div className="grid-4">
            <div className="stat-card">
              <div className="stat-label">Total Records</div>
              <div className="stat-value">{profile.total_rows.toLocaleString()}</div>
              <div className="stat-hint">Active sample size</div>
            </div>

            <div className="stat-card">
              <div className="stat-label">Features / Columns</div>
              <div className="stat-value">{profile.total_columns}</div>
              <div className="stat-hint">Inferred feature schema</div>
            </div>

            <div className="stat-card">
              <div className="stat-label">Duplicate Rows</div>
              <div className="stat-value" style={{ color: profile.duplicate_rows > 0 ? "var(--badge-warning-text)" : "var(--badge-success-text)" }}>
                {profile.duplicate_rows.toLocaleString()}
              </div>
              <div className="stat-hint">{(profile.duplicate_rate * 100).toFixed(1)}% duplication rate</div>
            </div>

            <div className="stat-card">
              <div className="stat-label">Memory Ingested</div>
              <div className="stat-value">
                {profile.memory_usage_bytes ? `${(profile.memory_usage_bytes / 1024).toFixed(1)} KB` : "Cached"}
              </div>
              <div className="stat-hint">{profile.file_name}</div>
            </div>
          </div>

          {/* Schema Profiler Table */}
          <div className="card">
            <div className="card-header">
              <div className="card-title">
                <FileCheck size={18} style={{ color: "var(--color-primary)" }} />
                Feature Schema & Data Quality Profiling
              </div>
            </div>
            <div className="table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Column Name</th>
                    <th>Inferred Type</th>
                    <th>Missing / Nulls</th>
                    <th>Missing Rate</th>
                    <th>Unique Cardinality</th>
                    <th>Sample Observations</th>
                  </tr>
                </thead>
                <tbody>
                  {profile.columns.map((c) => (
                    <tr key={c.name}>
                      <td>
                        <strong>{c.name}</strong>
                      </td>
                      <td>
                        <span className="badge badge-neutral" style={{ textTransform: "uppercase", fontSize: "10px" }}>
                          {c.dtype}
                        </span>
                      </td>
                      <td>{c.null_count.toLocaleString()}</td>
                      <td>
                        <span
                          className={`badge ${
                            c.null_rate > 0.1
                              ? "badge-error"
                              : c.null_rate > 0.02
                              ? "badge-warning"
                              : "badge-success"
                          }`}
                        >
                          {(c.null_rate * 100).toFixed(1)}%
                        </span>
                      </td>
                      <td style={{ fontFamily: "var(--font-mono)" }}>{c.unique_count}</td>
                      <td style={{ fontSize: "var(--text-xs)", color: "var(--text-muted)" }}>
                        {c.sample_values.slice(0, 5).join(", ")}
                        {c.sample_values.length > 5 ? "..." : ""}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Raw Data Preview (First 20 Rows) */}
          <div className="card">
            <div className="card-header">
              <div className="card-title">
                <Table size={18} style={{ color: "var(--color-primary)" }} />
                Dataset Sample Preview (First {profile.preview_rows.length} Rows)
              </div>
            </div>
            <div className="table-container" style={{ maxHeight: "360px" }}>
              <table className="data-table">
                <thead>
                  <tr>
                    {profile.columns.map((c) => (
                      <th key={c.name}>{c.name}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {profile.preview_rows.map((row, idx) => (
                    <tr key={idx}>
                      {profile.columns.map((c) => (
                        <td key={c.name} style={{ fontFamily: "var(--font-mono)", fontSize: "var(--text-xs)" }}>
                          {row[c.name] !== undefined && row[c.name] !== null ? String(row[c.name]) : "<NULL>"}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      ) : null}
    </div>
  );
};
