import sqlglot
from sqlglot import exp
from typing import Annotated, Any, Dict, List, Optional, TypedDict


def validate_sql_safety(sql_query: str) -> tuple[bool, Optional[str]]:
  """Inspects the SQL abstract syntax tree (AST) to block destructive

  operations (DROP, DELETE, UPDATE, ALTER, INSERT, TRUNCATE).
  """
  if not sql_query or not sql_query.strip():
    return False, "Generated SQL query is empty."

  try:
    # Parse the SQL string into an AST using sqlglot 
    parsed_statements = sqlglot.parse(sql_query, read="sqlite")

    if not parsed_statements:
      return False, "Could not parse SQL query."

    # Forbidden expression types that alter or destroy data/schema
    forbidden_types = (
        exp.Drop,
        exp.Delete,
        exp.Update,
        exp.Alter,
        exp.Insert,
        exp.TruncateTable,)

    for statement in parsed_statements:
      # Check if any node in the AST matches our forbidden operations
      if isinstance(statement, forbidden_types):
        return (False,
            f"Security Violation: Destructive operation '{type(statement).__name__}' is strictly prohibited.",
        )

      # Extra safety: ensure it's primarily a SELECT or Read operation
      if not isinstance(statement, (exp.Select, exp.Union)):
        return (False,"Security Violation: Only SELECT queries are permitted.",)

    return True, None

  except Exception as e:
    return (False,f"SQL Parse Error: Malformed query syntax ({str(e)}).",)