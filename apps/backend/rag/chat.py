from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import os
from openai import OpenAI
from dotenv import load_dotenv

router = APIRouter()

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

class ChatRequest(BaseModel):
    category: str
    message: str

class ChatResponse(BaseModel):
    reply: str

@router.post("", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    # /searchエンドポイントを内部呼び出し
    async with httpx.AsyncClient() as ac:
        resp = await ac.post("http://localhost:8000/search", json={"query": req.message, "n_results": 10})
        if resp.status_code != 200:
            raise HTTPException(status_code=500, detail="search failed")
        search_results = resp.json()

    context = ""
    if search_results.get('results'):
        context = "参考情報:\n"
        for i, result in enumerate(search_results['results'], 1):
            context += f"{i}. {result['text']} (出典: {result.get('url', '')})\n"

    # 参考情報がある場合は必ずそれを根拠に回答するよう明示
    if context:
        prompt = f"""あなたはIDOLY PRIDE公式サイトの情報のみを根拠に回答するカスタマーサポートBotです。\n\n【重要な指示】\n- 下記の参考情報のみを根拠に、必ず何らかの情報を回答してください。\n- 参考情報が質問内容に直接関係しない場合も、参考情報の内容を要約・抜粋して伝えてください。\n- 回答は日本語で、親しみやすく丁寧な口調でお願いします。\n\n【カテゴリー】{req.category}\n【ユーザーの質問】{req.message}\n\n{context}\n上記の指示に従って、ユーザーの質問に回答してください。"""
    else:
        prompt = f"""あなたはIDOLY PRIDE公式サイトの情報のみを根拠に回答するカスタマーサポートBotです。\n\n【重要な指示】\n- 参考情報がない場合は「申し訳ございませんが、公式サイトに記載がありません」と明記してください。\n- 回答は日本語で、親しみやすく丁寧な口調でお願いします。\n\n【カテゴリー】{req.category}\n【ユーザーの質問】{req.message}\n\n上記の指示に従って、ユーザーの質問に回答してください。"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "あなたはIDOLY PRIDE公式サイトの情報のみを根拠に回答するカスタマーサポートBotです。参考情報以外の知識や推測は一切使わないでください。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.2
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"申し訳ございません。エラーが発生しました: {str(e)}"
    return ChatResponse(reply=reply) 