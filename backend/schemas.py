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

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    display_name: str | None = None
    first_name: str | None = None
    last_name: str | None = None

class SeasonCreate(BaseModel):
    season_year: int


class SeasonRead(BaseModel):
    id: int
    season_year: int

    model_config = ConfigDict(from_attributes=True)


class SeasonUpdate(BaseModel):
    season_year: int | None = None
