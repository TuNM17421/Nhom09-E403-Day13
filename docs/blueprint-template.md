# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 0. Project Overview
- [PROJECT_NAME]: Day 13 Observability Lab
- [PROJECT_TYPE]: FastAPI agent observability implementation
- [PROJECT_GOAL]: Build and demonstrate a small FastAPI-based agent instrumented with structured logging, correlation ID propagation, PII scrubbing, tracing, metrics, SLOs, alerts, and a final blueprint report.
- [OBSERVABILITY_ARCHITECTURE]: Request enters FastAPI through middleware, correlation_id is attached and propagated through logs, application events are recorded as JSON logs, PII is scrubbed before persistence, traces are sent to Langfuse, metrics are aggregated in-memory, and dashboards plus alerts are used to monitor health, cost, latency, and quality.

## 1. Team Metadata
- [GROUP_NAME]: Group 9
- [REPO_URL]: https://github.com/TuNM17421/Nhom09-E403-Day13
- [MEMBERS]:
  - Member A: [Name] Hoàng Sơn Lâm | Role: Backend & Security
  - Member B: [Name] Lưu Linh Ly | Role: Tracing & Enrichment
  - Member C: [Name] Lê Tuấn Đạt | Role: Reliability & Incidents
  - Member D: [Name] Nguyễn Mạnh Tú | Role: UI & Integration Lead

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: /100
- [TOTAL_TRACES_COUNT]: 
- [PII_LEAKS_FOUND]: 

---

## 3. Technical Evidence (Group)

> Add screenshots into a shared evidence folder and paste the relative paths below.

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: [Path to image]
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: [Path to image]
- [EVIDENCE_TRACE_LIST_SCREENSHOT]: [Path to image]
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: [Path to image]
- [TRACE_WATERFALL_EXPLANATION]: (Briefly explain one interesting span in your trace)
- [LOGGING_SUMMARY]: Logs are emitted in JSON format, include correlation IDs, and contain contextual metadata for debugging.

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: [Path to image]
- [DASHBOARD_NOTES]: Main 6 panels currently include Latency P50/P95/P99, Traffic QPS, Error Rate %, Cost $/hour, Tokens in/out, and Hallucination %.
- [SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | |
| Error Rate | < 2% | 28d | |
| Cost Budget | < $2.5/day or team hourly equivalent | 1d | |
| Quality Proxy | > 75% | 28d | |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: [ALERT_RULES_SCREENSHOT](ALERT_RULES_SCREENSHOT.PNG)
- [SAMPLE_RUNBOOK_LINK]: [docs/alerts.md](docs/alerts.md)
- [ALERT_SUMMARY]: The team implemented 4 symptom-based alerts in [config/alert_rules.yaml](config/alert_rules.yaml): high_latency_p95, high_error_rate, cost_budget_spike, and low_quality_score. These alerts cover latency, reliability, spending, and AI answer quality. Each alert is mapped to a concrete runbook in [docs/alerts.md](docs/alerts.md), including severity, trigger condition, impact, first checks, and mitigation steps. The team uses the debug path Metrics -> Traces -> Logs to investigate any alert that fires.

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]: (e.g., rag_slow)
- [SYMPTOMS_OBSERVED]: 
- [ROOT_CAUSE_PROVED_BY]: (List specific Trace ID or log evidence)
- [DEBUG_PATH]: Metrics -> Traces -> Logs
- [FIX_ACTION]: 
- [PREVENTIVE_MEASURE]: 

---

## 5. Individual Contributions & Evidence

### [MEMBER_A_NAME]
- [ROLE]: Backend & Security
- [TASKS_COMPLETED]: Correlation ID propagation, structured logging, log schema verification
- [EVIDENCE_LINK]: (Link to specific commit or PR)

### [MEMBER_B_NAME]
- [ROLE]: Tracing & Enrichment
- [TASKS_COMPLETED]: Trace instrumentation, metadata tagging, context enrichment
- [EVIDENCE_LINK]: 

### [MEMBER_C_NAME]
- [ROLE]: Reliability & Incidents
- [TASKS_COMPLETED]: SLO definitions, alert rules, incident analysis and mitigation
- [EVIDENCE_LINK]: 

### [MEMBER_D_NAME]
- [ROLE]: UI & Integration Lead
- [TASKS_COMPLETED]: Dashboard design, evidence collection, report assembly, demo flow
- [EVIDENCE_LINK]: 

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: (Description + Evidence)
- [BONUS_AUDIT_LOGS]: (Description + Evidence)
- [BONUS_CUSTOM_METRIC]: (Description + Evidence)

---

## 7. Submission Packaging Checklist
- [ ] All screenshot paths are filled in
- [ ] All member names are filled in
- [ ] Final validator score is updated
- [ ] Total trace count is updated
- [ ] Incident response section is complete
- [ ] Commit or PR evidence is included for every member
- [ ] Report is ready for demo and grading review
