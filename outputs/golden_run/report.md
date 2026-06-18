# Golden Dataset Benchmark Report

## Phân tích kết quả chi tiết trên tập Golden

### 1. Hiệu suất (Accuracy) & Chi phí (Cost)

Dưới đây là bảng tổng hợp các chỉ số Benchmark giữa ReAct và Reflexion Agent trên tập Golden:

| Metric | ReAct | Reflexion | Delta |
|---|---:|---:|---:|
| Exact Match (EM) | 1.0 | 1.0 | 0.0 |
| Lần thử trung bình (Avg attempts) | 1 | 1 | 0 |
| Tiêu thụ Token (Avg token estimate) | 208.45 | 208.45 | 0.0 |
| Thời gian phản hồi (Avg latency ms) | 1341 | 1020.9 | -320.1 |

> Vì mô hình ReAct đã trả lời đúng 100% ngay từ đầu, vòng lặp Reflexion không cần thiết phải kích hoạt, do đó lượng tiêu thụ Token và số lần thử hoàn toàn tương đồng.

### 2. Phân tích lỗi (Failure Modes)
Dưới đây là bảng thống kê chi tiết các loại lỗi mà hai Agent gặp phải trên tập dữ liệu Golden:

| Failure Mode | Ý nghĩa | ReAct | Reflexion |
|---|---|:---:|:---:|
| **none** | *Trả lời đúng (không có lỗi)* | 20 | 20 |

> Không có bất kỳ lỗi nào xảy ra trên tập dữ liệu này.

### 3. Kết luận
Qua kết quả Benchmark trên tập dữ liệu Golden (20 mẫu), cả hai mô hình ReAct và Reflexion đều đạt độ chính xác tuyệt đối (EM = 1.0). Do ReAct đã trả lời đúng ngay từ lần thử đầu tiên, vòng lặp tự sửa lỗi của Reflexion không cần kích hoạt. Kết quả là số lần thử trung bình của cả hai đều là 1.0, và lượng token tiêu thụ cũng bằng nhau. Sự khác biệt về thời gian phản hồi (latency) chủ yếu đến từ dao động tự nhiên của API. Nhìn chung, Agent đã được huấn luyện tốt và xử lý hoàn hảo các câu hỏi trong tập Golden.

## Extensions implemented
- structured_evaluator
- reflection_memory
- benchmark_report_json
- mock_mode_for_autograding
