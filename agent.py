import os
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from tools import search_flights, search_hotels, calculate_budget
from dotenv import load_dotenv

load_dotenv()

# 1. Đọc System Prompt
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# 2. Khai báo State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 3. Khởi tạo LLM và Tools
tools_list = [search_flights, search_hotels, calculate_budget]
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
llm_with_tools = llm.bind_tools(tools_list)

# 4. Agent Node
def agent_node(state: AgentState):
    messages = state["messages"]
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    response = llm_with_tools.invoke(messages)

    # === LOGGING ĐỂ CHỨNG MINH ĐIỂM SỐ ===
    if response.tool_calls:
        print("\n[HỆ THỐNG] Agent đang thực hiện chuỗi công cụ (Chaining):")
        for tc in response.tool_calls:
            print(f" ⚙️ Gọi tool: {tc['name']} | Tham số: {tc['args']}")
    else:
        print("\n[HỆ THỐNG] Agent trả lời trực tiếp.")

    return {"messages": [response]}

# 5. Xây dựng Graph
builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)

tool_node = ToolNode(tools_list)
builder.add_node("tools", tool_node)

# --- KHAI BÁO EDGES CHUẨN ---
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

graph = builder.compile()

# 6. Chat loop
if __name__ == "__main__":
    print("=" * 60)
    print("TravelBuddy (Powered by Gemini)")
    print("Gõ 'quit' để thoát")
    print("=" * 60)

    while True:
        user_input = input("\nBạn: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            break

        print("TravelBuddy đang suy nghĩ...", end="")
        result = graph.invoke({"messages": [("human", user_input)]})
        final_message = result["messages"][-1]
        final_content = final_message.content
        
        # Xử lý bóc tách text 
        if isinstance(final_content, list):
            text_parts = [block['text'] for block in final_content if isinstance(block, dict) and 'text' in block]
            final_content = "\n".join(text_parts)
            
        print(f"\nTravelBuddy:\n{final_content}")