from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone

from app.config import settings

embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)
pc = Pinecone(api_key=settings.pinecone_api_key)
index = pc.Index(settings.pinecone_index_name)
llm = ChatGroq(api_key=settings.groq_api_key, model=settings.groq_model, temperature=0)

question = input("Your question: ")

# B1 + B2: sawal -> numbers -> Pinecone se chunks
q_vector = embeddings.embed_query(question)
result = index.query(vector=q_vector, top_k=3, include_metadata=True, namespace="docs")

# B3: prompt banao
context = ""
for i in range(len(result.matches)):
    chunk_text = result.matches[i].metadata["text"]
    context = context + f"[{i + 1}] {chunk_text}\n\n"

prompt = f"""You are a helpful assistant.
Answer the question using ONLY the context below.
If the answer is not in the context, say: I could not find this in the documents.

Context:
{context}
Question: {question}"""

# B4: LLM se jawab lo
response = llm.invoke(prompt)

# B5: jawab + source dikhao
print("")
print("Answer:", response.content)
print("")
print("Sources:")
for match in result.matches:
    print("-", match.metadata["source"], "| page", int(match.metadata["page"]))