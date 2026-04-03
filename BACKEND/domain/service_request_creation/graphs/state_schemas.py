from typing import TypedDict, Optional,Annotated,List,Dict
from operator import add
from pydantic import BaseModel, Field
class State(TypedDict, total=False):
    user_reqs:  List[str]
    prev_calrification_ques :  List[str]
    service_type: Optional[str]
    request_type: Optional[str]
    thread_id : Optional[str]
    final_summary : Optional[str]
    current_node : str 
    request : str
    service : Optional[str]
    clarification_question: Optional[str] = None
    is_classification_complete : bool = False
    is_mandatory_fields_complete : bool = False
    messages: List[Dict]
    data: Dict[str, Optional[str]] = {}
    missing_fields: List[str] = []
    sr_request_id : Optional[str]
    sr_doc_no : Optional[str]
class ClassificationResult(BaseModel):
    service: Optional[str] = None
    request_type: Optional[str] = None
    clarification_question: Optional[str] = None
    confidence: Optional[float] = None
    is_request_complete : bool = False
    needs_clarification : bool = False


class FinalSummary(BaseModel):
    final_summary : str

class MandatoryExtractionResult(BaseModel):
    is_complete: bool = False
    data: Dict[str, Optional[str]] = {}
    missing_fields: List[str] = []
    clarification_question: Optional[str] = None