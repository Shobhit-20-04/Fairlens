import React, { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Sidebar } from "./components/Sidebar";
import { TopBar } from "./components/TopBar";
import { Overview } from "./pages/Overview";
import { Discovery } from "./pages/Discovery";
import { Profiler } from "./pages/Profiler";
import { Audit } from "./pages/Audit";
import { Reports } from "./pages/Reports";
import { Research } from "./pages/Research";
import { SettingsPage } from "./pages/Settings";
import { api } from "./api/client";
import { HealthResponse, AuditReport, NormalizedDatasetMetadata } from "./api/types";
import "./styles/globals.css";

export function App() {
  // Theme state: dark mode default, persisted in localStorage
  const [theme, setTheme] = useState<"dark" | "light">(() => {
    return (localStorage.getItem("fairlens_theme") as "dark" | "light") || "dark";
  });

  // Health check & hardware telemetry state
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [healthLoading, setHealthLoading] = useState(true);

  // Active dataset context across pages
  const [selectedFilePath, setSelectedFilePath] = useState<string | null>(
    "tests/fixtures/auditing/indian_legal_synthetic_audit.csv"
  );

  // Latest audit report state across pages
  const [currentReport, setCurrentReport] = useState<AuditReport | null>(null);
  const [currentSummaryText, setCurrentSummaryText] = useState<string | null>(null);
  const [currentReportId, setCurrentReportId] = useState<string | null>(null);

  // Theme application
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("fairlens_theme", theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === "dark" ? "light" : "dark"));
  };

  // Health poll on mount and periodically
  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const res = await api.getHealth();
        setHealth(res);
      } catch (err) {
        console.warn("Backend API offline or unreachable:", err);
        setHealth(null);
      } finally {
        setHealthLoading(false);
      }
    };

    fetchHealth();
    const interval = setInterval(fetchHealth, 15000);
    return () => clearInterval(interval);
  }, []);

  const handleSetReport = (report: AuditReport, summaryText: string, reportId: string) => {
    setCurrentReport(report);
    setCurrentSummaryText(summaryText);
    setCurrentReportId(reportId);
  };

  const activeDatasetName = selectedFilePath
    ? selectedFilePath.split("/").pop() || selectedFilePath.split("\\").pop()
    : null;

  return (
    <BrowserRouter>
      <div className="app-shell">
        <Sidebar />
        <div className="main-wrapper">
          <TopBar
            health={health}
            loading={healthLoading}
            theme={theme}
            onToggleTheme={toggleTheme}
            activeDatasetName={activeDatasetName}
          />
          <Routes>
            <Route
              path="/"
              element={
                <Overview
                  health={health}
                  onSelectSampleDataset={(path) => setSelectedFilePath(path)}
                />
              }
            />
            <Route
              path="/discovery"
              element={
                <Discovery
                  onSelectDatasetForProfile={(ds: NormalizedDatasetMetadata) => {
                    // Navigate to profiler with dataset context
                  }}
                />
              }
            />
            <Route
              path="/profiler"
              element={
                <Profiler
                  selectedFilePath={selectedFilePath}
                  onSetSelectedFilePath={(path) => setSelectedFilePath(path)}
                />
              }
            />
            <Route
              path="/audit"
              element={
                <Audit
                  selectedFilePath={selectedFilePath}
                  onSetReport={handleSetReport}
                />
              }
            />
            <Route
              path="/reports"
              element={
                <Reports
                  currentReport={currentReport}
                  currentSummaryText={currentSummaryText}
                  currentReportId={currentReportId}
                />
              }
            />
            <Route path="/research" element={<Research />} />
            <Route path="/settings" element={<SettingsPage health={health} />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
