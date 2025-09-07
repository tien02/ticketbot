import os

import requests

API_URL = "http://localhost:8050"


def test_image_upload():
    image_path = "../../test/data/bill.jpg"
    if not os.path.exists(image_path):
        print(f"⚠️ Skipping image test, file not found: {image_path}")
        return

    with open(image_path, "rb") as f:
        files = {"file": ("test_image.png", f, "image/png")}
        response = requests.post(f"{API_URL}/media2text", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "image"
    print("🖼️ OCR Result:", data["text"])


def test_audio_upload():
    audio_path = "../../test/data/test.m4a"
    if not os.path.exists(audio_path):
        print(f"⚠️ Skipping audio test, file not found: {audio_path}")
        return

    with open(audio_path, "rb") as f:
        files = {"file": ("test_audio.wav", f, "audio/wav")}
        response = requests.post(f"{API_URL}/media2text", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "audio"
    print("🎤 Transcription Result:", data["text"])


if __name__ == "__main__":
    test_image_upload()
    test_audio_upload()
