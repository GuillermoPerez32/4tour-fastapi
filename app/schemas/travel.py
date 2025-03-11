
from pydantic import BaseModel


class BaseTravel(BaseModel):
    title: str
    description: str


class TravelResponse(BaseTravel):
    id: int


class TravelCreate(BaseModel):
    title: str
    description: str


class TravelUpdate(BaseModel):
    title: str | None
    description: str | None
