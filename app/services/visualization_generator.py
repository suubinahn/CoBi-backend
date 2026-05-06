def safe_text(text: str) -> str:
    if not text:
        return ""
    return (
        str(text)
        .replace('"', "'")
        .replace("\n", " ")
        .replace("{", "(")
        .replace("}", ")")
    )


def generate_flowchart(logic_ir):
    lines = ["flowchart TD"]
    lines.append("START([START])")

    # 조건 분기 생성
    for i, branch in enumerate(logic_ir.branches):
        cond_node = f"C{i}"
        res_node = f"R{i}"

        condition = safe_text(branch.condition)
        result = safe_text(branch.result)

        lines.append(f"{cond_node}{{{condition}}}")
        lines.append(f"{res_node}[{result}]")

        if i == 0:
            lines.append(f"START --> {cond_node}")
        else:
            lines.append(f"R{i-1} --> {cond_node}")

        lines.append(f"{cond_node} -->|True| {res_node}")

    lines.append("END([END])")

    if logic_ir.branches:
        last_res = f"R{len(logic_ir.branches)-1}"
        lines.append(f"{last_res} --> END")
    else:
        lines.append("START --> END")

    return "\n".join(lines)


def generate_state_diagram(logic_ir):
    # state 없으면 기본 다이어그램
    if not logic_ir.states:
        return "stateDiagram-v2\n[*] --> Idle"

    lines = ["stateDiagram-v2"]

    # 첫 번째 state만 시작점으로 연결
    first_state = logic_ir.states[0].name
    lines.append(f"[*] --> {first_state}")

    return "\n".join(lines)


def generate_visualizations(logic_ir):
    return {
        "flowchart": {
            "title": "조건 분기 흐름도",
            "type": "flowchart",
            "mermaid": generate_flowchart(logic_ir)
        },
        "state_diagram": {
            "title": "UI 상태 전이도",
            "type": "stateDiagram",
            "mermaid": generate_state_diagram(logic_ir)
        }
    }