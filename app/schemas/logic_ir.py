import json
from pydantic import BaseModel, field_validator
from typing import Any, List


class State(BaseModel):
    name: str
    initial: bool | int | float | str | None
    meaning: str


class DerivedValue(BaseModel):
    name: str
    expression: str
    meaning: str


class Branch(BaseModel):
    condition: str
    result: Any
    plain_meaning: str
    state_name: str = ""
    ui_message: str = ""
    severity: str = "info"
    transition_label: str = "다음"
    condition_var: str = ""   # 조건 변수명 (e.g., "사용자 ID")
    true_label: str = "YES"   # 조건 참일 때 엣지 레이블 (e.g., "없음", "0이하")
    false_label: str = "NO"   # 조건 거짓일 때 엣지 레이블 (e.g., "있음", "0초과")

    @field_validator("result", mode="before")
    @classmethod
    def serialize_complex_result(cls, v: Any) -> str | bool | int | float:
        if isinstance(v, (dict, list)):
            return json.dumps(v, ensure_ascii=False)
        return v


class LogicIR(BaseModel):
    language: str
    summary: str
    inputs: List[str] = []                
    states: List[State] = []             
    derived_values: List[DerivedValue] = []  
    branches: List[Branch] = []          
    edge_cases: List[str] = []           
    uncertainties: List[str] = []        