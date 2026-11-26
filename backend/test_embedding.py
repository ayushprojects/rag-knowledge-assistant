import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings

from app.config import settings


def cosine(a, b):
    a, b = np.array(a), np.array(b)
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


print("Loading embedding model...")
embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)

query = "How many casual leaves do employees get?"
related = "Employees are entitled to 12 days of paid time off every year."
unrelated = "The cafeteria serves lunch from 12 to 2 pm."

q_vec = embeddings.embed_query(query)
r_vec = embeddings.embed_query(related)
u_vec = embeddings.embed_query(unrelated)

print("Vector length:", len(q_vec))
print("First 5 numbers:", [round(x, 3) for x in q_vec[:5]])
print("Similarity with related text:  ", round(cosine(q_vec, r_vec), 3))
print("Similarity with unrelated text:", round(cosine(q_vec, u_vec), 3))