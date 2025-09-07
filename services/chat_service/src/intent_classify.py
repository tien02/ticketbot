import re

from src.llm import LLM


class IntentClassifier(LLM):
    CLASSIFY_PROMPT = """
    Classify the following message into one of these categories:
    - FAQ: asking for information about policies, services, or general inquiries
    - After-Service: requesting changes, cancellations, or support for existing bookings
    - Booking: making new reservations or inquiries about availability

    Message: "{user_message}"
    \nRespond with only one of the categories.
    """

    PATTERNS = {
        "FAQ": r"\bFAQ\b[^\w]*",
        "After-Service": r"\bAfter[- ]?Service\b[^\w]*",
        "Booking": r"\bBooking\b[^\w]*",
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
