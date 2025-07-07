from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class BookGenre(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
