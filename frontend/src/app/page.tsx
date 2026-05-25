"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Hero } from "@/components/Hero";
import { DemoInput } from "@/components/DemoInput";
import { ThreatMeter } from "@/components/ThreatMeter";
import { LiveAgentConsole } from "@/components/LiveAgentConsole";
import { EntityPanel } from "@/components/EntityPanel";
import { IntelligenceReport } from "@/components/IntelligenceReport";
import { InvestigationTimeline } from "@/components/InvestigationTimeline";
import { useInvestigationPolling } from "@/hooks/useInvestigationPolling";
import { startInvestigation } from "@/lib/api";

export default function Home() {
  const [input, setInput] = useState("");
  const [investigationId, setInvestigationId] = useState<string | null>(null);
  const [starting, setStarting] = useState(false);
  const { data, error, isPolling } = useInvestigationPolling(investigationId);

  const risk = data?.workflow_state?.risk || data?.findings?.risk;
  const riskScore =
    (risk as { risk_score?: number })?.risk_score ??
    data?.risk_score ??
    0;
  const confidence = (risk as { confidence?: number })?.confidence;
  const classification = (risk as { classification?: string })?.classification;
  const entities =
    data?.workflow_state?.entities ||
    (data?.findings?.entities as Record<string, string[]>);
  const redFlags = data?.findings?.reputation?.red_flags;

  async function handleInvestigate() {
    if (!input.trim()) return;
    setStarting(true);
    try {
      const res = await startInvestigation(input.trim());
      setInvestigationId(res.investigation_id);
    } catch {
      alert("Failed to connect to GhostTrace API. Is the backend running on :8000?");
    } finally {
      setStarting(false);
    }
  }

  const showDashboard = !!investigationId;

  return (
    <main className="min-h-screen pb-20">
      <Hero />

      <section className="px-4">
        <DemoInput
          value={input}
          onChange={setInput}
          onInvestigate={handleInvestigate}
          isLoading={starting || isPolling}
        />
        {error && (
          <p className="mx-auto mt-4 max-w-3xl text-center font-mono text-sm text-red-400">
            {error}
          </p>
        )}
      </section>

      <AnimatePresence>
        {showDashboard && (
          <motion.section
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="mx-auto mt-12 max-w-7xl px-4"
          >
            <div className="mb-6 flex items-center justify-between">
              <h2 className="font-mono text-sm uppercase tracking-[0.25em] text-cyan-400">
                Live Investigation Dashboard
              </h2>
              <span className="font-mono text-[10px] text-slate-600">
                ID: {investigationId?.slice(0, 8)}… · {data?.status || "connecting"}
              </span>
            </div>

            <div className="grid gap-4 lg:grid-cols-12">
              <div className="lg:col-span-3">
                <ThreatMeter
                  score={riskScore}
                  confidence={confidence}
                  classification={classification}
                  isActive={isPolling}
                />
                <div className="mt-4">
                  <InvestigationTimeline
                    currentStep={data?.workflow_state?.current_step}
                    status={data?.status}
                  />
                </div>
              </div>

              <div className="lg:col-span-5">
                <LiveAgentConsole logs={data?.logs || []} isActive={isPolling} />
                <div className="mt-4">
                  <EntityPanel entities={entities as Record<string, string[]>} />
                </div>
              </div>

              <div className="lg:col-span-4">
                <IntelligenceReport
                  report={data?.final_report}
                  classification={classification}
                  redFlags={redFlags}
                />
              </div>
            </div>
          </motion.section>
        )}
      </AnimatePresence>
    </main>
  );
}
