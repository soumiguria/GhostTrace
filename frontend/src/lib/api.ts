const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface AgentLog {
  id: string;
  agent_name: string;
  message: string;
  timestamp: string;
}

export interface InvestigationResponse {
  investigation_id: string;
  status: string;
  raw_input: string;
  created_at: string;
  workflow_state?: {
    current_step?: string;
    entities?: Record<string, unknown>;
    reputation?: Record<string, unknown>;
    risk?: {
      risk_score?: number;
      confidence?: number;
      classification?: string;
      scam_likelihood?: number;
      reasoning?: string;
    };
  };
  logs: AgentLog[];
  risk_score?: number | null;
  findings?: {
    entities?: Record<string, string[]>;
    reputation?: {
      red_flags?: string[];
      trust_signals?: string[];
      behavioral_analysis?: string;
    };
    risk?: Record<string, unknown>;
  };
  final_report?: string | null;
}

export async function startInvestigation(input: string): Promise<{ investigation_id: string; status: string }> {
  const res = await fetch(`${API_BASE}/investigate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ input }),
  });
  if (!res.ok) throw new Error("Failed to start investigation");
  return res.json();
}

export async function getInvestigation(id: string): Promise<InvestigationResponse> {
  const res = await fetch(`${API_BASE}/investigation/${id}`, { cache: "no-store" });
  if (!res.ok) throw new Error("Investigation not found");
  return res.json();
}
