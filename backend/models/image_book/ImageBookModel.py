from pydantic import BaseModel
from typing import Optional

class ImageBook(BaseModel):
    id: Optional[str] = None
    image_book: str
    book_id: str
    