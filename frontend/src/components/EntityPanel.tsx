"use client";

import { motion } from "framer-motion";
import { Globe, Link, Mail, Phone, User, Wallet } from "lucide-react";

interface EntityPanelProps {
  entities?: Record<string, string[] | string | unknown>;
}

const sections = [
  { key: "emails", label: "Emails", icon: Mail },
  { key: "urls", label: "URLs", icon: Link },
  { key: "domains", label: "Domains", icon: Globe },
  { key: "usernames", label: "Usernames", icon: User },
  { key: "phone_numbers", label: "Phones", icon: Phone },
  { key: "wallet_addresses", label: "Wallets", icon: Wallet },
] as const;

export function EntityPanel({ entities }: EntityPanelProps) {
  return (
    <div className="glass-panel p-4">
      <h3 className="mb-3 font-mono text-xs uppercase tracking-widest text-cyan-400">
        Extracted Entities
      </h3>
      <div className="grid gap-3 sm:grid-cols-2">
        {sections.map(({ key, label, icon: Icon }, i) => {
          const items = (entities?.[key] as string[]) || [];
          return (
            <motion.div
              key={key}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              className="rounded-lg border border-white/5 bg-black/30 p-3"
            >
              <div className="mb-2 flex items-center gap-2 text-slate-400">
                <Icon className="h-3.5 w-3.5" />
                <span className="text-[10px] uppercase tracking-wider">{label}</span>
              </div>
              {items.length > 0 ? (
                <ul className="space-y-1">
                  {items.map((item) => (
                    <li key={item} className="truncate font-mono text-xs text-emerald-300/90">
                      {item}
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="font-mono text-[10px] text-slate-600">— none —</p>
              )}
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
