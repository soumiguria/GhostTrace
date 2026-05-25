"use client";

import { motion, useSpring, useTransform, useMotionValueEvent } from "framer-motion";
import { useEffect, useState } from "react";

interface ThreatMeterProps {
  score: number;
  confidence?: number;
  classification?: string;
  isActive?: boolean;
}

export function ThreatMeter({ score, confidence, classification, isActive }: ThreatMeterProps) {
  const spring = useSpring(0, { stiffness: 60, damping: 18 });
  const [displayScore, setDisplayScore] = useState(0);
  const circumference = 2 * Math.PI * 54;
  const offset = useTransform(spring, (v) => circumference - (v / 100) * circumference);

  useMotionValueEvent(spring, "change", (v) => setDisplayScore(Math.round(v)));

  useEffect(() => {
    spring.set(score);
  }, [score, spring]);

  const color =
    score >= 75 ? "#f87171" : score >= 50 ? "#fbbf24" : score > 0 ? "#22d3ee" : "#64748b";

  return (
    <div className="glass-panel flex flex-col items-center p-6">
      <p className="mb-4 font-mono text-xs uppercase tracking-[0.3em] text-cyan-400/80">
        Threat Assessment
      </p>
      <div className="relative h-36 w-36">
        <svg className="h-full w-full -rotate-90" viewBox="0 0 120 120">
          <circle cx="60" cy="60" r="54" fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="8" />
          <motion.circle
            cx="60"
            cy="60"
            r="54"
            fill="none"
            stroke={color}
            strokeWidth="8"
            strokeLinecap="round"
            strokeDasharray={circumference}
            style={{ strokeDashoffset: offset, filter: `drop-shadow(0 0 8px ${color})` }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="font-mono text-4xl font-bold text-white">{displayScore}</span>
          <span className="text-xs text-slate-500">/ 100</span>
        </div>
        {isActive && (
          <motion.div
            className="absolute inset-0 rounded-full border border-cyan-400/30"
            animate={{ scale: [1, 1.08, 1], opacity: [0.4, 0.8, 0.4] }}
            transition={{ repeat: Infinity, duration: 2 }}
          />
        )}
      </div>
      {classification && (
        <p className="mt-4 text-center text-sm text-slate-300">{classification}</p>
      )}
      {confidence !== undefined && (
        <p className="mt-1 font-mono text-xs text-slate-500">
          Confidence: {Math.round(confidence)}%
        </p>
      )}
    </div>
  );
}
