import io

import pytesseract
import whisper
from config import model_settings
from PIL import Image


class Media2Text:
    def __init__(self):
        self.whisper_model = whisper.load_model(model_settings.WHISPER_MODEL_NAME)

    def image_to_text(self, image_bytes: bytes) -> str:
        try:
            image = Image.open(io.BytesIO(image_bytes))
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            raise RuntimeError(f"OCR failed: {str(e)}")

    def audio_to_text(self, file_path: str) -> str:
        try:
            result = self.whisper_model.transcribe(file_path)
            return result["text"].strip()
        except Exception as e:
            raise RuntimeError(f"Speech-to-text failed: {str(e)}")
