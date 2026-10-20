import React, { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Sidebar } from "./components/Sidebar";
import { TopBar } from "./components/TopBar";
import { ErrorBoundary } from "./components/ErrorBoundary";
import { Audit } from "./pages/Audit";
import { Discovery } from "./pages/Discovery";
import { Profiler } from "./pages/Profiler";
import { Research } from "./pages/Research";
import { api } from "./api/client";
import { HealthResponse, AuditReport, NormalizedDatasetMetadata } from "./api/types";
import "./styles/globals.css";

export function App() {
  const [theme, setTheme] = useState<"dark" | "light">(() => {
    return (localStorage.getItem("fairlens_theme") as "dark" | "light") || "dark";
  });

  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [healthLoading, setHealthLoading] = useState(true);

  const [selectedFilePath, setSelectedFilePath] = useState<string | null>(
    "tests/fixtures/auditing/indian_legal_synthetic_audit.csv"
  );

  const [currentReport, setCurrentReport] = useState<AuditReport | null>(null);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("fairlens_theme", theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === "dark" ? "light" : "dark"));
  };

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const res = await api.getHealth();
        setHealth(res);
      } catch (err) {
        setHealth(null);
      } finally {
        setHealthLoading(false);
      }
    };

    fetchHealth();
    const interval = setInterval(fetchHealth, 15000);
    return () => clearInterval(interval);
  }, []);

  const handleSetReport = (report: AuditReport, _summaryText: string, _reportId: string) => {
    setCurrentReport(report);
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
          <ErrorBoundary>
            <Routes>
              {/* Default home route is the Audit workspace */}
              <Route
                path="/"
                element={
                  <Audit
                    selectedFilePath={selectedFilePath}
                    onSetReport={handleSetReport}
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
                path="/profiler"
                element={
                  <Profiler
                    selectedFilePath={selectedFilePath}
                    onSetSelectedFilePath={(path) => setSelectedFilePath(path)}
                  />
                }
              />
              <Route
                path="/discovery"
                element={
                  <Discovery
                    onSelectDatasetForProfile={(_ds: NormalizedDatasetMetadata) => {
                      // Handled by router
                    }}
                  />
                }
              />
              <Route path="/research" element={<Research />} />
            </Routes>
          </ErrorBoundary>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
