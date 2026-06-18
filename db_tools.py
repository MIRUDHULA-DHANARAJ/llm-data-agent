import sqlite3
import pandas as pd
import sys
from io import StringIO
from langchain_core.tools import tool

DB_NAME = "ecommerce.db"

@tool
def get_db_schema() -> str:
    """Useful to fetch the schema of the database tables. Always run this before writing SQL queries."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    schema_info = []
    for table_name in tables:
        t_name = table_name[0]
        cursor.execute(f"PRAGMA table_info({t_name});")
        columns = cursor.fetchall()
        col_details = ", ".join([f"{col[1]} ({col[2]})" for col in columns])
        schema_info.append(f"Table: {t_name} -> Columns: {col_details}")
        
    conn.close()
    return "\n".join(schema_info)

@tool
def run_sql_query(query: str) -> str:
    """Executes a read-only SQL query on the SQLite database and returns the result as a string dataframe."""
    conn = sqlite3.connect(DB_NAME)
    try:
        forbidden_keywords = ["delete", "drop", "update", "insert", "alter"]
        if any(keyword in query.lower() for keyword in forbidden_keywords):
            return "Error: Data modification queries are strictly prohibited."
            
        df = pd.read_sql_query(query, conn)
        conn.close()
        if df.empty:
            return "Query returned no results."
        return df.to_string(index=False)
    except Exception as e:
        conn.close()
        return f"SQL Error: {str(e)}"

@tool
def python_sandbox(code: str) -> str:
    """Executes clean Python code for data processing and math. Captures standard output and returns it."""
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    local_vars = {"pd": pd}
    try:
        exec(code, {"__builtins__": __import__('builtins')}, local_vars)
        sys.stdout = old_stdout
        output = redirected_output.getvalue()
        return output if output.strip() else "Code executed successfully with no output."
    except Exception as e:
        sys.stdout = old_stdout
        return f"Python Execution Error: {str(e)}"
