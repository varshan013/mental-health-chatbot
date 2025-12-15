import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_text_splitters import RecursiveCharacterTextSplitter

from pathlib import Path
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

# ENV
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_HOST = os.getenv("PINECONE_HOST")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")


print("PINECONE_API_KEY:", "FOUND" if PINECONE_API_KEY else "MISSING")
print("PINECONE_HOST:", "FOUND" if PINECONE_HOST else "MISSING")
print("INDEX_NAME:", INDEX_NAME)

TEXT_DIR = "data/texts"
NAMESPACE = "mental_docs"

# Init Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(host=PINECONE_HOST)

# Text splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=120,
    length_function=len
)

def load_texts():
    docs = []
    for file in os.listdir(TEXT_DIR):
        if file.endswith(".txt"):
            path = os.path.join(TEXT_DIR, file)
            with open(path, "r", encoding="utf-8") as f:
                docs.append((file, f.read()))
    return docs


def embed_texts(texts):
    embeddings = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=texts,
        parameters={"input_type": "passage"}
    )
    return [e["values"] for e in embeddings]

def main():
    print("🚀 Starting ingestion...")

    documents = load_texts()
    print(f"📄 Loaded {len(documents)} text files")

    for filename, text in documents:
        chunks = splitter.split_text(text)
        print(f"➡️ {filename}: {len(chunks)} chunks")

        vectors = []
        embeddings = embed_texts(chunks)

        for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
            vectors.append({
                "id": f"{filename}-{i}",
                "values": emb,
                "metadata": {
                    "source": filename,
                    "chunk_id": i,
                    "text": chunk[:500]
                }
            })

        index.upsert(vectors=vectors, namespace=NAMESPACE)
        print(f"✅ Uploaded {filename}")

    print("\n🎉 INGESTION COMPLETE — Data is now in Pinecone!")


if __name__ == "__main__":
    main()
