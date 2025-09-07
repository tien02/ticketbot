from abc import ABC, abstractmethod

from schema import UserMessage
from src.llm import LLM


class BasePipeline(ABC, LLM):
    @abstractmethod
    def run(self, user_message: UserMessage):
        raise NotImplementedError("Subclasses must implement `run`.")
