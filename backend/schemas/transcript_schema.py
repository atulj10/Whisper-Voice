from pydantic import BaseModel, Field
from datetime import datetime


class TranscriptSchema(BaseModel):
    id: int | None = None
    text: str
    created_at: datetime | None = None
    status: str

    class Config:
        from_attributes = True


class TranscriptCreateSchema(BaseModel):
    text: str = Field(..., min_length=1)
    status: str = Field(default="completed")


class HealthResponse(BaseModel):
    status: str


class ListenerStatusResponse(BaseModel):
    status: str
    message: str
