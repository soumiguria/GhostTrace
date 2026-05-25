"use client";

import { motion } from "framer-motion";
import { ScanSearch } from "lucide-react";
import { Button } from "@/components/ui/button";

const SAMPLE = `URGENT: Your Microsoft account will be suspended in 24 hours.
Verify immediately: https://micros0ft-security-verify.net/login
Contact: support@micros0ft-security-verify.net
Send 0.5 BTC to 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb`;

interface DemoInputProps {
  value: string;
  onChange: (v: string) => void;
  onInvestigate: () => void;
  isLoading?: boolean;
}

export function DemoInput({ value, onChange, onInvestigate, isLoading }: DemoInputProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-panel mx-auto max-w-3xl p-4 md:p-6"
    >
      <label className="mb-2 block font-mono text-xs uppercase tracking-widest text-cyan-400">
        Suspicious Payload
      </label>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        rows={6}
        placeholder="Paste phishing email, scam DM, suspicious URL, recruiter message..."
        className="w-full resize-none rounded-lg border border-cyan-500/20 bg-black/50 p-4 font-mono text-sm text-slate-200 placeholder:text-slate-600 focus:border-cyan-400/50 focus:outline-none focus:ring-1 focus:ring-cyan-400/30"
      />
      <div className="mt-4 flex flex-wrap items-center gap-3">
        <Button size="lg" onClick={onInvestigate} disabled={isLoading || !value.trim()}>
          <ScanSearch className="h-4 w-4" />
          {isLoading ? "Investigating..." : "Investigate"}
        </Button>
        <Button
          variant="ghost"
          size="sm"
          type="button"
          onClick={() => onChange(SAMPLE)}
          disabled={isLoading}
        >
          Load demo payload
        </Button>
      </div>
    </motion.div>
  );
}
