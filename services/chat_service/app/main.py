import logging

import uvicorn
from config import app_settings
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schema import UserMessage
from src import ChatService

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def read_root():
    return {"msg": "Welcome to Chat service"}


@app.post("/chat")
async def chat(req: UserMessage):
    logger.info(f"Inp: {req}")

    chat_service = ChatService()

    try:
        answer: str = chat_service.run(req)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=app_settings.APP_PORT,
    )
