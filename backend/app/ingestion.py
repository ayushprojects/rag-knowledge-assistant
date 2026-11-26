import os

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.clients import embeddings, index

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)


def load_pages(file_path):
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return PyPDFLoader(file_path).load()
    if extension == ".md":
        return TextLoader(file_path, encoding="utf-8").load()

    raise ValueError("Only .pdf and .md files are supported")


def ingest_file(file_path):
    file_name = os.path.basename(file_path)

    pages = load_pages(file_path)
    chunks = splitter.split_documents(pages)

    if not chunks:
        return 0

    texts = [c.page_content for c in chunks]
    vectors = embeddings.embed_documents(texts)

    records = []
    for i in range(len(chunks)):
        records.append(
            {
                "id": file_name + "-" + str(i),
                "values": vectors[i],
                "metadata": {
                    "text": texts[i],
                    "source": file_name,
                    "page": chunks[i].metadata.get("page", 0) + 1,
                },
            }
        )

    for start in range(0, len(records), 50):
        index.upsert(vectors=records[start : start + 50], namespace="docs")

    return len(records)