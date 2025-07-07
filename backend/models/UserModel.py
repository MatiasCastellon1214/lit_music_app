from typing import List, Optional
from pydantic import BaseModel

class User(BaseModel):
    id: Optional[str] = None
    username: str
    email: str
    password: str
    