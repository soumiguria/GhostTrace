"use client";

import { motion } from "framer-motion";
import { CheckCircle2, Circle, Loader2 } from "lucide-react";

const STEPS = [
  { id: "entity_extraction", label: "Entity Extraction", agent: "Entity Agent" },
  { id: "reputation_analysis", label: "Reputation Analysis", agent: "Reputation Agent" },
  { id: "risk_scoring", label: "Risk Scoring", agent: "Risk Agent" },
  { id: "report_generation", label: "Report Generation", agent: "Report Agent" },
  { id: "completed", label: "Complete", agent: "Orchestrator" },
];

interface InvestigationTimelineProps {
  currentStep?: string;
  status?: string;
}

function stepIndex(step?: string): number {
  if (!step) return -1;
  const idx = STEPS.findIndex((s) => s.id === step);
  return idx >= 0 ? idx : -1;
}

export function InvestigationTimeline({ currentStep, status }: InvestigationTimelineProps) {
  const activeIdx = stepIndex(currentStep);
  const done = status === "completed";

  return (
    <div className="glass-panel p-4">
      <h3 className="mb-4 font-mono text-xs uppercase tracking-widest text-cyan-400">
        Investigation Timeline
      </h3>
      <div className="space-y-3">
        {STEPS.map((step, i) => {
          const isComplete = done || i < activeIdx;
          const isCurrent = !done && i === activeIdx;
          const isPending = i > activeIdx && !done;

          return (
            <motion.div
              key={step.id}
              layout
              className="flex items-center gap-3"
            >
              {isComplete ? (
                <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-400" />
              ) : isCurrent ? (
                <Loader2 className="h-4 w-4 shrink-0 animate-spin text-cyan-400" />
              ) : (
                <Circle className="h-4 w-4 shrink-0 text-slate-600" />
              )}
              <div className="flex-1">
                <p
                  className={`font-mono text-xs ${
                    isCurrent ? "text-cyan-300" : isPending ? "text-slate-600" : "text-slate-300"
                  }`}
                >
                  {step.label}
                </p>
                <p className="text-[10px] text-slate-600">{step.agent}</p>
              </div>
              {isCurrent && (
                <motion.span
                  className="font-mono text-[10px] text-cyan-500"
                  animate={{ opacity: [0.4, 1, 0.4] }}
                  transition={{ repeat: Infinity, duration: 1.5 }}
                >
                  RUNNING
                </motion.span>
              )}
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
