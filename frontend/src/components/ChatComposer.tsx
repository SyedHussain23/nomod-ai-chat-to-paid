import { useState } from "react";
import { api } from "@/services/api";
import type { ChatResponse } from "@/types";

interface Props {
  onResult: (r: ChatResponse) => void;
}

const SUGGESTIONS = [
  "Charge Ahmed 500 AED for AC repair",
  "Bill Fatima 1250 for monthly cleaning service, urgent",
  "Invoice Khalid 3200 AED for laptop repair — he's been asking for a refund",
  "Send Layla 75 AED payment link for delivery",
];

export function ChatComposer({ onResult }: Props) {
  const [value, setValue] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submit = async (text: string) => {
    if (!text.trim()) return;
    setBusy(true);
    setError(null);
    try {
      const r = await api.chat(text);
      onResult(r);
      setValue("");
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="card p-5">
      <div className="flex items-center justify-between mb-3">
        <div>
          <div className="text-sm font-semibold">Merchant Assistant</div>
          <div className="text-xs text-ink-dim">
            Type a charge request in plain English — AI builds the payment.
          </div>
        </div>
        <span className="badge bg-brand/10 text-brand-soft border border-brand/30">AI-native</span>
      </div>

      <form
        onSubmit={(e) => {
          e.preventDefault();
          submit(value);
        }}
        className="flex gap-2"
      >
        <input
          className="input"
          placeholder="e.g. Charge Ahmed 500 AED for AC repair"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          disabled={busy}
        />
        <button className="btn-primary" disabled={busy || !value.trim()}>
          {busy ? "Thinking..." : "Generate"}
        </button>
      </form>

      {error && <div className="mt-3 text-xs text-bad">{error}</div>}

      <div className="mt-4 flex flex-wrap gap-2">
        {SUGGESTIONS.map((s) => (
          <button
            key={s}
            className="text-xs px-3 h-7 rounded-full border border-border text-ink-dim hover:text-ink hover:border-brand/50 transition"
            onClick={() => submit(s)}
            disabled={busy}
          >
            {s}
          </button>
        ))}
      </div>
    </div>
  );
}
