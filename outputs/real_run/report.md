# Lab 16 Benchmark Report

## Phân tích kết quả chi tiết

### 1. Hiệu suất (Accuracy) & Chi phí (Cost)

Dưới đây là bảng tổng hợp các chỉ số Benchmark giữa ReAct và Reflexion Agent:

| Metric | ReAct | Reflexion | Delta |
|---|---:|---:|---:|
| Exact Match (EM) | 0.93 | 0.95 | +0.02 |
| Lần thử trung bình (Avg attempts) | 1.00 | 1.13 | +0.13 |
| Tiêu thụ Token (Avg token estimate) | 1828.43 | 2403.58 | +575.15 |
| Thời gian phản hồi (Avg latency ms) | 3017.63 | 3357.39 | +339.76 |

> Reflexion giúp cải thiện độ chính xác thêm 2% bằng cách cho phép Agent thử lại khi có lỗi. Đổi lại, Reflexion tiêu tốn thêm khoảng 31% tokens và chậm hơn 11% so với ReAct do phải thực hiện vòng lặp đánh giá (evaluator) và phản chiếu (reflector).

### 2. Phân tích lỗi (Failure Modes)
Dưới đây là bảng thống kê chi tiết các loại lỗi mà hai Agent gặp phải trên tập dữ liệu:

| Failure Mode | Ý nghĩa | ReAct | Reflexion | Đã khắc phục |
|---|---|:---:|:---:|:---:|
| **none** | *Trả lời đúng (không có lỗi)* | 93 | 95 | +2 |
| **wrong_final_answer** | Lỗi sai hoàn toàn do Agent không tìm được thông tin đúng (hoặc Context không đủ). | 2 | 2 | 0 |
| **entity_drift** | Nhầm lẫn giữa nhiều thực thể tương tự nhau trong ngữ cảnh (Context). | 3 | 2 | +1 |
| **incomplete_multi_hop**| Dừng lại sớm trước khi suy luận đủ số bước yêu cầu. | 2 | 1 | +1 |

### 3. Kết luận
Qua kết quả Benchmark trên 100 mẫu dữ liệu, ta thấy mô hình Reflexion Agent (EM = 95%) vượt trội hơn so với ReAct (EM = 93%). Sự cải thiện này chủ yếu đến từ việc Agent có khả năng tự động đánh giá (self-evaluate) những sai lầm trong lần thử đầu tiên, đặc biệt là các lỗi `incomplete_multi_hop` (chưa đi hết các bước suy luận) và `entity_drift` (nhầm lẫn giữa các thực thể trong văn bản). Mặc dù vậy, Reflexion cũng đánh đổi bằng việc tiêu thụ thêm khoảng 575 tokens (+31%) và tăng độ trễ (latency) thêm khoảng 340ms (+11%) cho mỗi câu hỏi. Nhìn chung, kiến trúc tự phản chiếu (Self-reflection) là một sự bổ sung đáng giá cho các bài toán QA phức tạp đòi hỏi suy luận nhiều bước.

## Extensions implemented
- structured_evaluator
- reflection_memory
- benchmark_report_json
- mock_mode_for_autograding
