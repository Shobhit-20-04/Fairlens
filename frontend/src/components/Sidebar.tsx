import React from "react";
import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Search,
  FileSpreadsheet,
  BarChart2,
  FileText,
  FlaskConical,
  Settings,
  Scale,
} from "lucide-react";

export const Sidebar: React.FC = () => {
  const navItems = [
    { to: "/", label: "Overview", icon: <LayoutDashboard size={18} /> },
    { to: "/discovery", label: "Dataset Discovery", icon: <Search size={18} /> },
    { to: "/profiler", label: "Data Profiler", icon: <FileSpreadsheet size={18} /> },
    { to: "/audit", label: "Representation Audit", icon: <BarChart2 size={18} /> },
    { to: "/reports", label: "Reports & Export", icon: <FileText size={18} /> },
    { to: "/research", label: "Research Workspace", icon: <FlaskConical size={18} />, badge: "Layer B" },
    { to: "/settings", label: "System & Settings", icon: <Settings size={18} /> },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div
          style={{
            width: 36,
            height: 36,
            borderRadius: "var(--radius-md)",
            backgroundColor: "var(--color-primary)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#ffffff",
          }}
        >
          <Scale size={20} />
        </div>
        <div>
          <div className="sidebar-brand-title">FairLens</div>
          <div className="sidebar-brand-subtitle">Fairness & Representation Audit</div>
        </div>
      </div>

      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}
            end={item.to === "/"}
          >
            {item.icon}
            <span>{item.label}</span>
            {item.badge && (
              <span className="nav-badge badge badge-neutral" style={{ fontSize: "10px" }}>
                {item.badge}
              </span>
            )}
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div><strong>M.Tech Project (MASET697)</strong></div>
        <div>SCOPE, VIT Vellore</div>
        <div style={{ color: "var(--text-muted)", fontSize: "11px", marginTop: "2px" }}>
          FairLens v0.1.0 • Review-1 Ready
        </div>
      </div>
    </aside>
  );
};
