from pydantic import BaseModel
from typing import List, Optional

class ProfileData(BaseModel):
    gender: Optional[str]
    age: Optional[int]
    location: Optional[str]
    occupation: Optional[List[str]]
    freelancing: Optional[bool]
    goal: Optional[str]
    favorites: Optional[List[str]]
    hobbies: Optional[List[str]]

class Profile(BaseModel):
    type: str
    data: ProfileData
    timestamp: str
