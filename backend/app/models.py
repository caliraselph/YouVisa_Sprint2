from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Case(BaseModel):
    user_id: str
    channel: str
    status: str
    created_at: Optional[str] = None
    email: Optional[str] = None
    log: Optional[List[str]] = Field(default_factory=list)

class Document(BaseModel):
    case_id: str
    tipo: str
    filename: str
    storage_path: str
    mime_type: str
    status: str
    created_at: Optional[str] = None
    validacao_visual: Optional[dict] = None
    error_message: Optional[str] = None
