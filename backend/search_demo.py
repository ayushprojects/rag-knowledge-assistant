import time

from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone

from app.config import settings

embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)
pc = Pinecone(api_key=settings.pinecone_api_key)
index = pc.Index(settings.pinecone_index_name)

texts = [
    "Casual Leave: Every employee is entitled to 12 days of casual leave per calendar year.",
    "Work From Home: Employees may work from home up to 2 days per week with manager approval.",
    "Exit Process: The notice period for all employees is 60 days.",
    "The cafeteria serves lunch from 12 pm to 2 pm on all working days.",
]

vectors = embeddings.embed_documents(texts)

records = []
for i in range(len(texts)):
    records.append(
        {"id": "c" + str(i + 1), "values": vectors[i], "metadata": {"text": texts[i]}}
    )

index.upsert(vectors=records, namespace="demo")
print("Stored", len(records), "chunks")

time.sleep(5)

question = "How many days of leave do I get in a year?"
q_vector = embeddings.embed_query(question)

result = index.query(vector=q_vector, top_k=2, include_metadata=True, namespace="demo")

print("Question:", question)
for match in result.matches:
    print(round(match.score, 3), "|", match.metadata["text"])