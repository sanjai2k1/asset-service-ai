from dataclasses import dataclass,field
from typing import Optional, List
import io
import pandas as pd
import duckdb
from pydantic import BaseModel, Field

@dataclass
class ContextInfo:
    excel_file: io.BytesIO = None
    processed_df: Optional[pd.DataFrame] = None
    table_name: str = "assets"  # Default name, can be updated dynamically
    summary: str = ""
    key_columns: List[str] = None 
    column_value_map : Optional[dict]= None


@dataclass
class SqlWriterContext:
    is_paginated:bool = None
    table_name: str = None
    db_path: Optional[str] =None



class RouterDecision(BaseModel):
    routes: List[str]   # ["summarize_excel", "sql_writer"]
    message: Optional[str] = None


class SummaryOutput(BaseModel):
    summary: str = Field(description="A 2-sentence non-technical overview of the file's purpose.")
    key_columns: List[str] = Field(description="The 4-5 most important business columns identified.")
    table_name: str = Field(description="A clean, SQL-friendly name for this dataset (e.g., 'work_orders').")
    is_complete : bool = False

class QueryOutput(BaseModel):
    is_sql_success : bool = False
    sql_query : Optional[str] = None

class QueryOutputResponse(BaseModel):
    is_sql_success : bool = False
    sql_query : Optional[str] = None
    summary : Optional[str] = None
    query_id : Optional[str] = None

class InitSummarizerOutput(BaseModel):
    summary: str = Field(description="A 2-sentence non-technical overview of the file's purpose.")
    key_columns: List[str] = Field(description="The 4-5 most important business columns identified.")
    table_name: str = Field(description="A clean, SQL-friendly name for this dataset (e.g., 'work_orders').")
    column_value_map : dict =  Field(description="A clean, SQL-friendly name for this dataset (e.g., 'work_orders').")
    is_complete : bool = False

@dataclass
class StateInfo:
    request: str 
    thread_id : Optional[str] = None
    table_name: Optional[str] =None
    db_path: Optional[str] =None
    excel_summary: Optional[str] =None
    excel_path : Optional[str] = None 
    current_node_message : Optional[str] =None                 
    key_columns: Optional[List[str]] = None
    column_value_map: Optional[dict] = None
    clarification_question : Optional[str] = None
    init_summarizer_state : Optional[SummaryOutput] = None
    user_reqs : Optional[List[str]] =field(default_factory=list)
    router_decision : Optional[RouterDecision] = None
    sql_writer_state: List[QueryOutputResponse] = field(default_factory=list)





