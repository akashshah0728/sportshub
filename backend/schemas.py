from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    email: EmailStr
    display_name: str
    first_name: str
    last_name: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    display_name: str
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)
