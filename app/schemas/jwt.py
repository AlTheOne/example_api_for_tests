from pydantic import BaseModel


class AccessTokenPayload(BaseModel):
    user_id: int
    phone: str
