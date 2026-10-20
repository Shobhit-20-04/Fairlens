import React from "react";
import { Cpu, Activity, Sun, Moon, ShieldCheck, Database } from "lucide-react";
import { HealthResponse } from "../api/types";

interface TopBarProps {
  health: HealthResponse | null;
  loading: boolean;
  theme: "dark" | "light";
  onToggleTheme: () => void;
  activeDatasetName?: string | null;
}

export const TopBar: React.FC<TopBarProps> = ({
  health,
  loading,
  theme,
  onToggleTheme,
  activeDatasetName,
}) => {
  return (
    <header className="topbar">
      <div className="topbar-left">
        {/* Academic Project Review Pill */}
        <div className="badge badge-neutral" style={{ gap: "var(--space-2)" }}>
          <ShieldCheck size={14} style={{ color: "var(--color-primary)" }} />
          <span>M.Tech Review-1 | VIT Vellore</span>
        </div>

        {/* Active Dataset Context */}
        {activeDatasetName && (
          <div className="badge badge-info" style={{ gap: "var(--space-1)" }}>
            <Database size={13} />
            <span>Active Dataset: <strong>{activeDatasetName}</strong></span>
          </div>
        )}
      </div>

      <div className="topbar-right">
        {/* GPU Hardware Telemetry */}
        <div
          className={`badge ${health?.gpu?.available ? "badge-success" : "badge-neutral"}`}
          title={
            health?.gpu?.available
              ? `Hardware: ${health.gpu.device} with ${health.gpu.vram_gb} GB VRAM (CUDA ${health.gpu.cuda_version})`
              : "No dedicated CUDA GPU detected; running in CPU mode."
          }
        >
          <Cpu size={13} />
          <span>
            {health?.gpu?.available
              ? `GPU: ${health.gpu.device.includes("RTX") ? "RTX 3050" : health.gpu.device} (${health.gpu.vram_gb} GB)`
              : "CPU Engine"}
          </span>
        </div>

        {/* Backend REST API Status */}
        <div
          className={`badge ${
            loading
              ? "badge-warning"
              : health?.status === "healthy"
              ? "badge-success"
              : "badge-error"
          }`}
          title={
            health?.status === "healthy"
              ? `Backend Connected (v${health.version}) | Python ${health.python_version} | Offline Mode: ${health.offline_mode}`
              : "Backend disconnected. Run .\\run.ps1 server"
          }
        >
          <Activity size={13} />
          <span>
            {loading ? "Connecting..." : health?.status === "healthy" ? "API Live" : "API Offline"}
          </span>
        </div>

        {/* Theme Toggle Button */}
        <button
          className="btn btn-ghost btn-sm"
          onClick={onToggleTheme}
          title={`Switch to ${theme === "dark" ? "light" : "dark"} theme`}
          aria-label="Toggle theme"
        >
          {theme === "dark" ? <Sun size={16} /> : <Moon size={16} />}
        </button>
      </div>
    </header>
  );
};
