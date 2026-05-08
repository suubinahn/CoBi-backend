# CoBi Backend

코드를 분석하여 Logic IR, Mermaid 기반 시각화(flowchart/stateDiagram),
역할별 설명(PM / Designer / QA / CS)을 생성하는 FastAPI 기반 백엔드 서버입니다.

---

# Tech Stack

- Python
- FastAPI
- OpenAI API
- Mermaid
- Pydantic

---

# Run Server

## 1. Install

```bash
pip install -r requirements.txt
```

## 2. Run Server

```bash
uvicorn app.main:app --reload
```

## 3. Swagger Docs

```text
http://127.0.0.1:8000/docs
```

---

# **Deployment**

## **Render Backend URL**

```text
https://cobi-backend-k8ff.onrender.com
```

## **Production API Endpoint**

```text
POST https://cobi-backend-k8ff.onrender.com/api/analyze
```

## **Frontend Connection Example**

```javascript
fetch("https://cobi-backend-k8ff.onrender.com/api/analyze")
```

---

# API

## POST `/api/analyze`

코드를 분석하여:

- Logic IR
- Mermaid 시각화(flowchart / stateDiagram)
- 역할별 설명(role_views)
- warnings
- confidence

를 반환합니다.

---

# Request Example

```json
{
  "code": "def apply_discount(user, cart):\n    if user.isPremium and cart.total > 50000:\n        return 0.2\n    return 0"
}
```

---

# Response Structure

```json
{
  "detected_language": "python",
  "logic_ir": {},
  "visualizations": {},
  "role_views": {},
  "warnings": [],
  "confidence": 0.9
}
```

---

# Response Fields

| Field | Description |
|------|------|
| detected_language | 감지된 프로그래밍 언어 |
| logic_ir | 구조화된 로직 정보 |
| visualizations | Mermaid 기반 flowchart / stateDiagram |
| role_views | 역할별 설명 결과 |
| warnings | 검증 warning 목록 |
| confidence | 분석 신뢰도 |

---

# Visualization

백엔드는 Mermaid 문자열만 반환하며,
실제 다이어그램 렌더링은 frontend에서 처리해야 합니다.

예시:

```json
{
  "type": "flowchart",
  "mermaid": "flowchart TD\nSTART --> END"
}
```

---

# Project Structure

```text
app/
 ├─ api/
 ├─ prompts/
 ├─ schemas/
 ├─ services/
 └─ main.py
```

---

# Environment Variables

`.env` 파일 필요:

```env
OPENAI_API_KEY=your_api_key
```

---

# Notes

- FastAPI 기반 API 서버
- CORS 허용 설정 포함
- Mermaid 렌더링은 frontend에서 처리
- OpenAI API KEY 필요
- Swagger Docs 지원
- **Render 배포 서버 기준으로 frontend(Vercel)와 연결**