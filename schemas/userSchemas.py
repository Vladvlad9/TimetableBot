from datetime import datetime

from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    id: int = Field(ge=1)

    lname: str
    fname: str
    mname: str
    positions_id: int = Field(ge=1, default=1)


class UserInDBSchema(UserSchema):
    id: int = Field(ge=1)
