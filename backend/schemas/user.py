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
    avatar_url:Optional[str] = None

class UserOut(BaseModel):
    id:int
    username:str
    email:EmailStr
    phone:str 
    role:Optional[Role] = None
    created_at:datetime
    avatar_url:Optional[str] = None

    model_config = {
        "from_attributes": True}
    @classmethod
    def model_validate(cls, user):
        avatar_url = user.avatar_url

        if avatar_url:
            fixed_path = avatar_url.replace("\\", "/")
            full_ava = f"http://localhost:8000/{fixed_path.lstrip('/')}"
        else:
            full_ava = None

        return cls(
            id = user.id,
            username = user.username,
            email = user.email,
            phone = user.phone,
            role = user.role,
            created_at = user.created_at,
            avatar_url = full_ava
        )




class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=9, max_length=9)
    role: Optional[Role] = None
    avatar_url: Optional[str] = None

class ProfileUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=9, max_length=9)
    
    
class PasswordUpdate(BaseModel):
    old_password:Optional[str] = Field(None, min_length=8, max_length=64)
    new_password:Optional[str] = Field(None, min_length=8, max_length=64)


