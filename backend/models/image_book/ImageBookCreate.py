from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ImageBookCreate(BaseModel):
    #id: Optional[str] = None
    image_book: str
    book_id: str
    
