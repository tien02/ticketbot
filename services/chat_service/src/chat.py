import logging

from schema import UserMessage
from src.intent_classify import IntentClassifier
from src.llm import LLM
from src.pipeline import AfterServicesPipeline, BasePipeline, RAGPipeline

logger = logging.getLogger(__name__)


class ChatService(LLM):
    def run(self, usr_msg: UserMessage) -> str:
        intent = IntentClassifier().classify(usr_msg.message)

        logger.info(f"[user={usr_msg.user_id}] Classified intent: {intent}")

        if intent == "After-Service":
            pipeline = AfterServicesPipeline()
        elif intent == "FAQ":
            pipeline = RAGPipeline()
        else:
            pipeline = BasePipeline()

        return pipeline.run(usr_msg)
