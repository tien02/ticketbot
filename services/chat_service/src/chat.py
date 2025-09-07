from schema import UserMessage
from src.intent_classify import IntentClassifier
from src.llm import LLM
from src.pipeline import AfterServicesPipeline, RAGPipeline


class ChatService(LLM):
    def run(self, usr_msg: UserMessage) -> str:
        intent = IntentClassifier().classify(usr_msg.message)
        if intent == "After-Service":
            pipeline = AfterServicesPipeline()
        elif intent == "FAQ":
            pipeline = RAGPipeline()
        else:
            return "I'm sorry, I couldn't understand your request. Could you please clarify?"

        return pipeline.run(usr_msg)
