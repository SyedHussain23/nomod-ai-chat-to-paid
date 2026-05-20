import { NavLink } from "react-router-dom";
import type { ReactNode } from "react";

const NAV = [
  { to: "/", label: "Assistant", icon: "◆" },
  { to: "/payments", label: "Payments", icon: "▤" },
  { to: "/dashboard", label: "Analytics", icon: "▮" },
];

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen flex">
      <aside className="w-60 shrink-0 border-r border-border bg-panel/60 backdrop-blur p-5 flex flex-col">
        <div className="flex items-center gap-2 mb-8">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-brand to-brand-glow flex items-center justify-center text-white font-bold">
            N
          </div>
          <div>
            <div className="text-sm font-semibold leading-tight">Nomod AI</div>
            <div className="text-[10px] text-ink-faint uppercase tracking-wider">Merchant Ops</div>
          </div>
        </div>
        <nav className="flex flex-col gap-1">
          {NAV.map((n) => (
            <NavLink
              key={n.to}
              to={n.to}
              end
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 h-9 rounded-md text-sm transition ${
                  isActive
                    ? "bg-brand/15 text-ink border border-brand/30"
                    : "text-ink-dim hover:text-ink hover:bg-card border border-transparent"
                }`
              }
            >
              <span className="text-ink-faint">{n.icon}</span>
              {n.label}
            </NavLink>
          ))}
        </nav>
        <div className="mt-auto pt-6 border-t border-border">
          <div className="text-[10px] uppercase tracking-wider text-ink-faint mb-1">Merchant</div>
          <div className="text-sm">Falcon AC Services</div>
          <div className="text-xs text-ink-dim">Dubai, AE</div>
        </div>
      </aside>
      <main className="flex-1 min-w-0">
        <div className="max-w-6xl mx-auto p-6 md:p-8">{children}</div>
      </main>
    </div>
  );
}
