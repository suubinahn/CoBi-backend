from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path

# .env 위치 강제 지정 + override
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env", override=True)


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def call_llm(system_prompt: str, user_prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content