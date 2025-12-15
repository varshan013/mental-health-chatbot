from pinecone import Pinecone
from app.config import (
    PINECONE_API_KEY,
    PINECONE_HOST,
    PINECONE_NAMESPACE,
    TOP_K
)

# Init Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(host=PINECONE_HOST)


def retrieve_context(query: str):
    # Embed query using Pinecone Inference
    embedding = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[query],
        parameters={"input_type": "query"}
    )[0]["values"]

    # Query Pinecone
    results = index.query(
        vector=embedding,
        top_k=TOP_K,
        include_metadata=True,
        namespace=PINECONE_NAMESPACE
    )

    contexts = []
    sources = []

    for match in results.get("matches", []):
        meta = match.get("metadata", {})
        text = meta.get("text", "")
        source = meta.get("source", "unknown")

        if text:
            contexts.append(text)
            sources.append({
                "source": source,
                "content": text
            })

    return contexts, sources
