interface Props {
  label: string;
  value: string | number;
  hint?: string;
  tone?: "default" | "good" | "warn" | "bad" | "brand";
}

const TONES: Record<NonNullable<Props["tone"]>, string> = {
  default: "text-ink",
  good: "text-good",
  warn: "text-warn",
  bad: "text-bad",
  brand: "text-brand-soft",
};

export function StatBox({ label, value, hint, tone = "default" }: Props) {
  return (
    <div className="card p-5">
      <div className="text-xs uppercase tracking-wider text-ink-faint">{label}</div>
      <div className={`mt-2 text-2xl font-semibold ${TONES[tone]}`}>{value}</div>
      {hint && <div className="mt-1 text-xs text-ink-dim">{hint}</div>}
    </div>
  );
}
