import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  Search,
  ExternalLink,
  ArrowRight,
  X,
  Database,
  Layers,
} from "lucide-react";
import { api } from "../api/client";
import { NormalizedDatasetMetadata, DiscoveryResult } from "../api/types";

interface DiscoveryProps {
  onSelectDatasetForProfile: (dataset: NormalizedDatasetMetadata) => void;
}

export const Discovery: React.FC<DiscoveryProps> = ({ onSelectDatasetForProfile }) => {
  const navigate = useNavigate();

  const [query, setQuery] = useState("");
  const [domain, setDomain] = useState<string>("all");
  const [provider, setProvider] = useState<string>("all");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [results, setResults] = useState<DiscoveryResult | null>(null);
  const [inspectingDataset, setInspectingDataset] = useState<NormalizedDatasetMetadata | null>(null);

  useEffect(() => {
    // Perform initial discovery search on mount
    executeSearch("");
  }, []);

  const executeSearch = async (searchKw: string) => {
    setLoading(true);
    setError(null);

    try {
      const res = await api.searchDatasets({
        query: searchKw,
        domain: domain === "all" ? undefined : domain,
        providers: provider === "all" ? undefined : [provider],
        limit: 20,
        use_mock_offline: true,
      });
      setResults(res);
    } catch (err: any) {
      setError(err.message || "Failed to search datasets.");
    } finally {
      setLoading(false);
    }
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    executeSearch(query);
  };

  const handleAuditDataset = (ds: NormalizedDatasetMetadata) => {
    onSelectDatasetForProfile(ds);
    navigate("/audit");
  };

  return (
    <div className="page-content">
      {/* Clean Header */}
      <div>
        <h1 style={{ fontSize: "var(--text-xl)", fontWeight: 700 }}>Dataset Discovery</h1>
        <p style={{ color: "var(--text-muted)", fontSize: "var(--text-sm)", marginTop: "2px" }}>
          Curated repository search for Indian statutory, financial, and demographic benchmark datasets.
        </p>
      </div>

      {/* Search & Filter Controls */}
      <form onSubmit={handleSearchSubmit} className="card" style={{ padding: "var(--space-3) var(--space-4)" }}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 180px 180px auto", gap: "var(--space-3)", alignItems: "center" }}>
          <input
            type="text"
            className="input"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search verified datasets (e.g. 'InSaAF', 'SEBI', 'census', 'credit')..."
          />

          <select
            className="select"
            value={domain}
            onChange={(e) => {
              setDomain(e.target.value);
            }}
          >
            <option value="all">All Domains</option>
            <option value="legal">Legal & Statutory</option>
            <option value="finance">Finance & Banking</option>
            <option value="sociodemographic">Socio-Demographic</option>
          </select>

          <select
            className="select"
            value={provider}
            onChange={(e) => {
              setProvider(e.target.value);
            }}
          >
            <option value="all">All Repositories</option>
            <option value="huggingface">Hugging Face</option>
            <option value="zenodo">Zenodo (CERN)</option>
            <option value="data_gov">Data.gov / India</option>
            <option value="uci">UCI Repository</option>
          </select>

          <button type="submit" className="btn btn-primary" disabled={loading} style={{ height: 38 }}>
            <Search size={14} />
            <span>Search</span>
          </button>
        </div>
      </form>

      {/* Error Notice */}
      {error && (
        <div className="alert-banner high">
          <span>{error}</span>
        </div>
      )}

      {/* Results List */}
      {results && (
        <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-3)" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <span style={{ fontSize: "var(--text-xs)", color: "var(--text-muted)", fontWeight: 600, textTransform: "uppercase" }}>
              {results.returned_count} Verified Datasets Available
            </span>
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-3)" }}>
            {results.datasets.map((ds) => (
              <div
                key={`${ds.source_provider}-${ds.dataset_id}`}
                className="card"
                style={{ padding: "var(--space-4)", display: "flex", flexDirection: "column", gap: "var(--space-3)" }}
              >
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: "var(--space-3)" }}>
                  <div>
                    <div style={{ display: "flex", alignItems: "center", gap: "var(--space-2)" }}>
                      <h3 style={{ fontSize: "var(--text-base)", fontWeight: 600, color: "var(--text-primary)" }}>
                        {ds.name}
                      </h3>
                      <span className="badge badge-neutral" style={{ fontSize: "10px" }}>
                        {ds.source_provider}
                      </span>
                      <span className="badge badge-success" style={{ fontSize: "10px" }}>
                        Verified
                      </span>
                    </div>

                    <p style={{ fontSize: "var(--text-xs)", color: "var(--text-secondary)", marginTop: "4px", lineHeight: 1.5 }}>
                      {ds.description}
                    </p>
                  </div>

                  <div style={{ display: "flex", gap: "var(--space-2)", flexShrink: 0 }}>
                    <button className="btn btn-secondary btn-sm" onClick={() => setInspectingDataset(ds)}>
                      Inspect
                    </button>
                    {ds.canonical_url && (
                      <a
                        href={ds.canonical_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn btn-ghost btn-sm"
                        title="Open Source URL"
                      >
                        <ExternalLink size={13} />
                      </a>
                    )}
                  </div>
                </div>

                {/* Metadata Pills Row */}
                <div style={{ display: "flex", alignItems: "center", gap: "var(--space-2)", flexWrap: "wrap", fontSize: "var(--text-xs)", color: "var(--text-muted)" }}>
                  <span>Domain: <strong style={{ textTransform: "capitalize", color: "var(--text-primary)" }}>{ds.domain}</strong></span>
                  <span>•</span>
                  <span>Geography: <strong style={{ color: "var(--text-primary)" }}>{ds.geography.join(", ") || "India"}</strong></span>
                  <span>•</span>
                  <span>Records: <strong style={{ fontFamily: "var(--font-mono)", color: "var(--text-primary)" }}>{ds.row_count ? ds.row_count.toLocaleString() : "Documented"}</strong></span>
                  <span>•</span>
                  <span>Format: <strong style={{ fontFamily: "var(--font-mono)", color: "var(--text-primary)" }}>{ds.format.toUpperCase()}</strong></span>
                  <span>•</span>
                  <span>License: <strong style={{ color: "var(--text-primary)" }}>{ds.license}</strong></span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Slide-over Inspection Drawer */}
      {inspectingDataset && (
        <div className="drawer-backdrop" onClick={() => setInspectingDataset(null)}>
          <div className="drawer-panel" onClick={(e) => e.stopPropagation()}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
              <div>
                <span className="badge badge-neutral">{inspectingDataset.source_provider}</span>
                <h2 style={{ fontSize: "var(--text-base)", fontWeight: 700, marginTop: "4px" }}>
                  {inspectingDataset.name}
                </h2>
              </div>
              <button className="btn btn-ghost btn-sm" onClick={() => setInspectingDataset(null)}>
                <X size={16} />
              </button>
            </div>

            <div>
              <div className="label">Overview</div>
              <p style={{ fontSize: "var(--text-xs)", color: "var(--text-secondary)", marginTop: "4px", lineHeight: 1.5 }}>
                {inspectingDataset.description}
              </p>
            </div>

            <div className="grid-2">
              <div>
                <div className="label">Domain</div>
                <div style={{ fontSize: "var(--text-xs)", textTransform: "capitalize" }}>{inspectingDataset.domain}</div>
              </div>
              <div>
                <div className="label">Geography</div>
                <div style={{ fontSize: "var(--text-xs)" }}>{inspectingDataset.geography.join(", ") || "India"}</div>
              </div>
              <div>
                <div className="label">Format</div>
                <div style={{ fontSize: "var(--text-xs)", fontFamily: "var(--font-mono)" }}>{inspectingDataset.format}</div>
              </div>
              <div>
                <div className="label">Row Count</div>
                <div style={{ fontSize: "var(--text-xs)", fontFamily: "var(--font-mono)" }}>
                  {inspectingDataset.row_count ? inspectingDataset.row_count.toLocaleString() : "N/A"}
                </div>
              </div>
            </div>

            {inspectingDataset.documented_demographics && inspectingDataset.documented_demographics.length > 0 && (
              <div>
                <div className="label">Documented Demographic Features</div>
                <div style={{ display: "flex", gap: "var(--space-1)", flexWrap: "wrap", marginTop: "4px" }}>
                  {inspectingDataset.documented_demographics.map((d, i) => (
                    <span key={i} className="badge badge-neutral" style={{ fontSize: "11px" }}>
                      {d}
                    </span>
                  ))}
                </div>
              </div>
            )}

            <div style={{ marginTop: "auto", display: "flex", gap: "var(--space-2)" }}>
              {inspectingDataset.canonical_url && (
                <a
                  href={inspectingDataset.canonical_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-secondary"
                  style={{ flex: 1 }}
                >
                  <ExternalLink size={13} />
                  <span>Open Repository</span>
                </a>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
