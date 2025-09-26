from pydantic import BaseModel
from typing import List, Optional

class Memory(BaseModel):
    id: int
    user_id: str
    message: Optional[str] = None
    vector_data: Optional[List[float]] = None
    cosine_similarity: Optional[float] = None
    rn: Optional[int] = None