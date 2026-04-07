# TravelBuddy - AI Travel Agent with LangGraph

Dự án này triển khai một AI Agent hỗ trợ lập kế hoạch du lịch sử dụng thư viện **LangGraph** và **Google Gemini API**. Agent có khả năng tự động gọi các công cụ (tools) để tìm chuyến bay, khách sạn và tính toán ngân sách một cách thông minh.

## 🛠 Thành phần dự án
- `agent.py`: Định nghĩa cấu trúc StateGraph, các Nodes và Edges điều hướng luồng suy nghĩ của Agent.
- `tools.py`: Triển khai các công cụ (Search Flights, Search Hotels, Calculate Budget) với xử lý lỗi try/except.
- `system_prompt.txt`: Chứa Persona và các ràng buộc (Guardrails) để đảm bảo Agent hoạt động đúng phạm vi du lịch.
- `run_tests.py`: Script tự động chạy 5 kịch bản kiểm thử (Test Cases) và xuất kết quả.

## 🚀 Hướng dẫn cài đặt và chạy

### 1. Chuẩn bị môi trường
Yêu cầu Python 3.10+ (Khuyến nghị 3.12.x).
```bash
# Tạo và kích hoạt môi trường ảo
python -m venv venv
source venv/bin/activate

# Cài đặt thư viện cần thiết
pip install langchain-google-genai langgraph python-dotenv