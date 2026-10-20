import React from "react";
import { Cpu, Activity, Sun, Moon, Database } from "lucide-react";
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
        {activeDatasetName && (
          <div className="badge badge-neutral" style={{ gap: "var(--space-1)" }}>
            <Database size={12} />
            <span>Dataset: <strong>{activeDatasetName}</strong></span>
          </div>
        )}
      </div>

      <div className="topbar-right">
        {/* Hardware telemetry */}
        <div
          className={`badge ${health?.gpu?.available ? "badge-success" : "badge-neutral"}`}
          title={
            health?.gpu?.available
              ? `${health.gpu.device} (${health.gpu.vram_gb} GB VRAM, CUDA ${health.gpu.cuda_version})`
              : "CPU mode"
          }
        >
          <Cpu size={12} />
          <span>
            {health?.gpu?.available ? "RTX 3050 (6 GB)" : "CPU"}
          </span>
        </div>

        {/* API connection */}
        <div
          className={`badge ${
            loading
              ? "badge-warning"
              : health?.status === "healthy"
              ? "badge-neutral"
              : "badge-error"
          }`}
        >
          <Activity size={12} />
          <span>{loading ? "Connecting..." : health?.status === "healthy" ? "API Live" : "API Offline"}</span>
        </div>

        {/* Theme switcher */}
        <button
          className="btn btn-ghost btn-sm"
          onClick={onToggleTheme}
          title={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
          aria-label="Toggle color theme"
        >
          {theme === "dark" ? <Sun size={15} /> : <Moon size={15} />}
        </button>
      </div>
    </header>
  );
};
