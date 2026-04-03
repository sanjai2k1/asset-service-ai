from agents import function_tool, RunContextWrapper
import pandas as pd
from ..state import ContextInfo


def is_mostly_numeric(series, threshold=0.7):
    numeric_count = series.apply(lambda x: pd.to_numeric(x, errors='coerce')).notna().sum()
    return numeric_count / len(series) > threshold
def extract_real_table(file_path, sheet_name=0):
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

    # Step 1: Drop fully empty rows/cols
    df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)

    # Step 2: Shift all values LEFT (critical fix)
    if df.isna().mean().mean() > 0.4:
        df = df.apply(lambda row: pd.Series(row.dropna().values), axis=1)
    # Step 3: Drop again (after shift)
    df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)

    # Step 4: Find header row (row with max non-null values)
    header_idx = df.notna().sum(axis=1).idxmax()

    # Step 5: Set header
    df.columns = df.iloc[header_idx]
    df = df[(header_idx + 1):].reset_index(drop=True)

    # Step 6: Final cleanup
    df = df.dropna(how='all')

    return df, header_idx



def clean_dynamic(df, min_non_null_ratio=0.5):
    """
    Dynamically removes non-data rows like totals, summaries, merged rows.

    Args:
        df: DataFrame
        min_non_null_ratio: minimum % of filled cells required to keep row

    Returns:
        Cleaned DataFrame
    """

    total_cols = df.shape[1]

    # 1. Remove rows with too many NaNs
    non_null_counts = df.notna().sum(axis=1)
    df = df[non_null_counts >= (total_cols * min_non_null_ratio)]

    # 2. Remove rows where first column is not numeric (Sl.No logic)
    def is_number(x):
        try:
            float(x)
            return True
        except:
            return False

    if is_mostly_numeric(df.iloc[:, 0]):
        df = df[df.iloc[:, 0].apply(lambda x: pd.to_numeric(x, errors='coerce')).notna()]
    # 3. Reset index
    return df.reset_index(drop=True)
# # ---- Usage ----
# table = extract_real_table("Rpt_WorkOrder_Scheduled_L2_List.xlsx")
# table = clean_dynamic(table)
# print(table.head())
# print(table.tail(20))   # last 20 rows
# print("Shape:", table.shape)



@function_tool
def analyze_and_load_excel(context: RunContextWrapper[ContextInfo]) -> str:
    """
    Dynamically finds the 'Sl.No.' anchor and loads the data into a clean DataFrame.
    """
    try:
        # Load the file
        context.context.excel_file.seek(0)
        # Step 1: Scan first 50 rows for the anchor 'Sl.No.'
        table, header_idx = extract_real_table(context.context.excel_file)
        df = clean_dynamic(table)
        print(f"--- DEBUG: Anchor 'Sl.No.' found at row {header_idx + 1} ---")

        # Step 3: Clean 'ghost' cells (empty rows/cols)
        df = df.dropna(how='all').dropna(axis=1, how='all')
        df.columns = (
    df.columns
    .str.strip()          # remove trailing spaces
    .str.lower()          # lowercase
    .str.replace(" ", "_")  # snake_case
)
        context.context.processed_df = df
        # Generate summary for LLM
        return f"""
        CLEAN TABLE DETECTED:
        - Anchor Row: {header_idx + 1}
        - Total Records: {len(df)}
        - Important Columns: {list(df.columns[:10])}...
        
        SAMPLE DATA:
        {df.head(5).to_string(index=False)}
        """

    except Exception as exc:
        print(exc)
        return f"Failed to process Excel: {exc}"