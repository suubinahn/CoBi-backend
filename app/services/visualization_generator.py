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

    if "login required" in raw_result:
        return "로그인 필요"

    elif "invalid amount" in raw_result:
        return "잘못된 금액"

    elif "approval required" in raw_result:
        return "승인 대기"

    elif "success" in raw_result:
        return "주문 완료"

    elif "password mismatch" in raw_result:
        return "비밀번호 불일치"

    elif "cannot be deleted" in raw_result:
        return "삭제 불가"

    elif "user not found" in raw_result:
        return "사용자 없음"

    elif "blocked user" in raw_result:
        return "차단 사용자"

    elif "out of stock" in raw_result:
        return "재고 부족"

    elif "error" in raw_result:
        return "오류"

    elif "pending" in raw_result:
        return "대기"

    return "결과"


def get_result_class(result: str) -> str:

    if result in [
        "로그인 필요",
        "잘못된 금액",
        "오류",
        "비밀번호 불일치",
        "삭제 불가",
        "사용자 없음",
        "차단 사용자"
    ]:
        return "errorNode"

    elif result in [
        "승인 대기",
        "대기"
    ]:
        return "pendingNode"

    elif result in [
        "주문 완료",
        "재고 부족",
        "결과"
    ]:
        return "successNode"

    return "defaultNode"


def generate_flowchart(logic_ir):

    lines = ["flowchart TD"]

    lines.append("START([START])")

    for i, branch in enumerate(logic_ir.branches):

        cond_node = f"C{i}"
        res_node = f"R{i}"

        # 조건 노드 텍스트: condition_var 우선, 없으면 plain_meaning fallback
        condition_label = safe_text(
            branch.condition_var if branch.condition_var else branch.plain_meaning
        )

        true_edge = safe_text(branch.true_label) or "YES"
        false_edge = safe_text(branch.false_label) or "NO"

        result = prettify_result(
            safe_text(branch.result)
        )

        result_class = get_result_class(result)

        # 조건 노드
        lines.append(
            f'{cond_node}{{"{condition_label}"}}'
        )

        # 결과 노드
        lines.append(
            f'{res_node}["{result}"]'
        )

        # 시작 연결
        if i == 0:
            lines.append(
                f"START --> {cond_node}"
            )

        else:
            prev_false = safe_text(logic_ir.branches[i-1].false_label) or "NO"
            lines.append(
                f"C{i-1} -->|{prev_false}| {cond_node}"
            )

        # 참 분기 → 결과
        lines.append(
            f"{cond_node} -->|{true_edge}| {res_node}"
        )

        # 결과 → END
        lines.append(
            f"{res_node} --> END"
        )

        # 스타일 적용
        lines.append(
            f"class {res_node} {result_class}"
        )

    # 마지막 거짓 분기 → END
    if logic_ir.branches:

        last_cond = f"C{len(logic_ir.branches)-1}"
        last_false = safe_text(logic_ir.branches[-1].false_label) or "NO"

        lines.append(
            f"{last_cond} -->|{last_false}| END"
        )

    lines.append("END([END])")

    # 스타일 정의
    lines.append(
        "classDef errorNode fill:#7f1d1d,stroke:#f87171,color:#ffffff,stroke-width:2px"
    )

    lines.append(
        "classDef pendingNode fill:#78350f,stroke:#fbbf24,color:#ffffff,stroke-width:2px"
    )

    lines.append(
        "classDef successNode fill:#064e3b,stroke:#34d399,color:#ffffff,stroke-width:2px"
    )

    lines.append(
        "classDef defaultNode fill:#27272a,stroke:#a1a1aa,color:#ffffff"
    )

    return "\n".join(lines)


def generate_state_diagram(logic_ir):

    lines = ["stateDiagram-v2"]

    lines.append("[*] --> Decision")

    added_states = set()

    for branch in logic_ir.branches:

        # 상태 다이어그램 레이블: "변수명 [참조건값]" 형태
        cond_var = safe_text(branch.condition_var) if branch.condition_var else ""
        true_lbl = safe_text(branch.true_label) or "YES"
        condition_label = f"{cond_var} [{true_lbl}]" if cond_var else safe_text(branch.plain_meaning)

        result = prettify_result(
            safe_text(branch.result)
        )

        # Mermaid state safe 처리
        safe_result = result.replace(" ", "_")

        # 상태 전이
        lines.append(
            f"Decision --> {safe_result} : {condition_label}"
        )

        added_states.add(safe_result)

    for state in added_states:

        lines.append(
            f"{state} --> [*]"
        )

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