from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class BookComment(BaseModel):
    id: Optional[str] = None
    content: str
    book_id: str = Field(..., min_length=1, description="Id must belong to a valid book") # book_id is mandatory
    sentiment: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None