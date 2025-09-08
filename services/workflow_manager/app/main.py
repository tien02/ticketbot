import logging

import uvicorn
from config import app_settings
from fastapi import FastAPI, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from schema import WorkflowResponse
from src import WorkflowService

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging
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
    return {"msg": "Welcome to Workflow Manager service"}


@app.post("/process", response_model=WorkflowResponse)
async def process(
    user_id: str = Form(...),
    message: str = Form(None),
    file: UploadFile = None,
):
    logger.info(f"Received request for user_id={user_id}")

    workflow_service = WorkflowService()

    try:
        result = await workflow_service.run(user_id=user_id, message=message, file=file)
        return result
    except Exception as e:
        logger.error(f"Workflow error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=app_settings.APP_PORT,
    )
