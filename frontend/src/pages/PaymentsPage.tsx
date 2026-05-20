import { useEffect, useState } from "react";
import { PaymentCard } from "@/components/PaymentCard";
import { api } from "@/services/api";
import type { Payment, PaymentStatus } from "@/types";

const FILTERS: { label: string; value: PaymentStatus | "all" }[] = [
  { label: "All", value: "all" },
  { label: "Pending", value: "pending" },
  { label: "Paid", value: "paid" },
  { label: "Overdue", value: "overdue" },
  { label: "Failed", value: "failed" },
];

export function PaymentsPage() {
  const [items, setItems] = useState<Payment[]>([]);
  const [filter, setFilter] = useState<PaymentStatus | "all">("all");

  const refresh = async () => setItems(await api.payments());
  useEffect(() => {
    refresh().catch(() => {});
  }, []);

  const filtered = filter === "all" ? items : items.filter((p) => p.status === filter);

  return (
    <div className="space-y-6">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Payments</h1>
          <p className="text-sm text-ink-dim mt-1">Every request flowing through Nomod AI.</p>
        </div>
        <div className="flex gap-2">
          {FILTERS.map((f) => (
            <button
              key={f.value}
              onClick={() => setFilter(f.value)}
              className={`text-xs px-3 h-8 rounded-md border transition ${
                filter === f.value
                  ? "border-brand/40 bg-brand/15 text-ink"
                  : "border-border text-ink-dim hover:text-ink"
              }`}
            >
              {f.label}
            </button>
          ))}
        </div>
      </header>

      {filtered.length === 0 ? (
        <div className="card p-8 text-center text-ink-dim">No payments yet.</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filtered.map((p) => (
            <PaymentCard key={p.id} payment={p} onChange={refresh} />
          ))}
        </div>
      )}
    </div>
  );
}
