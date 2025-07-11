from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
class TodoCreate(BaseModel):
    title: str = Field(...,example="Learn FastAPI")
    description: Optional[str] = Field(None, example="Use async and MongoDB")
    created_at : Optional[datetime] = None
    updated_at : Optional[datetime] = None
    
class TodoResponse(TodoCreate):
    id: str 