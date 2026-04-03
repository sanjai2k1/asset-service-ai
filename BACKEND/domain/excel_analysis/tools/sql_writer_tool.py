from agents import function_tool, RunContextWrapper
import pandas as pd
from ..state import SqlWriterContext
import duckdb


@function_tool
def query_excel_sql(context: RunContextWrapper[SqlWriterContext], sql_query: str) -> str:
    """Executes SQL against the dynamic table name stored in context."""
    try:
        t_name = context.context.table_name

        # Assuming 'con' is your persistent DuckDB connection
        # and 't_name' is the string name of your table
        db_path = context.context.db_path

        if not db_path:
            return "SQL Error: Database not initialized"

        # ✅ Open connection from file path
        con = duckdb.connect(db_path)

        
        result_proxy = con.execute(sql_query)
        
        # 2. Get the count of rows returned by this specific query
        # Fetching all results into memory to count them
        results = result_proxy.fetchall()
        count = len(results)
        
        # 3. Store the RAW query for your 'fetch_records' function to use later
        
        # 4. Return only the count to the LLM
        return f"SUCCESS: Query executed. Total records found: {count}. sql_query : {sql_query}"
    except Exception as e:
        print(str(e))
        return f"SQL Error: {str(e)}"


@function_tool
def query_with_intelligent_output(
    context: RunContextWrapper[SqlWriterContext], 
    sql_query: str,
    page_size: int = 50,
    page_number: int = 1
) -> str:
    """
    Executes SQL and returns:
    - Full data + analysis if small (<=50 rows)
    - Paginated data if large (>50 rows)
    """
    try:
        t_name = context.context.table_name
        db_path = context.context.db_path

        if not db_path:
            return "SQL Error: Database not initialized"

        # ✅ Open connection from file path
        con = duckdb.connect(db_path)

        # 👉 Get total count (efficient)
        count_query = f"SELECT COUNT(*) FROM ({sql_query}) t"
        total_count = con.execute(count_query).fetchone()[0]

        # 👉 CASE 1: SMALL RESULT
        if total_count <= 50:
            result = con.execute(sql_query).fetchall()
            columns = [desc[0] for desc in con.description]
            rows = [dict(zip(columns, r)) for r in result]

            formatted = "\n".join([str(r) for r in rows])

            return f"""
SUCCESS_SMALL_RESULT:
Total Rows: {total_count}

DATA:
{formatted}

INSTRUCTION:
Provide a short, human-friendly analysis of this data.
"""

        # 👉 CASE 2: LARGE RESULT → PAGINATION
        else:
            offset = (page_number - 1) * page_size

            paginated_query = f"""
            SELECT * FROM ({sql_query}) t
            LIMIT {page_size} OFFSET {offset}
            """
            context.context.is_paginated = True
            result = con.execute(paginated_query).fetchall()
            columns = [desc[0] for desc in con.description]
            rows = [dict(zip(columns, r)) for r in result]

            formatted = "\n".join([str(r) for r in rows])

            total_pages = (total_count + page_size - 1) // page_size

            return f"""
SUCCESS_LARGE_RESULT:
Total Rows: {total_count}
Page: {page_number} of {total_pages}

DATA:
{formatted}

INSTRUCTION:
Do NOT analyze.
Tell user:
- Showing page {page_number}

"""

    except Exception as e:
        return f"SQL Error: {str(e)}"
