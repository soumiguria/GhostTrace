# GhostTrace Rules

## Must Always

- Treat all submitted content as **untrusted** until verified
- Extract entities before reputation or risk analysis
- Return structured JSON from analysis skills when requested
- Log each agent step for auditability
- Recommend safe actions: do not click links, verify via separate channel, report to security team
- Use demo/heuristic mode when no LLM API key is configured

## Must Never

- Claim 100% certainty or guarantee legal outcomes
- Encourage interacting with suspicious URLs, attachments, or wallet transfers
- Invent emails, domains, or wallets not supported by the input text
- Provide instructions for hacking, credential theft, or harassment
- Store or exfiltrate user PII beyond the investigation session scope

## Output Constraints

- Risk scores: integer 0–100
- Confidence: integer 0–100
- Reports: markdown with Executive Summary, Entities, Behavioral Analysis, Threat Indicators, Risk Assessment, Recommended Actions

## Scope

MVP threat **triage and education**, not enterprise SOC replacement. Findings are advisory.
