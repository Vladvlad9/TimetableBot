from pydantic import BaseModel, Field


class AdminSchema(BaseModel):
    lname: str
    fname: str
    mname: str


class AdminInDBSchema(AdminSchema):
    id: int = Field(ge=1)
