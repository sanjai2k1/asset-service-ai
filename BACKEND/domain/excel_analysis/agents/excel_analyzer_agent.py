from agents import Agent,ModelSettings
from llm.factory.llm_factory import LLMFactory
from ..tools.analyze_excel_tool import analyze_and_load_excel
from ..state import SummaryOutput
from ..prompts import PROMPT
 

model = LLMFactory.get_open_ai_chat_completion_model()


initial_excel_agent = Agent(
    name="Summarizer",
        model=model,

    instructions=PROMPT, # Use your existing PROMPT here
    tools=[analyze_and_load_excel],
    model_settings=ModelSettings(tool_choice="required"),
output_type=SummaryOutput # 🛡️ THE GUARDRAIL
)