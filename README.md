# ⚡ Autonomous Text-to-SQL Agent

Ask questions about your database in plain English. The agent writes the SQL, checks it for safety, runs it, and fixes its own mistakes.

Built with **LangGraph**, **Groq**, **FastAPI**, **Streamlit** and **SQLite**.

---
#
Live Demo: [LLM AGENT APP](https://llm-data-agent-app.streamlit.app/)

## 🤔 Why this project?

Most people don't know SQL, so they depend on analysts to get answers from data. This agent lets anyone ask *"Which city has the most users?"* and get the answer instantly.

## ✨ Features

- **Natural language → SQL** using an LLM (Groq)
- **Safety guardrail**: every query is parsed with `sqlglot`, and anything other than `SELECT` (DROP, DELETE, UPDATE, INSERT, ALTER, TRUNCATE) is blocked
- **Self-healing loop**: if a query fails, the error is sent back to the LLM to fix (max 3 attempts)
- **Streamlit dashboard** with SQL trace, retry count, results table and auto bar chart
- **FastAPI endpoint** so other apps can use the agent

## 🧠 How it works

```
Question → generate SQL → validate (AST check) → execute → result
               ▲                 │ fail              │ error
               └─────────────────┴───────────────────┘
                          retry (max 3 times)
```

| Step | What it does |
|------|--------------|
| **generate** | LLM gets the DB schema + your question and writes a SQLite query |
| **validate** | `sqlglot` blocks anything that isn't a read-only SELECT |
| **execute** | Runs the query on SQLite and returns the rows |
| **retry** | On failure, LangGraph loops back to *generate* with the error |

## 🗂️ Project structure

```
├── app/
│   ├── database.py     # creates mock e-commerce DB + reads schema
│   ├── graph.py        # LangGraph workflow (generate → validate → execute)
│   ├── guardrails.py   # sqlglot safety check
│   ├── state.py        # shared agent state
│   └── main.py         # FastAPI app
├── streamlit_app.py    # Streamlit UI
├── requirements.txt
└── .env
```

## 🚀 Getting started

**1. Clone and install**

```bash
git clone https://github.com/MIRUDHULA-DHANARAJ/llm-data-agent.git
cd llm-data-agent
pip install -r requirements.txt
```

**2. Add your Groq API key**

Create a `.env` file:

```
GROQ_API_KEY=your_key_here
```

**3. Run the Streamlit app**

```bash
streamlit run streamlit_app.py
```

**4. Or run the API**

```bash
uvicorn app.main:app --reload
```

Then open `http://localhost:8000/docs` to try it.

## 📡 API

**POST** `/query`

```json
{ "query": "Total sales revenue per product category" }
```

Returns the generated SQL, results, retry count and any errors. There's also a `GET /health` check.

## 🗃️ Sample data

On first run, a mock e-commerce database is created automatically:

- `users` (50 rows)
- `orders` (120 rows)
- `order_items` (products, categories, prices, quantities)

## 💬 Try these questions

- Give me total sales revenue per product category
- Which city has the highest number of registered users?
- What are the top 3 most expensive products sold?



## 🛠️ Tech stack

LangGraph · LangChain · Groq · FastAPI · Streamlit · SQLite · pandas · sqlglot

---

Made by **Mirudhula D**
