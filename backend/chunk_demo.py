from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = PyPDFLoader("sample_docs/sample.pdf")
pages = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(pages)

print("Pages:", len(pages))
print("Chunks:", len(chunks))
print("Chunk 1 length:", len(chunks[0].page_content))
print("Chunk 1 metadata:", chunks[0].metadata)
print("--- Chunk 1 ---")
print(chunks[0].page_content)
print("--- Chunk 2 ---")
print(chunks[1].page_content)