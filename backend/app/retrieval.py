from app.clients import embeddings, index


def retrieve(question, top_k=3):
    q_vector = embeddings.embed_query(question)

    result = index.query(
        vector=q_vector,
        top_k=top_k,
        include_metadata=True,
        namespace="docs",
    )

    chunks = []
    for match in result.matches:
        chunks.append(
            {
                "text": match.metadata["text"],
                "source": match.metadata["source"],
                "page": int(match.metadata["page"]),
                "score": round(match.score, 3),
            }
        )
    return chunks