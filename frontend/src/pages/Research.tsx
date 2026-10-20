import React, { useState, useEffect } from "react";
import {
  Calculator,
  Cpu,
  Layers,
  HelpCircle,
} from "lucide-react";
import { api } from "../api/client";
import { CostEstimate } from "../api/types";

export const Research: React.FC = () => {
  const [runs, setRuns] = useState<number>(200);
  const [inputTokens, setInputTokens] = useState<number>(850);
  const [outputTokens, setOutputTokens] = useState<number>(300);
  const [useFreeTier, setUseFreeTier] = useState<boolean>(true);
  const [costEstimate, setCostEstimate] = useState<CostEstimate | null>(null);

  useEffect(() => {
    calculateCost();
  }, [runs, inputTokens, outputTokens, useFreeTier]);

  const calculateCost = async () => {
    try {
      const res = await api.estimateCost({
        runs,
        input_tokens: inputTokens,
        output_tokens: outputTokens,
        use_free_tier: useFreeTier,
      });
      setCostEstimate(res);
    } catch (err) {
      console.error("Cost estimate failed:", err);
    }
  };

  return (
    <div className="page-content">
      {/* Header */}
      <div>
        <h1 style={{ fontSize: "var(--text-xl)", fontWeight: 700 }}>
          Nemotron 3 Ultra Research & Cost Estimator
        </h1>
        <p style={{ color: "var(--text-muted)", fontSize: "var(--text-sm)", marginTop: "2px" }}>
          Phase 2 Infrastructure & Layer B Case Study evaluating <code>nvidia/nemotron-3-ultra-550b-a55b</code>.
        </p>
      </div>

      {/* Target Model Verified Specs */}
      <div className="card">
        <div className="card-header">
          <div className="card-title">
            <Cpu size={16} style={{ color: "var(--color-primary)" }} />
            Verified Architecture & Safety Card Facts
          </div>
        </div>

        <div className="grid-3">
          <div className="stat-card">
            <div className="stat-label">Model Architecture</div>
            <div className="stat-value" style={{ fontSize: "var(--text-base)" }}>550B MoE</div>
            <div className="stat-hint">~55B active parameters per token pass</div>
          </div>

          <div className="stat-card">
            <div className="stat-label">Verified OpenRouter Pricing</div>
            <div className="stat-value" style={{ fontSize: "var(--text-base)", color: "var(--badge-success-text)" }}>
              $0.00 Free Tier
            </div>
            <div className="stat-hint">nvidia/nemotron-3-ultra-550b-a55b:free</div>
          </div>

          <div className="stat-card">
            <div className="stat-label">Safety Card Finding</div>
            <div className="stat-value" style={{ fontSize: "var(--text-base)", color: "var(--badge-warning-text)" }}>
              Bias Mitigation: "None"
            </div>
            <div className="stat-hint">Official NVIDIA model card documentation</div>
          </div>
        </div>
      </div>

      {/* Token Cost Estimator */}
      <div className="card">
        <div className="card-header">
          <div className="card-title">
            <Calculator size={16} style={{ color: "var(--color-primary)" }} />
            Inference Cost Estimator & Budget Ceiling Enforcement
          </div>
          <div className="card-description">
            Verifies that projected evaluation batches remain strictly below the $5.00 budget ceiling.
          </div>
        </div>

        <div className="grid-2">
          {/* Controls */}
          <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-3)" }}>
            <div className="form-group">
              <label className="label">Evaluation Vignettes (Test Runs)</label>
              <input
                type="number"
                className="input"
                value={runs}
                onChange={(e) => setRuns(Math.max(1, parseInt(e.target.value) || 1))}
              />
            </div>

            <div className="form-group">
              <label className="label">Average Input Tokens per Vignette</label>
              <input
                type="number"
                className="input"
                value={inputTokens}
                onChange={(e) => setInputTokens(Math.max(1, parseInt(e.target.value) || 1))}
              />
            </div>

            <div className="form-group">
              <label className="label">Average Output Tokens per Decision</label>
              <input
                type="number"
                className="input"
                value={outputTokens}
                onChange={(e) => setOutputTokens(Math.max(1, parseInt(e.target.value) || 1))}
              />
            </div>

            <label style={{ display: "flex", alignItems: "center", gap: "var(--space-2)", fontSize: "var(--text-xs)", cursor: "pointer", color: "var(--text-secondary)" }}>
              <input
                type="checkbox"
                checked={useFreeTier}
                onChange={(e) => setUseFreeTier(e.target.checked)}
              />
              <span>Route via OpenRouter Free Tier ($0.00 / 1M tokens)</span>
            </label>
          </div>

          {/* Cost Result */}
          {costEstimate && (
            <div
              style={{
                backgroundColor: "var(--bg-card-subtle)",
                borderRadius: "var(--radius-md)",
                padding: "var(--space-4)",
                display: "flex",
                flexDirection: "column",
                gap: "var(--space-2)",
                border: "1px solid var(--border-subtle)",
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <span className="label">Projected Inference Spend</span>
                <span className={`badge ${costEstimate.is_within_budget ? "badge-success" : "badge-error"}`}>
                  {costEstimate.is_within_budget ? "Within $5.00 Limit" : "Exceeds Budget Limit"}
                </span>
              </div>

              <div style={{ fontSize: "var(--text-2xl)", fontWeight: 700 }}>
                ${costEstimate.total_cost_usd.toFixed(4)} USD
              </div>

              <div style={{ fontSize: "var(--text-xs)", color: "var(--text-secondary)", display: "flex", flexDirection: "column", gap: "var(--space-1)" }}>
                <div>Total Input Tokens: {costEstimate.input_tokens_total.toLocaleString()} (${costEstimate.input_cost_usd.toFixed(4)})</div>
                <div>Total Output Tokens: {costEstimate.output_tokens_total.toLocaleString()} (${costEstimate.output_cost_usd.toFixed(4)})</div>
                <div>Safety Margin Buffer: +{(costEstimate.safety_margin * 100).toFixed(0)}%</div>
                <div>Hard Budget Limit: ${costEstimate.budget_limit_usd.toFixed(2)} USD</div>
              </div>

              <div style={{ fontSize: "var(--text-xs)", color: "var(--text-muted)", marginTop: "auto" }}>
                {useFreeTier
                  ? "✓ Verified free endpoint selected: $0.00 API inference cost."
                  : "Paid marketplace routing estimate ($0.60/M in, $3.60/M out)."}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Planned Methodology Overview */}
      <div className="card">
        <div className="card-header">
          <div className="card-title">
            <Layers size={16} style={{ color: "var(--color-primary)" }} />
            Layer B Experimental Protocol (Review-2 Roadmap)
          </div>
        </div>

        <div className="grid-3">
          <div style={{ padding: "var(--space-3)", backgroundColor: "var(--bg-card-subtle)", borderRadius: "var(--radius-md)" }}>
            <strong style={{ fontSize: "var(--text-sm)" }}>1. Paired Legal Vignettes</strong>
            <p style={{ fontSize: "var(--text-xs)", color: "var(--text-secondary)", marginTop: "4px" }}>
              200 paired legal counterfactual scenarios across IPC/BNS offenses and SEBI regulations, isolating demographic and regional tokens.
            </p>
          </div>

          <div style={{ padding: "var(--space-3)", backgroundColor: "var(--bg-card-subtle)", borderRadius: "var(--radius-md)" }}>
            <strong style={{ fontSize: "var(--text-sm)" }}>2. Noise Floor Calibration</strong>
            <p style={{ fontSize: "var(--text-xs)", color: "var(--text-secondary)", marginTop: "4px" }}>
              Repeated stochastic sampling across temperature seeds on identical prompts to distinguish real statutory flips from stochastic variance.
            </p>
          </div>

          <div style={{ padding: "var(--space-3)", backgroundColor: "var(--bg-card-subtle)", borderRadius: "var(--radius-md)" }}>
            <strong style={{ fontSize: "var(--text-sm)" }}>3. QLoRA 3B-4B Fine-Tuning</strong>
            <p style={{ fontSize: "var(--text-xs)", color: "var(--text-secondary)", marginTop: "4px" }}>
              4-bit quantized Low-Rank Adaptation of an open 3B-4B parameter model running locally on the RTX 3050 6GB GPU using Supreme Court of India precedents.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
