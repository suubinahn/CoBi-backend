import json
from app.services.llm_client import call_llm
from app.prompts.role_prompt import (
    get_role_system_prompt,
    build_role_user_prompt
)


# JSON 클린
def clean_json(response: str) -> str:
    if "```" in response:
        parts = response.split("```")
        if len(parts) >= 2:
            response = parts[1]
        if response.startswith("json"):
            response = response[4:]
    return response.strip()


# fallback
def fallback_response():
    return {
        "primary_visualization": "flowchart",
        "title": "생성 실패",
        "summary": "설명 생성 중 오류 발생",
        "key_points": [],
        "questions_to_confirm": []
    }


# 메인
async def generate_role_views(logic_ir, visualizations, roles):
    role_views = {}

    logic_ir_json = json.dumps(logic_ir.model_dump(), ensure_ascii=False)

    for role in roles:
        system_prompt = get_role_system_prompt(role)
        user_prompt = build_role_user_prompt(logic_ir_json)

        for attempt in range(2):  # 재시도 1회
            try:
                response = await call_llm(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt
                )

                cleaned = clean_json(response)
                data = json.loads(cleaned)

                # 필수 필드 보정
                data["primary_visualization"] = "flowchart"

                role_views[role] = data
                break

            except Exception as e:
                print(f"ROLE 생성 실패 ({role}) - 시도 {attempt+1}")

                if attempt == 1:
                    role_views[role] = fallback_response()

    return role_views