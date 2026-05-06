import json
from datetime import datetime

def save_analysis_log(data: dict):
    log = {
        "id": datetime.utcnow().timestamp(),
        "input_code": data.get("code"),
        "detected_language": data.get("language"),
        "logic_ir": data.get("logic_ir"),
        "explanations": data.get("role_views"),
        "warnings": data.get("warnings"),
        "confidence": data.get("confidence"),
        "error_type": data.get("error"),
        "created_at": datetime.utcnow().isoformat()
    }

    with open("analysis_logs.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log, ensure_ascii=False) + "\n")