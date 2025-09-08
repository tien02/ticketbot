from abc import ABC, abstractmethod

from schema import UserMessage
from src.llm import LLM


class BasePipeline(ABC, LLM):
    DEFAULT_PROMPT = """
    Bạn là một trợ lý hữu ích.
    Hãy trả lời câu hỏi một cách ngắn gọn và rõ ràng.
    Câu hỏi: {question}

    Trả lời bằng Tiếng Việt.
    """

    @abstractmethod
    def run(self, user_message: UserMessage):
        question = user_message.message
        prompt = self.DEFAULT_PROMPT.format(question=question)
        prompt = self.RAG_PROMPT.format(question=question)
        return self.get_text_response(prompt)
