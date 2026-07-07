from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.enums import Gender


class ProfileCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=255)
    gender: Gender
    birth_date: date
    height: int = Field(ge=100, le=250)
    start_weight: float = Field(ge=20, le=300)

    model_config = ConfigDict(from_attributes=True)


class ProfileRead(ProfileCreate):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
