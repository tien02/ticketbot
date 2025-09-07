from typing import List, Literal, Optional

from pydantic import BaseModel


class InsertRequest(BaseModel):
    obj_uuid: Optional[str] = None
    question: str
    answer: str


class InsertResponse(BaseModel):
    status: Literal["SUCCESS", "FAIL"]
    uuid: str


class SearchRequest(BaseModel):
    query: str
    limit: int = 1


class SearchResult(BaseModel):
    question: str
    answer: str


class SearchResponse(BaseModel):
    status: Literal["SUCCESS", "FAIL"]
    results: List[SearchResult]
