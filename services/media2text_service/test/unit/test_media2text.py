from src import Media2Text

m2t = Media2Text()

image_path = "../../test/data/bill.jpg"
audio_path = "../../test/data/test.m4a"

print("========= Test Image to Text =========")
with open(image_path, "rb") as f:
    image_bytes = f.read()
text = m2t.image_to_text(image_bytes)
print(f"🖼️ OCR result from {image_path}:\n{text}\n")
print("========= Image to Text complete =========")

print("========= Test Audio to Text =========")
text = m2t.audio_to_text(audio_path)
print(f"🎤 Transcription result from {audio_path}:\n{text}\n")
print("========= Audio to Text complete =========")
