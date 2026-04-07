import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# 1. Tải các biến môi trường từ file .env
load_dotenv()

# 2. Kiểm tra xem Key đã được đọc thành công chưa
api_key = os.getenv("OPENAI_API_KEY")

try:
    # 3. Thử gọi một câu lệnh đơn giản tới OpenAI
    llm = ChatOpenAI(model="gpt-4o-mini")
    response = llm.invoke("Hãy nói 'Xin chào, hệ thống đã sẵn sàng!'")
    
    print(f"🤖 Phản hồi từ AI: {response.content}")
    print("🚀 Sanity Check thành công! Bạn có thể bắt đầu code Agent.")
    
except Exception as e:
    print(f"❌ Lỗi kết nối API: {e}")