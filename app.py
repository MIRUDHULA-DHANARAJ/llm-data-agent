import streamlit as st
import pandas as pd
from langchain_core.messages import HumanMessage
from agent import app

# Page configuration for a premium enterprise feel
st.set_page_config(
    page_title="InsightCore AI | Autonomous Analyst", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Enterprise Global CSS styling
st.markdown("""
    <style>
        /* Base app background tuning */
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        
        /* Metric Card styling */
        .metric-card {
            background-color: #1E293B;
            border: 1px solid #334155;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
        }
        .metric-label { font-size: 0.85rem; color: #94A3B8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
        .metric-value { font-size: 1.8rem; color: #F8FAFC; font-weight: 700; margin-top: 0.25rem; }
        
        /* Header typography adjustments */
        .main-title { font-size: 2.5rem; font-weight: 800; color: #F1F5F9; letter-spacing: -0.025em; margin-bottom: 0.5rem; }
        .sub-title { font-size: 1.1rem; color: #94A3B8; margin-bottom: 2rem; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTROL PANEL ---
with st.sidebar:
    st.markdown("<h2 style='color: #F1F5F9; font-size: 1.5rem; font-weight: 700;'>⚡ InsightCore Engine</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 0.85rem;'>Enterprise Multi-Agent Runtime Environment</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Live System Status Dashboard
    st.markdown("**Core Architecture Status:**")
    st.success("🟢 LLM Gateway: Connected")
    st.success("🟢 Graph Routing: Active")
    st.success("🟢 DB Sandbox: Isolated (Read-Only)")
    
    st.markdown("---")
    st.markdown("**⚡ Quick Prompt Templates:**")
    st.caption("Copy and paste these into the prompt analyzer:")
    st.info("• Give me a breakdown of total sales revenue per product category\n\n"
            "• Which city has the highest number of users?\n\n"
            "• What is our most expensive item and how many times was it purchased?")

# --- MAIN SCREEN INTERFACE ---
st.markdown("<h1 class='main-title'>⚡ InsightCore Autonomous Data Agent</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Translate complex enterprise natural language questions into deterministic SQL & execution logic trajectories instantly.</p>", unsafe_allow_html=True)

# High-Level Real-time System KPI Metrics Grid Panel
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div class='metric-card'><div class='metric-label'>Connected Store Layer</div><div class='metric-value'>SQLite Sandbox</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='metric-card'><div class='metric-label'>Inference Gateway</div><div class='metric-value'>Groq Cloud v3</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class='metric-card'><div class='metric-label'>Agent Loop Protocol</div><div class='metric-value'>LangGraph ReAct</div></div>", unsafe_allow_html=True)

# Clean, structured search panel layout
st.markdown("<h3 style='font-size: 1.25rem; font-weight: 600; color: #E2E8F0; margin-bottom: 0.5rem;'>🎯 Natural Language Query Analyzer</h3>", unsafe_allow_html=True)
user_query = st.text_input("Ask a question about your database", placeholder="e.g., Calculate total revenue metrics across all successful electronics transactions...", label_visibility="collapsed")

if user_query:
    st.markdown("---")
    # Modernized streaming visualization area splitting thought paths from the solution grid
    trace_col, display_col = st.columns([1, 1.2])
    
    with trace_col:
        st.markdown("<h4 style='font-size: 1.1rem; font-weight: 600; color: #94A3B8;'>🧠 Real-Time Compilation Trace</h4>", unsafe_allow_html=True)
        trace_placeholder = st.container()
        
    with display_col:
        st.markdown("<h4 style='font-size: 1.1rem; font-weight: 600; color: #94A3B8;'>🎯 Output Matrix & Visualizations</h4>", unsafe_allow_html=True)
        output_placeholder = st.container()

    with st.spinner("Processing execution trajectory..."):
        events = app.stream({"messages": [HumanMessage(content=user_query)]})
        last_sql_content = None

        for event in events:
            for node, output in event.items():
                
                # 1. Render execution step diagnostics into the Trace column
                if node == "tools":
                    for msg in output.get("messages", []):
                        with trace_placeholder.expander(f"🛠️ System Module Triggered: {msg.name}", expanded=True):
                            st.markdown("<p style='font-size:0.8rem; color:#94A3B8;'>RAW SYSTEM FRAME DATA:</p>", unsafe_allow_html=True)
                            st.code(msg.content, language="text")
                            
                        # Capture raw SQL tabular string outputs for extraction later
                        if msg.name == "run_sql_query" and "Error" not in msg.content and "returned no results" not in msg.content:
                            last_sql_content = msg.content
                                
                elif node == "agent":
                    for msg in output.get("messages", []):
                        if hasattr(msg, 'tool_calls') and msg.tool_calls:
                            for tool_call in msg.tool_calls:
                                t_name = tool_call.get('name')
                                t_args = tool_call.get('args', {})
                                
                                with trace_placeholder.expander(f"🧠 Routing Decision -> {t_name}", expanded=True):
                                    if 'query' in t_args:
                                        st.code(t_args['query'], language="sql")
                                    elif 'code' in t_args:
                                        st.code(t_args['code'], language="python")
                                        
                        # 2. Render final analytical compilation blocks into the Display column
                        elif msg.content:
                            with output_placeholder:
                                st.markdown("<div style='background-color: #064E3B; border: 1px solid #059669; padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
                                st.markdown("<h5 style='margin:0 0 0.5rem 0; color:#A7F3D0; font-size:1.1rem; font-weight:700;'>📝 System Insights Synthesis</h5>", unsafe_allow_html=True)
                                st.write(msg.content)
                                st.markdown("</div>", unsafe_allow_html=True)
                                
                                # --- UPGRADED AUTO-CHART DETECTOR ENGINE ---
                                if last_sql_content is not None:
                                    st.markdown("<div style='background-color: #0F172A; border: 1px solid #1E293B; padding: 1.5rem; border-radius: 12px;'>", unsafe_allow_html=True)
                                    st.markdown("<h5 style='margin:0 0 1rem 0; color:#F1F5F9; font-size:1rem; font-weight:600;'>📈 Interactive Analytical Chart View</h5>", unsafe_allow_html=True)
                                    try:
                                        from io import StringIO
                                        raw_string_data = StringIO(last_sql_content.strip())
                                        
                                        # Parse arbitrary white-space tabular layouts cleanly
                                        chart_df = pd.read_csv(raw_string_data, sep=r'\s{2,}', engine='python')
                                        
                                        if len(chart_df) >= 1 and len(chart_df.columns) >= 2:
                                            x_axis = chart_df.columns[0]
                                            y_axis = chart_df.columns[1]
                                            
                                            # Clean formatting string symbols and force numeric compliance
                                            chart_df[y_axis] = chart_df[y_axis].astype(str).str.replace(r'[^\d\.]', '', regex=True)
                                            chart_df[y_axis] = pd.to_numeric(chart_df[y_axis], errors='coerce')
                                            
                                            # Generate clean native chart component
                                            st.bar_chart(data=chart_df, x=x_axis, y=y_axis)
                                        else:
                                            st.info("Single metrics cell layout detected. Graphical matrix omitted.")
                                    except Exception as chart_err:
                                        st.info(f"Visual chart skipped: {str(chart_err)}")
                                    st.markdown("</div>", unsafe_allow_html=True)
