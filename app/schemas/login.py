from pydantic import BaseModel, EmailStr


class ResponseLogin(BaseModel):
    email:EmailStr
    password:str 


class RequestToken(BaseModel):
    access_token:str
    refresh_token:str
    token_type:str
