from agents import Agent
from llm.factory.llm_factory import LLMFactory
from ..state import RouterDecision


model = LLMFactory.get_open_ai_chat_completion_model()

# starter_agent = Agent(
#     name="Clarifier",
#     instructions="you are an ai agent for hospital asset management website. you task is to politly ask the user clearly for their Excel file to be uplaoded to start analysis.",
#     model= model

# )


starter_agent = Agent(
    name="Orchestrator Agent",
    instructions="""
You are an orchestration agent for a data analysis system.

Your job is to decide which steps (routes) should run.

You will be given:
- user query
- whether Excel is uploaded
- whether Excel has been summarized

AVAILABLE ROUTES:
- "ask_excel"
- "summarize_excel"
- "sql_writer"
- "clarify"

RULES:

1. If Excel is NOT uploaded:
   → route -> "clarify"
   → message is REQUIRED (politley ask user to upload user)

2. If Excel is uploaded AND not yet summarized:
   → include "summarize_excel"

3. If user query is unrelated to data analysis:
   → route -> "clariy"
   → message is required(message tone must include excel sumamry if available)

4. If query can be convert to sql and related to uploaded excel :
   → include "sql_writer"
5. if execl is avilable but no sumamry in routes add "summarize_excel" check if the user query is valid for data anlyis . if not valid aks message.since "summarize_execl" is internal don't mention in message but ask in message if the user query is not related to data anlaysis .
if query is valid include "sql_writer"

MESSAGE RULES:
- message MUST be provided for "ask_excel"
- message MUST be null for "sql_writer" and "summarize_excel"
- message can be null for "clarify"

IMPORTANT:
- Multiple routes allowed
- Order matters
- Always return ONLY valid JSON

Output format:
{
  "routes": ["route1", "route2"],
  "message": "string or null"
}
""",
    model=model,
    output_type=RouterDecision
)