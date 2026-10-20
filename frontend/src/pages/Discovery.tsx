import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  Search,
  Globe,
  ExternalLink,
  ShieldCheck,
  CheckCircle2,
  AlertCircle,
  FileSpreadsheet,
  X,
  Filter,
  Layers,
} from "lucide-react";
import { api } from "../api/client";
import {
  NormalizedDatasetMetadata,
  DiscoveryResult,
  ProviderInfo,
} from "../api/types";

interface DiscoveryProps {
  onSelectDatasetForProfile: (dataset: NormalizedDatasetMetadata) => void;
}

export const Discovery: React.FC<DiscoveryProps> = ({ onSelectDatasetForProfile }) => {
  const navigate = useNavigate();

  const [query, setQuery] = useState("legal");
  const [domain, setDomain] = useState<string>("all");
  const [geography, setGeography] = useState<string>("all");
  const [useOfflineMock, setUseOfflineMock] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [providers, setProviders] = useState<ProviderInfo[]>([]);
  const [selectedProviders, setSelectedProviders] = useState<string[]>([]);
  const [results, setResults] = useState<DiscoveryResult | null>(null);
  const [inspectingDataset, setInspectingDataset] = useState<NormalizedDatasetMetadata | null>(null);

  useEffect(() => {
    // Load providers status on mount
    api
      .getProviders()
      .then((res) => {
        setProviders(res.providers);
        setSelectedProviders(res.providers.map((p) => p.id));
      })
      .catch((err) => {
        console.error("Failed to load providers:", err);
      });

    // Run initial search with pre-loaded mock fixtures
    handleSearch();
  }, []);

  const handleSearch = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const res = await api.searchDatasets({
        query,
        domain: domain === "all" ? undefined : domain,
        geographic_coverage: geography === "all" ? undefined : geography,
        providers: selectedProviders.length > 0 ? selectedProviders : undefined,
        limit: 20,
        use_mock_offline: useOfflineMock,
      });
      setResults(res);
    } catch (err: any) {
      setError(err.message || "Search failed");
    } finally {
      setLoading(false);
    }
  };

  const toggleProvider = (id: string) => {
    if (selectedProviders.includes(id)) {
      setSelectedProviders(selectedProviders.filter((p) => p !== id));
    } else {
      setSelectedProviders([...selectedProviders, id]);
    }
  };

  return (
    <div className="page-content">
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "var(--space-3)" }}>
        <div>
          <h1 style={{ fontSize: "var(--text-xl)", fontWeight: 700 }}>Federated Dataset Discovery Engine</h1>
          <p style={{ color: "var(--text-muted)", fontSize: "var(--text-sm)", marginTop: "2px" }}>
            Phase 3 Discovery across Hugging Face, Zenodo, Data.gov, UCI, and Kaggle with audit suitability assessment.
          </p>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: "var(--space-2)" }}>
          <label style={{ display: "flex", alignItems: "center", gap: "var(--space-2)", fontSize: "var(--text-xs)", color: "var(--text-secondary)", cursor: "pointer" }}>
            <input
              type="checkbox"
              checked={useOfflineMock}
              onChange={(e) => setUseOfflineMock(e.target.checked)}
            />
            <span>Use Offline Fixtures (Deterministic Demo)</span>
          </label>
        </div>
      </div>

      {/* Provider Status Pill Strip */}
      <div className="card" style={{ padding: "var(--space-3)" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "var(--space-3)", flexWrap: "wrap" }}>
          <span style={{ fontSize: "var(--text-xs)", fontWeight: 600, color: "var(--text-muted)", textTransform: "uppercase" }}>
            Active Adapters:
          </span>
          {providers.map((p) => {
            const isSelected = selectedProviders.includes(p.id);
            return (
              <button
                key={p.id}
                onClick={() => toggleProvider(p.id)}
                className={`badge ${isSelected ? "badge-info" : "badge-neutral"}`}
                style={{ cursor: "pointer", border: isSelected ? "1px solid var(--color-primary)" : "1px solid transparent" }}
                title={`${p.description} (${p.rate_limit_authenticated})`}
              >
                <span>{p.name}</span>
                {p.authenticated && <CheckCircle2 size={11} style={{ color: "var(--badge-success-text)" }} />}
              </button>
            );
          })}
        </div>
      </div>

      {/* Search & Filter Bar */}
      <form onSubmit={handleSearch} className="card" style={{ padding: "var(--space-4)" }}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 180px 180px auto", gap: "var(--space-3)", alignItems: "center" }}>
          <div className="form-group" style={{ position: "relative" }}>
            <input
              type="text"
              className="input"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search datasets by keyword (e.g. 'legal', 'finance', 'court', 'census')..."
            />
          </div>

          <div className="form-group">
            <select className="select" value={domain} onChange={(e) => setDomain(e.target.value)}>
              <option value="all">All Domains</option>
              <option value="legal">Legal & Statutory</option>
              <option value="finance">Finance & Credit</option>
              <option value="healthcare">Healthcare</option>
              <option value="general">General Tabular</option>
            </select>
          </div>

          <div className="form-group">
            <select className="select" value={geography} onChange={(e) => setGeography(e.target.value)}>
              <option value="all">All Geographies</option>
              <option value="india">India Only</option>
              <option value="global">Global</option>
              <option value="us">United States</option>
            </select>
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading} style={{ height: 38 }}>
            <Search size={15} />
            <span>{loading ? "Searching..." : "Search"}</span>
          </button>
        </div>
      </form>

      {/* Error Message */}
      {error && (
        <div className="alert-banner high">
          <AlertCircle size={18} />
          <span>{error}</span>
        </div>
      )}

      {/* Results Section */}
      {results && (
        <div className="card">
          <div className="card-header">
            <div>
              <div className="card-title">
                <Layers size={18} style={{ color: "var(--color-primary)" }} />
                Discovered Candidate Datasets ({results.returned_count} of {results.total_found})
              </div>
              <div className="card-description">
                Execution time: {results.execution_time_seconds}s across {Object.keys(results.provider_counts).length} repositories.
              </div>
            </div>

            {/* Provider Breakdown Badges */}
            <div style={{ display: "flex", gap: "var(--space-2)", flexWrap: "wrap" }}>
              {Object.entries(results.provider_counts).map(([prov, count]) => (
                <span key={prov} className="badge badge-neutral" style={{ fontSize: "11px" }}>
                  {prov}: {count}
                </span>
              ))}
            </div>
          </div>

          {results.datasets.length === 0 ? (
            <div style={{ textAlign: "center", padding: "var(--space-8)", color: "var(--text-muted)" }}>
              No datasets matching query and filter criteria. Try expanding domain or providers.
            </div>
          ) : (
            <div className="table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Dataset Name & Source</th>
                    <th>Domain / Geography</th>
                    <th>Format & Size</th>
                    <th>Audit Suitability</th>
                    <th>Completeness</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {results.datasets.map((ds) => (
                    <tr key={`${ds.source_provider}-${ds.dataset_id}`}>
                      <td>
                        <div style={{ fontWeight: 600, color: "var(--text-primary)" }}>
                          {ds.name}
                        </div>
                        <div style={{ fontSize: "var(--text-xs)", color: "var(--text-muted)", display: "flex", alignItems: "center", gap: "6px" }}>
                          <span className="badge badge-neutral" style={{ fontSize: "10px", padding: "1px 5px" }}>
                            {ds.source_provider}
                          </span>
                          <span>{ds.license || "Open License"}</span>
                        </div>
                      </td>
                      <td>
                        <div style={{ textTransform: "capitalize", fontWeight: 500 }}>{ds.domain}</div>
                        <div style={{ fontSize: "var(--text-xs)", color: "var(--text-muted)" }}>
                          {ds.geography.join(", ") || "Global"}
                        </div>
                      </td>
                      <td>
                        <div style={{ fontFamily: "var(--font-mono)", fontSize: "var(--text-xs)" }}>
                          {ds.format.toUpperCase()}
                        </div>
                        <div style={{ fontSize: "var(--text-xs)", color: "var(--text-muted)" }}>
                          {ds.row_count ? `${ds.row_count.toLocaleString()} rows` : "Size unknown"}
                        </div>
                      </td>
                      <td>
                        <span
                          className={`badge ${
                            ds.audit_suitability === "high"
                              ? "badge-success"
                              : ds.audit_suitability === "medium"
                              ? "badge-warning"
                              : "badge-neutral"
                          }`}
                        >
                          {ds.audit_suitability.toUpperCase()}
                        </span>
                      </td>
                      <td>
                        <div style={{ display: "flex", alignItems: "center", gap: "var(--space-2)" }}>
                          <span style={{ fontSize: "var(--text-xs)", fontFamily: "var(--font-mono)", fontWeight: 600 }}>
                            {(ds.metadata_completeness_score * 100).toFixed(0)}%
                          </span>
                        </div>
                      </td>
                      <td>
                        <div style={{ display: "flex", gap: "var(--space-2)" }}>
                          <button
                            className="btn btn-secondary btn-sm"
                            onClick={() => setInspectingDataset(ds)}
                            title="Inspect 20+ Normalized Metadata Attributes"
                          >
                            Inspect
                          </button>
                          {ds.canonical_url && (
                            <a
                              href={ds.canonical_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="btn btn-ghost btn-sm"
                              title="Open original repository URL"
                            >
                              <ExternalLink size={13} />
                            </a>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* Slide-over Inspection Drawer */}
      {inspectingDataset && (
        <div className="drawer-backdrop" onClick={() => setInspectingDataset(null)}>
          <div className="drawer-panel" onClick={(e) => e.stopPropagation()}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div>
                <span className="badge badge-info">{inspectingDataset.source_provider}</span>
                <h2 style={{ fontSize: "var(--text-lg)", fontWeight: 700, marginTop: "var(--space-1)" }}>
                  {inspectingDataset.name}
                </h2>
              </div>
              <button className="btn btn-ghost btn-sm" onClick={() => setInspectingDataset(null)}>
                <X size={18} />
              </button>
            </div>

            {/* Suitability Box */}
            <div
              style={{
                padding: "var(--space-3)",
                backgroundColor: "var(--bg-card-subtle)",
                borderRadius: "var(--radius-md)",
                border: "1px solid var(--border-subtle)",
              }}
            >
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "var(--space-2)" }}>
                <strong>Phase 4 Auditing Suitability</strong>
                <span
                  className={`badge ${
                    inspectingDataset.audit_suitability === "high"
                      ? "badge-success"
                      : inspectingDataset.audit_suitability === "medium"
                      ? "badge-warning"
                      : "badge-neutral"
                  }`}
                >
                  {inspectingDataset.audit_suitability.toUpperCase()}
                </span>
              </div>
              <ul style={{ fontSize: "var(--text-xs)", color: "var(--text-secondary)", paddingLeft: "var(--space-4)" }}>
                {inspectingDataset.audit_suitability_reasons.map((r, idx) => (
                  <li key={idx}>{r}</li>
                ))}
              </ul>
            </div>

            {/* Description */}
            <div>
              <div className="label">Dataset Description</div>
              <p style={{ fontSize: "var(--text-sm)", color: "var(--text-secondary)", marginTop: "var(--space-1)" }}>
                {inspectingDataset.description || "No description provided by source."}
              </p>
            </div>

            {/* Metadata Attributes Grid */}
            <div className="grid-2">
              <div>
                <div className="label">Format</div>
                <div style={{ fontSize: "var(--text-sm)", fontFamily: "var(--font-mono)" }}>
                  {inspectingDataset.format}
                </div>
              </div>
              <div>
                <div className="label">License</div>
                <div style={{ fontSize: "var(--text-sm)" }}>
                  {inspectingDataset.license} {inspectingDataset.license_verified ? "✓ (Verified)" : "(Self-reported)"}
                </div>
              </div>
              <div>
                <div className="label">Domain</div>
                <div style={{ fontSize: "var(--text-sm)", textTransform: "capitalize" }}>
                  {inspectingDataset.domain}
                </div>
              </div>
              <div>
                <div className="label">Geographic Scope</div>
                <div style={{ fontSize: "var(--text-sm)" }}>
                  {inspectingDataset.geography.join(", ") || "Global"}
                </div>
              </div>
              <div>
                <div className="label">Completeness Score</div>
                <div style={{ fontSize: "var(--text-sm)", fontWeight: 600 }}>
                  {(inspectingDataset.metadata_completeness_score * 100).toFixed(0)}%
                </div>
              </div>
              <div>
                <div className="label">Row Count</div>
                <div style={{ fontSize: "var(--text-sm)", fontFamily: "var(--font-mono)" }}>
                  {inspectingDataset.row_count ? inspectingDataset.row_count.toLocaleString() : "Unknown"}
                </div>
              </div>
            </div>

            {/* Demographics */}
            {inspectingDataset.documented_demographics.length > 0 && (
              <div>
                <div className="label">Self-Reported Demographic Dimensions</div>
                <div style={{ display: "flex", gap: "var(--space-1)", flexWrap: "wrap", marginTop: "var(--space-1)" }}>
                  {inspectingDataset.documented_demographics.map((d, i) => (
                    <span key={i} className="badge badge-neutral">
                      {d}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Canonical Link */}
            <div style={{ marginTop: "auto", display: "flex", gap: "var(--space-3)" }}>
              <a
                href={inspectingDataset.canonical_url}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-primary"
                style={{ flex: 1 }}
              >
                <ExternalLink size={14} />
                <span>Open Source Repository</span>
              </a>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
