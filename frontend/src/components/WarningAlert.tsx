import React, { useState } from "react";
import { AlertTriangle, AlertCircle, Info, ChevronDown, ChevronUp } from "lucide-react";
import { AuditWarning } from "../api/types";

interface WarningAlertProps {
  warning: AuditWarning;
}

export const WarningAlert: React.FC<WarningAlertProps> = ({ warning }) => {
  const [expanded, setExpanded] = useState(false);

  const getIcon = () => {
    switch (warning.severity) {
      case "HIGH":
        return <AlertCircle size={18} style={{ color: "var(--badge-error-text)", flexShrink: 0 }} />;
      case "MEDIUM":
        return <AlertTriangle size={18} style={{ color: "var(--badge-warning-text)", flexShrink: 0 }} />;
      default:
        return <Info size={18} style={{ color: "var(--badge-info-text)", flexShrink: 0 }} />;
    }
  };

  const getBannerClass = () => {
    switch (warning.severity) {
      case "HIGH":
        return "alert-banner high";
      case "MEDIUM":
        return "alert-banner medium";
      default:
        return "alert-banner low";
    }
  };

  return (
    <div className={getBannerClass()} style={{ flexDirection: "column", gap: "var(--space-2)" }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", width: "100%" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "var(--space-2)" }}>
          {getIcon()}
          <span style={{ fontWeight: 600 }}>{warning.title}</span>
          <span
            className={`badge ${
              warning.severity === "HIGH"
                ? "badge-error"
                : warning.severity === "MEDIUM"
                ? "badge-warning"
                : "badge-info"
            }`}
            style={{ fontSize: "10px" }}
          >
            {warning.severity}
          </span>
          <span style={{ fontSize: "var(--text-xs)", color: "inherit", opacity: 0.85 }}>
            ({warning.dimension})
          </span>
        </div>
        <button
          className="btn btn-ghost btn-sm"
          onClick={() => setExpanded(!expanded)}
          style={{ padding: "2px 6px", color: "inherit" }}
          aria-label={expanded ? "Collapse warning details" : "Expand warning details"}
        >
          {expanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
        </button>
      </div>

      <p style={{ margin: 0, fontSize: "var(--text-xs)", opacity: 0.95 }}>{warning.message}</p>

      {expanded && (
        <div
          style={{
            marginTop: "var(--space-1)",
            padding: "var(--space-2)",
            backgroundColor: "rgba(0, 0, 0, 0.15)",
            borderRadius: "var(--radius-sm)",
            fontSize: "var(--text-xs)",
            display: "flex",
            flexDirection: "column",
            gap: "var(--space-2)",
          }}
        >
          <div>
            <strong>Remediation Guidance:</strong> {warning.remediation_hint}
          </div>
          {warning.context && Object.keys(warning.context).length > 0 && (
            <div>
              <strong>Audit Context Telemetry:</strong>
              <pre
                style={{
                  marginTop: "4px",
                  padding: "6px",
                  backgroundColor: "rgba(0,0,0,0.25)",
                  borderRadius: "var(--radius-sm)",
                  fontSize: "11px",
                  overflowX: "auto",
                }}
              >
                {JSON.stringify(warning.context, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
