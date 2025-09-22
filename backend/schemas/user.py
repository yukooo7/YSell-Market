from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from enums import Role
from typing import Optional

class UserCreate(BaseModel):
    username:str
    email:EmailStr
    phone:str = Field(..., min_length=9, max_length=9)
    role:Role
    password:str

class UserOut(BaseModel):
    id:int
    username:str
    email:EmailStr
    phone:str 
    role:Optional[Role] = None
    created_at:datetime

    model_config = {
        "from_attributes": True}
    
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=9, max_length=9)
    role: Optional[Role] = None

class ProfileUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str] = Field(None, min_length=9, max_length=9)
    
class PasswordUpdate(BaseModel):
    old_password:Optional[str] = Field(None, min_length=8, max_length=64)
    new_password:Optional[str] = Field(None, min_length=8, max_length=64)

