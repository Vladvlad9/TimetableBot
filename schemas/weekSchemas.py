from pydantic import BaseModel, Field


class WeekSchema(BaseModel):
    user_id: int = Field(ge=1)
    Monday: str = Field(default=None)
    Tuesday: str = Field(default=None)
    Wednesday: str = Field(default=None)
    Thursday: str = Field(default=None)
    Friday: str = Field(default=None)
    Saturday: str = Field(default=None)
    Sunday: str = Field(default=None)
    description: str = Field(default=None)
    handle: bool = Field(default=False)


class WeekInDBSchema(WeekSchema):
    id: int = Field(ge=1)
