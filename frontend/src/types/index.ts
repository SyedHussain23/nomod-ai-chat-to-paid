export type Urgency = "low" | "medium" | "high";
export type PaymentStatus = "pending" | "paid" | "overdue" | "failed";
export type Sentiment = "neutral" | "satisfied" | "frustrated" | "at_risk";

export interface Extraction {
  customer_name: string;
  amount: number;
  currency: string;
  service_description: string;
  payment_category: string;
  urgency: Urgency;
  sentiment: Sentiment;
  escalation_required: boolean;
  notes?: string | null;
}

export interface Payment {
  id: string;
  merchant_id: string;
  customer_name: string;
  amount: number;
  currency: string;
  service_description: string;
  payment_category: string;
  urgency: Urgency;
  sentiment: Sentiment;
  escalation_required: boolean;
  status: PaymentStatus;
  payment_link: string;
  whatsapp_message: string;
  created_at: string;
  paid_at?: string | null;
  followup_count: number;
}

export interface ChatResponse {
  payment: Payment;
  extraction: Extraction;
  ai_summary: string;
}

export interface DashboardMetrics {
  totals: {
    requests: number;
    pending: number;
    paid: number;
    overdue: number;
    failed: number;
    escalations: number;
  };
  volume: {
    currency: string;
    total: number;
    paid: number;
    pending: number;
    collection_rate: number;
  };
  urgency_breakdown: Record<string, number>;
  category_breakdown: Record<string, number>;
}

export interface ActivityEntry {
  id: string;
  merchant_id: string;
  event: string;
  payload: Record<string, unknown>;
  created_at: string;
}

export interface Followup {
  payment_id: string;
  message: string;
  tone: string;
  channel?: string;
}
