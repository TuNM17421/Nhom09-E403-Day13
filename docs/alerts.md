# Alert Rules and Runbooks

## 1. High latency P95
- Severity: P2
- Trigger: `latency_p95_ms > 2000 for 10m`
- Impact: Trải nghiệm người dùng bị ảnh hưởng, phản hồi chậm trễ.
- First checks:
  1. Mở các trace chậm nhất (top slow traces) trong 1 giờ qua trên Langfuse.
  2. So sánh thời gian xử lý của RAG span vs LLM span để tìm nút thắt cổ chai.
  3. Kiểm tra xem sự cố `rag_slow` có đang bị kích hoạt không bằng lệnh: `python scripts/inject_incident.py --status`.
- Mitigation:
  - Giảm số lượng tài liệu truy xuất (Top-K) trong RAG.
  - Sử dụng mô hình LLM nhỏ hơn/nhanh hơn nếu cần.
  - Tối ưu hóa prompt để giảm tokens đầu vào.

## 2. High error rate
- Severity: P1
- Trigger: `error_rate_pct > 1 for 2m`
- Impact: Người dùng nhận được thông báo lỗi, dịch vụ không ổn định.
- First checks:
  1. Nhóm logs theo trường `error_type` để tìm lỗi phổ biến nhất.
  2. Kiểm tra các trace bị lỗi (failed traces) để xem stack trace chi tiết.
  3. Xác định lỗi đến từ LLM (Timeout/Rate limit), Schema hay lỗi Logic Backend.
- Mitigation:
  - Hoàn tác (Rollback) bản cập nhật gần nhất nếu nghi ngờ do code mới.
  - Tạm thời tắt các tính năng (tools) đang gây lỗi.
  - Kích hoạt cơ chế Retry với backoff hoặc chuyển sang model dự phòng.

## 3. Cost budget spike
- Severity: P2
- Trigger: `hourly_cost_usd > 0.5 for 30m`
- Impact: Ngân sách dự án bị thâm hụt nhanh chóng.
- First checks:
  1. Phân tích trace theo `feature` và `model` để tìm nguồn tiêu tốn tiền nhiều nhất.
  2. So sánh tỷ lệ `tokens_in` và `tokens_out`.
  3. Kiểm tra xem có hiện tượng "Prompt Injection" hoặc vòng lặp vô tận nào không.
- Mitigation:
  - Áp dụng giới hạn số lượng token tối đa (max_tokens).
  - Chuyển các yêu cầu đơn giản sang mô hình rẻ hơn (ví dụ: GPT-3.5 thay vì GPT-4).
  - Kích hoạt bộ nhớ đệm (Prompt Cache) nếu có thể.

## 4. Low quality score
- Severity: P3
- Trigger: `quality_score_avg < 0.7 for 15m`
- Impact: AI trả lời không chính xác, gây mất lòng tin ở người dùng.
- First checks:
  1. Kiểm tra các trace có `quality_score` thấp.
  2. Xem xét dữ liệu đầu vào của RAG (Context) có liên quan đến câu hỏi không.
  3. Kiểm tra xem Prompt có bị thay đổi hoặc không đủ rõ ràng không.
- Mitigation:
  - Cập nhật lại cơ sở dữ liệu tri thức (Knowledge Base).
  - Tinh chỉnh System Prompt để hướng dẫn AI trả lời tốt hơn.
  - Thêm các ví dụ Few-shot vào prompt để cải thiện độ chính xác.
