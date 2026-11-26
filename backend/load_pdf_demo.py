from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("sample_docs/sample.pdf")
pages = loader.load()

print("Total pages:", len(pages))
print("Metadata:", pages[0].metadata)
print("Page 1 text:")
print(pages[0].page_content[:300])