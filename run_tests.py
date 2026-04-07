import sys
import time
from agent import graph

def run_auto_tests():
    test_cases = [
        {
            "id": "Test 1: Direct Answer",
            "input": "Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu."
        },
        {
            "id": "Test 2: Single Tool Call",
            "input": "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng"
        },
        {
            "id": "Test 3: Multi-Step Tool Chaining",
            "input": "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!"
        },
        {
            "id": "Test 4: Missing Info / Clarification",
            "input": "Tôi muốn đặt khách sạn"
        },
        {
            "id": "Test 5: Guardrail / Refusal",
            "input": "Giải giúp tôi bài lập trình Python về linked list"
        }
    ]

    print("# BÁO CÁO KẾT QUẢ LAB 4: LANGGRAPH TRAVEL AGENT\n")
    print("**Sinh viên:** Hoàng Hiệp")
    print("**MSSV:** [Điền MSSV Của Bạn]\n")
    print("---\n")

    for index, test in enumerate(test_cases):
        print(f"## {test['id']}")
        print(f"**User:** \"{test['input']}\"")
        print("\n**Console Log & TravelBuddy Response:**")
        print("```text")
        
        try:
            inputs = {"messages": [("human", test['input'])]}
            result = graph.invoke(inputs)
            
            final_message = result["messages"][-1]
            final_response = final_message.content
            
            # XỬ LÝ ĐẶC THÙ CỦA GEMINI: Nếu kết quả là List, bóc tách lấy 'text'
            if isinstance(final_response, list):
                text_parts = [block['text'] for block in final_response if isinstance(block, dict) and 'text' in block]
                final_response = "\n".join(text_parts)
                
            print("```")
            print(f"\n**TravelBuddy:**\n{final_response}\n")
            
        except Exception as e:
            print("```")
            print(f"\n**Lỗi trong quá trình chạy:** {e}\n")
            
        print("---\n")
        
        # Tạm dừng 15 giây sau mỗi test để tránh lỗi Rate Limit của API
        if index < len(test_cases) - 1:
            # sys.stderr giúp in ra Terminal để theo dõi, nhưng không lưu vào file test_results.md
            sys.stderr.write(f"⏳ Đang tạm dừng 15 giây chờ API phục hồi (Test {index+1}/{len(test_cases)})...\n")
            time.sleep(15)

if __name__ == "__main__":
    run_auto_tests()