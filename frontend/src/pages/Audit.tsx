import React, { useState, useEffect } from "react";
import {
  Play,
  Sliders,
  AlertTriangle,
  Download,
  Plus,
  Trash2,
  Layers,
  CheckCircle2,
  RefreshCw,
  FileText,
  HelpCircle,
} from "lucide-react";
import { api } from "../api/client";
import {
  AuditDimensionSpec,
  AuditReport,
  AuditRunResponse,
  SampleDataset,
} from "../api/types";
import { ScorecardGauge } from "../components/ScorecardGauge";
import { ConfidenceIntervalChart } from "../components/ConfidenceIntervalChart";
import { WarningAlert } from "../components/WarningAlert";

interface AuditProps {
  selectedFilePath: string | null;
  onSetReport: (report: AuditReport, summaryText: string, reportId: string) => void;
}

export const Audit: React.FC<AuditProps> = ({ selectedFilePath, onSetReport }) => {
  const [filePath, setFilePath] = useState<string>(
    selectedFilePath || "tests/fixtures/auditing/indian_legal_synthetic_audit.csv"
  );
  const [samples, setSamples] = useState<SampleDataset[]>([]);
  const [confidenceLevel, setConfidenceLevel] = useState<number>(0.95);
  const [enableIntersectional, setEnableIntersectional] = useState<boolean>(true);

  // Default clean dimensions modeled after Indian legal domains
  const [dimensions, setDimensions] = useState<AuditDimensionSpec[]>([
    {
      name: "gender",
      column_name: "gender",
      dimension_type: "demographic",
      expected_distribution: { Male: 0.48, Female: 0.48, "Non-Binary": 0.04 },
      expected_categories: ["Male", "Female", "Non-Binary"],
      min_sample_size: 30,
    },
    {
      name: "religion",
      column_name: "religion",
      dimension_type: "cultural",
      expected_distribution: { Hindu: 0.798, Muslim: 0.142, Christian: 0.023, Sikh: 0.017, Other: 0.02 },
      expected_categories: ["Hindu", "Muslim", "Christian", "Sikh", "Other"],
      min_sample_size: 30,
    },
    {
      name: "state",
      column_name: "state",
      dimension_type: "geographic",
      expected_categories: [
        "Maharashtra",
        "Karnataka",
        "Tamil Nadu",
        "Delhi",
        "Uttar Pradesh",
        "West Bengal",
        "Gujarat",
      ],
      min_sample_size: 30,
    },
  ]);

  const [activeTabDim, setActiveTabDim] = useState<string>("gender");
  const [auditResult, setAuditResult] = useState<AuditRunResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [exportNotice, setExportNotice] = useState<string | null>(null);

  // Load sample dataset manifests on mount
  useEffect(() => {
    api
      .getSampleDatasets()
      .then((res) => {
        setSamples(res.samples);
      })
      .catch((err) => console.error("Failed to fetch sample datasets:", err));

    // Execute audit on initial mount
    executeAudit(filePath, dimensions);
  }, []);

  const executeAudit = async (targetPath: string, targetDimensions: AuditDimensionSpec[]) => {
    setLoading(true);
    setError(null);
    setExportNotice(null);

    try {
      // Determine valid intersectional pairs
      const intersectionalPairs: [string, string][] =
        enableIntersectional && targetDimensions.length >= 2
          ? [
              [targetDimensions[0].name, targetDimensions[1].name],
              ...(targetDimensions.length >= 3
                ? [[targetDimensions[0].name, targetDimensions[2].name] as [string, string]]
                : []),
            ]
          : [];

      const res = await api.runAudit({
        file_path: targetPath,
        dimensions: targetDimensions,
        intersectional_pairs: intersectionalPairs.length > 0 ? intersectionalPairs : undefined,
        confidence_level: confidenceLevel,
      });

      setAuditResult(res);
      onSetReport(res.report, res.summary_text, res.report_id);

      // Set active dimension tab to the first audited dimension
      const dimNames = Object.keys(res.report.dimensions);
      if (dimNames.length > 0 && !dimNames.includes(activeTabDim)) {
        setActiveTabDim(dimNames[0]);
      }
    } catch (err: any) {
      setError(err.message || "Failed to execute audit. Please check your dimension column names.");
    } finally {
      setLoading(false);
    }
  };

  const handleSelectSample = (sample: SampleDataset) => {
    setFilePath(sample.file_path);
    if (sample.recommended_dimensions && sample.recommended_dimensions.length > 0) {
      setDimensions(sample.recommended_dimensions);
      setActiveTabDim(sample.recommended_dimensions[0].name);
      executeAudit(sample.file_path, sample.recommended_dimensions);
    } else {
      executeAudit(sample.file_path, dimensions);
    }
  };

  const handleAddDimension = () => {
    const newName = `dimension_${dimensions.length + 1}`;
    const newDim: AuditDimensionSpec = {
      name: newName,
      column_name: "",
      dimension_type: "demographic",
      min_sample_size: 30,
    };
    const updated = [...dimensions, newDim];
    setDimensions(updated);
    setActiveTabDim(newName);
  };

  const handleRemoveDimension = (index: number) => {
    const updated = dimensions.filter((_, i) => i !== index);
    setDimensions(updated);
    if (updated.length > 0) {
      setActiveTabDim(updated[0].name);
    }
  };

  const handleUpdateDimension = (index: number, field: keyof AuditDimensionSpec, val: any) => {
    const updated = [...dimensions];
    updated[index] = { ...updated[index], [field]: val };
    setDimensions(updated);
  };

  const handleExport = async (format: "json" | "csv") => {
    if (!auditResult) return;
    try {
      const res = await api.exportAudit(auditResult.report_id, format);
      setExportNotice(`Report exported: ${res.file_name} (${res.size_bytes} bytes in outputs/audit_reports/)`);
      setTimeout(() => setExportNotice(null), 6000);
    } catch (err: any) {
      setError("Export failed: " + err.message);
    }
  };

  const activeDimResult = auditResult?.report?.dimensions?.[activeTabDim];

  return (
    <div className="page-content">
      {/* Top Controls & Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "var(--space-3)" }}>
        <div>
          <h1 style={{ fontSize: "var(--text-xl)", fontWeight: 700 }}>Representation-Gap Audit</h1>
          <p style={{ color: "var(--text-muted)", fontSize: "var(--text-sm)", marginTop: "2px" }}>
            Measure subgroup representation disparities, Wilson 95% confidence intervals, and intersectional gaps.
          </p>
        </div>

        <div style={{ display: "flex", gap: "var(--space-2)" }}>
          <button
            className="btn btn-primary"
            onClick={() => executeAudit(filePath, dimensions)}
            disabled={loading}
          >
            {loading ? <RefreshCw size={14} className="spin" /> : <Play size={14} />}
            <span>{loading ? "Calculating Metrics..." : "Run Audit"}</span>
          </button>
        </div>
      </div>

      {/* Dataset Selection Bar */}
      <div className="card" style={{ padding: "var(--space-3) var(--space-4)" }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: "var(--space-3)" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "var(--space-2)" }}>
            <span style={{ fontSize: "var(--text-xs)", fontWeight: 600, color: "var(--text-muted)", textTransform: "uppercase" }}>
              Active Dataset:
            </span>
            <select
              className="select"
              style={{ width: "auto", minWidth: "280px", padding: "6px 10px", fontSize: "var(--text-sm)" }}
              value={filePath}
              onChange={(e) => {
                const s = samples.find((x) => x.file_path === e.target.value);
                if (s) handleSelectSample(s);
                else setFilePath(e.target.value);
              }}
            >
              {samples.map((s) => (
                <option key={s.file_name} value={s.file_path}>
                  {s.title}
                </option>
              ))}
            </select>
          </div>

          <div style={{ display: "flex", alignItems: "center", gap: "var(--space-4)", fontSize: "var(--text-xs)", color: "var(--text-secondary)" }}>
            <label style={{ display: "flex", alignItems: "center", gap: "var(--space-2)", cursor: "pointer" }}>
              <input
                type="checkbox"
                checked={enableIntersectional}
                onChange={(e) => setEnableIntersectional(e.target.checked)}
              />
              <span>2D Intersectional Analysis</span>
            </label>

            <div style={{ display: "flex", alignItems: "center", gap: "var(--space-15)" }}>
              <span>Confidence Level:</span>
              <select
                className="select"
                style={{ width: "auto", padding: "2px 6px", fontSize: "var(--text-xs)" }}
                value={confidenceLevel}
                onChange={(e) => setConfidenceLevel(parseFloat(e.target.value))}
              >
                <option value={0.95}>95% (Wilson z=1.96)</option>
                <option value={0.9}>90% (Wilson z=1.64)</option>
                <option value={0.99}>99% (Wilson z=2.58)</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Dimension Configuration Drawer / Panel */}
      <div className="card">
        <div className="card-header">
          <div className="card-title">
            <Sliders size={16} style={{ color: "var(--color-primary)" }} />
            Audit Dimensions ({dimensions.length})
          </div>
          <button className="btn btn-secondary btn-sm" onClick={handleAddDimension}>
            <Plus size={13} />
            <span>Add Dimension</span>
          </button>
        </div>

        <div className="grid-3">
          {dimensions.map((dim, idx) => (
            <div
              key={idx}
              style={{
                padding: "var(--space-3)",
                backgroundColor: "var(--bg-card-subtle)",
                borderRadius: "var(--radius-md)",
                border: "1px solid var(--border-subtle)",
                display: "flex",
                flexDirection: "column",
                gap: "var(--space-2)",
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <input
                  type="text"
                  className="input"
                  style={{ fontWeight: 600, fontSize: "var(--text-sm)", padding: "4px 6px", width: "120px" }}
                  value={dim.name}
                  onChange={(e) => handleUpdateDimension(idx, "name", e.target.value)}
                  placeholder="Dimension name"
                />
                <select
                  className="select"
                  style={{ width: "auto", fontSize: "var(--text-xs)", padding: "2px 6px" }}
                  value={dim.dimension_type}
                  onChange={(e) => handleUpdateDimension(idx, "dimension_type", e.target.value)}
                >
                  <option value="demographic">Demographic</option>
                  <option value="geographic">Geographic</option>
                  <option value="cultural">Cultural</option>
                  <option value="custom">Custom</option>
                </select>
                {dimensions.length > 1 && (
                  <button
                    className="btn btn-ghost btn-sm"
                    onClick={() => handleRemoveDimension(idx)}
                    title="Remove dimension"
                  >
                    <Trash2 size={13} style={{ color: "var(--badge-error-text)" }} />
                  </button>
                )}
              </div>

              <div>
                <label className="label" style={{ fontSize: "10px" }}>Dataset Column Name</label>
                <input
                  type="text"
                  className="input"
                  style={{ fontFamily: "var(--font-mono)", fontSize: "var(--text-xs)", padding: "4px 8px" }}
                  value={dim.column_name}
                  onChange={(e) => handleUpdateDimension(idx, "column_name", e.target.value)}
                  placeholder="e.g. gender, state"
                />
              </div>

              <div>
                <label className="label" style={{ fontSize: "10px" }}>Target Categories (comma-separated)</label>
                <input
                  type="text"
                  className="input"
                  style={{ fontSize: "var(--text-xs)", padding: "4px 8px" }}
                  value={
                    dim.expected_categories
                      ? dim.expected_categories.join(", ")
                      : dim.expected_distribution
                      ? Object.keys(dim.expected_distribution).join(", ")
                      : ""
                  }
                  onChange={(e) => {
                    const raw = e.target.value;
                    const cats = raw.split(",").map((c) => c.trim()).filter(Boolean);
                    handleUpdateDimension(idx, "expected_categories", cats.length > 0 ? cats : undefined);
                  }}
                  placeholder="e.g. Male, Female, Non-Binary"
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Notifications / Errors */}
      {error && (
        <div className="alert-banner high">
          <AlertTriangle size={18} />
          <span>{error}</span>
        </div>
      )}
      {exportNotice && (
        <div className="alert-banner low">
          <CheckCircle2 size={18} />
          <span>{exportNotice}</span>
        </div>
      )}

      {/* Results Section */}
      {auditResult && auditResult.report && (
        <>
          {/* Executive Summary Bar */}
          <div className="grid-4">
            <div className="stat-card">
              <div className="stat-label">Records Audited</div>
              <div className="stat-value">{auditResult.report.dataset_profile.total_rows.toLocaleString()}</div>
              <div className="stat-hint">{auditResult.report.dataset_profile.file_name}</div>
            </div>

            <div className="stat-card">
              <div className="stat-label">Execution Time</div>
              <div className="stat-value">{auditResult.report.execution_time_seconds.toFixed(3)}s</div>
              <div className="stat-hint">Python vectorized metrics</div>
            </div>

            <div className="stat-card">
              <div className="stat-label">Active Warnings</div>
              <div
                className="stat-value"
                style={{
                  color:
                    auditResult.report.high_severity_warnings > 0
                      ? "var(--badge-error-text)"
                      : "var(--badge-success-text)",
                }}
              >
                {auditResult.report.total_warnings_count}
              </div>
              <div className="stat-hint">
                {auditResult.report.high_severity_warnings} High Severity
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-label">Export Audit Report</div>
              <div style={{ display: "flex", gap: "var(--space-2)", marginTop: "4px" }}>
                <button className="btn btn-secondary btn-sm" onClick={() => handleExport("json")} style={{ flex: 1 }}>
                  <Download size={12} />
                  <span>JSON</span>
                </button>
                <button className="btn btn-secondary btn-sm" onClick={() => handleExport("csv")} style={{ flex: 1 }}>
                  <Download size={12} />
                  <span>CSV</span>
                </button>
              </div>
              <div className="stat-hint">Saved to outputs/audit_reports/</div>
            </div>
          </div>

          {/* Dimension Tabs */}
          <div className="tab-list">
            {Object.keys(auditResult.report.dimensions).map((dimName) => (
              <button
                key={dimName}
                className={`tab-btn ${activeTabDim === dimName ? "active" : ""}`}
                onClick={() => setActiveTabDim(dimName)}
              >
                <span style={{ textTransform: "capitalize" }}>{dimName}</span>
                {auditResult.report.dimensions[dimName].warnings.length > 0 && (
                  <span
                    className="badge badge-warning"
                    style={{ fontSize: "9px", marginLeft: "6px", padding: "1px 4px" }}
                  >
                    {auditResult.report.dimensions[dimName].warnings.length}
                  </span>
                )}
              </button>
            ))}
          </div>

          {/* Active Dimension Details */}
          {activeDimResult && (
            <div className="card">
              <div className="card-header">
                <div>
                  <div className="card-title">
                    <span style={{ textTransform: "capitalize" }}>{activeDimResult.dimension_name}</span>
                    <span className="badge badge-neutral" style={{ textTransform: "uppercase", fontSize: "10px" }}>
                      {activeDimResult.dimension_type}
                    </span>
                    <span style={{ fontSize: "var(--text-xs)", color: "var(--text-muted)" }}>
                      Column: <code>{activeDimResult.column_name}</code>
                    </span>
                  </div>
                  <div className="card-description">
                    Valid Records: {activeDimResult.valid_records.toLocaleString()} | Missing: {activeDimResult.missing_records.toLocaleString()} ({(activeDimResult.missing_rate * 100).toFixed(1)}%) | Distinct Subgroups: {activeDimResult.observed_category_count}
                  </div>
                </div>
              </div>

              {/* Scorecard Gauges Row */}
              <div className="grid-4">
                <ScorecardGauge
                  score={activeDimResult.scorecard.completeness_score}
                  label="Completeness"
                  sublabel="Data hygiene & null rate"
                />
                <ScorecardGauge
                  score={activeDimResult.scorecard.coverage_score}
                  label="Category Coverage"
                  sublabel="Target subgroup presence"
                />
                <ScorecardGauge
                  score={activeDimResult.scorecard.parity_score}
                  label="Parity Alignment"
                  sublabel="Reference distribution gap"
                />
                <ScorecardGauge
                  score={activeDimResult.scorecard.composite_score}
                  label="Composite Quality"
                  sublabel="Weighted reliability index"
                />
              </div>

              {/* Interactive Wilson Confidence Interval Chart */}
              <div style={{ padding: "var(--space-4)", backgroundColor: "var(--bg-card-subtle)", borderRadius: "var(--radius-md)" }}>
                <ConfidenceIntervalChart
                  proportions={activeDimResult.proportions}
                  expectedDistribution={
                    dimensions.find((d) => d.name === activeDimResult.dimension_name)?.expected_distribution
                  }
                  dimensionName={activeDimResult.dimension_name}
                />
              </div>

              {/* Proportions Breakdown Table */}
              <div>
                <div className="label" style={{ marginBottom: "var(--space-2)" }}>
                  Subgroup Proportions, Wilson 95% Bounds & Disparities
                </div>
                <div className="table-container">
                  <table className="data-table">
                    <thead>
                      <tr>
                        <th>Subgroup Category</th>
                        <th>Observed Count</th>
                        <th>Observed Proportion</th>
                        <th>Wilson 95% Confidence Interval</th>
                        <th>Deviation from Target</th>
                        <th>Sample Uncertainty</th>
                      </tr>
                    </thead>
                    <tbody>
                      {Object.entries(activeDimResult.proportions).map(([cat, data]) => {
                        const dev = activeDimResult.deviations?.[cat];
                        return (
                          <tr key={cat}>
                            <td>
                              <strong>{cat}</strong>
                            </td>
                            <td style={{ fontFamily: "var(--font-mono)" }}>{data.count.toLocaleString()}</td>
                            <td style={{ fontFamily: "var(--font-mono)", fontWeight: 600 }}>
                              {(data.share * 100).toFixed(2)}%
                            </td>
                            <td style={{ fontFamily: "var(--font-mono)" }}>
                              [{(data.ci_lower * 100).toFixed(2)}% — {(data.ci_upper * 100).toFixed(2)}%]
                            </td>
                            <td>
                              {dev !== undefined && dev !== null ? (
                                <span
                                  className={`badge ${
                                    Math.abs(dev) > 0.15
                                      ? "badge-error"
                                      : Math.abs(dev) > 0.05
                                      ? "badge-warning"
                                      : "badge-success"
                                  }`}
                                >
                                  {dev > 0 ? "+" : ""}
                                  {(dev * 100).toFixed(1)}%
                                </span>
                              ) : (
                                <span style={{ color: "var(--text-muted)" }}>—</span>
                              )}
                            </td>
                            <td>
                              {data.sample_size_sparse ? (
                                <span className="badge badge-warning" title="Subgroup count N < 30. High statistical uncertainty.">
                                  Sparse (N &lt; 30)
                                </span>
                              ) : (
                                <span className="badge badge-success">Sufficient (N ≥ 30)</span>
                              )}
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Zero-Observation Underrepresentation Warning */}
              {activeDimResult.zero_observation_categories &&
                activeDimResult.zero_observation_categories.length > 0 && (
                  <div className="alert-banner high">
                    <AlertTriangle size={18} />
                    <div>
                      <strong>Critical Underrepresentation Alert: Zero-Observation Categories</strong>
                      <div style={{ fontSize: "var(--text-xs)", marginTop: "2px" }}>
                        The following expected demographic categories have 0 observations in this dataset:{" "}
                        <strong>{activeDimResult.zero_observation_categories.join(", ")}</strong>.
                      </div>
                    </div>
                  </div>
                )}

              {/* Active Dimension Warnings */}
              {activeDimResult.warnings && activeDimResult.warnings.length > 0 && (
                <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-2)" }}>
                  <div className="label">Active Dimension Warnings ({activeDimResult.warnings.length})</div>
                  {activeDimResult.warnings.map((w, i) => (
                    <WarningAlert key={i} warning={w} />
                  ))}
                </div>
              )}
            </div>
          )}

          {/* 2D Intersectional Cross-Tabulation Matrix (Safe Rendering) */}
          {auditResult.report.intersectional_results &&
            Object.keys(auditResult.report.intersectional_results).length > 0 && (
              <div className="card">
                <div className="card-header">
                  <div className="card-title">
                    <Layers size={18} style={{ color: "var(--color-primary)" }} />
                    2D Intersectional Cross-Tabulation
                  </div>
                  <div className="card-description">
                    Cross-evaluates subgroup pairings to detect compounded demographic exclusion.
                  </div>
                </div>

                {Object.entries(auditResult.report.intersectional_results).map(([pairKey, interData]: [string, any]) => {
                  if (!interData || !interData.matrix) return null;
                  const rows = Object.keys(interData.matrix);
                  const cols = rows.length > 0 ? Object.keys(interData.matrix[rows[0]] || {}) : [];
                  const labelA = interData.dimension_a || (interData.pair && interData.pair[0]) || pairKey.split("__x__")[0];
                  const labelB = interData.dimension_b || (interData.pair && interData.pair[1]) || pairKey.split("__x__")[1] || "Dimension B";

                  return (
                    <div key={pairKey} style={{ display: "flex", flexDirection: "column", gap: "var(--space-2)" }}>
                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                        <strong>Intersection: {labelA} × {labelB}</strong>
                        <div style={{ fontSize: "var(--text-xs)", color: "var(--text-muted)" }}>
                          Valid Sample: {interData.total_valid_intersection?.toLocaleString() || 0} | Sparse Cells (N&lt;30):{" "}
                          <span style={{ color: "var(--badge-warning-text)", fontWeight: 600 }}>
                            {interData.sparse_cell_count || 0}
                          </span>
                        </div>
                      </div>

                      <div className="table-container">
                        <table className="data-table">
                          <thead>
                            <tr>
                              <th>{labelA} \ {labelB}</th>
                              {cols.map((col) => (
                                <th key={col}>{col}</th>
                              ))}
                            </tr>
                          </thead>
                          <tbody>
                            {rows.map((row) => (
                              <tr key={row}>
                                <td>
                                  <strong>{row}</strong>
                                </td>
                                {cols.map((col) => {
                                  const count = interData.matrix[row]?.[col] || 0;
                                  const isSparse = count > 0 && count < 30;
                                  const isZero = count === 0;

                                  return (
                                    <td
                                      key={col}
                                      style={{
                                        fontFamily: "var(--font-mono)",
                                        backgroundColor: isZero
                                          ? "rgba(244, 63, 94, 0.12)"
                                          : isSparse
                                          ? "rgba(245, 158, 11, 0.1)"
                                          : "transparent",
                                        fontWeight: isZero || isSparse ? 700 : 400,
                                        color: isZero
                                          ? "var(--badge-error-text)"
                                          : isSparse
                                          ? "var(--badge-warning-text)"
                                          : "inherit",
                                      }}
                                    >
                                      {count}
                                      {isSparse && " *"}
                                    </td>
                                  );
                                })}
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
        </>
      )}
    </div>
  );
};
