from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rag import search, chat

app = FastAPI()

# CORS設定（必要に応じて調整）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(search.router, prefix="/search")
app.include_router(chat.router, prefix="/chat")

@app.get("/")
def root():
    return {"message": "LS-BOT backend is running."} 