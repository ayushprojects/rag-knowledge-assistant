from app.retrieval import retrieve

question = input("Your question: ")

for c in retrieve(question):
    print("")
    print(c["score"], "|", c["source"], "| page", c["page"])
    print(c["text"])