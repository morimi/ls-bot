from pydantic import BaseModel
from typing import List, Optional

class SearchRequest(BaseModel):
    query: str
    n_results: int = 5

class SearchResult(BaseModel):
    id: str
    text: str
    score: float
    url: Optional[str] = None

class SearchResponse(BaseModel):
    results: List[SearchResult]

class ChatRequest(BaseModel):
    category: str
    message: str

class ChatResponse(BaseModel):
    reply: str 