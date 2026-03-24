import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage
import schemas.srcreation.classification_result_schema as sr_schemas
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

allowed = [
    (sr_schemas.__name__, "ClassificationResult"),
    (sr_schemas.__name__, "LLMResponseDetails"),
    (sr_schemas.__name__, "ClassificationState"),
    (sr_schemas.__name__, "Message")
]


class CheckpointUtil:
    _checkpointer = MemorySaver(
serde=JsonPlusSerializer(allowed_msgpack_modules=allowed)

    )
    _namespace = "default" 

    @staticmethod
    def create_thread_id() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def get_config(thread_id: str):
        return {
            "configurable": {
                "thread_id": thread_id,
            }
        }
