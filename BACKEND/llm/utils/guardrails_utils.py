from guardrails import Guard
from pydantic import BaseModel


class GuardrailsUtils:

    @staticmethod
    def create_guard(schema: type[BaseModel]):

        guard = Guard.for_pydantic(schema)

        return guard