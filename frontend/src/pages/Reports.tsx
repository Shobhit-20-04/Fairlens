import React, { useState } from "react";
import { FileText, Download, CheckCircle2, AlertTriangle, ShieldCheck, Copy } from "lucide-react";
import { api } from "../api/client";
import { AuditReport } from "../api/types";

interface ReportsProps {
  currentReport: AuditReport | null;
  currentSummaryText: string | null;
  currentReportId: string | null;
}

export const Reports: React.FC<ReportsProps> = ({
  currentReport,
  currentSummaryText,
  currentReportId,
}) => {
  const [downloadSuccess, setDownloadSuccess] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  const handleExport = async (format: "json" | "csv") => {
    if (!currentReportId) return;
    try {
      const res = await api.exportAudit(currentReportId, format);
      setDownloadSuccess(`Exported ${res.format.toUpperCase()} to ${res.file_path}`);
      setTimeout(() => setDownloadSuccess(null), 5000);
    } catch (err: any) {
      alert("Export failed: " + err.message);
    }
  };

  const handleCopySummary = () => {
    if (currentSummaryText) {
      navigator.clipboard.writeText(currentSummaryText);
      setCopied(true);
      setTimeout(() => setCopied(false), 3000);
    }
  };

  return (
    <div className="page-content">
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "var(--space-3)" }}>
        <div>
          <h1 style={{ fontSize: "var(--text-xl)", fontWeight: 700 }}>Audit Reports & Export Archive</h1>
          <p style={{ color: "var(--text-muted)", fontSize: "var(--text-sm)", marginTop: "2px" }}>
            Reproducible academic reports with methodology transparency, scorecards, and export files.
          </p>
        </div>

        {currentReportId && (
          <div style={{ display: "flex", gap: "var(--space-2)" }}>
            <button className="btn btn-secondary" onClick={() => handleExport("json")}>
              <Download size={14} />
              <span>Download JSON</span>
            </button>
            <button className="btn btn-secondary" onClick={() => handleExport("csv")}>
              <Download size={14} />
              <span>Download CSV</span>
            </button>
          </div>
        )}
      </div>

      {downloadSuccess && (
        <div className="alert-banner low">
          <CheckCircle2 size={18} />
          <span>{downloadSuccess}</span>
        </div>
      )}

      {!currentReport ? (
        <div className="card" style={{ textAlign: "center", padding: "var(--space-10)", color: "var(--text-muted)" }}>
          <FileText size={40} style={{ margin: "0 auto var(--space-3)", opacity: 0.5 }} />
          <h3 style={{ fontSize: "var(--text-base)", color: "var(--text-primary)" }}>No Audit Report Generated Yet</h3>
          <p style={{ fontSize: "var(--text-sm)", maxWidth: "500px", margin: "var(--space-2) auto var(--space-4)" }}>
            Navigate to the Representation Audit screen to run an audit on a dataset. The structured report and academic summary will appear here automatically.
          </p>
        </div>
      ) : (
        <>
          {/* Executive Summary Card */}
          <div className="card">
            <div className="card-header">
              <div className="card-title">
                <ShieldCheck size={18} style={{ color: "var(--color-primary)" }} />
                Executive Audit Summary: {currentReport.dataset_profile.file_name || "Dataset"}
              </div>
              <button className="btn btn-outline btn-sm" onClick={handleCopySummary}>
                <Copy size={13} />
                <span>{copied ? "Copied!" : "Copy Summary Text"}</span>
              </button>
            </div>

            <div className="grid-4">
              <div className="stat-card">
                <div className="stat-label">Total Records</div>
                <div className="stat-value">{currentReport.dataset_profile.total_rows.toLocaleString()}</div>
                <div className="stat-hint">{currentReport.dataset_profile.total_columns} columns inspected</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">Duplicate Rate</div>
                <div className="stat-value">{(currentReport.dataset_profile.duplicate_rate * 100).toFixed(1)}%</div>
                <div className="stat-hint">{currentReport.dataset_profile.duplicate_rows} duplicate rows</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">Total Warnings</div>
                <div className="stat-value" style={{ color: currentReport.high_severity_warnings > 0 ? "var(--badge-error-text)" : "var(--badge-success-text)" }}>
                  {currentReport.total_warnings_count}
                </div>
                <div className="stat-hint">{currentReport.high_severity_warnings} High Severity</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">Execution Time</div>
                <div className="stat-value">{currentReport.execution_time_seconds.toFixed(3)}s</div>
                <div className="stat-hint">Report ID: {currentReportId}</div>
              </div>
            </div>

            {/* Dimension Scorecards Table */}
            <div>
              <div className="label" style={{ marginBottom: "var(--space-2)" }}>
                Audited Dimension Scorecards
              </div>
              <div className="table-container">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Dimension</th>
                      <th>Column</th>
                      <th>Missing Rate</th>
                      <th>Completeness</th>
                      <th>Coverage</th>
                      <th>Parity</th>
                      <th>Composite</th>
                      <th>Active Warnings</th>
                    </tr>
                  </thead>
                  <tbody>
                    {Object.entries(currentReport.dimensions).map(([dimName, dimData]) => (
                      <tr key={dimName}>
                        <td>
                          <strong style={{ textTransform: "capitalize" }}>{dimName}</strong>
                        </td>
                        <td>
                          <code>{dimData.column_name}</code>
                        </td>
                        <td>{(dimData.missing_rate * 100).toFixed(1)}%</td>
                        <td>{dimData.scorecard.completeness_score.toFixed(1)}</td>
                        <td>{dimData.scorecard.coverage_score !== null ? dimData.scorecard.coverage_score.toFixed(1) : "N/A"}</td>
                        <td>{dimData.scorecard.parity_score !== null ? dimData.scorecard.parity_score.toFixed(1) : "N/A"}</td>
                        <td>
                          {dimData.scorecard.composite_score !== null ? (
                            <strong
                              style={{
                                color:
                                  dimData.scorecard.composite_score >= 80
                                    ? "var(--badge-success-text)"
                                    : dimData.scorecard.composite_score >= 60
                                    ? "var(--badge-warning-text)"
                                    : "var(--badge-error-text)",
                              }}
                            >
                              {dimData.scorecard.composite_score.toFixed(1)}
                            </strong>
                          ) : (
                            "N/A"
                          )}
                        </td>
                        <td>
                          {dimData.warnings.length > 0 ? (
                            <span className="badge badge-warning">{dimData.warnings.length} Warnings</span>
                          ) : (
                            <span className="badge badge-success">0 Warnings</span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          {/* Formatted Text Report Preview */}
          {currentSummaryText && (
            <div className="card">
              <div className="card-header">
                <div className="card-title">
                  <FileText size={16} style={{ color: "var(--color-primary)" }} />
                  Full Formatted Academic Summary (Markdown)
                </div>
              </div>
              <pre
                style={{
                  backgroundColor: "var(--bg-card-subtle)",
                  padding: "var(--space-4)",
                  borderRadius: "var(--radius-md)",
                  fontSize: "var(--text-xs)",
                  color: "var(--text-primary)",
                  overflowX: "auto",
                  lineHeight: 1.6,
                }}
              >
                {currentSummaryText}
              </pre>
            </div>
          )}
        </>
      )}
    </div>
  );
};
