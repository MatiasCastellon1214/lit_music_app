from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class BookCommentCreate(BaseModel):
    content: str
    book_id: str = Field(..., min_length=1, description="Id must belong to a valid book"),
    sentiment: Optional[str] = None
    