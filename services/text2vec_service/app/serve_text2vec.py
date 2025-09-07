import logging
from contextlib import asynccontextmanager

import uvicorn
from config import model_settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schema.service import Text2VecRequest, Text2VecResponse
from src import QwenEmbedder

logger = logging.getLogger("fastapi")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up... loading QwenEmbedder")

    app.state.embedder = QwenEmbedder(
        model_name=model_settings.MODEL_NAME_OR_PATH, use_half_precision=True
    )

    logger.info("QwenEmbedder loaded successfully")
    yield

    logger.info("Shutting down... cleaning up")
    del app.state.embedder


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"msg": "Welcome to Text to vector service"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/t2vec")
async def embed(inp: Text2VecRequest):
    logger.info(f"Inp: {inp}")
    embeddings = app.state.embedder.embed(texts=inp.texts)
    return Text2VecResponse(embeddings=embeddings.tolist())


if __name__ == "__main__":
    uvicorn.run("app.serve_text2vec:app", host="0.0.0.0", port=8010, reload=False)
