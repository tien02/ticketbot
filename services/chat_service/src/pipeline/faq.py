import requests
from config import model_settings
from schema import UserMessage

from ._base import BasePipeline


class RAGPipeline(BasePipeline):
    RAG_PROMPT = """
    You are a helpful assistant.
    Answer the question using the retrieved context.
    Give me a concise and clear answer.
    Try not to hallucinate.

    Question: {question}

    Context:
    {context_text}

    Final Answer:
    """

    def run(self, user_message: UserMessage) -> str:
        context = self._retrieve_context(query=user_message.message)
        return self._generate_response(user_message.message, context)

    def _retrieve_context(self, query: str, top_k: int = 1):
        payload = {"query": query, "limit": top_k}
        resp = requests.post(model_settings.RETRIEVAL_URL, json=payload)
        resp.raise_for_status()
        return resp.json().get("results", [])

    def _generate_response(self, question: str, context: list):
        if not context:
            return "Sorry, I couldn't find relevant information."

        context_text = "\n\n".join(
            [f"Context {idx}: {c['answer']}" for idx, c in enumerate(context)]
        )
        prompt = self.RAG_PROMPT.format(question=question, context_text=context_text)
        return self.get_text_response(prompt)
