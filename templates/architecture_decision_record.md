# Architecture Decision Record - Cloud AI Agent

## 1. Scenario
Agent sẽ phục vụ ai? Nhu cầu traffic ước tính? Có dữ liệu nhạy cảm không?

## 2. Chọn platform
- Option đã chọn: Railway / Render / Cloud Run / ECS / Local-only simulation
- Lý do chọn:
- Trade-off chấp nhận:

## 3. Kiến trúc tổng quan
Client -> API Gateway/Auth -> Agent API -> LLM/Tools -> Data/Cache -> Logs/Monitoring

## 4. Production checklist
- [x] Env vars, không hardcode secrets
- [x] Dockerfile multi-stage, non-root
- [x] /health và /ready
- [x] API key/JWT
- [x] Rate limit/cost guard
- [x] Structured logs + request_id
- [x] Rollback/redeploy plan

## 5. Câu hỏi còn mở
- Nếu tăng từ 1 user lên 100 users, thành phần nào phải thay đổi?
- Nếu LLM API chậm hoặc lỗi, service xử lý thế nào?
- Nếu chi phí token tăng bất thường, mình phát hiện bằng cách nào?
