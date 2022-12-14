from datetime import datetime

from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    lname: str
    fname: str
    mname: str
    positions_id: int = Field(default=1)
    user_id: int
    nickname: str = Field(default=None)
    checked: bool


class UserInDBSchema(UserSchema):
    id: int = Field(ge=1)
