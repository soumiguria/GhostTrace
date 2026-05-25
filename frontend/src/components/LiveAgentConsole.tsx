"use client";

import { AnimatePresence, motion } from "framer-motion";
import type { AgentLog } from "@/lib/api";

interface LiveAgentConsoleProps {
  logs: AgentLog[];
  isActive?: boolean;
}

const agentColors: Record<string, string> = {
  "Entity Agent": "text-emerald-400",
  "Reputation Agent": "text-amber-400",
  "Risk Agent": "text-red-400",
  "Report Agent": "text-violet-400",
  Orchestrator: "text-cyan-400",
};

export function LiveAgentConsole({ logs, isActive }: LiveAgentConsoleProps) {
  return (
    <div className="glass-panel flex h-[320px] flex-col overflow-hidden">
      <div className="flex items-center justify-between border-b border-white/10 px-4 py-3">
        <span className="font-mono text-xs uppercase tracking-widest text-cyan-400">
          Agent Console
        </span>
        <span className="flex items-center gap-2 font-mono text-[10px] text-slate-500">
          {isActive && (
            <motion.span
              className="h-2 w-2 rounded-full bg-emerald-400"
              animate={{ opacity: [1, 0.3, 1] }}
              transition={{ repeat: Infinity, duration: 1 }}
            />
          )}
          LIVE
        </span>
      </div>
      <div className="flex-1 overflow-y-auto p-3 font-mono text-xs">
        <AnimatePresence initial={false}>
          {logs.map((log) => (
            <motion.div
              key={log.id}
              initial={{ opacity: 0, x: -8 }}
              animate={{ opacity: 1, x: 0 }}
              className="mb-2 border-l-2 border-cyan-500/30 pl-3"
            >
              <span className="text-slate-600">
                [{new Date(log.timestamp).toLocaleTimeString()}]
              </span>{" "}
              <span className={agentColors[log.agent_name] || "text-cyan-300"}>
                [{log.agent_name}]
              </span>{" "}
              <span className="text-slate-300">{log.message}</span>
            </motion.div>
          ))}
        </AnimatePresence>
        {logs.length === 0 && (
          <p className="text-slate-600">Awaiting agent deployment...</p>
        )}
      </div>
    </div>
  );
}
