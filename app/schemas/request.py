from pydantic import BaseModel
from typing import List, Optional

class AnalyzeRequest(BaseModel):
    code: str
    language: str = "auto"
    roles: Optional[List[str]] = None
    output_style: str = "detailed"