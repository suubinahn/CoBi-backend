import json
import re
from app.schemas.logic_ir import LogicIR
from app.services.llm_client import call_llm
from app.prompts.logic_ir_prompt import (
    LOGIC_IR_SYSTEM_PROMPT,
    build_logic_ir_user_prompt
)


# JSON 클린 (코드블록 제거)
def clean_json(response: str) -> str:
    if "```" in response:
        parts = response.split("```")
        if len(parts) >= 2:
            response = parts[1]
        if response.startswith("json"):
            response = response[4:]
    return response.strip()


# 타입 보정
def normalize_types(logic_ir: LogicIR) -> LogicIR:
    for state in logic_ir.states:
        if state.initial in ["true", "True"]:
            state.initial = True
        elif state.initial in ["false", "False"]:
            state.initial = False
        elif state.initial == "0":
            state.initial = 0
    return logic_ir


# fallback
def ensure_derived_values(logic_ir: LogicIR) -> LogicIR:
    if not logic_ir.derived_values and logic_ir.states:
        logic_ir.derived_values.append({
            "name": "derived_from_state",
            "expression": "state 기반 파생값",
            "meaning": "상태 기반 계산 값"
        })
    return logic_ir


# state → input 분리
def separate_inputs_and_states(logic_ir: LogicIR) -> LogicIR:
    new_states = []
    inputs = []

    for state in logic_ir.states:
        if "." in state.name:
            inputs.append(state.name)
        else:
            new_states.append(state)

    logic_ir.states = new_states
    logic_ir.inputs.extend(inputs)

    return logic_ir


# input 정리
def deduplicate_inputs(logic_ir: LogicIR) -> LogicIR:
    filtered = []

    for inp in logic_ir.inputs:
        if "." not in inp:
            continue
        filtered.append(inp)

    logic_ir.inputs = list(set(filtered))
    return logic_ir


# 코드 기반 input 추출
def extract_inputs_from_code(code: str) -> list[str]:
    matches = re.findall(r"\b[a-zA-Z_]\w*\.\w+\b", code)
    return list(set(matches))


# derived 기반 input 추출
def extract_inputs_from_derived(logic_ir: LogicIR) -> list[str]:
    inputs = []

    for dv in logic_ir.derived_values:
        matches = re.findall(r"\b[a-zA-Z_]\w*\.\w+\b", dv.expression)
        inputs.extend(matches)

    return list(set(inputs))


# 메인 (재시도 포함)
async def generate_logic_ir(code: str, language: str) -> LogicIR:
    user_prompt = build_logic_ir_user_prompt(code, language)

    for attempt in range(2):  # 🔥 1회 재시도
        try:
            response = await call_llm(
                system_prompt=LOGIC_IR_SYSTEM_PROMPT,
                user_prompt=user_prompt
            )

            cleaned = clean_json(response)
            data = json.loads(cleaned)

            # 1. 객체 생성
            logic_ir = LogicIR(**data)

            # 2. 타입 보정
            logic_ir = normalize_types(logic_ir)

            # 3. fallback
            logic_ir = ensure_derived_values(logic_ir)

            # 4. state → input 분리
            logic_ir = separate_inputs_and_states(logic_ir)

            # 5. input 정리
            logic_ir = deduplicate_inputs(logic_ir)

            # 6. 코드 기반 input
            code_inputs = extract_inputs_from_code(code)

            # 7. derived 기반 input
            derived_inputs = extract_inputs_from_derived(logic_ir)

            # 최종 병합
            logic_ir.inputs = list(set(
                logic_ir.inputs + code_inputs + derived_inputs
            ))

            return logic_ir

        except Exception as e:
            print(f"JSON 파싱 실패 (시도 {attempt+1}):", response)

            if attempt == 1:
                raise ValueError("Logic IR 생성 실패 (JSON 파싱 오류)") from e