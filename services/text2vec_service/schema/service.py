from typing import List, Optional, Union

from pydantic import BaseModel


class Text2VecRequest(BaseModel):
    texts: Optional[Union[str, List[str]]] = None


class Text2VecResponse(BaseModel):
    embeddings: list[list]
