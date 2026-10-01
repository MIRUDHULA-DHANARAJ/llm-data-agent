import os
import streamlit as st
import pandas as pd
from langchain_core.messages import HumanMessage

from app.graph import app as workflow_app
from app.database import init_db

# Page configuration for a professional enterprise feel
st.set_page_config(
    page_title="Autonomous SQL Agent | LangGraph",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database on app load
init_db()

# Custom CSS for high-contrast dark theme styling
st.markdown("""
    <style>
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        .metric-card {
            background-color: #1E293B;
            border: 1px solid #334155;
            padding: 1.2rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        .metric-label { font-size: 0.8rem; color: #94A3B8; font-weight: 600; text-transform: uppercase; }
        .metric-value { font-size: 1.5rem; color: #F8FAFC; font-weight: 700; margin-top: 0.2rem; }
        .main-title { font-size: 2.2rem; font-weight: 800; color: #F1F5F9; letter-spacing: -0.02em; }
        .sub-title { font-size: 1rem; color: #94A3B8; margin-bottom: 1.5rem; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTROL PANEL ---
with st.sidebar:
    st.markdown("<h2 style='color: #F1F5F9; font-size: 1.4rem;'>⚡ Agent Control Panel</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 0.8rem;'>LangGraph + Groq Llama 3.3 70B</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("**System Health:**")
    st.success("🟢 Groq LLM Gateway: Online")
    st.success("🟢 AST Guardrail: Active")
    st.success("🟢 SQLite Sandbox: Connected")
    
    st.markdown("---")
    st.markdown("**💡 Quick Prompt Examples:**")
    st.info(
        "• Give me total sales revenue per product category\n\n"
        "• Which city has the highest number of registered users?\n\n"
        "• What are the top 3 most expensive products sold?"
    )

# --- MAIN INTERFACE ---
st.markdown("<h1 class='main-title'>⚡ Autonomous Agentic AI & LLM Core Framework</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Translate natural language into secure, self-healing SQLite queries with real-time AST validation and Groq inference.</p>", unsafe_allow_html=True)

# KPI Metrics Row
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div class='metric-card'><div class='metric-label'>Inference Engine</div><div class='metric-value'>Llama 3.3 70B</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='metric-card'><div class='metric-label'>Security Guardrail</div><div class='metric-value'>sqlglot AST</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class='metric-card'><div class='metric-label'>Error Correction</div><div class='metric-value'>Self-Healing Loop</div></div>", unsafe_allow_html=True)

# Query Input
st.markdown("### 🎯 Natural Language Query Analyzer")
user_query = st.text_input("Ask a question about your database:", placeholder="e.g., Show me all orders placed by users from Mumbai...")

if user_query:
    st.markdown("---")
    
    # Two-column layout: Left for agent trace, Right for final output & tables
    trace_col, result_col = st.columns([1, 1.2])

    with trace_col:
        st.markdown("#### 🧠 Execution & Self-Healing Trace")
        trace_container = st.container()

    with result_col:
        st.markdown("#### 📊 Query Results & Data Matrix")
        result_container = st.container()

    with st.spinner("Running autonomous agent loop..."):
        initial_state = {
            "user_query": user_query,
            "sql_query": None,
            "validation_passed": True,
            "validation_error": None,
            "execution_result": None,
            "error": None,
            "retry_count": 0
        }

        # Invoke the LangGraph workflow directly
        final_state = workflow_app.invoke(initial_state)

        # Render Trace Log
        with trace_container:
            st.code(f"Generated SQL:\n{final_state.get('sql_query')}", language="sql")
            st.metric("Self-Healing Retries", final_state.get('retry_count', 0))
            
            if final_state.get('validation_error'):
                st.error(f"Validation Error Blocked: {final_state['validation_error']}")
            if final_state.get('error'):
                st.warning(f"Runtime Exception Handled: {final_state['error']}")

        # Render Results Data Grid
        with result_container:
            exec_res = final_state.get("execution_result")
            if exec_res and isinstance(exec_res, list) and len(exec_res) > 0:
                df = pd.DataFrame(exec_res)
                st.dataframe(df, use_container_width=True)
                
                # Auto-chart if numeric columns exist
                if len(df.columns) >= 2 and len(df) > 1:
                    try:
                        x_col, y_col = df.columns[0], df.columns[1]
                        df[y_col] = pd.to_numeric(df[y_col], errors='coerce')
                        if df[y_col].notnull().all():
                            st.bar_chart(df.set_index(x_col)[y_col])
                    except Exception:
                        pass
            else:
                st.info("Query returned no records or execution failed.")