import requests

API_URL = "http://localhost:8040/chat"

test_msgs = [
    {"user_id": "U003", "message": "Customer wants to fly to NYC"},
    {"user_id": "U004", "message": "Customer needs to cancel their booking"},
    {"user_id": "U001", "message": "User is hungry and wants food delivered"},
    {"user_id": "U002", "message": "Tell me the weather in London"},
    {
        "user_id": "U003",
        "message": "Tôi không đi được lúc 7 giờ, có thể đổi sang ngày mai được không?",
    },
    {"user_id": "U004", "message": "Có thể dời chuyến đi của tôi sang tuần sau"},
    {"user_id": "U001", "message": "Tôi muốn hủy vé đặt chỗ."},
    {"user_id": "U002", "message": "Làm ơn hủy vé ngày mai giúp tôi."},
]

for msg in test_msgs:
    print(f"\nUser: {msg['message']}")
    try:
        response = requests.post(API_URL, json=msg)
        response.raise_for_status()
        print(f"Assistant: {response.json()['answer']}")
    except Exception as e:
        print(f"Error: {e}")
