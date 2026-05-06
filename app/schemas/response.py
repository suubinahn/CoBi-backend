from pydantic import BaseModel
from typing import Dict, List
from app.schemas.logic_ir import LogicIR
from app.schemas.visualization import Visualizations
from app.schemas.role_view import RoleView

class AnalyzeResponse(BaseModel):
    detected_language: str
    logic_ir: LogicIR
    visualizations: Visualizations
    role_views: Dict[str, RoleView]  
    warnings: List[str]
    confidence: float