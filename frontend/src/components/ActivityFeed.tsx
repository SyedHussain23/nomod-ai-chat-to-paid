import type { ActivityEntry } from "@/types";

const EVENT_LABELS: Record<string, { label: string; tone: string }> = {
  "payment.created": { label: "Payment created", tone: "text-brand-soft" },
  "payment.paid": { label: "Payment received", tone: "text-good" },
  "payment.overdue": { label: "Marked overdue", tone: "text-warn" },
  "payment.failed": { label: "Payment failed", tone: "text-bad" },
  "followup.sent": { label: "Follow-up sent", tone: "text-warn" },
  "escalation.flagged": { label: "Escalation flagged", tone: "text-bad" },
};

function timeAgo(iso: string) {
  const diff = Date.now() - new Date(iso).getTime();
  const s = Math.floor(diff / 1000);
  if (s < 60) return `${s}s ago`;
  const m = Math.floor(s / 60);
  if (m < 60) return `${m}m ago`;
  const h = Math.floor(m / 60);
  if (h < 24) return `${h}h ago`;
  return `${Math.floor(h / 24)}d ago`;
}

export function ActivityFeed({ items }: { items: ActivityEntry[] }) {
  if (!items.length) {
    return (
      <div className="card p-5 text-sm text-ink-dim">
        No activity yet — try a charge request.
      </div>
    );
  }
  return (
    <div className="card p-5">
      <div className="text-sm font-semibold mb-3">Activity</div>
      <ul className="space-y-3 max-h-[480px] overflow-y-auto scrollbar-thin pr-2">
        {items.map((a) => {
          const meta = EVENT_LABELS[a.event] ?? { label: a.event, tone: "text-ink-dim" };
          return (
            <li key={a.id} className="flex items-start gap-3 text-xs">
              <span className={`mt-1.5 w-1.5 h-1.5 rounded-full bg-current ${meta.tone}`} />
              <div className="flex-1">
                <div className={`font-medium ${meta.tone}`}>{meta.label}</div>
                <div className="text-ink-faint">
                  {Object.entries(a.payload)
                    .map(([k, v]) => `${k}: ${v}`)
                    .join(" • ")}
                </div>
              </div>
              <div className="text-ink-faint whitespace-nowrap">{timeAgo(a.created_at)}</div>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
