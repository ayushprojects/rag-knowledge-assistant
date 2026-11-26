import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone

from app.config import settings

file_path = "sample_docs/sample.pdf"
file_name = os.path.basename(file_path)

# A1: PDF padho
pages = PyPDFLoader(file_path).load()

# A2: Chunks banao
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(pages)

# A3: Embeddings banao
embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)
texts = [c.page_content for c in chunks]
vectors = embeddings.embed_documents(texts)

# A4: Pinecone mein store karo
pc = Pinecone(api_key=settings.pinecone_api_key)
index = pc.Index(settings.pinecone_index_name)

records = []
for i in range(len(chunks)):
    records.append(
        {
            "id": file_name + "-" + str(i),
            "values": vectors[i],
            "metadata": {
                "text": texts[i],
                "source": file_name,
                "page": chunks[i].metadata["page"] + 1,
            },
        }
    )

for start in range(0, len(records), 50):
    index.upsert(vectors=records[start : start + 50], namespace="docs")

print("Stored", len(records), "chunks from", file_name)