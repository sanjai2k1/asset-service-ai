from pydantic import BaseModel
from typing import List, Optional

# --- Health ---
class HealthResponse(BaseModel):
    status: str

class DBHealthResponse(BaseModel):
    db: str


# --- Message schema ---
class MessageSchema(BaseModel):
    role: str          # "user" or "assistant"
    content: str
    tokens: int

# --- Token usage schema ---
class UsageSchema(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

# --- LLM response schema ---
class LLMHealthResponse(BaseModel):
    content: str
    messages: Optional[List[MessageSchema]] =None
    usage: UsageSchema
    thread_id:str

# --- Prompt Template Variables ---
class PromptVariableResponse(BaseModel):
    id: int
    prompt_key: str
    keyword: str
    description: Optional[str] = None
    category: Optional[str] = None
    is_deleted: bool