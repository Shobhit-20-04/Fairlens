import React from "react";
import { ProportionItem } from "../api/types";

interface ConfidenceIntervalChartProps {
  proportions: Record<string, ProportionItem>;
  expectedDistribution?: Record<string, number> | null;
  dimensionName: string;
}

export const ConfidenceIntervalChart: React.FC<ConfidenceIntervalChartProps> = ({
  proportions,
  expectedDistribution,
  dimensionName,
}) => {
  const categories = Object.keys(proportions);
  if (categories.length === 0) {
    return <div style={{ color: "var(--text-muted)", fontSize: "var(--text-sm)" }}>No category observations available.</div>;
  }

  // Find max value for scaling (with padding up to 100%)
  const maxProportion = Math.max(
    ...categories.map((c) => Math.max(proportions[c].ci_upper, expectedDistribution?.[c] || 0)),
    0.3
  );
  const chartMax = Math.min(1.0, Math.ceil(maxProportion * 10) / 10 + 0.05);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-3)" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span style={{ fontSize: "var(--text-xs)", color: "var(--text-muted)", fontWeight: 600, textTransform: "uppercase" }}>
          Category Proportions & Wilson 95% Confidence Intervals ({dimensionName})
        </span>
        <div style={{ display: "flex", gap: "var(--space-3)", fontSize: "var(--text-xs)" }}>
          <span style={{ display: "flex", alignItems: "center", gap: "4px" }}>
            <span style={{ width: 10, height: 10, backgroundColor: "var(--color-primary)", borderRadius: 2 }} />
            Observed Proportion
          </span>
          <span style={{ display: "flex", alignItems: "center", gap: "4px" }}>
            <span style={{ width: 12, height: 2, backgroundColor: "#fbbf24", display: "inline-block" }} />
            Wilson 95% CI
          </span>
          {expectedDistribution && (
            <span style={{ display: "flex", alignItems: "center", gap: "4px" }}>
              <span style={{ width: 2, height: 10, backgroundColor: "#f43f5e", display: "inline-block" }} />
              Expected Target
            </span>
          )}
        </div>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-2)" }}>
        {categories.map((cat) => {
          const item = proportions[cat];
          const observedPct = (item.share / chartMax) * 100;
          const ciLowerPct = (item.ci_lower / chartMax) * 100;
          const ciUpperPct = (item.ci_upper / chartMax) * 100;
          const expectedVal = expectedDistribution?.[cat];
          const expectedPct = expectedVal !== undefined ? (expectedVal / chartMax) * 100 : null;

          return (
            <div key={cat} style={{ display: "grid", gridTemplateColumns: "180px 1fr 140px", alignItems: "center", gap: "var(--space-3)" }}>
              {/* Category Label */}
              <div style={{ display: "flex", alignItems: "center", gap: "var(--space-1)" }}>
                <span style={{ fontSize: "var(--text-sm)", fontWeight: 600, color: "var(--text-primary)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }} title={cat}>
                  {cat}
                </span>
                {item.sample_size_sparse && (
                  <span className="badge badge-warning" style={{ fontSize: "9px", padding: "1px 4px" }} title="Sample count N < 30. Elevated uncertainty.">
                    N&lt;30
                  </span>
                )}
              </div>

              {/* Bar and Error Whisker Canvas */}
              <div style={{ position: "relative", height: 24, backgroundColor: "var(--bg-card-subtle)", borderRadius: "var(--radius-sm)", overflow: "visible" }}>
                {/* Observed Bar */}
                <div
                  style={{
                    position: "absolute",
                    left: 0,
                    top: 4,
                    bottom: 4,
                    width: `${Math.max(1, observedPct)}%`,
                    backgroundColor: "var(--color-primary)",
                    borderRadius: "var(--radius-sm)",
                    opacity: 0.85,
                  }}
                />

                {/* Wilson CI Whisker Line */}
                <div
                  style={{
                    position: "absolute",
                    left: `${ciLowerPct}%`,
                    width: `${Math.max(2, ciUpperPct - ciLowerPct)}%`,
                    top: 11,
                    height: 2,
                    backgroundColor: "#fbbf24",
                    zIndex: 2,
                  }}
                />
                {/* CI Left Cap */}
                <div
                  style={{
                    position: "absolute",
                    left: `${ciLowerPct}%`,
                    top: 7,
                    height: 10,
                    width: 2,
                    backgroundColor: "#fbbf24",
                    zIndex: 2,
                  }}
                />
                {/* CI Right Cap */}
                <div
                  style={{
                    position: "absolute",
                    left: `${ciUpperPct}%`,
                    top: 7,
                    height: 10,
                    width: 2,
                    backgroundColor: "#fbbf24",
                    zIndex: 2,
                  }}
                />

                {/* Expected Reference Marker */}
                {expectedPct !== null && (
                  <div
                    style={{
                      position: "absolute",
                      left: `${expectedPct}%`,
                      top: 1,
                      bottom: 1,
                      width: 2,
                      backgroundColor: "#f43f5e",
                      zIndex: 3,
                    }}
                    title={`Expected: ${(expectedVal! * 100).toFixed(1)}%`}
                  />
                )}
              </div>

              {/* Numerical readout */}
              <div style={{ fontSize: "var(--text-xs)", color: "var(--text-secondary)", textAlign: "right", fontFamily: "var(--font-mono)" }}>
                <span>{(item.share * 100).toFixed(1)}%</span>{" "}
                <span style={{ color: "var(--text-muted)" }}>
                  [{(item.ci_lower * 100).toFixed(1)}%-{(item.ci_upper * 100).toFixed(1)}%]
                </span>{" "}
                <span style={{ color: "var(--text-muted)" }}>(n={item.count})</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
