from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class Demand(BaseModel):
    city: str
    demand: float
    unit:str

class PackageBody(BaseModel):
    demands: List[Demand]
    validUntil: datetime
    metaContent: str
    constraints: dict = Field(default_factory=dict)

class Event(BaseModel):
    idpk: str
    type: str
    packageBody: PackageBody

