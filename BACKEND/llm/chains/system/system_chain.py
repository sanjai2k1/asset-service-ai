from langchain_core.messages import HumanMessage
from llm.factory.llm_factory import LLMFactory
from llm.prompts.system import system_prompt


class SystemChain:

    def __init__(self):

        self.llm = LLMFactory.get_open_ai_llm()

    def run(self,thread_id):

        prompt = system_prompt.system_check_prompt
        response = self.llm.generate(prompt=prompt,thread_id=thread_id)


        return response







# class ClassifierChain:

#     def __init__(self):

#         self.llm = LLMFactory.get_llm()

#         self.guard = GuardrailsUtils.create_guard(
#             ClassificationResult
#         )

#     def run(self, request: str):

#         print(request)

#         prompt = classifier_prompt.format(
#             request=request
#         )

#         # Call LLM
#         response = self.llm.invoke(
#             [HumanMessage(content=prompt)]
#         )

#         content = response.content

#         # Guardrails validation
#         validated = self.guard.parse(
#             content
#         )

#         return validated.validated_output


# class ClassifierChain:

#     def __init__(self):

#         self.llm = LLMFactory.get_open_ai_llm()

#         self.guard = GuardrailsUtils.create_guard(
#             ClassificationResult
#         )

#     def run(self, request: str):

#         prompt = classifier_prompt.format(
#             request=request
#         )

#         content = self.llm.generate(prompt)
#         validated = self.guard.parse(
#             content
#         )

#         return validated.validated_output