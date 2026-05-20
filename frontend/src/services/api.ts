import type {
  ActivityEntry,
  ChatResponse,
  DashboardMetrics,
  Followup,
  Payment,
  PaymentStatus,
} from "@/types";

const BASE = import.meta.env.VITE_API_BASE ?? "/api";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`${res.status} ${res.statusText} — ${text}`);
  }
  return (await res.json()) as T;
}

export const api = {
  chat: (message: string, merchant_id = "mch_demo") =>
    request<ChatResponse>("/ai/chat", {
      method: "POST",
      body: JSON.stringify({ message, merchant_id }),
    }),
  payments: () => request<Payment[]>("/payments"),
  payment: (id: string) => request<Payment>(`/payments/${id}`),
  setStatus: (id: string, status: PaymentStatus) =>
    request<Payment>(`/payments/${id}/status`, {
      method: "PATCH",
      body: JSON.stringify({ status }),
    }),
  markPaid: (id: string) =>
    request<Payment>(`/payments/${id}/webhook/paid`, { method: "POST" }),
  followup: (id: string) =>
    request<Followup>(`/payments/${id}/followup`, { method: "POST" }),
  metrics: () => request<DashboardMetrics>("/dashboard/metrics"),
  activity: () => request<ActivityEntry[]>("/dashboard/activity"),
};
