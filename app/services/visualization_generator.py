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


def prettify_result(raw_result: str):

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


def get_result_class(result: str):

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


# =========================================================
# FLOWCHART
# =========================================================

def generate_flowchart(logic_ir):

    lines = ["flowchart TD"]

    lines.append("START([Start])")

    for i, branch in enumerate(logic_ir.branches):

        cond_node = f"C{i}"
        res_node = f"R{i}"

        condition_label = safe_text(
            branch.condition_var if branch.condition_var else branch.plain_meaning
        )

        true_edge = safe_text(branch.true_label) or "YES"

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

    # 마지막 NO → 정상 처리
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


# =========================================================
# [수정] STATE DIAGRAM
# 기존 condition 중심 → 상태(state) 중심 구조로 변경
# =========================================================

def generate_state_diagram(logic_ir):

    lines = ["stateDiagram-v2"]

    # =====================================================
    # 시작 상태
    # =====================================================

    lines.append("[*] --> 시작")

    current_state = "시작"

    for i, branch in enumerate(logic_ir.branches):

        # =================================================
        # [수정] plain_meaning 기반 사용
        # condition_var 대신 사용자 친화적 의미 사용
        # =================================================

        meaning = safe_text(branch.plain_meaning)

        result = prettify_result(
            safe_text(branch.result)
        )

        safe_result = result.replace(" ", "_")

        # =================================================
        # [수정] 상태(state) 이름 생성
        # =================================================

        if "로그인" in meaning:
            next_state = "로그인확인"

        elif "금액" in meaning:
            next_state = "금액검증"

        elif "승인" in meaning:
            next_state = "승인처리"

        elif "재고" in meaning:
            next_state = "재고확인"

        elif "비밀번호" in meaning:
            next_state = "비밀번호확인"

        elif "인증" in meaning:
            next_state = "추가인증"

        else:
            next_state = f"상태{i}"

        # =================================================
        # [수정] 시작 → 첫 상태
        # =================================================

        if current_state == "시작":

            lines.append(
                f"시작 --> {next_state}"
            )

        # =================================================
        # [수정] 실패 상태 연결
        # =================================================

        lines.append(
            f"{next_state} --> {safe_result} : 실패"
        )

        lines.append(
            f"{safe_result} --> [*]"
        )

        # =================================================
        # [수정] 다음 단계 상태 흐름
        # =================================================

        if i < len(logic_ir.branches) - 1:

            next_flow_state = f"FLOW_{i}"

            next_branch = logic_ir.branches[i + 1]

            next_meaning = safe_text(
                next_branch.plain_meaning
            )

            # =============================================
            # 다음 상태 transition label
            # =============================================

            if "로그인" in next_meaning:
                flow_label = "로그인 성공"

            elif "금액" in next_meaning:
                flow_label = "금액 확인"

            elif "승인" in next_meaning:
                flow_label = "승인 필요"

            elif "재고" in next_meaning:
                flow_label = "재고 있음"

            elif "인증" in next_meaning:
                flow_label = "인증 진행"

            else:
                flow_label = "다음 단계"

            # =============================================
            # 상태 이동
            # =============================================

            lines.append(
                f"{next_state} --> {next_flow_state} : 성공"
            )

            lines.append(
                f'{next_flow_state} : {flow_label}'
            )

            current_state = next_flow_state

        else:

            # =============================================
            # 마지막 정상 처리
            # =============================================

            lines.append(
                f"{next_state} --> 정상처리 : 성공"
            )

            lines.append(
                "정상처리 --> [*]"
            )

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