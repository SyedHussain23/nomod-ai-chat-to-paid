import { useEffect, useState } from "react";
import { StatBox } from "@/components/StatBox";
import { ActivityFeed } from "@/components/ActivityFeed";
import { api } from "@/services/api";
import type { ActivityEntry, DashboardMetrics } from "@/types";

function Bar({ label, value, max }: { label: string; value: number; max: number }) {
  const pct = max ? Math.max(4, (value / max) * 100) : 0;
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-xs">
        <span className="text-ink-dim capitalize">{label}</span>
        <span className="text-ink">{value}</span>
      </div>
      <div className="h-1.5 bg-panel rounded-full overflow-hidden">
        <div className="h-full bg-gradient-to-r from-brand to-brand-soft" style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

export function DashboardPage() {
  const [m, setM] = useState<DashboardMetrics | null>(null);
  const [activity, setActivity] = useState<ActivityEntry[]>([]);

  useEffect(() => {
    Promise.all([api.metrics(), api.activity()])
      .then(([metrics, act]) => {
        setM(metrics);
        setActivity(act);
      })
      .catch(() => {});
  }, []);

  if (!m) return <div className="text-ink-dim">Loading…</div>;

  const urgencyMax = Math.max(1, ...Object.values(m.urgency_breakdown));
  const catMax = Math.max(1, ...Object.values(m.category_breakdown));

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-semibold">Operations Dashboard</h1>
        <p className="text-sm text-ink-dim mt-1">
          Live merchant KPIs · collection rate · escalation watch.
        </p>
      </header>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatBox label="Total requests" value={m.totals.requests} tone="brand" />
        <StatBox
          label="Collection rate"
          value={`${m.volume.collection_rate}%`}
          hint={`${m.volume.currency} ${m.volume.paid.toLocaleString()} settled`}
          tone="good"
        />
        <StatBox
          label="Pending volume"
          value={`${m.volume.currency} ${m.volume.pending.toLocaleString()}`}
          hint={`${m.totals.pending} open`}
          tone="warn"
        />
        <StatBox label="Escalations" value={m.totals.escalations} tone="bad" hint="needs human review" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="card p-5 space-y-4">
          <div className="text-sm font-semibold">Urgency breakdown</div>
          {Object.entries(m.urgency_breakdown).map(([k, v]) => (
            <Bar key={k} label={k} value={v} max={urgencyMax} />
          ))}
          {Object.keys(m.urgency_breakdown).length === 0 && (
            <div className="text-xs text-ink-dim">No data yet.</div>
          )}
        </div>
        <div className="card p-5 space-y-4">
          <div className="text-sm font-semibold">Category mix</div>
          {Object.entries(m.category_breakdown).map(([k, v]) => (
            <Bar key={k} label={k} value={v} max={catMax} />
          ))}
          {Object.keys(m.category_breakdown).length === 0 && (
            <div className="text-xs text-ink-dim">No data yet.</div>
          )}
        </div>
        <ActivityFeed items={activity.slice(0, 8)} />
      </div>
    </div>
  );
}
