from pinecone import Pinecone, ServerlessSpec

from app.config import settings

pc = Pinecone(api_key=settings.pinecone_api_key)

pc.create_index(
    name=settings.pinecone_index_name,
    dimension=settings.embedding_dimension,
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
)

print("Index created")