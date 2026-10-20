import React from "react";

interface ScorecardGaugeProps {
  score: number | null;
  label: string;
  sublabel?: string;
  size?: number;
}

export const ScorecardGauge: React.FC<ScorecardGaugeProps> = ({
  score,
  label,
  sublabel,
  size = 110,
}) => {
  if (score === null || score === undefined) {
    return (
      <div className="stat-card" style={{ alignItems: "center", textAlign: "center" }}>
        <div className="stat-label">{label}</div>
        <div style={{ color: "var(--text-muted)", fontSize: "var(--text-sm)", margin: "14px 0" }}>
          N/A (Descriptive)
        </div>
        {sublabel && <div className="stat-hint">{sublabel}</div>}
      </div>
    );
  }

  const strokeWidth = 9;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const clampedScore = Math.max(0, Math.min(100, score));
  const strokeDashoffset = circumference - (clampedScore / 100) * circumference;

  let color = "var(--badge-error-text)";
  let strokeColor = "#f43f5e";
  if (clampedScore >= 80) {
    color = "var(--badge-success-text)";
    strokeColor = "#10b981";
  } else if (clampedScore >= 60) {
    color = "var(--badge-warning-text)";
    strokeColor = "#f59e0b";
  }

  return (
    <div className="stat-card" style={{ alignItems: "center", textAlign: "center" }}>
      <div className="stat-label">{label}</div>
      <div style={{ position: "relative", width: size, height: size, margin: "6px 0" }}>
        <svg width={size} height={size} style={{ transform: "rotate(-90deg)" }}>
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="var(--border-default)"
            strokeWidth={strokeWidth}
            fill="transparent"
          />
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={strokeColor}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            style={{ transition: "stroke-dashoffset 0.8s ease" }}
          />
        </svg>
        <div
          style={{
            position: "absolute",
            inset: 0,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            flexDirection: "column",
          }}
        >
          <span style={{ fontSize: "var(--text-xl)", fontWeight: 700, color }}>
            {clampedScore.toFixed(1)}
          </span>
          <span style={{ fontSize: "10px", color: "var(--text-muted)", marginTop: "-2px" }}>
            / 100
          </span>
        </div>
      </div>
      {sublabel && <div className="stat-hint">{sublabel}</div>}
    </div>
  );
};
