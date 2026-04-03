from pydantic import BaseModel, Field
from typing import Optional, List,Dict,Any
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
    collect_details : Dict[str,Any] = {}
class ClassificationResult(BaseModel):
    service: Optional[str] = None
    request_type: Optional[str] = None
    clarification_question: Optional[str] = None
    confidence: Optional[float] = None
    llm_response_dets : Optional[LLMResponseDetails] = None
class MandatoryFieldsResponse(BaseModel):
    clarification_question: Optional[str] = None    # polite question or None
    is_mandatory_fields_complete: bool = False        # True if all mandatory fields are filled
    needs_clarification: bool
    llm_response_dets : Optional[LLMResponseDetails] = None
    extracted_data : Optional[str] =None




class Message(BaseModel):
    role: str
    content: str
    tokens: int 
class ClassificationState(BaseModel):
    missing_fields: List[str] = []
    # ---- User Input ----
    request_type: Optional[str] = None
    request : str = ""
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
    extracted_data :Optional[str] = None
    conversation: List[Dict[str, Any]] = []
    user_requests: List[str] = []
    collect_details : Dict[str, Any] = {}
    # ---- Error Handling ----
    error: Optional[str] = None

    confidence: Optional[float] = None



class AskRequest(BaseModel):
    thread_id: Optional[str] = None
    request: str

class GetSRRecordsRequest(BaseModel):
    limit: int = Field(default=10, ge=1, description="Number of records to fetch")
    offset: int = Field(default=0, ge=0, description="Number of records to skip")
    service: Optional[str] = Field(default=None, description="Filter by service")
    request_type: Optional[str] = Field(default=None, description="Filter by request type")


class GetSRRecordsResponse(BaseModel):
    total_count: int
    records: List[dict]  # or create a Pydantic model for ServiceRequest if you want strict typing
