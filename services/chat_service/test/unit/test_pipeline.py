from schema import UserMessage
from src.pipeline import AfterServicesPipeline, RAGPipeline

rag = RAGPipeline()

test_msgs = [
    UserMessage(user_id="U003", message="Customer wants to fly to NYC"),
    UserMessage(user_id="U004", message="Customer needs to cancel their booking"),
    UserMessage(user_id="U001", message="User is hungry and wants food delivered"),
    UserMessage(user_id="U002", message="Tell me the weather in London"),
]

for test_msg in test_msgs:
    print(f"\nUser: {test_msg.message}")
    answer = rag.run(test_msg)
    print(f"Assistant: {answer}")

print("======= Test FAQ pipeline completed =======")

test_msgs = [
    UserMessage(
        user_id="U003",
        message="Tôi không đi được lúc 7 giờ, có thể đổi sang ngày mai được không?",
    ),
    UserMessage(user_id="U004", message="Có thể dời chuyến đi của tôi sang tuần sau"),
    UserMessage(user_id="U001", message="Tôi muốn hủy vé đặt chỗ."),
    UserMessage(user_id="U002", message="Làm ơn hủy vé ngày mai giúp tôi."),
]

for test_msg in test_msgs:
    print(f"\nUser: {test_msg.message}")
    after_service = AfterServicesPipeline()
    answer = after_service.run(test_msg)
    print(f"Assistant: {answer}")

print("======= Test AfterServices pipeline completed =======")
