from agent import app
from langchain_core.messages import HumanMessage

def test():
    user_query = "Which city has the highest number of users, and what is the total number of orders placed from there?"
    print(f"🚀 Prompt: {user_query}\n")
    
    # Stream the operational trace steps
    for chunk in app.stream({"messages": [HumanMessage(content=user_query)]}):
        for node, output in chunk.items():
            print(f"--- Node Executed: {node} ---")
            for msg in output.get("messages", []):
                if msg.content:
                    print(f"Content:\n{msg.content}\n")
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    print(f"Tool Calls Request: {msg.tool_calls}\n")

if __name__ == "__main__":
    test()
