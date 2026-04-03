from agents import Agent,ModelSettings
from llm.factory.llm_factory import LLMFactory
from ..tools.sql_writer_tool import query_excel_sql,query_with_intelligent_output
from ..state import QueryOutput
from ..prompts import SQL_PROMPT,SQL_RESULT_RESPONSE_PROMPT
 

model = LLMFactory.get_open_ai_chat_completion_model()

sql_writer_agent = Agent(
    name="SQL_Writer",
            model=model,

    instructions=SQL_PROMPT, # Use your existing SQL_PROMPT here
    tools=[query_excel_sql],
    output_type = QueryOutput
)


sql_result_resposne_agent = Agent(
    name="Result_Processor",
    model=model,
    instructions=SQL_RESULT_RESPONSE_PROMPT,
    tools=[query_with_intelligent_output]
)
