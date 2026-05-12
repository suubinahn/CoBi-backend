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
    lines = ["stateDiagram-v2"]
    lines.append("[*] --> Decision")

    added_states = set()

    for branch in logic_ir.branches:
        condition = safe_text(branch.condition)[:40]

        raw_result = safe_text(branch.result).lower()

        if "error" in raw_result:
            result = "Error"
        elif "pending" in raw_result:
            result = "Pending"
        elif "success" in raw_result:
            result = "Success"
        else:
            result = "Result"

        lines.append(
            f"Decision --> {result} : {condition}"
        )

        added_states.add(result)

    for state in added_states:
        lines.append(f"{state} --> [*]")

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