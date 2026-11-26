from app.clients import llm
from app.retrieval import retrieve


def answer_question(question):
    chunks = retrieve(question)

    if not chunks:
        return {"answer": "I could not find this in the documents.", "sources": []}

    context = ""
    for i in range(len(chunks)):
        context = context + f"[{i + 1}] {chunks[i]['text']}\n\n"

    prompt = f"""You are a helpful assistant.
Answer the question using ONLY the context below.
If the answer is not in the context, say: I could not find this in the documents.

Context:
{context}
Question: {question}"""

    response = llm.invoke(prompt)

    sources = []
    for c in chunks:
        sources.append({"source": c["source"], "page": c["page"]})

    return {"answer": response.content, "sources": sources}