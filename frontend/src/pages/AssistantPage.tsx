import { useEffect, useState } from "react";
import { ChatComposer } from "@/components/ChatComposer";
import { PaymentCard } from "@/components/PaymentCard";
import { ActivityFeed } from "@/components/ActivityFeed";
import { api } from "@/services/api";
import type { ActivityEntry, ChatResponse, Payment } from "@/types";

export function AssistantPage() {
  const [latest, setLatest] = useState<ChatResponse | null>(null);
  const [recent, setRecent] = useState<Payment[]>([]);
  const [activity, setActivity] = useState<ActivityEntry[]>([]);

  const refresh = async () => {
    const [p, a] = await Promise.all([api.payments(), api.activity()]);
    setRecent(p.slice(0, 6));
    setActivity(a);
  };

  useEffect(() => {
    refresh().catch(() => {});
  }, []);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div className="lg:col-span-2 space-y-6">
        <header>
          <h1 className="text-2xl font-semibold">Chat to paid in seconds.</h1>
          <p className="text-sm text-ink-dim mt-1">
            Describe the charge in plain English — Nomod AI extracts the intent, builds a payment link,
            writes the WhatsApp message, and tracks the rest.
          </p>
        </header>

        <ChatComposer
          onResult={(r) => {
            setLatest(r);
            refresh();
          }}
        />

        {latest && (
          <section>
            <div className="text-xs uppercase tracking-wider text-ink-faint mb-2">
              AI extraction · {latest.ai_summary}
            </div>
            <PaymentCard payment={latest.payment} onChange={refresh} />
          </section>
        )}

        {recent.length > 0 && (
          <section>
            <div className="text-xs uppercase tracking-wider text-ink-faint mb-2">Recent requests</div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {recent.map((p) => (
                <PaymentCard key={p.id} payment={p} onChange={refresh} />
              ))}
            </div>
          </section>
        )}
      </div>

      <aside>
        <ActivityFeed items={activity} />
      </aside>
    </div>
  );
}
