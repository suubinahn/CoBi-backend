def validate_logic_ir(logic_ir):
    warnings = []

    # 1. 완전 빈 구조 → warning
    if (
        not logic_ir.states
        and not logic_ir.derived_values
        and not logic_ir.branches
    ):
        warnings.append("로직 정보가 없는 단순 코드입니다.")
        return warnings  # 더 검사할 필요 없음

    # 2. branches 없음 → 단순 로직 처리
    if not logic_ir.branches:
        warnings.append("조건 분기 없이 실행되는 단순 로직입니다.")

    # 3. edge_case 없음 → warning
    if not logic_ir.edge_cases:
        warnings.append("엣지 케이스가 없습니다.")

    # 4. derived_values 없음 → warning
    if not logic_ir.derived_values:
        warnings.append("파생값이 없습니다.")

    # 5. state 타입 검사
    for state in logic_ir.states:
        if isinstance(state.initial, str):
            # 너무 일반적인 값이면 경고 안 함
            if state.initial.lower() not in ["true", "false"]:
                continue
            warnings.append(f"{state.name}의 초기값 타입이 문자열입니다.")

    # 6. inputs 없음 → warning
    if not getattr(logic_ir, "inputs", []):
        warnings.append("입력값 정보가 없습니다.")
    
    # 7. state 없음 → 안내
    if not logic_ir.states:
        warnings.append("상태 정보가 없어 기본 다이어그램으로 대체되었습니다.")


    return warnings