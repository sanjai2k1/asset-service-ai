from config.settings import settings
from llm.utils.self_hosted_llm import SelfHostedLLM
from llm.utils.open_ai_util import OpenAI_LLMUtil
from agents import OpenAIChatCompletionsModel, AsyncOpenAI

class LLMFactory:

    _llm = None
    _openai_llm = None
    _openai_chat_completion = None

    @staticmethod
    def get_llm():

        if LLMFactory._llm is None:

            LLMFactory._llm = SelfHostedLLM(
                api_url=settings.llm_url,
                api_key=settings.llm_key,
                model=settings.llm_model
            )

        return LLMFactory._llm
    @staticmethod
    def get_open_ai_llm():

        if LLMFactory._openai_llm is None:

            LLMFactory._openai_llm = OpenAI_LLMUtil(
                llm_url=settings.openai_llm_url,
                llm_key=settings.llm_key,
                llm_model=settings.llm_model
            )

        return LLMFactory._openai_llm
    @staticmethod
    def get_open_ai_chat_completion_model():
        if LLMFactory._openai_chat_completion is None:
            return OpenAIChatCompletionsModel( model=settings.llm_model,
    openai_client=AsyncOpenAI(base_url=settings.openai_llm_url, api_key=settings.llm_key))
        return LLMFactory._openai_chat_completion