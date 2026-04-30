from pydantic import BaseModel
from typing import List

class Candidate(BaseModel):
    name: str
    title: str
    experience: str
    match_percentage: int
    skills: List[str]