import re

from src.llm import LLM


class IntentClassifier(LLM):
    CLASSIFY_PROMPT = """
    Classify the following message into one of these categories:
    - FAQ: asking for information about policies, services, or general inquiries
    - After-Service: requesting changes, cancellations, or support for existing bookings
    For example:

    Message: Làm thế nào để đặt vé máy bay trên Vexere?
    Category: FAQ

    Message: Làm sao để kiểm tra thông tin vé đã đặt?
    Category: FAQ

    Message: Tại sao không thể check-in online?
    Category: FAQ

    Message: Có thể dời chuyến đi của tôi sang tuần sau.
    Category: After-Service

    Message: Đổi vé sang ngày hôm sau giúp tôi.
    Category: After-Service

    Message: Tôi muốn hủy vé đặt chỗ.
    Category: After-Service

    Message: "{user_message}"
    \nRespond with only one of the categories.
    """

    PATTERNS = {
        "FAQ": r"\bFAQ\b[^\w]*",
        "After-Service": r"\bAfter[- ]?Service\b[^\w]*",
    }

    def classify(self, user_message: str) -> str:
        prompt = self.CLASSIFY_PROMPT.format(user_message=user_message)
        response = self.get_text_response(prompt)

        matches = []
        for label, pattern in self.PATTERNS.items():
            for m in re.finditer(pattern, response, re.IGNORECASE):
                matches.append((m.start(), label))

        if matches:
            # sort by match position, pick last
            return sorted(matches, key=lambda x: x[0])[-1][1]
        return "Unknown"
