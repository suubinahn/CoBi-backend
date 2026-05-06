from app.services.language_detector import detect_language
from app.services.logic_ir_generator import generate_logic_ir
from app.services.visualization_generator import generate_visualizations
from app.services.role_view_generator import generate_role_views
from app.services.verifier import validate_logic_ir
from app.services.harness_validator import validate_harness  
from app.services.logger import save_analysis_log


async def analyze_code(request):
    detected_language = detect_language(request.code)

    try:
        # 1. Logic IR 생성
        logic_ir = await generate_logic_ir(request.code, detected_language)

        # 2. Logic IR 검증
        warnings = validate_logic_ir(logic_ir)

        # 3. 시각화 생성
        visualizations = generate_visualizations(logic_ir)

        # 4. 하네스 검증
        harness_warnings = validate_harness(logic_ir, visualizations)
        warnings.extend(harness_warnings)

        # 5. role 설명
        roles = request.roles or ["pm", "designer", "qa", "cs"]
        
        role_views = await generate_role_views(
            logic_ir=logic_ir,
            visualizations=visualizations,
            roles=roles
        )

        # 6. confidence 계산
        confidence = 0.9
        if len(warnings) > 2:
            confidence = 0.7
        if len(warnings) > 4:
            confidence = 0.5

        result = {
            "detected_language": detected_language,
            "logic_ir": logic_ir,
            "visualizations": visualizations,
            "role_views": role_views,
            "warnings": warnings,
            "confidence": confidence
        }

        # 7. 성공 로그 저장
        save_analysis_log({
            "code": request.code,
            "language": detected_language,
            "logic_ir": logic_ir.model_dump(),
            "role_views": role_views,
            "warnings": warnings,
            "confidence": confidence,
            "error": None,
            "error_type": None
        })

        return result

    except Exception as e:
        # 실패 로그 저장
        save_analysis_log({
            "code": request.code,
            "language": detected_language,
            "logic_ir": None,
            "role_views": None,
            "warnings": [],
            "confidence": 0,
            "error": str(e),
            "error_type": "UNKNOWN_ERROR"
        })

        raise e