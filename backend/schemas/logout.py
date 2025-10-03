from pydantic import BaseModel

class BlacklistTokenCreate(BaseModel):
    token: str
