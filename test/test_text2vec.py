import requests

API_URL = "http://localhost:8010/t2vec"

queries = ["What is the capital of China?", "Explain gravity"]

# --- Test 1: With list of texts only
response = requests.post(API_URL, json={"texts": queries})
print(
    "Test 1 - embeddings shape:",
    len(response.json()["embeddings"]),
    "x",
    len(response.json()["embeddings"][0]),
)
