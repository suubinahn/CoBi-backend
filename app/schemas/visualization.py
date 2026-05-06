from pydantic import BaseModel

class Diagram(BaseModel):
    title: str
    type: str
    mermaid: str

class Visualizations(BaseModel):
    flowchart: Diagram
    state_diagram: Diagram