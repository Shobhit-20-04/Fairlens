import React from "react";
import { NavLink } from "react-router-dom";
import {
  BarChart2,
  Search,
  FileSpreadsheet,
  FlaskConical,
  Scale,
} from "lucide-react";

export const Sidebar: React.FC = () => {
  const navItems = [
    { to: "/", label: "Representation Audit", icon: <BarChart2 size={18} /> },
    { to: "/profiler", label: "Data Profiler", icon: <FileSpreadsheet size={18} /> },
    { to: "/discovery", label: "Dataset Discovery", icon: <Search size={18} /> },
    { to: "/research", label: "Nemotron Research", icon: <FlaskConical size={18} /> },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div
          style={{
            width: 32,
            height: 32,
            borderRadius: "var(--radius-md)",
            backgroundColor: "var(--color-primary)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#ffffff",
          }}
        >
          <Scale size={18} />
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
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div style={{ fontWeight: 600, color: "var(--text-secondary)" }}>M.Tech Project (MASET697)</div>
        <div>SCOPE, VIT Vellore</div>
      </div>
    </aside>
  );
};
