from pydantic import BaseModel
from typing import List, Optional

from models.BookGenreModel import BookGenre

class Book(BaseModel):
    id: Optional[str] = None
    title: str
    author: str
    opinion: str
    genres: List[str] = []
    