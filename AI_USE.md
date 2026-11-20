# AI USAGE REPORT — Nhóm 02 (Track A: Dr May Day)

## 1. Tuyên bố sử dụng AI
Nhóm 02 xác nhận có sử dụng công cụ Trí tuệ Nhân tạo (AI) trong quá trình nghiên cứu đặc tả, thiết kế ca kiểm thử và hoàn thiện tài liệu kỹ thuật cho bài tập lớn KTPMUD Track A. Mọi đầu ra của AI đều được thành viên nhóm rà soát thủ công theo `docs/decision-table.md` V1 và kiểm chứng bằng `pytest` trước khi commit.

## 2. Nhật ký sử dụng AI (Theo chuẩn Mục 5.3)

| Công cụ / Model | Mục đích | Phạm vi (File / Module) | Kiểm chứng | Quyết định của nhóm | Người chịu trách nhiệm |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Gemini** (Google) | Phân tích đặc tả `docs/decision-table.md`, rà soát acceptance criteria `A-01`–`A-11`, gợi ý 22 ca unit test, viết script đo benchmark và soạn thảo báo cáo kỹ thuật. | `tests/test_classifier.py`, `benchmark.py`, `TEST_REPORT.md`, `SECURITY_PRIVACY_CHECKLIST.md`, `AI_USE.md` | Chạy `pytest -v` (22/22 PASSED), chạy `python benchmark.py` (`p95 = 0.0007 ms`) và đối chiếu thủ công từng ngưỡng tuổi/HATT với bảng quyết định. | **Giữ & Tinh chỉnh**: Giữ khung cấu trúc và mã kiểm thử; chỉnh sửa lại thông số môi trường và thông tin nhóm cho khớp thực tế. | TV_NHOM02 |
| **Claude** (Anthropic) | Tham vấn thiết kế các kịch bản biên (boundary) và cách xử lý ngoại lệ cho dữ liệu thiếu/sai kiểu (`missing` / `invalid`). | `rule_engine/classifier.py`, `REQUIREMENTS.md` | Đối chiếu từng điều kiện rẽ nhánh với các quy tắc làm rõ trên kênh hỏi đáp và kiểm thử qua nhóm test `TC-B01`–`TC-I04`. | **Giữ có chọn lọc**: Chỉ áp dụng các xử lý an toàn (`THEO_DOI` khi thiếu `tuoi` hoặc sai kiểu) đúng contract đã khóa, loại bỏ mọi gợi ý vượt phạm vi V1. | TV_NHOM02 |

## 3. Cam kết tuân thủ quy định (Mục 5.2)
- Không sử dụng dữ liệu bệnh nhân thật hay đưa thông tin nhận dạng cá nhân (PII/PHI) vào bất kỳ prompt nào.
- Không để AI tự động merge code, tự tạo release hay tự xác nhận bài đạt chuẩn.