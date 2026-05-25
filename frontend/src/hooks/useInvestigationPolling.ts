"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { getInvestigation, type InvestigationResponse } from "@/lib/api";

const POLL_MS = 800;

export function useInvestigationPolling(investigationId: string | null) {
  const [data, setData] = useState<InvestigationResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const poll = useCallback(async () => {
    if (!investigationId) return;
    try {
      const result = await getInvestigation(investigationId);
      setData(result);
      setError(null);
      if (result.status === "completed" || result.status === "failed") {
        if (intervalRef.current) {
          clearInterval(intervalRef.current);
          intervalRef.current = null;
        }
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : "Polling failed");
    }
  }, [investigationId]);

  useEffect(() => {
    if (!investigationId) {
      setData(null);
      return;
    }
    poll();
    intervalRef.current = setInterval(poll, POLL_MS);
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [investigationId, poll]);

  return { data, error, isPolling: !!investigationId && data?.status !== "completed" && data?.status !== "failed" };
}
