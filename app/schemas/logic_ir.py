from pydantic import BaseModel
from typing import List


class State(BaseModel):
    name: str
    initial: bool | int | float | str
    meaning: str


class DerivedValue(BaseModel):
    name: str
    expression: str
    meaning: str


class Branch(BaseModel):
    condition: str
    result: str | bool | int | float
    plain_meaning: str


class LogicIR(BaseModel):
    language: str
    summary: str
    inputs: List[str] = []                
    states: List[State] = []             
    derived_values: List[DerivedValue] = []  
    branches: List[Branch] = []          
    edge_cases: List[str] = []           
    uncertainties: List[str] = []        