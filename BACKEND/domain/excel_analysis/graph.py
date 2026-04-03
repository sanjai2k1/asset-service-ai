from .state import StateInfo,ContextInfo,InitSummarizerOutput,SqlWriterContext,QueryOutput,QueryOutputResponse,RouterDecision
from llm.utils.check_pointer_util import checkpoint_util
from .agents.starter_agent import starter_agent
from .agents.sql_writer_agent import sql_writer_agent,sql_result_resposne_agent
from .agents.excel_analyzer_agent import initial_excel_agent
from langgraph.graph import StateGraph
from agents import Runner
from .helpers import build_column_index,create_duckdb_for_request
import aiofiles
from core.utils import IDGenerator
import io


async def check_or_request_excel_node(state: StateInfo):
    if state.excel_path is None:
        response = await Runner.run(starter_agent ,input=state.request)
        return {"clarification_question": response.final_output,"current_node_message":"Asking Clarification"}
    return {"clarification_question": None,"current_node_message":"Analyzing Excel"}


async def initial_excel_summarizer_agent(state: StateInfo):
    if state.db_path is None:
        context = ContextInfo()
        async with aiofiles.open(state.excel_path, "rb") as f:
            file_bytes = await f.read()
            context.excel_file = io.BytesIO(file_bytes)
        result = await Runner.run(initial_excel_agent, input="Analyze this file", context=context)
        data_info = result.final_output
        context.table_name = data_info.table_name
        context.key_columns = data_info.key_columns
        context.summary = data_info.summary
        column_profiling_result = build_column_index(context)
        context.column_value_map = column_profiling_result
    
        Init_Summarizer_Output = InitSummarizerOutput(table_name = data_info.table_name,key_columns = data_info.key_columns,
        summary = data_info.summary,
        is_complete = data_info.is_complete,
        column_value_map = column_profiling_result
        )
    
        state.init_summarizer_state = Init_Summarizer_Output
        if Init_Summarizer_Output.is_complete:
            state.table_name = Init_Summarizer_Output.table_name
            if context.processed_df is not None:
                create_duckdb_for_request(state,context.processed_df)
                state.current_node_message = "Analyzing Query"
            else:
                state.current_node_message = "Analysis Failure"
    
    

    return state

async def sql_writer_node(state : StateInfo):
    context = SqlWriterContext(table_name=state.table_name,db_path=state.db_path)
    sql_writer_output = await Runner.run(
            sql_writer_agent, 
            input=f"Current Table Name: {state.table_name}. User Question: {state.request}", 
            context=context
        )
    Query_Output_Response = QueryOutputResponse(is_sql_success = sql_writer_output.final_output.is_sql_success,
        sql_query = sql_writer_output.final_output.sql_query)
    if Query_Output_Response.is_sql_success:
        Sql_Result_agent_output = await Runner.run(
        sql_result_resposne_agent,
        input=f"SQL Query: {Query_Output_Response.sql_query}",
        context=context
    )
        Query_Output_Response.summary = Sql_Result_agent_output.final_output
        Query_Output_Response.query_id = IDGenerator.generate_uuid()
    state.sql_writer_state.append(Query_Output_Response)
        
    return state

async def orchesterator_decision(state : StateInfo):
    summary_of_excel = None
    if state.init_summarizer_state is not None:
        summary_of_excel = state.init_summarizer_state.summary

    inpt_str = f"Excel Path : {state.excel_path} user request : {state.request} Excel summary : {summary_of_excel}"
    response = await Runner.run(starter_agent ,input=inpt_str)
    router_output = RouterDecision(routes = response.final_output.routes,message = response.final_output.message)
    state.router_decision = router_output
    return state

async def executor_node(state: StateInfo):

    decision = state.router_decision  # from router agent

    for route in decision.routes:

        if route == "clarify":
            state.clarification_question = (
                decision.message or "Can you clarify your request?"
            )
            return state

        if route == "summarize_excel":
            state = await initial_excel_summarizer_agent(state)

        elif route == "sql_writer":
            state = await sql_writer_node(state)

    return state

def build_graph():
    # -----------------------------
    # Build LangGraph flow
    # -----------------------------
    builder = StateGraph(StateInfo)

    # Add nodes
    builder.add_node("orchesterator_decision", orchesterator_decision)
    builder.add_node("executor_node", executor_node)

    builder.add_node("initial_excel_summarizer_agent",initial_excel_summarizer_agent)
    builder.add_node("sql_writer_node",sql_writer_node)

    builder.add_edge("orchesterator_decision","executor_node")


    # Entry point
    builder.set_entry_point("orchesterator_decision")
    return builder



# def build_graph():
#     # -----------------------------
#     # Build LangGraph flow
#     # -----------------------------
#     builder = StateGraph(StateInfo)

#     # Add nodes
#     builder.add_node("check_or_request_excel", check_or_request_excel_node)
#     builder.add_node("initial_excel_summarizer_agent",initial_excel_summarizer_agent)
#     builder.add_node("sql_writer_node",sql_writer_node)
#     builder.add_edge("check_or_request_excel", "initial_excel_summarizer_agent")
#     builder.add_edge("initial_excel_summarizer_agent","sql_writer_node")

#     # Entry point
#     builder.set_entry_point("check_or_request_excel")
#     return builder

def compile_graph():
    graph = build_graph()
    return graph.compile(checkpointer=checkpoint_util._checkpointer)
