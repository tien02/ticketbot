import os

import requests

API_URL = "http://localhost:8080/process"


def test_text_only():
    data = {
        "user_id": "U001",
        "message": "What is the weather in London?",
    }
    resp = requests.post(API_URL, data=data)
    print("\n📩 Text Only:")
    print(resp.status_code, resp.json())


def test_file_only():
    file_path = "test/data/bill.jpg"  # change to your path
    if not os.path.exists(file_path):
        print(f"⚠️ Skipping file-only test, file not found: {file_path}")
        return

    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f, "image/jpeg")}
        data = {"user_id": "U002"}
        resp = requests.post(API_URL, data=data, files=files)
        print("\n🖼️ File Only:")
        print(resp.status_code, resp.json())


def test_text_and_file():
    file_path = "test/data/test.m4a"  # change to your path
    if not os.path.exists(file_path):
        print(f"⚠️ Skipping text+file test, file not found: {file_path}")
        return

    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f, "audio/m4a")}
        data = {
            "user_id": "U003",
            "message": "Can you also tell me if I can reschedule this?",
        }
        resp = requests.post(API_URL, data=data, files=files)
        print("\n🎤 Text + File:")
        print(resp.status_code, resp.json())


if __name__ == "__main__":
    test_text_only()
    test_file_only()
    test_text_and_file()
