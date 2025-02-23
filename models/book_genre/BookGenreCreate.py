from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class BookGenreCreate(BaseModel):
    #id: Optional[str] = None
    name: str
    description: Optional[str] = None
    
