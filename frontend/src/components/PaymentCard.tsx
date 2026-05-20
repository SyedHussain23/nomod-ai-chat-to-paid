import { useState } from "react";
import type { Payment } from "@/types";
import { api } from "@/services/api";
import { StatusBadge, UrgencyBadge } from "./StatusBadge";

interface Props {
  payment: Payment;
  onChange: () => void;
}

export function PaymentCard({ payment, onChange }: Props) {
  const [busy, setBusy] = useState<"paid" | "followup" | null>(null);
  const [followup, setFollowup] = useState<string | null>(null);

  const markPaid = async () => {
    setBusy("paid");
    try {
      await api.markPaid(payment.id);
      onChange();
    } finally {
      setBusy(null);
    }
  };

  const sendFollowup = async () => {
    setBusy("followup");
    try {
      const r = await api.followup(payment.id);
      setFollowup(r.message);
      onChange();
    } finally {
      setBusy(null);
    }
  };

  return (
    <div className="card p-5 flex flex-col gap-3">
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="text-base font-semibold">{payment.customer_name}</div>
          <div className="text-xs text-ink-dim">{payment.service_description}</div>
        </div>
        <div className="text-right">
          <div className="text-lg font-semibold">
            {payment.currency} {payment.amount.toFixed(2)}
          </div>
          <div className="text-[10px] uppercase tracking-wider text-ink-faint">
            {payment.payment_category}
          </div>
        </div>
      </div>

      <div className="flex flex-wrap gap-2">
        <StatusBadge status={payment.status} />
        <UrgencyBadge urgency={payment.urgency} />
        {payment.escalation_required && (
          <span className="badge border bg-bad/10 text-bad border-bad/30">escalation</span>
        )}
        {payment.followup_count > 0 && (
          <span className="badge border bg-panel border-border text-ink-dim">
            {payment.followup_count} follow-up{payment.followup_count > 1 ? "s" : ""}
          </span>
        )}
      </div>

      <a
        href={payment.payment_link}
        target="_blank"
        rel="noreferrer"
        className="text-xs text-brand-soft hover:underline truncate"
      >
        {payment.payment_link}
      </a>

      <div className="rounded-md bg-panel border border-border p-3 text-xs text-ink-dim whitespace-pre-wrap">
        {payment.whatsapp_message}
      </div>

      {followup && (
        <div className="rounded-md bg-brand/5 border border-brand/30 p-3 text-xs text-ink whitespace-pre-wrap">
          <div className="text-[10px] uppercase tracking-wider text-brand-soft mb-1">
            AI follow-up draft
          </div>
          {followup}
        </div>
      )}

      <div className="flex gap-2 pt-1">
        {payment.status !== "paid" && (
          <button className="btn-primary text-xs h-8 px-3" onClick={markPaid} disabled={busy !== null}>
            {busy === "paid" ? "..." : "Mark paid"}
          </button>
        )}
        {payment.status !== "paid" && (
          <button className="btn-ghost text-xs h-8 px-3" onClick={sendFollowup} disabled={busy !== null}>
            {busy === "followup" ? "..." : "AI follow-up"}
          </button>
        )}
      </div>
    </div>
  );
}
