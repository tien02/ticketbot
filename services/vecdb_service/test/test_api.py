import requests

API_URL = "http://localhost:8024"

# Example documents to insert
data = [
    {
        "question": "I want to book a flight to New York City.",
        "answer": "Sure, I can help you book a flight to NYC.",
    },
    {
        "question": "How do I cancel my booking?",
        "answer": "You can cancel your booking by visiting the 'My Trips' section or contacting support.",
    },
    {
        "question": "Can I order food delivery?",
        "answer": "Yes, you can order food delivery through our partner apps.",
    },
    {
        "question": "What’s the weather like in London today?",
        "answer": "The weather in London today is mostly cloudy with occasional rain showers.",
    },
]

# Insert multiple documents
for entry in data:
    payload = {
        "question": entry["question"],
        "answer": entry["answer"],
    }
    resp = requests.post(f"{API_URL}/insert", json=payload)
    resp.raise_for_status()
    uuid_ = resp.json().get("uuid")
    print(f"Inserted UUID: {uuid_} | Question: {entry['question']}")

# Perform search with different query scenarios
queries = [
    "Customer wants to fly to NYC",
    "Customer needs to cancel their booking",
    "User is hungry and wants food delivered",
    "Tell me the weather in London",
]

for q in queries:
    payload = {"query": q, "limit": 2}
    resp = requests.post(f"{API_URL}/search", json=payload)
    resp.raise_for_status()
    results = resp.json().get("results", [])
    print(f"\nSearch query: {q}")
    for r in results:
        print(f"Question: {r['question']}")
        print(f"Answer: {r['answer']}")
        print("---")

# Clean up database
# resp = requests.post(f"{API_URL}/clean")
# print(resp.text)
