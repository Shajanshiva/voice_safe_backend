from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    full_name: str
    email: str
    password: str

class UserUpdate(BaseModel):
    full_name: str
    email: str
    password: Optional[str] = None

class UserResponse(BaseModel):
    user_id: int
    full_name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True
 
class IssueBase(BaseModel):
    category_name: str
    title: str
    description: str
    evidence_url: Optional[str] = None

class commentBase(BaseModel):
    issue_id: int
    user_id: int
    comment_text: str

class userLogin(BaseModel):
    email: str
    password: str


    