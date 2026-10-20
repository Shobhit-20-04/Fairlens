import React, { useState, useEffect } from "react";
import {
  FlaskConical,
  Calculator,
  ShieldAlert,
  BookOpen,
  DollarSign,
  Cpu,
  Layers,
  CheckCircle2,
  AlertTriangle,
  Info,
} from "lucide-react";
import { api } from "../api/client";
import { ResearchStatusResponse, CostEstimate } from "../api/types";

export const Research: React.FC = () => {
  const [researchData, setResearchData] = useState<ResearchStatusResponse | null>(null);
  const [loading, setLoading] = useState(true);

  // Cost calculator state
  const [runs, setRuns] = useState<number>(200);
  const [inputTokens, setInputTokens] = useState<number>(850);
  const [outputTokens, setOutputTokens] = useState<number>(300);
  const [useFreeTier, setUseFreeTier] = useState<boolean>(true);
  const [costEstimate, setCostEstimate] = useState<CostEstimate | null>(null);

  useEffect(() => {
    api
      .getResearchStatus()
      .then((res) => {
        setResearchData(res);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch research status:", err);
        setLoading(false);
      });

    calculateCost();
  }, []);

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

  useEffect(() => {
    calculateCost();
  }, [runs, inputTokens, outputTokens, useFreeTier]);

  return (
    <div className="page-content">
      {/* Header */}
      <div>
        <div style={{ display: "flex", alignItems: "center", gap: "var(--space-2)" }}>
          <span className="badge badge-warning">Review-2 Roadmap</span>
          <span className="badge badge-neutral">Future Experiment</span>
        </div>
        <h1 style={{ fontSize: "var(--text-xl)", fontWeight: 700, marginTop: "var(--space-1)" }}>
          Layer B Research Workspace: NVIDIA Nemotron 3 Ultra Case Study
        </h1>
        <p style={{ color: "var(--text-muted)", fontSize: "var(--text-sm)", marginTop: "2px" }}>
          Indian Statutory & Financial Fairness Case Study evaluating <code>nvidia/nemotron-3-ultra-550b-a55b</code>.
        </p>
      </div>

      {/* Strict Academic Disclaimer Alert */}
      <div className="alert-banner medium" style={{ flexDirection: "column", gap: "var(--space-1)" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "var(--space-2)", fontWeight: 600 }}>
          <ShieldAlert size={18} />
          <span>Academic Integrity & Research Transparency Statement</span>
        </div>
        <p style={{ fontSize: "var(--text-xs)", opacity: 0.95 }}>
          In strict compliance with academic standards and non-negotiable project rules, no experimental Nemotron flip rates, benchmark metrics, or fine-tuning results are fabricated. All technical specifications below reflect verified model card facts and planned methodology for Phase 5.
        </p>
      </div>

      {/* Target Model Verified Specs */}
      <div className="card">
        <div className="card-header">
          <div className="card-title">
            <Cpu size={18} style={{ color: "var(--color-primary)" }} />
            Target Model: NVIDIA Nemotron 3 Ultra Architecture & Pricing
          </div>
          <span className="badge badge-info">Verified OpenRouter Ledger</span>
        </div>

        <div className="grid-3">
          <div className="stat-card">
            <div className="stat-label">Model Architecture</div>
            <div className="stat-value" style={{ fontSize: "var(--text-base)", fontWeight: 600 }}>
              550B MoE (~55B Active)
            </div>
            <div className="stat-hint">Sparse Mixture-of-Experts</div>
          </div>

          <div className="stat-card">
            <div className="stat-label">Verified Free Tier</div>
            <div className="stat-value" style={{ fontSize: "var(--text-base)", color: "var(--badge-success-text)", fontWeight: 600 }}>
              $0.00 / 1M Tokens
            </div>
            <div className="stat-hint">Model ID: nvidia/nemotron-3-ultra-550b-a55b:free</div>
          </div>

          <div className="stat-card">
            <div className="stat-label">Safety Card Finding</div>
            <div className="stat-value" style={{ fontSize: "var(--text-base)", color: "var(--badge-warning-text)", fontWeight: 600 }}>
              Bias Mitigation: "None"
            </div>
            <div className="stat-hint">Relies on external classifiers, not regex</div>
          </div>
        </div>
      </div>

      {/* Pre-Execution Cost Estimator */}
      <div className="card">
        <div className="card-header">
          <div className="card-title">
            <Calculator size={18} style={{ color: "var(--color-primary)" }} />
            Pre-Execution Token Cost Estimator & Budget Enforcement
          </div>
          <div className="card-description">
            Validates projected experimental inference spend against the FairLens $5.00 budget ceiling before dispatching API calls.
          </div>
        </div>

        <div className="grid-2">
          {/* Controls */}
          <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-3)" }}>
            <div className="form-group">
              <label className="label">Evaluation Vignettes / Runs</label>
              <input
                type="number"
                className="input"
                value={runs}
                onChange={(e) => setRuns(Math.max(1, parseInt(e.target.value) || 1))}
              />
              <span style={{ fontSize: "var(--text-xs)", color: "var(--text-muted)" }}>
                Planned 200 paired counterfactual test cases.
              </span>
            </div>

            <div className="form-group">
              <label className="label">Average Input Tokens per Prompt</label>
              <input
                type="number"
                className="input"
                value={inputTokens}
                onChange={(e) => setInputTokens(Math.max(1, parseInt(e.target.value) || 1))}
              />
            </div>

            <div className="form-group">
              <label className="label">Average Output Tokens per Response</label>
              <input
                type="number"
                className="input"
                value={outputTokens}
                onChange={(e) => setOutputTokens(Math.max(1, parseInt(e.target.value) || 1))}
              />
            </div>

            <label style={{ display: "flex", alignItems: "center", gap: "var(--space-2)", fontSize: "var(--text-sm)", cursor: "pointer" }}>
              <input
                type="checkbox"
                checked={useFreeTier}
                onChange={(e) => setUseFreeTier(e.target.checked)}
              />
              <span>Route through OpenRouter Free Endpoint ($0.00 / 1M)</span>
            </label>
          </div>

          {/* Cost Result Box */}
          {costEstimate && (
            <div
              style={{
                backgroundColor: "var(--bg-card-subtle)",
                borderRadius: "var(--radius-md)",
                padding: "var(--space-5)",
                display: "flex",
                flexDirection: "column",
                gap: "var(--space-3)",
                border: "1px solid var(--border-subtle)",
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <strong>Projected Inference Cost</strong>
                <span className={`badge ${costEstimate.is_within_budget ? "badge-success" : "badge-error"}`}>
                  {costEstimate.is_within_budget ? "APPROVED (Within Budget)" : "BLOCKED (Exceeds Limit)"}
                </span>
              </div>

              <div style={{ fontSize: "var(--text-3xl)", fontWeight: 700, color: "var(--text-primary)" }}>
                ${costEstimate.total_cost_usd.toFixed(4)} USD
              </div>

              <div style={{ fontSize: "var(--text-xs)", color: "var(--text-secondary)", display: "flex", flexDirection: "column", gap: "var(--space-1)" }}>
                <div>Total Input Tokens: {costEstimate.input_tokens_total.toLocaleString()} (${costEstimate.input_cost_usd.toFixed(4)})</div>
                <div>Total Output Tokens: {costEstimate.output_tokens_total.toLocaleString()} (${costEstimate.output_cost_usd.toFixed(4)})</div>
                <div>Safety Margin: +{(costEstimate.safety_margin * 100).toFixed(0)}%</div>
                <div>Configured Budget Ceiling: ${costEstimate.budget_limit_usd.toFixed(2)} USD</div>
              </div>

              <div style={{ fontSize: "var(--text-xs)", color: "var(--text-muted)", marginTop: "auto" }}>
                {useFreeTier
                  ? "✓ Free tier selected: $0.00 inference cost. Synthetic data only."
                  : "Paid marketplace fallback estimate ($0.60/M in, $3.60/M out)."}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Planned Methodology Flowchart */}
      <div className="card">
        <div className="card-header">
          <div className="card-title">
            <Layers size={18} style={{ color: "var(--color-primary)" }} />
            Planned Statutory Evaluation Protocol (Layer B Pipeline)
          </div>
        </div>

        <div className="grid-3">
          <div style={{ padding: "var(--space-3)", backgroundColor: "var(--bg-card-subtle)", borderRadius: "var(--radius-md)" }}>
            <div style={{ fontWeight: 600, fontSize: "var(--text-sm)", marginBottom: "4px" }}>
              1. Paired Counterfactuals
            </div>
            <p style={{ fontSize: "var(--text-xs)", color: "var(--text-secondary)" }}>
              200 legal vignettes generated across IPC / Bharatiya Nyaya Sanhita (BNS) and SEBI regulations, isolating demographic tokens (e.g., Hindu vs Muslim vs Christian names; Maharashtra vs Uttar Pradesh states).
            </p>
          </div>

          <div style={{ padding: "var(--space-3)", backgroundColor: "var(--bg-card-subtle)", borderRadius: "var(--radius-md)" }}>
            <div style={{ fontWeight: 600, fontSize: "var(--text-sm)", marginBottom: "4px" }}>
              2. Noise Floor Calibration
            </div>
            <p style={{ fontSize: "var(--text-xs)", color: "var(--text-secondary)" }}>
              Isolating baseline stochastic generation variance by running identical prompts across multiple temperature seeds to ensure measured statutory flips are statistically meaningful.
            </p>
          </div>

          <div style={{ padding: "var(--space-3)", backgroundColor: "var(--bg-card-subtle)", borderRadius: "var(--radius-md)" }}>
            <div style={{ fontWeight: 600, fontSize: "var(--text-sm)", marginBottom: "4px" }}>
              3. QLoRA 3B-4B Correction
            </div>
            <p style={{ fontSize: "var(--text-xs)", color: "var(--text-secondary)" }}>
              Grounded corrective prompt fine-tuning on our RTX 3050 6GB GPU using 4-bit quantized Low-Rank Adaptation on curated Supreme Court of India precedents.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
