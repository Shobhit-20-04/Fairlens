import React, { useState, useEffect } from "react";
import {
  BarChart2,
  Play,
  Sliders,
  AlertTriangle,
  FileCheck,
  Download,
  Plus,
  Trash2,
  Layers,
  Sparkles,
  Info,
  CheckCircle2,
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

  // Audit Dimensions Config
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
  const [exportMessage, setExportMessage] = useState<string | null>(null);

  useEffect(() => {
    // Load pre-loaded sample datasets
    api
      .getSampleDatasets()
      .then((res) => {
        setSamples(res.samples);
      })
      .catch((err) => console.error("Failed to fetch samples:", err));

    // If no initial audit ran, run automatically for quick demonstration
    runAuditExecution();
  }, []);

  const handleSelectSample = (sample: SampleDataset) => {
    setFilePath(sample.file_path);
    if (sample.recommended_dimensions && sample.recommended_dimensions.length > 0) {
      setDimensions(sample.recommended_dimensions);
      setActiveTabDim(sample.recommended_dimensions[0].name);
    }
  };

  const handleAddDimension = () => {
    const newDim: AuditDimensionSpec = {
      name: `dim_${dimensions.length + 1}`,
      column_name: "",
      dimension_type: "demographic",
      min_sample_size: 30,
    };
    setDimensions([...dimensions, newDim]);
    setActiveTabDim(newDim.name);
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

  const runAuditExecution = async () => {
    setLoading(true);
    setError(null);
    setExportMessage(null);

    try {
      const intersectionalPairs: [string, string][] = enableIntersectional
        ? [
            ["gender", "state"],
            ["gender", "religion"],
          ]
        : [];

      const res = await api.runAudit({
        file_path: filePath,
        dimensions,
        intersectional_pairs: intersectionalPairs.length > 0 ? intersectionalPairs : undefined,
        confidence_level: confidenceLevel,
      });

      setAuditResult(res);
      onSetReport(res.report, res.summary_text, res.report_id);
    } catch (err: any) {
      setError(err.message || "Audit execution failed");
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async (format: "json" | "csv") => {
    if (!auditResult) return;
    try {
      const res = await api.exportAudit(auditResult.report_id, format);
      setExportMessage(`Successfully exported ${res.format.toUpperCase()} report to ${res.file_name} (${res.size_bytes} bytes)`);
    } catch (err: any) {
      setError(err.message || "Export failed");
    }
  };

  const activeDimResult = auditResult?.report.dimensions[activeTabDim];

  return (
    <div className="page-content">
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "var(--space-3)" }}>
        <div>
          <h1 style={{ fontSize: "var(--text-xl)", fontWeight: 700 }}>Dataset Representation-Gap Audit</h1>
          <p style={{ color: "var(--text-muted)", fontSize: "var(--text-sm)", marginTop: "2px" }}>
            Phase 4 Engine: Wilson 95% Confidence Intervals, category coverage, parity deviations, and intersectional cross-tabs.
          </p>
        </div>

        <button className="btn btn-primary" onClick={runAuditExecution} disabled={loading}>
          <Play size={15} />
          <span>{loading ? "Computing Metrics in Python..." : "Run Representation Audit"}</span>
        </button>
      </div>

      {/* Dataset & Configuration Card */}
      <div className="card">
        <div className="card-header">
          <div className="card-title">
            <Sliders size={16} style={{ color: "var(--color-primary)" }} />
            Audit Parameters & Demographic Dimension Specifications
          </div>

          {/* Quick preset selector */}
          <div style={{ display: "flex", alignItems: "center", gap: "var(--space-2)" }}>
            <span style={{ fontSize: "var(--text-xs)", color: "var(--text-muted)" }}>Benchmark Pre-set:</span>
            <select
              className="select"
              style={{ width: "auto", padding: "4px 8px", fontSize: "var(--text-xs)" }}
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
        </div>

        {/* Dimension Configuration Table */}
        <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-3)" }}>
          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Dimension Name</th>
                  <th>Dataset Column</th>
                  <th>Dimension Type</th>
                  <th>Expected Categories / Distribution</th>
                  <th>Min Sample (N)</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {dimensions.map((dim, idx) => (
                  <tr key={idx}>
                    <td>
                      <input
                        type="text"
                        className="input"
                        value={dim.name}
                        onChange={(e) => handleUpdateDimension(idx, "name", e.target.value)}
                        style={{ padding: "4px 8px", fontSize: "var(--text-xs)" }}
                      />
                    </td>
                    <td>
                      <input
                        type="text"
                        className="input"
                        value={dim.column_name}
                        onChange={(e) => handleUpdateDimension(idx, "column_name", e.target.value)}
                        style={{ padding: "4px 8px", fontSize: "var(--text-xs)", fontFamily: "var(--font-mono)" }}
                      />
                    </td>
                    <td>
                      <select
                        className="select"
                        value={dim.dimension_type}
                        onChange={(e) => handleUpdateDimension(idx, "dimension_type", e.target.value)}
                        style={{ padding: "4px 8px", fontSize: "var(--text-xs)" }}
                      >
                        <option value="demographic">Demographic</option>
                        <option value="geographic">Geographic</option>
                        <option value="cultural">Cultural</option>
                        <option value="custom">Custom</option>
                      </select>
                    </td>
                    <td>
                      <input
                        type="text"
                        className="input"
                        placeholder='{"Male": 0.5, "Female": 0.5}'
                        value={
                          dim.expected_distribution
                            ? JSON.stringify(dim.expected_distribution)
                            : dim.expected_categories
                            ? dim.expected_categories.join(", ")
                            : ""
                        }
                        onChange={(e) => {
                          const val = e.target.value.trim();
                          if (val.startsWith("{")) {
                            try {
                              const parsed = JSON.parse(val);
                              handleUpdateDimension(idx, "expected_distribution", parsed);
                              handleUpdateDimension(idx, "expected_categories", Object.keys(parsed));
                            } catch {
                              // user still typing json
                            }
                          } else if (val) {
                            handleUpdateDimension(
                              idx,
                              "expected_categories",
                              val.split(",").map((s) => s.trim())
                            );
                            handleUpdateDimension(idx, "expected_distribution", undefined);
                          }
                        }}
                        style={{ padding: "4px 8px", fontSize: "var(--text-xs)", fontFamily: "var(--font-mono)" }}
                      />
                    </td>
                    <td style={{ width: 100 }}>
                      <input
                        type="number"
                        className="input"
                        value={dim.min_sample_size || 30}
                        onChange={(e) => handleUpdateDimension(idx, "min_sample_size", parseInt(e.target.value, 10))}
                        style={{ padding: "4px 8px", fontSize: "var(--text-xs)" }}
                      />
                    </td>
                    <td style={{ width: 60 }}>
                      <button
                        className="btn btn-ghost btn-sm"
                        onClick={() => handleRemoveDimension(idx)}
                        disabled={dimensions.length <= 1}
                        title="Remove Dimension"
                      >
                        <Trash2 size={14} style={{ color: "var(--badge-error-text)" }} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "var(--space-3)" }}>
            <button className="btn btn-secondary btn-sm" onClick={handleAddDimension}>
              <Plus size={13} />
              <span>Add Dimension</span>
            </button>

            <div style={{ display: "flex", alignItems: "center", gap: "var(--space-4)", fontSize: "var(--text-xs)" }}>
              <label style={{ display: "flex", alignItems: "center", gap: "var(--space-2)", cursor: "pointer" }}>
                <input
                  type="checkbox"
                  checked={enableIntersectional}
                  onChange={(e) => setEnableIntersectional(e.target.checked)}
                />
                <span>Enable 2D Intersectional Cross-tabs (e.g. gender × state)</span>
              </label>

              <div style={{ display: "flex", alignItems: "center", gap: "var(--space-2)" }}>
                <span>Confidence Level:</span>
                <select
                  className="select"
                  style={{ width: "auto", padding: "2px 6px", fontSize: "var(--text-xs)" }}
                  value={confidenceLevel}
                  onChange={(e) => setConfidenceLevel(parseFloat(e.target.value))}
                >
                  <option value={0.9}>90% (z=1.645)</option>
                  <option value={0.95}>95% (z=1.960)</option>
                  <option value={0.99}>99% (z=2.576)</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Error or Export Message */}
      {error && (
        <div className="alert-banner high">
          <AlertTriangle size={18} />
          <span>{error}</span>
        </div>
      )}
      {exportMessage && (
        <div className="alert-banner low">
          <CheckCircle2 size={18} />
          <span>{exportMessage}</span>
        </div>
      )}

      {/* Audit Findings Section */}
      {auditResult && (
        <>
          {/* Summary Metric Ribbon */}
          <div className="grid-4">
            <div className="stat-card">
              <div className="stat-label">Audit Dataset</div>
              <div className="stat-value" style={{ fontSize: "var(--text-lg)" }}>
                {auditResult.report.dataset_profile.file_name || "Synthetic Tabular"}
              </div>
              <div className="stat-hint">
                {auditResult.report.dataset_profile.total_rows.toLocaleString()} records • {auditResult.report.dataset_profile.total_columns} columns
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-label">Execution Time</div>
              <div className="stat-value">{auditResult.report.execution_time_seconds.toFixed(3)}s</div>
              <div className="stat-hint">Python vectorized calculation</div>
            </div>

            <div className="stat-card">
              <div className="stat-label">Total Warnings</div>
              <div
                className="stat-value"
                style={{
                  color: auditResult.report.high_severity_warnings > 0 ? "var(--badge-error-text)" : "var(--badge-success-text)",
                }}
              >
                {auditResult.report.total_warnings_count}
              </div>
              <div className="stat-hint">
                {auditResult.report.high_severity_warnings} High Severity
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-label">Report Export</div>
              <div style={{ display: "flex", gap: "var(--space-2)", marginTop: "var(--space-1)" }}>
                <button className="btn btn-secondary btn-sm" onClick={() => handleExport("json")} style={{ flex: 1 }}>
                  <Download size={12} />
                  <span>JSON</span>
                </button>
                <button className="btn btn-secondary btn-sm" onClick={() => handleExport("csv")} style={{ flex: 1 }}>
                  <Download size={12} />
                  <span>CSV</span>
                </button>
              </div>
              <div className="stat-hint">Outputs to outputs/audit_reports/</div>
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
                  <span className="badge badge-warning" style={{ fontSize: "9px", marginLeft: "6px", padding: "1px 4px" }}>
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
                    <span className="badge badge-neutral">{activeDimResult.dimension_type}</span>
                    <span style={{ fontSize: "var(--text-xs)", color: "var(--text-muted)" }}>
                      Column: <code>{activeDimResult.column_name}</code>
                    </span>
                  </div>
                  <div className="card-description">
                    Valid Records: {activeDimResult.valid_records.toLocaleString()} | Missing: {activeDimResult.missing_records.toLocaleString()} ({(activeDimResult.missing_rate * 100).toFixed(1)}%) | Observed Categories: {activeDimResult.observed_category_count}
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
                  sublabel="Proportion alignment to target"
                />
                <ScorecardGauge
                  score={activeDimResult.scorecard.composite_score}
                  label="Composite Score"
                  sublabel="Penalty-weighted quality"
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
                  Detailed Proportions, Bounds, and Deviations
                </div>
                <div className="table-container">
                  <table className="data-table">
                    <thead>
                      <tr>
                        <th>Category</th>
                        <th>Observed Count</th>
                        <th>Observed Share</th>
                        <th>Wilson 95% Confidence Interval</th>
                        <th>Deviation from Target</th>
                        <th>Sample Size Uncertainty</th>
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
                                <span style={{ color: "var(--text-muted)" }}>No target reference</span>
                              )}
                            </td>
                            <td>
                              {data.sample_size_sparse ? (
                                <span className="badge badge-warning" title="Subgroup sample count N < 30. Caution advised.">
                                  N &lt; 30 (Sparse)
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

              {/* Zero-Observation Warning Box */}
              {activeDimResult.zero_observation_categories.length > 0 && (
                <div className="alert-banner high">
                  <AlertTriangle size={18} />
                  <div>
                    <strong>Critical Underrepresentation Alert: Zero-Observation Categories</strong>
                    <div style={{ fontSize: "var(--text-xs)", marginTop: "2px" }}>
                      The following expected target demographic categories have 0 observations in this dataset:{" "}
                      <strong>{activeDimResult.zero_observation_categories.join(", ")}</strong>.
                    </div>
                  </div>
                </div>
              )}

              {/* Statistical Divergence Indicators */}
              {activeDimResult.max_abs_deviation !== null && (
                <div className="grid-3">
                  <div className="stat-card">
                    <div className="stat-label">Max Absolute Deviation</div>
                    <div className="stat-value">{((activeDimResult.max_abs_deviation || 0) * 100).toFixed(1)}%</div>
                    <div className="stat-hint">Peak subgroup disparity</div>
                  </div>
                  <div className="stat-card">
                    <div className="stat-label">Mean Absolute Deviation</div>
                    <div className="stat-value">{((activeDimResult.mean_abs_deviation || 0) * 100).toFixed(1)}%</div>
                    <div className="stat-hint">Average distribution gap</div>
                  </div>
                  <div className="stat-card">
                    <div className="stat-label">Jensen-Shannon Divergence</div>
                    <div className="stat-value">{(activeDimResult.js_divergence || 0).toFixed(4)}</div>
                    <div className="stat-hint">JSD distance (0.0=identical, 1.0=disjoint)</div>
                  </div>
                </div>
              )}

              {/* Active Dimension Warnings */}
              {activeDimResult.warnings.length > 0 && (
                <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-2)" }}>
                  <div className="label">Active Dimension Warnings ({activeDimResult.warnings.length})</div>
                  {activeDimResult.warnings.map((w, i) => (
                    <WarningAlert key={i} warning={w} />
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Intersectional Cross-Tabulation Matrix */}
          {auditResult.report.intersectional_results &&
            Object.keys(auditResult.report.intersectional_results).length > 0 && (
              <div className="card">
                <div className="card-header">
                  <div className="card-title">
                    <Layers size={18} style={{ color: "var(--color-primary)" }} />
                    2D Intersectional Representation Cross-Tabulations
                  </div>
                  <div className="card-description">
                    Evaluates intersectional subgroup representation (e.g. Gender × State) to detect compounded demographic exclusion.
                  </div>
                </div>

                {Object.entries(auditResult.report.intersectional_results).map(([pairKey, interData]) => {
                  const rows = Object.keys(interData.matrix);
                  const cols = rows.length > 0 ? Object.keys(interData.matrix[rows[0]]) : [];

                  return (
                    <div key={pairKey} style={{ display: "flex", flexDirection: "column", gap: "var(--space-2)" }}>
                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                        <strong>Intersection: {pairKey}</strong>
                        <div style={{ fontSize: "var(--text-xs)", color: "var(--text-muted)" }}>
                          Total Valid: {interData.total_valid_intersection.toLocaleString()} | Sparse Cells (N&lt;30):{" "}
                          <span style={{ color: "var(--badge-warning-text)", fontWeight: 600 }}>
                            {interData.sparse_cell_count}
                          </span>
                        </div>
                      </div>

                      <div className="table-container">
                        <table className="data-table">
                          <thead>
                            <tr>
                              <th>{interData.pair[0]} / {interData.pair[1]}</th>
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
                                          ? "rgba(244, 63, 94, 0.15)"
                                          : isSparse
                                          ? "rgba(245, 158, 11, 0.12)"
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

          {/* Academic Assumptions & Limitations */}
          <div className="card" style={{ backgroundColor: "var(--bg-card-subtle)" }}>
            <div className="card-header">
              <div className="card-title" style={{ fontSize: "var(--text-sm)" }}>
                <Info size={16} style={{ color: "var(--color-primary)" }} />
                Methodological Assumptions & Limitations (Audit Transparency)
              </div>
            </div>
            <ul style={{ fontSize: "var(--text-xs)", color: "var(--text-secondary)", paddingLeft: "var(--space-5)", display: "flex", flexDirection: "column", gap: "var(--space-1)" }}>
              {auditResult.report.assumptions_and_limitations.map((caveat, idx) => (
                <li key={idx}>{caveat}</li>
              ))}
            </ul>
          </div>
        </>
      )}
    </div>
  );
};
