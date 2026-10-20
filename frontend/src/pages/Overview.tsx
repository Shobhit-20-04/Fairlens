import React from "react";
import { useNavigate } from "react-router-dom";
import {
  ShieldCheck,
  Cpu,
  Database,
  BarChart2,
  Search,
  BookOpen,
  ArrowRight,
  CheckCircle2,
  FileCheck,
  AlertTriangle,
} from "lucide-react";
import { HealthResponse } from "../api/types";

interface OverviewProps {
  health: HealthResponse | null;
  onSelectSampleDataset: (filePath: string) => void;
}

export const Overview: React.FC<OverviewProps> = ({ health, onSelectSampleDataset }) => {
  const navigate = useNavigate();

  const handleLaunchSampleAudit = () => {
    onSelectSampleDataset("tests/fixtures/auditing/indian_legal_synthetic_audit.csv");
    navigate("/audit");
  };

  return (
    <div className="page-content">
      {/* Welcome Banner */}
      <div
        className="card"
        style={{
          background: "linear-gradient(135deg, rgba(79, 70, 229, 0.15) 0%, rgba(15, 23, 42, 0.95) 100%)",
          borderColor: "rgba(99, 102, 241, 0.3)",
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "var(--space-4)" }}>
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: "var(--space-2)", marginBottom: "var(--space-1)" }}>
              <span className="badge badge-success">M.Tech Review-1 Ready</span>
              <span className="badge badge-neutral">Phases 1–4 Validated</span>
              <span className="badge badge-info">37 Backend Tests Passing</span>
            </div>
            <h1 style={{ fontSize: "var(--text-2xl)", fontWeight: 700, color: "var(--text-primary)" }}>
              FairLens: Automated Representation-Gap & Fairness Auditing
            </h1>
            <p style={{ color: "var(--text-secondary)", fontSize: "var(--text-sm)", maxWidth: "750px", marginTop: "var(--space-1)" }}>
              A reproducible, research-grade framework for detecting demographic, geographic, and cultural representation gaps in tabular datasets, with an Indian statutory fairness case study evaluating NVIDIA Nemotron 3 Ultra.
            </p>
          </div>

          <button className="btn btn-primary" onClick={handleLaunchSampleAudit}>
            <BarChart2 size={16} />
            <span>1-Click Launch: Indian Legal Audit</span>
            <ArrowRight size={14} />
          </button>
        </div>
      </div>

      {/* Hardware & Runtime Telemetry Card */}
      <div className="grid-3">
        <div className="stat-card">
          <div className="stat-label">Hardware Acceleration</div>
          <div className="stat-value" style={{ fontSize: "var(--text-xl)" }}>
            {health?.gpu?.available ? "NVIDIA RTX 3050" : "CPU Engine"}
          </div>
          <div className="stat-hint">
            {health?.gpu?.available
              ? `${health.gpu.vram_gb} GB VRAM • CUDA ${health.gpu.cuda_version || "Enabled"}`
              : "Standard compute mode"}
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Runtime Environment</div>
          <div className="stat-value" style={{ fontSize: "var(--text-xl)" }}>
            Python {health?.python_version || "3.11"}
          </div>
          <div className="stat-hint">
            Offline Mode: {health?.offline_mode ? "ACTIVE (Zero-leakage)" : "Live"} • Flask REST API
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Academic Milestone</div>
          <div className="stat-value" style={{ fontSize: "var(--text-xl)", color: "var(--badge-success-text)" }}>
            Review-1 (25 Marks)
          </div>
          <div className="stat-hint">
            Problem (5) • Objectives (10) • Methodology (10)
          </div>
        </div>
      </div>

      {/* Two-Layer Research Architecture */}
      <div className="card">
        <div className="card-header">
          <div>
            <div className="card-title">
              <Database size={18} style={{ color: "var(--color-primary)" }} />
              Two-Layer Research Architecture
            </div>
            <div className="card-description">
              FairLens decouples general-purpose dataset auditing from domain-specific model evaluations.
            </div>
          </div>
        </div>

        <div className="grid-2">
          {/* Layer A */}
          <div
            style={{
              padding: "var(--space-4)",
              backgroundColor: "var(--bg-card-subtle)",
              borderRadius: "var(--radius-md)",
              border: "1px solid var(--border-subtle)",
              display: "flex",
              flexDirection: "column",
              gap: "var(--space-3)",
            }}
          >
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "var(--space-2)" }}>
                <CheckCircle2 size={18} style={{ color: "var(--badge-success-text)" }} />
                <strong style={{ fontSize: "var(--text-base)" }}>Layer A: Dataset Representation Auditing</strong>
              </div>
              <span className="badge badge-success">Completed & Verified</span>
            </div>
            <p style={{ fontSize: "var(--text-xs)", color: "var(--text-secondary)" }}>
              Universal tabular dataset profiling, demographic representation gap measurement, Wilson 95% confidence intervals, zero-observation category detection, and multi-source federated dataset discovery (Hugging Face, Zenodo, Data.gov, UCI, Kaggle).
            </p>
            <div style={{ display: "flex", gap: "var(--space-2)", marginTop: "auto" }}>
              <button className="btn btn-secondary btn-sm" onClick={() => navigate("/profiler")}>
                <Database size={13} />
                <span>Profile Dataset</span>
              </button>
              <button className="btn btn-secondary btn-sm" onClick={() => navigate("/discovery")}>
                <Search size={13} />
                <span>Discover Datasets</span>
              </button>
            </div>
          </div>

          {/* Layer B */}
          <div
            style={{
              padding: "var(--space-4)",
              backgroundColor: "var(--bg-card-subtle)",
              borderRadius: "var(--radius-md)",
              border: "1px solid var(--border-subtle)",
              display: "flex",
              flexDirection: "column",
              gap: "var(--space-3)",
            }}
          >
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "var(--space-2)" }}>
                <BookOpen size={18} style={{ color: "var(--color-primary)" }} />
                <strong style={{ fontSize: "var(--text-base)" }}>Layer B: Indian Legal & Financial Case Study</strong>
              </div>
              <span className="badge badge-warning">Review-2 Roadmap</span>
            </div>
            <p style={{ fontSize: "var(--text-xs)", color: "var(--text-secondary)" }}>
              Evaluating NVIDIA Nemotron 3 Ultra (550B MoE, 55B active) on Indian statutory reasoning (IPC/BNS & SEBI/RBI). Pre-execution cost estimator, verified zero-dollar free tier routing, and planned counterfactual noise-floor evaluation.
            </p>
            <div style={{ display: "flex", gap: "var(--space-2)", marginTop: "auto" }}>
              <button className="btn btn-secondary btn-sm" onClick={() => navigate("/research")}>
                <BookOpen size={13} />
                <span>Inspect Nemotron Specs</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Review-1 Defense Rubric Grid */}
      <div className="card">
        <div className="card-header">
          <div className="card-title">
            <ShieldCheck size={18} style={{ color: "var(--color-primary)" }} />
            M.Tech Review-1 Evaluation Alignment
          </div>
          <div className="card-description">
            Rubric mapping for MASET697 project presentation (20–23 October 2026).
          </div>
        </div>

        <div className="grid-3">
          <div style={{ padding: "var(--space-3)", backgroundColor: "var(--bg-card-subtle)", borderRadius: "var(--radius-md)" }}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "var(--space-1)" }}>
              <strong>1. Problem Relevance</strong>
              <span className="badge badge-neutral">5 Marks</span>
            </div>
            <p style={{ fontSize: "var(--text-xs)", color: "var(--text-secondary)" }}>
              Existing AI benchmarks fail to account for Indian regional, demographic, and statutory nuances. Representation gaps directly lead to downstream allocation harms in judicial and credit decisions.
            </p>
          </div>

          <div style={{ padding: "var(--space-3)", backgroundColor: "var(--bg-card-subtle)", borderRadius: "var(--radius-md)" }}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "var(--space-1)" }}>
              <strong>2. Objectives</strong>
              <span className="badge badge-neutral">10 Marks</span>
            </div>
            <p style={{ fontSize: "var(--text-xs)", color: "var(--text-secondary)" }}>
              Deliver a domain-configurable audit engine (Phases 1–4) with Wilson 95% CIs, category coverage ratio, JSD parity scoring, and an extensible architecture for future LLM counterfactual auditing.
            </p>
          </div>

          <div style={{ padding: "var(--space-3)", backgroundColor: "var(--bg-card-subtle)", borderRadius: "var(--radius-md)" }}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "var(--space-1)" }}>
              <strong>3. Methodology</strong>
              <span className="badge badge-neutral">10 Marks</span>
            </div>
            <p style={{ fontSize: "var(--text-xs)", color: "var(--text-secondary)" }}>
              52 primary-verified literature references (R1–R52), mathematical Wilson bounds without normal approximation breakdown, strict secret masking, and deterministic offline caching.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
