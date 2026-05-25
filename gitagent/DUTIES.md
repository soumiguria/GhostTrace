# Segregation of Duties — GhostTrace Investigation Swarm

| Role | Agent | Permissions | Boundaries |
|------|-------|-------------|------------|
| Orchestrator | `ghosttrace-orchestrator` | Delegate, sequence workflow, persist logs | Does not score risk or write final report body alone |
| Entity Extractor | `entity-extractor` | Parse IOCs (email, URL, domain, wallet) | No reputation or risk judgments |
| Reputation Analyst | `reputation-analyst` | Red flags, trust signals, behavioral notes | No numeric risk score |
| Risk Scorer | `risk-scorer` | risk_score, confidence, classification | No entity parsing |
| Report Generator | `report-generator` | Markdown report synthesis | No new IOC extraction |

## Conflict Rules

- Entity extraction **must complete** before reputation analysis
- Reputation analysis **must complete** before risk scoring
- Risk scoring **must complete** before report generation
