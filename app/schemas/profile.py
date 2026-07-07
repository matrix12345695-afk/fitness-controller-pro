from datetime import date

from pydantic import BaseModel, ConfigDict

from app.enums import Gender


class ProfileCreate(BaseModel):
    full_name: str
    gender: Gender
    birth_date: date
    height: int
    start_weight: float

    model_config = ConfigDict(from_attributes=True)
