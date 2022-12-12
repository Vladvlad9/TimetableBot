from pydantic import BaseModel, Field


class PositionSchema(BaseModel):
    name: str


class PositionInDBSchema(PositionSchema):
    id: int = Field(ge=1)
