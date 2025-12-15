from pydantic import BaseModel
from typing import List, Optional


class ChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []


class SourceChunk(BaseModel):
    source: str
    content: str


class ChatResponse(BaseModel):
    reply: str
    sources: Optional[List[SourceChunk]] = []
