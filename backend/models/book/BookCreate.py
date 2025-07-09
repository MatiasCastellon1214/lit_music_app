from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional

from models.book_genre.BookGenreModel import BookGenre

class BookCreate(BaseModel):
    title: str
    author: str
    genres_id: List[str] = Field(..., min_length=1, description="Id must belong to a valid genre")
    image: Optional[List[str]] = []
    comment_id: Optional[List[str]] = []
    
    
    