from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone

from app.config import settings

embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)
pc = Pinecone(api_key=settings.pinecone_api_key)
index = pc.Index(settings.pinecone_index_name)

question = input("Your question: ")

q_vector = embeddings.embed_query(question)

result = index.query(
    vector=q_vector, top_k=3, include_metadata=True, namespace="docs"
)

for match in result.matches:
    print("")
    print("Score:", round(match.score, 3))
    print("Source:", match.metadata["source"], "| Page:", int(match.metadata["page"]))
    print(match.metadata["text"])