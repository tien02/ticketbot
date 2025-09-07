import logging
import os

import uvicorn
from config import app_settings
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from src import Media2Text

app = FastAPI(title="Media2Text Service")
media2text = Media2Text()

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
    return {"msg": "Welcome to Media to text service"}


@app.post("/media2text")
async def media_to_text(file: UploadFile = File(...)):
    logger.info(f"Received file: {file.filename}, content_type: {file.content_type}")
    content_type = file.content_type

    try:
        if content_type.startswith("image/"):
            image_bytes = await file.read()
            text = media2text.image_to_text(image_bytes)
            return {"type": "image", "text": text}

        elif content_type.startswith("audio/") or content_type in ["video/mp4"]:
            tmp_path = f"/tmp/{file.filename}"
            with open(tmp_path, "wb") as f:
                f.write(await file.read())
            text = media2text.audio_to_text(tmp_path)
            os.remove(tmp_path)  # cleanup
            return {"type": "audio", "text": text}

        else:
            raise HTTPException(
                status_code=400, detail=f"Unsupported file type: {content_type}"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=app_settings.APP_PORT)
