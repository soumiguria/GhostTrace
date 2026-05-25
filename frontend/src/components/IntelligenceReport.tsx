"use client";

import { motion } from "framer-motion";
import ReactMarkdown from "react-markdown";
import { FileText, ShieldAlert } from "lucide-react";

interface IntelligenceReportProps {
  report?: string | null;
  classification?: string;
  redFlags?: string[];
}

export function IntelligenceReport({ report, classification, redFlags }: IntelligenceReportProps) {
  if (!report) {
    return (
      <div className="glass-panel flex h-64 items-center justify-center p-6 text-slate-500">
        <p className="font-mono text-sm">Report pending agent synthesis...</p>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-panel overflow-hidden"
    >
      <div className="flex items-center gap-3 border-b border-white/10 bg-red-500/5 px-5 py-4">
        <ShieldAlert className="h-5 w-5 text-red-400" />
        <div>
          <h3 className="font-mono text-sm uppercase tracking-widest text-red-300">
            Intelligence Report
          </h3>
          {classification && (
            <p className="text-xs text-slate-400">{classification}</p>
          )}
        </div>
        <FileText className="ml-auto h-4 w-4 text-slate-600" />
      </div>
      {redFlags && redFlags.length > 0 && (
        <div className="border-b border-white/5 px-5 py-3">
          <p className="mb-2 text-[10px] uppercase tracking-wider text-amber-400">Active Indicators</p>
          <div className="flex flex-wrap gap-2">
            {redFlags.map((f) => (
              <span
                key={f}
                className="rounded border border-amber-500/30 bg-amber-500/10 px-2 py-0.5 font-mono text-[10px] text-amber-200"
              >
                {f}
              </span>
            ))}
          </div>
        </div>
      )}
      <div className="prose-invert max-h-[400px] overflow-y-auto p-5 prose prose-sm prose-headings:font-mono prose-headings:text-cyan-300 prose-p:text-slate-300">
        <ReactMarkdown>{report}</ReactMarkdown>
      </div>
    </motion.div>
  );
}
