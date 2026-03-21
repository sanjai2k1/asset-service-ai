from pydantic import BaseModel, Field
from typing import Optional, List
from schemas.system.system_schema import UsageSchema,LLMHealthResponse

class LLMResponseDetails(LLMHealthResponse):
    pass

class ClassificationResultAskResponse(BaseModel):
    service: Optional[str] = None
    request_type: Optional[str] = None
    clarification_question: Optional[str] = None
    confidence: Optional[float] = None
    llm_response_dets : Optional[LLMResponseDetails] = None
    missing_fields: List[str] = []                 # list of missing mandatory field names
    is_mandatory_fields_complete: bool = False        # True if all mandatory fields are filled
    needs_clarification: bool = False
    
class ClassificationResult(BaseModel):
    service: Optional[str] = None
    request_type: Optional[str] = None
    clarification_question: Optional[str] = None
    confidence: Optional[float] = None
    llm_response_dets : Optional[LLMResponseDetails] = None
class MandatoryFieldsResponse(BaseModel):
    missing_fields: List[str] = []                 # list of missing mandatory field names
    clarification_question: Optional[str]     # polite question or None
    is_mandatory_fields_complete: bool = False        # True if all mandatory fields are filled
    needs_clarification: bool
    llm_response_dets : Optional[LLMResponseDetails] = None
    extracted_fields : List[str] = []


class ClassificationState(BaseModel):
    missing_fields: List[str] = []
    # ---- User Input ----
    request_type: Optional[str] = None
    request : str
    # ---- Prompt Data (from DB) ----
    service: Optional[str] = None
    typesofrequests: Optional[str] = None

    # ---- Prompt sent to LLM ----
    prompt: Optional[str] = None
    # ---- LLM Result ----
    classification: Optional[ClassificationResult] = None
    llm_response_dets : Optional[LLMResponseDetails] = None

    # ---- Conversation Control ----
    clarification_question: Optional[str] = None
    user_response: Optional[str] = None

    # ---- Workflow Flags ----
    is_request_complete: bool = False
    is_mandatory_details_complete : bool = False
    is_mandatory_fields_complete : bool = False
    needs_clarification: bool = False

    # ---- Loop Control ----
    retry_count: int = 0
    max_retries: int = 1

    # ---- History ----
    conversation_history: List[str] = Field(default_factory=list)

    # ---- Error Handling ----
    error: Optional[str] = None

    confidence: Optional[float] = None



class AskRequestResponse(BaseModel):
    thread_id: Optional[str] = None
    request: str