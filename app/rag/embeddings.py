from openai import OpenAI

from app.core.config import settings
from app.core.openai_client import client

def create_embedding(
    text: str,
):

    response = client.embeddings.create(
        model=settings.OPENAI_EMBEDDING_MODEL,
        input=text,
    )

    return response.data[0].embedding