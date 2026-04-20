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
  - Member A: Hoàng Sơn Lâm | Role: Backend & Security
  - Member B: Lưu Linh Ly | Role: Tracing & Enrichment
  - Member C: Lê Tuấn Đạt | Role: Reliability & Incidents
  - Member D: Nguyễn Mạnh Tú | Role: UI & Integration Lead

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: 100/100
- [TOTAL_TRACES_COUNT]: 56
- [PII_LEAKS_FOUND]: 0

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: ![alt text](EVIDENCE_CORRELATION_ID_SCREENSHOT.PNG)
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: ![alt text](EVIDENCE_PII_REDACTION_SCREENSHOT.jpg)
- [EVIDENCE_TRACE_LIST_SCREENSHOT]: ![alt text](EVIDENCE_TRACE_LIST_SCREENSHOT.jpg)
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: ![alt text](EVIDENCE_TRACE_WATERFALL_SCREENSHOT.jpg)
- [TRACE_WATERFALL_EXPLANATION]: Trace này đại diện cho một request tiêu chuẩn. Run span hoàn thành trong khoảng 150ms với việc sử dụng token ổn định (29 input, 152 output), cho thấy hệ thống phản hồi chính xác mà không gặp phải độ trễ bất thường nào. Nó đóng vai trò là điểm tham chiếu hữu ích để so sánh với các kịch bản sự cố như rag_slow.
- [LOGGING_SUMMARY]: Các bản ghi log được phát hành dưới dạng JSON, bao gồm Correlation ID và chứa metadata theo ngữ cảnh để phục vụ việc chẩn đoán lỗi.

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: ![alt text](DASHBOARD_6_PANELS_SCREENSHOT.jpg)
- [DASHBOARD_NOTES]: 6 bảng điều khiển chính hiện bao gồm: Latency P50/P95/P99, Traffic QPS, Error Rate %, Cost $/hour, Tokens in/out, và Hallucination %.
- [SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 2000ms | 7d | ~315ms (Baseline) / ~2660ms (Incident) |
| Error Rate | < 1% | 7d | 0% |
| Cost Budget | < $2.0/day | 1d | ~$0.017/day |
| Quality Proxy | > 80% | 7d | 80% |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: ![alt text](ALERT_RULES_SCREENSHOT.PNG)
- [SAMPLE_RUNBOOK_LINK]: [docs/alerts.md](docs/alerts.md)
- [ALERT_SUMMARY]: Nhóm đã triển khai 4 cảnh báo dựa trên triệu chứng (symptom-based) trong [config/alert_rules.yaml](config/alert_rules.yaml): high_latency_p95, high_error_rate, cost_budget_spike, và low_quality_score. Mỗi cảnh báo được ánh xạ tới một runbook cụ thể trong [docs/alerts.md](docs/alerts.md), bao gồm mức độ nghiêm trọng, điều kiện kích hoạt, tác động, các bước kiểm tra đầu tiên và biện pháp giảm thiểu.

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]: rag_slow
- [SYMPTOMS_OBSERVED]: Sau khi kích hoạt sự cố `rag_slow`, độ trễ P95 tăng vọt từ ~315ms lên mức trung bình ~2660ms (vượt ngưỡng SLO 2000ms). Người dùng sẽ cảm thấy ứng dụng phản hồi rất chậm.
- [ROOT_CAUSE_PROVED_BY]: Sự cố được xác nhận thông qua Correlation ID `req-dab0459e`. Khi kiểm tra Trace Waterfall trên Langfuse, span `retrieve` (RAG) chiếm tới ~2500ms, trong khi các bước khác vẫn ổn định. Điều này chứng minh nút thắt cổ chai nằm ở tầng truy xuất dữ liệu.
- [DEBUG_PATH]: Metrics (Dashboard) -> Traces (Langfuse Waterfall) -> Logs (JSONL with Correlation ID)
- [FIX_ACTION]: Vô hiệu hóa kịch bản sự cố và kiểm tra lại hệ thống RAG để đảm bảo không có độ trễ giả lập.
- [PREVENTIVE_MEASURE]: Thiết lập **Timeout** (ví dụ: 1000ms) cho các cuộc gọi RAG và bổ sung cơ chế phản hồi dự phòng (fallback) để đảm bảo UX khi RAG gặp sự cố.

---

## 5. Individual Contributions & Evidence

### Hoàng Sơn Lâm
- [ROLE]: Backend & Security
- [TASKS_COMPLETED]: Triển khai Correlation ID propagation, Structured Logging và bộ lọc PII đệ quy (Recursive Scrubbing).
- [EVIDENCE_LINK]: ![alt text](SonLam_commit.PNG)

### Lưu Linh Ly
- [ROLE]: Reliability & Incidents
- [TASKS_COMPLETED]: Định nghĩa SLO, cấu hình Alert Rules và phân tích/khắc phục sự cố (Incident Analysis).
- [EVIDENCE_LINK]: ![alt text](LinhLy_commit.PNG)

### Lê Tuấn Đạt
- [ROLE]: Tracing & Enrichment
- [TASKS_COMPLETED]: Tích hợp Langfuse Tracing, gắn metadata tagging và enrichment context cho Agent.
- [EVIDENCE_LINK]: ![alt text](TuanDat_commit.PNG)

### Nguyễn Mạnh Tú
- [ROLE]: UI & Integration Lead
- [TASKS_COMPLETED]: Thiết kế Dashboard 6 panels, thu thập bằng chứng và tổng hợp báo cáo Blueprint cuối cùng.
- [EVIDENCE_LINK]: ![alt text](ManhTu_commit.PNG)

---

## 6. Bonus Items (Optional)
- [BONUS_PII_RECURSIVE_SCRUBBING]: Đã triển khai bộ lọc PII quét đệ quy qua toàn bộ Object/List trong Log, đảm bảo không rò rỉ thông tin nhạy cảm ở bất kỳ tầng nào.
- [BONUS_SLO_ALIGNMENT]: Các ngưỡng Alert được tinh chỉnh khớp hoàn toàn với SLO mục tiêu (2000ms Latency, 1% Error Rate).

---

## 7. Submission Packaging Checklist
- [v] All screenshot paths are filled in
- [v] All member names are filled in
- [v] Final validator score is updated
- [v] Total trace count is updated
- [v] Incident response section is complete
- [v] Commit or PR evidence is included for every member
- [v] Report is ready for demo and grading review
