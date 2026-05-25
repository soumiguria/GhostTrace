"use client";

import { motion } from "framer-motion";
import { Ghost, Radar, Shield } from "lucide-react";

export function Hero() {
  return (
    <section className="relative overflow-hidden px-4 pb-12 pt-16 text-center md:pt-24">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_center,_rgba(34,211,238,0.12)_0%,_transparent_55%)]" />
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="relative z-10 mx-auto max-w-4xl"
      >
        <div className="mb-6 flex items-center justify-center gap-3">
          <Ghost className="h-10 w-10 text-cyan-400 drop-shadow-[0_0_12px_rgba(34,211,238,0.8)]" />
          <span className="font-mono text-xs uppercase tracking-[0.4em] text-cyan-500/80">
            GhostTrace AI
          </span>
        </div>
        <h1 className="bg-gradient-to-b from-white via-cyan-100 to-cyan-600/80 bg-clip-text text-4xl font-bold tracking-tight text-transparent md:text-6xl">
          Autonomous Cyber Investigation Lab
        </h1>
        <p className="mx-auto mt-6 max-w-2xl text-lg text-slate-400">
          Deploy a multi-agent swarm to analyze suspicious messages, links, and identities.
          Watch live orchestration. Receive structured threat intelligence.
        </p>
        <div className="mt-8 flex flex-wrap items-center justify-center gap-6 text-sm text-slate-500">
          <span className="flex items-center gap-2">
            <Radar className="h-4 w-4 text-cyan-500" /> LangGraph Agents
          </span>
          <span className="flex items-center gap-2">
            <Shield className="h-4 w-4 text-emerald-500" /> Risk Scoring
          </span>
          <span className="font-mono text-cyan-600/60">v1.0 MVP</span>
        </div>
      </motion.div>
    </section>
  );
}
