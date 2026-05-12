LOGIC_IR_SYSTEM_PROMPT = """
너는 코드 로직을 구조화하는 분석기다.

역할:
- 입력된 코드를 설명하지 말고 Logic IR(JSON)로 변환한다.

핵심 규칙:
- 코드에 있는 내용만 사용하고, 없는 내용은 추측하지 않는다.
- Logic IR은 다음 요소를 포함해야 한다:
  - inputs
  - states
  - derived_values
  - branches
  - edge_cases
  - uncertainties

구조 규칙:
- state: 외부 입력 또는 상태값만 포함한다.
- derived_values: 계산된 값 또는 조건 결과를 표현한다.
- branch: 반드시 condition과 result를 포함한다.

summary 규칙:
- summary는 코드 설명이 아니라 "로직의 결정 구조"를 요약한다.
- 조건을 나열하지 말고 전체 흐름을 한 문장으로 표현한다.
- 조건이 없는 경우 "조건 없이 실행되는 단순 로직"으로 작성한다.

출력 규칙:
- 반드시 한국어로 작성한다.
- 반드시 JSON만 출력한다. (설명 금지)
- 반드시 지정된 JSON schema를 따른다.
"""


def build_logic_ir_user_prompt(code: str, language: str) -> str:
    return f"""
분석 대상 언어: {language}

아래 코드를 분석하여 Logic IR JSON을 생성하라.

반드시 포함:
1. 상태(state)
2. 파생값(derived_values) 특히 아래 패턴을 찾는다:
- boolean 변환 (!!)
- 조건 계산 결과
- 변수 기반 상태
3. 조건(branches)
4. UI 결과(result)

출력 형식:
{{
  "language": "{language}",
  "summary": "...",

  "inputs": ["..."],  

  "states": [
    {{
      "name": "...",
      "initial": "...",
      "meaning": "..."
    }}
  ],

  "derived_values": [
    {{
      "name": "...",
      "expression": "...",
      "meaning": "..."
    }}
  ],

  "branches": [
    {{
      "condition": "...",
      "result": "...",
      "plain_meaning": "..."
    }}
  ],

  "edge_cases": ["..."],
  "uncertainties": ["..."]
}}

코드:
```{language}
{code}
"""