import type { PaymentStatus, Urgency } from "@/types";

const STATUS_STYLES: Record<PaymentStatus, string> = {
  pending: "bg-warn/10 text-warn border-warn/30",
  paid: "bg-good/10 text-good border-good/30",
  overdue: "bg-bad/10 text-bad border-bad/30",
  failed: "bg-bad/20 text-bad border-bad/40",
};

const URGENCY_STYLES: Record<Urgency, string> = {
  low: "bg-ink-faint/10 text-ink-dim border-border",
  medium: "bg-brand/10 text-brand-soft border-brand/30",
  high: "bg-bad/10 text-bad border-bad/30",
};

export function StatusBadge({ status }: { status: PaymentStatus }) {
  return (
    <span className={`badge border ${STATUS_STYLES[status]}`}>
      <span className="w-1.5 h-1.5 rounded-full bg-current" />
      {status}
    </span>
  );
}

export function UrgencyBadge({ urgency }: { urgency: Urgency }) {
  return <span className={`badge border ${URGENCY_STYLES[urgency]}`}>{urgency} priority</span>;
}
