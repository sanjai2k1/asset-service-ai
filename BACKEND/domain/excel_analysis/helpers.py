import pandas as pd
import duckdb
from core.utils import IDGenerator
import os
from config.settings import settings
from .state import StateInfo,ContextInfo,QueryOutputResponse
UPLOAD_FOLDER = settings.excel_uploaded_dir

def build_column_index(context: ContextInfo) -> dict:
    df = context.processed_df

    if df is None:
        return {"error": "No data loaded"}

    column_value_map = {}

    for col in df.columns:
        series = df[col].dropna()

        # Skip empty
        if len(series) == 0:
            continue

        # Convert to string safely
        series_str = series.astype(str).str.strip()
        unique_vals = series_str.unique()

        # 🔍 Basic cleaning
        clean_vals = [
            v for v in unique_vals
            if len(v) < 30 and v.lower() not in ["nan", "none", ""]
        ]

        if len(clean_vals) < 2:
            continue

        # ✅ Your new logic
        if len(clean_vals) < 20:
            column_value_map[col] = clean_vals
        else:
            column_value_map[col] = clean_vals[:10]

    return column_value_map




def create_duckdb_for_request(state: StateInfo, df):

    if state.db_path is None:
        db_dir = f"{UPLOAD_FOLDER}/{state.thread_id}"
        os.makedirs(db_dir, exist_ok=True)

        db_path = f"{db_dir}/{IDGenerator.generate_uuid()}.duckdb"

        conn = duckdb.connect(db_path)

        table = state.table_name.replace('"', '')  # safety

        # ✅ Register using table_name
        conn.register(table, df)

        # ✅ Use same name in SQL
        conn.execute(f"""
            CREATE OR REPLACE TABLE {table} AS 
            SELECT * FROM {table}
        """)

        conn.close()

        state.db_path = db_path

    return state




def get_paged_results(context : QueryOutputResponse,  page_size: int = 50, page_number: int = 1) -> str:
    """
    Executes a paginated SQL query.
    - table_name: The name of the registered DuckDB table.
    - sql_query: The base query (e.g., 'SELECT * FROM assets').
    - page_size: Records per page.
    - page_number: Which page to fetch (starts at 1).
    """
    try:
        db_path = context.db_path

        if not db_path:
            return "SQL Error: Database not initialized"

        # ✅ Open connection from file path
        con = duckdb.connect(db_path)
        
        # 1. Calculate offset
        offset = (page_number - 1) * page_size
        
        # 2. Build the paginated query
        # This keeps the logic inside the database engine
        paged_query = context.sql_query

        
        # 3. Execute
        results = con.execute(paged_query).fetchall()
        
        if not results:
            return "No records found for this page."
            
        # 4. Format as a clean string for the console
        output = [str(row) for row in results]
        
        return f"PAGE {page_number} (Records {offset+1} to {offset+len(results)}):\n" + "\n".join(output)
        
    except Exception as e:
        return f"SQL Error: {str(e)}"
