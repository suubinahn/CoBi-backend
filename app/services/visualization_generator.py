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

    elif "soldout" in raw_result:
        return "재고 부족"

    elif "insufficient balance" in raw_result:
        return "잔액 부족"

    elif "verification" in raw_result:
        return "추가 인증"

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
        "대기",
        "추가 인증"
    ]:
        return "pendingNode"

    elif result in [
        "주문 완료",
        "재고 부족",
        "잔액 부족",
        "결과"
    ]:
        return "successNode"

    return "defaultNode"


def generate_flowchart(logic_ir):

    lines = ["flowchart TD"]

    lines.append("START([Start])")

    for i, branch in enumerate(logic_ir.branches):

        cond_node = f"C{i}"
        res_node = f"R{i}"

        # 조건 라벨
        condition_label = safe_text(
            branch.condition_var
            if hasattr(branch, "condition_var") and branch.condition_var
            else branch.plain_meaning
        )

        # 긴 조건 자동 줄바꿈
        if len(condition_label) > 16:
            condition_label = (
                condition_label[:16]
                + "<br/>"
                + condition_label[16:]
            )

        true_edge = (
            safe_text(branch.true_label)
            if hasattr(branch, "true_label")
            else "YES"
        ) or "YES"

        false_edge = (
            safe_text(branch.false_label)
            if hasattr(branch, "false_label")
            else "NO"
        ) or "NO"

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

            # 이전 조건 실패 시 다음 조건
            lines.append(
                f"C{i-1} -->|{false_edge}| {cond_node}"
            )

        # 성공 분기
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

    # 마지막 실패 → 정상 처리
    if logic_ir.branches:

        last_cond = f"C{len(logic_ir.branches)-1}"

        lines.append(
            'SUCCESS["정상 처리"]'
        )

        lines.append(
            f"{last_cond} -->|NO| SUCCESS"
        )

        lines.append(
            "SUCCESS --> END"
        )

        lines.append(
            "class SUCCESS successNode"
        )

    lines.append("END([End])")

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

    # 시작 상태
    lines.append("[*] --> 상태확인0")

    for i, branch in enumerate(logic_ir.branches):

        current_state = f"상태확인{i}"

        next_state = (
            f"상태확인{i+1}"
            if i < len(logic_ir.branches) - 1
            else "정상처리"
        )

        # 조건 이름
        cond_var = (
            safe_text(branch.condition_var)
            if hasattr(branch, "condition_var") and branch.condition_var
            else safe_text(branch.plain_meaning)
        )

        # 너무 긴 조건 줄바꿈
        if len(cond_var) > 14:
            cond_var = (
                cond_var[:14]
                + "\\n"
                + cond_var[14:]
            )

        # 결과 상태
        result = prettify_result(
            safe_text(branch.result)
        )

        safe_result = result.replace(" ", "_")

        # 현재 상태 정의
        lines.append(
            f'state "{cond_var}" as {current_state}'
        )

        # YES → 결과 상태
        lines.append(
            f"{current_state} --> {safe_result} : YES"
        )

        # NO → 다음 조건
        lines.append(
            f"{current_state} --> {next_state} : NO"
        )

        # 결과 종료
        lines.append(
            f"{safe_result} --> [*]"
        )

    # 마지막 정상 처리
    lines.append(
        'state "정상 처리" as 정상처리'
    )

    lines.append(
        "정상처리 --> [*]"
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