# ⚡ InsightCore AI: Autonomous Data Analyst Agent
An enterprise-grade, multi-agent analytical system that translates natural language business queries into deterministic SQL and Python code execution loops over relational databases.

[![Live App Gateway](https://shields.io)](https://llm-data-agent.onrender.com/)
![Python](https://shields.io)
![LangGraph](https://shields.io)
![Groq](https://shields.io)
![Streamlit](https://shields.io)
![Docker](https://shields.io)
![SQLite](https://shields.io)

---

## 💡 The Business Problem It Solves
In traditional enterprises, non-technical stakeholders (Sales, Marketing, Operations) face severe bottlenecks when requesting simple data reports. They open Jira tickets, waiting days for data analysts to write custom SQL scripts, extract metrics into Excel, and plot trends. 

**InsightCore AI completely eliminates this bottleneck.** It enables real-time data access using natural English. Non-technical users ask questions, and the agent autonomously reasons, constructs schemas, queries the target layer, handles math dependencies via an isolated execution sandbox, and renders dynamic chart panels.

---

## ⚙️ Core Architecture Blueprint
Unlike legacy linear chains that break during minor runtime anomalies, this architecture runs on a stateful execution loop utilizing **LangGraph**:

```text
       [ User Prompt Input ]
                │
                ▼
       ┌─────────────────┐
       │   Agent Node    │◀──────────────────┐
       │  (Reasoning)    │                   │
       └─────────────────┘                   │
                │                            │
      [ Evaluates Next Step ]                │
                │                            │
                ▼                            │
      (Conditional Router)                   │ (Self-Correction Loop)
        /       │         \                  │
       /        │          \                 │
      ▼         ▼           ▼                │
┌──────────┐┌──────────┐┌───────────┐        │
│  Schema  ││ SQL Tool ││  Python   │        │
│ Fetcher  ││ (Query)  ││ Sandbox   │        │
└──────────┘└──────────┘└───────────┘        │
      │         │           │                │
      └─────────┴───────────┴────────────────┘
            [ Intercepts Output / Errors ]
```

1. **The Reasoning Node (LLM Brain):** `llama-3.3-70b-versatile` running via Groq Developer API (zero-latency structured JSON tool-calling).
2. **Orchestrator Logic (LangGraph):** Manages shared application memory state variables dynamically across tasks.
3. **The Self-Correcting Execution Route:** If a database query fails due to a structural constraint, the router captures the raw traceback log error, pushes it back into the LLM context, and forces an autonomous rewrite.

---

## 🛠️ Technical Stack
* **Orchestration Framework:** LangGraph Framework (State Machines) & LangChain Core
* **Inference Pipeline Engine:** Groq Cloud Systems (`llama-3.3-70b-versatile`)
* **Relational Layer Database:** SQLite Store (3-table mock Indian e-commerce data footprint: `users`, `orders`, `order_items`)
* **Frontend Analytics Deck:** Streamlit UI Ecosystem + Custom CSS Embedded Grid Paneling
* **Container Environment:** Docker Microservices Runtime Isolation Engine

---

## 🔒 Enterprise Production Guardrails
* **Deterministic Security Filters:** Hardcoded lexical parsers scan every generated SQL string block to detect and abort data modification hooks (`DROP`, `DELETE`, `ALTER`, `INSERT`), preventing malicious structural mutations.
* **Isoruntime Code Sandboxing:** Captures `sys.stdout` streams dynamically using isolated contextual execution dictionaries to keep runtime calculations sandboxed from parent server nodes.
* **Dynamic Content Alignment:** Standardizes arbitrary space-separated string matrices into compliant Pandas arrays automatically to guarantee robust front-end chart components.

---

## 🚀 Step-by-Step Local Deployment Installation

### 1. Pre-requisites & Local Variables Configuration
Clone the repository path and set your authenticated API secret:
```bash
git clone https://github.com
cd llm-data-agent

# Set temporary terminal environment key
export GROQ_API_KEY="gsk_your_actual_key_here"
```

### 2. Standalone Native Script Execution
Build your package management architecture and run the web visualization platform:
```bash
# Create and turn on Python Environment 
python -m venv venv
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate

# Setup Python packages
pip install -r requirements.txt

# Create relational data store structures
python setup_db.py

# Launch web server instance 
streamlit run app.py
```

### 3. Containerized Isolation Build (Docker Implementation)
To test container performance locally using your portable Docker microservice file layers:
```bash
# Build the container target file tracking
docker build -t insightcore-agent .

# Boot the isolated local docker image instance
docker run -p 8501:8501 -e GROQ_API_KEY="gsk_your_actual_key_here" insightcore-agent
```
