import os
import sqlite3
import pandas as pd

from typing import Literal
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END

from app.database import DB_NAME, get_db_schema
from app.guardrails import validate_sql_safety
from app.state import AgentState

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app.database import DB_NAME, get_db_schema
from langchain_groq import ChatGroq
# 1. Initialize Groq LLM

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.0,
    groq_api_key=os.environ.get("GROQ_API_KEY")
)


# 2. Generate SQL

def generate_sql_node(state: AgentState):

    question = state["user_query"]
    error = state.get("error")
    failed_sql = state.get("sql_query")
    retry_count = state.get("retry_count", 0)

    schema = get_db_schema()

    system_prompt = """
    You are an expert SQL assistant.
    Generate only valid SQLite SELECT queries.
    Use only the tables and columns provided in the schema.
    Never generate INSERT, UPDATE, DELETE, or DROP statements.
    Return only the SQL query.
    """

    human_prompt = f"""
    Database schema:
    {schema}

    User question:
    {question}
    """

    if error:
        human_prompt += f"""
        Previous SQL:
        {failed_sql}

        Error:
        {error}

        Please correct the SQL query.
        """

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]

    response = llm.invoke(messages)

    content = response.content

    # Clean Markdown formatting if present
    sql_query = content.strip()
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    return {
        "sql_query": sql_query,
        "retry_count": retry_count + 1,
        "error": None
    }


# 3. Validate SQL

def validate_sql_node(state: AgentState):

    sql = state["sql_query"]

    is_valid, error = validate_sql_safety(sql)

    return {
        "validation_passed": is_valid,
        "validation_error": error
    }


# 4. Execute SQL

def execute_sql_node(state: AgentState):

    sql = state["sql_query"]

    try:
        connection = sqlite3.connect(DB_NAME)

        df = pd.read_sql_query(sql, connection)

        result = df.to_dict(orient="records")

        return {
            "execution_result": result,
            "error": None
        }

    except Exception as e:

        return {
            "execution_result": None,
            "error": str(e)
        }

    finally:
        if "connection" in locals():
            connection.close()


# 5. Route after validation

def route_after_validation(state: AgentState) -> Literal["execute", "retry", "end"]:

    if state.get("validation_passed"):
        return "execute"

    if state.get("retry_count", 0) < 3:
        return "retry"

    return "end"


# 6. Route after execution

def should_retry_or_end(state: AgentState) -> Literal["retry", "end"]:

    if state.get("error") and state.get("retry_count", 0) < 3:
        return "retry"

    return "end"


# 7. Build LangGraph workflow

workflow = StateGraph(AgentState)

# Register nodes
workflow.add_node("generate", generate_sql_node)
workflow.add_node("validate", validate_sql_node)
workflow.add_node("execute", execute_sql_node)

# Set starting node
workflow.set_entry_point("generate")

# Connect generation to validation
workflow.add_edge("generate", "validate")

# Route after validation
workflow.add_conditional_edges(
    "validate",
    route_after_validation,
    {
        "execute": "execute",
        "retry": "generate",
        "end": END
    }
)

# Route after execution
workflow.add_conditional_edges(
    "execute",
    should_retry_or_end,
    {
        "retry": "generate",
        "end": END
    }
)

# Compile workflow
app = workflow.compile()


# 8. Run the agent

def run_agent(question: str):

    result = app.invoke({
        "user_query": question,
        "sql_query": "",
        "validation_passed": False,
        "validation_error": None,
        "execution_result": None,
        "error": None,
        "retry_count": 0
    })

    return result