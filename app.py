import os
import json
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google import genai
from google.genai import types
from dotenv import load_dotenv
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

load_dotenv()

app = FastAPI(title="The Flash-Debate Arena")
app.mount("/static", StaticFiles(directory="static"), name="static")

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# 무료 티어 할당량이 더 넉넉한 1.5 Flash를 기본으로 사용 (분당 15회 가능)
model_id = "gemini-1.5-flash"


class DebateRequest(BaseModel):
    topic: str
    history: list = []


class FactCheckRequest(BaseModel):
    claim: str


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(Exception),
)
def generate_safe_content(contents, system_instruction, tools=None, is_json=False):
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        tools=tools,
        temperature=0.7,
        response_mime_type="application/json" if is_json else "text/plain",
    )
    return client.models.generate_content(
        model=model_id, contents=contents, config=config
    )


@app.post("/debate_batch")
async def debate_batch(request: DebateRequest):
    """
    한 번의 API 호출로 3명의 페르소나 답변을 모두 생성하며, 페르소나의 개성을 상세히 유지합니다.
    """
    system_inst = """당신은 3명의 서로 다른 토론자를 연기하는 시스템입니다.
1. philosopher (논리 술사): 이성적이고 철학적이며, 전통적인 가치와 윤리를 중시합니다. 차분하고 논리적인 문어체를 사용하며 인문학적 식견을 담아 한국어로 답변하세요.
2. chaos (혼돈의 사도): 상식을 파괴하고 창의적이며 도발적입니다. 유머러스하고 에너지 넘치는 구어체를 사용하며 틀에 박히지 않은 시각을 유지하세요. 한국어로 답변하세요.
3. scientist (데이터 가디언): 철저하게 객관적이고 통계와 과학적 근거만을 신봉합니다. 수치와 연구 결과를 언급하며 냉철하게 한국어로 답변하세요.

반드시 지정된 JSON 형식으로만 답변해야 합니다."""

    batch_prompt = f"""
토론 주제: {request.topic}
최근 대화 맥락: {json.dumps(request.history[-4:] if request.history else [], ensure_ascii=False)}

위 주제와 맥락에 대해 3명의 페르소나가 각자의 입장에서 답변하세요. 
답변은 서로의 의견을 부분적으로 참고하거나 반박하며 토론의 활기를 띄어야 합니다.

JSON 형식:
{{
  "philosopher": "...",
  "chaos": "...",
  "scientist": "..."
}}
"""
    try:
        response = generate_safe_content(batch_prompt, system_inst, is_json=True)
        return json.loads(response.text)
    except Exception as e:
        print(f"Batch Debate Error: {str(e)}")
        return {
            "philosopher": "시스템 부하로 인해 답변을 생성하기 어렵습니다.",
            "chaos": "에너지가 부족하네요! 잠시 후 다시 시도해주세요.",
            "scientist": "데이터 수신에 기술적 문제가 발생했습니다.",
        }


@app.post("/factcheck")
async def factcheck(request: FactCheckRequest):
    arbiter_prompt = """당신은 '중재자(The Arbiter)'입니다. 
제시된 주장의 사실 여부를 Google 검색으로 검증하고 리포트를 한국어로 작성하세요."""

    try:
        response = generate_safe_content(
            f"다음 주장을 팩트체크 해주세요: {request.claim}",
            arbiter_prompt,
            tools=[types.Tool(google_search=types.GoogleSearch())],
        )
        if not response.text:
            return {"text": "중재자가 자료 조사를 거부했습니다."}
        return {"text": response.text}
    except Exception as e:
        print(f"Factcheck Error: {str(e)}")
        return {"text": f"팩트체크 중 오류가 발생했습니다: {str(e)}"}


@app.get("/")
async def read_index():
    from fastapi.responses import FileResponse

    return FileResponse("static/index.html")
