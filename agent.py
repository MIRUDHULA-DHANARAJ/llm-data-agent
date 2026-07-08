import os
from typing import TypedDict, Annotated, Sequence
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from db_tools import get_db_schema, run_sql_query, python_sandbox

# Initialize the model
llm = ChatGroq(
    model="llama-3.3-70b-versatile", 
    temperature=0.0,
    groq_api_key=os.environ.get("GROQ_API_KEY")
)

# Bind the tools
tools = [get_db_schema, run_sql_query, python_sandbox]
llm_with_tools = llm.bind_tools(tools)



# 2. Define the shared Agent State structure
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], lambda x, y: x + y]

# 3. Define Node: Call the LLM Agent
def call_model(state: AgentState):
    messages = state['messages']
    
    # Inject a strict system prompt if it's the beginning of the conversation
    if not any(isinstance(m, SystemMessage) for m in messages):
        system_prompt = SystemMessage(content=(
            "You are an expert data analyst AI agent. You have access to an e-commerce database.\n"
            "Step 1: ALWAYS call 'get_db_schema' first to understand table fields and structures.\n"
            "Step 2: Formulate valid SQL queries based on table names. Only use 'run_sql_query'.\n"
            "Step 3: If you need data manipulation, math, or calculations, pass the data string to 'python_sandbox'.\n"
            "Step 4: Present your final answer clearly to the user with a breakdown of your steps."
        ))
        messages = [system_prompt] + list(messages)
        
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# 4. Define Router Logic: Check if tools are needed or if we should stop
def should_continue(state: AgentState):
    last_message = state['messages'][-1]
    # If the LLM didn't request any tool calls, exit the graph loop
    if not last_message.tool_calls:
        return "end"
    return "continue"

# 5. Build the Workflow Execution Graph
workflow = StateGraph(AgentState)

# Define our two functional nodes
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))

# Set the starting processing node
workflow.set_entry_point("agent")

# Add conditional execution routes
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "tools",
        "end": END
    }
)

# Add a normal return loop back to the LLM after tools execute
workflow.add_edge("tools", "agent")

# Compile the workflow into a runnable asset
app = workflow.compile()
