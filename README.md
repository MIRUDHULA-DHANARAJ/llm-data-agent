# InsightCore AI — Autonomous Data Analyst Agent

An AI agent that answers natural language questions about a database by autonomously writing and executing SQL queries, running Python calculations, and rendering results with charts — no manual query writing needed.

**Live demo:** [llm-data-agent.onrender.com](https://llm-data-agent.onrender.com)
> ⚠️ Hosted on Render free tier — first load may take 30–60 seconds to wake up.

---

## What it does

You type a question in plain English. The agent figures out how to answer it by:

1. Inspecting the database schema to understand what tables and columns exist
2. Writing and executing a SQL query to retrieve the relevant data
3. Running Python calculations if further processing is needed
4. Returning a clear answer with an auto-generated bar chart where applicable

The agent's full reasoning trace — every tool call, every SQL query it wrote, every decision — is visible in the UI alongside the final answer.

**Example questions you can ask:**
- *Which city has the highest number of users?*
- *What is the total revenue per product category?*
- *Which product was purchased the most times?*
- *What is the average order value across all transactions?*

---

## Architecture

The agent is built on a **LangGraph stateful execution graph** — not a simple linear chain. This means it can loop back, self-correct on SQL errors, and handle multi-step reasoning without breaking.

```
[ User Question ]
       │
       ▼
 ┌───────────┐
 │ Agent     │ ◀─────────────────────┐
 │ (LLM)    │                       │
 └───────────┘                       │  (self-correction loop)
       │                             │
  tool needed?                       │
    /      \                         │
  yes       no → return answer       │
   │                                 │
   ▼                                 │
┌──────────────────────────────┐     │
│  Tool Node                   │─────┘
│  ├── get_db_schema()         │
│  ├── run_sql_query()         │
│  └── python_sandbox()        │
└──────────────────────────────┘
```

The agent always calls `get_db_schema` first, then writes SQL based on actual column names — preventing hallucinated column errors. If a query fails, the error is fed back into the LLM context and the agent rewrites the query automatically.

---

## Tech stack

| Layer | Technology |
|---|---|
| Agent framework | LangGraph + LangChain Core |
| LLM | Groq Cloud — `llama-3.3-70b-versatile` (free tier) |
| Tools | Custom `@tool` functions: schema inspector, SQL executor, Python sandbox |
| Database | SQLite — mock Indian e-commerce data (users, orders, order_items) |
| Frontend | Streamlit — live reasoning trace + auto bar chart |
| Deployment | Docker + Render |

---

## Database schema

Three tables modelling an Indian e-commerce store:

- **users** — user_id, name, city, signup_date
- **orders** — order_id, user_id, product, category, amount, status, order_date
- **order_items** — item_id, order_id, product_name, quantity, unit_price

---

## Tools

**`get_db_schema()`** — returns table names, column names, and types. The agent calls this first on every query before writing any SQL.

**`run_sql_query(query)`** — executes a read-only SQL query against the SQLite database. Blocks any query containing `DELETE`, `DROP`, `UPDATE`, `INSERT`, or `ALTER` before execution.

**`python_sandbox(code)`** — runs Python code with pandas available for calculations that SQL can't handle cleanly (e.g. percentage calculations, multi-step aggregations). Stdout is captured and returned to the agent.

---

## Run locally

**Prerequisites:** Python 3.11+, a free [Groq API key](https://console.groq.com)

```bash
git clone https://github.com/MIRUDHULA-DHANARAJ/llm-data-agent
cd llm-data-agent

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

python setup_db.py              # creates ecommerce.db with sample data

export GROQ_API_KEY=gsk_...     # Windows: set GROQ_API_KEY=gsk_...

streamlit run app.py
```

**With Docker:**

```bash
docker build -t insightcore-agent .
docker run -p 8501:8501 -e GROQ_API_KEY=gsk_... insightcore-agent
# open http://localhost:8501
```

---

## Project structure

```
llm-data-agent/
├── agent.py          # LangGraph state machine — agent node, tool node, routing logic
├── db_tools.py       # Three LangChain tools: schema, SQL, Python sandbox
├── app.py            # Streamlit UI — query input, reasoning trace, chart output
├── setup_db.py       # Creates and seeds ecommerce.db
├── ecommerce.db      # SQLite database
├── Dockerfile
└── requirements.txt
```

---

## Key design decisions

**Why LangGraph instead of AgentExecutor?** LangGraph gives explicit control over the execution loop as a typed state machine. The self-correction behaviour (SQL error → rewrite → retry) is a real conditional edge in the graph, not a hidden retry inside a black-box executor.

**Why Groq?** Sub-second inference on `llama-3.3-70b-versatile` at zero cost on the free tier. The 70B model handles structured tool-calling reliably enough for production-quality SQL generation.

**Why block write queries in the tool, not in the prompt?** Prompt-level restrictions can be overridden by a sufficiently persistent user. Blocking at the tool level in Python is deterministic — no query containing those keywords will ever execute regardless of what the LLM decides.

---

## Built by

**Mirudhula D** — AI & Data Science

[LinkedIn](https://linkedin.com/in/mirudhula-dhanaraj) · [GitHub](https://github.com/MIRUDHULA-DHANARAJ) · [Email](mailto:mirudhula.d534@gmail.com)
