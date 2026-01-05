# from pydantic import BaseModel

# class ChatRequest(BaseModel):
#     message: str

# class ChatResponse(BaseModel):
#     reply: str

from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    user_id: str | None = None
    message: str

class Button(BaseModel):
    id: str
    label: str

class ChatResponse(BaseModel):
    reply: str
    buttons: Optional[List[Button]] = None

