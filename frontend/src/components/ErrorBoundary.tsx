import React, { Component, ErrorInfo, ReactNode } from "react";
import { AlertCircle, RefreshCw } from "lucide-react";

interface Props {
  children: ReactNode;
  fallbackTitle?: string;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("FairLens UI Uncaught Error:", error, errorInfo);
  }

  private handleReset = () => {
    this.setState({ hasError: false, error: null });
    window.location.reload();
  };

  public render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: "var(--space-8)", maxWidth: "600px", margin: "40px auto" }}>
          <div className="card" style={{ textAlign: "center", padding: "var(--space-6)" }}>
            <AlertCircle size={36} style={{ color: "var(--badge-error-text)", margin: "0 auto var(--space-3)" }} />
            <h2 style={{ fontSize: "var(--text-lg)", fontWeight: 600 }}>Unable to render view</h2>
            <p style={{ color: "var(--text-secondary)", fontSize: "var(--text-sm)", margin: "var(--space-2) 0 var(--space-4)" }}>
              {this.state.error?.message || "An unexpected rendering error occurred."}
            </p>
            <button className="btn btn-primary" onClick={this.handleReset} style={{ margin: "0 auto" }}>
              <RefreshCw size={14} />
              <span>Reload Interface</span>
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
