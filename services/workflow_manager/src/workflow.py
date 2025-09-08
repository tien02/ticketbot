import logging

import requests
from config import app_settings
from fastapi import UploadFile

logger = logging.getLogger(__name__)


class WorkflowService:
    async def run(self, user_id: str, message: str = None, file: UploadFile = None):
        parts = []

        if file:
            try:
                logger.info(f"[user={user_id}] Processing file: {file.filename}")
                files = {"file": (file.filename, await file.read(), file.content_type)}
                media_resp = requests.post(
                    app_settings.MEDIA_URL, files=files, timeout=30
                )
                media_resp.raise_for_status()
                media_data = media_resp.json()

                media_text = media_data.get("text", "").strip()
                if not media_text:
                    raise ValueError("Media2Text service returned no text")

                parts.append(f"With this information: {media_text}")
                logger.info(f"[user={user_id}] Extracted text from file")

            except Exception as e:
                logger.error(f"[user={user_id}] Media2Text error: {e}")
                parts.append(
                    "⚠️ Sorry, I couldn’t extract text from the provided file."
                )

        if message:
            logger.info(f"[user={user_id}] Received message: {message}")
            parts.append(f"My question is: {message}")

        if not parts:
            logger.warning(f"[user={user_id}] No input provided")
            raise ValueError("No input provided (neither text nor file)")

        input_text = " ".join(parts)
        logger.debug(f"[user={user_id}] Final input_text: {input_text}")

        try:
            chat_resp = requests.post(
                app_settings.CHAT_URL,
                json={"user_id": user_id, "message": input_text},
                timeout=30,
            )
            chat_resp.raise_for_status()
            chat_data = chat_resp.json()
            chat_answer = chat_data.get("answer", "⚠️ No response from chat service")
            logger.info(f"[user={user_id}] Got chat response")
        except Exception as e:
            logger.error(f"[user={user_id}] Chat service error: {e}")
            raise RuntimeError(f"Chat service error: {e}")

        return {
            "user_id": user_id,
            "input_text": input_text,
            "chat_response": chat_answer,
        }
