from fastapi import FastAPI, HTTPException
from httpx2 import get, post
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from langchain_core.messages import HumanMessage

from app.graph import app as workflow_app
from app.database import init_db

# Initialize FastAPI application
app = FastAPI(
    title="Autonomous SQL Agent API",
    description="Production-grade Text-to-SQL microservice with LangGraph self-healing loop and AST safety guardrails.",
    version="1.0.0"
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    user_query: str
    sql_query: Optional[str] = None
    validation_passed: bool
    validation_error: Optional[str] = None
    execution_result: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
    retry_count: int

@post("/query", response_model=QueryResponse)
def run_agent_query(request: QueryRequest):
    """Executes the natural language query through the LangGraph self-healing agent pipeline."""
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    
    initial_state = {
        "user_query": request.query,
        "sql_query": None,
        "validation_passed": True,
        "validation_error": None,
        "execution_result": None,
        "error": None,
        "retry_count": 0
    }

    try:
        # Invoke the compiled LangGraph workflow
        final_state = workflow_app.invoke(initial_state)
        
        return QueryResponse(
            user_query=final_state.get("user_query", request.query),
            sql_query=final_state.get("sql_query"),
            validation_passed=final_state.get("validation_passed", True),
            validation_error=final_state.get("validation_error"),
            execution_result=final_state.get("execution_result"),
            error=final_state.get("error"),
            retry_count=final_state.get("retry_count", 0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent Execution Failure: {str(e)}")

@get("/health")
def health_check():
    return {"status": "healthy", "service": "Autonomous SQL Agent"}