from pydantic import BaseModel
from typing import List

class RoleView(BaseModel):
    primary_visualization: str
    title: str
    summary: str
    key_points: List[str]
    questions_to_confirm: List[str]