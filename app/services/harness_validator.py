def validate_harness(logic_ir, visualizations):
    warnings = []

    flow = visualizations.get("flowchart", {})
    state = visualizations.get("state_diagram", {})

    # 1. Mermaid 비어있는지
    if not flow.get("mermaid"):
        warnings.append("flowchart Mermaid가 비어 있습니다.")

    # 2. 타입 체크
    if flow.get("type") != "flowchart":
        warnings.append("flowchart type이 잘못되었습니다.")

    if state.get("type") != "stateDiagram":
        warnings.append("stateDiagram type이 잘못되었습니다.")

    # 3. branches 없는데 flowchart 생성
    if not logic_ir.branches and flow.get("mermaid"):
        warnings.append("조건이 없는데 flowchart가 생성되었습니다.")

    # 4. 너무 긴 다이어그램
    if len(flow.get("mermaid", "")) > 2000:
        warnings.append("flowchart가 너무 깁니다.")

    return warnings