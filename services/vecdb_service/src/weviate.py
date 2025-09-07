import uuid

import requests
import weaviate
import weaviate.classes as wvc
from schema.app import InsertRequest
from weaviate.classes.config import Configure


class WeviateClient:
    def __init__(
        self,
        host: str,
        port: int,
        collection_name: str = "QuestionAnswerPairs",
        embedding_url: str = "http://localhost:8010/t2vec",
    ):
        self.client = weaviate.connect_to_local(host=host, port=port)
        self.collection_name = collection_name
        self.embedding_url = embedding_url

        if not self.client.collections.exists(collection_name):
            self.client.collections.create(
                name=collection_name,
                vectorizer_config=Configure.Vectorizer.none(),
                properties=[
                    wvc.config.Property(
                        name="question",
                        data_type=wvc.config.DataType.TEXT,
                        vectorize_property_name=False,
                    ),
                    wvc.config.Property(
                        name="answer",
                        data_type=wvc.config.DataType.TEXT,
                        vectorize_property_name=False,
                    ),
                ],
            )

        self.collection = self.client.collections.get(name=collection_name)

    def _get_embedding(self, query: str) -> list[float]:
        response = requests.post(self.embedding_url, json={"texts": query})
        response.raise_for_status()
        return response.json()["embeddings"][0]

    def insert(self, input_data: InsertRequest) -> str:
        query = f"Question: {input_data.question}. Answer: {input_data.answer}"

        vector = self._get_embedding(query)
        obj_uuid = (
            str(uuid.uuid4()) if input_data.obj_uuid is None else input_data.obj_uuid
        )

        self.collection.data.insert(
            uuid=obj_uuid,
            properties={
                "question": input_data.question,
                "answer": input_data.answer,
            },
            vector=vector,
        )
        return obj_uuid

    def search_by_question(self, query: str, limit: int = 1) -> list[dict]:
        query_vector = self._get_embedding(query)

        results = self.collection.query.near_vector(
            near_vector=query_vector,
            limit=limit,
            return_metadata=wvc.query.MetadataQuery(score=True),
        )

        return [
            {
                "uuid": obj.uuid,
                "score": getattr(obj.metadata, "score", None),
                "properties": obj.properties,
                "metadata": obj.metadata,
            }
            for obj in results.objects
        ]

    def delete(self, obj_uuid: str) -> bool:
        try:
            self.collection.data.delete_by_id(obj_uuid)
            return True
        except Exception as e:
            print(f"Delete error: {e}")
            return False

    def update(self, obj_uuid: str, updates: dict[str, str | list[str]]) -> bool:
        try:
            self.collection.data.update(uuid=obj_uuid, properties=updates)
            return True
        except Exception as e:
            print(f"Update error: {e}")
            return False

    def get_by_id(self, obj_uuid: str) -> dict | None:
        try:
            obj = self.collection.query.fetch_object_by_id(obj_uuid)
            return {"uuid": obj.uuid, "properties": obj.properties}
        except Exception:
            return None

    def close(self):
        self.client.close()

    def clean(self):
        if self.client.collections.exists(self.collection_name):
            self.client.collections.delete(self.collection_name)
