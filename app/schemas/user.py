from pydantic import BaseModel

class SignupRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class SignupResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
