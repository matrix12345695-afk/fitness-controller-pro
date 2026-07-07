from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    telegram_id: int
    username: str | None = None
    first_name: str
    last_name: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UserRead(BaseModel):
    id: int
    telegram_id: int
    username: str | None = None
    first_name: str
    last_name: str | None = None
    language: str

    model_config = ConfigDict(from_attributes=True)
