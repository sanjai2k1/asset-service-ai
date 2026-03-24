from llm.factory.llm_factory import LLMFactory


llm = LLMFactory.get_open_ai_llm()


def make_llm_call():
    chat_messages = [{"role": "user", "content": "This is a system check..tell anything.."}]
    llm_result = llm.generate(chat_messages=chat_messages)
    return llm_result
