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


def prettify_result(raw_result: str) -> str:
    raw_result = raw_result.lower()

    if "error" in raw_result:
        return "오류"
    elif "pending" in raw_result:
        return "승인 대기"
    elif "success" in raw_result:
        return "완료"
    elif "soldout" in raw_result:
        return "재고 부족"

    return "결과"


def generate_flowchart(logic_ir):
    lines = ["flowchart TD"]
    lines.append("START([START])")

    for i, branch in enumerate(logic_ir.branches):
        cond_node = f"C{i}"
        res_node = f"R{i}"

        # 사용자 친화적 조건 설명 사용
        condition = safe_text(branch.plain_meaning)

        # 상태 결과 한글화
        result = prettify_result(
            safe_text(branch.result)
        )

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

        # 사용자 친화적 조건 설명 사용
        condition = safe_text(branch.plain_meaning)

        # 상태 결과 한글화
        result = prettify_result(
            safe_text(branch.result)
        )

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