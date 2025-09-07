import logging

import uvicorn
from config import app_settings, data_settings, embed_settings
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schema import (
    InsertRequest,
    InsertResponse,
    SearchRequest,
    SearchResponse,
    SearchResult,
)
from src import WeviateClient

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def read_root():
    return {"msg": "Welcome to Vector database service"}


@app.post("/insert")
def insert_item(req: InsertRequest):

    logger.info(f"Inp: {req}")

    client = WeviateClient(
        host=data_settings.VECTOR_DB_HOST,
        port=data_settings.VECTOR_DB_PORT,
        collection_name=data_settings.COLLECTION_NAME,
        embedding_url=embed_settings.EMBEDDING_URL,
    )

    try:
        obj_uuid: str = client.insert(input_data=req)
        return InsertResponse(status="SUCCESS", uuid=obj_uuid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        client.close()


@app.post("/search")
def search_item(req: SearchRequest):

    logger.info(f"Inp: {req}")

    client = WeviateClient(
        host=data_settings.VECTOR_DB_HOST,
        port=data_settings.VECTOR_DB_PORT,
        collection_name=data_settings.COLLECTION_NAME,
        embedding_url=embed_settings.EMBEDDING_URL,
    )

    try:
        results = client.search_by_question(query=req.query, limit=req.limit)

        formated_results = list()

        for r in results:
            res = SearchResult(
                question=r["properties"]["question"],
                answer=r["properties"]["answer"],
            )

            formated_results.append(res)

        return SearchResponse(status="SUCCESS", results=formated_results)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        client.close()


@app.post("/clean")
def clean_collection():
    client = WeviateClient(
        host=data_settings.VECTOR_DB_HOST,
        port=data_settings.VECTOR_DB_PORT,
        collection_name=data_settings.COLLECTION_NAME,
        embedding_url=embed_settings.EMBEDDING_URL,
    )

    try:
        client.clean()
        return {"status": "SUCCESS"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        client.close()


@app.get("/exists")
def check_collection_exists():
    client = WeviateClient(
        host=data_settings.VECTOR_DB_HOST,
        port=data_settings.VECTOR_DB_PORT,
        collection_name=data_settings.COLLECTION_NAME,
        embedding_url=embed_settings.EMBEDDING_URL,
    )
    try:
        exists = client.client.collections.exists(data_settings.COLLECTION_NAME)
        return {"collection": data_settings.COLLECTION_NAME, "exists": exists}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        client.close()


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=app_settings.APP_PORT,
    )
