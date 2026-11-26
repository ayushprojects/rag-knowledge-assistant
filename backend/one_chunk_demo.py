import time

from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone

from app.config import settings

embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)
pc = Pinecone(api_key=settings.pinecone_api_key)
index = pc.Index(settings.pinecone_index_name)

text = "Casual Leave: Every employee is entitled to 12 days of casual leave per calendar year."
vector = embeddings.embed_query(text)

index.upsert(
    vectors=[{"id": "c1", "values": vector, "metadata": {"text": text}}],
    namespace="demo",
)
print("Stored 1 chunk")

time.sleep(5)

result = index.fetch(ids=["c1"], namespace="demo")
record = result.vectors["c1"]
print("Vector length:", len(record.values))
print("Text:", record.metadata["text"])