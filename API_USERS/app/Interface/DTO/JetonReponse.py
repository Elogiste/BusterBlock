from pydantic import BaseModel


class JetonReponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
