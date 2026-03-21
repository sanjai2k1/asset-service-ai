from app.llm.llm_factory import LLMFactory


class LLMUtils:

    @staticmethod
    async def ask(prompt: str):

        llm = LLMFactory.get_llm()

        response = await llm.predict(prompt)

        return response