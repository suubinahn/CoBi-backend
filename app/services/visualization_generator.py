def safe_text(text: str):
    if not text:
        return ""

    return (
        str(text)
        .replace('"', "'")
        .replace("\n", " ")
        .replace("{", "(")
        .replace("}", ")")
    )


# =========================================================
# [수정]
# 기존 하드코딩 prettify_result 제거 방향
# fallback 용도로만 최소 유지
# =========================================================

def prettify_result(raw_result: str):

    raw_result = raw_result.lower()

    if "error" in raw_result:
        return "오류"

    elif "pending" in raw_result:
        return "대기"

    elif "success" in raw_result:
        return "성공"

    return "결과"


# =========================================================
# [수정]
# severity 기반 스타일 사용
# 기존 result 이름 기반 분기 제거
# =========================================================

def get_result_class(severity: str):

    severity = safe_text(severity).lower()

    if severity == "error":
        return "errorNode"

    elif severity == "warning":
        return "pendingNode"

    elif severity == "success":
        return "successNode"

    return "defaultNode"


# =========================================================
# FLOWCHART
# =========================================================

def generate_flowchart(logic_ir):

    lines = ["flowchart TD"]

    lines.append("START([Start])")

    for i, branch in enumerate(logic_ir.branches):

        cond_node = f"C{i}"
        res_node = f"R{i}"

        # =================================================
        # 조건 라벨
        # =================================================

        condition_label = safe_text(
            branch.condition_var
            if branch.condition_var
            else branch.plain_meaning
        )

        true_edge = safe_text(
            branch.true_label
        ) or "YES"

        # =================================================
        # [수정]
        # LLM 생성 ui_message 사용
        # =================================================

        result = safe_text(
            branch.ui_message
        )

        # fallback
        if not result:
            result = prettify_result(
                safe_text(branch.result)
            )

        # =================================================
        # [수정]
        # severity 사용
        # =================================================

        result_class = get_result_class(
            branch.severity
        )

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

            prev_false = safe_text(
                logic_ir.branches[i-1].false_label
            ) or "NO"

            lines.append(
                f"C{i-1} -->|{prev_false}| {cond_node}"
            )

        # YES → 결과
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

    # =====================================================
    # 마지막 NO → 정상 처리
    # =====================================================

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

    # =====================================================
    # 스타일 정의
    # =====================================================

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


# =========================================================
# STATE DIAGRAM
# 완전 LLM semantic 기반
# =========================================================

def generate_state_diagram(logic_ir):

    lines = ["stateDiagram-v2"]

    # =====================================================
    # 시작 상태
    # =====================================================

    lines.append("[*] --> 시작")

    previous_state = "시작"

    for i, branch in enumerate(logic_ir.branches):

        # =================================================
        # [수정]
        # state_name 사용
        # =================================================

        state_name = safe_text(
            branch.state_name
        ) or f"상태{i}"

        safe_state = state_name.replace(" ", "_")

        # =================================================
        # [수정]
        # ui_message 사용
        # =================================================

        result = safe_text(
            branch.ui_message
        )

        if not result:
            result = prettify_result(
                safe_text(branch.result)
            )

        safe_result = result.replace(" ", "_")

        # =================================================
        # 이전 상태 → 현재 상태
        # =================================================

        lines.append(
            f"{previous_state} --> {safe_state}"
        )

        # =================================================
        # [수정]
        # transition_label 사용
        # =================================================

        transition_label = safe_text(
            branch.transition_label
        ) or "실패"

        # 결과 상태 연결
        lines.append(
            f"{safe_state} --> {safe_result} : {transition_label}"
        )

        lines.append(
            f"{safe_result} --> [*]"
        )

        # =================================================
        # 마지막 상태 → 정상 처리
        # =================================================

        if i == len(logic_ir.branches) - 1:

            lines.append(
                f"{safe_state} --> 정상처리 : 성공"
            )

            lines.append(
                "정상처리 --> [*]"
            )

        previous_state = safe_state

    return "\n".join(lines)


# =========================================================
# VISUALIZATION EXPORT
# =========================================================

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