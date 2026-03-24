from guardrails import Guard
from pydantic import BaseModel
from typing import Type, Union

class GuardrailsUtils:

    @staticmethod
    def create_guard(schema: type[BaseModel]):

        guard = Guard.for_pydantic(schema)

        return guard

    @staticmethod
    def map_to_schema(
        schema_class: Type[BaseModel],
        raw_data: Union[dict, BaseModel]
    ) -> BaseModel:

        if isinstance(raw_data, dict):
            return schema_class(**raw_data)

        elif isinstance(raw_data, BaseModel):
            return schema_class(**raw_data.model_dump())

        else:
            raise TypeError(f"Cannot map type {type(raw_data)} to schema {schema_class}")