---
name: investigate-payload
description: End-to-end investigation entry skill — coordinates the four-phase pipeline on a single suspicious payload.
license: MIT
metadata:
  category: orchestration
  risk_tier: standard
---

# Investigate Payload

When the user provides suspicious content:

1. Invoke **entity-extraction** on the raw text
2. Pass entities to **reputation-analysis**
3. Pass reputation + entities to **risk-scoring**
4. Pass all findings to **report-generation**

Emit brief status logs after each phase for live console display.

Final output: JSON summary + markdown report.
