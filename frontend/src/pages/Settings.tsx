import React, { useState, useEffect } from "react";
import {
  Settings as SettingsIcon,
  ShieldCheck,
  Key,
  DollarSign,
  Cpu,
  Database,
  CheckCircle2,
  XCircle,
  RefreshCw,
} from "lucide-react";
import { api } from "../api/client";
import { SettingsResponse, HealthResponse } from "../api/types";

interface SettingsPageProps {
  health: HealthResponse | null;
}

export const SettingsPage: React.FC<SettingsPageProps> = ({ health }) => {
  const [settings, setSettings] = useState<SettingsResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .getSettings()
      .then((res) => {
        setSettings(res);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to load settings:", err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="page-content">
      {/* Header */}
      <div>
        <h1 style={{ fontSize: "var(--text-xl)", fontWeight: 700 }}>System Configuration & Credentials</h1>
        <p style={{ color: "var(--text-muted)", fontSize: "var(--text-sm)", marginTop: "2px" }}>
          Central settings management with strict secret masking and budget limits.
        </p>
      </div>

      {loading ? (
        <div className="card" style={{ textAlign: "center", padding: "var(--space-8)" }}>
          <RefreshCw size={24} className="spin" style={{ margin: "0 auto var(--space-2)" }} />
          <div>Loading settings...</div>
        </div>
      ) : settings ? (
        <>
          {/* Security & Masked Credentials Card */}
          <div className="card">
            <div className="card-header">
              <div className="card-title">
                <Key size={18} style={{ color: "var(--color-primary)" }} />
                API Credentials & Provider Authentication
              </div>
              <span className="badge badge-success">Secret Masking Active</span>
            </div>

            <div className="table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Provider / Integration</th>
                    <th>Status</th>
                    <th>Configured Key / Token (Masked)</th>
                    <th>Operational Mode</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>
                      <strong>OpenRouter API</strong>
                    </td>
                    <td>
                      {settings.openrouter_api_key_configured ? (
                        <span className="badge badge-success">Configured</span>
                      ) : (
                        <span className="badge badge-neutral">Offline Mock Mode</span>
                      )}
                    </td>
                    <td>
                      <code>{settings.openrouter_api_key_masked}</code>
                    </td>
                    <td>Model: {settings.openrouter_model}</td>
                  </tr>

                  <tr>
                    <td>
                      <strong>Hugging Face Hub</strong>
                    </td>
                    <td>
                      {settings.providers.huggingface ? (
                        <span className="badge badge-success">Authenticated</span>
                      ) : (
                        <span className="badge badge-neutral">Public Anonymous API</span>
                      )}
                    </td>
                    <td><code>{settings.providers.huggingface ? "hf_***" : "<not-set>"}</code></td>
                    <td>Public search available without token</td>
                  </tr>

                  <tr>
                    <td>
                      <strong>Zenodo (CERN / OpenAIRE)</strong>
                    </td>
                    <td>
                      {settings.providers.zenodo ? (
                        <span className="badge badge-success">Authenticated</span>
                      ) : (
                        <span className="badge badge-neutral">Public Anonymous API</span>
                      )}
                    </td>
                    <td><code>{settings.providers.zenodo ? "zen_***" : "<not-set>"}</code></td>
                    <td>Public search enabled</td>
                  </tr>

                  <tr>
                    <td>
                      <strong>Data.gov & Open Gov</strong>
                    </td>
                    <td>
                      {settings.providers.data_gov ? (
                        <span className="badge badge-success">API Key Set</span>
                      ) : (
                        <span className="badge badge-neutral">DEMO_KEY Rate Limited</span>
                      )}
                    </td>
                    <td><code>{settings.providers.data_gov ? "dgov_***" : "DEMO_KEY"}</code></td>
                    <td>CKAN & Data.gov catalog endpoints</td>
                  </tr>

                  <tr>
                    <td>
                      <strong>Kaggle Datasets</strong>
                    </td>
                    <td>
                      {settings.providers.kaggle ? (
                        <span className="badge badge-success">Configured</span>
                      ) : (
                        <span className="badge badge-neutral">Requires API Token</span>
                      )}
                    </td>
                    <td><code>{settings.providers.kaggle ? "kg_***" : "<not-set>"}</code></td>
                    <td>Offline fixtures fallback supported</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          {/* Budget Limits & Cost Thresholds Card */}
          <div className="card">
            <div className="card-header">
              <div className="card-title">
                <DollarSign size={18} style={{ color: "var(--color-primary)" }} />
                Budget Ceilings & Spending Guards
              </div>
            </div>

            <div className="grid-4">
              <div className="stat-card">
                <div className="stat-label">Maximum Spend Ceiling</div>
                <div className="stat-value">${settings.budget.max_spend_usd.toFixed(2)} USD</div>
                <div className="stat-hint">Hard enforcement limit</div>
              </div>

              <div className="stat-card">
                <div className="stat-label">Spend Warning Threshold</div>
                <div className="stat-value">${settings.budget.warn_spend_usd.toFixed(2)} USD</div>
                <div className="stat-hint">Pre-execution warning alert</div>
              </div>

              <div className="stat-card">
                <div className="stat-label">Fallback Input Price</div>
                <div className="stat-value">${settings.budget.input_price_per_m.toFixed(2)} / M</div>
                <div className="stat-hint">Paid token marketplace rate</div>
              </div>

              <div className="stat-card">
                <div className="stat-label">Fallback Output Price</div>
                <div className="stat-value">${settings.budget.output_price_per_m.toFixed(2)} / M</div>
                <div className="stat-hint">Paid token marketplace rate</div>
              </div>
            </div>
          </div>

          {/* Hardware & Runtime Specs */}
          <div className="card">
            <div className="card-header">
              <div className="card-title">
                <Cpu size={18} style={{ color: "var(--color-primary)" }} />
                Runtime & Machine Hardware Specifications
              </div>
            </div>

            <div className="grid-3">
              <div>
                <div className="label">Operating System</div>
                <div style={{ fontSize: "var(--text-sm)" }}>Windows 11 (PowerShell Execution)</div>
              </div>
              <div>
                <div className="label">GPU Device</div>
                <div style={{ fontSize: "var(--text-sm)", fontWeight: 600 }}>
                  {health?.gpu?.available ? health.gpu.device : "CPU Compute Only"}
                </div>
              </div>
              <div>
                <div className="label">VRAM Telemetry</div>
                <div style={{ fontSize: "var(--text-sm)" }}>
                  {health?.gpu?.available ? `${health.gpu.vram_gb} GB VRAM (CUDA ${health.gpu.cuda_version})` : "N/A"}
                </div>
              </div>
              <div>
                <div className="label">Python Runtime</div>
                <div style={{ fontSize: "var(--text-sm)" }}>Python {health?.python_version || "3.11"}</div>
              </div>
              <div>
                <div className="label">Backend Web Framework</div>
                <div style={{ fontSize: "var(--text-sm)" }}>Flask 3.1.2 + Flask-CORS 6.0.1</div>
              </div>
              <div>
                <div className="label">Frontend Stack</div>
                <div style={{ fontSize: "var(--text-sm)" }}>React 19 + TypeScript + Vite + Vanilla CSS</div>
              </div>
            </div>
          </div>
        </>
      ) : null}
    </div>
  );
};
